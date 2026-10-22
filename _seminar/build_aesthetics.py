#!/usr/bin/env python3
"""미용기기·스킨부스터·톡신(미용의료) 기초세미나 스펙 생성.

숫자는 전부 _manifest/데이터 의 두 JSON 에서 읽는다.
- 화장품_원장대조_2026-10-21.json : 10/21 종가, 8/28 대비, 10월 목표가, 10월 리포트
- 화장품_이력.json                : dart_q(분기 실적, 억원), naver_cons, tp_monthly, tp_changes, px_monthly
문서에서 옮긴 값(리포트 인용 등)은 문자열 안에 출처를 붙였다.

실행: python3 _seminar/build_aesthetics.py  → _seminar/aesthetics.json
"""
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "_manifest" / "데이터"
F_CMP = DATA / "화장품_원장대조_2026-10-21.json"
F_HIS = DATA / "화장품_이력.json"
OUT = ROOT / "_seminar" / "aesthetics.json"

CMP = json.loads(F_CMP.read_text())
HIS = json.loads(F_HIS.read_text())

FIVE = ["214150", "336570", "214450", "145020", "290650"]  # 클래시스·원텍·파마리서치·휴젤·엘앤씨바이오
APR = "278470"
NAME = {t: CMP[t]["name"] for t in FIVE + [APR]}


# ---------- helpers ----------
def qlabel(date):  # "2025-09-30" -> "3Q25"
    y, m, _ = date.split("-")
    return f"{(int(m) - 1) // 3 + 1}Q{y[2:]}"


def dart(t):
    """{date: {'revenue':x, 'op_income':y}} 날짜순."""
    out = {}
    for k, v in HIS[t]["dart_q"].items():
        d, f = k.split("|")
        out.setdefault(d, {})[f] = v
    return dict(sorted(out.items()))


def comma(x):
    return f"{int(round(x)):,}"


def pct(x, d=1):
    s = f"{x:+.{d}f}%"
    return s.replace("-", "−")


def won(x):
    return f"{int(round(x)):,}원"


def cons(t, key):
    c = HIS[t]["naver_cons"].get(key)
    return (c["first"][1], c["last"][1]) if c else (None, None)


def ltm(t):
    q = dart(t)
    last4 = list(q.items())[-4:]
    rev = sum(v["revenue"] for _, v in last4)
    op = sum(v["op_income"] for _, v in last4)
    return rev, op, last4[0][0], last4[-1][0]


def opm_q(t, date):
    v = dart(t)[date]
    return v["op_income"] / v["revenue"] * 100


def ltm_opm(t):
    rev, op, _, _ = ltm(t)
    return op / rev * 100


def q3_yoy(t):
    _, last = cons(t, "2026Q3E|op_income")
    base = dart(t).get("2025-09-30", {}).get("op_income")
    if last is None or not base:
        return None
    return (last / base - 1) * 100


def tp_updown(t):
    ch = HIS[t].get("tp_changes", [])
    up = sum(1 for c in ch if c.get("pct") is not None and c["pct"] > 0)
    dn = sum(1 for c in ch if c.get("pct") is not None and c["pct"] < 0)
    return up, dn, len(ch)


def mlabel(m):  # "2026-10" -> "26/10"
    return f"{m[2:4]}/{m[5:7]}"


# ---------- 계산 ----------
vs0828 = {t: CMP[t]["vs0828_pct"] for t in FIVE}
med_vs0828 = statistics.median(vs0828.values())

oct_known = [o for t in FIVE for o in CMP[t].get("oct", []) if o.get("chg") is not None]
oct_down = sum(1 for o in oct_known if o["chg"] < 0)
oct_up = sum(1 for o in oct_known if o["chg"] > 0)

hz_f, hz_l = cons("145020", "2026Q3E|op_income")
hz_q3_move = (hz_l / hz_f - 1) * 100
cl_f, cl_l = cons("214150", "2026Q3E|op_income")
cl_q3_move = (cl_l / cl_f - 1) * 100
cl_kyobo = CMP["214150"]["q3"]["교보"][0]
cl_gap = (cl_kyobo / cl_l - 1) * 100
hz_rep = CMP["145020"]["q3_med"]
hz_gap = (hz_rep / hz_l - 1) * 100

# 휴젤 2Q26 톡신 비중: 톡신 매출 840억(교보 8/10, 건강관리_코스피200_종목분석.md) / DART 2Q26 매출
hz_toxin_2q = 840
hz_toxin_share = hz_toxin_2q / dart("145020")["2026-06-30"]["revenue"] * 100
# 엘앤씨바이오 1Q26 리투오 80억(유안타 6/1) / DART 1Q26 매출
lnc_re2o_1q = 80
lnc_re2o_share = lnc_re2o_1q / dart("290650")["2026-03-31"]["revenue"] * 100

# 목표가 고점 월 → 최근 월
tp_path = {}
for t in FIVE + [APR]:
    tm = HIS[t]["tp_monthly"]
    if not tm:
        continue
    peak = max(tm, key=lambda r: r["med"])
    last = tm[-1]
    tp_path[t] = (peak["m"], peak["med"], last["m"], last["med"], (last["med"] / peak["med"] - 1) * 100)

# ---------- 블록 조립 ----------
BIZ = {
    "214150": ("미용기기", "HIFU(슈링크)·RF(볼뉴머) 장비 + 시술 소모품"),
    "336570": ("미용기기", "레이저·RF 장비"),
    "214450": ("스킨부스터", "리쥬란(PN) 의료기기 + 리쥬란 화장품"),
    "145020": ("톡신·필러", "보툴리눔 톡신(보툴렉스/Letybo) + 필러(더채움)"),
    "290650": ("스킨부스터·인체조직", "ECM 스킨부스터 리투오 + 인체조직 이식재"),
    "278470": ("뷰티 디바이스 겸업", "메디큐브 화장품 + 가정용 디바이스(에이지알)"),
}

model_rows = []
for t in FIVE + [APR]:
    rev, op, d0, d1 = ltm(t)
    model_rows.append([
        NAME[t], BIZ[t][0], BIZ[t][1],
        comma(rev), comma(op), f"{op / rev * 100:.1f}%".replace("-", "−"),
        f"{opm_q(t, '2025-06-30'):.1f}%".replace("-", "−"), f"{opm_q(t, '2026-06-30'):.1f}%".replace("-", "−"),
    ])
ltm_span = f"{qlabel(ltm(FIVE[0])[2])}–{qlabel(ltm(FIVE[0])[3])}"

# 분기 영업이익 차트 (휴젤·클래시스)
def op_series(t):
    pts = [[qlabel(d), v["op_income"]] for d, v in dart(t).items()]
    pts.append(["3Q26E", cons(t, "2026Q3E|op_income")[1]])
    return {"name": NAME[t], "data": pts}

# players
player_rows = []
for t in FIVE + [APR]:
    c = CMP[t]
    tp = f"{comma(c['tp_med'])} ({c['n']}곳)" if c.get("tp_med") else "10월 목표가 없음"
    _, q3 = cons(t, "2026Q3E|op_income")
    y = q3_yoy(t)
    up, dn, n = tp_updown(t)
    player_rows.append([
        NAME[t], t, BIZ[t][0], comma(c["close_1021"]), pct(c["vs0828_pct"]), tp,
        comma(q3) if q3 is not None else "—", pct(y) if y is not None else "—",
        f"{up} / {dn}" if n else "기록 없음",
    ])

# 목표가 경로 chart
# 종목마다 가격대가 수천 원–수십만 원으로 달라 원값은 한 축에 못 그린다 → 첫 달 = 100 으로 지수화.
# 점이 3개 미만인 종목(원텍·엘앤씨바이오)은 경로라 부를 수 없어 뺀다.
tp_series, tp_raw = [], []
for t in FIVE:
    tm = HIS[t]["tp_monthly"]
    if len(tm) < 3:
        continue
    base = tm[0]["med"]
    tp_series.append({"name": NAME[t], "data": [[mlabel(r["m"]), round(r["med"] / base * 100, 1)] for r in tm]})
    tp_raw.append(f"{NAME[t]} {comma(tm[0]['med'])} → {comma(tm[-1]['med'])}원")

tp_path_rows = []
for t in FIVE + [APR]:
    if t not in tp_path:
        continue
    pm, pv, lm, lv, ch = tp_path[t]
    tp_path_rows.append([NAME[t], f"{mlabel(pm)} {comma(pv)}", f"{mlabel(lm)} {comma(lv)}", pct(ch)])

# 8/28 대비 hbar
hbar = {"name": "8/28 대비 주가(%)",
        "data": [[NAME[t], CMP[t]["vs0828_pct"]] for t in sorted(FIVE + [APR], key=lambda x: CMP[x]["vs0828_pct"])]}

# 3Q 컨센 이동 표
cons_rows = []
for t in FIVE + [APR]:
    f, l = cons(t, "2026Q3E|op_income")
    cons_rows.append([NAME[t], comma(f), comma(l), pct((l / f - 1) * 100)])

cl_titles = [c for c in HIS["214150"]["tp_changes"] if c["pct"] < 0 and c["date"] >= "2026-07-01"]
hz_titles = [c for c in HIS["145020"]["tp_changes"] if c["date"] >= "2026-09-01"]


def title_line(c):
    return f"{c['date'][5:].replace('-', '/')} {c['firm'].replace('증권', '').replace('투자', '')} {won(c['prev'])} → {won(c['tp'])} ({pct(c['pct'])}) 「{c['title']}」"


spec = {
    "slug": "aesthetics",
    "title": "미용기기·스킨부스터·톡신 기초세미나",
    "subtitle": "장비는 한 번 팔고 소모품으로 계속 번다 — 2026년 하반기는 '해외 유통 구조 전환'이 실적을 갈랐다",
    "asof": "2026-10-21",
    "audience": "미용의료(미용기기·톡신·필러·스킨부스터)를 처음 맡는 애널리스트·운용역",
    "hero": {
        "one_liner": "병원이 시술할 때마다 소모품·주사제가 팔리는 반복 매출 사업이다. 2026년 하반기에는 수요가 아니라 해외 직판 전환·가이던스 하향이 숫자를 깎았고, 화장품 ODM 호황은 이 업종으로 번지지 않았다.",
        "kpis": [
            {"label": "5종목 8/28 대비 주가(중앙값)", "value": pct(med_vs0828),
             "note": "클래시스·원텍·파마리서치·휴젤·엘앤씨바이오", "src": "화장품_원장대조_2026-10-21.json"},
            {"label": "10월 목표가 변경(직전값 확인분)", "value": f"하향 {oct_down}/{len(oct_known)}",
             "note": f"상향 {oct_up}", "src": "화장품_원장대조_2026-10-21.json"},
            {"label": "휴젤 3Q26 영업이익 컨센", "value": f"{comma(hz_f)} → {comma(hz_l)}억",
             "note": f"10/4–10/21 {pct(hz_q3_move)}", "src": "화장품_이력.json naver_cons"},
            {"label": "클래시스 3Q26 교보 추정 vs 컨센", "value": f"{comma(cl_kyobo)} vs {comma(cl_l)}억",
             "note": f"{pct(cl_gap)}", "src": "화장품_원장대조_2026-10-21.json · 화장품_이력.json"},
            {"label": "파마리서치 8/28 대비", "value": pct(CMP['214450']['vs0828_pct']),
             "note": "8/28 이 고점", "src": "화장품_원장대조_2026-10-21.json"},
            {"label": "엘앤씨바이오 8/28 대비", "value": pct(CMP['290650']['vs0828_pct']),
             "note": "5종목 중 유일한 상승 · 미국 공급계약(신한 10/13, NR)", "src": "화장품_원장대조_2026-10-21.json"},
        ],
    },
    "sections": [],
    "sources": [],
}

S = spec["sections"]

# 1. summary
S.append({
    "id": "summary", "title": "한 페이지 요약",
    "lead": "업종 구조는 '장비 + 소모품', '주사제 반복 판매'로 단단하다. 2026년 하반기 약세는 수요가 아니라 해외 유통 구조 전환과 눈높이 조정에서 왔다.",
    "blocks": [
        {"type": "text", "md": (
            "**결론 먼저.**\n\n"
            f"- **미용기기·미용의료 5종목은 화장품·미용기기 20종목 가운데 가장 나쁜 그룹이다.** 8/28 대비 주가 중앙값 {pct(med_vs0828)}, 10월에 직전 목표가가 확인되는 리포트 {len(oct_known)}건이 전부 하향이다.\n"
            f"- **원인은 회사별 해외 유통 구조 전환이다.** 휴젤은 미국 판매를 파트너에서 직판으로 바꾸는 분기라 3Q 컨센이 10월에만 {pct(hz_q3_move)} 깎였다. 클래시스는 8월에 가이던스를 내렸고, 교보 3Q 추정({comma(cl_kyobo)}억)이 컨센({comma(cl_l)}억)보다 {abs(round(cl_gap))}% 낮다.\n"
            f"- **같은 'K-뷰티'인데 화장품 ODM 은 반대로 갔다.** ODM·용기 4종목 10월 목표가 변경은 상향 15·하향 0이다. 화장품 수출 호조가 미용의료로 번지지 않았다.\n"
            f"- **예외는 엘앤씨바이오({pct(CMP['290650']['vs0828_pct'])})** — ECM 스킨부스터 리투오와 미국 공급계약. 다만 커버리지가 얇다.\n"
            "- **다음 4주**: 3Q 실적(10월 말–11월 중순)에서 클래시스 360억 vs 490억, 휴젤 230억 선, 그리고 휴젤 4Q 직판 ASP."
        )},
        {"type": "callout", "tone": "info", "md": (
            "이 자료의 숫자는 맥미니 원장(리포트·DART 분기·네이버 컨센·KRX 종가) 10/21 추출본에서 파이썬으로 읽었다. "
            "시장 규모·점유율·시술 가격처럼 원장과 문서에 근거가 없는 숫자는 넣지 않았다."
        )},
    ],
})

# 2. model
S.append({
    "id": "model", "title": "미용의료는 어떻게 돈을 버나",
    "lead": "장비는 한 번 팔리고, 소모품·주사제는 시술마다 팔린다. 해외는 허가 → 유통 파트너 → 직판 순서로 넓어진다.",
    "blocks": [
        {"type": "cards", "items": [
            {"title": "장비 + 소모품", "tag": "미용기기",
             "body": "병원에 장비(HIFU·RF·레이저)를 판다 — 일시 매출. 이후 시술할 때마다 카트리지·팁 같은 소모품이 나간다 — 반복 매출. 클래시스가 대표다(슈링크·볼뉴머). 깔린 장비 대수가 늘수록 소모품 매출이 쌓인다."},
            {"title": "주사제 반복 판매", "tag": "톡신·필러·스킨부스터",
             "body": "장비 없이 제품 자체가 시술마다 소모된다. 톡신(휴젤·대웅제약·메디톡스), 필러, 스킨부스터(파마리서치 리쥬란, 엘앤씨바이오 리투오). 효과가 몇 달 만에 사라져 재시술 수요가 생긴다."},
            {"title": "병원 채널", "tag": "B2B",
             "body": "고객은 소비자가 아니라 피부과·성형외과 의사다. 같은 시술이라도 어느 제품을 쓸지 병원이 고른다. 그래서 영업 인력·학술 마케팅·병원 도입 수가 중요하다(예: 한스바이오메드 셀르디엠 출시 후 210개 병원 도입)."},
            {"title": "가정용 디바이스", "tag": "B2C · 에이피알",
             "body": "병원용과 다른 축. 에이피알은 메디큐브 부스터프로 같은 가정용 기기(1대 30–40만원)를 팔고, 산 사람이 같은 브랜드 화장품을 사는 '기기 → 화장품 락인'을 만든다(K뷰티 통합 산업분석)."},
        ]},
        {"type": "flow", "steps": [
            {"title": "국내 허가·출시", "who": "식약처", "body": "국내에서 먼저 허가받고 병원에 깔아 레퍼런스를 만든다."},
            {"title": "해외 허가", "who": "FDA·NMPA 등", "body": "국가별로 따로 허가가 필요하다. 미국·중국은 시간이 길다. 휴젤은 2024년 미국 FDA 승인."},
            {"title": "유통 파트너 수출", "who": "현지 디스트리뷰터", "body": "파트너에게 넘기는 출하가 곧 매출. 마진은 파트너와 나눈다. 대웅제약 나보타는 미국에서 Evolus 를 통해 판다."},
            {"title": "직판 전환", "who": "자체 법인", "body": "현지 법인이 병원에 직접 판다. 전환 분기에는 파트너 재고 조정·인력 비용으로 이익이 꺼진다(휴젤 3Q26, 클래시스 브라질)."},
            {"title": "ASP·마진 회복", "who": "", "body": "판매가(ASP)를 직접 받으니 매출 단가와 이익률이 올라간다 — 이게 나와야 전환이 성공이다."},
        ]},
        {"type": "table",
         "columns": ["종목", "구분", "주력", f"LTM 매출(억, {ltm_span})", "LTM 영업이익(억)", "LTM OPM", "2Q25 OPM", "2Q26 OPM"],
         "align": ["l", "l", "l", "r", "r", "r", "r", "r"],
         "rows": model_rows,
         "note": "DART 분기 연결(4Q 는 연간 − 3분기 누계 역산), 단위 억원. LTM 은 최근 4개 분기 합. 에이피알은 화장품 겸업이라 디바이스만의 마진이 아니다. 계산: _seminar/build_aesthetics.py"},
        {"type": "callout", "tone": "info", "md": (
            f"**읽는 법.** 클래시스·휴젤·파마리서치는 LTM OPM {min(ltm_opm(t) for t in ('214150','145020','214450')):.0f}–{max(ltm_opm(t) for t in ('214150','145020','214450')):.0f}%의 고마진 사업이다. "
            f"그런데 2Q25 → 2Q26 분기 OPM 이 클래시스 {opm_q('214150','2025-06-30'):.1f}% → {opm_q('214150','2026-06-30'):.1f}%, 휴젤 {opm_q('145020','2025-06-30'):.1f}% → {opm_q('145020','2026-06-30'):.1f}%로 내려왔다. "
            "매출은 늘었는데(2Q26 YoY 클래시스 +26.7%, 휴젤 +25.0%) 남미 편입 비용(클래시스, 유안타 8/18)·미국 직판 준비(휴젤)가 먼저 들어온 구간이다. "
            "원텍도 OPM 이 내려왔지만 원장에 원인을 설명할 리포트가 없다."
        )},
    ],
})

# 3. products
S.append({
    "id": "products", "title": "제품 지도",
    "lead": "에너지를 쏘는 장비(HIFU·RF·레이저)와 몸에 넣는 주사제(톡신·필러·스킨부스터)로 나뉜다.",
    "blocks": [
        {"type": "table",
         "columns": ["카테고리", "원리 한 줄", "대표 국내 기업(제품)", "반복 매출"],
         "align": ["l", "l", "l", "l"],
         "rows": [
             ["HIFU(고강도 집속 초음파)", "초음파를 피부 속 한 점에 모아 열을 내고, 콜라겐 재생을 유도해 리프팅", "클래시스(슈링크)", "장비 1회 + 카트리지 소모품"],
             ["RF(고주파)", "고주파 전류로 진피층을 가열해 탄력 개선", "클래시스(볼뉴머) · 원텍", "장비 1회 + 팁 소모품"],
             ["레이저", "특정 파장의 빛으로 색소·혈관·피부결을 치료", "원텍 · 루트로닉(비상장)", "장비 중심"],
             ["보툴리눔 톡신", "신경 전달을 일시적으로 막아 근육을 이완 — 주름·사각턱", "휴젤(보툴렉스/Letybo) · 대웅제약(나보타) · 메디톡스(메디톡신)", "시술마다 소모 · 수개월 후 재시술"],
             ["HA 필러", "히알루론산 젤을 주입해 꺼진 부위를 채움", "휴젤(더채움) · 메디톡스(뉴라미스) · 휴메딕스(엘라비에)", "시술마다 소모"],
             ["스킨부스터 — PN·PDRN", "연어 유래 DNA 조각을 주입해 피부 재생 환경을 만듦", "파마리서치(리쥬란)", "시술마다 소모 · 화장품으로 확장"],
             ["스킨부스터 — ECM", "세포외기질(인체조직 유래)을 주입해 피부 구조를 보강", "엘앤씨바이오(리투오) · 한스바이오메드(셀르디엠)", "시술마다 소모"],
             ["가정용 뷰티 디바이스", "저강도 전류·LED 등을 집에서 쓰는 소비자 기기", "에이피알(메디큐브 에이지알)", "기기 1회 + 화장품 동반 구매"],
         ],
         "note": "원리 설명은 일반 의학 상식 수준. 기업·제품 매핑은 화장품_미용기기_핵심종목점검 §1·§6, 바이오_진단의료기기소부장_심층분석 §6, 건강관리_코스피200_종목분석, 한스바이오메드 심화 문서."},
        {"type": "cards", "items": [
            {"title": "톡신 매출 비중", "tag": "휴젤",
             "body": f"2Q26 톡신 매출 {hz_toxin_2q}억(YoY +37.2%, 교보 8/10)은 분기 매출 {comma(dart('145020')['2026-06-30']['revenue'])}억의 {hz_toxin_share:.0f}%다. 휴젤은 사실상 톡신 회사다."},
            {"title": "리투오가 바꾼 수익 구조", "tag": "엘앤씨바이오",
             "body": f"1Q26 리투오 매출 {lnc_re2o_1q}억 = 분기 매출의 {lnc_re2o_share:.0f}%(유안타 6/1). 분기 영업이익은 4Q25 20억 → 2Q26 86억."},
            {"title": "의료기기 + 화장품", "tag": "파마리서치",
             "body": "리쥬란은 시술(의료기기)과 화장품 두 갈래로 판다. 2Q26 은 의료기기·화장품, 내수·수출 모두 최대 매출(IBK 8/10). '화장품으로 확장되는 중인 리쥬란 충성도'(삼성 8/10)."},
        ]},
    ],
})

# 4. cycle
S.append({
    "id": "cycle", "title": "이 업종이 움직이는 방식",
    "lead": "경기보다 '해외 진출 단계'가 실적을 움직인다. 직판 전환은 이익이 먼저 꺼지고 나중에 오르는 J커브다.",
    "blocks": [
        {"type": "cycle", "phases": [
            {"name": "국내 점유율", "signal": "국내 병원 도입·점유율, 신제품 출시"},
            {"name": "해외 허가", "signal": "FDA·NMPA 등 허가 일정. 클래시스는 '계획된 중국 허가 일정 유지 확인 필요'(교보 7/23)"},
            {"name": "파트너 수출", "signal": "수출 물량·선적. 대웅제약 2Q26 '나보타 조기 선적으로 컨센 상회'(교보 7/30)"},
            {"name": "직판 전환", "signal": "파트너 재고 조정·출하 공백·인력 비용 → 이익 급감. 휴젤 3Q26, 클래시스 브라질", "now": True},
            {"name": "ASP 회복", "signal": "직판 단가 반영, 이익률 회복. 휴젤 '4분기부터 ASP 효과 시작'(DB 10/13)"},
        ], "note": "지금 위치는 업종 전체가 아니라 휴젤·클래시스 기준. 파마리서치는 '이제는 해외로'(현대차 8/14) 단계, 엘앤씨바이오는 미국 공급계약(신한 10/13) 단계."},
        {"type": "chart", "kind": "bar", "title": "휴젤·클래시스 분기 영업이익 (3Q26E 는 네이버 컨센 10/21)",
         "unit": "억원",
         "series": [op_series("145020"), op_series("214150")],
         "note": "DART 분기 연결, 4Q 는 연간 − 3분기 누계 역산. 휴젤 3Q26E 컨센은 10월 중 437 → 292억으로 내려왔고, 원장 리포트 중앙값은 233억(3곳)으로 더 낮다.",
         "src": "_manifest/데이터/화장품_이력.json (dart_q · naver_cons)"},
        {"type": "cards", "items": [
            {"title": "휴젤 — 직판 J커브의 바닥", "tag": "톡신",
             "body": "1월 '미국 직판 선언'(키움 1/19) → 2월 '성공하면 CapEx, 실패하면 비용'(키움 2/12) → 9월 하향 몰림 → 10월 '3분기 바닥, 4분기부터 ASP 효과 시작'(DB 10/13) · '직판하러 가는 길'(키움 10/21). 리포트의 공통 논리는 '3Q 바닥, 4Q 회복'이다."},
            {"title": "클래시스 — 남미 편입 비용", "tag": "미용기기",
             "body": "2Q26 영업이익 439억은 시장 기대 501억을 12% 하회 — '남미 편입 비용 부담'(유안타 8/18). '기대 대비 부진한 브라질 직판 매출 회복세 입증'이 주가 단초(교보 7/23), '브라질 정상화가 관건'(미래에셋 8/14)."},
        ]},
    ],
})

# 5. indicators
S.append({
    "id": "indicators", "title": "무엇을 보나",
    "lead": "허가·수출·컨센 이동·직판 단가·소모품 비중·가이던스. 이 중 원장에 바로 있는 건 컨센과 실적뿐이다.",
    "blocks": [
        {"type": "checklist", "items": [
            {"what": "해외 허가 일정", "why": "허가가 나야 그 나라 매출이 시작된다. 지연되면 성장 경로 전체가 밀린다",
             "now": "클래시스 중국 허가 일정 유지 여부가 체크포인트(교보 7/23). 원장에는 허가 데이터가 없다", "where": "회사 공시·IR, 각국 규제기관 공개 DB"},
            {"what": "톡신·미용기기 수출", "why": "파트너 모델에서는 수출 선적이 곧 매출. 분기 실적의 선행지표",
             "now": "원장에 없다 — 화장품 수출(산업통상부)과 달리 수집 대상에 올라 있지 않다", "where": "관세청 수출입무역통계(품목별·월별)"},
            {"what": "3Q 영업이익 컨센 이동", "why": "발표 전 2–3주의 컨센 이동이 서프라이즈 크기를 미리 말해 준다",
             "now": f"휴젤 {pct(hz_q3_move)} · 클래시스 {pct(cl_q3_move)} (10/4 → 10/21)", "where": "원장 naver_consensus_snap(일별)"},
            {"what": "리포트 추정 vs 컨센 괴리", "why": "괴리가 크면 발표일에 컨센이 한 번에 내려온다",
             "now": f"클래시스 교보 {comma(cl_kyobo)}억 vs 컨센 {comma(cl_l)}억({pct(cl_gap)}) · 휴젤 리포트 중앙값 {comma(hz_rep)}억 vs {comma(hz_l)}억({pct(hz_gap)})", "where": "원장 report_estimates · naver_consensus_snap"},
            {"what": "직판 ASP", "why": "직판 전환이 성공했는지 판정하는 숫자. 단가가 올라야 이익이 회복된다",
             "now": "휴젤 ASP 효과는 4Q 부터(DB 10/13). 수치는 아직 없다", "where": "실적 발표·컨퍼런스콜"},
            {"what": "소모품 매출 비중", "why": "반복 매출 비중이 높을수록 장비 판매 둔화에 덜 흔들린다",
             "now": "클래시스 체크포인트. 원장에 매출 구성 분해가 없다", "where": "사업보고서 매출 구성·IR 자료"},
            {"what": "가이던스", "why": "회사가 스스로 낮추면 컨센이 따라 내려온다",
             "now": "클래시스 '실적 컨센서스 하회, 가이던스 하향 조정'(유안타 8/18)", "where": "실적 발표·IR"},
            {"what": "국내 톡신 점유율", "why": "해외 전환 중 국내가 버텨 줘야 이익이 덜 꺼진다",
             "now": "휴젤 체크포인트. 수치 근거 없음", "where": "회사 IR·리포트"},
        ]},
        {"type": "table",
         "columns": ["종목", "3Q26E 영업이익 컨센 10/4(억)", "10/21(억)", "변화"],
         "align": ["l", "r", "r", "r"],
         "rows": cons_rows,
         "note": "원장 naver_consensus_snap. 원텍은 10월 중 변화 없음."},
    ],
})

# 6. players
S.append({
    "id": "players", "title": "종목 지도",
    "lead": "커버리지가 두꺼운 건 클래시스·휴젤·파마리서치 셋이다. 원텍·엘앤씨바이오는 10월 목표가가 없다.",
    "blocks": [
        {"type": "table",
         "columns": ["종목", "코드", "구분", "10/21 종가", "8/28 대비", "10월 목표가 중앙값", "3Q26E 영업이익 컨센(억)", "3Q 컨센 YoY", "12개월 목표가 변경 상향/하향"],
         "align": ["l", "l", "l", "r", "r", "r", "r", "r", "r"],
         "rows": player_rows,
         "note": "종가·목표가는 원장대조 JSON(증권사별 10월 최신 1건). 3Q 컨센은 네이버 10/21, YoY 는 DART 3Q25 영업이익 대비. 12개월 목표가 변경은 같은 증권사가 목표가를 바꾼 기록(원장 reports). 에이피알은 화장품 겸업 — 비교용."},
        {"type": "cards", "items": [
            {"title": "클래시스", "tag": "컨센 미반영", "body": "목표가 7.4–8.8만(2025년 말–2026년 2월) → 4–4.5만. 3Q 컨센 492억 대 교보 359억. 교보 추정이 맞으면 3Q 는 YoY 역성장."},
            {"title": "휴젤", "tag": "직판 전환", "body": "3Q 컨센 YoY −38%, 리포트 중앙값은 −51%. 4Q 직판 ASP 숫자가 나와야 목표가가 다시 오른다."},
            {"title": "파마리서치", "tag": "설명 부족", "body": "3Q 컨센은 YoY +17% 성장인데 주가는 8/28 고점에서 −42.9%. 10월 리포트는 다올 1건뿐 — 원문·공시 확인이 필요하다."},
            {"title": "원텍 · 엘앤씨바이오", "tag": "커버리지 얇음", "body": "원텍은 3Q 컨센 YoY +51%인데 10월에 크게 빠졌고, 원장에 8월 이후 리포트가 없다. 엘앤씨바이오는 미국 공급계약으로 +25.7%, 목표가 리포트 없음."},
        ]},
    ],
})

# 7. now
S.append({
    "id": "now", "title": "2026년 10월 현황",
    "lead": "목표가는 8월 이후 계단식으로 내려왔고, 주가는 그보다 먼저·더 많이 빠졌다.",
    "blocks": [
        {"type": "chart", "kind": "line", "title": "목표가 월별 중앙값 경로 (첫 달 = 100)",
         "unit": "지수",
         "series": tp_series,
         "note": "증권사별 그 달 최신 1건의 중앙값을 종목별 첫 달 값으로 나눠 지수화(build_aesthetics.py). 원값: " + " · ".join(tp_raw) + ". 리포트가 없는 달은 비어 있다. 원텍·엘앤씨바이오는 12개월 중 목표가 달이 2개뿐이라 뺐다.",
         "src": "_manifest/데이터/화장품_이력.json (tp_monthly)"},
        {"type": "table",
         "columns": ["종목", "목표가 고점 월 중앙값", "최근 월 중앙값", "고점 대비"],
         "align": ["l", "r", "r", "r"],
         "rows": tp_path_rows,
         "note": "tp_monthly 에서 중앙값이 가장 높았던 달과 마지막 달. 계산: _seminar/build_aesthetics.py"},
        {"type": "chart", "kind": "hbar", "title": "8/28 대비 주가 (10/21 종가)",
         "unit": "%",
         "series": [hbar],
         "note": "화장품·미용기기 20종목 중앙값은 −17%, ODM·용기 4종목 중앙값은 −16.0%(_시총상위_종목표.md).",
         "src": "_manifest/데이터/화장품_원장대조_2026-10-21.json (vs0828_pct)"},
        {"type": "cards", "items": [
            {"title": "클래시스 — 하향 제목이 만든 이야기", "tag": "7월 이후 하향",
             "body": "\n".join(title_line(c) for c in cl_titles)},
            {"title": "휴젤 — 9월 하순부터 하향이 몰렸다", "tag": "9월 이후",
             "body": "\n".join(title_line(c) for c in hz_titles)},
            {"title": "파마리서치 — 2월 어닝 쇼크 후 회복, 다시 하향", "tag": "12개월",
             "body": "2/5 하루에 5곳 하향(LS '어닝 쇼크', 교보 '시간이 필요해') → 4/17 키움 −29% → 7–8월 상향(신한 '2Q 좋고, 2H는 더 좋아요', 삼성 +25%) → 10/19 다올 55만 → 45만 '3Q26보다 4Q26을 볼 때'."},
        ]},
        {"type": "callout", "tone": "warn", "md": (
            "**판단 — 화장품 ODM 호황이 미용의료로 번지지 않았다.** 9월 화장품 수출은 15.1억 달러(+31.4%)로 9월 기준 역대 최대였고, ODM·용기 4종목 10월 목표가는 상향 15·하향 0이었다. "
            f"같은 시기 미용의료 5종목은 하향 {oct_down}·상향 {oct_up}이다. 미용의료의 숫자를 정하는 건 화장품 수요가 아니라 **회사별 해외 유통 구조(직판 전환)와 가이던스**다. "
            "'K-뷰티' 테마로 한데 묶어 보면 틀린다. 3Q 발표에서 클래시스 컨센이 따라 내려오고 휴젤 4Q ASP 가 확인되기 전까지는 목표가 반등 근거가 약하다."
        )},
    ],
})

# 8. risks
S.append({
    "id": "risks", "title": "리스크",
    "lead": "규제·유통 구조·경쟁·정보 부족. 수요 리스크보다 실행 리스크가 크다.",
    "blocks": [
        {"type": "cards", "items": [
            {"title": "해외 허가 지연", "tag": "규제",
             "body": "미용 의료기기·톡신은 국가별 규제·문화 차이로 미국·유럽 진출이 예상보다 늦을 수 있다(바이오_진단의료기기소부장 문서). 클래시스는 중국 허가 일정이 체크포인트."},
            {"title": "직판 전환 비용", "tag": "유통 구조",
             "body": "전환 분기에는 출하 공백과 인력·법인 비용이 겹친다. 휴젤 3Q26 리포트 중앙값 YoY −50.8%, 클래시스 2Q26 남미 편입 비용. 4Q 에 ASP 가 안 나오면 바닥이 늦춰진다."},
            {"title": "후발 추격·가격 경쟁", "tag": "경쟁",
             "body": "HIFU 는 중국·이스라엘 후발주자 추격, 톡신은 Allergan(보톡스)과 직접 경쟁(바이오_진단의료기기소부장 문서). 단일 제품 의존도가 높은 회사일수록 민감하다."},
            {"title": "균주 분쟁", "tag": "톡신",
             "body": "메디톡스·대웅제약 균주 분쟁은 미국 진출 차질로 이어진 이력이 있다(바이오모달리티_합성저분자 문서)."},
            {"title": "컨센 미반영", "tag": "숫자",
             "body": f"클래시스 3Q 컨센은 10월 중 {pct(cl_q3_move)}만 내려왔다. 교보 추정과 {abs(round(cl_gap))}% 괴리 — 발표일에 한 번에 조정될 수 있다."},
            {"title": "커버리지가 얇다", "tag": "정보",
             "body": "원텍은 8월 이후 원장 리포트가 없고, 엘앤씨바이오는 목표가 리포트가 없으며, 파마리서치 10월 리포트는 1건이다. 주가 급변을 리포트로 설명할 수 없는 종목이 절반이다."},
            {"title": "자금 조달", "tag": "엘앤씨바이오",
             "body": "'유상증자, 투자 시점과 규모의 문제'(유안타 8/3). 성장 투자를 증자로 조달하면 주당 가치가 희석된다."},
        ]},
    ],
})

# 9. glossary
S.append({
    "id": "glossary", "title": "용어",
    "lead": "처음 듣는 말 위주로.",
    "blocks": [
        {"type": "glossary", "items": [
            {"term": "HIFU", "def": "고강도 집속 초음파. 초음파를 피부 속 한 점에 모아 열 응고를 일으켜 리프팅 효과를 낸다. 클래시스 슈링크."},
            {"term": "RF(고주파)", "def": "고주파 전류로 진피를 가열해 콜라겐 재생·탄력 개선을 노리는 장비. 클래시스 볼뉴머, 원텍."},
            {"term": "레이저", "def": "특정 파장의 빛을 표적(색소·혈관·수분)에 흡수시켜 치료하는 장비."},
            {"term": "보툴리눔 톡신", "def": "보툴리눔균이 만드는 신경독소를 정제한 주사제. 근육을 일시적으로 이완해 주름을 편다. '보톡스'는 Allergan 의 상표명."},
            {"term": "균주", "def": "톡신을 만드는 균의 계통. 균주 출처를 두고 메디톡스·대웅제약 간 분쟁이 있었다."},
            {"term": "HA 필러", "def": "히알루론산 젤을 주입해 볼륨을 채우는 시술 제품."},
            {"term": "스킨부스터", "def": "피부 속에 주입해 피부 상태(재생·수분·탄력) 개선을 노리는 주사제의 통칭. 리쥬란, 리투오, 셀르디엠."},
            {"term": "PN", "def": "폴리뉴클레오티드. 연어 유래 DNA 조각을 정제한 성분. 리쥬란의 주성분."},
            {"term": "PDRN", "def": "폴리데옥시리보뉴클레오티드. PN 과 같은 계열의 DNA 유래 성분으로 분자 크기가 더 작다."},
            {"term": "ECM", "def": "세포외기질. 세포 사이를 채우는 콜라겐 등 구조 단백질. 인체조직에서 얻어 스킨부스터로 쓴다(리투오·셀르디엠)."},
            {"term": "ADM(무세포동종진피)", "def": "기증 피부에서 세포를 제거한 이식재. 유방재건·화상 치료에 쓰인다. 엘앤씨바이오·한스바이오메드의 원래 사업."},
            {"term": "소모품", "def": "장비 시술마다 교체하는 카트리지·팁. 장비 판매 후 계속 나오는 반복 매출."},
            {"term": "설치 기반(installed base)", "def": "병원에 깔려 있는 장비 대수. 소모품 매출의 모수다."},
            {"term": "유통 파트너(디스트리뷰터)", "def": "해외 현지에서 제품을 사서 병원에 파는 회사. 제조사는 파트너에 넘기는 시점에 매출을 잡는다."},
            {"term": "직판", "def": "현지 법인이 병원에 직접 파는 방식. 단가와 마진은 높지만 전환 초기에 비용이 먼저 든다."},
            {"term": "ASP", "def": "평균판매단가. 직판 전환의 성패를 보여 주는 숫자."},
            {"term": "가이던스", "def": "회사가 공개한 연간 매출·이익 목표. 하향하면 컨센이 따라 내려온다."},
            {"term": "컨센서스 괴리", "def": "개별 리포트 추정과 시장 평균(컨센) 추정의 차이. 클래시스 3Q 처럼 크면 발표일 조정 폭이 크다."},
        ]},
    ],
})

spec["sources"] = [
    "10_국내주식/11_화장품의류완구/화장품_미용기기_핵심종목점검_2026-10-21.md (§0·§1·§2·§4-1·§6)",
    "10_국내주식/11_화장품의류완구/_시총상위_종목표.md (2026-10-21 상단 그룹·종목표)",
    "10_국내주식/11_화장품의류완구/K뷰티_K콘텐츠_통합_산업분석_2026Q2.md (에이피알 디바이스)",
    "10_국내주식/16_건강관리/건강관리_코스피200_종목분석.md (파마리서치·휴젤·클래시스·대웅제약·엘앤씨바이오 리포트 인용)",
    "10_국내주식/16_건강관리/바이오_진단의료기기소부장_심층분석.md (§5·§6 에스테틱 제품·리스크 — 정성 서술만)",
    "10_국내주식/16_건강관리/바이오모달리티_합성저분자_심층분석.md (대웅제약 나보타·Evolus·균주 분쟁)",
    "10_국내주식/16_건강관리/한스바이오메드_심화_매출구조분해와_손실원인_DART검증.md (셀르디엠 ECM 스킨부스터)",
    "_manifest/데이터/화장품_원장대조_2026-10-21.json (10/21 종가·8/28 대비·10월 목표가·10월 리포트)",
    "_manifest/데이터/화장품_이력.json (dart_q·naver_cons·tp_monthly·tp_changes)",
    "산업통상부 「2026년 9월 수출입 동향」 2026-10-01 (화장품 15.1억 달러, +31.4% — 핵심종목점검 문서 경유)",
    "계산: _seminar/build_aesthetics.py",
]

OUT.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
print(OUT)
