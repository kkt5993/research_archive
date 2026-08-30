#!/usr/bin/env python3
"""
종목 → WI26 대분류 배정 (26개 저장소 폴더)

**축은 하나다 — WI26.** 맥미니 PG `research.sector_map` 이 그 축이고, 그 테이블은
미니의 `build_sector_map.py`·`load_qw_consensus.py` 가 QuantiWise WI26 으로 채운다.
아카이브가 따로 규칙을 만들지 않는다. 만들면 데이터와 문서가 다른 기준으로 묶인다.

배정 순서
  1. `sector_map.sector_source='wi26'` 인 행 → 그 값이 곧 WI26 대분류다.
  2. 그 외(naver_mapped·미커버·미분류) → 종목의 **WICS 산업**을 1번 행들에서 뽑은
     `WICS 산업 → WI26` 다수결 표로 접는다. 이 표는 wi26 소스 2,596행에서 유도했고
     78개 산업 전부 만장일치였다(갈린 산업 0).
  3. 그래도 안 되면 '미분류' 로 남긴다. 억지로 밀어넣지 않는다.

2번이 필요한 이유: `sector_map` 의 naver_mapped 행은 손으로 쓴 `TO_WICS` 표로 접힌
것이라 QuantiWise 실제 WI26 과 6개 산업에서 어긋난다(전기장비·포장재·가구·전자제품·
가정용기기와용품·양방향미디어와서비스). 어긋난 채 두면 LG전자는 IT가전, LG전자우는
IT하드웨어로 갈라진다 — 실제로 그랬다.

산출: _manifest/데이터/업종_WI26_유니버스_<날짜>.csv
      code,name,market,wi26,dir,wics,source,k200,prev_dir
"""
from __future__ import annotations
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "_manifest" / "데이터"
ROOT = REPO / "10_국내주식"
STAMP = "2026-08-30"

sm = json.loads((DATA / f"업종_WI26_sector_map_{STAMP}.json").read_text(encoding="utf-8"))
quote = {r["code"]: r for r in csv.DictReader((DATA / f"국내주식_시세컨센_{STAMP}.csv").open(encoding="utf-8"))}
k200 = {r["code"] for r in csv.DictReader((DATA / f"코스피200_구성종목_{STAMP}.csv").open(encoding="utf-8"))}
prev = {r["종목코드"]: r["저장소폴더"] for r in
        csv.DictReader((DATA / "컨센서스_목표가_2026-08-11.csv").open(encoding="utf-8-sig"))}

# ── WICS 산업 → WI26 대분류 (wi26 소스 행에서 유도) ────────────────────────
tab = defaultdict(Counter)
for v in sm.values():
    if v["src"] == "wi26" and v["detail"] and v["wi26"] != "미분류":
        tab[v["detail"]][v["wi26"]] += 1
FOLD = {k: c.most_common(1)[0][0] for k, c in tab.items()}
SPLIT = {k: dict(c) for k, c in tab.items() if len(c) > 1}   # 갈린 산업이 있으면 드러낸다

norm = lambda s: re.sub(r"[,()\s]", "", s)
DIRS = [p.name for p in sorted(ROOT.iterdir()) if p.is_dir()]
W2D = {norm(d.split("_", 1)[1]): d for d in DIRS}


def main() -> int:
    rows, unresolved = [], []
    for code, q in quote.items():
        e = sm.get(code) or {}
        wi, src, how = e.get("wi26"), e.get("src"), "PG sector_map(wi26)"
        if not (src == "wi26" and wi and wi != "미분류"):
            det = q["wics"] or e.get("detail")
            folded = FOLD.get(det)
            wi, how = (folded, f"WICS '{det}' → WI26 다수결") if folded else (None, "불가")
        if not wi or norm(wi) not in W2D:
            unresolved.append((code, q["name"], q["wics"], wi))
            continue
        rows.append({"code": code, "name": q["name"], "market": q.get("market") or "",
                     "wi26": wi, "dir": W2D[norm(wi)],
                     "wics": q["wics"] or e.get("detail") or "", "source": how,
                     "k200": "1" if code in k200 else "", "prev_dir": prev.get(code, "")})
    rows.sort(key=lambda r: (r["dir"], -(float(quote[r["code"]]["mktcap_억"] or 0))))
    p = DATA / f"업종_WI26_유니버스_{STAMP}.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["code", "name", "market", "wi26", "dir", "wics",
                                          "source", "k200", "prev_dir"])
        w.writeheader(); w.writerows(rows)
    moved = [r for r in rows if r["prev_dir"] and r["prev_dir"] != r["dir"]]
    print(f"{len(rows)}종목 배정 → {p}")
    print(f"  K200 {sum(1 for r in rows if r['k200'])} · 이전 판과 폴더가 달라진 종목 {len(moved)}")
    print(f"  WICS 다수결로 접은 종목 {sum(1 for r in rows if r['source'] != 'PG sector_map(wi26)')}")
    if SPLIT:
        print(f"  ⚠ WICS→WI26 이 갈린 산업: {SPLIT}", file=sys.stderr)
    if unresolved:
        print(f"  ⚠ 배정 불가 {len(unresolved)}: {unresolved}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
