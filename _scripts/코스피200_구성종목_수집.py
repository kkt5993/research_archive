#!/usr/bin/env python3
"""
코스피200 구성종목 수집 (로컬 전용)

KRX 공식 API(data.krx.co.kr)는 이 환경에서 403 이라 네이버 금융의
'코스피200 편입종목' 목록(finance.naver.com/sise/entryJongmok.naver)에서 받는다.
목록 자체가 거래소 지수 편입 종목이므로 구성은 KRX 와 같다.

산출: _manifest/데이터/코스피200_구성종목_<날짜>.{csv,json}
      code,name,price,mktcap_억

원칙 (_scripts/README.md 와 동일)
  - 사람이 손으로 넣지 않는다. 수집은 스크립트가 한다.
  - 실패한 페이지는 지우지 않고 실패로 기록한다.
"""
from __future__ import annotations
import csv, json, re, sys, time, urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUTDIR = REPO / "_manifest" / "데이터"
URL = "https://finance.naver.com/sise/entryJongmok.naver?&page={}"
UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://finance.naver.com/sise/"}
ROW = re.compile(
    r'/item/main\.naver\?code=([0-9A-Z]{6})"[^>]*>([^<]+)</a>.*?'
    r'class="number_2">([\d,]+)</td>',
    re.S,
)
MCAP = re.compile(r'class="number_2">([\d,]+)</td>\s*</tr>', re.S)


def fetch(page: int) -> str:
    req = urllib.request.Request(URL.format(page), headers=UA)
    return urllib.request.urlopen(req, timeout=20).read().decode("euc-kr", "replace")


def main() -> int:
    out, failed, seen = [], [], set()
    for page in range(1, 26):
        try:
            html = fetch(page)
        except Exception as e:                      # 실패는 실패로 남긴다
            failed.append((page, repr(e)))
            continue
        blocks = re.findall(r"<tr>\s*<td class=\"ctg\">.*?</tr>", html, re.S)
        if not blocks:
            break
        for b in blocks:
            m = re.search(r'code=([0-9A-Z]{6})"[^>]*>([^<]+)</a>', b)
            if not m:
                continue
            code, name = m.group(1), m.group(2).strip()
            if code in seen:
                continue
            nums = re.findall(r'class="number_2">\s*([\d,]+)\s*</td>', b)
            price = int(nums[0].replace(",", "")) if nums else None
            mcap = int(nums[-1].replace(",", "")) if len(nums) >= 2 else None
            seen.add(code)
            out.append({"code": code, "name": name, "price": price, "mktcap_억": mcap})
        time.sleep(0.4)

    today = date.today().isoformat()
    OUTDIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTDIR / f"코스피200_구성종목_{today}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["code", "name", "price", "mktcap_억"])
        w.writeheader()
        w.writerows(out)
    (OUTDIR / f"코스피200_구성종목_{today}.json").write_text(
        json.dumps({"as_of": today, "source": "naver:entryJongmok",
                    "count": len(out), "failed_pages": failed, "rows": out},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out)}종목 → {csv_path}")
    if failed:
        print("실패 페이지:", failed, file=sys.stderr)
    return 0 if out else 1


if __name__ == "__main__":
    raise SystemExit(main())
