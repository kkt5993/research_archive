# -*- coding: utf-8 -*-
"""분류 정본(taxonomy.json)으로부터 폴더 트리와 루트 README를 생성한다.

사용법
    python _manifest/build_tree.py            # 폴더 생성 + README 갱신
    python _manifest/build_tree.py --readme   # README만 갱신
    python _manifest/build_tree.py --dry-run  # 무엇이 생기는지만 출력

분류를 바꾸려면 taxonomy.json만 고치고 다시 돌린다. 스크립트는 손대지 않는다.
기존 폴더와 문서는 지우지 않는다. 없는 것만 추가한다.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "_manifest" / "taxonomy.json"

BEGIN = "<!-- BEGIN:수록리포트 -->"
END = "<!-- END:수록리포트 -->"


def load_taxonomy() -> dict:
    with MANIFEST.open(encoding="utf-8") as fh:
        return json.load(fh)


def write_text(path: Path, text: str) -> None:
    """줄바꿈을 LF로 고정해서 쓴다.

    윈도우 기본값으로 쓰면 CRLF가 섞여 맥에서 돌릴 때마다 파일 전체가
    변경으로 잡힌다. 기기가 섞인 환경이라 여기서 못박아 둔다.
    """
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


# ---------------------------------------------------------------- 폴더 생성

def section_children(tax: dict, sec: dict) -> list[dict]:
    """섹션의 하위 항목을 {dir, label} 형태로 통일해 돌려준다.

    children 에 문자열을 적으면 이름이 곧 표시명이고,
    industry_set 을 적으면 industry_sets 에 정의된 목록을 그대로 끌어 쓴다.
    """
    key = sec.get("industry_set")
    if key:
        return list(tax["industry_sets"][key]["items"])
    out = []
    for child in sec.get("children", []):
        out.append(child if isinstance(child, dict) else {"dir": child, "label": child})
    return out


def iter_dirs(tax: dict):
    """생성해야 할 디렉터리 경로를 순서대로 내놓는다.

    두 층까지만 판다. 문서 성격은 폴더가 아니라 파일명 접미사로 구분하므로
    업종 아래에 다시 폴더를 만들지 않는다.
    """
    for sec in tax["sections"]:
        base = ROOT / sec["dir"]
        yield base
        if sec["type"] == "flat":
            continue
        for child in section_children(tax, sec):
            yield base / child["dir"]


DOC_TEMPLATE = """# {label} 기초자료

> (한 줄 요지를 여기에 적는다. README 색인이 이 줄을 가져간다.)

| 항목 | 값 |
|---|---|
| 시장 | {market} |
| 업종 | WI26 {code} {label} |
| 작성 기준일 | 미작성 |

## 1. 업종 정의와 범위

## 2. 수익 구조

## 3. 밸류체인

## 4. 경쟁 구도

## 5. 실적 변동 요인

## 6. 주요 상장 기업

## 7. 점검 지표

## 8. 용어

## 출처
"""


STRUCTURE_TEMPLATE = """# {label} 산업구조

> (한 줄 요지를 여기에 적는다. README 색인이 이 줄을 가져간다.)

| 항목 | 값 |
|---|---|
| 시장 | {market} |
| 업종 | {code} {label} |
| 작성 기준일 | 미작성 |

## 1. 이익이 고이는 지점

## 2. 가치사슬 단계별 교섭력

## 3. 진입 장벽의 실체

## 4. 사이클의 작동 방식

## 5. 구조를 바꾸는 힘

## 6. 무너질 수 있는 전제

## 출처
"""

COMPANY_TEMPLATE = """# {label} 기업분석

> (한 줄 요지를 여기에 적는다. README 색인이 이 줄을 가져간다.)

| 항목 | 값 |
|---|---|
| 시장 | {market} |
| 업종 | {code} {label} |
| 작성 기준일 | 미작성 |

## 1. 같은 업종인데 왜 갈리는가

## 2. 기업별 위치

## 3. 비교해야 할 항목

## 4. 함정

## 출처
"""

# 파일 접미사 -> 서식
DOC_KINDS = [
    ("기초자료", DOC_TEMPLATE),
    ("산업구조", STRUCTURE_TEMPLATE),
    ("기업분석", COMPANY_TEMPLATE),
]


def seed_industry_docs(tax: dict, dry_run: bool = False) -> int:
    """업종마다 성격별 문서를 하나씩 깔아 둔다. 이미 있으면 건드리지 않는다."""
    made = 0
    for sec in tax["sections"]:
        if sec["type"] != "industry":
            continue
        set_key = sec.get("industry_set", "")
        for child in section_children(tax, sec):
            code = child["dir"].split("_", 1)[0]
            slug = child["dir"].split("_", 1)[1]
            for suffix, tmpl in DOC_KINDS:
                target = ROOT / sec["dir"] / child["dir"] / f"{slug}_{suffix}.md"
                if target.exists():
                    continue
                made += 1
                if dry_run:
                    print(f"  + {target.relative_to(ROOT).as_posix()}")
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                write_text(target, tmpl.format(
                    label=child["label"], market=sec["title"],
                    code=f"{set_key} {code}".strip()))
    return made


def scaffold(tax: dict, dry_run: bool = False) -> int:
    created = 0
    for path in iter_dirs(tax):
        if path.exists():
            continue
        created += 1
        rel = path.relative_to(ROOT).as_posix()
        if dry_run:
            print(f"  + {rel}")
            continue
        path.mkdir(parents=True, exist_ok=True)
    return created


def prune_empty(tax: dict, dry_run: bool = False) -> int:
    """문서가 하나도 없는 디렉터리는 지운다.

    빈 폴더를 자리 표시용 파일로 붙잡아 두면 목록에 껍데기만 늘어난다.
    분류는 taxonomy.json 이 정본이므로 폴더가 사라져도 다시 만들면 된다.
    """
    removed = 0
    for path in sorted((p for p in ROOT.rglob("*") if p.is_dir()),
                       key=lambda p: len(p.parts), reverse=True):
        if ".git" in path.parts or path.name.startswith("_"):
            continue
        if any(path.iterdir()):
            continue
        removed += 1
        if dry_run:
            print(f"  - {path.relative_to(ROOT).as_posix()}")
            continue
        path.rmdir()
    return removed


# ---------------------------------------------------------------- README 생성

def git_last_date(path: Path) -> str:
    """마지막 커밋일. 저장소가 아니거나 미추적이면 파일 수정일로 대체한다."""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "log", "-1", "--format=%ad", "--date=short", "--", str(path)],
            capture_output=True, text=True, timeout=10,
        )
        stamp = out.stdout.strip()
        if stamp:
            return stamp
    except (OSError, subprocess.SubprocessError):
        pass
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")


SUMMARY_LIMIT = 110


def read_summary(path: Path) -> str:
    """문서 맨 앞의 인용 한 줄(> ...)을 한 줄 정의로 쓴다. 없으면 빈칸.

    옮겨온 문서는 이 자리에 머리말 전체를 적어 둔 것이 섞여 있다. 표가
    한 칸 때문에 늘어지지 않게 잘라 쓰고, 세로줄은 표를 깨므로 바꾼다.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            for _ in range(20):
                line = fh.readline()
                if not line:
                    break
                line = line.strip()
                if line.startswith(">"):
                    text = re.sub(r"\s+", " ", line.lstrip("> ").strip())
                    text = text.replace("|", "·")
                    if len(text) > SUMMARY_LIMIT:
                        text = text[:SUMMARY_LIMIT].rstrip() + "…"
                    return text
    except OSError:
        pass
    return ""


def docs_under(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted(
        (p for p in base.rglob("*.md") if p.name.upper() != "README.MD"),
        key=lambda p: p.relative_to(base).as_posix(),
    )


def build_index(tax: dict) -> str:
    lines: list[str] = []
    for sec in tax["sections"]:
        base = ROOT / sec["dir"]
        docs = docs_under(base)
        if not docs:
            continue
        lines.append(f"### {sec['title']}")
        lines.append("")
        lines.append(f"문서 {len(docs)}건")
        lines.append("")
        lines.append("| 위치 | 문서 | 요지 | 최종 수정 |")
        lines.append("|---|---|---|---|")
        for doc in docs:
            rel = doc.relative_to(ROOT).as_posix()
            href = "./" + rel
            title = doc.stem.replace("_", " ")
            branch = doc.parent.relative_to(base).as_posix() or "-"
            lines.append(f"| {branch} | [{title}]({href}) | {read_summary(doc)} | {git_last_date(doc)} |")
        lines.append("")
    if not lines:
        lines = ["수록된 문서가 없다. 문서를 넣고 스크립트를 다시 돌리면 채워진다.", ""]
    return "\n".join(lines).rstrip() + "\n"


def build_readme(tax: dict) -> str:
    repo = tax["repo"]
    kinds = repo["doc_kinds"]
    n_sec = len(tax["sections"])
    out: list[str] = []

    out.append(f"# {repo['title']}")
    out.append("")
    out.append(f"{repo['subtitle']}.")
    out.append("")
    out.append(f"디렉터리는 두 층까지만 내려간다. 첫 층이 자산군 {n_sec}개, "
               "둘째 층이 업종이다. 업종을 두지 않는 자산군은 첫 층에 문서를 바로 놓는다. "
               "문서 성격은 폴더가 아니라 파일명 접미사로 구분한다. "
               "폴더를 더 파면 문서 서너 개에 껍데기만 늘어나기 때문이다.")
    out.append("")

    out.append("## 운영 방식")
    out.append("")
    out.append("디렉터리를 손으로 만들지 않는다. 구성 명세는 "
               "[`_manifest/taxonomy.json`](./_manifest/taxonomy.json) 한 파일에 모아 두었고, "
               "명세를 고친 뒤 아래 명령을 실행하면 빠진 디렉터리가 채워지고 색인이 다시 계산된다. "
               "이미 있는 디렉터리와 문서는 그대로 둔다.")
    out.append("")
    out.append("```")
    out.append("python _manifest/build_tree.py")
    out.append("```")
    out.append("")

    out.append("## 자산군")
    out.append("")
    out.append("| 디렉터리 | 다루는 범위 |")
    out.append("|---|---|")
    for sec in tax["sections"]:
        out.append(f"| [`{sec['dir']}/`](./{sec['dir']}/) — {sec['title']} | {sec['desc']} |")
    out.append("")

    used_sets = []
    for sec in tax["sections"]:
        key = sec.get("industry_set")
        if key and key not in used_sets:
            used_sets.append(key)
    for key in used_sets:
        iset = tax["industry_sets"][key]
        users = [s["title"] for s in tax["sections"] if s.get("industry_set") == key]
        out.append(f"## 업종 구분 ({key})")
        out.append("")
        out.append(iset["note"])
        out.append("")
        out.append(f"적용 대상은 {', '.join(users)}이다. {iset['sanitized']}")
        out.append("")
        out.append("| 디렉터리 | 명칭 | 디렉터리 | 명칭 |")
        out.append("|---|---|---|---|")
        items = iset["items"]
        half = (len(items) + 1) // 2
        for left, right in zip(items[:half], items[half:] + [None] * half):
            row = f"| `{left['dir']}` | {left['label']} |"
            row += f" `{right['dir']}` | {right['label']} |" if right else "  |  |"
            out.append(row)
        out.append("")

    out.append("## 문서 성격 구분")
    out.append("")
    out.append("업종을 두는 자산군은 업종마다 아래 세 갈래를 기본으로 깔아 둔다. "
               "폴더가 아니라 파일명 끝에 붙는 말이다. "
               "어디에 넣을지 애매하면 조사 대상이 무엇인지로 판단한다. "
               "업종 자체면 두 번째, 특정 기업이면 세 번째다. "
               "이 세 갈래에 들어가지 않는 개별 조사는 접미사 없이 제목만으로 같은 폴더에 둔다.")
    out.append("")
    out.append("| 접미사 | 넣는 것 |")
    out.append("|---|---|")
    for kind in kinds:
        out.append(f"| `_{kind['suffix']}.md` | {kind['what']} |")
    out.append("")

    out.append("## 문서 색인")
    out.append("")
    out.append("아래는 실제 파일을 훑어 만든 것이다. 표를 직접 손보지 말고 스크립트를 다시 돌린다.")
    out.append("")
    out.append(BEGIN)
    out.append(build_index(tax))
    out.append(END)
    out.append("")

    out.append("## 작성 표준")
    out.append("")
    out.append("**파일명** 은 `주제_성격.md`로 붙인다. 기업 문서는 종목코드를 사이에 끼워 "
               "`기업명_005930_성격.md`로 쓴다. 내용을 크게 고칠 때는 덮어쓰지 않고 "
               "`_v2`를 붙여 새 파일을 만들고 이전 판을 남긴다.")
    out.append("")
    out.append("**첫머리** 에는 제목 다음 줄에 `> `로 시작하는 한 문장을 넣는다. "
               "위 색인이 이 문장을 요지 칸으로 가져간다.")
    out.append("")
    out.append("**그림** 은 문서와 같은 위치의 `img_주제/` 아래에 두고 `01_설명.png`처럼 번호를 앞세운다.")
    out.append("")
    out.append("**본문 구성** 은 세 덩어리로 잡는다. "
               "머리에는 결론과 그 근거를 먼저 적어 문서를 끝까지 읽지 않아도 요지가 잡히게 한다. "
               "가운데에는 조사 내용을 배치하되 대상 정의에서 출발해 수익 구조, 실적 흐름, 경쟁 환경, "
               "변수 순으로 좁혀 간다. 끝에는 위와 아래 시나리오를 각각의 전제와 함께 제시하고, "
               "앞으로 확인할 지표와 인용한 자료의 링크 목록으로 닫는다.")
    out.append("")
    out.append("**숫자** 는 기준일을 함께 적는다. 기준일 없는 수치는 넣지 않는다.")
    out.append("")

    out.append("## 면책")
    out.append("")
    out.append("여기 있는 글은 개인이 공부하며 남긴 조사 기록이다. "
               "매수나 매도를 권하는 문서가 아니며 어떤 성과도 보장하지 않는다.")
    out.append("")
    out.append("기재된 수치는 작성 시점에 확인한 값이고 이후 갱신되지 않는다. "
               "실제 판단에는 전자공시시스템과 EDGAR의 원문을 직접 확인해야 한다.")
    out.append("")
    out.append("작성자가 속한 기관의 견해와 무관하다. "
               "미공개 정보와 이용 계약으로 제한된 데이터의 가공물은 올리지 않는다.")
    out.append("")
    return "\n".join(out)


def write_readme(tax: dict, dry_run: bool = False) -> None:
    target = ROOT / "README.md"
    # README 는 전체가 생성물이다. 일부만 갈아끼우면 분류를 바꿔도 머리말이
    # 옛 내용 그대로 남아 실제 트리와 어긋난다. 매번 통째로 다시 쓴다.
    content = build_readme(tax)
    if dry_run:
        print(f"  ~ README.md ({len(content)} chars)")
        return
    write_text(target, content)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--readme", action="store_true", help="README만 갱신")
    ap.add_argument("--dry-run", action="store_true", help="변경 없이 계획만 출력")
    args = ap.parse_args()

    tax = load_taxonomy()

    if not args.readme:
        n = scaffold(tax, dry_run=args.dry_run)
        print(f"폴더 {n}개 {'생성 예정' if args.dry_run else '생성'}")
        d = seed_industry_docs(tax, dry_run=args.dry_run)
        print(f"업종 문서 {d}건 {'생성 예정' if args.dry_run else '생성'}")
        e = prune_empty(tax, dry_run=args.dry_run)
        print(f"빈 폴더 {e}개 {'삭제 예정' if args.dry_run else '삭제'}")

    write_readme(tax, dry_run=args.dry_run)
    print(f"README {'갱신 예정' if args.dry_run else '갱신'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
