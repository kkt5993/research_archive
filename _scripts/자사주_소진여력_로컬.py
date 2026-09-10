#!/usr/bin/env python3
"""
자사주 매입 소진 여력 재계산 (로컬 전용)

삼성전자·SK하이닉스처럼 장내 **직접취득** 하는 회사의 매수는 KRX 투자자별 통계에서
'기타법인' 으로 잡힌다. 이 스크립트는 종목별 기타법인 순매수(금액·주식수)와 종가를
pykrx 로 받아, 공시된 취득예정주식수·금액 대비 집행률과 잔여, 지금 속도로의 소진 예상일을
결정론적으로 계산한다. 클라우드는 KRX 가 차단돼 있으니 맥북/맥미니에서 돌리고 결과 CSV 를 커밋한다.

  ~/.venv/krx/bin/python _scripts/자사주_소진여력_로컬.py                # 오늘까지
  ~/.venv/krx/bin/python _scripts/자사주_소진여력_로컬.py --end 20261019

원칙
  - 수치는 KRX 공식 데이터. 계산은 파이썬. LLM 산술 배제.
  - 기타법인 = 회사 매수 라는 등식은 이 두 종목처럼 직접취득이고 다른 기타법인 매매가 없을 때만 성립한다.
    다른 종목에 쓰려면 PLANS 에 추가하되 그 전제를 먼저 확인할 것.
  - 잔여 주식수는 '공시 예정주식수 − 기타법인 누적 순매수 주식수' 다. 금액은 참고치(결의 전일 종가 환산).
"""
from __future__ import annotations
import argparse, csv, json, sys, time
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUTDIR = REPO / "_manifest" / "데이터"

# DART 주요사항보고서(자기주식취득결정) 조건. 금액은 결의 전일 종가 환산치(참고).
PLANS = [
    dict(code="000660", name="SK하이닉스", start="20260820", end="20261119",
         shares=24_070_000, amount=40_004_340_000_000, daily_cap=2_407_000,
         purpose="소각", rcp="20260819000254"),
    dict(code="005930", name="삼성전자", start="20260824", end="20261121",
         shares=53_285_968, amount=53_285_968 * 281_500, daily_cap=7_321_653,
         purpose="임직원 성과급", rcp="20260821000616"),
]

# 2026 하반기 거래소 휴장일(평일만). 추석 9/24·25, 대체휴일 9/28, 개천절 대체 10/5, 한글날 10/9, 성탄 12/25.
HOLIDAYS = {date(2026, 9, 24), date(2026, 9, 25), date(2026, 9, 28),
            date(2026, 10, 5), date(2026, 10, 9), date(2026, 12, 25)}


def eprint(*a):
    print(*a, file=sys.stderr)


def is_tday(d: date) -> bool:
    return d.weekday() < 5 and d not in HOLIDAYS


def add_tdays(start: date, n: int) -> date:
    """start 다음 거래일부터 세어 n번째 거래일."""
    d, c = start, 0
    while c < n:
        d += timedelta(1)
        if is_tday(d):
            c += 1
    return d


def tdays_between(a: date, b: date) -> int:
    d, c = a, 0
    while d <= b:
        if is_tday(d):
            c += 1
        d += timedelta(1)
    return c


def fetch(code: str, start: str, end: str, retries: int = 3):
    from pykrx import stock
    for i in range(retries):
        try:
            val = stock.get_market_trading_value_by_date(start, end, code, on="순매수")
            vol = stock.get_market_trading_volume_by_date(start, end, code, on="순매수")
            px = stock.get_market_ohlcv_by_date(start, end, code)
            return val, vol, px
        except Exception as e:  # noqa: BLE001
            eprint(f"  {code} 재시도 {i+1}/{retries}: {e}")
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"{code} 수집 실패")


def analyze(plan: dict, end: str, pace_days: int) -> tuple[dict, list[dict]]:
    val, vol, px = fetch(plan["code"], plan["start"], end)
    if "기타법인" not in val.columns:
        raise RuntimeError(f"{plan['code']} 기타법인 열이 없다: {list(val.columns)}")
    rows = []
    cum_won = cum_sh = 0
    for d in val.index:
        won = int(val.loc[d, "기타법인"])
        sh = int(vol.loc[d, "기타법인"]) if d in vol.index else 0
        close = int(px.loc[d, "종가"]) if d in px.index else 0
        cum_won += won
        cum_sh += sh
        rows.append(dict(code=plan["code"], name=plan["name"], date=d.strftime("%Y-%m-%d"),
                         close=close, other_corp_won=won, other_corp_shares=sh,
                         cum_won=cum_won, cum_shares=cum_sh))
    if not rows:
        raise RuntimeError(f"{plan['code']} 데이터 없음")
    last = rows[-1]
    last_close = last["close"]
    rem_sh = plan["shares"] - cum_sh
    recent = rows[-pace_days:]
    pace_sh = sum(r["other_corp_shares"] for r in recent) / len(recent)
    days_left = (rem_sh / pace_sh) if pace_sh > 0 else float("inf")
    last_d = datetime.strptime(last["date"], "%Y-%m-%d").date()
    end_d = datetime.strptime(plan["end"], "%Y%m%d").date()
    exhaust = add_tdays(last_d, int(-(-days_left // 1))) if pace_sh > 0 else None
    summary = dict(
        code=plan["code"], name=plan["name"], purpose=plan["purpose"], rcp=plan["rcp"],
        as_of=last["date"], last_close=last_close,
        plan_shares=plan["shares"], plan_amount=plan["amount"],
        cum_shares=cum_sh, cum_won=cum_won,
        progress_shares=round(cum_sh / plan["shares"], 4),
        progress_won=round(cum_won / plan["amount"], 4),
        avg_price=round(cum_won / cum_sh) if cum_sh else None,
        remaining_shares=rem_sh,
        remaining_won_plan=plan["amount"] - cum_won,
        remaining_won_at_close=rem_sh * last_close,
        pace_shares_per_day=round(pace_sh),
        pace_won_per_day_at_close=round(pace_sh * last_close),
        pace_vs_daily_cap=round(pace_sh / plan["daily_cap"], 3),
        tdays_to_exhaust=round(days_left, 1) if pace_sh > 0 else None,
        exhaust_date=exhaust.isoformat() if exhaust else None,
        tdays_to_plan_end=tdays_between(last_d + timedelta(1), end_d),
        plan_end=end_d.isoformat(),
    )
    return summary, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--end", default=date.today().strftime("%Y%m%d"))
    ap.add_argument("--pace-days", type=int, default=5, help="소진 속도 산정에 쓰는 최근 거래일 수")
    ap.add_argument("--out", default="자사주_소진여력")
    a = ap.parse_args()

    OUTDIR.mkdir(parents=True, exist_ok=True)
    summaries, daily = [], []
    for p in PLANS:
        eprint(f"{p['name']}({p['code']}) {p['start']}–{a.end}")
        s, rows = analyze(p, a.end, a.pace_days)
        summaries.append(s)
        daily.extend(rows)
        time.sleep(0.5)

    tag = a.end[:4] + "-" + a.end[4:6] + "-" + a.end[6:]
    csv_path = OUTDIR / f"{a.out}_{tag}.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(daily[0].keys()))
        w.writeheader()
        w.writerows(daily)
    json_path = OUTDIR / f"{a.out}_{tag}.json"
    json_path.write_text(json.dumps(dict(collected_at=datetime.now().isoformat(timespec="seconds"),
                                         summary=summaries), ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"| 종목 | 기준일 | 종가 | 집행 주식수 | 집행률(주식) | 집행 금액 | 잔여 주식수 | 잔여(종가환산) | 속도/일 | 소진 예상 | 공시 종료 |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|")
    for s in summaries:
        print(f"| {s['name']} | {s['as_of']} | {s['last_close']:,} | {s['cum_shares']:,} | {s['progress_shares']:.1%} | "
              f"{s['cum_won']/1e12:.2f}조 | {s['remaining_shares']:,} | {s['remaining_won_at_close']/1e12:.2f}조 | "
              f"{s['pace_shares_per_day']:,} | {s['exhaust_date']} ({s['tdays_to_exhaust']}일) | {s['plan_end']} ({s['tdays_to_plan_end']}일) |")
    eprint(f"→ {csv_path}\n→ {json_path}")


if __name__ == "__main__":
    main()
