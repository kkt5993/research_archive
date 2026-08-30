#!/usr/bin/env python3
"""
네이버 금융 종목 시세·컨센서스 수집 (로컬 전용)

KRX 공식 API 는 이 환경에서 403 이고 pykrx 도 같은 이유로 막혔다. 종가·시총·
후행/선행 PER·컨센 EPS 는 네이버 종목 통합 API 에서 받는다.

  python3 _scripts/네이버_시세컨센_수집.py --codes 034020 012450 --out 기계
  python3 _scripts/네이버_시세컨센_수집.py --codes-file /tmp/codes.txt --out 기계

산출: _manifest/데이터/<접두어>_시세컨센_<날짜>.{csv,json}
실패한 종목은 지우지 않고 error 로 남긴다.
"""
from __future__ import annotations
import argparse, csv, json, re, sys, time, urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUTDIR = REPO / "_manifest" / "데이터"
API = "https://m.stock.naver.com/api/stock/{}/integration"
UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://m.stock.naver.com/"}
SISE = ("https://api.finance.naver.com/siseJson.naver?symbol={}&requestType=1"
        "&startTime={}&endTime={}&timeframe=day")
ITEM = "https://finance.naver.com/item/main.naver?code={}"
FIELDS = ["code", "name", "market", "wics", "trade_date", "close", "mktcap_억", "per", "eps",
          "cns_per", "cns_eps", "pbr", "bps", "foreign_pct", "hi52", "lo52", "error"]


def num(s):
    if s in (None, "", "N/A"):
        return None
    s = str(s).replace(",", "").replace("배", "").replace("%", "").replace("원", "")
    try:
        return float(s)
    except ValueError:
        return None


def mktcap_억(s):
    """'56조 4,975억' → 564975 (억원)"""
    if not s or s == "N/A":
        return None
    s = s.replace(",", "").strip()
    tot, cur = 0, ""
    for ch in s:
        if ch.isdigit():
            cur += ch
        elif ch == "조":
            tot += int(cur or 0) * 10000; cur = ""
        elif ch == "억":
            tot += int(cur or 0); cur = ""
    if cur:
        tot += int(cur)
    return tot


def last_close(code: str, days: int = 20):
    """m.stock 의 lastClosePrice 는 *전일* 종가다. 실제 최종 거래일 종가는 일별 시세로 받는다."""
    end = date.today().strftime("%Y%m%d")
    start = (date.today() - __import__("datetime").timedelta(days=days)).strftime("%Y%m%d")
    req = urllib.request.Request(SISE.format(code, start, end), headers=UA)
    txt = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
    rows = json.loads(txt.replace("'", '"'))
    if len(rows) < 2:
        return None, None
    d, *_ , = rows[-1]
    return f"{d[:4]}-{d[4:6]}-{d[6:]}", float(rows[-1][4])


def item_page(code: str):
    """네이버 종목 페이지에서 **시장(코스피/코스닥)** 과 **WICS 산업**을 한 번에 뽑는다.

    이 페이지는 **UTF-8** 이다. 목록 페이지(entryJongmok)가 EUC-KR 이라고 같은 인코딩으로
    읽으면 업종명이 통째로 깨진다 — 그렇게 읽은 '복합기업' 을 '복합기계' 로 잘못 읽어
    한화머시너리앤서비스홀딩스를 기계로 분류한 적이 있다. meta charset 을 보고 정한다.
    """
    raw = urllib.request.urlopen(urllib.request.Request(ITEM.format(code), headers=UA), timeout=20).read()
    cs = re.search(rb"charset=([\w-]+)", raw[:2000])
    h = raw.decode(cs.group(1).decode() if cs else "euc-kr", "replace")
    up = re.search(r"sise_group_detail\.naver\?type=upjong[^>]*>([^<]+)</a>", h, re.S)
    # 시장 배지. 우선주·리츠·인프라펀드처럼 원장에 시장 정보가 없는 종목도 여기서 나온다.
    mk = re.search(r'class="description">.*?<img[^>]*alt="(코스피|코스닥)"', h, re.S)
    return ({"코스피": "KOSPI", "코스닥": "KOSDAQ"}.get(mk.group(1)) if mk else None,
            up.group(1).strip() if up else None)


def fetch(code: str) -> dict:
    req = urllib.request.Request(API.format(code), headers=UA)
    j = json.loads(urllib.request.urlopen(req, timeout=20).read())
    t = {x["code"]: x["value"] for x in j.get("totalInfos", [])}
    td, close = last_close(code)
    market, sector = item_page(code)
    return {"code": code, "name": j.get("stockName"), "market": market, "wics": sector, "trade_date": td,
            "close": close, "mktcap_억": mktcap_억(t.get("marketValue")),
            "per": num(t.get("per")), "eps": num(t.get("eps")),
            "cns_per": num(t.get("cnsPer")), "cns_eps": num(t.get("cnsEps")),
            "pbr": num(t.get("pbr")), "bps": num(t.get("bps")),
            "foreign_pct": num(t.get("foreignRate")),
            "hi52": num(t.get("highPriceOf52Weeks")), "lo52": num(t.get("lowPriceOf52Weeks")),
            "error": None}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--codes", nargs="*", default=[])
    ap.add_argument("--codes-file")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    codes = list(a.codes)
    if a.codes_file:
        codes += [l.split(",")[0].strip() for l in open(a.codes_file, encoding="utf-8") if l.strip()]
    codes = list(dict.fromkeys(codes))

    rows = []
    for i, c in enumerate(codes, 1):
        try:
            rows.append(fetch(c))
        except Exception as e:
            rows.append({**{k: None for k in FIELDS}, "code": c, "error": repr(e)})
            print(f"  실패 {c}: {e}", file=sys.stderr)
        time.sleep(0.3)
        if i % 10 == 0:
            print(f"  {i}/{len(codes)}", file=sys.stderr)

    today = date.today().isoformat()
    OUTDIR.mkdir(parents=True, exist_ok=True)
    p = OUTDIR / f"{a.out}_시세컨센_{today}.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    (OUTDIR / f"{a.out}_시세컨센_{today}.json").write_text(
        json.dumps({"as_of": today, "source": "naver:m.stock integration",
                    "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(1 for r in rows if r["error"] is None)
    print(f"{ok}/{len(rows)}종목 → {p}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
