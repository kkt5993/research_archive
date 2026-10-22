#!/usr/bin/env python3
"""미용의료 3종목(클래시스·휴젤·파마리서치) 심층 업데이트 — 숫자 계산.

DEEP_UPDATE_BRIEF.md 를 따른다. 숫자는 아래에서만 읽는다.
- _manifest/데이터/화장품_원장대조_2026-10-21.json   10월 리포트 정리본·10/21 종가·8/28 대비
- _manifest/데이터/화장품_이력.json                  dart_q·naver_cons·tp_monthly·tp_changes·px_monthly
- _manifest/데이터/화장품_일별종가_2026-10-15_10-21.json  10/20·10/21 KRX 종가
- _manifest/데이터/화장품_종가_2026-08-28.json        8/28 KRX 종가
- _manifest/데이터/화장품_미용의료_원장추출_2026-10-21.json
      맥미니 research.ro.duckdb(읽기 전용 사본)에서 뽑은 것: prices(12개월 고점용)·
      naver_consensus_snap(10/21 3Q·2026E)·reports 메타(본문 제외).
      `python3 _seminar/deep_aesthetics.py --fetch` 로 다시 뽑는다.

리포트 본문·PDF 에서 사람이 읽어 옮긴 값은 아래 READ_FROM_TEXT 에 출처와 함께 둔다.
산술은 전부 이 스크립트가 한다.

실행: python3 _seminar/deep_aesthetics.py            → 표 조각을 stdout 으로
"""
import json
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_manifest" / "데이터"
F_CMP = DATA / "화장품_원장대조_2026-10-21.json"
F_HIS = DATA / "화장품_이력.json"
F_DAY = DATA / "화장품_일별종가_2026-10-15_10-21.json"
F_828 = DATA / "화장품_종가_2026-08-28.json"
F_LED = DATA / "화장품_미용의료_원장추출_2026-10-21.json"

TICKERS = {"214150": "클래시스", "145020": "휴젤", "214450": "파마리서치"}
ASOF = "2026-10-21"
WIN_START = "2025-10-22"  # 12개월 창: 2025-10-22 – 2026-10-21

# ---------------------------------------------------------------- fetch
FETCH_PY = r'''
import duckdb, json, datetime
c = duckdb.connect("/Users/benopenclaw/research-site/stable/warehouse/research.ro.duckdb", read_only=True)
S = lambda x: str(x) if isinstance(x, (datetime.date, datetime.datetime)) else x
out = {}
for t in ["214150", "145020", "214450"]:
    o = {}
    o["px"] = [[S(a), b] for a, b in c.execute(
        "select d, close from prices where symbol=? and d>='2025-10-01' and d<='2026-10-22' order by d", [t]).fetchall()]
    o["cons"] = [[S(a), p, i, v] for a, p, i, v in c.execute(
        "select snap_date, period, item, value from naver_consensus_snap where ticker=? "
        "and period in ('2026Q3E','2026E') and snap_date between '2026-10-04' and '2026-10-21' order by 1", [t]).fetchall()]
    o["rep"] = [[S(a), s, f, tp, op, ti] for a, s, f, tp, op, ti in c.execute(
        "select published_at, source, firm, target_price, opinion, title from reports "
        "where ticker=? and published_at>='2025-10-01' order by 1", [t]).fetchall()]
    out[t] = o
o = {}
o["kosdaq"] = [[S(a), b] for a, b in c.execute(
    "select d, close from prices where symbol='KOSDAQ' and d>='2025-10-01' and d<='2026-10-22' order by d").fetchall()]
out["_index"] = o
c.close()
print(json.dumps(out, ensure_ascii=False))
'''


def fetch():
    r = subprocess.run(["ssh", "-o", "ConnectTimeout=10", "mini", "python3 -"], input=FETCH_PY,
                       capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    d["_meta"] = {"src": "mini research.ro.duckdb (read_only)", "tables": "prices, naver_consensus_snap, reports(meta)"}
    F_LED.write_text(json.dumps(d, ensure_ascii=False, indent=1))
    print("wrote", F_LED)


# ---------------------------------------------------------------- 본문·PDF 에서 읽은 값
READ_FROM_TEXT = {
    # 상상인증권: 원장 reports.target_price 가 비어 있다. 원장 report_pdf_files 의 PDF 마지막 쪽
    # '목표가격' 이력표에서 읽었다(PDF 표의 일자는 원장 published_at 보다 하루 늦게 찍힌 경우가 있다).
    "sangsangin": {
        "214150": [("2025-11-10", 75000, "클래시스(214150):2026년에도 고성장 가능하다"),
                   ("2025-12-16", 75000, "클래시스(214150):2026년에도 실적 고성장 기대된다"),
                   ("2026-03-10", 87000, "클래시스(214150):2026년에도 30%대 성장 기대된다"),
                   ("2026-05-13", 83000, "클래시스(214150):2분기부터 정상적 실적 성장 전망"),
                   ("2026-07-22", 70000, "클래시스(214150):매출 성장성과 수익성 회복")],
        "145020": [("2025-11-07", 360000, "휴젤(145020):성장률 둔화, 2026년을 보자"),
                   ("2026-03-27", 360000, "휴젤(145020):2026년에도 외형 고성장은 지속된다"),
                   ("2026-05-12", 380000, "휴젤(145020):해외 성장 중심의 고성장 지속 전망"),
                   ("2026-08-06", 380000, "하반기 주가 회복 가능성 높아졌다")],  # 8/6 은 원장 텔레그램 행(하태기)
        "214450": [("2025-11-11", 700000, "파마리서치(214450):4분기부터 다시 QoQ 성장 기대된다"),
                   ("2026-01-16", 730000, "파마리서치(214450):2차 주가 조정 끝내고 상승 전환 기대"),
                   ("2026-02-04", 700000, "파마리서치(214450):그래도 고성장 스토리는 유효하다"),
                   ("2026-03-04", 600000, "파마리서치(214450):수출 중심 고성장은 여전히 기대된다"),
                   ("2026-05-15", 540000, "파마리서치(214450):화장품 부문 매출 성장 확대"),
                   ("2026-07-27", 540000, "파마리서치(214450):금리 상승기에 주목 받을 종목이다"),
                   ("2026-08-26", 610000, "파마리서치(214450):리쥬란 화장품의 미국 성장에 주목한다")],
    },
    # 10월 리포트 3Q 영업이익 추정 중 원장대조 정리본(q3)에 없고 본문 요약에만 있는 것
    "q3_body": {
        "145020": {"DB": 224},     # 10/13 DB PDF 1쪽 "3Q26E 영업이익 224억원, 컨센서스 하회 전망"
        "214150": {"다올": 375},   # 10/15 「미씽 링크」 "3Q26E 영업이익은 375억원으로 컨센서스를 25% 하회"
        "214450": {"다올": 626},   # 10/19 「3Q26보다 4Q26을 볼 때」 "3Q26 영업이익은 626억원 ... 컨센서스를 14% 하회"
    },
    # 원장대조 정리본(oct)에 없는 10월 리포트. 목표가 칸이 비어 있어 PDF·원장 news 에서 읽었다.
    "oct_extra": {
        "145020": [
            {"date": "2026-10-13", "firm": "상상인", "prev": 380000, "tp": 330000, "q3": 214,
             "src": "원장 news(머니투데이 10/13) — reports 테이블에 행 없음",
             "title": "\"휴젤, 美 판매개편 따른 일시 감익…목표가↓\"-상상인 (기사 제목)"},
            {"date": "2026-10-15", "firm": "KB", "prev": 400000, "tp": 290000, "q3": 276,
             "src": "원장 reports(tp 빈칸) + report_pdf_files PDF 1쪽",
             "title": "3분기, 재정비의 시간"},
        ],
    },
    # D절 — 저장소 기존 문서의 날짜 붙은 숫자 판단
    "prior": {
        # 10_국내주식/16_건강관리/건강관리_코스피200_종목분석.md (기준일 2026-08-28)
        "214150": {"op26_0828": 1872, "tp_0828": 60000, "fpe_0828": 14.0, "fpe_band": (15, 20), "opm_claim": 50},
        "145020": {"op26_0828": 2264, "tp_0828": 380000, "fpe_0828": 18.4, "fpe_band": (18, 22), "opm_claim": 35},
        "214450": {"op26_0828": 2765, "tp_0828": 510000, "fpe_0828": 24.1},
        # fpe_band·opm_claim: 바이오_진단의료기기소부장_심층분석.md (작성일 2026-04-29) §6·§10-2
    },
    "kyobo_op26": {"214150": 1688},  # 교보 10/21 2026F 영업이익 168.8십억원 (원장 report_estimates)
    # 회사 가이던스 (리포트 본문에서)
    "guidance": {
        "214150": [{"what": "2026 매출(억원, 8월 하향 후)", "lo": 4300, "hi": 4600,
                    "src": "신한 8/28 NDR 후기 — 중앙값 4,900 → 4,450억",
                    "cmp_name": "교보 10/21 2026F 매출", "cmp": 4038}],
    },
    # 12개월 보충(E절)에서 낡은 값으로 빼는 기준일 = 2Q26 실적 발표 다음 영업일.
    # 이 날 이후 갱신이 없는 증권사의 목표가는 가이던스 하향(클래시스)·2Q 숫자 이전 값이라 쓰지 않는다.
    "e_cutoff": {"214150": "2026-08-13", "214450": "2026-08-10"},
    # 파싱 오류로 확인된 원장 행 (원장 tp_monthly 도 drop 처리)
    "bad_rows": [("214450", "2026-05-11", "LS증권", 44000.0)],
}

FIRM_ALIAS = {"한국투자증권": "한국투자", "미래에셋증권": "미래에셋", "신한투자증권": "신한", "유진투자증권": "유진",
              "다올투자증권": "다올", "IBK투자증권": "IBK", "현대차증권": "현대차", "상상인증권": "상상인"}


def short(f):
    if not f:
        return None
    if f in FIRM_ALIAS:
        return FIRM_ALIAS[f]
    return f.replace("투자증권", "").replace("증권", "")


def pct(a, b):
    return (a / b - 1) * 100


def f0(x):
    return f"{x:,.0f}"


def fp(x, d=1):
    s = f"{x:+.{d}f}%"
    return s.replace("-", "−")


# ---------------------------------------------------------------- main
def main():
    if "--fetch" in sys.argv:
        fetch()
        return
    CMP = json.loads(F_CMP.read_text())
    HIS = json.loads(F_HIS.read_text())
    DAY = json.loads(F_DAY.read_text())
    C828 = json.loads(F_828.read_text())
    LED = json.loads(F_LED.read_text())
    kq = dict(LED["_index"]["kosdaq"])
    print(f"KOSDAQ 8/28 {kq['2026-08-28']:,} → 10/21 {kq['2026-10-21']:,} ({fp(pct(kq['2026-10-21'], kq['2026-08-28']))})"
          f" · 25/10월말 {kq['2025-10-31']:,} 대비 {fp(pct(kq['2026-10-21'], kq['2025-10-31']))}")

    for t, nm in TICKERS.items():
        c, h, led = CMP[t], HIS[t], LED[t]
        print("\n" + "=" * 70 + f"\n{nm} ({t})")
        # ---------- A
        p21, p20 = DAY[t]["2026-10-21"], DAY[t]["2026-10-20"]
        p828 = C828[t]
        px = [(d, v) for d, v in led["px"] if WIN_START <= d <= ASOF]
        hi_d, hi_v = max(px, key=lambda r: r[1])
        lo_d, lo_v = min(px, key=lambda r: r[1])
        m2510 = h["px_monthly"]["2025-10"]
        print("[A]")
        print(f"  10/21 종가 {f0(p21)} ({fp(pct(p21, p20), 2)} vs 10/20 {f0(p20)})")
        print(f"  8/28 {f0(p828)} 대비 {fp(pct(p21, p828))}")
        print(f"  12개월 고점(원장 prices 종가) {f0(hi_v)} ({hi_d}) 대비 {fp(pct(p21, hi_v))} · 저점 {f0(lo_v)} ({lo_d})")
        print(f"  원장대조 'hi'(8/1 이후 KRX) {f0(c['hi'])} ({c['hi_date']}) 대비 {c['from_hi_pct']}%")
        print(f"  25/10 월말 {f0(m2510)} 대비 {fp(pct(p21, m2510))}")
        # ledger vs KRX close diff
        lp = dict(led["px"])
        for d in ["2026-10-15", "2026-10-16", "2026-10-19", "2026-10-20", "2026-10-21"]:
            if d in lp and lp[d] != DAY[t][d]:
                print(f"  ! 원장 prices {d} {f0(lp[d])} ≠ KRX {f0(DAY[t][d])}")
        # DART
        dq = {}
        for k, v in h["dart_q"].items():
            d, f = k.split("|")
            dq.setdefault(d, {})[f] = v
        rev2, op2 = dq["2026-06-30"]["revenue"], dq["2026-06-30"]["op_income"]
        print(f"  2Q26 매출 {f0(rev2)} ({fp(pct(rev2, dq['2025-06-30']['revenue']))}) · 영업이익 {f0(op2)} ({fp(pct(op2, dq['2025-06-30']['op_income']))})")
        # cons 10/21
        cons = {(p, i): v for sd, p, i, v in led["cons"] if sd == "2026-10-21"}
        cons04 = {(p, i): v for sd, p, i, v in led["cons"] if sd == "2026-10-04"}
        q3op, q3rev = cons[("2026Q3E", "op_income")], cons[("2026Q3E", "revenue")]
        op25, rev25 = dq["2025-09-30"]["op_income"], dq["2025-09-30"]["revenue"]
        print(f"  3Q26E 컨센(10/21) 매출 {f0(q3rev)} ({fp(pct(q3rev, rev25))}) · 영업이익 {f0(q3op)} ({fp(pct(q3op, op25))} YoY, 3Q25 DART {op25})"
              f" · 10/4 {f0(cons04[('2026Q3E','op_income')])} → {fp(pct(q3op, cons04[('2026Q3E','op_income')]))}")
        print(f"  2026E 컨센 OP {f0(cons04[('2026E','op_income')])} → {f0(cons[('2026E','op_income')])} ({fp(pct(cons[('2026E','op_income')], cons04[('2026E','op_income')]))})"
              f" · EPS {f0(cons[('2026E','eps')])} → 현재 PER {p21 / cons[('2026E','eps')]:.1f}배"
              f" (같은 EPS 로 8/28 주가면 {p828 / cons[('2026E','eps')]:.1f}배)")
        # 3Q report estimates
        q3 = {k: v[0] for k, v in c["q3"].items()}
        q3.update(READ_FROM_TEXT["q3_body"].get(t, {}))
        extra = READ_FROM_TEXT["oct_extra"].get(t, [])
        for o in extra:
            q3[o["firm"]] = o["q3"]
        oct_all = c["oct"] + [dict(o, chg=round(pct(o["tp"], o["prev"]), 1)) for o in extra]
        if q3:
            vals = sorted(q3.values())
            med = statistics.median(vals)
            print(f"  3Q 원장 리포트 추정 {q3} → 범위 {vals[0]}–{vals[-1]}, 중앙값 {med:g} · 컨센 대비 {fp(pct(vals[0], q3op))} – {fp(pct(vals[-1], q3op))}"
                  f" (중앙값 {fp(pct(med, q3op))}) · YoY(중앙값) {fp(pct(med, op25))}")
            for k, v in q3.items():
                print(f"    {k} {v}: 컨센 대비 {fp(pct(v, q3op))} · YoY {fp(pct(v, op25))}")
        print(f"  [정리본] 10월 목표가 중앙값 {f0(c['tp_med'])} ({c['n']}곳, {f0(c['tp_rng'][0])}–{f0(c['tp_rng'][1])}) · 현재가 대비 {fp(pct(c['tp_med'], p21), 0)}"
              f" · 8/28 원장 {f0(c['tp0828'])} 대비 {fp(pct(c['tp_med'], c['tp0828']))}")
        ov = sorted(o["tp"] for o in oct_all)
        om = statistics.median(ov)
        print(f"  [보강] 10월 목표가 중앙값 {f0(om)} ({len(ov)}곳, {f0(ov[0])}–{f0(ov[-1])}) · 현재가 대비 {fp(pct(om, p21), 0)} · 8/28 원장 {f0(c['tp0828'])} 대비 {fp(pct(om, c['tp0828']))}")
        nt = h["naver_target"]
        print(f"  네이버 목표가 평균 {f0(nt['first'][1])}(10/4) → {f0(nt['last'][1])}(10/21) {fp(pct(nt['last'][1], nt['first'][1]))}")

        # ---------- D
        pr = READ_FROM_TEXT["prior"][t]
        o26 = cons[("2026E", "op_income")]
        print("[D]")
        print(f"  8/28 원장 2026E OP {pr['op26_0828']:,} → 10/21 컨센 {f0(o26)} ({fp(pct(o26, pr['op26_0828']))})"
              + (f" · 교보 10/21 {READ_FROM_TEXT['kyobo_op26'][t]:,} ({fp(pct(READ_FROM_TEXT['kyobo_op26'][t], pr['op26_0828']))})" if t in READ_FROM_TEXT['kyobo_op26'] else ""))
        print(f"  8/28 목표가 {pr['tp_0828']:,} (상방은 8/28 주가 기준 {fp(pct(pr['tp_0828'], p828), 0)}) · 8/28 선행PER {pr['fpe_0828']} → 10/21 {p21 / cons[('2026E','eps')]:.1f}")
        if "fpe_band" in pr:
            print(f"  4/29 적정 P/E 밴드 {pr['fpe_band'][0]}–{pr['fpe_band'][1]}배 → 하단이면 {f0(pr['fpe_band'][0] * cons[('2026E','eps')])}원 (2026E 컨센 EPS)")
        if "opm_claim" in pr:
            print(f"  4/29 OPM 주장 {pr['opm_claim']}%+ vs 2026E 컨센 OPM {o26 / cons[('2026E','revenue')] * 100:.1f}%")

        # ---------- B
        print("[B] 분기")
        qs = ["2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31", "2026-03-31", "2026-06-30"]
        for d in qs:
            y = str(int(d[:4]) - 1) + d[4:]
            r, o = dq[d]["revenue"], dq[d]["op_income"]
            print(f"  | {(int(d[5:7]) - 1) // 3 + 1}Q{d[2:4]} | {f0(r)} | {f0(o)} | {o / r * 100:.1f}% | {fp(pct(r, dq[y]['revenue']))} | {fp(pct(o, dq[y]['op_income']))} |")
        print(f"  | 3Q26E 컨센 | {f0(q3rev)} | {f0(q3op)} | {q3op / q3rev * 100:.1f}% | {fp(pct(q3rev, rev25))} | {fp(pct(q3op, op25))} |")
        h1_26 = dq["2026-03-31"]["op_income"] + dq["2026-06-30"]["op_income"]
        h1_25 = dq["2025-03-31"]["op_income"] + dq["2025-06-30"]["op_income"]
        r1_26 = dq["2026-03-31"]["revenue"] + dq["2026-06-30"]["revenue"]
        r1_25 = dq["2025-03-31"]["revenue"] + dq["2025-06-30"]["revenue"]
        print(f"  1H26 매출 {f0(r1_26)} ({fp(pct(r1_26, r1_25))}) OP {f0(h1_26)} ({fp(pct(h1_26, h1_25))}) OPM {h1_26 / r1_26 * 100:.1f}% vs 1H25 {h1_25 / r1_25 * 100:.1f}%")
        ann25 = sum(dq[d]["op_income"] for d in qs[:4])
        rev25a = sum(dq[d]["revenue"] for d in qs[:4])
        r26, o26 = cons[("2026E", "revenue")], cons[("2026E", "op_income")]
        print(f"  2025 매출 {f0(rev25a)} · 2026E 컨센 매출 {f0(r26)} ({fp(pct(r26, rev25a))}) · OPM {o26 / r26 * 100:.1f}%")
        for g in READ_FROM_TEXT["guidance"].get(t, []):
            print(f"  가이던스 {g['what']}: {g['lo']:,}–{g['hi']:,} ({g['src']}) · 컨센 {f0(r26)} 은 하단 대비 {fp(pct(r26, g['lo']))}"
                  + (f" · {g['cmp_name']} {f0(g['cmp'])} 은 하단 대비 {fp(pct(g['cmp'], g['lo']))}" if g.get('cmp') else ""))
        print(f"  2025 OP {f0(ann25)} · 2026E 컨센 OP {f0(cons[('2026E','op_income')])} ({fp(pct(cons[('2026E','op_income')], ann25))})"
              f" · 4Q26E 역산(2026E−1H−3QE) {f0(cons[('2026E','op_income')] - h1_26 - q3op)} vs 4Q25 {dq['2025-12-31']['op_income']}")

        # ---------- C
        print("[C] 목표가 월별 중앙값")
        print("  " + " → ".join(f"{m['m'][2:].replace('-', '/')} {f0(m['med'])}({m['n']})" for m in h["tp_monthly"]))
        tc = h["tp_changes"]
        print(f"  12개월 변경 {len(tc)}건: 상향 {sum(1 for x in tc if x['pct'] > 0)} · 하향 {sum(1 for x in tc if x['pct'] < 0)}")
        for x in sorted(tc, key=lambda x: x["pct"])[:6]:
            print(f"    {x['date']} {x['firm']} {f0(x['prev'])}→{f0(x['tp'])} ({fp(x['pct'])}) 「{x['title']}」")
        for x in [x for x in tc if x["pct"] > 0]:
            print(f"    (상향) {x['date']} {x['firm']} {f0(x['prev'])}→{f0(x['tp'])} ({fp(x['pct'])}) 「{x['title']}」")
        print("  10월 리포트:")
        for o in oct_all:
            cur = o["tp"]
            prev = f0(o["prev"]) if o["prev"] else "—"
            print(f"    {o['date']} {o['firm']} {prev}→{f0(cur)} chg {o['chg']} q3 {q3.get(o['firm'], o['q3'])} 「{o['title']}」 ({o['src']}) 현재가 대비 {fp(pct(cur, p21), 0)}")
        ss = READ_FROM_TEXT["sangsangin"][t]
        print("  상상인 목표가 경로(PDF): " + " → ".join(f"{d[2:]} {f0(v)}" for d, v, _ in ss))
        last = ss[-1]
        print(f"    최신 {last[0]} {f0(last[1])} · 현재가 대비 {fp(pct(last[1], p21), 0)}")

        # ---------- E
        print("[E]")
        # 증권사별 최신 목표가 (12개월, 원장 + 상상인 PDF)
        bad = {(b[1], b[2], b[3]) for b in READ_FROM_TEXT["bad_rows"] if b[0] == t}
        latest = {}
        for d, src, firm, tp, op, ti in led["rep"]:
            if not tp or not firm or d < WIN_START or d > ASOF:
                continue
            if (d, firm, tp) in bad:
                continue
            f = short(firm)
            if f not in latest or d >= latest[f][0]:
                latest[f] = (d, tp, ti)
        for d, v, ti in ss:
            if d >= WIN_START and ("상상인" not in latest or d >= latest["상상인"][0]):
                latest["상상인"] = (d, float(v), ti)
        if len(oct_all) >= 3:
            vals = sorted(o["tp"] for o in oct_all)
            label = f"10월 원장 {len(oct_all)}곳 (정리본 {c['n']} + 보강 {len(extra)})"
            used = {o["firm"]: o["tp"] for o in oct_all}
            dropped = {}
        else:
            cut = READ_FROM_TEXT["e_cutoff"][t]
            used = {f: v[1] for f, v in latest.items() if v[0] >= cut}
            dropped = {f: (v[0], v[1]) for f, v in latest.items() if v[0] < cut}
            vals = sorted(used.values())
            label = f"12개월 보충: 증권사별 최신 1건, {cut} 이후 {len(vals)}곳"
        bull, base, bear = vals[-1], statistics.median(vals), vals[0]
        eps = cons[("2026E", "eps")]
        print(f"  {label}")
        print(f"  used {dict(sorted(used.items(), key=lambda x: -x[1]))}")
        if dropped:
            print(f"  dropped(낡음) {dropped}")
        for nmx, v in [("Bull", bull), ("Base", base), ("Bear", bear), ("시장", p21)]:
            print(f"  {nmx} {f0(v)} · 현재가 대비 {fp(pct(v, p21), 0)} · 2026E 컨센 EPS {f0(eps)} 기준 {v / eps:.1f}배")
        print("  증권사별 최신(12개월 전체): " + ", ".join(f"{f} {f0(v[1])}({v[0][2:]})" for f, v in sorted(latest.items(), key=lambda x: x[1][0])))

        # ---------- 8/28 이후 구간 분해 (원장 prices 종가 — KRX 와 수백 원 차이가 있어 구간 수익률만 본다)
        print("[구간] 원장 prices 종가 기준, 같은 구간 KOSDAQ")
        cuts = ["2026-08-25", "2026-08-28", "2026-09-03", "2026-09-30", "2026-10-12", "2026-10-15", "2026-10-21"]
        for a, b in zip(cuts[:-1], cuts[1:]):
            print(f"  {a[5:]}→{b[5:]}  {nm} {fp(pct(lp[b], lp[a]))} ({f0(lp[a])}→{f0(lp[b])}) · KOSDAQ {fp(pct(kq[b], kq[a]))}")
        big = []
        ds = [d for d, _ in led["px"] if "2026-08-28" <= d <= ASOF]
        for a, b in zip(ds[:-1], ds[1:]):
            r = pct(lp[b], lp[a])
            if r <= -4:
                big.append(f"{b[5:]} {fp(r)}(KOSDAQ {fp(pct(kq[b], kq[a]))})")
        print("  −4% 이하 일간: " + ", ".join(big))


if __name__ == "__main__":
    main()
