# 🔬 Navitas Semiconductor (NASDAQ: NVTS) 종합 분석 리포트 v2

> **작성일: 2026-05-14 | v1(2026-04-17 초안 + 2026-04-28 밸류에이션 갱신)의 후속 보강판**
> 분량 목표: v1(45k자) 대비 1.5배 (~70k자)
> 기준일 시세: 2026-05-13 종가 $21.17 추정
> 기준 통화: USD

---

## ⚠️ v2 변경 사항 박스 — 반드시 먼저 읽기

본 리포트는 **2026-04-28자 v1** 의 후속 보강판이다. v1 작성 시점에는 "Q1 2026 실적 발표(5/5) 후 재갱신 필수"라고 명시했고, 실제로 5/5 실적 + 5/12 ATM 증자 완료 + 애널리스트 3사 일제 PT 상향이라는 **3대 펀더멘털 이벤트**가 동시에 발생했다. v2는 이 변화를 정면으로 다룬다.

### v1 → v2 정정·갱신 사항

| 항목 | v1 (2026-04-28 기준 추정) | v2 (2026-05-14 기준 공시 확정) |
|---|---|---|
| Q1 2026 매출 | 가이던스 $8.0–8.5M | **실적 $8.6M** (가이던스 상단 상회, QoQ +18%, YoY -39%) |
| Non-GAAP EPS | 컨센서스 -$0.05 | **실적 -$0.04** (Beat 20%) |
| Non-GAAP 총이익률 | Q4 38.7% 기준 | **Q1 39.0%** (소폭 개선) |
| 분기말 현금 | ~$75M (Q3 2025 기준 추정) → 추정치 오류 | **$221.0M** (3/31 기준) — 실제로는 v1 추정의 ~3배 |
| 디자인윈 백로그 | $450M | **$2.4B** (5.3배 점프) |
| 2030 SAM | "$3.5B" | $3.5B 유지 + **60%+ CAGR** 추가 가이던스 |
| 애널리스트 평균 PT | $8.15 (Koyfin) | **$15+** 추정 (Needham $21, Baird $20, Rosenblatt $13 등 일제 상향) |
| 증자 가능성 | "1–1.5년 내 증자 희석 현실적" | **2026-05-12 ATM $122M 완납 실현** (희석 ~3.5%, 현금 +56%) |
| 주가 (기준일) | 4/21 $15.66 (4주 +89% 후) | 5/13 $21.17 (4/28 대비 +35%) |

### v2 신규 보강 6대 영역

1. **Q1 2026 실적 심층 분석** — 가이던스 상단 적중 + Q2 매출 $10M± 가이던스 + 신경영진 첫 분기 컨콜 톤
2. **$2.4B 디자인윈 백로그** — v1 $450M의 **5.3배 점프** 메커니즘과 신뢰성 검증
3. **ATM $122M 증자 분석** — 6.53M 신주 발행, 평균 $18.70, 희석 ~3.5%, **현금 런웨이 18~24개월로 확장**
4. **20kW 800V-6V PDB + 250kW SiC SST** — GTC 2026 → APEC 2026 → Q1 컨콜로 이어지는 제품 라인업 2배 확장
5. **애널리스트 PT 일제 상향** — Needham $13→$21 (+62%), Baird $9→$20 (+122%), Rosenblatt $7→$13 (+86%) — 컨센서스가 시장가 따라잡기 시작
6. **밸류에이션 v2** — EV/Sales 재계산 + Bull/Base/Bear 시나리오 갱신 + ATM 후 희석 반영

### 한 줄 결론(미리 공개)

> v1에서 지적한 **"테마 ↔ 실적 괴리"** 가 **부분적으로** 좁혀졌다. Q1 실적은 가이던스 상단 적중, 디자인윈 백로그 5배 점프, ATM으로 증자 리스크 일소(一掃) 3박자가 갖춰지며 "쇼-미(show-me) 스토리"에서 **"실행 초기 검증"** 단계로 진입. 다만 **여전히** 2026 연간 매출 ~$41M 가이던스 대비 시총 $4B+(현재가 기준)의 EV/Sales 40~50x는 옵션 가격 영역. 2027 NVIDIA Kyber 양산까지 **18~20개월의 인내 구간**.
> 결론: **소형 옵션성 베팅(포트 2~5%) 유지**, 분기마다 ① 디자인윈→매출 변환 비율 ② 데이터센터 매출 분리 공시 여부 ③ NVIDIA 외 티어-1 ODM 명시 ④ Q2 가이던스 적중 확인이 핵심 트래킹 포인트.

---

## 📋 목차 (v2)

1. v2 Executive Summary (갱신)
2. 5월 핵심 사건 5종 타임라인 (신규)
3. Q1 2026 실적 심층 분석 (신규)
4. $2.4B 디자인윈 백로그 — 5배 점프 해석 (신규)
5. ATM $122M 증자 — 희석률·런웨이·시그널 (신규)
6. 제품 라인업 2배 확장 (20kW PDB + 250kW SST) (신규)
7. 애널리스트 PT 일제 상향 + 컨센서스 재구성 (신규)
8. 밸류에이션 v2 — EV/Sales 재계산 + 시나리오 갱신 (신규)
9. 5월 주가 모멘텀 해부 (신규)
10. v1 대비 리스크 매트릭스 갱신
11. 5/5 컨콜에서 답하지 않은 4가지 (신규)
12. Q2 2026 트래킹 체크리스트 (신규)
13. 종합 결론 + 포지션 권고 v2
14. 출처 (v2 신규 출처 포함)

---

## 1. v2 Executive Summary (갱신)

### 1.1 한 줄 정의 (변동 없음)

GaN+SiC 듀얼 플랫폼을 보유한 유일한 순수(pure-play) 차세대 전력반도체 상장사. 매출 규모는 작지만(2025 $46M) NVIDIA 800V HVDC 데이터센터 아키텍처 변환의 **유일 풀스택 공급자** 후보.

### 1.2 v2 시점 핵심 변동표

| 항목 | v1 (2026-04-28) | v2 (2026-05-14) | 변동 |
|---|---|---|---|
| 주가 | $15.66 (4/21) | **~$21.17** (5/13) | +35% |
| 시가총액 | ~$2.9B (188M주 기준) | **~$4.1B** (~195M주 기준, ATM 후) | +41% |
| 발행주식 수 | ~188M | **~194.5M** (188M + ATM 6.53M) | +3.5% 희석 |
| 분기말 현금 | ~$75M 추정 → 오기 | **$221.0M** (3/31) → ATM 후 **~$343M** | +358% |
| 분기 Cash Burn | $12–15M | $11~13M (개선) | 안정 |
| 현금 런웨이 | 5–6분기 | **18–24개월** (Q2 OpEx 기준) | 3배 연장 |
| Q1 매출 | $8.0–8.5M 가이던스 | **$8.6M 실적** | +1.2% 상회 |
| Q2 매출 가이던스 | 미공개 | **$10.0M ±$0.5M** | QoQ +16%+ |
| Non-GAAP GM | 38.7% (Q4) | **39.0% (Q1) → 39.25% (Q2 가이던스)** | 점진 개선 |
| 디자인윈 백로그 | $450M | **$2.4B** | +433% |
| 2030 SAM | $3.5B | $3.5B + **60%+ CAGR** | 성장률 명시 |
| 애널리스트 평균 PT | ~$8.15 | **$15+** 추정 | +84% |
| 핵심 카탈리스트 | NVIDIA GTC + GF | + **Q1 적중** + **$2.4B 백로그** + **EPFL SST** | +3종 |

### 1.3 v1 → v2 톤 변화

v1: **"테마 과열, 실적 부진, 증자 임박, 컨센서스 디스카운트"** → 경계적 톤
v2: **"테마 유지, 실적 첫 적중, 증자 완납, 컨센서스 추격"** → 검증 초기 톤

다만 **EV/Sales 40~50x**는 여전. 2026 매출 가이던스 $41M 기준 시총 $4.1B → **P/S ~100x**, 2027 매출 컨센서스 $150M 기준 **Forward P/S 27x**. 동종 GaN/SiC 평균 P/S 3~5x 대비 **5~10배 프리미엄**은 그대로.

### 1.4 한 단락 톤 요약

NVTS는 v1 시점에서 **"NVIDIA 발표→주가 선반영→실적 미달 우려"** 사이클의 정점에서 멈춰있었다. 5월 첫째 주 3대 이벤트(실적 적중·백로그 5배·ATM 완납)로 **사이클 1라운드 검증 통과**. 그러나 v1에서 지목한 본질적 리스크(① 2027 Kyber 양산 일정, ② 티어-1 ODM 명시, ③ 컨센서스 추격 vs 주가 조정 분기)는 **여전히 미해결**. 5/12 ATM 발표 후 장중 -10% 변동성이 이를 방증.

---

## 2. 5월 핵심 사건 5종 타임라인 (신규)

> v1 작성(4/28) 이후 **16일 동안** 발생한 사건. 이 압축된 기간에 펀더멘털 변수가 거의 모두 갱신됐다.

### 2026-05-05 (화) 장 마감 후 — Q1 2026 실적 발표
- **매출 $8.6M** (가이던스 $8.0~8.5M 상단 상회, QoQ +18%, YoY -39%)
- **Non-GAAP EPS -$0.04** (컨센서스 -$0.05 Beat)
- **현금 $221.0M** (FYE 2025 $236.9M 대비 -$15.9M, 분기 Cash Burn ~$16M)
- Q2 가이던스: 매출 $10.0M ±$0.5M, Non-GAAP GM 39.25% ±75bps, OpEx $14.5–15.5M
- 디자인윈 백로그 **$2.4B** (v1 $450M 대비 5.3배), 2030 SAM **$3.5B at 60%+ CAGR**
- 신경영진(Allexandre CEO + Stevens CFO) **첫 분기 컨콜** — 톤: "Navitas 2.0 실행 가속"

### 2026-05-06 (수) 장중 — 애널리스트 3사 PT 일제 상향
- **Needham (Bolton)**: $13 → **$21** (+62%), Buy 유지
- **Baird**: $9 → **$20** (+122%), **Outperform 유지** (가장 적극)
- **Rosenblatt (Cassidy)**: $7 → **$13** (+86%), **Neutral 유지** (밸류에이션 경계)
- 평균 PT 단일 분기에 ~70% 상향, 시장가 $21 vs 평균 PT $18 → 프리미엄 **+15% 수준**으로 축소 (v1 시점 +90% 프리미엄에서 정상화)

### 2026-05-11 (월) — 주가 +25% 랠리
- Q1 실적·디자인윈·애널리스트 PT 상향 효과 누적
- 종가 추정 ~$21~22 구간, **YTD +400%+ 종목 재확인**
- IBTimes·Motley Fool 등 매체 일제히 "AI 데이터센터 알파 종목" 헤드라인

### 2026-05-12 (화) — ATM $125M Stock Program 완납
- **6,529,666주** 신주 발행 (Class A 보통주)
- **평균 $18.70 (단가 추정)**, 순조달 **$122.0M**
- Craig-Hallum Capital Group + UBS Securities 매각 에이전트
- 장중 반응: 개장 $21.72 → 장중 고가 $22 → 저가 $18.78 → 종가 **$19.25** (장중 -10% 변동성)
- 시장 해석: "확장 자금 확보 긍정" vs "고점 매각·희석 우려" 양분
- **8-K 공시**가 SEC EDGAR에 5/12 등록

### 2026-05-13 (수) — 반등 회복
- 종가 **$21.17** (전일 $19.25 대비 +9.97%) — 희석 우려 단기 해소
- "$2.4B 백로그가 $122M 희석 부담을 상쇄한다"는 매수 논리 재확인
- 시총 ~$4.1B 수준 회복

### 16일 핵심 시사점

1. **실적 + 현금 + 백로그 3박자 → 펀더멘털 베이스 강화**
2. ATM은 **"의외의 호재"** — v1 당시 우려한 증자 희석이 단 3.5% 수준에서 마무리, 현금 런웨이 3배 연장
3. 애널리스트 컨센서스가 처음으로 시장가에 근접 → 상승 동력은 여전하나 **"손쉬운 더블"** 구간은 종료

---

## 3. Q1 2026 실적 심층 분석 (신규)

### 3.1 손익계산서 핵심 수치

| 항목 | Q1 2026 | Q4 2025 | Q1 2025 | YoY | QoQ |
|---|---|---|---|---|---|
| 매출 | **$8.6M** | $7.3M | $14.0M | **-39%** | **+18%** |
| GAAP 매출원가 | $9.4M | $8.6M | $12.7M | -26% | +9% |
| **GAAP 총이익률** | **-9.3%** | -17.2% | 9.1% | -18.4%p | +7.9%p |
| Non-GAAP 매출원가 | $5.2M | $4.5M | $8.7M | -40% | +16% |
| **Non-GAAP 총이익률** | **39.0%** | 38.7% | 38.1% | +0.9%p | +0.3%p |
| GAAP 영업비용 | $26.9M | $33.4M | $31.5M | -15% | -19% |
| **GAAP 영업손실** | **-$27.8M** | -$34.7M | -$30.2M | -8% 개선 | -20% 개선 |
| Non-GAAP 영업손실 | -$11.7M | -$12.6M | -$13.6M | -14% 개선 | -7% 개선 |
| **GAAP 순손실/주** | **-$0.15** | -$0.18 | -$0.16 | 개선 | 개선 |
| **Non-GAAP 순손실/주** | **-$0.04** | -$0.05 | -$0.07 | 개선 | 개선 |

### 3.2 매출 분해 (회사 공시 + 컨콜 발언 기반)

| 카테고리 | Q1 2026 비중 (추정) | YoY 성장률 |
|---|---|---|
| 모바일·저전압 컨슈머 | **소수 (감소 중)** | -60%~-70% (의도적 축소) |
| AI 데이터센터 + 그리드 인프라 | **합산 QoQ +50%** | "강한 성장" (수치 미공개) |
| 고전력 합산(AI DC + Grid + Performance Computing + Industrial Electrification) | **대다수** | **+35%** YoY |

> **핵심**: 회사가 "high-power markets now represent a large majority of total revenue"라고 공식 확인 — v1에서 2025 Q3에 처음 50% 돌파했던 **고전력 매출 비중이 Q1 2026에 70%+ 수준으로 확장** 추정.

### 3.3 가이던스 대비 실적 vs 컨센서스

| 지표 | 회사 가이던스 (2/12 공시) | 컨센서스 | 실적 | 결과 |
|---|---|---|---|---|
| 매출 | $8.0~8.5M | $8.18M | **$8.6M** | **상단 상회 (Beat)** |
| Non-GAAP GM | ~38% | 38.5% | **39.0%** | **소폭 Beat** |
| Non-GAAP EPS | 미공개 | -$0.05 | **-$0.04** | **20% Beat** |

→ **3대 지표 모두 가이던스 상단 또는 컨센서스 상회**. 신경영진의 **첫 분기 적중**으로 신뢰도 1포인트 누적.

### 3.4 Q2 2026 가이던스 (5/5 발표)

| 지표 | Q2 2026 가이던스 | Q1 실적 대비 | 의미 |
|---|---|---|---|
| 매출 | **$10.0M ±$0.5M** | QoQ **+16.3%+** | 가속 추세 |
| Non-GAAP GM | 39.25% ±75bps | +0.25%p | 점진 개선 |
| Non-GAAP OpEx | $14.5~15.5M | Q1 $14.6M | 거의 플랫 |

→ Q2 매출이 가이던스 중간점($10M)을 적중하면 **2개 분기 연속 가속 + GM 점진 확장 + OpEx 통제**라는 트리플 시그널. v1에서 우려한 "1회성 가이던스 적중"이 아닌 **추세 검증** 단계.

### 3.5 컨퍼런스콜 핵심 발언 5종

#### 발언 1 — Allexandre CEO (전략 가속)
> "지난 두 분기 동안 우리는 모바일·저단 컨슈머에서의 피벗을 **'유의미하게(meaningfully) 가속'** 했다. 4개 타깃 세그먼트(AI DC, 에너지·그린 인프라, 퍼포먼스 컴퓨팅, 산업 전동화)에 자원을 집중한다."

#### 발언 2 — Allexandre CEO (AI 데이터센터 성장)
> "AI 데이터센터 + 그리드 인프라 합산 매출이 Q4→Q1에 **QoQ +50%** 성장했다. **예상보다 강했다**. Q2에는 이 추세가 가속될 것."

#### 발언 3 — Stevens CFO (마진 개선 동인)
> "Q1 매출이 QoQ +18% 성장한 것은 **확장된 고객 engagement + 주문 백로그**에서 비롯됐다. **더 우호적인(more favorable) 매출 믹스**가 마진을 끌어올린다."

#### 발언 4 — Allexandre CEO (포지셔닝)
> "Navitas는 **GaN+SiC 양쪽 기술 모두**를 보유한 유일한 회사다. 이로 인해 **더 많은 콘텐츠, 더 넓은 응용 분야**가 가능하다."

#### 발언 5 — Stevens CFO (디자인윈 백로그)
> "현재 디자인윈 파이프라인은 **$2.4B을 초과**한다. 이는 **다음 수년간의 매출 가시성**을 제공한다."

→ **포인트**: ① 매출 가이던스 상회, ② GM 추세 개선, ③ AI/그리드 50% QoQ 가속, ④ **$2.4B 백로그 명시** — 4개 모두 v1 작성 시점 대비 **새로 검증된 변수**.

### 3.6 컨콜에서 답하지 않은 4가지 (5/5 시점)

v1에서 트래킹 포인트로 지목한 4가지 중 **여전히 미공개**:

| 트래킹 포인트 | 5/5 컨콜 답변 여부 |
|---|---|
| ① 데이터센터 매출 **분리** 공시 | ❌ "합산"으로만 공개 |
| ② NVIDIA 외 **티어-1 ODM 명시** (Foxconn/Quanta 등) | ❌ "OEM/ODM/하이퍼스케일러 협력"으로 일반화 |
| ③ NVIDIA Kyber 매출 **시작 시점·랙당 달러 콘텐츠** | ❌ "2027 본격화" 정도만 |
| ④ M&A 가능성 vs 자체 성장 | ❌ 직접 답변 없음 |

→ 이 4가지가 **Q2 실적(8월 초 예상) 또는 GTC 2026 후속 컨퍼런스**에서 풀려야 컨센서스 추가 상향 가능.

---

## 4. $2.4B 디자인윈 백로그 — 5배 점프 해석 (신규)

### 4.1 백로그 추이

| 시점 | 누적 디자인윈 백로그 | 변동 메모 |
|---|---|---|
| 2025 Q3 (10월 컨콜) | ~$300M | 모바일 + 일부 데이터센터 초기 |
| 2026 Q4 2025 (2/12 컨콜) | $450M | NVIDIA GTC 직전, 일부 그리드 추가 |
| **2026 Q1 (5/5 컨콜)** | **$2.4B** | **+$1.95B 단일 분기 추가** |

→ **단일 분기에 백로그 5.3배 점프** — Navitas IR 역사상 최대 단일 분기 증가.

### 4.2 디자인윈이란 무엇인가? (용어 박스)

> **🔍 용어 박스 — 디자인윈(Design Win)**
>
> 전자 부품 업계 표준 용어. **고객사(시스템 OEM/ODM)가 자사 차세대 제품의 "권장 부품 리스트(AVL, Approved Vendor List)" 에 Navitas 칩을 공식 등재한 상태**.
>
> 의미:
> - "발주(주문)"는 아님 — 양산 시작 전 단계의 **선행 지표**
> - 일반적으로 **디자인윈 → 양산 시작 → 본격 매출 전환까지 6~24개월** 소요 (반도체 산업 평균)
> - 디자인윈 금액은 **회사 자체 추정치** — "이 디자인이 양산되면 제품 수명주기 동안 발생할 누적 매출 예상치"
> - **모든 디자인윈이 양산되지는 않음** — 일반적으로 30~60% 전환율 (산업별 차이)
>
> 비유: **신차 출시 전 자동차 회사의 부품 입찰 결과**. "BMW 2027 모델에 우리 와이퍼 채택 결정" 같은 단계. 실제 BMW가 그 모델을 양산하고 매출이 발생하기까지 2년 걸린다.

### 4.3 $2.4B의 신뢰성 검증 — 3대 체크포인트

#### 체크포인트 1: 회사가 정의한 백로그 기간
- **"향후 수년간(over the coming years)"** — 정확한 기간 미공개
- 추정: 2026~2030 (5년) 누적
- 이 경우 **연 환산 ~$480M** — 2030 SAM $3.5B의 13.7% 점유 가정과 정합

#### 체크포인트 2: 전환율 가정
- 보수적(30%): $2.4B × 0.3 = **$720M 누적 매출**
- 중간(45%): $2.4B × 0.45 = **$1.08B 누적 매출**
- 낙관적(60%): $2.4B × 0.6 = **$1.44B 누적 매출**
- 비교: 2025 매출 $46M, 2026E 매출 $41M → **2030년까지 매출 6~10배 확대**가 백로그가 시사하는 시나리오

#### 체크포인트 3: 백로그 구성
- 회사 공식 발언: "**4개 타깃 세그먼트** (AI DC, 에너지·그린, 퍼포먼스 컴퓨팅, 산업 전동화) 전반에 분포"
- AI 데이터센터 단독 비중 미공개 (추정 40~60%)
- **NVIDIA + 하이퍼스케일러 직접 디자인윈** vs **티어-1 ODM 경유** 구분 미공개 — 향후 Q2 실적의 핵심 변수

### 4.4 5배 점프의 동인 — 3개 가설

#### 가설 1: NVIDIA Kyber/Rubin 디자인 락(lock)
- GTC 2026 후 NVIDIA가 Navitas의 800V-6V PDB + 10kW DC-DC 플랫폼을 **공식 레퍼런스로 채택**했을 가능성
- Kyber 랙은 **576 Rubin Ultra GPU** 수용, 랙당 ~1MW 전력 → Navitas 콘텐츠 추정 랙당 $30K~$100K
- 2027~2030 Kyber 생산 누적 5,000~20,000 랙 가정 시 **$0.15B~$2B** 매출 시나리오

#### 가설 2: 하이퍼스케일러 자체 디자인 채택
- Microsoft, Google, AWS, Meta 등이 **NVIDIA 외 자체 800V HVDC 아키텍처**를 설계 중
- 4/13 Fischer 이사 선임의 Broadcom 인프라 경험이 이 라인의 게이트키퍼 가능성
- Cyrient (인도) 7개 신제품 파트너십 (5월 발표)도 영역 확장 신호

#### 가설 3: 그리드/SST 신규 영역
- **EPFL 250kW SST**(5/5 컨콜 언급) — 3.3kV AC → 800V DC 직접 변환
- 데이터센터 **상위 그리드 단(MV/HV)** 진입 → AI DC 전체 전력 체인 풀스택 커버리지
- Eaton, Schneider, ABB 등 그리드 OEM과의 백엔드 협력 가능성

### 4.5 백로그 vs 매출 변환 일정표 (추정)

| 연도 | 매출 추정 (컨센서스) | 누적 백로그 소진 |
|---|---|---|
| 2025 (실적) | $46M | $300M 잔존 |
| 2026E | $41M | $450M 잔존 |
| 2027E | $150~200M | $1.0B 소진 (전체의 41%) |
| 2028E | $300~400M | $1.5B 소진 (62%) |
| 2029E | $500~700M | $2.0B 소진 (83%) |
| 2030E | $700~1,000M | $2.4B 완납 |

→ **2027~2030 연평균 50~60% 성장** 가정과 정합. 회사 가이던스 "2030 SAM $3.5B at 60%+ CAGR"과 부합.

### 4.6 백로그의 한계 — 3가지 주의

1. **취소·축소 가능성** — 디자인윈은 법적 구속력 없는 약속. 고객 제품 출시 지연·취소 시 함께 증발.
2. **타이밍 미스매치** — $2.4B 누적이지만 매출 인식 시점은 제품 출시·양산 ramp에 좌우.
3. **회사 자체 추정치** — 외부 감사·검증 없음. Innoscience 등 경쟁사도 유사하게 큰 숫자 발표 사례 있음.

---

## 5. ATM $122M 증자 — 희석률·런웨이·시그널 (신규)

### 5.1 거래 개요

| 항목 | 내용 |
|---|---|
| 프로그램 발표 | 미공개(소급 추정 2025년 말~2026년 초 등록) |
| 프로그램 한도 | $125.0M |
| **완납 발표일** | **2026-05-12** (8-K) |
| 신주 발행 | **6,529,666주** (Class A 보통주) |
| **평균 매각가** | **~$18.70/주** (역산) |
| 매각 기간 | 약 1~3개월 (ATM은 시장 분산 매각) |
| **순조달** | **$122.0M** (수수료·비용 차감 후) |
| 매각 에이전트 | Craig-Hallum Capital Group + UBS Securities |
| 자금 사용처 | 8-K에 명시 없음 (일반 운전자본 + 성장 자금 추정) |

### 5.2 ATM이란? (용어 박스)

> **🔍 용어 박스 — At-the-Market Offering (ATM)**
>
> 회사가 **사전 등록된 한도 내에서, 시장 시세대로 신주를 분산 매각**하는 방식. 전통 유상증자(공모가 할인 발행) 대비 장단점:
>
> **장점**:
> - 시장가 매각 → 기존 주주 가치 보호 (할인율 0~3%)
> - 분산 매각 → 단일 공시 충격 최소화
> - 한도 내 유연 매각 → 시장 상황 우호적일 때 집중
>
> **단점**:
> - 상시 잠재 매도 압력 — "주가가 오르면 회사가 매도하지 않을까" 우려
> - 완납 공시 시점 시장 충격 (예: NVTS 5/12 장중 -10%)
>
> 비유: **연예인 콘서트 티켓을 한 번에 다 풀지 않고, 시즌 동안 시장가 따라 천천히 풀어 파는 방식**. 단점은 콘서트 종료 직전 "마지막 티켓"이 나올 때마다 시장이 출렁이는 것.

### 5.3 희석률 분석

| 항목 | 발행 전 (4/30 기준) | 발행 후 (5/12 기준) | 변동 |
|---|---|---|---|
| 발행주식 수 | ~188.0M | ~194.5M | +3.5% |
| 시가총액 (5/13 종가 $21.17) | $3.98B | **$4.12B** | +3.5% |
| EPS (Q2E -$0.04 가정) | -$0.04 | **-$0.0385** | 1.2% 희석 (분모 ↑) |

→ **희석률 3.5%는 v1 우려(20~30% 희석) 대비 매우 경미**. 시장가 매각 + 단일 분기 완납으로 충격 최소화.

### 5.4 현금 포지션 변동

| 시점 | 현금 + 단기투자 | 변동 |
|---|---|---|
| FYE 2025 (12/31) | $236.9M | - |
| Q1 2026말 (3/31) | $221.0M | -$15.9M (Q1 Cash Burn) |
| **5/12 ATM 완납 후 (추정)** | **~$343M** | +$122M |
| Q2E말 (6/30, OpEx 차감 추정) | ~$330M | -$13M (Q2 Cash Burn) |

### 5.5 런웨이 재계산

| 시나리오 | 분기 Cash Burn 가정 | 분기수 | 개월 |
|---|---|---|---|
| 보수 (현재 수준) | $15M | **22분기** | **66개월 = 5.5년** |
| 중간 (OpEx 점진 확대) | $20M | 17분기 | 50개월 = 4.2년 |
| 공격 (R&D 가속 시) | $30M | 11분기 | **33개월 = 2.75년** |

→ **공격 시나리오에서도 2.75년 런웨이** — 2027 Kyber 양산까지 충분. **추가 증자 없이 BEP 도달 가능성**이 v1 대비 크게 상승.

### 5.6 ATM 완납의 3가지 시그널

#### 시그널 1: 회사가 "현재 주가가 자금 조달 적정선"이라고 판단
- 평균 $18.70 매각은 4~5월 평균가 $17~19와 일치 — 회사가 가격 고점에 매각한 것은 아니지만, **저가 매각도 회피**
- 만약 회사가 "주가가 더 오를 것"이라 봤다면 매각 지연했을 것 → **단기 추가 모멘텀에 보수적** 시각

#### 시그널 2: 디자인윈 백로그가 자금 수요 동인
- $2.4B 백로그 양산 ramp에는 ① 재고 확보 ② 추가 R&D ③ 운전자본 필요
- ATM 자금은 이 ramp 자본 — **공격적 자본 배치**

#### 시그널 3: M&A 가능성 제한적
- ATM은 일반 운전자본 조달, **대규모 인수합병 자금원으로는 부족** ($122M)
- 만약 NVTS가 인수당하는 측이라면 ATM 매각 안 했을 가능성 → **장기 독립경영 의지 시그널**

---

## 6. 제품 라인업 2배 확장 (20kW PDB + 250kW SST) (신규)

v1에서 GTC 2026의 2종 제품(800V-6V PDB + 10kW 800V-50V DC-DC)을 분석했다. v2 시점에는 **추가로 2종**이 공개되어 총 4종으로 확장.

### 6.1 신규 제품 1: 20kW 800V-6V GaNFast PDB (4월 추가 발표)

| 항목 | v1 (4/28) — 5kW급 PDB | v2 (5/14) — **20kW 신모델** |
|---|---|---|
| 출력 전력 | 5kW급 (10kW DC-DC와는 별개) | **20kW** (단일 보드) |
| 피크 효율 | 96.5% | **97.5%** |
| 스위칭 주파수 | 1 MHz | 1 MHz 유지 |
| 전력 밀도 | 2,100 W/in³ | 2,100 W/in³ 유지 |
| 1차측 FET | 16x 650V GaNFast | 16x 650V GaNFast (DFN8x8) |
| 2차측 | 25V Si MOSFET | 25V Si MOSFET (center-tapped) |
| 타깃 랙 | MGX | **Kyber 랙 (Rubin Ultra GPU)** |

→ 4배 전력 + 1%p 효율 향상 → 단일 보드로 **GPU 클러스터 직접 공급** 가능. v1의 5kW급은 "데모 수준"이었다면 v2 20kW는 **양산 지향 플랫폼**.

### 6.2 신규 제품 2: 250kW SiC 솔리드스테이트 트랜스포머 (SST, EPFL 협력, 3월 발표 → 5/5 컨콜 강조)

| 항목 | 스펙 |
|---|---|
| 출력 전력 | **250 kW** |
| 입력/출력 | **3.3 kV AC → 800V DC** (단일 스테이지) |
| 토폴로지 | 모듈러 브릿지 정류 SST |
| GaN/SiC 구성 | **GeneSiC 3300V (UHV) + 1200V (HV) SiC MOSFET** (TAP 구조) |
| 협력 | **EPFL 전력전자 연구소** (Power Electronics Lab) |
| 발표 | 2026-03-04 (사전공시) → 2026-03-22~26 APEC 2026 데모 → 5/5 컨콜 강조 |
| 의의 | **데이터센터 상위 그리드 단(MV/HV) 진입** — 기존 변압기 대체 |

### 6.3 SST의 전략적 의의 — 데이터센터 풀스택 커버리지

#### 기존 데이터센터 전력 체인
```
[그리드 13.8kV AC]
   ↓ 저주파 변압기 (Liquid-filled, 무겁고 비효율)
[480V AC]
   ↓ AC-DC 변환 + 48V IBC
[48V DC]
   ↓ 48V→1V VRM
[GPU 1V DC]
```

#### NVIDIA 800V HVDC + Navitas 풀스택 비전
```
[그리드 13.8kV AC]
   ↓ Navitas SST 250kW (NEW)
[800V DC]
   ↓ Navitas 20kW PDB
[6V DC]
   ↓ Navitas 1V VRM (개발 중)
[GPU 1V DC]
```

→ **변환 단수 5단 → 3단으로 축소**, 손실 -30%, 풋프린트 -50%, 무게 -70% 추정.

### 6.4 제품 라인업 매트릭스 (v2 기준)

| 카테고리 | 제품명 | 출력 | 효율 | 발표 시점 | 양산 |
|---|---|---|---|---|---|
| 모듈/디스크리트 | GaNFast IC | <0.5kW | 95% | 2014~ | 양산 중 |
| 모듈/디스크리트 | GaNSafe | <2kW | 96% | 2024 | 양산 중 |
| 모듈/디스크리트 | Bidirectional GaN | <5kW | 97% | 2025 | 샘플링 |
| 데이터센터 보드 | **800V-6V PDB (20kW)** | **20kW** | **97.5%** | 2026-03 (GTC) | 평가 중 |
| 데이터센터 모듈 | 10kW 800V-50V DC-DC | 10kW | 98.5% | 2026-02 | 평가 중 |
| **그리드 SST** | **250kW SiC SST (EPFL)** | **250kW** | **>98%** | **2026-03 (APEC)** | **데모 단계** |

→ **6개 제품 라인 중 3개가 2025~2026 신규** — 회사 제품 포트폴리오 50% 갱신.

### 6.5 경쟁사 800V 진척 비교 (v2 갱신)

| 경쟁사 | 800V 진입 | GTC 2026 / APEC 2026 공개 | Navitas 대비 |
|---|---|---|---|
| **Infineon** | 2025-05 NVIDIA 공동개발 | 5kW급 800V 효율 데모 | 규모 압도, 풀라인 미완성 |
| **TI (Texas Instruments)** | **2026-03-16 완전 800V 아키텍처 발표** | 모든 단계(grid→GPU) 커버 주장 | **가장 강력한 경쟁자, 8조원+ 자본** |
| **onsemi** | NVIDIA 800VDC 협력 + Innoscience MoU | 저전압(40~200V) 집중 | 그리드 SST 미공개 |
| **Innoscience** | onsemi MoU + 자체 GaN IDM | 고전압 직접 데모 없음 | 가격 공세 지속 |
| **Vicor** | factorized power 전통 | 새 800V 데모 미확인 | 아키텍처 다름 |
| **Power Integrations** | InnoSwitch 시리즈 | 800V 풀스택 미공개 | 디스크리트 강점 |
| **Renesas / Rohm / ST / AOS / MPS / Richtek / ADI** | NVIDIA 실리콘 파트너 리스트 | 동급 250kW SST 미공개 | 부분 영역 강점 |

→ **TI가 가장 명확한 경쟁자**로 부상 — 3/16 발표로 풀스택 800V 라인업 공개. 단, 일반적으로 **소형 전문 업체가 신기술 선행, 대형 업체가 추격**하는 반도체 산업 패턴에서 Navitas는 1~2년 선행 가능.

---

## 7. 애널리스트 PT 일제 상향 + 컨센서스 재구성 (신규)

### 7.1 5/6 단일 일자 3사 동시 상향

| 애널리스트 | 이전 PT | 신규 PT | 변동 | 등급 |
|---|---|---|---|---|
| **Needham (Bolton)** | $13.00 (2025-11) | **$21.00** | **+62%** | Buy 유지 |
| **Baird** | $9.00 | **$20.00** | **+122%** | **Outperform 유지** |
| **Rosenblatt (Cassidy)** | $7.00 | **$13.00** | **+86%** | Neutral 유지 |
| Craig-Hallum | (미공개, 기존 Hold) | (미상향) | - | Hold |

### 7.2 평균 PT 추이

| 시점 | 평균 PT (4사 합산) | 비고 |
|---|---|---|
| 2025-11 (v1 시점 추정) | $8.15 | Needham만 $13, 나머지 $5~9 |
| 2026-04-28 (v1 작성) | $8.64 | 소폭 상향 |
| **2026-05-06 (v2 시점)** | **~$17.0 (재산정)** | 3사 일제 상향 |

→ **단일 분기에 컨센서스 +100%** — 이는 일반적인 분기 실적 후 PT 상향(10~30%)을 크게 넘는 **거의 V자형 재평가**.

### 7.3 시장가 vs 컨센서스 프리미엄 변동

| 시점 | 주가 | 평균 PT | 프리미엄 |
|---|---|---|---|
| 2026-04-21 (v1 직전 정점) | $15.66 | $8.64 | **+81%** |
| 2026-04-28 (v1 작성) | $15+ | $8.15 | **+84%** |
| **2026-05-13 (v2)** | **$21.17** | **~$17.0** | **+24%** |

→ 시장가가 컨센서스를 추월하는 구조는 동일하나 **프리미엄이 +84% → +24%로 정상화**. v1에서 우려한 **"과열 위험"이 컨센서스 재평가로 해소** 진행 중.

### 7.4 PT 상향의 3대 근거 (각사 리포트 요약)

#### Needham (Bolton, PT $21)
- "디자인윈 백로그 $2.4B가 2027~2030 매출 가시성을 제공"
- "20kW PDB + 10kW DC-DC + 250kW SST 라인업이 풀스택 GaN+SiC 경쟁우위"
- "ATM 자금으로 양산 ramp 자본 확보 → 추가 증자 리스크 해소"

#### Baird (가장 적극, PT $20, Outperform)
- "Navitas가 800V HVDC 풀스택 공급자 후보군에서 **1순위**"
- "EV/Sales 30~40x는 고평가지만, 디자인윈 백로그 vs 시총 비율(약 0.6x)은 **합리적**"
- "Q2~Q4 가이던스 상향 가능성 + 2027 NVIDIA 매출 본격화 선반영"

#### Rosenblatt (Cassidy, PT $13, Neutral 유지)
- "디자인윈 백로그는 인상적이나 **전환율 불확실성** 잔존"
- "TI 등 대형 경쟁자 진입으로 마진 압박 가능성"
- "현재가 $21 vs 적정가 $13 → **38% 하방 리스크**"

### 7.5 컨센서스 재구성 — 2026~2027 매출 전망

| 연도 | v1 시점 컨센서스 | v2 시점 컨센서스 | 변동 |
|---|---|---|---|
| 2026E 매출 | $50M | **$41.3M** | -17% (실적 부진 반영) |
| 2027E 매출 | $120M | $150~200M (추정) | +30~67% |
| 2028E 매출 | $250M | $300~400M (추정) | +20~60% |
| 2026E EPS | -$0.18 | -$0.18 | 유지 |

→ **2026은 하향, 2027~은 상향** — **"단기 부진은 의도된 모바일 철수, 장기는 AI DC 가속"** 시나리오의 컨센서스 채택.

---

## 8. 밸류에이션 v2 — EV/Sales 재계산 + 시나리오 갱신 (신규)

### 8.1 v2 시점 멀티플 매트릭스 (2026-05-13 기준)

| 종목 | 시가총액 | EV | Forward P/E (2026E) | EV/Sales (2026E) | EV/Sales (2027E) | P/B | 현재 위치 |
|---|---|---|---|---|---|---|---|
| **Navitas (NVTS)** | **$4.12B** | **$3.78B** (현금 $343M 차감) | **n/a (적자)** | **~92x** ($41M) | **~25x** ($150M 가정) | ~5x | **5년 밴드 최상단** |
| Power Integrations (POWI) | ~$4.4B | ~$4.0B | 35-40x | ~9x | ~8x | ~5x | 5년 평균 부근 |
| Wolfspeed (WOLF) | ~$0.8B | ~$2.5B (부채 多) | n/a | ~3x | ~2.5x | ~1x | 5년 밴드 하단 |
| onsemi (ON) | ~$25B | ~$24B | 18-22x | ~3.5x | ~3x | ~2.5x | 5년 평균 부근 |
| Infineon (IFX) | ~€55B | ~€52B | 22-25x | ~3x | ~2.7x | ~2x | 5년 평균 부근 |
| TI (Texas Instruments) | ~$160B | ~$155B | 25-28x | ~7x | ~6.5x | ~10x | 평균 부근 |

> **핵심**: Navitas EV/Sales는 동종 그룹 중 **2027E 기준 25x로 onsemi/Infineon 대비 8~10배 프리미엄**. 단, **2026E 92x → 2027E 25x로 4배 압축** — 매출 가속 시 멀티플 정상화 빠를 것.

### 8.2 EV/Sales 시계열 (NVTS 단독)

| 시점 | 시가총액 | EV/Sales (Forward) |
|---|---|---|
| 2024 (NVIDIA 발표 전) | $0.4B | ~5x |
| 2025-05 (NVIDIA 발표 직후) | $1.5B | ~30x |
| 2026-04 (v1) | $2.9B | ~58x (2026E $50M 기준) |
| **2026-05-13 (v2)** | **$4.1B** | **~92x (2026E $41M)** / **25x (2027E $150M)** |

### 8.3 백로그/시총 비율 — 신규 잣대

> **이 비율의 의미**: 동종 적자 성장주에서 **"백로그가 시총 대비 얼마나 큰가"** 를 보는 잣대. **>1.0이면 백로그가 시총을 정당화**, <0.5면 백로그 대비 고평가.

| 항목 | 값 |
|---|---|
| 디자인윈 백로그 | **$2.4B** |
| 시가총액 | $4.12B |
| **백로그/시총 비율** | **0.58x** |

→ 0.58x는 **"백로그가 시총의 절반을 정당화"** 수준. 백로그 전환율 50% 가정 시 **$1.2B 누적 매출 → 평균 매출 인식 기간 4년 → 연 $300M 매출 → P/S 14x 정상화**.

### 8.4 Bull / Base / Bear 시나리오 v2 (갱신)

| 시나리오 | 핵심 가정 | 2027E 매출 | 2027E 적용 P/S | 12개월 함의 |
|---|---|---|---|---|
| **🟢 Bull** | ① NVIDIA Kyber 2027 양산 시작 + Microsoft·Google 추가 디자인윈, ② $2.4B 백로그 50%+ 전환율 양산화, ③ Non-GAAP BEP 2027 Q3 도달, ④ TI 추격 지연 | **$250M** | **25x** = **$6.25B 시총** | **주당 ~$32** (+51% 상방) |
| **🟡 Base** | ① Q2~Q4 가이던스 적중, ② $2.4B 백로그 40% 전환, ③ NVIDIA 매출 2027 $100M 적중, ④ 추가 ATM 없음 | $150M | 20x = $3.0B 시총 | **주당 ~$15** (-29% 하방) |
| **🔴 Bear** | ① NVIDIA Kyber 양산 6개월~1년 지연, ② TI/Infineon 가격 공세, ③ 백로그 전환율 25%로 하향, ④ 2027 Q1 추가 ATM $100M | $90M | 10x = $0.9B 시총 | **주당 ~$4.5** (-79% 하방) |

> **확률 가중**: Bull 30% × $32 + Base 50% × $15 + Bear 20% × $4.5 = **기댓값 $18 → 현재가 $21.17 대비 -15%**.

### 8.5 v1 → v2 시나리오 비교

| 시나리오 | v1 (4/28) | v2 (5/14) | 변동 |
|---|---|---|---|
| Bull 12개월 | $30 (+90%) | **$32 (+51%)** | 주당 가치 ↑, 상승률 ↓ (출발선 상승) |
| Base 12개월 | $15 (±10%) | **$15 (-29%)** | 주당 가치 동일, 출발선 상승 |
| Bear 12개월 | $5 (-65%) | **$4.5 (-79%)** | 주당 가치 ↓ (ATM 희석 반영) |
| 기댓값 | ~$15 | **~$18** | 기댓값 자체는 +20% |

→ **시장가 vs 기댓값 갭은 v1에서 -10%, v2에서 -15%** — 약간 더 벌어졌지만, **이는 컨센서스가 추격 중이고 펀더멘털 가속 시 갭이 빠르게 좁아질 수 있는 구간**.

### 8.6 ⚠️ v2 멀티플 사용 시 추가 주의

- ATM 후 발행주식 ~194.5M 기준으로 EPS·주당가치 재계산 필요
- 2027E 매출 컨센서스는 **회사 가이던스 + Needham/Baird 추정의 평균** — 30% 오차 범위
- **EV/Sales 25x는 동종 평균(3~5x) 대비 5~8배 프리미엄** — 정당화 변수: ① 백로그 전환 가시화, ② NVIDIA Kyber 매출 적중, ③ 추가 하이퍼스케일러
- TI의 800V 풀스택 진입으로 **장기 마진 압박 가능성** (BoM 단가 -10~20% 시나리오)

---

## 9. 5월 주가 모멘텀 해부 (신규)

### 9.1 5월 일자별 주가 추이 (추정 + 공개치)

| 날짜 | 시가 | 고가 | 저가 | 종가 | 주요 이벤트 |
|---|---|---|---|---|---|
| 5/1 (금) | $14.5 | $15.0 | $14.2 | $14.8 | - |
| 5/4 (월) | $14.8 | $15.5 | $14.5 | $15.2 | Baird 주말 사전 노트 |
| **5/5 (화)** | $15.2 | $16.0 | $14.8 | $15.5 | **Q1 실적 발표 (장 마감 후)** |
| 5/6 (수) | $17.5 | $19.0 | $17.0 | **$18.8** (+21%) | **3사 PT 일제 상향** |
| 5/7 (목) | $18.8 | $20.5 | $18.5 | $19.5 | 추가 매수세 |
| 5/8 (금) | $19.5 | $21.0 | $19.0 | $20.2 | 주말 모멘텀 |
| **5/11 (월)** | $20.2 | $22.5 | $20.0 | **~$21.5** (+25% 주간) | **IBTimes·Motley Fool 헤드라인** |
| **5/12 (화)** | $21.72 | $22.00 | $18.78 | **$19.25 (-10.5%)** | **ATM 완납 8-K 공시** |
| **5/13 (수)** | $19.25 | $21.30 | $19.05 | **$21.17** (+9.97%) | **희석 우려 해소** |

> 정확한 시·종가는 추정. 핵심 흐름만 참조.

### 9.2 5월 12일 -10% 변동성의 4가지 해석

#### 해석 1: ATM 완납이 매도 신호로 인식됨
- "회사가 고점에서 매도 완료" → "주가 추가 상승 동력 약화"
- 단기 트레이더 차익실현 트리거

#### 해석 2: 희석 우려 즉시 반영
- 6.53M 신주 (3.5%) 일거 시장 등장 → 수급 부담
- 단, 분산 매각이므로 실제 신주는 이미 1~3개월에 걸쳐 풀려 있었을 가능성 → **이미 반영된 희석**

#### 해석 3: 컨센서스 추격 완료 후 단기 과열
- 5/5~5/11 단일 주에 +30% → 단기 RSI 과열 (70 이상)
- 차익실현 + 추가 모멘텀 부재 시 자연 조정

#### 해석 4: 시장의 검증 요구
- "실적·백로그·ATM 모두 좋다 → 그렇다면 **다음 카탈리스트는?**"
- Q2 실적까지 **약 2.5개월 공백** → 단기 트리거 부재

### 9.3 5/13 반등의 의미

- 종가 $21.17은 5/5 실적 직전 $15.5 대비 **+36% 누적**
- ATM 후 즉시 V자 반등 → 시장이 **"$122M 신규 자본이 $2.4B 백로그 ramp에 충분"** 으로 판단
- 단기 변동성은 유지되나 **장기 추세는 상승 베이스 형성**

### 9.4 변동성 지표 (v1 → v2)

| 지표 | v1 (4/28) | v2 (5/14) |
|---|---|---|
| 30일 평균 일중 변동성 | ±5~8% | ±6~10% |
| 5월 단일일 최대 하락 | -8% (4/22) | **-10.5% (5/12)** |
| 5월 단일일 최대 상승 | +18% (4/21) | +21% (5/6) |
| RSI(14) | 68 | 62 (조정 후) |

→ 변동성은 v1 대비 소폭 확대되었으나 **RSI는 정상 영역으로 복귀** (70 이상 과열 → 60대).

### 9.5 단기 매매 관점 vs 중장기 보유 관점

| 관점 | 권고 | 근거 |
|---|---|---|
| **단기 (1~3개월)** | **관망** | 컨센서스 따라잡기 완료, Q2까지 카탈리스트 공백 |
| **중기 (6~12개월)** | **유지/소분 추가** | 2027 Kyber 양산 선반영 + 백로그 가시화 진행 |
| **장기 (2~3년)** | **포트 2~5% 보유** | $2.4B 백로그 + NVIDIA 풀스택 베팅 |

---

## 10. v1 대비 리스크 매트릭스 갱신

| 리스크 | v1 (4/28) | v2 (5/14) | 변동 |
|---|---|---|---|
| **NVIDIA 매출 타임라인 지연** | 🔴 High | 🔴 High | 유지 (Kyber 2027 시작 여전히 미확정) |
| **현금 소진 → 증자 희석** | 🔴 High | 🟡 Medium → 🟢 Low | **해소** (ATM 완납 + 런웨이 3배 연장) |
| **컨센서스 vs 시장가 갭** | 🔴 High (+90% 프리미엄) | 🟡 Medium (+24% 프리미엄) | **개선** |
| **중국 스마트폰 OEM 의존** | 🟠 Med-High | 🟡 Medium | **완화** (모바일 비중 의도적 축소) |
| **Fab-lite 공급망 (TSMC/GF/PSMC)** | 🟠 Med-High | 🟠 Med-High | 유지 |
| **SiC/Si 슈퍼정션 대체** | 🟡 Medium | 🟡 Medium | 유지 |
| **거시 반도체 사이클** | 🟡 Medium | 🟡 Medium | 유지 |
| **TI 등 대형 경쟁자 진입** | 🟡 Medium | 🔴 High | **악화** (TI 3/16 풀스택 발표 + 자본 5000배 우위) |
| **백로그 전환율 불확실성** | (미식별) | 🟠 Med-High | **신규 위험** (백로그 5배 점프의 신뢰성 검증 필요) |
| **단기 차익실현 변동성** | (미식별) | 🟡 Medium | **신규** (RSI 과열 → 조정 → 회복 사이클) |

### 10.1 v2 리스크 종합

**해소된 리스크 2종**: 현금 소진, 컨센서스 갭
**악화된 리스크 1종**: TI 경쟁
**신규 리스크 2종**: 백로그 전환율, 단기 변동성

→ **순효과**: 펀더멘털 리스크는 완화, 시장·경쟁 리스크는 확대. 전체적으로는 **약간 개선** 평가.

---

## 11. 5/5 컨콜에서 답하지 않은 4가지 (신규)

> v1에서 트래킹 포인트로 지목했던 4가지가 5/5 컨콜에서 어떻게 답변되었는지 점검. **4개 중 0개 완전 해소** — 즉 Q2 실적이 더 중요해짐.

### 미해소 1: 데이터센터 매출 분리 공시
- **현재 상태**: "고전력 4개 세그먼트 합산"으로만 공개
- **시장이 원하는 것**: AI DC 단독 매출 (분기별)
- **다음 갱신 시점**: Q2 2026 실적 (예상 8월 초)
- **확률**: 50/50 — 회사가 경쟁사 노출 우려로 거부 가능

### 미해소 2: NVIDIA 외 티어-1 ODM 명시
- **현재 상태**: "OEM/ODM/하이퍼스케일러 협력" 일반화
- **시장이 원하는 것**: **Foxconn, Quanta, Wistron, Inventec** 등 명시
- **다음 갱신 시점**: COMPUTEX 2026 (2026-06, Taipei) — 대만 ODM 행사
- **확률**: COMPUTEX에서 부분 공개 가능성 60%

### 미해소 3: NVIDIA Kyber 매출 시작 시점 + 랙당 달러 콘텐츠
- **현재 상태**: "2027 본격화" 정도
- **시장이 원하는 것**: ① 첫 매출 인식 분기, ② 랙당 $ 콘텐츠, ③ 2027~2030 누적 매출 가이드
- **다음 갱신 시점**: NVIDIA GTC 2026 후속 또는 Q3 2026 실적
- **확률**: NVIDIA 측 발표가 선행될 가능성

### 미해소 4: M&A 시나리오
- **현재 상태**: 컨콜 직접 질의 없음
- **시장이 원하는 것**: Infineon·onsemi·TI 인수 후보 vs 독립 경영 방침
- **다음 갱신 시점**: 미정 (ATM 완납으로 자본 조달 자체 능력 입증)
- **확률**: 독립 경영 의지 강화 시그널

---

## 12. Q2 2026 트래킹 체크리스트 (신규)

> Q2 실적 발표는 **2026년 8월 초 예상**. 약 11주 후. 다음 12개 항목을 분기 동안 모니터링.

### A. 회사 공시 (월 1~2회 발생 예상)

- [ ] **신규 디자인윈 보도자료** — NVIDIA 외 이름 명시 여부
- [ ] **티어-1 ODM 파트너십 발표** — Foxconn/Quanta/Wistron
- [ ] **COMPUTEX 2026 (6월) 부스 발표** — 신제품 + 고객 명시
- [ ] **하반기 SK하이닉스·삼성 HBM 협력 가능성** — 한국 시장 진입

### B. 재무 시그널

- [ ] **Q2 매출 가이던스 $10.0M ±0.5M 적중 여부**
- [ ] **Non-GAAP GM 39.25% ±75bps 적중 여부**
- [ ] **분기 Cash Burn $13~15M 유지 (확대 시 적신호)**
- [ ] **추가 ATM 등록 여부** (8-K 또는 S-3 모니터링)

### C. 외부 검증 시그널

- [ ] **추가 애널리스트 PT 상향** (Craig-Hallum Hold 유지 vs 상향)
- [ ] **NVIDIA Kyber 매출 시작 공식 발표** (NVIDIA 측)
- [ ] **TI/Infineon 800V 양산 시점 공개** — 경쟁 강도 측정
- [ ] **YOLE Group·Omdia 등 시장 조사 데이터 — GaN 모듈 시장 점유율** Q2 갱신

### D. 거버넌스

- [ ] **2026년 6월 주주총회** — 이사 재선임·보상안·M&A 권한 변동
- [ ] **Fischer 이사 첫 분기 활동** — Compensation 위원회 변화

---

## 13. 종합 결론 + 포지션 권고 v2

### 13.1 v1 → v2 핵심 변화 1줄 요약

> **"테마 과열 + 실적 미달 + 증자 임박" → "테마 유지 + 실적 첫 적중 + 증자 완납 + 컨센서스 추격"**

### 13.2 v2 시점 종합 평가

| 영역 | v1 평가 | v2 평가 | 변동 |
|---|---|---|---|
| 펀더멘털 | 🔴 부진 (매출 -45%) | 🟡 회복 초기 (QoQ +18%, 가이던스 적중) | **개선** |
| 자본 구조 | 🔴 증자 임박 | 🟢 ATM 완납, 런웨이 18~24개월 | **크게 개선** |
| 디자인윈 | 🟡 $450M | 🟢 $2.4B | **크게 개선** |
| 밸류에이션 | 🔴 +90% 프리미엄 | 🟡 +24% 프리미엄 | **개선** |
| 경쟁 환경 | 🟡 Infineon·Wolfspeed 압박 | 🔴 + TI 풀스택 진입 | **악화** |
| NVIDIA 노출 | 🟢 매우 강함 | 🟢 매우 강함 | **유지** |
| 변동성 | 🟡 ±5~8% | 🟠 ±6~10% (ATM 충격) | **소폭 악화** |

→ **종합**: 7개 중 4개 개선, 1개 악화, 2개 유지. **약 60% 호전, 14% 악화** — 펀더멘털 베이스 확대 평가.

### 13.3 포지션 권고 v2

| 투자자 유형 | 권고 | 비중 | 진입 가격 | 보유 기간 |
|---|---|---|---|---|
| **공격형** | **유지/소분 추가** | 3~5% | 시장가 OK ($21~24) | 2~3년 (Kyber 양산 사이클) |
| **균형형** | **유지** | 2~3% | 조정 시 분할 ($18~20) | 1~2년 (Q2~Q4 확인 후) |
| **보수형** | **신규 진입 보류** | 0~1% | 추가 조정 시 ($15 이하) | Q4 2026 이후 |

### 13.4 핵심 매도 시그널 (감시 트리거)

1. **Q2 매출 가이던스 미달** ($9.0M 이하) → 즉시 50% 축소
2. **추가 ATM 등록** → 발행주식 5% 이상 추가 희석 시 30% 축소
3. **NVIDIA Kyber 양산 6개월 이상 지연 발표** → 50% 축소
4. **TI/Infineon이 동급 800V 풀스택 양산 진입** → 25% 축소
5. **컨센서스 PT 평균 $25 돌파 + 시장가 $30 돌파** → 차익실현 50%

### 13.5 핵심 매수 가속 시그널

1. **NVIDIA가 Navitas를 공식 디자인 파트너로 명시 (Kyber 데이터시트)** → 추가 매수
2. **Foxconn/Quanta 등 티어-1 ODM 디자인윈 명시 발표** → 추가 매수
3. **하이퍼스케일러(Microsoft/Google/AWS) 자체 800V 아키텍처 Navitas 채택** → 비중 확대
4. **Q2 실적이 가이던스 $10M 상회 + Q3 가이던스 $12M+ 제시** → 추가 매수
5. **백로그 $2.4B → $4B 추가 점프** → 비중 확대

### 13.6 1문장 결론

> NVTS는 **v1에서 지목한 펀더멘털 리스크 2종(증자·실적)을 해소하고 디자인윈 백로그 5배 확장으로 베이스를 강화**했으나, **여전히 EV/Sales 25~40x의 옵션 가격대**에 있다. 2027 NVIDIA Kyber 양산까지의 **18~20개월 인내 구간**에서 **소형 옵션성 베팅(2~5%)** 으로 보유 + Q2/COMPUTEX 트래킹이 합리적.

---

## 14. 출처 (v2 신규 출처 포함)

### v1에서 인용한 핵심 출처 (그대로 유효)
- [Navitas IR — Quarterly Results](https://ir.navitassemi.com/financial-information/quarterly-results)
- [NVIDIA Selects Navitas for 800V HVDC (Navitas IR, 2025.05.21)](https://ir.navitassemi.com/news-releases/news-release-details/nvidia-selects-navitas-collaborate-next-generation-800-v-hvdc)
- [SEC EDGAR — Navitas 10-K / 10-Q](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001821742)
- [Yole Group — Power GaN 2025](https://www.yolegroup.com/product/report/power-gan-2025/)
- [NVIDIA Developer Blog — 800V HVDC Architecture](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/)

### v2 신규 출처

#### Q1 2026 실적 (5/5)
- [Navitas Semiconductor Announces First Quarter 2026 Financial Results (GlobeNewswire, 2026-05-05)](https://www.globenewswire.com/news-release/2026/05/05/3288263/0/en/Navitas-Semiconductor-Announces-First-Quarter-2026-Financial-Results.html)
- [Navitas (NVTS) Q1 2026 Earnings Transcript (Motley Fool)](https://www.fool.com/earnings/call-transcripts/2026/05/06/navitas-nvts-q1-2026-earnings-transcript/)
- [Navitas Q1 2026 Earnings Call Transcript (Seeking Alpha)](https://seekingalpha.com/article/4899053-navitas-semiconductor-corporation-nvts-q1-2026-earnings-call-transcript)
- [Full Transcript: Navitas Q1 2026 Earnings Call (Benzinga)](https://www.benzinga.com/insights/news/26/05/52309138/full-transcript-navitas-semiconductor-q1-2026-earnings-call)
- [AI data center push lifts Navitas sales 18% (StockTitan)](https://www.stocktitan.net/news/NVTS/navitas-semiconductor-announces-first-quarter-2026-financial-0o2455ucfllj.html)
- [Earnings call transcript: Navitas Q1 2026 (Investing.com)](https://ng.investing.com/news/stock-market-news/earnings-call-transcript-navitas-semiconductor-q1-2026-sees-stock-surge-on-revenue-beat-93CH-2499476)
- [Live: Navitas Q1 Earnings (24/7 Wall St.)](https://247wallst.com/investing/2026/05/05/live-navitas-semiconductor-q1-earnings-tonight-can-the-676-surge-survive-the-print/)
- [NVTS Q1-2026 Earnings Call (Alpha Spread)](https://www.alphaspread.com/security/nasdaq/nvts/investor-relations/earnings-call/q1-2026)

#### ATM $125M 증자 (5/12)
- [Navitas completes $125.0 million ATM stock program — 8-K (StockTitan)](https://www.stocktitan.net/sec-filings/NVTS/8-k-navitas-semiconductor-corp-reports-material-event-220005520de1.html)
- [Why Is Navitas Semiconductor Stock Falling On Tuesday? (Benzinga, 5/12)](https://www.benzinga.com/trading-ideas/movers/26/05/52497770/why-is-navitas-semiconductor-stock-falling-on-tuesday)
- [Is Navitas Semiconductor's New Shelf Offering Rewriting AI DC Narrative? (Simply Wall St)](https://simplywall.st/stocks/us/semiconductors/nasdaq-nvts/navitas-semiconductor/news/is-navitas-semiconductors-nvts-new-shelf-offering-quietly-re)

#### 애널리스트 PT 상향 (5/6)
- [Navitas Analyst Ratings and Price Targets (Benzinga)](https://www.benzinga.com/quote/NVTS/analyst-ratings)
- [NVTS Stock Forecast (TipRanks)](https://www.tipranks.com/stocks/nvts/forecast)
- [NVTS Stock Forecast (Public.com)](https://public.com/stocks/nvts/forecast-price-target)
- [NVTS Stock Forecast 2026 (MarketBeat)](https://www.marketbeat.com/stocks/NASDAQ/NVTS/forecast/)

#### 20kW 800V-6V PDB (GTC 2026 → 5/5 컨콜)
- [Navitas Debuts 800V-6V PDB at NVIDIA GTC 2026 (Navitas IR)](https://navitassemi.com/navitas-debuts-revolutionary-800-v-6-v-power-delivery-board-at-nvidia-gtc-2026/)
- [Navitas debuts 800V-6V DC-DC PDB (Semiconductor Today)](https://www.semiconductor-today.com/news_items/2026/mar/navitas-170326.shtml)
- [Navitas Skips 48V Bus in 800V-to-6V GaN PDB (All About Circuits)](https://www.allaboutcircuits.com/news/navitas-skips-48-v-bus-in-800-v-to-6-v-gan-pdb-for-ai-racks/)
- [Navitas 800V-6V PDB at GTC 2026 (Compound Semiconductor)](https://compoundsemiconductor.net/article/123782/Navitas_debuts_800V-6V_board_at_NVIDIA_GTC_2026)

#### 250kW SiC SST (EPFL 협력, APEC 2026)
- [Navitas, EPFL Demonstrate Novel SST Solution (GlobeNewswire, 2026-03-04)](https://www.globenewswire.com/news-release/2026/03/04/3249361/0/en/Navitas-EPFL-to-Demonstrate-Novel-Solid-State-Transformer-Solution-for-AI-Data-Center-Enabling-800-V-DC-Implementation.html)
- [Navitas and EPFL demo 250kW SST (Semiconductor Today)](https://www.semiconductor-today.com/news_items/2026/mar/navitas-epfl-050326.shtml)
- [Navitas 250kW SST at APEC 2026 (Compound Semiconductor)](https://compoundsemiconductor.net/article/123672/Navitas_and_EPFL_to_show_solid_state_transformer_at_APEC_2026)
- [Navitas 250kW SiC-Based SST at APEC 2026 (EverythingPE)](https://www.everythingpe.com/news/details/9970-navitas-and-epfl-demonstrate-250-kw-sic-based-solid-state-transformer-at-apec-2026)

#### 시장 분석·주가 모멘텀
- [Navitas Stock Explodes 25% on AI DC Demand (IBTimes, 5/11)](https://www.ibtimes.com.au/navitas-semiconductor-stock-explodes-25-surging-ai-data-center-demand-strong-q1-results-1868589)
- [Navitas Stock: Buy AI Power Surge or Sell After 400%+ Run? (IBTimes)](https://www.ibtimes.com.au/navitas-semiconductor-stock-buy-ai-power-surge-sell-after-400-2026-run-1868600)
- [Why Navitas Rallied Today (Motley Fool, 5/11)](https://www.fool.com/investing/2026/05/11/why-navitas-semiconductor-rallied-today/)
- [Navitas AI Data Center Pivot 88% YTD (TradingKey)](https://www.tradingkey.com/analysis/stocks/us-stocks/261874727-navitas-nvts-ai-data-center-semi-conductor-tradingkey)
- [Navitas 25% Surge on AI DC Demand (Rolling Out)](https://rollingout.com/2026/05/11/navitas-semiconductor-surges-25-ai-data/)
- [Navitas (NVTS): Power Bottleneck Bet (Seeking Alpha)](https://seekingalpha.com/article/4895287-navitas-power-bottleneck-bet-inside-ai-infrastructure-buildout)
- [The 'Behind-the-Scenes' AI Chip Stock (24/7 Wall St., 4/21)](https://247wallst.com/investing/2026/04/21/the-behind-the-scenes-ai-chip-stock-few-investors-know-but-every-hyperscaler-will-soon-need/)
- [Navitas When 74x Sales Multiple Meets Reality (Trefis)](https://www.trefis.com/stock/nvts/articles/597567/navitas-semiconductor-when-a-74x-sales-multiple-meets-structural-reality/2026-04-27)

#### 경쟁 환경
- [TI Unveils Complete 800VDC Power Architecture with NVIDIA (TI, 2026-03-16)](https://www.ti.com/about-ti/newsroom/news-releases/2026/2026-03-16-ti-unveils-complete-800-vdc-power-architecture-for-future-generation-ai-data-centers-with-nvidia.html)
- [Did Navitas's New AI Power Board Shift Investment Narrative? (Simply Wall St)](https://simplywall.st/stocks/us/semiconductors/nasdaq-nvts/navitas-semiconductor/news/did-navitass-new-ai-power-board-and-fischer-hire-just-shift)

---

## ⚠️ v2 주의 박스

- 본 리포트는 **2026-04-17 v1 초안 + 2026-04-28 밸류에이션 갱신 + 2026-05-14 v2** 의 누적 업데이트본.
- 일부 수치(주가 일자별, 백로그 구성)는 공개 자료 + 추정 혼합. **투자 결정 전 SEC 10-Q, 분기 컨콜 원문 재확인 필수**.
- ATM 후 발행주식 수 및 시총은 정확한 5/12 8-K + Q1 10-Q (2026-05 후순 공시) 기준으로 재검증 필요.
- **다음 v3 갱신 시점**: Q2 2026 실적 발표 (2026년 8월 초 예상). 단, COMPUTEX 2026(6월) 또는 NVIDIA GTC 후속 행사에서 중대 발표 시 조기 갱신.
- 본 리포트는 **개인 투자자/연구자용 종합 정리**이며, 투자 자문이 아닙니다. 최종 매수·매도 결정은 본인의 판단과 책임으로.
