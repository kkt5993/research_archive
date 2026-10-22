"""화장품 5종목 심층 업데이트(2026-10-21, 원장 기준) 계산 스크립트.

대상: 에이피알(278470) · 아모레퍼시픽(090430) · LG생활건강(051900) · 코스맥스(192820) · 한국콜마(161890)
지침: _seminar/DEEP_UPDATE_BRIEF.md

숫자의 출처
  - _manifest/데이터/화장품_원장대조_2026-10-21.json   10월 리포트 정리본·종가·8/28 대비
  - _manifest/데이터/화장품_이력.json                 DART 분기·네이버 컨센·목표가 월별·변경·월말 종가
  - _manifest/데이터/화장품_일별종가_2026-10-15_10-21.json  KRX 10/20·10/21 종가
  - _manifest/데이터/화장품_심층조회_2026-10-21.json    맥미니 원장 **읽기 전용 사본**(research.ro.duckdb) 조회 캐시
        (10/21 3Q 컨센 · reports.body 요약 · 12개월 일별 종가 고점 · LG생활건강 12개월 리포트 · 상상인 PDF 1쪽 텍스트)
  - BODY_Q3 (아래)                                     reports.body / 상상인 PDF 본문에 적힌 3Q26 영업이익 추정을 옮겨 적은 것

실행
  python3 _seminar/deep_cosmetics.py --fetch      # 원장 사본 조회 → 캐시 갱신 (ssh mini, 읽기 전용)
  python3 _seminar/deep_cosmetics.py [out.md]     # 캐시+데이터 파일로 표 렌더링 (기본: stdout)
"""
import json
import re
import statistics as st
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_manifest" / "데이터"
CACHE = DATA / "화장품_심층조회_2026-10-21.json"
TICKERS = ["278470", "090430", "051900", "192820", "161890"]
NAMES = {"278470": "에이피알", "090430": "아모레퍼시픽", "051900": "LG생활건강",
         "192820": "코스맥스", "161890": "한국콜마"}

# ---------------------------------------------------------------- fetch (read-only)
REMOTE = r'''
import duckdb, json, subprocess
DB = "/Users/benopenclaw/research-site/stable/warehouse/research.ro.duckdb"
c = duckdb.connect(DB, read_only=True)
T = %s
out = {}
for t in T:
    d = {}
    for item in ("op_income", "revenue"):
        r = c.execute("select value, snap_date from naver_consensus_snap where ticker=? and item=? and period='2026Q3E' and snap_date<='2026-10-21' order by snap_date desc limit 1", [t, item]).fetchone()
        d["cons1021_" + item] = [r[0], str(r[1])] if r else None
    d["bodies"] = [[str(a), b, cc, e, (f or "")[:900]] for a, b, cc, e, f in c.execute(
        "select published_at, firm, target_price, title, left(body,900) from reports where ticker=? and published_at>='2026-09-15' order by 1", [t]).fetchall()]
    r = c.execute("select d, close from prices where symbol=? and d between '2025-10-22' and '2026-10-21' order by close desc, d limit 1", [t]).fetchone()
    d["hi12m"] = [str(r[0]), r[1]]
    r = c.execute("select d, close from prices where symbol=? and d between '2025-10-22' and '2026-10-21' order by close asc, d limit 1", [t]).fetchone()
    d["lo12m"] = [str(r[0]), r[1]]
    d["ledger_close"] = {str(a): b for a, b in c.execute("select d, close from prices where symbol=? and d between '2026-10-20' and '2026-10-21'", [t]).fetchall()}
    d["reports12m"] = [[str(a), b, cc, e, f] for a, b, cc, e, f in c.execute(
        "select published_at, firm, target_price, opinion, title from reports where ticker=? and published_at between '2025-10-22' and '2026-10-21' order by 1", [t]).fetchall()]
    d["eps"] = [[str(a), b, p, v] for a, b, p, v in c.execute(
        "select published_at, firm, period, value from report_estimates where ticker=? and metric='eps' and period in ('2026E','2026F','2027E','2027F') and published_at>='2026-09-15' and dup_of is null order by 1,2", [t]).fetchall()]
    d["eps_90d"] = [[str(a), b, p, v] for a, b, p, v in c.execute(
        "select published_at, firm, period, value from report_estimates where ticker=? and metric='eps' and period in ('2026E','2026F','2027E','2027F') and published_at>='2026-07-23' and dup_of is null order by 1,2", [t]).fetchall()]
    ssi = []
    for a, path in c.execute("select published_at, path from report_pdf_files where ticker=? and firm like '%%상상인%%' and published_at between '2025-10-22' and '2026-10-21' and status='ok' order by 1", [t]).fetchall():
        try:
            txt = subprocess.run(["pdftotext", "-l", "1", "-layout", path, "-"], capture_output=True, text=True, timeout=60).stdout
        except Exception:
            txt = ""
        if not txt.strip():
            try:
                from pypdf import PdfReader
                txt = PdfReader(path).pages[0].extract_text() or ""
            except Exception as e:
                txt = "ERR " + str(e)
        title = c.execute("select title from reports where ticker=? and firm like '%%상상인%%' and published_at=? limit 1", [t, a]).fetchone()
        ssi.append([str(a), title[0] if title else None, txt[:2500]])
    d["ssi_pdf"] = ssi
    out[t] = d
print(json.dumps(out, ensure_ascii=False))
''' % json.dumps(TICKERS)


def fetch():
    r = subprocess.run(["ssh", "mini", "python3 -"], input=REMOTE, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        sys.exit(r.stderr)
    CACHE.write_text(json.dumps(json.loads(r.stdout), ensure_ascii=False, indent=1))
    print("cache ->", CACHE)


# ---------------------------------------------------------------- 본문 3Q 추정 (억원)
# reports.body(텔레그램·네이버 요약)와 상상인 PDF 1쪽에 적힌 숫자를 옮긴 것. basis: 회계 기준 표기.
# 증권사 칸이 빈 텔레그램 요약은 정리본(원장대조)이 맞춘 증권사로 적는다.
BODY_Q3 = {
    "278470": [  # 2026-10-13 프리뷰 일제 발간
        ("신한", "10-13", 1781, "관세환급 100억 반영, 기준 미기재"),
        ("SK", "10-13", 1802, "IFRS18 적용 전"),
        ("교보", "10-13", 1727, "IFRS18 적용 (적용 전 1,840–1,920)"),
        ("상상인", "10-13", 1686, "IFRS18 적용 (적용 전 1,870)"),
        ("메리츠", "10-13", 1678, "기준 미기재, OPM 21.6%"),
        ("신영", "10-13", 1838, "기준 미기재"),
        ("다올", "10-13", 1877, "기준 미기재"),
    ],
    "090430": [
        ("교보", "09-29", 1195, ""),
        ("LS", "10-06", 1110, ""),
        ("다올", "10-06", 1082, ""),
        ("SK", "10-08", 1084, ""),
    ],
    "051900": [
        ("교보", "09-29", 900, ""),
    ],
    "192820": [
        ("유안타", "10-07", 830, ""),
        ("현대차", "10-07", 745, "텔레그램 요약, 정리본 미포함"),
        ("SK", "10-07", 756, ""),
        ("교보", "10-07", 782, ""),
        ("하나", "10-07", 790, ""),
        ("메리츠", "10-07", 768, ""),
        ("다올", "10-07", 787, ""),
        ("NH", "10-07", 772, ""),
        ("신영", "10-08", 781, ""),
        ("삼성", "10-08", 789, ""),
    ],
    "161890": [
        ("유안타", "09-29", 977, ""),
        ("KB", "10-06", 950, "제목 기재"),
        ("NH", "10-07", 918, ""),
        ("삼성", "10-09", 905, ""),
        ("교보", "10-12", 912, ""),
        ("다올", "10-12", 906, ""),
        ("SK", "10-14", 957, ""),
        ("상상인", "10-19", 873, ""),
    ],
}
# IFRS18(외화환산손익 영업이익 반영) 기준이 명시된 에이피알 추정 쌍: (적용 후, 적용 전)
APR_IFRS18_PAIRS = {"상상인": (1686, 1870), "교보": (1727, (1840 + 1920) / 2)}


# ---------------------------------------------------------------- helpers
def r0(x):
    return int(Decimal(str(x)).quantize(Decimal("1"), ROUND_HALF_UP))


def r1(x):
    return float(Decimal(str(x)).quantize(Decimal("0.1"), ROUND_HALF_UP))


def pct(a, b):
    return r1((a / b - 1) * 100)


def sp(x, unit=""):
    """부호 붙인 퍼센트 문자열 (마이너스는 −)."""
    s = f"{x:+.1f}%".replace("-", "−")
    return s


def won(x):
    return f"{r0(x):,}"


QKEYS = [("1Q25", "2025-03-31", "2024-03-31"), ("2Q25", "2025-06-30", "2024-06-30"),
         ("3Q25", "2025-09-30", "2024-09-30"), ("4Q25", "2025-12-31", "2024-12-31"),
         ("1Q26", "2026-03-31", "2025-03-31"), ("2Q26", "2026-06-30", "2025-06-30")]


def load():
    L = json.loads((DATA / "화장품_원장대조_2026-10-21.json").read_text())
    H = json.loads((DATA / "화장품_이력.json").read_text())
    D = json.loads((DATA / "화장품_일별종가_2026-10-15_10-21.json").read_text())
    C = json.loads(CACHE.read_text())
    return L, H, D, C


def ssi_tp(txt):
    """상상인 PDF 1쪽의 '종가(yy.mm.dd) X원' · '상승여력 Y%' 로 목표가 역산(만원 단위 반올림 전 값)."""
    m1 = re.search(r"종가\((\d\d\.\d\d\.\d\d)\)\s*([\d,]+)원", txt)
    m2 = re.search(r"상승여력\s*(-?[\d.]+)%", txt)
    if not (m1 and m2):
        return None
    px = int(m1.group(2).replace(",", ""))
    up = float(m2.group(1))
    raw = px * (1 + up / 100)
    return {"base_date": m1.group(1), "close": px, "upside": up, "tp_raw": r0(raw),
            "tp_10k": r0(raw / 10000) * 10000}


def render(t, L, H, D, C):
    a, h, d, c = L[t], H[t], D[t], C[t]
    out = []
    P = out.append
    name = NAMES[t]
    dq = h["dart_q"]
    px = d["2026-10-21"]
    px0 = d["2026-10-20"]
    P(f"\n\n######## {name} ({t})\n")

    # ---------------- A
    cons_op = c["cons1021_op_income"][0]
    cons_rev = c["cons1021_revenue"][0] if c["cons1021_revenue"] else None
    q3_25_op = dq["2025-09-30|op_income"]
    q3_25_rev = dq["2025-09-30|revenue"]
    m10 = h["px_monthly"]["2025-10"]
    hi_d, hi = c["hi12m"]
    if a.get("hi_date") == hi_d:  # 같은 날이면 KRX(정리본) 값 우선 — 원장 prices 종가는 KRX 와 수백원씩 다르다
        hi = a["hi"]
    lo_d, lo = c["lo12m"]
    rev2, op2 = dq["2026-06-30|revenue"], dq["2026-06-30|op_income"]
    rev2p, op2p = dq["2025-06-30|revenue"], dq["2025-06-30|op_income"]
    bq = [x[2] for x in BODY_Q3[t]]
    bq_med = st.median(bq)
    P("### A")
    P(f"- 주가 10/21 KRX {won(px)} (10/20 {won(px0)}, {sp(pct(px, px0))})")
    P(f"- 원장 prices 10/21 종가 {c['ledger_close'].get('2026-10-21')} (KRX 와 차이 {px - c['ledger_close'].get('2026-10-21', px):+,.0f})")
    P(f"- 8/28 {won(a['close_0828'])} → {sp(pct(px, a['close_0828']))}")
    P(f"- 12M 고점(원장 prices 종가, 같은 날이면 KRX) {won(hi)} ({hi_d}) → {sp(pct(px, hi))} · 12M 저점 {won(lo)} ({lo_d}) → {sp(pct(px, lo))}")
    P(f"- 12M 전 2025-10 월말 {won(m10)} → {sp(pct(px, m10))}")
    P(f"- 2Q26 매출 {won(rev2)} ({sp(pct(rev2, rev2p))}) · 영업이익 {won(op2)} ({sp(pct(op2, op2p))}) · OPM {r1(op2 / rev2 * 100)}%")
    P(f"- 3Q26 컨센(네이버 {c['cons1021_op_income'][1]}) 영업이익 {won(cons_op)} YoY {sp(pct(cons_op, q3_25_op))} (3Q25 {won(q3_25_op)})"
      + (f" · 매출 {won(cons_rev)} YoY {sp(pct(cons_rev, q3_25_rev))}" if cons_rev else ""))
    nc = h["naver_cons"]["2026Q3E|op_income"]
    P(f"- 컨센 이동 10/4 {won(nc['first'][1])} → 10/21 {won(nc['last'][1])} ({sp(pct(nc['last'][1], nc['first'][1]))})")
    if a["q3"]:
        P(f"- 정리본 3Q 추정 {a['q3']} 중앙값 {a['q3_med']} → 컨센 대비 {sp(pct(a['q3_med'], cons_op))}")
    P(f"- 본문 3Q 추정 {len(bq)}곳 {min(bq):,}–{max(bq):,} 중앙값 {bq_med:,} → 컨센 대비 {sp(pct(bq_med, cons_op))} · YoY {sp(pct(bq_med, q3_25_op))}")
    for f, dt, v, note in BODY_Q3[t]:
        P(f"    - {f} {dt}: {v:,} (컨센 대비 {sp(pct(v, cons_op))}) {note}")
    if a["tp_med"]:
        P(f"- 10월 목표가 중앙값 {won(a['tp_med'])} ({a['n']}곳, {won(a['tp_rng'][0])}–{won(a['tp_rng'][1])}) · 8/28 {won(a['tp0828'])} 대비 {sp(a['tp_med_vs0828_pct'])}")

    # ---------------- B
    P("\n### B 분기 표")
    P("| 분기 | 매출(억) | 영업이익(억) | OPM | 매출 YoY | 영업이익 YoY |")
    P("|---|---:|---:|---:|---:|---:|")
    for q, k, kp in QKEYS:
        rv, op = dq[f"{k}|revenue"], dq[f"{k}|op_income"]
        rvp, opp = dq[f"{kp}|revenue"], dq[f"{kp}|op_income"]
        oy = sp(pct(op, opp)) if opp > 0 and op > 0 else ("적전" if op < 0 <= opp else ("흑전" if opp < 0 <= op else "적지"))
        P(f"| {q} | {rv:,} | {op:,} | {r1(op / rv * 100)}% | {sp(pct(rv, rvp))} | {oy} |")
    if cons_rev:
        P(f"| **3Q26E 컨센** (네이버 10/21) | {won(cons_rev)} | **{won(cons_op)}** | {r1(cons_op / cons_rev * 100)}% | {sp(pct(cons_rev, q3_25_rev))} | {sp(pct(cons_op, q3_25_op))} |")
    P(f"| 3Q26E 원장 리포트 본문 중앙값 ({len(bq)}곳) | | {bq_med:,} | | | {sp(pct(bq_med, q3_25_op))} |")
    # 1H 누계, QoQ
    P(f"- 2Q26 QoQ 매출 {sp(pct(rev2, dq['2026-03-31|revenue']))} 영업이익 {sp(pct(op2, dq['2026-03-31|op_income']))}")
    P(f"- 3Q 컨센 QoQ 영업이익 {sp(pct(cons_op, op2))}" + (f" 매출 {sp(pct(cons_rev, rev2))}" if cons_rev else ""))
    for yr in ("2026E",):
        k = f"{yr}|op_income"
        if k in h["naver_cons"]:
            n = h["naver_cons"][k]
            P(f"- 네이버 {yr} 영업이익 10/4 {won(n['first'][1])} → 10/21 {won(n['last'][1])} ({sp(pct(n['last'][1], n['first'][1]))})")
    s1 = sum(dq[f"{k}|op_income"] for k in ("2026-03-31", "2026-06-30"))
    P(f"- 1H26 영업이익 {s1:,} · 2025 연간 {sum(dq[f'{k}|op_income'] for k in ('2025-03-31','2025-06-30','2025-09-30','2025-12-31')):,}")

    # ---------------- C
    P("\n### C ① 목표가 월별 중앙값")
    P(" → ".join(f"{m['m'][2:].replace('-', '/')} {won(m['med'])}({m['n']})" for m in h["tp_monthly"]))
    first = h["tp_monthly"][0]["med"]
    last = h["tp_monthly"][-1]["med"]
    peak = max(h["tp_monthly"], key=lambda m: m["med"])
    P(f"- 처음 {won(first)} → 최근 {won(last)} ({sp(pct(last, first))}); 고점 {peak['m']} {won(peak['med'])}, 최근은 고점 대비 {sp(pct(last, peak['med']))}")
    ch = h["tp_changes"]
    up = sum(1 for x in ch if x["pct"] > 0)
    dn = sum(1 for x in ch if x["pct"] < 0)
    P(f"- 12M 목표가 변경 {len(ch)}건: 상향 {up} · 하향 {dn}")
    P("### C ② 큰 변경 (|%| 상위)")
    for x in sorted(ch, key=lambda x: -abs(x["pct"]))[:7]:
        P(f"- {x['date']} {x['firm']} {won(x['prev'])}→{won(x['tp'])} ({sp(x['pct'])}) 「{x['title']}」 {x['op']}")
    P("### C ③ 10월 정리본")
    for o in a["oct"]:
        chg = sp(o["chg"]) if o["chg"] is not None else "—"
        prev = won(o["prev"]) if o["prev"] else "—"
        P(f"- {o['firm']} {o['date']} {prev}→{won(o['tp'])} {chg} q3={o['q3']} src={o['src']} 「{o['title']}」 상방 {sp(pct(o['tp'], px))}")

    # 상상인
    P("### 상상인 PDF")
    for dt, title, txt in c["ssi_pdf"]:
        info = ssi_tp(txt)
        P(f"- {dt} 「{title}」 → {info}" + (f" · 현재가 대비 {sp(pct(info['tp_10k'], px))}" if info else ""))

    # ---------------- E
    P("\n### E 시나리오")
    if a["n"] >= 3:
        lo_tp, base_tp, hi_tp = a["tp_rng"][0], a["tp_med"], a["tp_rng"][1]
        P(f"- 근거: 10월 원장 {a['n']}곳")
    else:
        # 10월 3곳 미만 → 12개월(10/22/25–10/21/26) 증권사별 최신 목표가로 보충 (증권사 미상 제외)
        latest = {}
        for dt, firm, tp, op, title in c["reports12m"]:
            if tp and firm:
                latest[firm] = (dt, tp, op, title)
        vals = sorted(v[1] for v in latest.values())
        lo_tp, base_tp, hi_tp = vals[0], st.median(vals), vals[-1]
        P(f"- 근거: 10월 {a['n']}곳 → 12개월 증권사별 최신 {len(vals)}곳 보충")
        for firm, v in sorted(latest.items(), key=lambda kv: kv[1][1]):
            P(f"    - {firm} {v[0]} {won(v[1])} {v[2]} 「{v[3]}」")
        unk = [(dt, tp, title) for dt, firm, tp, op, title in c["reports12m"] if tp and not firm]
        P(f"    - (증권사 미상 제외: {unk})")
    for lab, v in (("Bull", hi_tp), ("Base", base_tp), ("Bear", lo_tp)):
        P(f"- {lab} {won(v)} → 현재가 대비 {sp(pct(v, px))}")
    # 시장이 매긴 값: 리포트 EPS 기준 배수 (있으면)
    if c["eps"]:
        for dt, firm, per, v in c["eps"]:
            P(f"- EPS {firm} {dt} {per} {v:,.0f} → 현재가 PER {r1(px / v)}배 · Base 목표가 PER {r1(base_tp / v)}배")
    P(f"- 현재가/Bear {sp(pct(px, lo_tp))}")
    # 90일(7/23–) 증권사별 최신 EPS 중앙값 기준 PER
    for fy in ("2026", "2027"):
        latest = {}
        for dt, firm, per, v in c["eps_90d"]:
            if per.startswith(fy):
                latest[firm] = (dt, v)
        if latest:
            vals = [v for _, v in latest.values()]
            m = st.median(vals)
            P(f"- {fy}E EPS 90일 증권사별 최신 {len(vals)}곳 중앙값 {won(m)} ({', '.join(f'{k} {v[0][5:]} {won(v[1])}' for k, v in latest.items())}) → 현재가 PER {r1(px / m)}배 · Bull {r1(hi_tp / m)} · Base {r1(base_tp / m)} · Bear {r1(lo_tp / m)}배")
    return "\n".join(out)


# D절 '당시 판단' — 화장품의류완구_코스피200_종목분석.md §3 (2026-08-28 기준)에 적힌 값
#   (원장 리포트 90일 목표가 중앙값, 2026E 영업이익 원장 리포트 중앙값 억원, QuantiWise 7/30 목표가)
PREV0828 = {"278470": (540000, 7448, 530526), "090430": (178000, 4842, 166941), "051900": (342500, 3750, 268000),
            "192820": (280000, 2486, 247389), "161890": (160000, 3346, 132526)}


def d_checks(L, H, D, C):
    out = ["\n\n######## D절 계산"]
    for t in TICKERS:
        a, h, c = L[t], H[t], C[t]
        px = D[t]["2026-10-21"]
        tp0, op0, qw0 = PREV0828[t]
        op26 = h["naver_cons"]["2026E|op_income"]["last"][1]
        tp_now = a["tp_med"]
        nt = h["naver_target"]["last"][1]
        out.append(f"- {NAMES[t]}: 8/28 원장TP {won(tp0)} (8/28 종가 {won(a['close_0828'])} 대비 {sp(pct(tp0, a['close_0828']))}) → 10월 {won(tp_now)} ({sp(pct(tp_now, tp0))}) · 현재가 대비 {sp(pct(tp_now, px))}"
                   f" | 2026E OP 원장 {op0:,} → 네이버 10/21 {won(op26)} ({sp(pct(op26, op0))}) | QW 7/30 TP {won(qw0)} vs 네이버 목표가 평균 10/21 {won(nt)} ({sp(pct(nt, qw0))})")
        latest = {}
        for dt, firm, per, v in c["eps_90d"]:
            if per.startswith("2026"):
                latest[firm] = v
        if latest:
            m = st.median(latest.values())
            out.append(f"    - 2026E EPS 중앙값 {won(m)} 기준 PER: 8/28 {r1(a['close_0828'] / m)}배 → 10/21 {r1(px / m)}배")
    # 한국콜마 시총: 상상인 PDF 10/16 시총 × 주가비
    out.append(f"- 한국콜마 시총 근사(상상인 PDF 10/16 30,639억 × 127,300/129,800) {won(30639 * 127300 / 129800)}억")
    # 에이피알 상상인 지역 표 (십억원): 북미 3Q26E 367 vs 3Q25 164, 유럽 172 vs 21, 한국 53 vs 78
    for k, (a1, b1) in {"북미": (367, 164), "유럽": (172, 21), "한국": (53, 78), "아시아": (118, 104)}.items():
        out.append(f"- 에이피알 상상인 3Q26E {k} {a1} vs 3Q25 {b1} 십억원 → {sp(pct(a1, b1))}")
    # 코스맥스 OPM 2Q26·3Q 컨센 vs 한국콜마
    for t in ("192820", "161890"):
        dq = H[t]["dart_q"]
        out.append(f"- {NAMES[t]} 2Q26 OPM {r1(dq['2026-06-30|op_income'] / dq['2026-06-30|revenue'] * 100)}% · 2Q26 영업이익 {dq['2026-06-30|op_income']:,}")
    # 1H26 영업이익 / 2025 연간
    for t in TICKERS:
        dq = H[t]["dart_q"]
        h1 = dq["2026-03-31|op_income"] + dq["2026-06-30|op_income"]
        y25 = sum(dq[f"{k}|op_income"] for k in ("2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31"))
        out.append(f"- {NAMES[t]} 1H26 영업이익 {h1:,} / 2025 연간 {y25:,} = {r1(h1 / y25 * 100)}%")
    # 코스맥스: 정리본 11곳 + 현대차(텔레그램 380,000, 10/7) 포함 시 중앙값
    v = [o["tp"] for o in L["192820"]["oct"]] + [380000.0]
    out.append(f"- 코스맥스 현대차 포함 {len(v)}곳 중앙값 {won(st.median(v))} 범위 {won(min(v))}–{won(max(v))}")
    # 코스맥스: 10월 리포트들이 인용한 컨센 677억 대비 본문 중앙값
    bq = st.median([x[2] for x in BODY_Q3["192820"]])
    out.append(f"- 코스맥스 본문 중앙값 {bq} vs 10/4 컨센 677 {sp(pct(bq, 677))} · vs 10/21 761 {sp(pct(bq, 761))} · 상단 830 vs 761 {sp(pct(830, 761))}")
    # 아모레퍼시픽: 4월 문서 디레이팅 하단 22배 × 2026E EPS 중앙값
    eps = st.median({f: v for dt, f, per, v in C["090430"]["eps_90d"] if per.startswith("2026")}.values())
    out.append(f"- 아모레퍼시픽 22배 × 2026E EPS {won(eps)} = {won(22 * eps)}원 (현재가 대비 {sp(pct(22 * eps, D['090430']['2026-10-21']))})")
    return "\n".join(out)


def extra(L, H, D, C):
    out = ["\n\n######## 에이피알 IFRS18 차이"]
    for f, (post, pre) in APR_IFRS18_PAIRS.items():
        out.append(f"- {f}: 적용 후 {post:,} · 적용 전 {pre:,.0f} → 차이 {pre - post:,.0f}억 ({sp(pct(post, pre))})")
    cons = C["278470"]["cons1021_op_income"][0]
    q2 = H["278470"]["dart_q"]["2026-06-30|op_income"]
    out.append(f"- 컨센 {cons:,} vs IFRS18 적용 추정 상상인 {sp(pct(1686, cons))} · 교보 {sp(pct(1727, cons))} / 적용 전 SK {sp(pct(1802, cons))} · 상상인 {sp(pct(1870, cons))}")
    out.append(f"- 2Q26 DART {q2:,} (상상인 표: 18호 적용 1,910 vs 적용 전 1,850 — 십억원 191/185)")
    # 원/달러
    fx = H["_usdkrw_monthend"]
    out.append(f"- 원/달러 6월말 {fx['202606'][1]} → 9월말 {fx['202609'][1]} → 10/21 {fx['202610'][1]} : 6월말 대비 {sp(pct(fx['202610'][1], fx['202606'][1]))}, 3Q 평균 근사 불가(월말만)")
    out.append(f"- 2Q25말 {fx['202506'][1] if '202506' in fx else 'NA'} · 2025-09말 {fx['202509'][1]} → 10/21 YoY 근사 {sp(pct(fx['202610'][1], fx['202509'][1]))}")
    return "\n".join(out)


if __name__ == "__main__":
    if "--fetch" in sys.argv:
        fetch()
        sys.exit(0)
    L, H, D, C = load()
    text = "".join(render(t, L, H, D, C) for t in TICKERS) + d_checks(L, H, D, C) + extra(L, H, D, C)
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(text)
        print("->", sys.argv[1])
    else:
        print(text)
