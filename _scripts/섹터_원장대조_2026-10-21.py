# -*- coding: utf-8 -*-
"""대표주 — 원장 10월 리포트 × KRX 종가 대조 (2026-10-21). 화장품·인터넷/게임용.

사용: python _scripts/섹터_원장대조_2026-10-21.py 화장품|인터넷게임
입력(_manifest/데이터):
  <섹터>_원장리포트_2026-09-01_10-21.json  맥미니 원장 reports·report_estimates(읽기 전용 사본)
  <섹터>_2026-10-21.json · <섹터>_일별종가_2026-10-15_10-21.json  KRX 종가
출력: <섹터>_원장대조_2026-10-21.json + 표준출력 요약. 산술은 전부 여기서 한다.

원장 정리 규칙
- 같은 리포트가 naver·hankyung·telegram 으로 여러 번 들어온다. 증권사별로 10월 최신 1건,
  같은 날이면 naver > broker > hankyung > telegram 순으로 고른다(hankyung 목표가 파싱 오류 회피).
- 증권사 칸이 빈 telegram:companyreport 행: 같은 날 같은 목표가의 증권사 행이 있으면 중복이라 버린다.
  같은 날 제목이 겹치거나 목표가 없는 증권사 행이 하나뿐이면 그 증권사로 맞춘다. 못 맞추면 '미상'.
- 목표가 없는 행은 중앙값에서 뺀다. 직전 목표가는 10/1 이전 같은 증권사 최신값, 180일 넘게 묵었으면 비교 안 함.
- 3Q 영업이익 단위(억/십억)는 리포트마다 다르다. 같은 리포트의 3Q25 실적 자릿수를 업종 최빈 자릿수에 맞춰 10배수로만 옮긴다.
"""
import json, statistics, sys, math, datetime
from collections import Counter

SEC = sys.argv[1]
D = __import__("os").path.join(__import__("os").path.dirname(__file__), "..", "_manifest", "데이터")
rep = json.load(open(f"{D}/{SEC}_원장리포트_2026-09-01_10-21.json"))
krx = json.load(open(f"{D}/{SEC}_2026-10-21.json"))["데이터"]
daily = json.load(open(f"{D}/{SEC}_일별종가_2026-10-15_10-21.json"))
# 8/28 원장 표(이전 스냅샷)의 종가·목표가
SNAP = {"278470": (461500, 540000), "090430": (150600, 178000), "051900": (318000, 342500),
        "161890": (161700, 160000), "192820": (303000, 280000), "483650": (229000, 300000),
        "035420": (220500, 320000), "035720": (36850, 57000), "259960": (222500, 380000),
        "036570": (225000, 355000), "251270": (37450, 57000), "462870": (32900, 45000), "263750": (32500, 50500)}
PRI = {"naver:research": 0, "broker:bnk": 1, "hankyung": 2, "telegram:reportsnow": 3, "telegram:companyreport": 4}
SHORT = lambda f: (f.replace("투자증권", "").replace("증권", "") or f) if f else f


def attribute(code, rows):
    octr = [r for r in rows if r["date"] >= "2026-10-01"]
    out = []
    for r in octr:
        r = dict(r)
        if r["firm"] is None:
            same = [x for x in octr if x["firm"] and x["date"] == r["date"]]
            if any(x["tp"] == r["tp"] for x in same):
                continue
            tit = [x for x in same if x["title"] and len(x["title"]) >= 6 and
                   (x["title"][:8] in r["title"] or r["title"].split("] ")[-1][:8] in x["title"])]
            notp = [x for x in same if x["tp"] is None]
            pick = tit[0] if tit else (notp[0] if len(notp) == 1 else None)
            r["firm"] = pick["firm"] if pick else "미상"
            r["prev_tp"], r["prev_date"] = (pick["prev_tp"], pick["prev_date"]) if pick else (None, None)
            r["matched"] = bool(pick)
        out.append(r)
    return out


def prev_before_oct(code, firm, r):
    p, d = r.get("prev_tp"), r.get("prev_date")
    while d and d >= "2026-10-01":
        older = [x for x in rep[code] if x["firm"] == firm and x["date"] == d and x["tp"]]
        if not older:
            return None, None
        p, d = older[0]["prev_tp"], older[0]["prev_date"]
    if d and (datetime.date(2026, 10, 1) - datetime.date.fromisoformat(d)).days > 180:
        return None, d
    return p, d


def q3(r):
    e = {}
    for x in r["est"]:
        if x["metric"] == "op_income" and x["value"] is not None:
            e.setdefault(x["period"][:4], x["value"] * (10 if x["unit"] == "십억원" else 1))
    return e.get("3Q26"), e.get("3Q25")


res = {}
for code, rows in rep.items():
    rows = attribute(code, rows)
    best = {}
    for r in rows:
        if r["tp"] is None:
            continue
        k = SHORT(r["firm"]) if r["firm"] != "미상" else f"미상{r['date']}"
        cur = best.get(k)
        if cur is None or (r["date"], -PRI.get(r["source"], 9)) > (cur["date"], -PRI.get(cur["source"], 9)):
            best[k] = r
    # 3Q 추정은 목표가 행과 별개로, 증권사별 아무 10월 행에서나 모은다
    q3s = {}
    for r in rows:
        a, b = q3(r)
        if a is not None:
            q3s.setdefault(SHORT(r["firm"]), (a, b))
    mags = [math.floor(math.log10(abs(b))) for a, b in q3s.values() if b]
    mode = max(Counter(mags).items(), key=lambda kv: (kv[1], kv[0]))[0] if mags else None
    q3n = {}
    for f, (a, b) in q3s.items():
        k = (mode - math.floor(math.log10(abs(b)))) if (b and mode is not None) else 0
        q3n[f] = (round(a * 10 ** k), round(b * 10 ** k) if b else None)
    tab = []
    for k, r in sorted(best.items(), key=lambda kv: kv[1]["date"]):
        p, pd = prev_before_oct(code, r["firm"], r) if r["firm"] != "미상" else (r.get("prev_tp"), r.get("prev_date"))
        a = q3n.get(SHORT(r["firm"]), (None, None))
        tab.append(dict(date=r["date"], firm=SHORT(r["firm"]), src=r["source"], tp=r["tp"], prev=p, prev_date=pd,
                        chg=round((r["tp"] / p - 1) * 100, 1) if p else None, q3=a[0], q3_25=a[1], title=r["title"]))
    tps = [x["tp"] for x in tab]
    q3v = [a for a, b in q3n.values()]
    yoy = [round((a / b - 1) * 100, 1) for a, b in q3n.values() if b and b > 0]
    c0828, tp0828 = SNAP[code]
    c1021 = daily[code]["2026-10-21"]
    assert c1021 == krx[code]["last_close"]
    med = statistics.median(tps) if tps else None
    res[code] = dict(name=krx[code]["name"], close_1021=c1021, close_0828=c0828,
                     vs0828_pct=round((c1021 / c0828 - 1) * 100, 1), hi=krx[code]["high"], hi_date=krx[code]["high_date"],
                     from_hi_pct=round((c1021 / krx[code]["high"] - 1) * 100, 1), sep_close=krx[code]["monthly"]["2026-09"],
                     vs_sep_pct=round((c1021 / krx[code]["monthly"]["2026-09"] - 1) * 100, 1),
                     oct=tab, n=len(tps), tp_med=med, tp_rng=(min(tps), max(tps)) if tps else None, tp0828=tp0828,
                     tp_med_vs0828_pct=round((med / tp0828 - 1) * 100, 1) if med else None,
                     upside_pct=round((med / c1021 - 1) * 100) if med else None,
                     n_up=sum(1 for x in tab if x["chg"] and x["chg"] > 0), n_down=sum(1 for x in tab if x["chg"] and x["chg"] < 0),
                     n_flat=sum(1 for x in tab if x["chg"] == 0),
                     q3=q3n, q3_med=statistics.median(q3v) if q3v else None, q3_rng=(min(q3v), max(q3v)) if q3v else None,
                     q3_yoy_med=statistics.median(yoy) if yoy else None, q3_25=statistics.median([b for a, b in q3n.values() if b]) if q3n else None)

json.dump(res, open(f"{D}/{SEC}_원장대조_2026-10-21.json", "w"), ensure_ascii=False, indent=1)
for code, r in res.items():
    print(f"== {code} {r['name']} 10/21 {r['close_1021']:,} 8/28대비 {r['vs0828_pct']:+}% 9월말대비 {r['vs_sep_pct']:+}% 고점({r['hi_date']}) {r['from_hi_pct']:+}%")
    for x in r["oct"]:
        print(f"   {x['date']} {x['firm']:<8} {x['tp']:>9,.0f} prev {x['prev'] or 0:>9,.0f} {x['chg']}  3Q {x['q3']} / {x['q3_25']}  {x['src'][:9]} {x['title'][:30]}")
    print(f"   n={r['n']} med={r['tp_med']} rng={r['tp_rng']} 8/28 {r['tp0828']} → {r['tp_med_vs0828_pct']}% 상방 {r['upside_pct']}% 상/하/유 {r['n_up']}/{r['n_down']}/{r['n_flat']}")
    print(f"   3Q med={r['q3_med']} rng={r['q3_rng']} 3Q25={r['q3_25']} YoY med={r['q3_yoy_med']}")
