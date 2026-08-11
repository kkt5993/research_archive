#!/usr/bin/env python3
"""
KRX 종가 수집 (로컬 전용)

클라우드에서는 Yahoo·네이버·Stooq가 모두 차단돼 있어 종목 시세를 받을 수 없다.
이 스크립트는 맥북/맥미니 로컬에서 pykrx로 KRX 공식 종가를 받아 CSV·JSON 으로
떨어뜨린다. 리포트 작성은 그 파일을 읽어서 클라우드가 한다.
(설계 배경: 90_정기발간/수급리뷰_운영메모.md 의 하이브리드 운영과 동일한 원칙)

원칙
  - 모든 수치는 KRX 공식 데이터. 계산은 결정론적 파이썬이 한다. LLM 산술 배제.
  - 실패한 종목은 지우지 않고 실패로 기록한다.
  - 액면분할·병합 의심 구간을 자동 표시한다(일간 급변 스캔).

사용법
  # 1) 저장소 문서에서 종목코드를 뽑아 수집
  python3 _scripts/종가_수집_로컬.py --from-docs 10_국내주식/22_반도체 --out 반도체

  # 2) 코드 목록 파일로 수집 (한 줄에 하나: 005930 또는 005930,삼성전자)
  python3 _scripts/종가_수집_로컬.py --codes codes.txt --out 내포트폴리오

  # 3) 코드 직접 지정 + 기간 지정
  python3 _scripts/종가_수집_로컬.py --code 005930 000660 --start 20260101 --out 메모리

  # 4) PER·PBR·배당까지 (KRX 계정 필요)
  KRX_ID=xxx KRX_PW=yyy python3 _scripts/종가_수집_로컬.py --from-docs 10_국내주식 --fundamental --out 전체

준비
  python3 -m venv ~/.venv/krx && ~/.venv/krx/bin/pip install pykrx
  ~/.venv/krx/bin/python _scripts/종가_수집_로컬.py ...
"""
from __future__ import annotations
import argparse, csv, json, os, re, sys, time
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUTDIR = REPO / "_manifest" / "데이터"

# 저장소 문서의 "종목명(123456)" 표기에서 코드를 뽑는다
NAMECODE = re.compile(r"([가-힣A-Za-z0-9㈜&.\-]{2,20})\s*[(（]\s*(\d{6})\s*[)）]")
# 국내 상장이 아닌 6자리(중국 A주 등)를 걸러내기 위한 최소 방어
NOT_KRX = {"601869"}


def eprint(*a):
    print(*a, file=sys.stderr)


def codes_from_docs(target: str) -> dict[str, str]:
    """저장소 문서에서 종목코드를 추출한다. target 은 파일 또는 디렉터리."""
    p = (REPO / target) if not Path(target).is_absolute() else Path(target)
    files = [p] if p.is_file() else sorted(p.rglob("*.md"))
    found: dict[str, str] = {}
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for name, code in NAMECODE.findall(text):
            if code in NOT_KRX:
                continue
            found.setdefault(code, name.strip("㈜ "))
    return found


def codes_from_file(path: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [x.strip() for x in line.replace("\t", ",").split(",")]
        code = parts[0]
        if re.fullmatch(r"\d{6}", code):
            out[code] = parts[1] if len(parts) > 1 and parts[1] else ""
    return out


def fetch(codes: dict[str, str], start: str, end: str, delay: float,
          retries: int, want_fundamental: bool):
    from pykrx import stock

    ok: dict[str, dict] = {}
    failed: list[tuple[str, str, str]] = []
    total = len(codes)

    for i, (code, name) in enumerate(sorted(codes.items()), 1):
        df = None
        last_err = ""
        for attempt in range(retries):
            try:
                df = stock.get_market_ohlcv(start, end, code)
                if df is not None and len(df) > 0:
                    break
                last_err = "empty"
            except Exception as e:
                last_err = f"{type(e).__name__}: {e}"
                time.sleep(delay * (attempt + 2))
        if df is None or len(df) == 0:
            failed.append((code, name, last_err or "empty"))
            eprint(f"  [{i}/{total}] 실패 {code} {name} — {last_err or 'empty'}")
            time.sleep(delay)
            continue

        df = df[df["종가"] > 0]
        if len(df) == 0:
            failed.append((code, name, "all-zero"))
            time.sleep(delay)
            continue

        closes = df["종가"]
        # 액면분할·병합 의심: 하루 -40% 이하 또는 +60% 이상
        chg = closes.pct_change()
        suspects = [
            {"date": str(d.date()), "pct": round(float(v) * 100, 1)}
            for d, v in chg.items() if v is not None and (v <= -0.40 or v >= 0.60)
        ]

        rec = {
            "name": name or stock.get_market_ticker_name(code),
            "start": str(df.index[0].date()),
            "last_date": str(df.index[-1].date()),
            "last_close": int(closes.iloc[-1]),
            "high": int(closes.max()), "high_date": str(closes.idxmax().date()),
            "low": int(closes.min()),  "low_date": str(closes.idxmin().date()),
            "monthly": {d.strftime("%Y-%m"): int(v)
                        for d, v in closes.resample("ME").last().items()},
            "split_suspect": suspects,
        }

        if want_fundamental:
            try:
                fd = stock.get_market_fundamental(start, end, code)
                if fd is not None and len(fd) > 0:
                    last = fd.iloc[-1]
                    rec["fundamental"] = {
                        k: (None if str(last.get(k, "")) in ("", "nan") else float(last[k]))
                        for k in ("BPS", "PER", "PBR", "EPS", "DIV", "DPS") if k in fd.columns
                    }
                    rec["fundamental_date"] = str(fd.index[-1].date())
                else:
                    rec["fundamental_error"] = "empty (KRX 로그인 필요)"
            except Exception as e:
                rec["fundamental_error"] = f"{type(e).__name__}"

        ok[code] = rec
        if i % 25 == 0 or i == total:
            eprint(f"  진행 {i}/{total}")
        time.sleep(delay)

    return ok, failed


def write_outputs(ok: dict, failed: list, tag: str, start: str, end: str, want_fundamental: bool):
    OUTDIR.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    base = f"{tag}_{stamp}"

    (OUTDIR / f"{base}.json").write_text(
        json.dumps({
            "수집시각": datetime.now().isoformat(timespec="seconds"),
            "기간": {"start": start, "end": end},
            "종목수": len(ok), "실패": [{"code": c, "name": n, "reason": r} for c, n, r in failed],
            "데이터": ok,
        }, ensure_ascii=False, indent=1), encoding="utf-8")

    months = sorted({m for r in ok.values() for m in r["monthly"]})
    cols = ["종목명", "종목코드", "최종일", "종가", "기간고가", "고가일", "기간저가", "저가일"] \
        + [f"{m}말" for m in months] + ["분할의심"]
    if want_fundamental:
        cols += ["PER", "PBR", "EPS", "BPS", "DIV", "DPS", "지표일"]

    rows = []
    for code, r in sorted(ok.items(), key=lambda kv: kv[1]["name"]):
        row = {
            "종목명": r["name"], "종목코드": code, "최종일": r["last_date"],
            "종가": r["last_close"], "기간고가": r["high"], "고가일": r["high_date"],
            "기간저가": r["low"], "저가일": r["low_date"],
            "분할의심": "; ".join(f"{s['date']} {s['pct']:+}%" for s in r["split_suspect"]),
        }
        for m in months:
            row[f"{m}말"] = r["monthly"].get(m, "")
        if want_fundamental:
            f = r.get("fundamental", {})
            for k in ("PER", "PBR", "EPS", "BPS", "DIV", "DPS"):
                row[k] = f.get(k, "")
            row["지표일"] = r.get("fundamental_date", r.get("fundamental_error", ""))
        rows.append(row)

    # 엑셀에서 한글이 깨지지 않도록 UTF-8 BOM
    with (OUTDIR / f"{base}.csv").open("w", newline="", encoding="utf-8-sig") as fp:
        w = csv.DictWriter(fp, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    return OUTDIR / f"{base}.csv", OUTDIR / f"{base}.json"


def main():
    ap = argparse.ArgumentParser(description="KRX 종가 수집 (로컬 전용)")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--from-docs", metavar="경로", help="저장소 문서에서 종목코드 추출 (파일 또는 디렉터리)")
    src.add_argument("--codes", metavar="파일", help="종목코드 목록 파일")
    src.add_argument("--code", nargs="+", metavar="코드", help="종목코드 직접 지정")
    ap.add_argument("--start", default="20260101", help="시작일 YYYYMMDD (기본 20260101)")
    ap.add_argument("--end", default=date.today().strftime("%Y%m%d"), help="종료일 YYYYMMDD (기본 오늘)")
    ap.add_argument("--out", default="종가", help="출력 파일 접두어 (기본 '종가')")
    ap.add_argument("--delay", type=float, default=0.35, help="종목 간 대기 초 (기본 0.35)")
    ap.add_argument("--retries", type=int, default=3, help="종목별 재시도 횟수 (기본 3)")
    ap.add_argument("--fundamental", action="store_true", help="PER·PBR·배당도 수집 (KRX_ID/KRX_PW 필요)")
    a = ap.parse_args()

    try:
        import pykrx  # noqa: F401
    except ImportError:
        eprint("pykrx 가 없다. 설치:\n"
               "  python3 -m venv ~/.venv/krx && ~/.venv/krx/bin/pip install pykrx\n"
               "  ~/.venv/krx/bin/python _scripts/종가_수집_로컬.py ...")
        sys.exit(1)

    if a.fundamental and not (os.getenv("KRX_ID") and os.getenv("KRX_PW")):
        eprint("주의: --fundamental 은 KRX_ID/KRX_PW 환경변수가 필요하다. "
               "없으면 PER·PBR 열이 비고 가격만 수집된다.")

    if a.from_docs:
        codes = codes_from_docs(a.from_docs)
        eprint(f"문서에서 {len(codes)}종목 추출: {a.from_docs}")
    elif a.codes:
        codes = codes_from_file(a.codes)
        eprint(f"파일에서 {len(codes)}종목 로드")
    else:
        codes = {c: "" for c in a.code if re.fullmatch(r"\d{6}", c)}

    if not codes:
        eprint("수집할 종목이 없다."); sys.exit(1)

    eprint(f"수집 시작: {a.start}–{a.end}, {len(codes)}종목")
    ok, failed = fetch(codes, a.start, a.end, a.delay, a.retries, a.fundamental)
    csv_path, json_path = write_outputs(ok, failed, a.out, a.start, a.end, a.fundamental)

    eprint(f"\n성공 {len(ok)} / 실패 {len(failed)}")
    for c, n, r in failed:
        eprint(f"  실패: {c} {n} — {r}")
    susp = {c: r["split_suspect"] for c, r in ok.items() if r["split_suspect"]}
    if susp:
        eprint(f"\n분할·병합 의심 {len(susp)}종목 (CSV '분할의심' 열 확인):")
        for c, s in list(susp.items())[:10]:
            eprint(f"  {c} {ok[c]['name']}: " + ", ".join(f"{x['date']} {x['pct']:+}%" for x in s))
    print(csv_path)
    print(json_path)


if __name__ == "__main__":
    main()
