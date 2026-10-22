"""인터넷·게임 5종목 심층 업데이트(2026-10-21) 계산 스크립트.

대상: NHN(181710) · NAVER(035420) · 카카오(035720) · 크래프톤(259960) · NC(036570)
산출 문서: 10_국내주식/20_소프트웨어/<종목명>_심층분석리포트.md (A–F절의 숫자)

입력
- _manifest/데이터/인터넷게임_원장대조_2026-10-21.json  10월 리포트 정리본·종가·8/28 대비
- _manifest/데이터/인터넷게임_이력.json                 dart_q·naver_cons·tp_monthly·tp_changes·px_monthly
- _manifest/데이터/인터넷게임_일별종가_2026-10-15_10-21.json  KRX 10/20·10/21 종가
- 아래 RO 상수: 맥미니 원장 읽기 전용 사본(research.ro.duckdb)을 2026-10-22 에 조회한 값.
  쿼리는 DEEP_UPDATE_BRIEF.md 의 것(naver_consensus_snap 10/21, reports 본문 09-15 이후)과
  prices(12개월 최고 종가·리포트 발간 전 종가). 본문에서 읽은 숫자는 증권사·발간일과 같이 적었다.

실행: python3 _seminar/deep_internet_game.py  → 종목별 계산값을 출력한다. 문서의 숫자는 이 출력에서 옮겼다.
"""
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "_manifest" / "데이터"
OCT = json.loads((D / "인터넷게임_원장대조_2026-10-21.json").read_text())
HIST = json.loads((D / "인터넷게임_이력.json").read_text())
DAILY = json.loads((D / "인터넷게임_일별종가_2026-10-15_10-21.json").read_text())

CODES = ["181710", "035420", "035720", "259960", "036570"]
MINUS = "−"

# ── 원장 읽기 전용 사본 조회값 (2026-10-22) ────────────────────────────────
RO = {
    # naver_consensus_snap, period=2026Q3E, snap_date<=2026-10-21 (이력.json last 와 같다 — 대조용)
    "cons_q3_1021": {
        "181710": (7646, 539), "035420": (35146, 5000), "035720": (20493, 2522),
        "259960": (11248, 2801), "036570": (7010, 1007),
    },
    # prices: 2025-10-22–2026-10-21 최고 종가 (원장 prices — KRX 종가와 ±1% 다를 수 있다)
    "hi12": {
        "181710": ("2026-08-21", 75200), "035420": ("2026-01-29", 287000),
        "035720": ("2025-10-29", 67700), "259960": ("2026-05-14", 293500),
        "036570": ("2026-06-02", 338000),
    },
    # 원장 prices 10/21 종가 (KRX 일별종가 파일과 대조용)
    "px1021_ledger": {"181710": 56400, "035420": 179500, "035720": 30950, "259960": 194500, "036570": 214000},
    # reports.body 에서 읽은 3Q26 영업이익 추정(억원). report_estimates 정리본(oct.q3)에 없는 것 포함
    "q3_body": {
        "181710": {"한화 10/8": 549, "메리츠 9/25(9월)": 536},
        "035420": {"LS 10/1": 4910, "하나 10/2": 4789, "한화 10/2": 4925, "대신 10/2": 4493,
                   "교보 10/6": 4824, "유진 10/7": 4893, "메리츠 10/11": 4858, "NH 10/12": 5030, "DB 10/13": 4909},
        "035720": {"한화 10/6": 2385, "다올 10/12": 2412, "대신 10/13": 2240, "LS 10/15": 2280},
        "259960": {"교보 10/6": 2526, "하나 10/12": 2442, "유진 10/12": 2501, "유안타 10/13": 2611,
                   "다올 10/13": 2484, "메리츠 10/13": 2942},
        "036570": {"삼성 10/2": 1089, "유진 10/6": 1133, "메리츠 10/7": 1063, "하나 10/12": 1022,
                   "교보 10/12": 1059, "유안타 10/13": 1045, "다올 10/15": 980},
    },
    # NHN 2Q26 부문 매출(억원)·YoY — 교보 8/12 본문. 합계와 연결 매출의 차이는 기타·연결조정
    "nhn_seg_2q26": {"게임": (1396, 21.5), "결제(KCP 등)": (3940, 27.3), "기술(클라우드·테코러스)": (1598, 52.9)},
    # NHN 9–10월 리포트 목표가 (원장). 메리츠는 9/21 네이버 행 80,000 · 9/25 텔레그램 행은 목표가 칸 빈 값(본문 "6.4만원->8만원")
    "nhn_tp_sep_oct": {"미래에셋 9/18": 80000, "메리츠 9/21·9/25": 80000, "삼성 9/23→10/8 유지": 92000, "한화 10/8": 87000},
    # 배수 역산용: 리포트가 말한 PER 과 그 기준 주가
    "per_refs": {
        "181710": ("메리츠 9/21·9/25 '2027년 PER 11.7배'", 11.7, 56700, "발간 직전 원장 종가 9/18"),
        "035420": ("DB 10/13 '2026년 예상 P/E 14.9배'", 14.9, 183800, "발간 직전 원장 종가 10/8"),
        "035720": ("미상 10/14 '27년 EPS × 역사적 하단 P/E 25배 = 42,000원'", 25.0, 42000, "목표가 자체"),
        "259960": ("다올 10/13 'Fwd 12M P/E 13.0배 → 310,000원'", 13.0, 310000, "목표가 자체"),
        "036570": ("하나 10/11 'P/E 9.76배'(현재가 222,000원 기준)", 9.76, 222000, "본문 현재가"),
    },
    # 기준일(10/21) 뒤 원장에 들어온 리포트 — 중앙값에 넣지 않는다
    "after_cutoff": {"259960": ("미래에셋 10/22", 280000, "잠시 쉬어가는 구간"),
                     "036570": ("미래에셋 10/22", 300000, "AI 시대, 우월전략을 갖춘 게임사")},
    # 정리본에 빠진 10월 행
    "nc_hyundai": ("현대차 10/2", 380000, "원장 목표가 칸 비어 있음 · 제목 'TP 380,000원' · 같은 날 미상 요약 380,000원"),
}
KOSPI = {"0828": 6788.88, "1021": 5735.66}


def pct(a, b):
    return (a / b - 1) * 100


def fp(x, nd=1):
    if x is None:
        return "—"
    s = f"{abs(x):.{nd}f}%"
    return ("+" if x > 0 else MINUS if x < 0 else "") + s


def w(x):
    return f"{int(round(x)):,}"


QS = ["2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31", "2026-03-31", "2026-06-30"]


def qlab(d):
    y, m, _ = d.split("-")
    return f"{(int(m) - 1) // 3 + 1}Q{y[2:]}"


def prev_year(d):
    y, rest = d.split("-", 1)
    return f"{int(y) - 1}-{rest}"


def yoy(cur, base):
    if base is None:
        return None
    if base <= 0 and cur > 0:
        return "흑전"
    if base > 0 and cur <= 0:
        return "적전"
    if base <= 0 and cur <= 0:
        return "적지"
    return pct(cur, base)


def fy(v):
    return v if isinstance(v, str) else fp(v)


def run(c):
    o, h = OCT[c], HIST[c]
    dq = h["dart_q"]
    out = {"name": o["name"]}
    # A
    c21, c20 = DAILY[c]["2026-10-21"], DAILY[c]["2026-10-20"]
    hi_d, hi = RO["hi12"][c]
    m25 = h["px_monthly"]["2025-10"]
    out["A"] = {
        "close_1021": c21, "close_1020": c20, "d1": fp(pct(c21, c20)),
        "close_0828": o["close_0828"], "vs0828": fp(pct(c21, o["close_0828"])),
        "kospi_vs0828": fp(pct(KOSPI["1021"], KOSPI["0828"])),
        "rel_kospi_pp": round(pct(c21, o["close_0828"]) - pct(KOSPI["1021"], KOSPI["0828"]), 1),
        "hi12": (hi_d, hi), "vs_hi12": fp(pct(c21, hi)),
        "px_2025_10": m25, "vs_12m": fp(pct(c21, m25)),
        "ledger_px1021": RO["px1021_ledger"][c], "krx_vs_ledger": fp(pct(c21, RO["px1021_ledger"][c])),
    }
    # B: 분기
    rows = []
    for q in QS:
        r, op = dq[f"{q}|revenue"], dq[f"{q}|op_income"]
        rb, ob = dq.get(f"{prev_year(q)}|revenue"), dq.get(f"{prev_year(q)}|op_income")
        rows.append((qlab(q), r, op, fp(op / r * 100).lstrip("+"), fy(yoy(r, rb)), fy(yoy(op, ob))))
    rev_c, op_c = RO["cons_q3_1021"][c]
    assert op_c == h["naver_cons"]["2026Q3E|op_income"]["last"][1], "10/21 컨센 불일치"
    r25, o25 = dq["2025-09-30|revenue"], dq["2025-09-30|op_income"]
    rows.append(("3Q26E 컨센", rev_c, op_c, f"{op_c / rev_c * 100:.1f}%", fy(yoy(rev_c, r25)), fy(yoy(op_c, o25))))
    out["B"] = rows
    out["2Q26_qoq_op"] = fp(pct(dq["2026-06-30|op_income"], dq["2026-03-31|op_income"]))
    out["3Q_cons_qoq_op"] = fp(pct(op_c, dq["2026-06-30|op_income"]))
    first = h["naver_cons"]["2026Q3E|op_income"]["first"]
    out["cons_move_oct"] = (first[1], op_c, fp(pct(op_c, first[1])))
    fy26 = h["naver_cons"]["2026E|op_income"]
    out["cons_2026E_op"] = (fy26["first"][1], fy26["last"][1], fp(pct(fy26["last"][1], fy26["first"][1])))
    out["naver_target_avg"] = (h["naver_target"]["first"][1], h["naver_target"]["last"][1],
                               fp(pct(h["naver_target"]["last"][1], h["naver_target"]["first"][1])))
    # 연간 실적 (2025 DART 합)
    out["rev_2025"] = sum(dq[f"{q}|revenue"] for q in QS[:4])
    out["op_2025"] = sum(dq[f"{q}|op_income"] for q in QS[:4])
    out["1H26_opm"] = f"{(dq['2026-03-31|op_income'] + dq['2026-06-30|op_income']) / (dq['2026-03-31|revenue'] + dq['2026-06-30|revenue']) * 100:.1f}%"
    out["2025_opm"] = f"{out['op_2025'] / out['rev_2025'] * 100:.1f}%"
    # 3Q 원장 추정: 정리본(report_estimates) + 본문
    q3_tab = {k: v[0] for k, v in o["q3"].items()}
    est = list(q3_tab.values())
    out["q3_tab"] = q3_tab
    if est:
        med = statistics.median(est)
        out["q3_tab_med"] = (med, min(est), max(est), fp(pct(med, op_c)), fy(yoy(med, o25)))
    body = RO["q3_body"][c]
    bv = [v for k, v in body.items() if "9월" not in k]
    bm = statistics.median(bv)
    out["q3_body"] = body
    out["q3_body_med"] = (bm, min(bv), max(bv), len(bv), fp(pct(bm, op_c)), fy(yoy(bm, o25)))
    out["q3_body_each_vs_cons"] = {k: fp(pct(v, op_c)) for k, v in body.items()}
    # 목표가
    out["tp_oct"] = (o["tp_med"], o["n"], o["tp_rng"], fp(pct(o["tp_med"], c21)))
    out["tp_0828"] = (o["tp0828"], fp(pct(o["tp_med"], o["tp0828"])))
    out["tp_path"] = " → ".join(f"{r['m'][2:4]}/{r['m'][5:]} {w(r['med'])}({r['n']})" for r in h["tp_monthly"])
    ch = h["tp_changes"]
    out["tp_changes_n"] = (len(ch), sum(1 for x in ch if x["pct"] > 0), sum(1 for x in ch if x["pct"] < 0))
    out["tp_changes_big"] = sorted(ch, key=lambda x: -abs(x["pct"]))[:6]
    out["oct_rows"] = [(r["date"][5:].replace("-", "/"), r["firm"], r["prev"], r["tp"], r["chg"], r["q3"], r["title"]) for r in o["oct"]]
    out["n_up_down_flat"] = (o["n_up"], o["n_down"], o["n_flat"])
    # E 시나리오
    lo, hi_tp = o["tp_rng"]
    scen = {"Bull": hi_tp, "Base": o["tp_med"], "Bear": lo}
    if c == "181710":  # 10월 2곳 → 9–10월 4곳으로 보충
        v = list(RO["nhn_tp_sep_oct"].values())
        scen = {"Bull": max(v), "Base": statistics.median(v), "Bear": min(v)}
        out["nhn_sep_oct"] = (statistics.median(v), min(v), max(v), len(v))
    out["E"] = {k: (v, fp(pct(v, c21))) for k, v in scen.items()}
    # 배수 역산
    label, per, ref_px, basis = RO["per_refs"][c]
    out["per_implied"] = (label, per, ref_px, basis, round(per * c21 / ref_px, 1))
    if c in RO["after_cutoff"]:
        f, tp, t = RO["after_cutoff"][c]
        out["after_cutoff"] = (f, tp, t, fp(pct(tp, c21)))
    return out


def nhn_extra():
    seg = RO["nhn_seg_2q26"]
    total = HIST["181710"]["dart_q"]["2026-06-30|revenue"]
    s = {k: (v, y, f"{v / total * 100:.1f}%") for k, (v, y) in seg.items()}
    seg_sum = sum(v for v, _ in seg.values())
    s["기타·연결조정(잔여)"] = (total - seg_sum, None, f"{(total - seg_sum) / total * 100:.1f}%")
    # 3축만의 비중
    s3 = {k: f"{v / seg_sum * 100:.1f}%" for k, (v, _) in seg.items()}
    # 클라우드: 메리츠 '25 2,600억 → '29 1.2조 CAGR 확인
    cagr = ((12000 / 2600) ** (1 / 4) - 1) * 100
    # GPUaaS: 25MW × 300억/MW
    return {"seg": s, "seg3": s3, "seg_sum": seg_sum, "total": total,
            "meritz_cloud_cagr": f"{cagr:.1f}%", "mw_x_rev": 25 * 300,
            # 삼성 9/23 신규 30MW 매출 범위 1,500–7,500억: 메리츠 클라우드 '25 매출 2,600억 대비 배수, 2025 연결 매출 대비 비중
            "range_x_cloud2025": (round(1500 / 2600, 2), round(7500 / 2600, 2)),
            "range_share_of_2025_rev": (f"{1500 / 25162 * 100:.1f}%", f"{7500 / 25162 * 100:.1f}%"),
            # 시가총액 근사: 8/28 문서 '2.3조'(69,700원) × 종가 비율 → 삼성 클라우드 적정가치 1.6조와 비교
            "mcap_1021_approx_jo": round(2.3 * 57100 / 69700, 2),
            "samsung_cloud_value_share": f"{1.6 / (2.3 * 57100 / 69700) * 100:.0f}%",
            # 메리츠 PER 11.7배 기준 2027E EPS 역산(발간 직전 원장 종가 56,700)
            "meritz_eps27_implied": round(56700 / 11.7)}


def nc_extra():
    tps = [r["tp"] for r in OCT["036570"]["oct"]] + [RO["nc_hyundai"][1]]
    return {"with_hyundai_med": statistics.median(tps), "n": len(tps)}


def kakao_extra():
    o = OCT["035720"]
    tps_wo_unknown = [r["tp"] for r in o["oct"] if r["firm"] != "미상"]
    dq = HIST["035720"]["dart_q"]
    return {"med_wo_unknown": statistics.median(tps_wo_unknown), "n": len(tps_wo_unknown),
            "q3_25_dart": dq["2025-09-30|op_income"], "q3_25_tab": o["q3_25"],
            "q3_yoy_tab_basis": fp(pct(o["q3_med"], o["q3_25"])), "q3_yoy_dart_basis": fp(pct(o["q3_med"], dq["2025-09-30|op_income"])),
            "op_2q_yoy": fp(pct(dq["2026-06-30|op_income"], dq["2025-06-30|op_income"]))}


if __name__ == "__main__":
    res = {c: run(c) for c in CODES}
    res["_nhn"] = nhn_extra()
    res["_nc"] = nc_extra()
    res["_kakao"] = kakao_extra()
    # 이전 판단 대조에 쓰는 값
    prev = {
        "035420": {"§7 Base 26만 대비": fp(pct(OCT["035420"]["close_1021"], 260000)),
                   "§7 Bear 16만 대비": fp(pct(OCT["035420"]["close_1021"], 160000)),
                   "§7 2026-04 22만 대비": fp(pct(OCT["035420"]["close_1021"], 220000))},
        "035720": {"§7 Bear 4.5만 대비": fp(pct(OCT["035720"]["close_1021"], 45000)),
                   "§7 Base 7만 대비": fp(pct(OCT["035720"]["close_1021"], 70000)),
                   "§7 2026-04 6만 대비": fp(pct(OCT["035720"]["close_1021"], 60000))},
        "8/28 QW·원장 26E OP → 10/21 네이버 26E": {
            "181710": fp(pct(HIST["181710"]["naver_cons"]["2026E|op_income"]["last"][1], 1781)),
            "035720": fp(pct(HIST["035720"]["naver_cons"]["2026E|op_income"]["last"][1], 9474)),
            "036570": fp(pct(HIST["036570"]["naver_cons"]["2026E|op_income"]["last"][1], 4987)),
        },
    }
    res["_prev"] = prev
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
