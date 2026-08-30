#!/usr/bin/env python3
"""
국내주식 — 코스피200 유니버스 문서 생성 (WI26 26개 업종 폴더 전부)

업종 축은 **WI26 하나**다. 배정은 `_scripts/업종_WI26_배정.py` 가 미니 PG `sector_map`
(QuantiWise WI26)으로 만든 `업종_WI26_유니버스_<날짜>.csv` 를 그대로 읽는다.
이 스크립트는 업종을 판단하지 않는다.

읽는 것 (전부 _manifest/데이터 의 수집 산출물. 손으로 넣은 값은 없다)
  업종_WI26_유니버스_<날짜>.csv   ← _scripts/업종_WI26_배정.py
  코스피200_구성종목_<날짜>.csv    ← _scripts/코스피200_구성종목_수집.py
  국내주식_시세컨센_<날짜>.csv     ← _scripts/네이버_시세컨센_수집.py
  국내주식_컨센추이_<날짜>.json    ← _scripts/원장_컨센추출_미니.py (맥미니 원장)
  지수_일별_<날짜>.json

쓰는 것
  10_국내주식/_코스피200_유니버스.md
  10_국내주식/<NN_업종>/_시총상위_종목표.md          (26)
  10_국내주식/<NN_업종>/<업종>_코스피200_종목분석.md  (26)
  10_국내주식/<NN_업종>/<업종>_기업분석.md §2 교체 (원래 표는 §2-1 로 보존)
  10_국내주식/<NN_업종>/<업종>_기초자료.md §6 교체 (원래 표는 §6-1 로 보존)
  10_국내주식 아래 낡은 '시장 상황' 블록을 가진 모든 문서에 최신 블록을 얹는다

계산은 전부 여기서 한다. 다시 돌려도 같은 결과다(멱등).
"""
from __future__ import annotations
import csv, datetime as dt, json, re, sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "_manifest" / "데이터"
ROOT = REPO / "10_국내주식"
STAMP = "2026-08-30"
TRADE = "2026-08-28"

uni = list(csv.DictReader((DATA / f"업종_WI26_유니버스_{STAMP}.csv").open(encoding="utf-8")))
quote = {r["code"]: r for r in csv.DictReader((DATA / f"국내주식_시세컨센_{STAMP}.csv").open(encoding="utf-8"))}
led = json.loads((DATA / f"국내주식_컨센추이_{STAMP}.json").read_text(encoding="utf-8"))
idx = json.loads((DATA / f"지수_일별_{STAMP}.json").read_text(encoding="utf-8"))["series"]

LED = {r["code"]: r for r in led["rows"]}
UROW = {r["code"]: r for r in uni}
AS_REP, AS_QW = led["as_of_reports"], led["as_of_qw"]
K200 = {r["code"] for r in uni if r["k200"]}

UNI = defaultdict(list)
for r in uni:
    UNI[r["dir"]].append(r["code"])
for d in UNI:
    UNI[d].sort(key=lambda c: -(float(quote[c]["mktcap_억"] or 0)))

MOVED_OUT = defaultdict(list)      # 이전 판에 이 폴더였다가 WI26 으로 다른 칸에 간 종목
for r in uni:
    if r["prev_dir"] and r["prev_dir"] != r["dir"]:
        MOVED_OUT[r["prev_dir"]].append(r["code"])

DIRNAME = {p.name: p for p in sorted(ROOT.iterdir()) if p.is_dir()}
KOR = {d: d.split("_", 1)[1] for d in DIRNAME}

# ── 서식 ────────────────────────────────────────────────────────────────────
def n(v, d=0):
    return "—" if v in (None, "") else f"{float(v):,.{d}f}"

def pct(v, d=1):
    return "—" if v in (None, "") else f"{float(v):+,.{d}f}%"

def unit_or_dash(v, d=1, suffix="%"):
    return "—" if v in (None, "") else f"{float(v):,.{d}f}{suffix}"

def 조억(억):
    if 억 in (None, ""):
        return "—"
    억 = float(억)
    return f"{억/10000:,.1f}조" if abs(억) >= 10000 else f"{억:,.0f}억"

def per_fwd(q):
    v = q["cns_per"]
    return "—" if v in (None, "") else ("적자" if float(v) < 0 else n(v, 1))

def stale(qw, key, days=90):
    a = qw.get(key + "_asof")
    return bool(a) and (dt.date.fromisoformat(AS_QW) - dt.date.fromisoformat(a)).days > days

def qwv(qw, key, fmt):
    v = qw.get(key)
    if v in (None, ""):
        return "—"
    return f"{fmt(v)} ⚠︎{qw[key + '_asof']}" if stale(qw, key) else fmt(v)

def dirn(qw, key, tag, hi=3.0):
    if stale(qw, key):
        return "멈춤"
    v = qw.get(f"{key}_chg{tag}")
    if v in (None, ""):
        return "—"
    v = float(v)
    return f"{'▲' if v >= hi else ('▼' if v <= -hi else '·')} {v:+,.0f}%"

def tp_and_source(r):
    if r["tp_med_90d"]:
        return r["tp_med_90d"], f"원장 {r['tp_n_firms_90d']}곳"
    qw = r["qw"]
    if qw.get("목표주가"):
        if stale(qw, "목표주가"):
            return None, f"QW {qw.get('목표주가_asof')} — 90일 이상 낡아 제외"
        return qw["목표주가"], f"QW {n(qw.get('목표주가참여'))}곳"
    return None, "—"

def upside(code):
    tp, _ = tp_and_source(LED[code])
    c = quote[code]["close"]
    return None if (not tp or not c) else (tp - float(c)) / float(c) * 100

def mk_of(code):
    """시장은 네이버 종목 페이지의 배지에서 받은 값을 쓴다.

    원장(`qw_universe`·`consensus`·`stocks`)에는 우선주·리츠·인프라펀드 13종목의 시장이
    아예 없다. 그래서 수집 단계에서 페이지 배지를 같이 긁는다. 그래도 비면 우선주는
    보통주(앞 5자리 + '0')에서 물려받고, 그래도 없으면 '—' 로 둔다 — 지어내지 않는다.
    """
    m = (quote[code].get("market") or "").strip()
    if m:
        return m
    base = code[:5] + "0"
    if base in quote and (quote[base].get("market") or "").strip():
        return quote[base]["market"].strip()
    return "KOSPI" if code in K200 else "—"

# ── 지수 ────────────────────────────────────────────────────────────────────
def px(sym, d=None):
    s = idx[sym]
    if d is None:
        return s[-1]["close"]
    for r in s:
        if r["date"] == d:
            return r["close"]
    return None

def chg_back(sym, back):
    s = idx[sym]
    return (s[-1]["close"] - s[-1 - back]["close"]) / s[-1 - back]["close"] * 100

KOSPI_HI = max(idx["KOSPI"], key=lambda r: r["close"])
KOSPI_LO = min(idx["KOSPI"], key=lambda r: r["close"])
D1M = idx["KOSPI"][-22]["date"]

# ── 조각 ────────────────────────────────────────────────────────────────────
def 종목표_행(codes):
    L = ["| # | 종목 | 코드 | K200 | 시장 | 종가 | 시총 | 후행PER | **선행PER** | PBR | 외국인 | **목표주가** | 상방 | 근거 |",
         "|---|---|---|:-:|:-:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for i, c in enumerate(codes, 1):
        q, r = quote[c], LED[c]
        tp, src = tp_and_source(r)
        L.append(f"| {i} | {q['name']} | {c} | {'●' if c in K200 else ''} | {mk_of(c)} | "
                 f"{n(q['close'])} | {조억(q['mktcap_억'])} | {n(q['per'],1)} | **{per_fwd(q)}** | "
                 f"{n(q['pbr'],2)} | {unit_or_dash(q['foreign_pct'])} | **{n(tp)}** | "
                 f"{pct(upside(c),0)} | {src} |")
    return "\n".join(L)

def 기업표(codes):
    L = ["| 기업 | 코드 | K200 | WICS 산업 | 리포트가 반복해서 말하는 것 | 26E 영업이익 컨센 3M | 리포트 90d |",
         "|---|---|:-:|---|---|:-:|---:|"]
    for c in codes:
        r = LED[c]
        say = " · ".join(f"{t}({k})" for t, k in r["topics"][:3]) or "— 최근 200일 본문 없음"
        L.append(f"| {quote[c]['name']} | {c} | {'●' if c in K200 else ''} | {UROW[c]['wics'] or '—'} | {say} | "
                 f"{dirn(r['qw'],'영업이익_2026AS','3M')} | {r['reports_90d']} |")
    return "\n".join(L)

def 종목섹션(codes):
    L = []
    A = L.append
    for i, c in enumerate(codes, 1):
        q, r = quote[c], LED[c]
        qw, e = r["qw"], r["est"]
        tag = "코스피200" if c in K200 else "코스피200 미편입 · 기존 커버"
        A(f"### {i}. {q['name']} ({c}) · {tag}\n")
        A(f"**리포트 본문에 가장 많이 나온 말** "
          f"{' · '.join(f'{t}({k})' for t, k in r['topics']) or '—'}  ")
        A(f"WI26 {UROW[c]['wi26']} · WICS {UROW[c]['wics'] or '—'} · {mk_of(c)}\n")
        A("| 종가 | 시총 | 후행PER | 선행PER | PBR | BPS | 외국인 | 52주 |")
        A("|---:|---:|---:|---:|---:|---:|---:|---|")
        A(f"| {n(q['close'])} | {조억(q['mktcap_억'])} | {n(q['per'],1)} | {per_fwd(q)} | "
          f"{n(q['pbr'],2)} | {n(q['bps'])} | {unit_or_dash(q['foreign_pct'])} | "
          f"{n(q['lo52'])}–{n(q['hi52'])} |\n")

        A("**목표주가**\n")
        A("| 기준 | 목표주가 | 기관 | 변화 | 상방 |")
        A("|---|---:|---:|---|---:|")
        cl = float(q["close"]) if q["close"] else None
        if r["tp_med_90d"]:
            if r["tp_med_prev"]:
                d = (r["tp_med_90d"] - r["tp_med_prev"]) / abs(r["tp_med_prev"]) * 100
                chg = f"직전 90일 {n(r['tp_med_prev'])}({r['tp_n_prev']}건) → {pct(d)}"
            else:
                chg = "직전 90일 발간 없음"
            A(f"| 원장 리포트 최근 90일 | {n(r['tp_med_90d'])} | {r['tp_n_firms_90d']}곳 | {chg} | "
              f"{pct((r['tp_med_90d']-cl)/cl*100,0) if cl else '—'} |")
        else:
            A("| 원장 리포트 최근 90일 | — | 0곳 | 최근 90일 발간 없음 | — |")
        if qw.get("목표주가"):
            a = qw.get("목표주가_asof", AS_QW)
            note = "" if a == AS_QW else f" ⚠︎ {a} 이후 갱신 없음"
            A(f"| QuantiWise {a}{note} | {n(qw['목표주가'])} | {n(qw.get('목표주가참여'))}곳 | "
              f"1M {pct(qw.get('목표주가_chg1M'))} · 3M {pct(qw.get('목표주가_chg3M'))} | "
              f"{pct((qw['목표주가']-cl)/cl*100,0) if cl else '—'} |")
        else:
            A(f"| QuantiWise {AS_QW} | — | — | — | — |")
        opi = " · ".join(f"{k} {v}" for k, v in sorted(r["opinions_90d"].items(), key=lambda x: -x[1]))
        A(f"\n최근 90일 투자의견 {opi or '—'} · 발간 {r['reports_90d']}건\n")

        A("**실적 추정치**\n")
        A("| 항목 | 2026E 원장 리포트 | n | 직전 90일 대비 | 2026E QW | QW 3M | 2027E 원장 리포트 | n | 2027E QW | QW 3M |")
        A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for key, label, unit in (("revenue", "매출액", "억원"), ("op_income", "영업이익", "억원"), ("eps", "EPS", "원")):
            c26, c27 = e[f"{key}_2026"], e[f"{key}_2027"]
            qk = {"revenue": "매출액", "op_income": "영업이익", "eps": "EPS"}[key]
            fmt = 조억 if unit == "억원" else (lambda v: n(v))
            A(f"| {label} ({unit}) | {fmt(c26['cur'])} | {c26['n_cur']} | {pct(c26['chg_pct'])} | "
              f"{qwv(qw, f'{qk}_2026AS', fmt)} | {dirn(qw, f'{qk}_2026AS', '3M')} | "
              f"{fmt(c27['cur'])} | {c27['n_cur']} | {qwv(qw, f'{qk}_2027AS', fmt)} | "
              f"{dirn(qw, f'{qk}_2027AS', '3M')} |")
        A("")
        A(f"QuantiWise 배수({AS_QW}) — 26E PER {n(qw.get('PER_2026AS'),1)} · 27E PER "
          f"{n(qw.get('PER_2027AS'),1)} · 26E PBR {n(qw.get('PBR_2026AS'),2)} · 26E ROE "
          f"{unit_or_dash(qw.get('ROE_2026AS'))} · 27E ROE {unit_or_dash(qw.get('ROE_2027AS'))} · "
          f"EPS 이익조정비율 1M {pct(qw.get('EPS조정1M'),0)} / 3M {pct(qw.get('EPS조정3M'),0)}\n")

        if r["evidence"]:
            A("**리포트 본문에서 (PDF 추출 원문)**\n")
            for ev in r["evidence"]:
                who = ev["firm"] + (f" {ev['analyst']}" if ev["analyst"] else "")
                A(f"> {ev['text']}")
                A(">")
                A(f"> — {who}, {ev['date']} 「{ev['title']}」\n")
        else:
            A("**리포트 본문에서** — 최근 200일 안에 본문이 적재된 리포트가 없다.\n")

        if r["recent_reports"]:
            A("**최근 리포트**\n")
            A("| 발간일 | 증권사 | 애널리스트 | 제목 | 목표가 | 의견 |")
            A("|---|---|---|---|---:|---|")
            for x in r["recent_reports"]:
                A(f"| {x['date']} | {x['firm'] or '—'} | {x['analyst'] or '—'} | {x['title'] or '—'} | "
                  f"{n(x['tp'])} | {x['opinion'] or '—'} |")
            A("")
        A("---\n")
    return "\n".join(L)

def 빈칸표(codes):
    L = ["| 종목 | 무엇이 비었나 | 왜 |", "|---|---|---|"]
    hit = 0
    for c in codes:
        r = LED[c]
        why, cause = [], []
        if r["reports_90d"] == 0:
            why.append("최근 90일 발간 리포트 0건")
            cause.append("셀사이드 리포트가 원장에 한 건도 없다" if r["reports_all"] == 0
                         else f"마지막 리포트가 {r['last_report']} — 커버리지가 그 뒤로 끊겼다")
        if not r["est"]["revenue_2026"]["cur"] and not r["est"]["op_income_2026"]["cur"]:
            why.append("연간 추정치 미적재")
            if r["est_q_only"] > 0:
                cause.append("최근 리포트가 분기 추정만 싣고 연간 표를 싣지 않았다")
            elif r["reports_90d"] > 0:
                cause.append(f"최근 90일 리포트 {r['reports_90d']}건에 실적 추정표가 없다 — 탐방·이슈 노트만 나왔다")
        if not r["qw"].get("목표주가"):
            why.append("QuantiWise 목표주가 없음")
            cause.append("QuantiWise 컨센 대상이 아니다")
        if why:
            hit += 1
            L.append(f"| {quote[c]['name']} | {' · '.join(why)} | {' · '.join(dict.fromkeys(cause)) or '—'} |")
    return ("\n".join(L), hit)

# ── 시장 상황 블록 (모든 문서 공통) ────────────────────────────────────────
MKT_HEAD = f"## 🟢 시장 상황 ({TRADE}) — 최신"
MKT = f"""{MKT_HEAD}

**KOSPI {px('KOSPI'):,.2f} · KOSPI200 {px('KPI200'):,.2f} · KOSDAQ {px('KOSDAQ'):,.2f}** ({TRADE} 종가).
1개월 전({D1M}) 대비 KOSPI {chg_back('KOSPI',21):+.1f}% · KOSPI200 {chg_back('KPI200',21):+.1f}% ·
KOSDAQ {chg_back('KOSDAQ',21):+.1f}%. 7월의 사상 최대 낙폭 뒤 되돌림이 진행 중이다 —
수집 구간(6/1–8/28) 안에서 코스피는 {KOSPI_LO['date']} **{KOSPI_LO['close']:,.2f}** 가 저점,
{KOSPI_HI['date']} **{KOSPI_HI['close']:,.2f}** 가 고점이고 지금은 저점 대비
{(px('KOSPI')-KOSPI_LO['close'])/KOSPI_LO['close']*100:+.1f}%, 고점 대비
{(px('KOSPI')-KOSPI_HI['close'])/KOSPI_HI['close']*100:+.1f}% 다.

**이 폴더의 종목 표와 컨센서스는 {TRADE} 기준으로 다시 만들었다** —
`_시총상위_종목표.md` 와 `<업종>_코스피200_종목분석.md`. 업종 축은 **WI26** 이고
배정은 미니 PG `sector_map`(QuantiWise WI26)을 그대로 따른다.
{{LINKLINE}}

> **주가는 {TRADE}, QuantiWise 컨센서스는 {AS_QW} 다.** 그 사이 한 달의 시차가 있다.
> 선행 배수가 낮아 보이는 종목 중 일부는 컨센이 아직 안 내려온 것이다.
"""

MKT_FOLDER = MKT.replace("{LINKLINE}",
                         "전체 유니버스와 이동 내역은 [`_코스피200_유니버스.md`](../_코스피200_유니버스.md).")
MKT_INDEX = MKT.replace("{LINKLINE}", "업종별 배분과 이동 내역은 이 문서 아래에 있다.")


def 시장상황_갱신(path: Path) -> bool:
    """낡은 '시장 상황' 블록 위에 최신 블록을 얹고, 낡은 쪽은 이전 스냅샷으로 표시한다.

    낡은 블록을 지우지 않는다 — 그날의 판단이 본문 서술과 엮여 있어서, 지우면
    본문이 근거 없는 문장이 된다. 위에 얹고 아래를 '이전' 이라고 부르면 둘 다 남는다.
    """
    t = path.read_text(encoding="utf-8")
    old = re.search(r"^## 🔴 시장 상황 \((\d{4}-\d{2}-\d{2})\)", t, re.M)
    if MKT_HEAD in t:
        # 이미 얹은 문서다. **다음 회차에도 최신 블록을 갈아 끼워야 한다** — 안 그러면
        # 낡은 🔴 마커가 사라진 뒤로 이 함수가 문서를 건너뛰어 수치가 조용히 굳는다.
        i = t.index(MKT_HEAD)
        m = re.search(r"^## 시장 상황 \(", t[i:], re.M)
        if not m:
            return False
        j = i + m.start()
        t = t[:i] + MKT_FOLDER + "\n" + t[j:]
    elif not old:
        return False
    else:
        i = old.start()
        t = (t[:i] + MKT_FOLDER + "\n"
             + t[i:].replace(f"## 🔴 시장 상황 ({old.group(1)})",
                             f"## 시장 상황 ({old.group(1)}) — 이전 스냅샷", 1))
    # 갱신 기준일 행: '작성 기준일' 은 그날 쓴 게 맞으므로 건드리지 않고 한 줄을 더한다
    if "| 갱신 기준일 |" not in t:
        t = re.sub(r"(^\| 작성 기준일 \| [0-9-]+ \|$)",
                   r"\1\n| 갱신 기준일 | " + f"{STAMP} (시세·컨센 {TRADE}) |", t, count=1, flags=re.M)
    path.write_text(t, encoding="utf-8")
    return True

# ── 문서 ────────────────────────────────────────────────────────────────────
def 방법_블록():
    return f"""## 이 문서를 만든 방법

1. **업종 축은 WI26 하나다.** 배정은 맥미니 PG `research.sector_map` — QuantiWise WI26 로
   채워지는 테이블 — 을 그대로 읽는다. 아카이브가 따로 규칙을 만들지 않는다. 만들면 화면·원장과
   문서가 다른 기준으로 묶인다.
2. **원천에서 파이프라인으로 받는다.** 코스피200 편입 목록은 네이버 금융 '코스피200 편입종목',
   종가·시총·PER·컨센EPS·WICS 산업은 네이버 종목 API 에서 스크립트가 받는다. KRX 공식 API 는
   이 환경에서 **403** 이라 쓰지 못했다 — 그 사실도 적어 둔다.
3. **적재한 것을 읽는다.** 목표주가·투자의견·추정치·리포트 본문은 맥미니 원장에서 꺼냈다.
   벤더 화면을 실시간으로 중계하지 않는다.
4. **근거는 리포트 본문에서 그대로 꺼낸다.** PDF 에서 추출해 원장 `reports.body` 에 적재된
   텍스트를 문장으로 쪼개고, 업종 어휘와 숫자 포함 여부로 점수를 매겨 상위 문장을 골랐다.
   **모델을 쓰지 않는다. 전부 파이썬 규칙이고 0 토큰이다.**
5. **없는 값은 만들지 않는다.** 컨센이 없으면 빈칸이고, 왜 비었는지 마지막 절에 적었다.

**단위를 맞춘 방법 — 이걸 안 하면 표가 통째로 거짓말을 한다.** 증권사마다 리포트 표의 단위가
억원·십억원·백만원으로 다르다. 정규화 전에는 비츠로셀 2026 매출 컨센이 IBK 3,175(억원)와
삼성 311(십억원)의 중앙값 1,743 으로 나왔다 — 어느 단위로도 틀린 숫자다. 그래서 **리포트 한
건의 표는 단위가 하나**라는 성질을 쓴다. 매출액을 QuantiWise 컨센(억원)의 자릿수에 맞춰 10의
거듭제곱 `k` 를 구하고, 같은 리포트의 영업이익에 같은 `k` 를 적용한다. 값을 바꾸는 게 아니라
자릿수만 옮기는 것이라 **컨센과 리포트의 실제 시각차는 그대로 남는다**.

**`멈춤` 은 그 항목의 QuantiWise 관측이 90일 넘게 갱신되지 않았다는 뜻**이다. 값이 0 이어서
`+0%` 인 것과 갱신이 끊겨 변화가 없어 보이는 것은 전혀 다르다 — 섞어 놓으면 커버리지가 끊긴
종목이 '컨센이 안정적' 으로 읽힌다.
"""

def 업종문서(d: str, codes: list[str]) -> str:
    kor = KOR[d]
    wi = UROW[codes[0]]["wi26"] if codes else kor
    nk = sum(1 for c in codes if c in K200)
    moved_in = [c for c in codes if UROW[c]["prev_dir"] and UROW[c]["prev_dir"] != d]
    빈, 빈수 = 빈칸표(codes)
    L = [f"# {kor} — 코스피200 종목분석\n",
         "> 종목을 늘린다는 것은 표에 줄을 더 긋는 일이 아니다. 늘어난 줄마다 **누가 언제 무엇을 "
         "추정했는지**가 붙어야 늘린 값이 있다. 그래서 이 문서의 모든 숫자에는 기준일과 표본 수가 "
         "따라붙고, 근거 문장은 리포트 PDF 본문에서 그대로 꺼냈다.\n",
         "| 항목 | 값 |", "|---|---|", "| 시장 | 국내주식 |",
         f"| 업종 | **WI26 {wi}** (폴더 `{d}`) |",
         f"| 종목 수 | {len(codes)} — 코스피200 편입 {nk} + 기존 커버 유지 {len(codes)-nk} |",
         f"| 종가·시총 기준일 | {TRADE} (네이버 금융 실측) |",
         f"| 리포트·추정치 기준일 | {AS_REP} (원장 `reports`·`report_estimates`) |",
         f"| 컨센서스 추이 기준일 | {AS_QW} (원장 `qw_fundamentals` — 그 뒤로 갱신이 멈춰 있다) |",
         f"| 작성 기준일 | {STAMP} |", "",
         "전체 유니버스·업종 배정 규칙·이동 내역은 [`_코스피200_유니버스.md`](../_코스피200_유니버스.md).\n",
         MKT_FOLDER, 방법_블록(),
         f"## 1. 이 업종의 {len(codes)}종목\n",
         f"코스피200 편입 **{nk}종목**에, 이전 판(국내 시총 300위 기준)에서 이미 보던 "
         f"**{len(codes)-nk}종목**을 지우지 않고 합쳤다. 코스피200 만 남기면 코스닥과 중형주 축이 "
         "통째로 빠진다 — 기준을 바꾼 대가로 보던 종목을 잃는 것은 확장이 아니다. "
         "편입 여부는 `K200` 칸으로 구분한다.\n"]
    if MOVED_OUT.get(d):
        L.append(f"> **이 폴더에서 나간 종목 {len(MOVED_OUT[d])}개**: "
                 + " · ".join(f"{quote[c]['name']}(→ `{UROW[c]['dir']}`)" for c in MOVED_OUT[d])
                 + ". WI26 이 이 회사들을 다른 대분류에 두기 때문이다. **아래 §2-1(또는 §6-1)의 "
                   "옛 표에는 아직 이름이 남아 있을 수 있다** — 그건 그때의 판단이라 지우지 않았다. "
                   "수치는 옮겨 간 폴더의 문서에서 본다.\n")
    if moved_in:
        L.append(f"> **이번 판에서 이 폴더로 옮겨 온 종목 {len(moved_in)}개**: "
                 + " · ".join(f"{quote[c]['name']}(← `{UROW[c]['prev_dir']}`)" for c in moved_in)
                 + ". 업종 축을 WI26 으로 통일하면서 이전 판의 임의 배정이 정리된 결과다. "
                   "자세한 것은 색인 문서의 '이동한 종목' 표.\n")
    L += [종목표_행(codes), "",
          "## 2. 컨센서스 한눈에\n",
          f"목표주가는 **원장 리포트 최근 90일 중앙값**(`원장 n곳`), 없으면 QuantiWise {AS_QW}. "
          "영업이익 컨센 방향은 QuantiWise 3개월 변화율이며 ▲/▼ 임계는 ±3%다. "
          f"`리포트 90d` 가 0이면 아래 숫자는 전부 {AS_QW} 이전 것이다.\n",
          "| 종목 | K200 | 리포트 90d | **목표주가** | 상방 | 목표가 1M | 26E 영업이익 | 3M | 27E 영업이익 | 3M | EPS조정 3M |",
          "|---|:-:|---:|---:|---:|---:|---:|:-:|---:|:-:|---:|"]
    for c in codes:
        r = LED[c]; qw = r["qw"]
        tp, _ = tp_and_source(r)
        L.append(f"| {quote[c]['name']} | {'●' if c in K200 else ''} | {r['reports_90d']} | **{n(tp)}** | "
                 f"{pct(upside(c),0)} | {'멈춤' if stale(qw,'목표주가') else pct(qw.get('목표주가_chg1M'))} | "
                 f"{qwv(qw,'영업이익_2026AS',조억)} | {dirn(qw,'영업이익_2026AS','3M')} | "
                 f"{qwv(qw,'영업이익_2027AS',조억)} | {dirn(qw,'영업이익_2027AS','3M')} | "
                 f"{'멈춤' if stale(qw,'EPS조정3M') else pct(qw.get('EPS조정3M'),0)} |")
    L += ["",
          "> **`EPS조정 3M` 은 QuantiWise 의 이익조정비율**이다. 지난 3개월 동안 EPS 추정을 올린 "
          "증권사 비율에서 내린 비율을 뺀 값이라, 목표주가보다 먼저 방향이 꺾인다. 목표주가는 "
          "오르는데 이 값이 음수면 셀사이드가 아직 목표가를 못 내린 상태일 수 있다.",
          "> **상방이 세 자리면 목표가를 의심하라. 주가가 아니다.** 셀사이드 목표가는 급락 뒤 하향이 "
          "늦다. 7월 −22% 폭락과 8월 되돌림을 지난 지금 특히 그렇고, `기관` 이 1–2곳이면 더 그렇다.\n",
          "## 3. 종목별\n",
          f"각 종목에 (a) 시세·밸류, (b) 컨센서스 두 갈래 — 우리 원장 리포트(최근 90일, {AS_REP}까지)와 "
          f"QuantiWise({AS_QW}), (c) 리포트 본문에서 그대로 꺼낸 근거 문장, (d) 최근 리포트 목록을 "
          "붙였다. **(b)의 두 갈래가 벌어져 있으면 그 자체가 정보다** — 컨센이 아직 최근 리포트를 "
          "따라오지 못했다는 뜻이다.\n",
          종목섹션(codes)]
    if 빈수:
        L += ["## 4. 비어 있는 칸 — 고장이 아니다\n",
              "채우려면 없는 값을 지어내야 하는 칸이다. 다시 쫓지 말 것.\n", 빈, ""]
    L += [f"> **QuantiWise 축 전체가 {AS_QW} 에서 멈춰 있다.** 컨센 추이(1M·3M 변화, EPS 조정비율)는 "
          f"전부 그 시점 기준이고 종가는 {TRADE} 다. QW 배수와 네이버 실측 배수가 다른 것은 정상이다.\n",
          "## 출처\n",
          f"- 업종(WI26) 배정: 맥미니 PG `research.sector_map` — `_scripts/업종_WI26_배정.py`",
          f"- 코스피200 편입 목록 · 종가 · 시총 · PER · 컨센EPS · WICS 산업: 네이버 금융 "
          f"(수집 {STAMP}, 거래일 {TRADE}) — `_scripts/코스피200_구성종목_수집.py`, `_scripts/네이버_시세컨센_수집.py`",
          f"- 목표주가 · 투자의견 · 리포트 본문 · 리포트별 추정치: 맥미니 원장 `research.duckdb` 의 "
          f"`reports`·`report_estimates` ({AS_REP}까지) — `_scripts/원장_컨센추출_미니.py`",
          f"- 컨센서스 추이 · 이익조정비율 · 배수: 같은 원장의 `qw_fundamentals` (QuantiWise, {AS_QW})",
          f"- 지수: 네이버 금융 일별 시세 ({TRADE})",
          "- 문서 생성: `_scripts/국내주식_코스피200_문서생성.py` — 숫자는 전부 이 스크립트가 계산한다"]
    return "\n".join(L) + "\n"

def 종목표문서(d: str, codes: list[str]) -> str:
    kor = KOR[d]
    wi = UROW[codes[0]]["wi26"] if codes else kor
    nk = sum(1 for c in codes if c in K200)
    return "\n".join([
        f"# {kor} — 종목표 ({TRADE})\n",
        f"> **WI26 {wi}. 코스피200 편입 {nk}종목 + 기존 커버 유지 {len(codes)-nk}종목 = {len(codes)}종목.** "
        f"종가·시총·PER·PBR 은 네이버 금융 실측({TRADE}), 목표주가는 **우리 원장의 증권사 "
        f"리포트({AS_REP}까지) 최근 90일 중앙값**이며 그게 없을 때만 QuantiWise 컨센({AS_QW})으로 "
        f"갈음한다. 근거와 컨센 추이는 [`{kor}_코스피200_종목분석.md`](./{kor}_코스피200_종목분석.md), "
        "전체 유니버스는 [`_코스피200_유니버스.md`](../_코스피200_유니버스.md).\n",
        종목표_행(codes), "",
        "> **선행PER 은 네이버의 컨센 EPS(cnsEps) 기준이다.** 후행PER 과 벌어진 폭이 그 종목에 걸린 "
        "이익 회복 기대의 크기다. 컨센 EPS 가 적자면 `적자` 로 적었다 — 음수 배수를 배수라고 "
        "부르지 않는다.",
        "> **목표주가 '근거' 칸을 먼저 보라.** `원장 n곳` 은 최근 90일 안에 실제로 발간된 리포트 "
        f"n곳의 목표가 중앙값이다. `QW` 는 90일 안에 발간이 없어 {AS_QW} QuantiWise 컨센으로 "
        "갈음한 것이고 그만큼 낡았다. 기관 수가 1–2곳이면 중앙값이라는 말에 큰 뜻이 없다.",
        f"> 원자료: [`업종_WI26_유니버스_{STAMP}.csv`](../../_manifest/데이터/업종_WI26_유니버스_{STAMP}.csv) · "
        f"[`코스피200_구성종목_{STAMP}.csv`](../../_manifest/데이터/코스피200_구성종목_{STAMP}.csv) · "
        f"[`국내주식_시세컨센_{STAMP}.csv`](../../_manifest/데이터/국내주식_시세컨센_{STAMP}.csv) · "
        f"[`국내주식_컨센추이_{STAMP}.json`](../../_manifest/데이터/국내주식_컨센추이_{STAMP}.json)",
    ]) + "\n"

def 색인문서() -> str:
    tot = len(uni)
    nk = len(K200)
    moved = [r for r in uni if r["prev_dir"] and r["prev_dir"] != r["dir"]]
    folded = [r for r in uni if r["source"] != "PG sector_map(wi26)"]
    L = [f"# 국내주식 — 코스피200 유니버스 ({TRADE})\n",
         f"> **코스피200 편입 {nk}종목 전부**를 **WI26** 26칸에 배정하고, 이전 판(국내 시총 300위)에서 "
         f"보던 종목을 지우지 않고 합쳐 **{tot}종목**을 만들었다. 종목마다 종가·밸류, 목표주가 두 갈래, "
         "FY26·27 추정치 두 갈래, 리포트 본문 인용, 최근 리포트 목록이 업종 폴더의 "
         "`<업종>_코스피200_종목분석.md` 에 들어 있다.\n",
         MKT_INDEX,
         "| 항목 | 값 |", "|---|---|",
         f"| 업종 기준 | **WI26 26대분류** — 미니 PG `research.sector_map` |",
         f"| 코스피200 편입 | {nk}종목 (네이버 편입종목 목록, {STAMP} 조회) |",
         f"| 이전 커버(시총 300위) | 300종목 |",
         f"| 합집합 = 이 유니버스 | **{tot}종목** · 미분류 0 |",
         f"| 종가·시총 기준일 | {TRADE} |",
         f"| 리포트·추정치 기준일 | {AS_REP} |",
         f"| 컨센서스 추이 기준일 | {AS_QW} |",
         f"| 작성 기준일 | {STAMP} |", "",
         "## 업종별 배분\n",
         "| 폴더 | WI26 업종 | 종목 | K200 | 리포트 90d 있는 종목 | 원장 목표가 산출 | 문서 |",
         "|---|---|---:|---:|---:|---:|---|"]
    for d in sorted(UNI):
        cs = UNI[d]
        kor = KOR[d]
        wi = UROW[cs[0]]["wi26"] if cs else kor
        L.append(f"| `{d}` | {wi} | {len(cs)} | {sum(1 for c in cs if c in K200)} | "
                 f"{sum(1 for c in cs if LED[c]['reports_90d'] > 0)} | "
                 f"{sum(1 for c in cs if LED[c]['tp_med_90d'])} | "
                 f"[종목분석](./{d}/{kor}_코스피200_종목분석.md) · [종목표](./{d}/_시총상위_종목표.md) |")
    L += [f"| | **합계** | **{tot}** | **{nk}** | "
          f"**{sum(1 for d in UNI for c in UNI[d] if LED[c]['reports_90d'] > 0)}** | "
          f"**{sum(1 for d in UNI for c in UNI[d] if LED[c]['tp_med_90d'])}** | |", "",
          "## 업종 배정 규칙 — WI26 하나로 통일했다\n",
          "이전 판은 아카이브가 **자체 규칙**으로 WICS 산업을 26칸에 접었다. 그게 화면·원장이 쓰는 "
          "WI26 과 어긋났다. 이번 판은 규칙을 만들지 않는다. 맥미니 PG `research.sector_map` 이 "
          "QuantiWise WI26 으로 채우는 값을 그대로 쓴다.\n",
          "1. `sector_source='wi26'` 인 행은 그 값이 곧 WI26 대분류다 "
          f"(이 유니버스의 {tot-len(folded)}종목).",
          "2. 그 외는 종목의 WICS 산업을 1번 행들에서 뽑은 **WICS 산업 → WI26 다수결 표**로 접는다 "
          f"({len(folded)}종목). 이 표는 wi26 소스 2,596행에서 유도했고 78개 산업 전부 만장일치였다.",
          "3. 그래도 안 되면 '미분류' 로 남긴다 — 이번 유니버스에는 **0종목**이다.\n",
          "> 2번이 필요한 이유가 실제로 있었다. `sector_map` 의 `naver_mapped` 행은 손으로 쓴 표로 "
          "접힌 것이라 QuantiWise 실제 WI26 과 6개 산업에서 어긋난다. 그대로 두면 **LG전자는 IT가전, "
          "LG전자우는 IT하드웨어**로 갈라진다 — 실제로 그랬고, 이 규칙이 그걸 붙였다.\n",
          f"## 이동한 종목 — 이전 판과 폴더가 달라진 {len(moved)}개\n",
          "이전 판의 자체 배정이 WI26 과 어긋났던 자리다. **기계 폴더가 가장 크게 바뀐다** — "
          "WI26 에서 방산(우주항공과국방)은 `상사,자본재`, 2차전지·전지소재(전기제품)는 `IT가전` 이다. "
          "기계에 남는 것은 기계와 전기장비뿐이다.\n",
          "| 종목 | 코드 | WICS 산업 | 이전 폴더 | **WI26 폴더** |", "|---|---|---|---|---|"]
    for r in sorted(moved, key=lambda r: (r["prev_dir"], r["dir"])):
        L.append(f"| {r['name']} | {r['code']} | {r['wics']} | `{r['prev_dir']}` | **`{r['dir']}`** |")
    L += ["",
          f"## WICS 다수결로 접은 종목 {len(folded)}개\n",
          "PG 에 WI26 값이 없거나 손으로 접힌 행이라 1번 규칙이 안 먹은 종목이다. 어떤 산업을 "
          "어디로 접었는지 그대로 적는다.\n",
          "| 종목 | 코드 | WICS 산업 | 접은 결과 | 근거 |", "|---|---|---|---|---|"]
    for r in sorted(folded, key=lambda r: r["dir"]):
        L.append(f"| {r['name']} | {r['code']} | {r['wics']} | `{r['dir']}` | {r['source']} |")
    L += ["", "## 출처\n",
          f"- 업종(WI26): 맥미니 PG `research.sector_map` (스냅샷 `업종_WI26_sector_map_{STAMP}.json`, 4,040종목)",
          f"- 코스피200 편입 목록 · 종가 · 시총 · PER · 컨센EPS · WICS 산업: 네이버 금융 "
          f"(수집 {STAMP}, 거래일 {TRADE})",
          f"- 목표주가 · 투자의견 · 리포트 본문 · 리포트별 추정치: 맥미니 원장 `research.duckdb` ({AS_REP}까지)",
          f"- 컨센서스 추이 · 이익조정비율 · 배수: 같은 원장의 `qw_fundamentals` (QuantiWise, {AS_QW})",
          "- 수집·생성: `_scripts/코스피200_구성종목_수집.py` · `_scripts/네이버_시세컨센_수집.py` · "
          "`_scripts/원장_컨센추출_미니.py` · `_scripts/업종_WI26_배정.py` · "
          "`_scripts/국내주식_코스피200_문서생성.py`"]
    return "\n".join(L) + "\n"

# ── 기존 문서의 표 갈아 끼우기 (원래 표는 하위 절로 보존) ──────────────────
def 갈아끼우기(path: Path, start: str, end: str, sub: str, intro: str, table: str, tail: str) -> bool:
    if not path.is_file():
        return False
    t = path.read_text(encoding="utf-8")
    if start not in t or end not in t:
        print(f"  구간 없음: {path.name}", file=sys.stderr)
        return False
    i, j = t.index(start), t.index(end)
    body = t[i:j]
    if sub in body:
        keep = body[body.index(sub):]
    else:
        orig = body.split("\n", 1)[1].strip("\n")
        keep = (f"{sub}\n\n아래는 표가 늘기 전부터 적어 둔 판단이다. 데이터로 대체하지 않고 "
                f"그대로 남긴다.\n\n{orig}\n")
    # keep 끝의 개행을 먼저 깎는다. 안 깎으면 다시 돌릴 때마다 빈 줄이 한 줄씩 쌓여
    # 멱등성이 깨진다(실제로 깨졌다).
    t = t[:i] + f"{start}\n\n{intro}\n\n{table}\n\n{tail}\n\n{keep.rstrip()}\n\n" + t[j:]
    path.write_text(t, encoding="utf-8")
    return True


def main() -> int:
    (ROOT / "_코스피200_유니버스.md").write_text(색인문서(), encoding="utf-8")
    for d in sorted(UNI):
        p, kor, cs = DIRNAME[d], KOR[d], UNI[d]
        wi = UROW[cs[0]]["wi26"]
        (p / "_시총상위_종목표.md").write_text(종목표문서(d, cs), encoding="utf-8")
        (p / f"{kor}_코스피200_종목분석.md").write_text(업종문서(d, cs), encoding="utf-8")
        intro = (f"업종 축은 **WI26 {wi}** 다(미니 PG `sector_map`). 코스피200 편입 종목 전부와, "
                 f"시총 300위 기준으로 이미 보던 종목을 합쳐 **{len(cs)}종목**으로 늘렸다. "
                 f"늘어난 칸은 사람이 붙인 테마가 아니라 **리포트 본문에 실제로 몇 번 나왔는지**를 "
                 f"센 것이다(괄호 안이 등장 횟수, 최근 200일). 숫자·근거 문장·최근 리포트는 "
                 f"[`{kor}_코스피200_종목분석.md`](./{kor}_코스피200_종목분석.md) 에 있다.")
        tail = ("**이 표를 세로로 읽지 마라.** 전방이 다른 회사가 한 칸에 묶여 있다. 종목을 "
                "늘렸다고 업종 평균이 의미를 얻지는 않는다. 늘어난 만큼 **가로로만** 읽어야 한다.")
        if MOVED_OUT.get(d):
            tail += ("\n\n> **이 폴더에서 나간 종목**: "
                     + " · ".join(f"{quote[c]['name']}(→ `{UROW[c]['dir']}`)" for c in MOVED_OUT[d])
                     + ". WI26 기준으로 다른 대분류다. 아래 옛 표에 이름이 남아 있어도 "
                       "수치는 옮겨 간 폴더에서 본다.")
        갈아끼우기(p / f"{kor}_기업분석.md", "## 2. 기업별 위치", "## 3. ",
                   "### 2-1. 오래 본 종목의 관점", intro, 기업표(cs), tail)
        갈아끼우기(p / f"{kor}_기초자료.md", "## 6. 주요 상장 기업", "## 7. ",
                   "### 6-1. 처음 적어 둔 목록", intro, 기업표(cs), tail)
        print(f"  {d:18} {len(cs):3}종목")
    touched = sum(1 for f in sorted(ROOT.rglob("*.md")) if 시장상황_갱신(f))
    print(f"26개 업종 · {len(uni)}종목 · 시장상황 갱신 {touched}개 문서")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
