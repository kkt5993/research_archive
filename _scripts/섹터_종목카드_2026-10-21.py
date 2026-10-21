# -*- coding: utf-8 -*-
"""종목 카드의 숫자 표를 원장 이력에서 렌더링한다 (2026-10-21). 해석 문장은 템플릿에 사람이 쓴다.

사용: python _scripts/섹터_종목카드_2026-10-21.py 화장품|인터넷게임 템플릿.md 출력.md
템플릿 안의 {{CARD:코드}} 는 종목 숫자 블록으로, {{FX}} 는 원/달러 월말 표로 바뀐다.
입력(_manifest/데이터): <섹터>_이력.json(맥미니 원장: reports·dart_fin_quarterly·naver_consensus_*·prices·macro_series)
                      <섹터>_원장대조_2026-10-21.json(10월 리포트 정리본)
"""
import json, os, sys, statistics

SEC, TPL, OUT = sys.argv[1:4]
D = os.path.join(os.path.dirname(__file__), "..", "_manifest", "데이터")
H = json.load(open(f"{D}/{SEC}_이력.json"))
R = json.load(open(f"{D}/{SEC}_원장대조_2026-10-21.json"))
QN = {"03-31": "1Q", "06-30": "2Q", "09-30": "3Q", "12-31": "4Q"}


def f(v, d=0):
    return "—" if v is None else (f"{v:,.{d}f}")


def pct(a, b):
    if a is None or b is None or b == 0:
        return "—"
    if b < 0 < a:
        return "흑전"
    if a < 0 <= b:
        return "적전"
    if a < 0 and b < 0:
        return "적지"
    return f"{(a / b - 1) * 100:+.1f}%"


def card(code):
    h, r = H[code], R[code]
    L = []
    # 주가 경로
    px = h["px_monthly"]
    ms = [m for m in sorted(px) if m >= "2025-10"]
    if ms:
        first = px[ms[0]]
        L.append(f"- **주가(월말 종가, 원장 `prices`)**: " + " → ".join(f"{m[2:].replace('-', '/')} {f(px[m])}" for m in ms[::3] + ([ms[-1]] if (len(ms) - 1) % 3 else []))
                 + f" · 10/21 KRX {f(r['close_1021'])} · 12개월 {pct(r['close_1021'], first)} · 8/28 대비 {r['vs0828_pct']:+.1f}% · 고점({r['hi_date'][5:].replace('-', '/')}) 대비 {r['from_hi_pct']:+.1f}%")
    # 분기 실적
    dq = h["dart_q"]
    qs = sorted({k.split("|")[0] for k in dq})
    rows = []
    for pe in qs:
        y, md = pe[:4], pe[5:]
        rev, op = dq.get(f"{pe}|revenue"), dq.get(f"{pe}|op_income")
        prev = f"{int(y) - 1}-{md}"
        rows.append((f"{QN[md]}{y[2:]}", rev, op, pct(rev, dq.get(f"{prev}|revenue")), pct(op, dq.get(f"{prev}|op_income")),
                     f"{op / rev * 100:.1f}%" if rev and op is not None else "—"))
    nc = h["naver_cons"]
    c3 = nc.get("2026Q3E|op_income"); c3r = nc.get("2026Q3E|revenue")
    op25 = dq.get("2025-09-30|op_income"); rev25 = dq.get("2025-09-30|revenue")
    L.append("")
    L.append("| 분기 | 매출(억) | 영업이익(억) | 매출 YoY | 영업이익 YoY | OPM |")
    L.append("|---|---:|---:|---:|---:|---:|")
    for q, rev, op, ry, oy, m in rows[-6:]:
        L.append(f"| {q} | {f(rev)} | {f(op)} | {ry} | {oy} | {m} |")
    if c3:
        cv = c3["last"][1]; crv = c3r["last"][1] if c3r else None
        L.append(f"| **3Q26E 컨센** (네이버 {c3['last'][0][5:].replace('-', '/')}) | {f(crv)} | **{f(cv)}** | {pct(crv, rev25)} | {pct(cv, op25)} | {f'{cv / crv * 100:.1f}%' if crv else '—'} |")
    if r.get("q3_med") is not None:
        lab = "원장 리포트 중앙값" + (f" ({len(r['q3'])}곳)" if len(r["q3"]) > 1 else f" ({list(r['q3'])[0]})")
        vs = f" · 컨센 대비 {pct(r['q3_med'], c3['last'][1])}" if c3 else ""
        L.append(f"| 3Q26E {lab} | | {f(r['q3_med'])} | | {pct(r['q3_med'], op25)} | |")
    L.append("")
    L.append("> 실적은 DART 분기(연결 우선, 4Q 는 연간 − 3분기 누계로 역산), 단위 억원. " +
             (f"3Q26 영업이익 컨센은 10월 중 {f(c3['first'][1])} → {f(c3['last'][1])}억({pct(c3['last'][1], c3['first'][1])})으로 움직였다" if c3 else "네이버 컨센 3Q26E 없음") +
             (f"; 원장 리포트 중앙값은 컨센 대비 {pct(r['q3_med'], c3['last'][1])}." if (c3 and r.get('q3_med') is not None) else "."))
    # 연간 컨센 변화
    a26, a27 = nc.get("2026E|op_income"), nc.get("2027E|op_income")
    tg = h["naver_target"]
    bits = []
    if a26: bits.append(f"2026E 영업이익 {f(a26['first'][1])} → {f(a26['last'][1])}억({pct(a26['last'][1], a26['first'][1])})")
    if a27: bits.append(f"2027E {f(a27['first'][1])} → {f(a27['last'][1])}억({pct(a27['last'][1], a27['first'][1])})")
    if tg: bits.append(f"목표가 평균 {f(tg['first'][1])} → {f(tg['last'][1])}원({pct(tg['last'][1], tg['first'][1])})")
    if bits:
        L.append(f"- **네이버 컨센 10/4 → 10/21**: " + " · ".join(bits))
    # 목표가 월별 경로
    tm = h["tp_monthly"]
    if tm:
        L.append("- **리포트 목표가 월별 중앙값(원장, 증권사별 그 달 최신 1건)**: " +
                 " → ".join(f"{x['m'][2:].replace('-', '/')} {f(x['med'])}({x['n']})" for x in tm) +
                 (f" · 범위는 최근 달 {f(tm[-1]['lo'])}–{f(tm[-1]['hi'])}" if tm else ""))
        drop = sum(x["drop"] for x in tm)
        if drop:
            L.append(f"  - 월 중앙값의 1/3–3배를 벗어난 값 {drop}건은 파싱 오류로 보고 뺐다.")
    # 큰 변경
    ch = [c for c in h["tp_changes"] if c["date"] >= "2025-10-01"]
    if ch:
        big = sorted(ch, key=lambda c: -abs(c["pct"]))[:5]
        big = sorted(big, key=lambda c: c["date"])
        L.append("- **12개월 중 큰 목표가 변경**: " + " · ".join(
            f"{c['date'][2:].replace('-', '/')} {c['firm'].replace('투자증권', '').replace('증권', '')} {f(c['prev'])}→{f(c['tp'])}({c['pct']:+.0f}%, \"{(c['title'] or '')[:22]}\")" for c in big))
        up = sum(1 for c in ch if c["pct"] > 0); dn = sum(1 for c in ch if c["pct"] < 0)
        L.append(f"  - 12개월 목표가 변경 {len(ch)}건: 상향 {up} · 하향 {dn}.")
    elif tm:
        L.append("- 12개월 안에 같은 증권사가 목표가를 바꾼 기록은 없다.")
    else:
        L.append("- **리포트 목표가 이력**: 원장 12개월 안에 목표가가 붙은 리포트가 없다(NR·한국IR협의회 커버).")
    return "\n".join(L)


def fx():
    m = H["_usdkrw_monthend"]
    ks = sorted(m)
    pick = [k for k in ks if k[4:] in ("09", "12", "03", "06")] + [ks[-1]]
    pick = sorted(set(pick))
    s = " → ".join(f"{m[k][0][2:4]}/{m[k][0][4:6]}/{m[k][0][6:]} {f(m[k][1], 1)}" for k in pick)
    peak = max(ks, key=lambda k: m[k][1])
    return (f"원/달러(ECOS 매매기준율, 월말): {s}. 연중 최고 월말 {m[peak][0][:4]}-{m[peak][0][4:6]} {f(m[peak][1], 1)}원 대비 10/21 {pct(m[ks[-1]][1], m[peak][1])}.")


t = open(TPL).read()
for code in [c for c in R if "{{CARD:%s}}" % c in t]:
    t = t.replace("{{CARD:%s}}" % code, card(code))
t = t.replace("{{FX}}", fx())
assert "{{" not in t, [x for x in t.split("{{")[1:]][:3]
open(OUT, "w").write(t)
print("ok", OUT)
