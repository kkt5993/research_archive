# -*- coding: utf-8 -*-
"""조선 11종목 — 원장 10월 리포트 × KRX 종가 × 공개 보도치 대조 (2026-10-21).

입력(전부 _manifest/데이터):
  조선_원장리포트_2026-09-01_10-21.json  맥미니 원장 reports·report_estimates 추출(읽기 전용 사본)
  조선_2026-10-21.json                   KRX 종가(_scripts/종가_수집_로컬.py)
  조선_일별종가_2026-10-15_10-21.json     pykrx 일별 종가
출력: 조선_원장대조_2026-10-21.json + 표준출력 요약. 산술은 전부 여기서 한다.
"""
import json, statistics, os

D = os.path.join(os.path.dirname(__file__), "..", "_manifest", "데이터")
rep = json.load(open(f"{D}/조선_원장리포트_2026-09-01_10-21.json"))
krx = json.load(open(f"{D}/조선_2026-10-21.json"))["데이터"]
cons = {r["code"]: r for r in json.load(open(f"{D}/조선_원장컨센_2026-10-21.json"))["rows"]}
daily = json.load(open(f"{D}/조선_일별종가_2026-10-15_10-21.json"))

NAME = {"329180": "HD현대중공업", "042660": "한화오션", "009540": "HD한국조선해양", "010140": "삼성중공업",
        "267250": "HD현대", "443060": "HD현대마린솔루션", "082740": "한화엔진", "439260": "대한조선",
        "071970": "HD현대마린엔진", "017960": "한국카본", "077970": "STX엔진"}
# 8/28 원장 표(이전 스냅샷)의 종가·목표가
C0828 = {"329180": 457000, "042660": 88500, "009540": 354500, "010140": 21200, "267250": 218000,
         "443060": 221000, "082740": 48250, "439260": 49000, "071970": 53100, "017960": 24950, "077970": 25300}
TP0828 = {"329180": 880000, "042660": 140000, "009540": 620000, "010140": 40000, "267250": 350000,
          "443060": 340000, "082740": 95000, "439260": 118000, "071970": 96000, "017960": 50000, "077970": 75500}
SHORT = {"NH투자증권": "NH", "IBK투자증권": "IBK", "SK증권": "SK", "상상인증권": "상상인", "키움증권": "키움",
         "현대차증권": "현대차", "DB증권": "DB", "다올투자증권": "다올", "DS투자증권": "DS", "유안타증권": "유안타",
         "하나증권": "하나", "삼성증권": "삼성", "미래에셋증권": "미래에셋", "LS증권": "LS"}
# 텔레그램 companyreport 요약(증권사 칸 없음) 본문에서 읽은 3Q26 영업이익(억원). 본문 연간치는 단위가 깨져 쓰지 않는다.
TG_PREV = {("082740", "2026-10-08"): 103000}  # 본문 "기존 103,000원에서 하향"
TG_3Q = {("010140", "2026-10-12"): 3398, ("082740", "2026-10-08"): 542, ("071970", "2026-10-12"): 448}
# 원장 report_estimates 에 3Q 칸이 없는 리포트 — 같은 리포트의 텔레그램 요약(reportsnow 10/18, 상상인 이서연) 본문에 적힌 3Q26 영업이익(억원)
BODY_3Q = {("329180", "상상인"): 9161, ("042660", "상상인"): 5088}
# 원장에 없고 공개 보도로만 확인된 10월 리포트 (목표가, 3Q 영업이익 억원)
PRESS = {"329180": [("KB", "10/20", 500000, 9012), ("LS", "10월", 600000, None), ("리딩", "10월", 500000, None)],
         "042660": [("JPMorgan", "10/13", 130000, None)],
         "009540": [("한국투자", "10/15", 440000, 15020)],
         "443060": [("다올", "10/12", 310000, None)]}
CONS3Q = {k: v["op"][1] for k, v in json.load(open(f"{D}/조선_네이버컨센3Q_2026-10-21.json")).items() if v["op"]}  # 원장 네이버 컨센 10/21


def oct_rows(code):
    rows = [r for r in rep[code] if r["date"] >= "2026-10-01"]
    out = []
    for r in rows:
        if r["firm"] is None:  # 텔레그램 요약
            twin = [x for x in rows if x["firm"] and x["date"] == r["date"] and x["tp"] is None
                    and x["title"] and x["title"][:12] in r["title"]]
            dup = [x for x in rows if x["firm"] and x["date"] == r["date"] and x["tp"] == r["tp"]]
            if dup:
                continue
            firm = SHORT.get(twin[0]["firm"], twin[0]["firm"]) if twin else "현대차(추정)"
        else:
            firm = SHORT.get(r["firm"], r["firm"])
            if r["tp"] is None:
                continue  # 목표가 없는 행(텔레그램 쌍둥이·코멘트)은 뺀다
        q3 = [e["value"] * (10 if e["unit"] == "십억원" else 1) for e in r["est"]
              if e["metric"] == "op_income" and e["period"].startswith("3Q26")]
        q3 = q3[0] if q3 else TG_3Q.get((code, r["date"])) or BODY_3Q.get((code, firm))
        prev, prev_date = r["prev_tp"], r["prev_date"]
        if prev is None and (code, r["date"]) in TG_PREV:
            prev, prev_date = TG_PREV[(code, r["date"])], "본문"
        out.append(dict(date=r["date"], firm=firm, tp=r["tp"], prev=prev, prev_date=prev_date,
                        q3=q3, title=r["title"]))
    # 같은 증권사가 10월에 두 번 냈으면 최신만
    last = {}
    for x in sorted(out, key=lambda x: x["date"]):
        last[x["firm"]] = x
    return sorted(last.values(), key=lambda x: x["date"])


def rng(xs):
    return (min(xs), max(xs)) if xs else None


res = {}
for code, nm in NAME.items():
    k = krx[code]
    c1021 = daily[code]["2026-10-21"]
    c1020 = daily[code]["2026-10-20"]
    c1019 = daily[code]["2026-10-19"]
    assert c1021 == k["last_close"]
    rows = oct_rows(code)
    tps = [r["tp"] for r in rows]
    press = PRESS.get(code, [])
    alltp = tps + [p[2] for p in press]
    q3 = [r["q3"] for r in rows if r["q3"]]
    med = statistics.median(tps) if tps else None
    medall = statistics.median(alltp) if alltp else None
    res[code] = dict(
        name=nm, close_1021=c1021, close_1020=c1020, chg_1020_pct=round((c1020 / c1019 - 1) * 100, 2),
        chg_1021_pct=round((c1021 / c1020 - 1) * 100, 2), close_0828=C0828[code],
        vs0828_pct=round((c1021 / C0828[code] - 1) * 100, 1), sep_close=k["monthly"]["2026-09"],
        hi=k["high"], hi_date=k["high_date"], from_hi_pct=round((c1021 / k["high"] - 1) * 100, 1),
        oct=rows, n=len(tps), tp_med=med, tp_rng=rng(tps),
        tp_med_vs0828_pct=round((med / TP0828[code] - 1) * 100, 1) if med else None,
        upside_pct=round((med / c1021 - 1) * 100, 0) if med else None,
        press=press, n_all=len(alltp), tp_med_all=medall, tp_rng_all=rng(alltp),
        upside_all_pct=round((medall / c1021 - 1) * 100, 0) if medall else None,
        q3=q3, q3_med=statistics.median(q3) if q3 else None, q3_rng=rng(q3),
        q3_vs_cons_pct=round((statistics.median(q3) / CONS3Q[code] - 1) * 100, 1) if q3 and code in CONS3Q else None,
        tp_med_90d=cons[code]["tp_med_90d"], tp_n_90d=cons[code]["tp_n_firms_90d"],
        upside_90d_pct=round((cons[code]["tp_med_90d"] / c1021 - 1) * 100, 0) if cons[code]["tp_med_90d"] else None,
        last_report=[(x["date"], x["firm"], x["tp"]) for x in cons[code]["recent_reports"][:2]],
        cuts=[dict(firm=r["firm"], prev=r["prev"], tp=r["tp"], pct=round((r["tp"] / r["prev"] - 1) * 100, 1))
              for r in rows if r["prev"]],
    )

json.dump(res, open(f"{D}/조선_원장대조_2026-10-21.json", "w"), ensure_ascii=False, indent=1)
for code, r in res.items():
    print(f"== {code} {r['name']}  10/21 {r['close_1021']:,} ({r['chg_1021_pct']:+}%)  10/20 {r['close_1020']:,} ({r['chg_1020_pct']:+}%)"
          f"  8/28대비 {r['vs0828_pct']:+}%  고점({r['hi_date']})대비 {r['from_hi_pct']:+}%")
    for x in r["oct"]:
        print(f"   {x['date']} {x['firm']:<10} TP {x['tp']:>9,.0f}  prev {x['prev'] or 0:>9,.0f} ({x['prev_date']})  3Q {x['q3']}")
    print(f"   원장 n={r['n']} med={r['tp_med']} rng={r['tp_rng']} 8/28대비 {r['tp_med_vs0828_pct']} 상방 {r['upside_pct']}"
          f" | +보도 n={r['n_all']} med={r['tp_med_all']} rng={r['tp_rng_all']} 상방 {r['upside_all_pct']}")
    print(f"   90d med={r['tp_med_90d']} n={r['tp_n_90d']} 상방 {r['upside_90d_pct']} last={r['last_report']}")
    print(f"   3Q med={r['q3_med']} rng={r['q3_rng']} vs컨센 {r['q3_vs_cons_pct']}%  cuts={[(c['firm'],c['pct']) for c in r['cuts']]}")
