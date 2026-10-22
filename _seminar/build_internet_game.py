"""인터넷·게임 기초세미나 스펙 생성기 → _seminar/internet_game.json

숫자는 전부 _manifest/데이터 의 원장 추출 JSON 에서 읽는다. 문장 속 숫자는
10_국내주식/20_소프트웨어/인터넷게임_핵심종목점검_2026-10-21.md 등 문서에 적힌 값을 옮겼다.
계산(OPM, YoY, 중앙값, 원장 추정 대 컨센 괴리, 목표가 지수화)은 이 파일에서만 한다.
"""
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "_manifest" / "데이터"
LEDGER = json.loads((D / "인터넷게임_원장대조_2026-10-21.json").read_text())
HIST = json.loads((D / "인터넷게임_이력.json").read_text())
PX = json.loads((D / "인터넷게임_2026-10-21.json").read_text())["데이터"]

ORDER = ["181710", "035420", "035720", "259960", "036570", "251270", "462870", "263750"]
NAME = {c: LEDGER[c]["name"] for c in ORDER}
MINUS = "−"


def won(x):
    return f"{int(round(x)):,}"


def pct(x, nd=1):
    s = f"{abs(x):.{nd}f}%"
    return ("+" if x > 0 else MINUS if x < 0 else "") + s


def q_label(date):  # '2025-09-30' -> '3Q25'
    y, m, _ = date.split("-")
    return f"{(int(m) - 1) // 3 + 1}Q{y[2:]}"


# ── 계산 ──────────────────────────────────────────────
cons_q3 = {c: HIST[c]["naver_cons"]["2026Q3E|op_income"]["last"][1] for c in ORDER}
cons_q3_first = {c: HIST[c]["naver_cons"]["2026Q3E|op_income"]["first"][1] for c in ORDER}
dart_q3_25 = {c: HIST[c]["dart_q"]["2025-09-30|op_income"] for c in ORDER}


def cons_yoy(c):
    base = dart_q3_25[c]
    if base <= 0:
        return None  # 흑자 전환
    return (cons_q3[c] / base - 1) * 100


yoy = {c: cons_yoy(c) for c in ORDER}
n_yoy_down = sum(1 for c in ORDER if yoy[c] is not None and yoy[c] < 0)
cons_move = {c: (cons_q3[c] / cons_q3_first[c] - 1) * 100 for c in ORDER}
est_vs_cons = {c: (LEDGER[c]["q3_med"] / cons_q3[c] - 1) * 100 for c in ORDER}

med_vs0828 = statistics.median(LEDGER[c]["vs0828_pct"] for c in ORDER)
n_up = sum(LEDGER[c]["n_up"] for c in ORDER)
n_down = sum(LEDGER[c]["n_down"] for c in ORDER)
n_flat = sum(LEDGER[c]["n_flat"] for c in ORDER)

tpm = {c: {r["m"]: r["med"] for r in HIST[c]["tp_monthly"]} for c in ORDER}
nhn_tp_first_m = HIST["181710"]["tp_monthly"][0]["m"]
nhn_tp_first = HIST["181710"]["tp_monthly"][0]["med"]
nhn_tp_last = HIST["181710"]["tp_monthly"][-1]["med"]


def tp_counts(c):
    ch = HIST[c]["tp_changes"]
    return len(ch), sum(1 for t in ch if (t["pct"] or 0) > 0), sum(1 for t in ch if (t["pct"] or 0) < 0)


def opm_series(c):
    dq = HIST[c]["dart_q"]
    dates = sorted({k.split("|")[0] for k in dq})
    out = []
    for dt in dates:
        r, o = dq.get(f"{dt}|revenue"), dq.get(f"{dt}|op_income")
        if r and o is not None:
            out.append([q_label(dt), round(o / r * 100, 1)])
    return out


naver_opm = opm_series("035420")
kakao_opm = opm_series("035720")
naver_q3e_opm = round(cons_q3["035420"] / HIST["035420"]["naver_cons"]["2026Q3E|revenue"]["last"][1] * 100, 1)
kakao_q3e_opm = round(cons_q3["035720"] / HIST["035720"]["naver_cons"]["2026Q3E|revenue"]["last"][1] * 100, 1)
naver_opm_e = naver_opm + [["3Q26E", naver_q3e_opm]]
kakao_opm_e = kakao_opm + [["3Q26E", kakao_q3e_opm]]

# 목표가 경로: NHN·카카오·NC, 세 종목 모두 값이 있는 첫 달(2025-11)=100
TP3 = ["181710", "035720", "036570"]
base_m = "2025-11"
months = sorted(set().union(*[tpm[c].keys() for c in TP3]))
tp_series = []
for c in TP3:
    b = tpm[c][base_m]
    tp_series.append({"name": NAME[c], "data": [[m[2:].replace("-", "/"), round(tpm[c][m] / b * 100, 1)] for m in months if m in tpm[c] and m >= base_m]})

# 펄어비스 분기 영업이익(출시 분기 집중 예시)
pa = HIST["263750"]["dart_q"]
pa_q = [[q_label(d), pa[f"{d}|op_income"]] for d in ["2025-09-30", "2025-12-31", "2026-03-31", "2026-06-30"]]
pa_q.append(["3Q26E", cons_q3["263750"]])

# ── 표: 종목 지도 ──────────────────────────────────
GROUP = {"035420": "인터넷", "035720": "인터넷", "181710": "인터넷+클라우드",
         "259960": "게임", "036570": "게임", "251270": "게임", "462870": "게임", "263750": "게임"}
ROLE = {
    "181710": "업종 핵심주. 게임·결제(KCP)·클라우드(GPUaaS)의 합. 12개월 목표가 변경 17건 전부 상향",
    "035420": "검색·커머스·핀테크. 매출은 YoY +12–16% 성장, 이익은 AI·커머스 비용에 눌림",
    "035720": "카카오톡 광고(톡비즈)·커머스. 이익은 늘지만 AI 실행 증명 전까지 배수 하향",
    "259960": "PUBG 단일 IP. 1H26 정점 뒤 신작 공백, 매수 근거는 2027 신작·PUBG 10주년",
    "036570": "아이온2·아이온2 글로벌. 이익과 목표가가 같이 버틴 유일한 게임주",
    "251270": "퍼블리싱 구조(로열티가 원가). 신작 출시일 확정 전까지 하향",
    "462870": "니케·스텔라블레이드. 2025 출시작 효과 소멸, Spirits 공개 대기",
    "263750": "붉은사막(1Q26 출시) 뒤 이익 하강. 10월 리포트 1곳뿐",
}
rows = []
for c in ["035420", "035720", "181710", "259960", "036570", "251270", "462870", "263750"]:
    L = LEDGER[c]
    lo, hi = L["tp_rng"]
    tp = f"{won(L['tp_med'])} ({L['n']}곳)" if L["n"] > 1 else f"{won(L['tp_med'])} (1곳)"
    y = yoy[c]
    rows.append([GROUP[c], f"{NAME[c]} ({c})", won(L["close_1021"]), tp,
                 "흑자 전환" if y is None else pct(y), pct(L["vs0828_pct"]), ROLE[c]])

players_table = {
    "type": "table",
    "columns": ["구분", "종목", "10/21 종가", "10월 목표가 중앙값", "3Q 컨센 영업이익 YoY", "8/28 대비 주가", "역할 한 줄"],
    "align": ["l", "l", "r", "r", "r", "r", "l"],
    "rows": rows,
    "note": "종가 KRX 10/21. 목표가는 원장 reports 10월분, 증권사별 최신 1건 중앙값(인터넷게임_원장대조_2026-10-21.json). "
            "3Q 컨센 YoY = 네이버 컨센 10/21 스냅 ÷ DART 3Q25 영업이익 − 1(NC 3Q25 −75억이라 YoY 대신 흑자 전환). "
            "펄어비스 목표가는 메리츠 1곳(8월 리포트는 3만–5만)이라 상방 계산에 쓰지 않는다.",
}

tp_change_rows = []
for c in ORDER:
    n, u, dn = tp_counts(c)
    first = HIST[c]["tp_monthly"][0]
    last = HIST[c]["tp_monthly"][-1]
    tp_change_rows.append([NAME[c], str(n), str(u), str(dn),
                           f"{won(first['med'])} ({first['m']})", f"{won(last['med'])} ({last['m']})"])

# ── 스펙 ──────────────────────────────────────────
spec = {
    "slug": "internet_game",
    "title": "인터넷·게임 기초세미나",
    "subtitle": "광고·커머스로 버는 인터넷, 신작으로 버는 게임, 그리고 GPU 를 빌려주는 NHN",
    "asof": "2026-10-21",
    "audience": "인터넷·게임 업종을 처음 맡는 애널리스트·운용역",
    "hero": {
        "one_liner": "인터넷은 AI 비용이 이익을 누르는 해, 게임은 신작이 나온 곳만 숫자가 있는 해다. 업종에서 목표가가 오른 곳은 GPU 를 빌려주는 NHN 과 신작이 이미 나온 NC 뿐이다.",
        "kpis": [
            {"label": "NHN 목표가 중앙값", "value": f"{won(nhn_tp_first)} → {won(nhn_tp_last)}원",
             "note": f"{nhn_tp_first_m} → 2026-10, 12개월 변경 {tp_counts('181710')[0]}건 전부 상향",
             "src": "원장 tp_monthly (인터넷게임_이력.json)"},
            {"label": "대표 8종목 주가 8/28 대비 중앙값", "value": pct(med_vs0828),
             "note": "KOSPI 같은 기간 −15.5%", "src": "인터넷게임_원장대조_2026-10-21.json · 인터넷플랫폼광고_산업분석.md"},
            {"label": "10월 목표가 변경", "value": f"하향 {n_down} · 유지 {n_flat} · 상향 {n_up}",
             "note": f"직전값이 확인되는 {n_down + n_flat + n_up}건. 상향은 NHN(한화)·NAVER(신한)",
             "src": "인터넷게임_원장대조_2026-10-21.json"},
            {"label": "3Q 컨센 영업이익 YoY 감소", "value": f"{n_yoy_down} / 8종목",
             "note": "NAVER·크래프톤·넷마블·시프트업", "src": "네이버 컨센 10/21 ÷ DART 3Q25"},
            {"label": "카카오 목표가 중앙값", "value": f"{won(LEDGER['035720']['tp0828'])} → {won(LEDGER['035720']['tp_med'])}원",
             "note": pct((LEDGER['035720']['tp_med'] / LEDGER['035720']['tp0828'] - 1) * 100) + " (8/28 → 10월), 업종 최대 하향",
             "src": "인터넷게임_원장대조_2026-10-21.json"},
            {"label": "NAVER 3Q 컨센 영업이익률", "value": f"{naver_q3e_opm}%",
             "note": f"4Q25 {dict(naver_opm)['4Q25']}% → 2Q26 {dict(naver_opm)['2Q26']}%", "src": "DART 분기 · 네이버 컨센 10/21"},
        ],
    },
    "sections": [],
    "sources": [
        "10_국내주식/20_소프트웨어/인터넷게임_핵심종목점검_2026-10-21.md (원장 기준, 최신 판단)",
        "10_국내주식/20_소프트웨어/_시총상위_종목표.md (2026-10-21 상단 표·10월 리포트 명세)",
        "10_국내주식/20_소프트웨어/인터넷플랫폼광고_산업분석.md (2026-04-30 작성, §1·§3·§5·§6, 시장 상황 10/21)",
        "10_국내주식/20_소프트웨어/소프트웨어_기초자료.md · 소프트웨어_기업분석.md",
        "10_국내주식/20_소프트웨어/프론티어랩_추론손익_국내IT_2026-09-01.md",
        "10_국내주식/11_화장품의류완구/K뷰티_K콘텐츠_통합_산업분석_2026Q2.md (§4 용어 박스, §5-3 크래프톤, §5-4 시프트업, §7-3)",
        "_manifest/데이터/인터넷게임_원장대조_2026-10-21.json (10월 목표가·3Q 원장 추정·8/28 대비)",
        "_manifest/데이터/인터넷게임_이력.json (dart_q · naver_cons · tp_monthly · tp_changes)",
        "_manifest/데이터/인터넷게임_2026-10-21.json (KRX 일별 종가 8/3–10/21)",
        "증권사 리포트 인용(메리츠 9/25·10/7, 삼성 9/23·10/8, 한화 10/2·10/8, 하나 10/11 등)은 핵심종목점검 문서에 적힌 원장 reports 제목·요약에서 옮김",
        "10_국내주식/22_반도체/SK스퀘어_지주_심층분석.md (원스토어·구글플레이 앱마켓 점유)",
        "_seminar/build_internet_game.py (OPM·YoY·중앙값·괴리 계산)",
    ],
}
S = spec["sections"]

# 1. summary
S.append({
    "id": "summary", "title": "한 장 요약",
    "lead": "업종 안에서 방향이 셋으로 갈렸다. NHN 은 올라가고, 인터넷·게임 대부분은 이익이 내려오고, NC 만 신작으로 버틴다.",
    "blocks": [
        {"type": "cards", "items": [
            {"tag": "올라가는 쪽", "title": "NHN — 작은 네오클라우드로 재평가",
             "body": f"목표가 중앙값 {won(nhn_tp_first)}원({nhn_tp_first_m}) → {won(nhn_tp_last)}원(2026-10). 근거는 양평 AI 데이터센터 GPU 임대(GPUaaS). 3Q 컨센 영업이익 {won(cons_q3['181710'])}억, YoY {pct(yoy['181710'], 0)}. 주가는 8/21 고점 대비 {pct(LEDGER['181710']['from_hi_pct'])}."},
            {"tag": "내려오는 쪽", "title": "이익이 꺾이는 분기",
             "body": f"3Q 컨센 영업이익 YoY: NAVER {pct(yoy['035420'], 0)} · 크래프톤 {pct(yoy['259960'], 0)} · 넷마블 {pct(yoy['251270'], 0)} · 시프트업 {pct(yoy['462870'], 0)}. 10월 중 컨센도 내려왔다(크래프톤 {pct(cons_move['259960'])}, 펄어비스 {pct(cons_move['263750'])}, NAVER {pct(cons_move['035420'])})."},
            {"tag": "배수가 내려가는 쪽", "title": "카카오 — 이익은 늘고 목표가는 반 토막",
             "body": f"12개월 목표가 변경 {tp_counts('035720')[0]}건 중 {tp_counts('035720')[2]}건 하향. 3Q 컨센 YoY {pct(yoy['035720'], 0)}로 이익은 늘지만, 리포트 공통 결론은 'AI 전략 실행을 증명하기 전까지 배수를 안 준다'."},
            {"tag": "예외", "title": "NC — 신작이 숫자를 만든 곳",
             "body": f"분기 영업이익 −75억(3Q25) → 1,739억(2Q26). 12개월 변경 {tp_counts('036570')[0]}건 전부 상향, 10월 7곳 전부 유지. 3Q 컨센 {won(cons_q3['036570'])}억(10월 중 {pct(cons_move['036570'])})."},
        ]},
        {"type": "text", "md": "**다음 4주에 볼 것**\n\n- 3Q 실적: 원장 리포트 추정이 컨센보다 낮은 넷마블(" + pct(est_vs_cons['251270']) + ")·펄어비스(" + pct(est_vs_cons['263750']) + ")·크래프톤(" + pct(est_vs_cons['259960']) + ")의 하회 위험\n- NHN 포항 AIDC 계약 구체화\n- 카카오 AI 에이전트(카나나 스페이스) 12월 출시 전 지표\n- 게임 신작 일정: 크래프톤 2027 라인업, 넷마블 출시일 확정"},
        {"type": "callout", "tone": "warn",
         "md": "**주가가 덜 빠졌다고 이익이 좋다는 뜻은 아니다.** 대표 8종목은 8/28 대비 중앙값 " + pct(med_vs0828) + "로 KOSPI(−15.5%)보다 덜 빠졌지만, 10월 목표가는 하향 " + str(n_down) + " · 상향 " + str(n_up) + "이다. 리포트들은 이익이 2026년 하반기에 바닥이라고 전제하는데, 그것을 증명하는 숫자는 출시된 신작(NC)과 클라우드 이익(NHN)뿐이고 나머지(카카오 AI·NAVER AIDC·크래프톤 2027 신작)는 아직 일정이다."},
    ],
})

# 2. model
S.append({
    "id": "model", "title": "어떻게 돈을 버나",
    "lead": "인터넷은 사람을 모아 광고·수수료를 받는 '어장', 게임은 IP 를 만들어 오래 운영하는 '흥행 사업'이다. 같은 소프트웨어 업종이지만 매출 지속성이 전혀 다르다.",
    "blocks": [
        {"type": "flow", "steps": [
            {"title": "사용자 모으기", "body": "검색(NAVER)·메신저(카카오톡)로 사람과 체류시간을 모은다. 카카오톡 DAU/MAU 90%+.", "who": "NAVER · 카카오"},
            {"title": "광고", "body": "검색(CPC)·디스플레이(CPM)·동영상·피드 광고. 인터넷 매출의 코어(약 50–70%).", "who": "파워링크 · 톡비즈 비즈보드"},
            {"title": "커머스", "body": "입점 판매자 거래액(GMV)에서 수수료(Take rate)를 뗀다. 스마트스토어 약 5–7%.", "who": "스마트스토어 · 선물하기"},
            {"title": "핀테크·결제", "body": "결제·송금·대출 중개. 커머스와 묶여 거래액을 키운다.", "who": "네이버페이 · 카카오페이 · NHN KCP(PG)"},
            {"title": "콘텐츠·구독·클라우드", "body": "웹툰·멤버십·이모티콘 구독은 광고 의존을 줄이는 안전판. 클라우드는 서버를 빌려주는 사업.", "who": "웹툰 · 네이버플러스 · NHN 클라우드"},
        ]},
        {"type": "text", "md": "**매출 공식.** 매출 ≈ MAU × DAU 비율 × 체류시간 × 광고 단가(CPC/CPM) × 광고 도달률. 하나가 흔들리면 매출이 출렁인다 — 사용자가 빠지면(MAU↓), 체류시간이 다른 앱으로 새면, AI 로 단가가 오르면(↑).\n\n**한국 인터넷의 천장.** 매출은 사용자 수 × 1인당 매출의 곱이고, 한국은 인구 5천만이 한계다. 그래서 \"한국 안에선 무적, 밖에선 약자\" 구도이고, 성장주에서 디펜시브 가치주로 성격이 바뀌는 중이다."},
        {"type": "table", "columns": ["부문", "NAVER 비중", "카카오 부문", "카카오 비중"],
         "align": ["l", "r", "l", "r"],
         "rows": [
             ["검색·디스플레이 광고 (서치플랫폼)", "40%", "톡비즈 (광고·이모티콘·선물하기)", "30%"],
             ["커머스 (스마트스토어·쇼핑)", "30%", "카카오페이·뱅크 (지분법)", "20%"],
             ["핀테크 (네이버페이)", "10%", "게임즈·픽코마", "15%"],
             ["콘텐츠 (웹툰 등)", "10%", "카카오엔터테인먼트", "15%"],
             ["클라우드·기술 (NCP·하이퍼클로바X)", "10%", "모빌리티·기타", "20%"],
         ],
         "note": "인터넷플랫폼광고_산업분석.md §3 의 2025년 매출 구성 추정치(2026-04 작성). 감사 수치가 아니라 감 잡기용이다."},
        {"type": "flow", "steps": [
            {"title": "개발", "body": "IP(세계관·캐릭터)를 만든다. 한 번 만들기 어렵지만 만들고 나면 복제 비용이 거의 0.", "who": "개발사(스튜디오)"},
            {"title": "퍼블리싱", "body": "마케팅·서비스 운영·결제를 맡고 매출을 나눈다. 남의 IP 를 서비스하면 로열티가 원가다.", "who": "넷마블(퍼블리싱 구조) · NC 의 TL 퍼블리싱 계약"},
            {"title": "유통 플랫폼", "body": "앱 마켓(구글플레이 70%+, 원스토어 2위)·PC(스팀)·콘솔 스토어를 거쳐 팔고 플랫폼에 수수료를 낸다.", "who": "구글플레이 · 스팀 · PS5"},
            {"title": "출시", "body": "출시 분기에 이익이 몰린다. 펄어비스 붉은사막 1Q26 영업이익 2,121억, 26일 만에 500만 장.", "who": "NC 아이온2 · 펄어비스 붉은사막"},
            {"title": "라이브 서비스", "body": "업데이트·이벤트로 매출을 유지한다. 시간이 지나면 '하향 안정화' — 기존작 매출 감소 속도가 실적을 정한다.", "who": "리니지 · 니케 · PUBG"},
            {"title": "IP 확장", "body": "PC·모바일·콘솔·영상으로 넓힌다. PUBG 는 드라마·영화화 논의까지. 흥행 IP 는 10년 단위로 쓴다.", "who": "크래프톤 PUBG 10주년(2027)"},
        ]},
        {"type": "chart", "kind": "bar", "title": "출시 분기에 몰리는 이익 — 펄어비스 분기 영업이익", "unit": "억원",
         "series": [{"name": "영업이익", "data": pa_q}],
         "note": "붉은사막 1Q26 출시. 3Q26E 는 네이버 컨센 10/21. 3Q25 는 DART 기준 106억 흑자(리포트 표의 −152억은 오류).",
         "src": "인터넷게임_이력.json dart_q · naver_cons"},
        {"type": "cards", "items": [
            {"tag": "장르", "title": "MMORPG — 길게, 하지만 서서히 줄어든다",
             "body": "출시 뒤 하향 안정화가 기본. NC 3Q 는 리니지 클래식 하향 안정화·아이온2 국내 트래픽 감소로 2Q(1,739억)보다 내려온다."},
            {"tag": "장르", "title": "패키지·콘솔 — 출시 분기 집중",
             "body": "시프트업 분기 영업이익 682억(2Q25) → 281억(2Q26). 2025 출시작 효과가 빠지면 공백이 그대로 보인다."},
            {"tag": "장르", "title": "배틀로얄·라이프 시뮬 — 장수 IP",
             "body": "PUBG 는 1세대 배틀로얄 대표작으로 PC·모바일·콘솔 합산. 라이프 시뮬레이션(inZOI)은 '10년 단위로 쓰는 장르'."},
            {"tag": "함정", "title": "게임사를 소프트웨어 배수로 재면 어긋난다",
             "body": "구독 소프트웨어처럼 반복 매출이 쌓이지 않는다. 신작 일정과 흥행 편차가 실적을 정하고, 단일 IP 의존(크래프톤·시프트업)이 늘 약점이다."},
        ]},
    ],
})

# 3. ai
S.append({
    "id": "ai", "title": "AI 가 바꾸는 것 — 쓰는 쪽과 빌려주는 쪽",
    "lead": "NAVER·카카오는 AI 에 돈을 쓰고 회수를 증명해야 하는 쪽이다. NHN 은 GPU 를 빌려주고 임대료를 받는 쪽이다. 같은 AI 가 한쪽엔 비용, 다른 쪽엔 매출이다.",
    "blocks": [
        {"type": "cards", "items": [
            {"tag": "쓰는 쪽", "title": "NAVER — 매출은 크는데 이익률이 내려온다",
             "body": f"매출 YoY +12–16% 유지. 영업이익률은 {dict(naver_opm)['4Q25']}%(4Q25) → {dict(naver_opm)['2Q26']}%(2Q26) → 3Q 컨센 {naver_q3e_opm}%. 원인은 커머스 프로모션·Npay 단말기 설치비·AI 인프라 감가상각. 답안은 AI Factory·AIDC(에셋라이트 구조). 한화: '비용 압박은 하반기가 정점'."},
            {"tag": "쓰는 쪽", "title": "카카오 — AI 서비스는 아직 매출이 없다",
             "body": "카카오톡 안의 AI 에이전트(카나나)가 답안. 카나나 스페이스 12월·칸버스 연말 출시 예정, 카카오톡 내 소규모 테스트 전환율 40%(10/14 요약). 리포트 제목이 요구를 말한다 — '증명해야 할 것이 많아진 때'(메리츠), '탁월한 계획보다 완벽한 실행'(IBK)."},
            {"tag": "빌려주는 쪽", "title": "NHN — 정부 GPU 를 운영하고 일부를 민간에 임대",
             "body": "양평 리전에서 정부 소유 GPU(B200 7,656장, 20MW)를 운영하고 일부를 민간에 임대해 연 1천억 규모 GPUaaS 매출(삼성 9/23). 고객 임대 기간과 데이터센터 리스 기간을 맞춰 가격 하락 위험을 막아 두었다. 2Q26 클라우드 분기 매출이 처음 1천억을 넘었고, 1Q −100억 → 2Q +100억 흑자 전환(메리츠 9/25)."},
            {"tag": "빌려주는 쪽", "title": "NHN 다음 단계 — 30MW 추가",
             "body": "2027년까지 포항 임차 20MW(5년 임대차 확약서 체결)와 자체 10MW 를 추가 확보(삼성 9/23). 전량 민간 임대 시 연 최대 7,500억 매출 가능(메리츠 9/25, 삼성 10/8). 정부·민간 비중에 따라 1,500–7,500억 범위로 달라지고, 신규 사이트 매출은 4Q27 이후(삼성)."},
        ]},
        {"type": "text", "md": "**광고 쪽에서 AI 가 하는 일.** 타겟팅 정밀화 → 광고 소재 자동 생성 → 입찰·예산 자동 최적화 → 에이전트 광고(미래) 순서다. 글로벌에선 Meta Advantage+·Google Performance Max 가 광고 효율을 끌어올렸다. 한국은 하이퍼클로바X(검색+광고 통합)·카나나(톡비즈 타겟팅)로 따라가지만 글로벌 대비 후발이다.\n\n**리포트가 매기는 NHN 의 값.** 삼성은 NHN 클라우드 적정 가치를 1.6조로 본다. 메리츠는 2027년 PER 11.7배로 \"공급자 우위 시장의 네오클라우드를 싸게 사는 기회\"라고 한다. 10월 목표가는 한화 87,000(65,000에서 +33.8%, '클라우드 사업 가치 반영 구간')·삼성 92,000('AI 인프라 기업으로 리레이팅') 두 곳이다.\n\n**하우스 메모(9/1).** 배포형(NAVER·카카오)은 모델을 검색·커머스·카톡에 붙이는 구조라 토큰 가격 전쟁의 직접 피해자가 아니다. GPUaaS(NHN)는 '이미 계약된 용량'만 반영하고 가동률·어태치를 본다."},
        {"type": "callout", "tone": "info",
         "md": "**판단.** 'AI 관련 발표를 매출로 환산하면 이르다'는 하우스 원칙은 NAVER·카카오에 아직 맞다 — 둘 다 비용이 먼저 잡히고 매출은 일정이다. NHN 은 예외로, GPUaaS 가 이미 분기 매출(클라우드 1천억)과 흑자로 찍혔다. 다만 NHN 근거는 리포트 2–5곳의 추정이고 10월 리포트는 2곳뿐이다."},
    ],
})

# 4. cycle
S.append({
    "id": "cycle", "title": "사이클 — 게임은 신작, 인터넷은 광고·비용",
    "lead": "게임주의 이익은 신작 출시 시점이 정하고, 인터넷주의 이익률은 광고 경기와 투자 비용이 정한다. 2026년 하반기 업종 다수는 게임 신작 공백기에 있다.",
    "blocks": [
        {"type": "cycle", "phases": [
            {"name": "공개", "signal": "게임쇼(게임스컴·도쿄게임쇼) 공개, 트레일러 반응. 크래프톤 2027 신작 5종 게임스컴 공개"},
            {"name": "사전예약·테스트", "signal": "사전 예약 규모, 베타 테스트 반응. 목표가가 먼저 움직인다"},
            {"name": "출시", "signal": "출시 분기 이익 급증, 목표가 일괄 상향. NC 2026-05-14 하루 4곳 상향"},
            {"name": "초기 피크", "signal": "앱 매출 순위·스팀 동시접속 정점. 아이온2 글로벌 최고 동접 39.7만"},
            {"name": "하향 안정화", "signal": "기존작 매출 감소 속도가 이익을 정한다. 리니지 클래식·니케"},
            {"name": "신작 공백", "signal": "이익 추정 하향, 매수 근거가 '다음 신작'으로 이동. 크래프톤·넷마블·시프트업", "now": True},
        ],
         "note": "업종 다수(크래프톤·넷마블·시프트업)가 '신작 공백'에 있다. NC 는 아이온2 글로벌 출시 직후(초기 피크), 펄어비스는 붉은사막 출시 뒤 하향 안정화다. 리포트들은 대부분 2027년 신작을 근거로 매수를 유지해 목표가는 버티고 이익 추정은 내려온다."},
        {"type": "chart", "kind": "line", "title": "인터넷 영업이익률 — NAVER·카카오 분기 OPM", "unit": "%",
         "series": [{"name": "NAVER", "data": naver_opm_e}, {"name": "카카오", "data": kakao_opm_e}],
         "note": "DART 분기 연결(4Q 는 연간 − 3분기 누계 역산). 3Q26E 는 네이버 컨센 10/21 영업이익 ÷ 매출. NAVER 는 19%대에서 14%대로, 카카오는 6%대에서 13%대로 서로 반대 방향이다.",
         "src": "인터넷게임_이력.json dart_q · naver_cons (build_internet_game.py 계산)"},
        {"type": "text", "md": "**두 회사가 반대로 움직인 이유.** NAVER 는 매출이 크는 동안 커머스 프로모션·Npay 단말기·AI 인프라 감가상각이 겹쳐 이익률이 내려왔다. 카카오는 광고 성장이 숨을 고르는 대신 비용 효율화로 이익률을 올렸다. 그런데 시장의 배수는 거꾸로 매겨졌다 — 카카오 12개월 목표가 변경은 대부분 하향이다. 인터넷주에서 이익률은 필요조건이지 충분조건이 아니고, 'AI 투자가 언제 매출로 돌아오나'가 배수를 정한다."},
    ],
})

# 5. indicators
S.append({
    "id": "indicators", "title": "무엇을 보나",
    "lead": "발표 전 컨센 이동, 신작의 주간 성과, NHN 클라우드 숫자, 카카오 AI 지표가 다음 판정을 정한다. 앱 순위·스팀 동접은 아직 원장에 없다.",
    "blocks": [
        {"type": "checklist", "items": [
            {"what": "3Q 컨센 수정 방향", "why": "발표 전 컨센 이동이 서프라이즈 크기를 미리 말한다",
             "now": "하향: " + " · ".join(f"{NAME[c]} {pct(cons_move[c])}" for c in sorted(ORDER, key=lambda c: cons_move[c]) if cons_move[c] < -1) + f" / 상향: NC {pct(cons_move['036570'])}",
             "where": "원장 naver_consensus_snap (일별, 10/4–10/21)"},
            {"what": "3Q 실적 발표", "why": "판정의 채점", "now": "10월 말–11월 중순 (원장 calendar_events 에 일정 없음)", "where": "DART 잠정실적 공시"},
            {"what": "앱 매출 순위·스팀 동시접속", "why": "신작 성과의 주간 지표. NC 는 '스팀 데이터에 달린 주가'(메리츠 10/7)",
             "now": "아이온2 글로벌 최고 동접 39.7만(하나 10/11)", "where": "원장에 없다 — 모바일인덱스·센서타워·SteamDB 수집 대상"},
            {"what": "신작 일정", "why": "2027년 이익 추정의 근거",
             "now": "크래프톤 데드넷·NO LAW·프로젝트 제타 등 5종(게임스컴 공개) · 시프트업 Spirits 연내 공개 · 펄어비스 붉은사막 DLC · 넷마블 출시일 미확정", "where": "회사 발표·게임쇼"},
            {"what": "NHN 클라우드 분기 매출·이익", "why": "리레이팅의 유일한 근거",
             "now": "2Q26 분기 매출 첫 1천억 · 1Q −100억 → 2Q +100억 흑자 전환(메리츠 9/25). 3Q 는 1천억 선 유지 여부", "where": "실적 발표 부문별 공시"},
            {"what": "NHN AIDC 계약", "why": "2028년 GPUaaS 매출(삼성 가정 연 4천억)의 전제",
             "now": "포항 20MW 5년 임대차 확약서 · 자체 10MW 증설 계획(삼성 9/23). 본계약·착공·정부 GPU 2차 사업 대기", "where": "공시·IR"},
            {"what": "카카오 AI 지표", "why": "하향 사이클을 끝낼 유일한 재료",
             "now": "카나나 스페이스 12월·칸버스 연말 출시 예정 · 테스트 전환율 40%(10/14 요약) · 3Q 톡비즈 광고 성장률", "where": "회사 발표·실적"},
            {"what": "NAVER 이익률", "why": "비용 정점 통과 확인",
             "now": f"3Q 컨센 OPM {naver_q3e_opm}% · 커머스 프로모션비 · AI Factory 외부 자본 구조", "where": "실적 발표"},
            {"what": "금리", "why": "성장주 배수. NHN 은 '8월 말 금리 급등과 차익 실현으로 한 달 상승분 절반 반납'(메리츠 9/25)",
             "now": "—", "where": "원장 macro_series (ECOS)"},
        ]},
    ],
})

# 6. players
S.append({
    "id": "players", "title": "종목 지도",
    "lead": "인터넷 둘, 인터넷+클라우드 하나(NHN), 게임 다섯. 업종 핵심주는 NHN 이다 — 게임·결제·클라우드를 다 가졌고 목표가가 유일하게 크게 올랐다.",
    "blocks": [
        players_table,
        {"type": "table", "columns": ["종목", "12개월 목표가 변경", "상향", "하향", "첫 달 중앙값", "10월 중앙값"],
         "align": ["l", "r", "r", "r", "r", "r"], "rows": tp_change_rows,
         "note": "원장 reports, 증권사별 그 달 최신 1건 기준 월별 중앙값(tp_monthly)과 목표가 변경 이력(tp_changes). 카카오 10월 중앙값이 위 표(43,500, 6곳)와 다른 것은 증권사 칸이 빈 '미상' 1건 포함 여부 차이다."},
    ],
})

# 7. now
S.append({
    "id": "now", "title": "2026년 10월 현황",
    "lead": "목표가 경로가 세 종목의 운명을 그대로 보여 준다. NHN 은 세 배, NC 는 완만한 상향, 카카오는 반 토막. 3Q 는 원장 리포트 추정이 컨센보다 낮은 곳이 많다.",
    "blocks": [
        {"type": "chart", "kind": "line", "title": "12개월 목표가 경로 — NHN·카카오·NC (2025-11 = 100)", "unit": "지수",
         "series": tp_series,
         "note": f"원장 월별 목표가 중앙값을 2025-11 값으로 나눠 지수화. 원값: NHN {won(tpm['181710'][base_m])} → {won(tpm['181710']['2026-10'])}원, 카카오 {won(tpm['035720'][base_m])} → {won(tpm['035720']['2026-10'])}원, NC {won(tpm['036570'][base_m])} → {won(tpm['036570']['2026-10'])}원. 리포트가 없는 달은 비어 있다.",
         "src": "인터넷게임_이력.json tp_monthly (build_internet_game.py 계산)"},
        {"type": "chart", "kind": "hbar", "title": "3Q26 컨센 영업이익 YoY", "unit": "%",
         "series": [{"name": "YoY", "data": [[NAME[c], round(yoy[c], 1)] for c in sorted(ORDER, key=lambda c: (yoy[c] is None, yoy[c] or 0)) if yoy[c] is not None and c != "263750"]}],
         "note": f"네이버 컨센 10/21 ÷ DART 3Q25 영업이익 − 1. 축 밖 2종목: NC 흑자 전환(3Q25 −75억 → 컨센 {won(cons_q3['036570'])}억), 펄어비스 {pct(yoy['263750'], 0)}(3Q25 106억 저기저).",
         "src": "인터넷게임_이력.json naver_cons · dart_q"},
        {"type": "chart", "kind": "hbar", "title": "3Q 원장 리포트 추정 vs 컨센 — 괴리", "unit": "%",
         "series": [{"name": "원장 추정 중앙값 ÷ 컨센 − 1", "data": [[NAME[c], round(est_vs_cons[c], 1)] for c in sorted(ORDER, key=lambda c: est_vs_cons[c])]}],
         "note": "원장 10월 리포트 3Q 영업이익 추정 중앙값(펄어비스·시프트업 메리츠 1곳, NHN 한화 1곳) ÷ 네이버 컨센 10/21. 음수 = 발표 전 컨센 하회 위험.",
         "src": "인터넷게임_원장대조_2026-10-21.json q3_med · 인터넷게임_이력.json naver_cons"},
        {"type": "table", "columns": ["종목", "3Q 컨센 10/4", "3Q 컨센 10/21", "10월 중 변화", "원장 추정 중앙값"],
         "align": ["l", "r", "r", "r", "r"],
         "rows": [[NAME[c], won(cons_q3_first[c]), won(cons_q3[c]), pct(cons_move[c]), won(LEDGER[c]["q3_med"])] for c in ORDER],
         "note": "단위 억원. 컨센은 원장 naver_consensus_snap, 원장 추정은 10월 리포트 report_estimates."},
        {"type": "callout", "tone": "warn",
         "md": "**판단.** 3Q 발표에서 하회 위험이 큰 곳은 넷마블(원장 추정이 컨센보다 " + pct(est_vs_cons['251270']) + ")·펄어비스(" + pct(est_vs_cons['263750']) + ")·크래프톤(" + pct(est_vs_cons['259960']) + ")이다. NHN 시장이 볼 것은 3Q 이익(쉬어 가는 분기, 양평 감가상각 약 100억)이 아니라 **클라우드 부문 매출이 1천억 선을 지키는지와 4Q 공공 프로젝트 반영**이다. 주가 57,100원은 10월 목표가(8.7–9.2만)보다 34–38% 낮지만 근거 리포트가 2곳뿐이다. 카카오는 이익보다 12월 카나나 스페이스 초기 지표가 배수를 정한다."},
    ],
})

# 8. risks
S.append({
    "id": "risks", "title": "리스크",
    "lead": "업종 공통은 'AI 비용 회수'와 '신작 공백'이다. NHN 은 구조가 다르지만 커버리지가 얇고 매출 범위가 넓다.",
    "blocks": [
        {"type": "cards", "items": [
            {"tag": "인터넷", "title": "AI 비용 회수가 늦어진다",
             "body": f"NAVER 영업이익 YoY 는 +15%(1Q25)에서 3Q 컨센 {pct(yoy['035420'], 0)}로 내려왔다. 카카오 AI 서비스는 아직 매출이 없다. 회수가 일정보다 늦으면 배수 하향이 이어진다(카카오 12개월 {tp_counts('035720')[2]}건 하향)."},
            {"tag": "게임", "title": "신작 공백과 일정 지연",
             "body": "크래프톤·넷마블·시프트업의 매수 근거는 2027년 신작이다. 넷마블 리포트 제목 흐름: '다소 아쉬운 신작 성과'(5월) → '부족한 하반기'(8월) → '신작 출시일 확인 필요'(10월)."},
            {"tag": "게임", "title": "단일 IP 의존",
             "body": "크래프톤은 PUBG, 시프트업은 스텔라블레이드·니케 의존. 후속작이 흥행하지 못하면 '한 게임 회사'로 돌아간다."},
            {"tag": "인터넷", "title": "트래픽 이탈 — AI 검색",
             "body": "ChatGPT·Perplexity 같은 AI 챗봇이 검색을 대체하는 것이 인터넷주 최대 리스크로 꼽힌다(NAVER 매출의 약 40%가 검색 광고). 미래에셋은 5월 '트래픽 감소 우려'로 NAVER 목표가를 −30% 내렸다."},
            {"tag": "규제", "title": "규제는 양방향",
             "body": "NHN 은 웹보드 결제 한도 상향(규제 완화)이 게임 이익 바닥을 받쳤다(메리츠 1월). 반대로 카카오는 골목상권·사법 리스크, 플랫폼 공정거래법 검토가 디스카운트 요인이다."},
            {"tag": "NHN", "title": "매출 범위가 넓고 시점이 멀다",
             "body": "정부·민간 비중에 따라 GPUaaS 매출이 1,500–7,500억으로 달라지고, 신규 사이트 매출은 4Q27 이후다(삼성)."},
            {"tag": "데이터", "title": "커버리지가 얇다",
             "body": "10월 리포트: NHN 2곳, 시프트업 2곳, 펄어비스 1곳(메리츠, 8월은 3만–5만으로 갈림). 중앙값·상방이 한 증권사 의견에 좌우된다. 앱 순위·스팀 동접도 원장에 없다."},
            {"tag": "매크로", "title": "금리",
             "body": "성장주 배수에 직접 작용한다. NHN 은 8월 말 금리 급등과 차익 실현으로 한 달 상승분 절반을 반납했다(메리츠 9/25)."},
        ]},
    ],
})

# 9. glossary
S.append({
    "id": "glossary", "title": "용어",
    "lead": "리포트에서 바로 마주치는 말만 골랐다.",
    "blocks": [
        {"type": "glossary", "items": [
            {"term": "MAU / DAU", "def": "월간·일간 활성 사용자. DAU/MAU 비율이 높을수록 매일 들어오는 '끈끈한' 플랫폼(카카오톡 90%+)."},
            {"term": "ARPU", "def": "사용자 1인당 평균 매출. ARPU × MAU = 매출."},
            {"term": "ARPPU", "def": "결제 사용자 1인당 평균 매출. 게임은 일부가 결제하므로 ARPU 와 따로 본다."},
            {"term": "CPC / CPM", "def": "클릭당 광고비 / 1,000회 노출당 광고비. 검색 광고는 주로 CPC, 디스플레이는 CPM."},
            {"term": "GMV · Take rate", "def": "거래액 총합(매출이 아님)과 그중 회사가 매출로 가져가는 비율. 스마트스토어 약 5–7%."},
            {"term": "톡비즈", "def": "카카오톡 광고(비즈보드)·알림톡·이모티콘·선물하기 매출. 카카오 이익의 중심."},
            {"term": "PG", "def": "온라인 결제대행. 가맹점과 카드사 사이에서 결제를 처리하고 수수료를 받는다. NHN KCP."},
            {"term": "IP", "def": "지식재산권. 캐릭터·세계관·게임 같은 무형 자산. 한 번 흥행하면 여러 플랫폼·매체로 확장한다."},
            {"term": "퍼블리싱", "def": "개발된 게임의 마케팅·운영·결제를 맡아 서비스하는 일. 남의 IP 를 퍼블리싱하면 로열티가 원가."},
            {"term": "라이브 서비스", "def": "출시 뒤 업데이트·이벤트로 수년간 매출을 이어가는 운영 방식. 기존작 매출 감소 속도가 핵심."},
            {"term": "하향 안정화", "def": "신작 출시 뒤 매출이 정점에서 내려와 일정 수준에 자리 잡는 과정. 리포트에 자주 나오는 표현."},
            {"term": "동접(동시접속자)", "def": "같은 시각 접속한 사용자 수. 스팀(SteamDB)에서 공개돼 PC 신작 성과의 주간 지표로 쓴다."},
            {"term": "웹보드", "def": "포커·고스톱 같은 웹 기반 보드게임. 결제 한도 규제를 받는다. NHN 게임 이익의 바닥."},
            {"term": "GPUaaS", "def": "GPU 를 시간·기간 단위로 빌려주는 클라우드 서비스. NHN 클라우드가 양평 리전 B200 으로 제공."},
            {"term": "네오클라우드", "def": "AI 연산용 GPU 임대에 특화한 신생 클라우드 사업자. 메리츠는 NHN 을 '공급자 우위 시장의 네오클라우드'로 본다."},
            {"term": "AIDC", "def": "AI 데이터센터. GPU 와 전력(MW)을 갖춘 시설. NHN 포항 20MW, NAVER AI Factory·AIDC."},
            {"term": "에셋라이트", "def": "설비를 직접 소유하지 않고 외부 자본·임차로 확보하는 구조. NAVER AIDC 의 방향."},
            {"term": "컨센서스(컨센)", "def": "증권사 추정치 평균. 이 자료는 네이버 금융 컨센 일별 스냅(원장 naver_consensus_snap)을 쓴다."},
            {"term": "OPM", "def": "영업이익률 = 영업이익 ÷ 매출. NAVER 14–19%, 시프트업 45–66% 처럼 사업 구조에 따라 크게 다르다."},
        ]},
    ],
})

out = ROOT / "_seminar" / "internet_game.json"
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n")
print("wrote", out)
print("vs0828 median", med_vs0828, "up/down/flat", n_up, n_down, n_flat, "yoy_down", n_yoy_down)
print({NAME[c]: (None if yoy[c] is None else round(yoy[c], 1)) for c in ORDER})
print({NAME[c]: round(est_vs_cons[c], 1) for c in ORDER})
print({NAME[c]: round(cons_move[c], 1) for c in ORDER})
print("naver", naver_opm_e); print("kakao", kakao_opm_e)
for s in tp_series: print(s)
