# -*- coding: utf-8 -*-
"""06_기계 코스피200 종목 — 원장에서 컨센서스·리포트 근거를 뽑아 JSON 으로 낸다.
   맥미니에서만 돈다(원장이 여기 있다). 읽기 전용.
"""
import duckdb, json, os, re, statistics, datetime, sys

DB = "warehouse/research.duckdb"
TODAY = datetime.date(2026, 8, 30)
c = duckdb.connect(DB, read_only=True)

# 탭 구분이다. WICS 산업명에 쉼표가 들어간다('섬유,의류,신발,호화품').
UNIVERSE = os.environ.get("UNIVERSE", "/tmp/universe.tsv")
rows = [l.rstrip("\n").split("\t") for l in open(UNIVERSE, encoding="utf-8") if l.strip()]

def q(sql, p=()):
    return c.execute(sql, list(p)).fetchall()

OPI = {"매수": "매수", "Buy": "매수", "BUY": "매수", "buy": "매수", "적극매수": "매수",
       "Strong Buy": "매수", "중립": "중립", "Hold": "중립", "HOLD": "중립", "보유": "중립",
       "Neutral": "중립", "Marketperform": "중립", "매도": "매도", "Sell": "매도",
       "축소": "매도", "비중축소": "매도", "없음": None, "N/R": None, "NR": None}
BADAN = {"십억원", "억원", "백만원", "원", "십억", "%", "배", "-"}


def norm_opi(x):
    if not x:
        return None
    return OPI.get(x.strip(), OPI.get(x.strip().title(), x.strip()))


def clean_analyst(a):
    if not a:
        return None
    a = a.strip()
    return None if (a in BADAN or len(a) > 12 or any(ch.isdigit() for ch in a)) else a


def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None

# ── qw 컨센 축(월/일 스냅샷, 최신 = 2026-07-30) ──────────────────────────────
QW = {"영업이익": "E121500.M", "매출액": "E121000.M", "EPS": "E312000.M",
      "PER": "E382100.M", "PBR": "E382500.M", "ROE": "E211500.M"}
QW_CUR = {"목표주가": "E610300.M", "목표주가최고": "E610301.M", "목표주가최저": "E610302.M",
          "목표주가참여": "E610560.M", "투자의견": "E610100.M",
          "EPS_Fwd12M": "E312060.M", "PER_Fwd12M": "E382160.M",
          "EPS조정1M": "E311310.M", "EPS조정3M": "E391310.M",
          "수정주가": "S100300", "시가총액": "S102100"}
QW_LAST = q("select max(as_of) from qw_fundamentals")[0][0]

def qw_series(tk, item, period):
    return dict(q("""select as_of, value from qw_fundamentals
                     where ticker=? and item_code=? and period=? order by as_of""", (tk, item, period)))

def qw_at(ser, on_or_before):
    ks = [d for d in ser if d <= on_or_before]
    return ser[max(ks)] if ks else None

# ── 리포트 추정치(우리 파이프라인, 최신 = 2026-08-28) ────────────────────────
# 증권사마다 표의 단위가 다르다(억원/십억원/백만원). 같은 항목을 그대로 중앙값 내면
# 단위가 섞여 숫자가 무의미해진다(예: 비츠로셀 매출 IBK 3,175억 vs 삼성 311십억).
# QuantiWise 컨센서스(억원)를 자릿수 기준선으로 삼아 10의 거듭제곱만 맞춘다.
# 값 자체는 바꾸지 않는다 — 기준선에서 √10 배를 넘게 벗어나면 버리고 버린 수를 남긴다.
import math

def unit_k(v, anchor):
    """v 를 anchor 와 같은 자릿수로 옮기는 10의 지수. 못 맞추면 None."""
    if not v or not anchor:
        return None
    k = round(math.log10(abs(anchor)) - math.log10(abs(v)))
    if abs(k) > 4:
        return None
    return k


def est_by_report(tk, fy, d0, d1, anchor_rev, anchor_op, anchor_eps):
    """구간 [d0,d1] 리포트별 FY 추정치 — 리포트 1건 = 단위 1개.

    증권사마다 표 단위가 다르다(억/십억/백만원). 값마다 따로 맞추면 같은 리포트의
    매출과 영업이익이 다른 단위로 갈린다. 그래서 **리포트 단위로** 배수를 정한다:
    매출액을 QuantiWise 컨센(억원) 자릿수에 맞춰 10^k 를 구하고, 같은 리포트의
    영업이익에 그 k 를 그대로 쓴다. 매출이 없으면 영업이익으로 k 를 구한다.
    자릿수를 못 맞추거나 정규화 뒤에도 기준선의 1/3~3배를 벗어나면 그 리포트는 버린다.
    """
    rows = q("""select source_id, metric, value from report_estimates
                where ticker=? and fy=? and kind='E' and metric in ('revenue','op_income','eps')
                  and published_at>=? and published_at<=?""", (tk, fy, d0, d1))
    rep = {}
    for sid, m, v in rows:
        rep.setdefault(sid, {}).setdefault(m, []).append(v)
    rev, op, eps, dropped = [], [], [], 0
    for sid, m in rep.items():
        r = med(m.get("revenue", []))
        o = med(m.get("op_income", []))
        e = med(m.get("eps", []))
        k = unit_k(r, anchor_rev)
        if k is None:
            k = unit_k(o, anchor_op)
        if k is None:
            if e is not None and anchor_eps and 0.05 <= abs(e / anchor_eps) <= 20:
                eps.append(e)
            else:
                dropped += 1
            continue
        r2 = r * 10 ** k if r is not None else None
        o2 = o * 10 ** k if o is not None else None
        if r2 is not None and anchor_rev and not (1 / 3 <= abs(r2 / anchor_rev) <= 3):
            dropped += 1
            continue
        if r2 is not None:
            rev.append(r2)
        if o2 is not None:
            op.append(o2)
        if e is not None and (not anchor_eps or 0.05 <= abs(e / anchor_eps) <= 20):
            eps.append(e)
    return {"revenue": (med(rev), len(rev)), "op_income": (med(op), len(op)),
            "eps": (med(eps), len(eps)), "dropped": dropped}


# ── 리포트 본문에서 근거 문장 뽑기 (파이썬 규칙만. 모델 안 쓴다) ──────────────
KEY = ("수주", "잔고", "가이던스", "증설", "capa", "CAPA", "계약", "인도", "납품", "점유율",
       "마진", "수요", "가동", "국산화", "수출", "발주", "매출", "영업이익", "출하", "판가")
NOISE = re.compile(r"(투자의견|목표주가를? 유지|커버리지|본 자료|Compliance|애널리스트|당사는)")
NUM = re.compile(r"\d")

def sentences(body):
    body = re.sub(r"\[\d+\]_\d+\.pdf\s*$", "", body or "")
    body = re.sub(r"\s+", " ", body)
    out = []
    for s in re.split(r"(?<=[다요\.])\s+", body):
        s = s.strip()
        if 25 <= len(s) <= 190 and not NOISE.search(s):
            out.append(s)
    return out

def pick_evidence(tk, n=2):
    reps = q("""select firm, analyst, published_at, title, body from reports
                where ticker=? and body is not null and published_at>=?
                order by published_at desc limit 12""", (tk, TODAY - datetime.timedelta(days=200)))
    scored = []
    for firm, analyst, d, title, body in reps:
        for s in sentences(body):
            sc = sum(1 for k in KEY if k in s) + (1 if NUM.search(s) else 0)
            if sc >= 2:
                scored.append((sc, d, firm, analyst, title, s))
    scored.sort(key=lambda x: (-x[0], -x[1].toordinal()))
    seen, out = set(), []
    for sc, d, firm, analyst, title, s in scored:
        k = s[:28]
        if k in seen:
            continue
        seen.add(k)
        out.append({"score": sc, "date": str(d), "firm": firm, "analyst": analyst,
                    "title": title, "text": s})
        if len(out) >= n:
            break
    return out

# 리포트 본문에 실제로 몇 번 나오는지 세는 축. 사람이 붙인 테마가 아니라 본문의 말이다.
TOPICS = ["수주잔고", "신규수주", "수주", "가이던스", "증설", "원전", "SMR", "가스터빈",
          "변압기", "해저케이블", "전선", "데이터센터", "전력망", "송배전", "방산", "수출",
          "폴란드", "중동", "관세", "로봇", "휴머노이드", "감속기", "액추에이터", "협동로봇",
          "양극재", "분리막", "전기차", "ESS", "굴착기", "건설기계", "엘리베이터", "물류자동화",
          "위성", "발사체", "항공", "애프터마켓", "유지보수", "가동률", "판가", "환율", "점유율"]


def topics_of(tk, n=4):
    bodies = [b for (b,) in q("""select body from reports where ticker=? and body is not null
                                 and published_at>=? limit 40""",
                              (tk, TODAY - datetime.timedelta(days=200)))]
    txt = " ".join(bodies)
    hits = [(t, txt.count(t)) for t in TOPICS]
    hits = [h for h in hits if h[1] > 0]
    # '수주잔고'가 잡힌 몫은 '수주'에서 뺀다 — 같은 글자를 두 번 세지 않는다
    d = dict(hits)
    if "수주" in d:
        d["수주"] -= d.get("수주잔고", 0) + d.get("신규수주", 0)
        if d["수주"] <= 0:
            d.pop("수주")
    return sorted(d.items(), key=lambda x: -x[1])[:n]


D90 = TODAY - datetime.timedelta(days=90)
D180 = TODAY - datetime.timedelta(days=180)
D270 = TODAY - datetime.timedelta(days=270)

result = []
for code, name, wics, mk in rows:
    o = {"code": code, "name": name, "wics": wics, "market": mk, "k200": mk == "K200"}

    # 1) 목표주가·의견 — 우리 리포트 원장 (최근 90일)
    tp = q("""select firm, target_price, opinion, published_at, title, analyst from reports
              where ticker=? and published_at>=? order by published_at desc""", (code, D90))
    tps = [t[1] for t in tp if t[1]]
    o["reports_90d"] = len(tp)
    o["tp_med_90d"] = med(tps)
    o["tp_n_firms_90d"] = len({t[0] for t in tp if t[1]})
    o["opinions_90d"] = {}
    for t in tp:
        v = norm_opi(t[2])
        if v:
            o["opinions_90d"][v] = o["opinions_90d"].get(v, 0) + 1
    o["recent_reports"] = [{"date": str(t[3]), "firm": t[0], "analyst": clean_analyst(t[5]),
                            "title": t[4], "tp": t[1], "opinion": norm_opi(t[2])} for t in tp[:5]]
    tp_prev = [t[1] for t in q("""select firm,target_price from reports
                                  where ticker=? and published_at>=? and published_at<? and target_price is not null""",
                               (code, D270, D180))]
    lr = q("select max(published_at), count(*) from reports where ticker=?", (code,))[0]
    o["last_report"] = str(lr[0]) if lr[0] else None
    o["reports_all"] = lr[1]
    o["est_q_only"] = q("""select count(*) from report_estimates where ticker=? and kind='Q'
                           and published_at>=?""", (code, D90))[0][0]
    o["tp_med_prev"] = med(tp_prev)
    o["tp_n_prev"] = len(tp_prev)

    # 2) 리포트 추정치 추이 — FY26 / FY27, 최근 90일 vs 그 이전 90일
    #    단위 기준선은 QuantiWise 컨센(억원 / EPS 는 원).
    def anch(item, fy):
        ser = qw_series(code, QW[item], f"{fy}AS")
        return ser[max(ser)] if ser else None

    o["est"] = {}
    for fy in (2026, 2027):
        ar, ao, ae = anch("매출액", fy), anch("영업이익", fy), anch("EPS", fy)
        cur = est_by_report(code, fy, D90, TODAY, ar, ao, ae)
        pre = est_by_report(code, fy, D270, D180, ar, ao, ae)
        for metric in ("revenue", "op_income", "eps"):
            c1, n1 = cur[metric]
            p1, n2 = pre[metric]
            o["est"][f"{metric}_{fy}"] = {
                "cur": c1, "n_cur": n1, "prev": p1, "n_prev": n2,
                "unit": "원" if metric == "eps" else "억원",
                "anchor": {"revenue": ar, "op_income": ao, "eps": ae}[metric],
                "chg_pct": (None if not (c1 and p1) else round((c1 - p1) / abs(p1) * 100, 1))}
        o["est"][f"dropped_{fy}"] = cur["dropped"]

    # 3) QuantiWise 컨센 추이 (as_of ≤ 2026-07-30)
    qw = {"as_of": str(QW_LAST)}
    for label, item in QW.items():
        for period in ("2026AS", "2027AS"):
            ser = qw_series(code, item, period)
            if not ser:
                continue
            last = max(ser)
            qw[f"{label}_{period}"] = ser[last]
            qw[f"{label}_{period}_asof"] = str(last)
            for tag, days in (("1M", 30), ("3M", 91), ("6M", 182)):
                base = qw_at(ser, last - datetime.timedelta(days=days))
                if base and ser[last] is not None and base != 0:
                    qw[f"{label}_{period}_chg{tag}"] = round((ser[last] - base) / abs(base) * 100, 1)
    for label, item in QW_CUR.items():
        ser = qw_series(code, item, "CUR")
        if not ser:
            continue
        last = max(ser)
        qw[label] = ser[last]
        qw[label + "_asof"] = str(last)          # 항목마다 마지막 관측일이 다르다
        for tag, days in (("1M", 30), ("3M", 91)):
            base = qw_at(ser, last - datetime.timedelta(days=days))
            if base and ser[last] is not None and base != 0:
                qw[f"{label}_chg{tag}"] = round((ser[last] - base) / abs(base) * 100, 1)
    o["qw"] = qw
    o["qw_rows"] = q("select count(*) from qw_fundamentals where ticker=?", (code,))[0][0]

    # 4) 리포트 본문 근거
    o["evidence"] = pick_evidence(code)
    o["topics"] = topics_of(code)
    result.append(o)
    print(f"  {code} {name} 리포트90d={o['reports_90d']:3} qw_rows={o['qw_rows']:6} 근거={len(o['evidence'])}", file=sys.stderr)

out = {"as_of_reports": str(q("select max(published_at) from reports")[0][0]),
       "as_of_qw": str(QW_LAST), "generated_for": str(TODAY), "rows": result}
open(os.environ.get("OUT", "/tmp/consensus.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print("wrote", os.environ.get("OUT", "/tmp/consensus.json"), len(result))
