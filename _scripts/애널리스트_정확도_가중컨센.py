# -*- coding: utf-8 -*-
"""애널리스트 실적 추정 정확도 → 상위 N명 가중 컨센서스 (조선·화장품·인터넷/게임).

맥미니에서 돈다(원장 읽기 전용 사본만 연다). 결과 JSON 을 맥북으로 가져와 문서를 만든다.

    python3 애널리스트_정확도_가중컨센.py --universe 애널리스트정확도_유니버스.json --out result.json
        [--top 3] [--w-top 2.0] [--w-rest 1.0] [--asof 2026-10-21]

■ 무엇을 채점하나
  분기 영업이익 추정(report_estimates: metric=op_income, kind=Q, 기간 접미사 E/F). 'P'(잠정)·접미사 없음은 실적이라 뺀다.
  정답은 DART 분기 실적(dart_fin_quarterly, 연결 우선, 4Q 는 연간−3분기 역산).
■ 어떤 추정을 쓰나
  분기말 92일 전 ~ 분기말 30일 후(프리뷰 시즌, 대부분 잠정실적 전)에 나온 것 중 애널리스트별 마지막 1건.
■ 단위
  리포트마다 억/십억/조 단위가 섞이고 라벨이 틀린 행도 있다. 같은 리포트(source_id)에 적힌 과거 분기 실적 행을
  DART 와 맞춰 10의 거듭제곱 보정값을 리포트별로 정한다. 실적 행이 없으면 unit 라벨을 믿는다.
  보정 뒤에도 정답과 10^1.5 배 넘게 어긋나면 파싱 오류로 버린다.
■ 오차와 점수
  APE = |추정−실적| / max(|실적|, 2%×그 분기 매출), 1.0 에서 자른다(적자 근처 폭발 방지).
  상대점수 = 내 APE − 같은 종목·분기 다른 애널리스트들의 APE 중앙값(그 분기 추정자 3명 이상일 때만).
  애널리스트 점수 = 상대점수 평균(작을수록 정확). 최소 6건·3개 분기 이상 채점된 사람만 순위에 넣는다.
■ 신원
  애널리스트 이름(한글 2–4자)으로 묶는다. 이직해도 같은 사람으로 본다. 표기가 깨진 값(숫자·단위·긴 문자열)은 버린다.
■ 가중
  업종별 상위 N명 가중치 w_top, 나머지(순위권 밖·미채점·증권사 미상) w_rest.
  워크포워드 백테스트: 목표 분기 이전 이벤트만으로 순위를 매겨 그 분기 가중 평균의 오차를 단순 평균·중앙값과 비교한다.
"""
import argparse
import datetime as dt
import json
import math
import re
import statistics as st
from collections import defaultdict

import duckdb

DB = "/Users/benopenclaw/research-site/stable/warehouse/research.ro.duckdb"
UNIT = {"억원": 1.0, "십억원": 10.0, "조원": 10000.0, "백만원": 0.01, "천원": 1e-5}
BAD = {"십억원", "억원", "백만원", "원", "십억", "투자의견", "목표주가", "없음", "조업일수"}
QEND = {"1": "03-31", "2": "06-30", "3": "09-30", "4": "12-31"}

ap = argparse.ArgumentParser()
ap.add_argument("--universe", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--top", type=int, default=3)
ap.add_argument("--w-top", type=float, default=2.0)
ap.add_argument("--w-rest", type=float, default=1.0)
ap.add_argument("--asof", default="2026-10-21")
ap.add_argument("--target", default="3Q26")
ap.add_argument("--cur-days", type=int, default=70, help="현재 컨센에 쓸 최근 일수 — 직전 분기 실적 발표 이후만(2Q 발표 ≈ 8월 중순)")
ap.add_argument("--min-events", type=int, default=6)
ap.add_argument("--min-quarters", type=int, default=3)
ap.add_argument("--shrink", type=float, default=10.0, help="순위용 수축 강도: rel × n/(n+k)")
A = ap.parse_args()
SHRINK = A.shrink
ASOF = dt.date.fromisoformat(A.asof)
U = json.load(open(A.universe, encoding="utf-8"))["sectors"]
c = duckdb.connect(DB, read_only=True)
# 이름 칸 오염(본문 문구 '추정한다'·'전망이다' 등)을 막는다: 구조화된 출처(네이버 리서치 목록·증권사 사이트)나
# 이메일이 붙은 리포트에서 한 번이라도 나온 이름만 사람으로 인정한다.
NAMES = {r[0].strip() for r in c.execute(
    """select distinct analyst from reports where analyst is not null and
       (source='naver:research' or source like 'broker:%' or analyst_email is not null)""").fetchall()}


def clean_name(a):
    if not a:
        return None
    a = a.strip()
    # 한글 3자 + 조사·어미로 끝나지 않을 것. 2자·4자 실명 일부를 잃는 대신 '동사는'·'전망이'·'시작해'·'전분기'·'오픈채팅'을 막는다.
    if a in BAD or not re.fullmatch(r"[가-힣]{3}", a) or a not in NAMES or a[-1] in "다함음됨임요는은이가을를에의해며고서도기될할된던":
        return None
    return a


_TITLE = {}


def title_freq(name):
    """리포트 제목에 그 낱말이 나오는 횟수. 사람 이름은 제목에 거의 안 나온다(기대 5,753 · 예상 2,198 vs 사람 0)."""
    if name not in _TITLE:
        _TITLE[name] = c.execute("select count(*) from reports where title like ?", [f"%{name}%"]).fetchone()[0]
    return _TITLE[name]


def identity_map(pairs):
    """[(analyst, email)] → ident(analyst, email) 함수. 이메일이 신원이다(메모리 analyst-name-repair).
    이메일별 정본 이름 = 그 이메일 행에서 가장 많이 나온 '사람 같은' 이름. 이메일 없는 행은 그 이름이 가리키는
    이메일이 하나뿐일 때만 그 사람으로 잇는다. 반환값은 표시용 정본 이름(동명이인은 '이름(이메일앞)' 으로 구분)."""
    from collections import Counter
    ok = lambda a: (clean_name(a) is not None) and title_freq(a.strip()) < 50
    by_email, name_emails = defaultdict(Counter), defaultdict(set)
    for a, em in pairs:
        if em and a and ok(a):
            by_email[em.lower()][a.strip()] += 1
    # 정본 이름: 세 글자 이름을 우선(한국 이름 대부분), 그 안에서 최빈. '석오'(94) 대신 '강석오'(87).
    canon = {em: max(cnt.items(), key=lambda kv: (len(kv[0]) == 3, kv[1]))[0] for em, cnt in by_email.items()}
    for em, nm in canon.items():
        name_emails[nm].add(em)
    dup = {nm for nm, ems in name_emails.items() if len(ems) > 1}

    def label(em):
        nm = canon[em]
        return f"{nm}({em.split('@')[0]})" if nm in dup else nm

    def ident(a, em):
        if em and em.lower() in canon:
            return label(em.lower())
        if a and ok(a):
            ems = name_emails.get(a.strip(), set())
            if len(ems) == 1:
                return label(next(iter(ems)))
            # 이메일과 한 번도 이어진 적 없는 이름은 사람으로 보지 않는다('경우'·'오픈채팅'·'전망치에').
        return None
    return ident


def wmedian(pairs):
    """가중 중앙값: 누적 가중치가 절반을 넘는 첫 값(동률이면 두 값 평균)."""
    pairs = sorted(pairs)
    tot = sum(w for _, w in pairs)
    acc = 0.0
    for i, (v, w) in enumerate(pairs):
        acc += w
        if acc > tot / 2:
            return v
        if acc == tot / 2:
            return (v + pairs[i + 1][0]) / 2
    return pairs[-1][0]


def qkey(period):
    """'3Q25E' → ('3Q25', 'E'). 분기 아니면 None."""
    m = re.fullmatch(r"([1-4])Q(\d{2})([A-Z]?)", period or "")
    return (f"{m.group(1)}Q{m.group(2)}", m.group(3)) if m else None


def qend(q):
    return dt.date.fromisoformat(f"20{q[2:]}-{QEND[q[0]]}")


def short(f):
    return (f or "").replace("투자증권", "").replace("증권", "") or None


result = {"params": vars(A), "generated": dt.datetime.now().isoformat(timespec="seconds"), "sectors": {}}

for sec, uni in U.items():
    T = sorted(uni)
    ph = ",".join("?" * len(T))
    # ── 정답: DART 분기 영업이익·매출(억원)
    act, rev = {}, {}
    for t, pe, acc, v, fs in c.execute(
            f"""select ticker, period_end, account, value, fs_div from dart_fin_quarterly
                where ticker in ({ph}) and account in ('op_income','revenue') and period_end>='2021-01-01'
                order by fs_div desc""", T).fetchall():
        q = f"{(pe.month - 1) // 3 + 1}Q{str(pe.year)[2:]}"
        d = act if acc == "op_income" else rev
        if (t, q) not in d or fs == "CFS":
            d[(t, q)] = v / 1e8
    # ── 추정치 + 리포트 메타
    rows = c.execute(
        f"""select e.source_id, e.ticker, e.period, e.value, e.unit, r.published_at, r.firm, r.analyst, r.target_price, r.source, r.analyst_email
            from report_estimates e join reports r on r.source_id = e.source_id
            where e.ticker in ({ph}) and e.metric='op_income' and e.kind='Q' and e.dup_of is null
              and r.published_at >= '2021-07-01' and e.value is not null""", T).fetchall()
    # 리포트별 단위 보정: 같은 리포트의 실적 행(접미사 없음/A) vs DART
    scale_votes = defaultdict(list)
    for sid, t, per, v, unit, *_rest in rows:
        k = qkey(per)
        if not k or k[1] not in ("", "A") or (t, k[0]) not in act or not v:
            continue
        a = act[(t, k[0])]
        if a and abs(a) > 1:
            scale_votes[sid].append(round(math.log10(abs(a) / abs(v))))
    scale = {sid: 10 ** st.mode(vs) for sid, vs in scale_votes.items() if vs}
    # 추정 행 정리
    est = []   # (ticker, q, published, analyst, firm, value억, sid)
    dropped = 0
    ident = identity_map([(r[7], r[10]) for r in rows])
    for sid, t, per, v, unit, pub, firm, an, tp, src, em in rows:
        k = qkey(per)
        if not k or k[1] not in ("E", "F"):
            continue
        f = scale.get(sid) or UNIT.get(unit or "", None)
        if f is None:
            dropped += 1
            continue
        val = v * f
        a = act.get((t, k[0]))
        if a is not None and abs(a) > 1 and val and abs(math.log10(abs(val) / abs(a))) > 1.5:
            dropped += 1
            continue
        est.append((t, k[0], pub, ident(an, em), short(firm), val, sid))
    # ── 채점 이벤트: (ticker, q) 별 애널리스트 마지막 프리뷰 추정
    events = defaultdict(dict)   # (t,q) -> {analyst: (ape, firm, pub, val)}
    for t, q, pub, an, firm, val, sid in est:
        if not an or (t, q) not in act:
            continue
        e = qend(q)
        if not (e - dt.timedelta(days=92) <= pub <= e + dt.timedelta(days=30)):
            continue
        prev = events[(t, q)].get(an)
        if prev and prev[2] >= pub:
            continue
        a = act[(t, q)]
        denom = max(abs(a), 0.02 * abs(rev.get((t, q), 0) or 0), 1.0)
        ape = min(abs(val - a) / denom, 1.0)
        events[(t, q)][an] = (ape, firm, pub, val)

    def score_from(evs):
        per = defaultdict(list)
        for (t, q), d in evs.items():
            if len(d) < 3:
                continue
            m = st.median(x[0] for x in d.values())
            for an, (ape, firm, pub, val) in d.items():
                per[an].append((ape - m, ape, q, firm, pub, t))
        out = {}
        for an, L in per.items():
            qs = {x[2] for x in L}
            if len(L) < A.min_events or len(qs) < A.min_quarters:
                continue
            last = max(L, key=lambda x: x[4])
            rel = sum(x[0] for x in L) / len(L)
            out[an] = dict(rel=rel, rel_shrunk=rel * len(L) / (len(L) + SHRINK), ape_med=st.median(x[1] for x in L), n=len(L),
                           quarters=len(qs), beat=sum(1 for x in L if x[0] < 0) / len(L), firm=last[3],
                           tickers=sorted({x[5] for x in L}))
        return out

    scores = score_from(events)
    # 지속성: 2025-06-30 이전 분기로 매긴 점수 vs 이후 분기 점수의 순위상관(둘 다 채점된 사람만)
    cut = dt.date(2025, 6, 30)
    s1 = score_from({k: v for k, v in events.items() if qend(k[1]) <= cut})
    s2 = score_from({k: v for k, v in events.items() if qend(k[1]) > cut})
    both = sorted(set(s1) & set(s2))
    persist = None
    if len(both) >= 5:
        def ranks(xs):
            o = sorted(range(len(xs)), key=lambda i: xs[i])
            r = [0] * len(xs)
            for k_, i in enumerate(o):
                r[i] = k_
            return r
        r1 = ranks([s1[a]["rel"] for a in both]); r2 = ranks([s2[a]["rel"] for a in both])
        n_ = len(both)
        rho = 1 - 6 * sum((x - y) ** 2 for x, y in zip(r1, r2)) / (n_ * (n_ ** 2 - 1))
        top1 = set(sorted(both, key=lambda a: s1[a]["rel"])[:3]); top2 = set(sorted(both, key=lambda a: s2[a]["rel"])[:3])
        persist = dict(n=n_, spearman=rho, top3_overlap=len(top1 & top2), top3_first=sorted(top1), top3_second=sorted(top2))
    ranked = sorted(scores.items(), key=lambda kv: kv[1]["rel_shrunk"])
    top = [an for an, _ in ranked[:A.top]]

    def weight(an, topset):
        return A.w_top if an in topset else A.w_rest

    # ── 워크포워드 백테스트
    quarters = sorted({q for (_, q) in events}, key=lambda q: qend(q))
    bt = []
    for tq in quarters:
        if qend(tq) < dt.date(2023, 12, 31) or qend(tq) > ASOF:
            continue
        hist = {k: v for k, v in events.items() if qend(k[1]) < qend(tq) - dt.timedelta(days=60)}
        sc = score_from(hist)
        tops = set(sorted(sc, key=lambda a: sc[a]["rel_shrunk"])[:A.top])
        for (t, q), d in events.items():
            if q != tq or len(d) < 3 or not (tops & set(d)):
                continue
            a = act[(t, q)]
            denom = max(abs(a), 0.02 * abs(rev.get((t, q), 0) or 0), 1.0)
            vals = [(an, x[3]) for an, x in d.items()]
            eq = sum(v for _, v in vals) / len(vals)
            md = st.median(v for _, v in vals)
            ws = sum(weight(an, tops) for an, _ in vals)
            wm = sum(weight(an, tops) * v for an, v in vals) / ws
            topm = st.mean(v for an, v in vals if an in tops)
            w3 = [(3.0 if an in tops else 1.0) for an, _ in vals]
            wm3 = sum(w * v for w, (_, v) in zip(w3, vals)) / sum(w3)
            # 연속 가중: 상대점수가 좋을수록 무겁게, 채점 건수가 적으면 0 쪽으로 당긴다(수축 k=8)
            def cw(an):
                s_ = sc.get(an)
                if not s_:
                    return 1.0
                shrunk = s_["rel_shrunk"]
                return math.exp(-shrunk / 0.05)
            wc = [cw(an) for an, _ in vals]
            wmc = sum(w * v for w, (_, v) in zip(wc, vals)) / sum(wc)
            wmed = wmedian([(v, weight(an, tops)) for an, v in vals])
            bt.append(dict(t=t, q=q, n=len(vals), n_top=len(tops & set(d)), ape_wmed=min(abs(wmed - a) / denom, 1),
                           ape_eq=min(abs(eq - a) / denom, 1), ape_med=min(abs(md - a) / denom, 1),
                           ape_w=min(abs(wm - a) / denom, 1), ape_w3=min(abs(wm3 - a) / denom, 1),
                           ape_cont=min(abs(wmc - a) / denom, 1), ape_top=min(abs(topm - a) / denom, 1)))
    summ = {}
    if bt:
        for k in ("ape_eq", "ape_med", "ape_wmed", "ape_w", "ape_w3", "ape_cont", "ape_top"):
            summ[k] = dict(mean=st.mean(x[k] for x in bt), median=st.median(x[k] for x in bt))
        summ["n_groups"] = len(bt)
        summ["w_beats_eq"] = sum(1 for x in bt if x["ape_w"] < x["ape_eq"]) / len(bt)
        summ["w_ties_eq"] = sum(1 for x in bt if x["ape_w"] == x["ape_eq"]) / len(bt)
        summ["cont_beats_eq"] = sum(1 for x in bt if x["ape_cont"] < x["ape_eq"]) / len(bt)
        summ["wmed_beats_med"] = sum(1 for x in bt if x["ape_wmed"] < x["ape_med"]) / len(bt)
        summ["wmed_loses_med"] = sum(1 for x in bt if x["ape_wmed"] > x["ape_med"]) / len(bt)
        summ["by_quarter"] = {q: dict(n=len(L), eq=st.mean(x["ape_eq"] for x in L), w=st.mean(x["ape_w"] for x in L))
                              for q in quarters for L in [[x for x in bt if x["q"] == q]] if L}

    # ── 현재(목표 분기) 가중 컨센: 최근 110일 안 애널리스트별 최신 추정
    tq = A.target
    cur = defaultdict(dict)
    for t, q, pub, an, firm, val, sid in est:
        if q != tq or pub > ASOF or pub < ASOF - dt.timedelta(days=A.cur_days):
            continue
        key = an or f"미상:{firm}:{sid}"
        if key in cur[t] and cur[t][key]["pub"] >= pub.isoformat():
            continue
        cur[t][key] = dict(val=val, firm=firm, pub=pub.isoformat(), rated=an in scores, top=an in top)
    # 목표가: 최근 90일 애널리스트별 최신
    tps = defaultdict(dict)
    for t, pub, firm, an, tp, em in c.execute(
            f"""select ticker, published_at, firm, analyst, target_price, analyst_email from reports
                where ticker in ({ph}) and target_price>0 and published_at between ? and ?""",
            T + [ASOF - dt.timedelta(days=90), ASOF]).fetchall():
        an = ident(an, em)
        if not an:
            continue
        if an not in tps[t] or tps[t][an][1] < pub:
            tps[t][an] = (tp, pub, short(firm))
    cons = {}
    for t, (sd, v) in {r[0]: (r[1], r[2]) for r in c.execute(
            f"""select ticker, max(snap_date), arg_max(value, snap_date) from naver_consensus_snap
                where ticker in ({ph}) and item='op_income' and period=? and snap_date<=? group by 1""",
            T + [f"20{tq[2:]}Q{tq[0]}E", ASOF]).fetchall()}.items():
        cons[t] = v
    stocks = {}
    for t in T:
        d = cur.get(t, {})
        tpd = tps.get(t, {})
        if not d and not tpd:
            continue
        rec = dict(name=uni[t], naver_cons=cons.get(t), estimates=[dict(analyst=k if not k.startswith("미상") else None, **v) for k, v in d.items()])
        if d:
            vals = list(d.items())
            rec["eq_mean"] = sum(v["val"] for _, v in vals) / len(vals)
            rec["median"] = st.median(v["val"] for _, v in vals)
            ws = sum(weight(k, set(top)) for k, _ in vals)
            rec["w_mean"] = sum(weight(k, set(top)) * v["val"] for k, v in vals) / ws
            rec["n"] = len(vals)
            rec["n_top"] = sum(1 for k, _ in vals if k in top)
        if tpd:
            items = list(tpd.items())
            rec["tp_eq"] = sum(v[0] for _, v in items) / len(items)
            ws = sum(weight(k, set(top)) for k, _ in items)
            rec["tp_w"] = sum(weight(k, set(top)) * v[0] for k, v in items) / ws
            rec["tp_n"] = len(items)
            rec["tp_top"] = [dict(analyst=k, tp=v[0], date=v[1].isoformat(), firm=v[2]) for k, v in items if k in top]
        stocks[t] = rec

    result["sectors"][sec] = dict(
        universe=len(T), est_rows=len(est), dropped_unit=dropped, events=len(events),
        scored_events=sum(1 for d in events.values() if len(d) >= 3), rated=len(scores),
        ranking=[dict(analyst=an, **s) for an, s in ranked], top=top, backtest=summ, persistence=persist, stocks=stocks)
    print(f"[{sec}] 유니버스 {len(T)} · 추정행 {len(est)} (단위 탈락 {dropped}) · 이벤트 {len(events)} · 순위권 {len(scores)}명 · 상위 {top}")
    if persist:
        print(f"   지속성: 전·후반 모두 채점 {persist['n']}명 · 순위상관 {persist['spearman']:+.2f} · 상위3 겹침 {persist['top3_overlap']}/3")
    if summ:
        print(f"   백테스트 {summ['n_groups']}건: 단순평균 APE {summ['ape_eq']['mean']:.3f} · 중앙값 {summ['ape_med']['mean']:.3f} · "
              f"가중중앙값 {summ['ape_wmed']['mean']:.3f}(중앙값 대비 승 {summ['wmed_beats_med']:.0%}·패 {summ['wmed_loses_med']:.0%}) · 상위3×2 {summ['ape_w']['mean']:.3f} · ×3 {summ['ape_w3']['mean']:.3f} · 연속 {summ['ape_cont']['mean']:.3f} · 상위만 {summ['ape_top']['mean']:.3f} · ×2 승률 {summ['w_beats_eq']:.0%} · 연속 승률 {summ['cont_beats_eq']:.0%}")

json.dump(result, open(A.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("wrote", A.out)
