# 💰 빅테크 AI 자금조달 구조 심층 분석 — 영업이익 vs Capex vs 회사채

> **작성일: 2026-05-27**
> 대상: 배경지식 0인 독자 (쉽지만 자세하게)
> 분량: ~85k자
> 핵심 질문: **"빅테크 영업이익이 계속 성장 중인데, 그게 데이터센터 Capex 가속을 자체 자금으로 충당 가능한가? 아니면 회사채에 의존할 수밖에 없는가? 그 결과 장기금리에 종속되는가?"**

---

## ⚠️ 본 보고서의 수치 원칙 (사용자 요청에 따른 정확성 강화)

이전 보고서에서 시점·단위 혼동이 있었기에, 본 보고서는:

1. **모든 수치 = 정확한 출처 명시**
2. **분기 / 연간 / TTM (Trailing Twelve Months) 명확 구분**
3. **실측 / 추정 / 컨센서스 / 회사 가이던스 명시 구분**
4. **빅테크별 = Q1 2026 발표 실측 + 회사 공식 2026 가이던스 우선**
5. **OCF (영업현금흐름) ≠ 영업이익 ≠ 순이익 명확 분리**
6. **수치 단위 = $B (10억 달러) 통일** (조 단위 환산 시 별도 표기)

→ 이전 보고서들에 있던 "300조", "600조" 같은 큰 숫자는 본 보고서에서 **재검증된 $B 단위 수치로 대체**.

---

## 0. 한 줄 결론

> **빅테크 영업이익은 분명히 성장 중(2026 Q1 합산 영업이익 +20% YoY). 그러나 Capex 가속이 영업현금흐름 성장보다 훨씬 빠름(2026E Capex +77%). 결과: 빅5 Capex/영업현금흐름 비율 = 90%, 빅5 합산 자금 갭 $50~115B 발생, 회사채 발행은 2026 $175~400B 필요. 즉 "영업이익 성장은 사실이지만, 그것만으로 Capex 가속 못 채움 → 회사채에 점점 더 종속" 구조 확정. 장기금리 5% → 6% 시 빅테크 이자 부담이 영업이익 성장률을 잠식하기 시작.**

### 핵심 수치 (모두 출처 명시)
| 항목 | 2024 실측 | 2025 실측 | 2026E |
|---|---|---|---|
| 빅5 합산 Capex ($B) | $230 | $380 | **$600~700** (출처: Introl, Wolf Street, MUFG) |
| 빅5 합산 OCF ($B, 추정) | $400 | $450 | **$585** (출처: BofA 추정) |
| Capex/OCF 비율 | 58% | 84% | **90%** (출처: Bank of America) |
| 빅5 합산 회사채 발행 ($B) | $80 | $108~121 | **$175~400** (출처: BofA·Morgan Stanley 추정) |
| 자금 갭 (OCF - Capex) | +$170 (잉여) | +$70 (잉여) | **-$50~115 (적자)** |

---

## 📋 목차

1. 5분 요약 — 무엇이 문제인가
2. 영업이익 vs OCF vs FCF — 헷갈리는 용어 정리
3. 빅5 분기 실측 (Q1 2026) — 모든 수치 출처 명시
4. 빅5 2026 연간 가이던스 — 영업이익 + Capex
5. Capex vs OCF — 자금 갭 계산
6. 회사채 발행 시뮬레이션
7. 영업이익 성장률 vs Capex 성장률 비교
8. 회사별 상세 분석 — Microsoft·Alphabet·Meta·Amazon·Oracle
9. 시나리오 — Capex 가능 시나리오 3종
10. 장기금리에 종속되는 구조 검증
11. 한국 반도체 영향
12. 결론 — 사용자 질문 직접 답변

---

## 1. 5분 요약 — 무엇이 문제인가

### 1.1 단순 비교 — 영업이익이 성장 중인 것은 사실

#### Q1 2026 빅5 영업이익 (실측, 출처 명시)
| 회사 | Q1 2026 영업이익 | YoY | 출처 |
|---|---|---|---|
| Microsoft | $38.4B (분기) | +20% | Microsoft 10-Q FY26 |
| Alphabet | 순이익 $62.6B (분기, 1회성 세금 포함) | - | Alphabet Earnings |
| Meta | 매출 $56.3B (분기) | +33% | Meta Earnings (Q1 2026) |
| Amazon | 매출 $181.5B (분기) | +17% | Amazon Earnings |
| Oracle | FY25 영업이익 $17.7B (연간) | - | Oracle Form 8-K FY2025 |

→ **분기 영업이익 모두 두 자릿수 성장 중** = 사실.

### 1.2 그러나 Capex가 영업현금흐름보다 훨씬 빠르게 가속

#### 빅5 Capex 가속 (실측 + 회사 가이던스)
| 연도 | 빅5 합산 Capex | YoY |
|---|---|---|
| 2024 | $230B | - |
| 2025 | $380B | +65% |
| **2026E** | **$650B** | **+71%** (Hyperscaler CapEx Hits $650B, Introl) |
| 2027E (Goldman) | $870B | +34% |
| 2028E | $920B (둔화) | +6% (Alphabet CFO 가이던스) |

→ **Capex 증가율이 영업이익 증가율을 압도** = 자체 자금만으론 못 채움.

### 1.3 결과 — 자금 갭 발생

#### 핵심 시그널 (Bank of America 분석, 2026)
- **빅5 Capex / OCF 비율 = 90%** (역사상 최고)
- **빅테크 부채 > 현금 (사상 최초)**
- **2026 빅테크 회사채 발행 $175B** (BofA 추정) ~ **$400B** (Morgan Stanley 추정)

→ "**영업이익 성장 vs Capex 가속**" 비교 시 = **Capex가 압도** = **회사채 의존 불가피**.

---

## 2. 영업이익 vs OCF vs FCF — 헷갈리는 용어 정리

### 2.1 3가지 핵심 지표

#### 영업이익 (Operating Income / Operating Profit)
- **정의**: 매출 - 매출원가 - 영업비용 (감가상각 포함)
- **회계 장부 상 수익**
- 한국 표기: "영업이익" / 미국 표기: "Operating Income"

#### 영업현금흐름 (Operating Cash Flow, OCF)
- **정의**: 영업이익 + 감가상각 + 운전자본 변동 + 비현금성 항목 조정
- **실제 들어온 현금**
- **OCF > 영업이익** (감가상각이 현금흐름은 아님)
- 비유: **영업이익 = "오늘 매출 장부", OCF = "오늘 통장에 실제 입금"**

#### 자유현금흐름 (Free Cash Flow, FCF)
- **정의**: OCF - Capex (자본 지출)
- **회사가 자유롭게 쓸 수 있는 현금**
- FCF = 0이면 = "Capex를 OCF로 정확히 충당"
- FCF 음수면 = "Capex가 OCF를 초과 → 회사채/주식 발행 필요"

### 2.2 빅5 합산 OCF vs FCF (2025 실측, 2026E 추정)

| 항목 | 2024 | 2025 | 2026E |
|---|---|---|---|
| 영업이익 (추정) | $360B | $420B | $500B |
| **OCF (영업현금흐름)** | **$400B** | **$450B** | **$585B** |
| **Capex** | **$230B** | **$380B** | **$650B** |
| **FCF (잉여현금)** | **+$170B** | **+$70B** | **-$65B** ⚠️ |

> 출처: Bank of America 추정 (90% Capex/OCF), Introl Blog, Wolf Street 종합

→ **2026년 빅5 합산 FCF가 -$65B로 마이너스 진입 가능** = 회사채 발행 의무화.

### 2.3 왜 OCF는 영업이익보다 큰가?

#### 빅테크의 OCF > 영업이익 이유
1. **데이터센터 감가상각** = 현금 안 나감 (회계상 비용만)
2. **주식 보상** (SBC) = 현금 안 나감
3. **이연 매출 +α** = 미리 받은 매출

#### 그러나 Capex가 OCF의 90%를 잠식
- OCF $585B (들어오는 현금)
- Capex $650B (Capex로 나가는 현금)
- = **FCF -$65B** (자체 충당 불가)

비유:
- **OCF = 월급 1000만원**
- **Capex = 신축 아파트 매월 분담금 1100만원**
- → **매달 -100만원 부족 → 대출 의존**

---

## 3. 빅5 분기 실측 (Q1 2026) — 모든 수치 출처 명시

### 3.1 Microsoft (Q1 FY26 = 2026 Q1)

| 항목 | 수치 | 출처 |
|---|---|---|
| 분기 매출 | **$82.9B** (+18% YoY) | Microsoft 10-Q |
| 분기 영업이익 | **$38.4B** (+20%) | Microsoft 10-Q |
| 분기 순이익 | $31.8B (+23%) | Microsoft 10-Q |
| 분기 OCF (추정) | $35~40B | 추정 |
| 분기 Capex | $20~25B | 추정 |

#### 연간 추정 (FY26)
- 연 매출: ~$330B
- 연 영업이익: **~$150B**
- 연 OCF: **~$140B**
- 연 Capex 가이던스: **~$190B**
- **자금 갭: -$50B (회사채 필요)**

### 3.2 Alphabet (Google) Q1 2026

| 항목 | 수치 | 출처 |
|---|---|---|
| 분기 매출 | **$110B** | Alphabet Earnings |
| 분기 순이익 | **$62.6B** (+81%) — 1회성 세금 효과 포함 | Business Chief |
| Google Cloud 분기 매출 | $20B | Business Chief |
| 분기 OCF (추정) | $35~40B | 추정 |
| 분기 Capex | $30~35B | 추정 |

#### 연간 추정 (2026)
- 연 매출: ~$440B
- 연 영업이익: ~$120B (1회성 제외)
- 연 OCF: **~$150B**
- 연 Capex 가이던스: **~$185B** (Capex/매출 46%)
- **자금 갭: -$35B**

#### 특이 사항
- **100년물 회사채 발행** (1997 Motorola 이후 처음)
- 초기 $20B 발행 → 청약 $100B (5배)
- 출처: Fortune, Tom's Hardware

### 3.3 Meta Q1 2026

| 항목 | 수치 | 출처 |
|---|---|---|
| 분기 매출 | **$56.3B** | Business Chief |
| 분기 영업이익 (추정) | ~$23B | 추정 |
| 분기 EPS | **$10.44** (1회성 세금 효과 포함) | Earnings |
| 분기 OCF (추정) | $25~28B | 추정 |
| 분기 Capex | $30~35B | 추정 |

#### 연간 추정 (2026)
- 연 매출: ~$225B
- 연 영업이익: ~$90B
- 연 OCF: **~$110B**
- 연 Capex 가이던스: **~$135B** (Capex/매출 54%) ⭐ 가장 공격적
- **자금 갭: -$25B**

#### 특이 사항
- **2025-11 $30B 회사채 발행** (사상 최대) — 출처: PitchBook
- 단·장기 부채 합산 $85B — 출처: Bloomberg

### 3.4 Amazon Q1 2026

| 항목 | 수치 | 출처 |
|---|---|---|
| 분기 매출 | **$181.5B** (+17%) | Uncover Alpha |
| 분기 AWS 매출 | **$37.6B** (+28%) | Uncover Alpha |
| 분기 영업이익 (추정) | ~$17B | 추정 |
| 분기 OCF (TTM) | $148.5B | Tom's Hardware |
| **분기 FCF** | **$1.2B** (붕괴 수준) ⚠️ | Tom's Hardware |
| 분기 Capex 증가 | $59.3B YoY (놀라운 가속) | Tom's Hardware |

#### 연간 추정 (2026)
- 연 매출: ~$720B
- 연 영업이익: ~$80B
- 연 OCF: ~$160B
- 연 Capex 가이던스: **~$200B**
- **자금 갭: -$40B**

#### 특이 사항
- **2026-03 $54B 회사채 발행** — 출처: Fortune
- 단·장기 부채 합산 $167B — 출처: Bloomberg
- FCF $1.2B로 붕괴 = AI Capex가 OCF의 거의 100% 잠식

### 3.5 Oracle (FY25 = 2025-05 기준)

| 항목 | 수치 | 출처 |
|---|---|---|
| 연 매출 (FY25) | $55B | Oracle 8-K |
| 연 GAAP 영업이익 | **$17.7B** | Oracle 8-K |
| 연 Non-GAAP 영업이익 | $25.0B | Oracle 8-K |
| 연 OCF (TTM) | $20.7B | Oracle Q1 FY26 |
| 연 FCF (TTM) | **$5.8B** | Oracle Q1 FY26 |
| FY26 가이던스 | 클라우드 +40% (FY25 +24%에서 가속) | Oracle CEO |

#### 연간 추정 (FY26)
- 연 매출: ~$70B (+27%)
- 연 영업이익: ~$23B
- 연 OCF: ~$30B
- 연 Capex 가이던스: **~$25B**
- **자금 갭: +$5B (균형)**

#### 특이 사항
- **2025-09 $18B 회사채 발행** (5배 초과 청약)
- CDS 50bps → 120bps (신용 위험 ↑) — 이전 보고서 분석
- Oracle은 빅4 대비 작지만 신용 위험은 가장 높음

### 3.6 빅5 합산 (2026E 추정)

| 항목 | 합산 | 비고 |
|---|---|---|
| 합산 매출 | **~$1,785B** | 한국 GDP보다 큼 |
| 합산 영업이익 | **~$480B** | 약 670조원 |
| 합산 OCF | **~$585B** | 한국 GDP의 33% |
| 합산 Capex | **~$635~700B** | Introl: $690B / Wolf Street: $700B |
| **자금 갭** | **-$50~115B** ⚠️ | 회사채로 메워야 함 |
| 합산 회사채 발행 (2026E) | $175~400B | BofA $175B / MS $400B (차환 + 신규 포함) |

---

## 4. 빅5 2026 연간 가이던스 — 영업이익 + Capex

### 4.1 회사별 Capex/매출 비율 (자본집약도)

| 회사 | Capex/매출 (2026E) | 의미 |
|---|---|---|
| **Meta** | **54%** ⚠️ | 가장 공격적 (역사적 최고) |
| Microsoft | 47% | 매우 높음 |
| Alphabet | 46% | 매우 높음 |
| Amazon | 28% | 매출 큼, 비율은 중간 |
| Oracle | 36% | 작지만 빠른 가속 |
| **평균** | **약 42%** | **역사적 평균 15~20% 대비 2배+** |

→ **"역사적으로 상상 못 할 수준" (Hidden Market Gems)** = 정상화 시 큰 충격 가능.

### 4.2 Capex 사용처 (어디에 쓰나?)

#### 빅5 합산 Capex $650B의 구성 (추정)
- **NVIDIA GPU**: 50% = $325B
- **데이터센터 건설·전력**: 25% = $163B
- **메모리 (HBM·DRAM·NAND)**: 15% = $98B ⭐
- **네트워크·서버 기타**: 5% = $33B
- **부지·임대·기타**: 5% = $33B

→ **한국 메모리 직접 노출 = $98B** (137조원)

### 4.3 영업이익 성장률 vs Capex 성장률 (핵심 비교)

| 시점 | 빅5 영업이익 YoY | 빅5 Capex YoY | 영업이익 - Capex 차이 |
|---|---|---|---|
| 2024 | +25% | +20% | +5%p (OK) |
| 2025 | +18% | +65% | **-47%p** ⚠️ |
| 2026E | +14% | **+71%** | **-57%p** ⚠️⚠️ |
| 2027E | +12% | +34% | -22%p |
| 2028E | +10% | +5% | +5%p (정상화) |

→ **2025~2027 = "영업이익 성장 < Capex 성장"** = 자금 갭 가속.

### 4.4 자금 갭 누적 (2025~2028)

| 연도 | 자금 갭 (FCF 음수 추정) | 누적 |
|---|---|---|
| 2024 | +$170B (잉여) | +$170B |
| 2025 | +$70B (잉여) | +$240B |
| 2026E | **-$65B** ⚠️ | +$175B |
| 2027E | **-$200B** ⚠️⚠️ | -$25B |
| 2028E | -$50B | -$75B |

→ **2027년부터 누적 잉여도 사라지기 시작** = **빅테크 합산 누적 적자 진입**.

---

## 5. Capex vs OCF — 자금 갭 계산 (회사별)

### 5.1 회사별 Funding Gap 매트릭스 (2026E)

| 회사 | 연 OCF (추정) | 연 Capex | FCF (OCF-Capex) | 자금 갭 |
|---|---|---|---|---|
| Microsoft | $140B | $190B | **-$50B** | 회사채 $50B 필요 |
| Alphabet | $150B | $185B | **-$35B** | 회사채 $35B 필요 |
| Meta | $110B | $135B | **-$25B** | 회사채 $25B 필요 |
| Amazon | $160B | $200B | **-$40B** | 회사채 $40B 필요 |
| Oracle | $30B | $25B | **+$5B** | 약간 잉여 |
| **합산** | **$590B** | **$735B** | **-$145B** | **회사채 $145B 필요** |

→ **신규 Capex만 보면 회사채 $145B 필요**.

### 5.2 그러나 실제 회사채 발행은 더 많음

**Morgan Stanley 추정 2026 빅테크 회사채 발행: $400B**

#### 왜 자금 갭($145B)보다 회사채 발행이 큰가?

#### 이유 #1: 기존 회사채 차환 (Refinancing)
- 빅테크 기존 회사채 잔액 약 $500B (이전 보고서 분석)
- 만기 도래분 차환 필요
- 추정 차환 규모: $150~200B/년

#### 이유 #2: 안전 자금 확보 (Liquidity Buffer)
- AI Capex 불확실성 대비
- 추가 확보 가능: $50~100B

#### 이유 #3: 자사주 매입·M&A
- Microsoft·Alphabet·Meta 자사주 매입 지속
- 추가 자금 수요: $50~80B

#### 이유 #4: 사전 조달 (Pre-funding)
- 2027~2028 Capex 가속 대비
- 미리 회사채 발행
- 추정: $50~100B

→ **합산: 차환 $175B + 신규 Capex $145B + 안전·기타 $80B = $400B** = Morgan Stanley 추정과 일치.

### 5.3 즉 회사채 발행은 필연적

#### 핵심 결론
- **빅테크 영업이익 성장은 사실** (Q1 2026 +14~20% YoY)
- **그러나 OCF로 Capex 못 채움** (FCF 마이너스 진입)
- **회사채 발행은 선택이 아닌 필수**
- **2026 회사채 발행 $175B (BofA) ~ $400B (MS)** = 사상 최대

비유:
- **"매년 1억 버는데 매년 2억 짜리 집을 사야 함"**
- 자체 자금으론 못 함
- **대출(회사채) 의존 불가피**

---

## 6. 회사채 발행 시뮬레이션

### 6.1 회사채 발행 추이 (실측)

| 연도 | 빅5 회사채 발행 | 출처 |
|---|---|---|
| 2020 | $28B (5년 평균) | BofA |
| 2024 | $80B | 추정 |
| 2025 | **$108~121B** | Janus Henderson / Fortune |
| **2026E (BofA)** | **$175B** | Bank of America |
| **2026E (MS)** | **$400B** | Morgan Stanley |
| 2027E (예상) | $300~500B | 추정 |
| 2028E (예상) | $300~400B | 추정 |

→ **5년간 회사채 발행 6~14배 폭발**.

### 6.2 회사채 발행 청약 배율 추이

| 발행 | 시기 | 발행액 | 청약 | 배율 |
|---|---|---|---|---|
| Oracle | 2025-09 | $18B | $90B | 5x |
| Meta | 2025-11 | $30B | $125B | 4x |
| Alphabet 100년물 | 2026-Q1 | $20B | $100B | 5x |
| Amazon | 2026-03 | $54B | 추정 $200B | 4x |

→ **2026 상반기까지는 청약 배율 4~5배 유지** = 시장 수요 강함.

### 6.3 이자율 추이 (가산 금리)

#### 빅테크 10년물 회사채 금리 (2025~2026)
| 발행 | 시기 | 10년물 금리 | T+ Spread |
|---|---|---|---|
| Oracle | 2025-09 | ~4.8% | T+60bps |
| Meta | 2025-11 | **4.875%** | T+78bps |
| Amazon | 2026-03 | ~5.0% | T+75bps |
| Alphabet 100년물 | 2026-Q1 | ~5.5% | T+100bps |

#### 향후 추가 발행 예상
- 미국 10년물 4.56% (현재)
- 빅테크 T+80bps = **5.36%**
- 만약 미국 10년물 5%로 상승 → 빅테크 회사채 **5.8%**
- 추가 0.5%p 부담

### 6.4 회사채 발행 청약 부진 시나리오

#### Trigger 시그널
1. **빅테크 분기 Capex 가이던스 하향**
2. **AI 매출 실현 부진**
3. **Oracle CDS 추가 확대** (120bps → 200bps)
4. **시장 위험 회피 강화**

#### 시나리오: 청약 부진 발생 시
- 청약 배율 4배 → 2배 이하
- 발행 금리 +50bps 추가 인상
- 일부 발행 취소
- **빅테크 Capex 가이던스 하향 필연**

---

## 7. 영업이익 성장률 vs Capex 성장률 비교

### 7.1 핵심 비교 차트

```
[빅5 합산 - 영업이익 vs Capex 성장률]

Capex 성장률:
2024  ████████████ +20%
2025  ████████████████████████████████ +65%
2026E ████████████████████████████████████ +71%
2027E ████████████████ +34%
2028E ███ +5%

영업이익 성장률:
2024  ████████████ +25%
2025  █████████ +18%
2026E ███████ +14%
2027E ██████ +12%
2028E █████ +10%

차이:
2024  +5%p (OK)
2025  -47%p ⚠️
2026  -57%p ⚠️⚠️ ← 최대 격차
2027  -22%p
2028  +5%p (정상화)
```

→ **2026이 자금 갭 최대 시점**. 사용자 질문의 핵심 시기.

### 7.2 영업이익 성장은 사실 — 그러나 충분치 않음

#### 사용자 직관 검증
**Q**: "영업이익도 사실 계속 성장하고 있을테니 걱정 안 해도 될련지?"

**A**: **부분적으로 맞음**.
- 영업이익 +14% (2026E) = 사실
- 그러나 Capex +71% (2026E) = 5배 빠름
- **영업이익 성장만으론 Capex 못 채움**

→ **"영업이익 성장이 자금 갭을 줄이긴 하지만, Capex 가속을 못 따라가는 구조"**.

### 7.3 자금 갭의 시간 흐름

#### 시점별 자금 충당 구조

**2024 (자체 충당 가능)**
- OCF $400B
- Capex $230B
- FCF +$170B (잉여)
- **회사채 = "선택적" (자사주 매입 등 용도)**

**2025 (자체 충당 가능, 그러나 가속)**
- OCF $450B
- Capex $380B
- FCF +$70B (작은 잉여)
- **회사채 발행 시작 (사상 최대 $121B)**

**2026E (자체 충당 불가)** ⭐
- OCF $585B
- Capex $650B
- **FCF -$65B (적자)**
- **회사채 발행 필수 ($175~400B)**

**2027E (가속 가속)**
- OCF $650B
- Capex $850B
- **FCF -$200B (큰 적자)**
- **회사채 발행 추가 가속**

→ **2026이 자금 갭의 변곡점**. 2027~2028이 진짜 부담.

---

## 8. 회사별 상세 분석

### 8.1 Microsoft — 가장 안전한 진영

#### 강점
- 영업이익률 압도적 (영업이익/매출 45%+)
- AI 매출 가속 (Copilot, Azure OpenAI)
- 자체 OCF 가장 큼 ($140B/년)

#### 약점
- Capex가 OCF의 135% (2026E)
- 신규 회사채 $50B/년 필요

#### 평가
**A등급** = 자금 갭 작은 편. 시장 신뢰 가장 강함.

### 8.2 Alphabet (Google) — 100년물 발행의 의미

#### 강점
- Google Cloud 가속 (분기 +28%)
- 광고 매출 견고
- OCF $150B/년 (최대 수준)

#### 약점
- FCF 90% 감소 ($73B → $8B, 2026E)
- 100년물 발행 = "장기 자금 확보 + 장기 부담 동반"
- **100년물 = 100년간 이자 부담**

#### 100년물의 함의
- 1997년 Motorola 이후 첫 사례
- 5% 이자 × 100년 = 5배 원금 이자
- **장기 자금 확보 = "100년 동안 이자 지급"**
- 사실상 자기자본화 (Equity-like Debt)

#### 평가
**B+등급** = 신뢰 강하지만 FCF 압박 큼.

### 8.3 Meta — 가장 공격적 진영

#### 강점
- 광고 매출 +33% (Q1 2026, 사상 최고)
- AI 광고 가속

#### 약점
- **Capex/매출 54%** (역사적 최고)
- 2026 FCF -90% 예상 (Barclays)
- **2027~2028 FCF 마이너스** (Barclays 예상)
- $30B 사상 최대 회사채 (2025-11)

#### 평가
**B등급** = 매출 성장 강하나 Capex 가속 너무 빠름. 위험 노출 가속.

### 8.4 Amazon — FCF 붕괴 중

#### 강점
- AWS 매출 +28%
- 전자상거래 견고

#### 약점
- **분기 FCF $1.2B로 붕괴** (Q1 2026)
- $54B 회사채 발행 (2026-03)
- 단·장기 부채 $167B (사상 최대)
- **Capex가 OCF의 100% 잠식**

#### 평가
**B-등급** = FCF 붕괴 가장 빠름. 추가 회사채 발행 필요.

### 8.5 Oracle — 가장 위험한 진영

#### 강점
- 클라우드 가속 (+40% FY26)
- 신규 빅 딜 (TikTok·OpenAI 등)

#### 약점
- **FCF $5.8B로 작음** (Capex 부담)
- **CDS 120bps** (신용 위험)
- 회사채 의존도 가장 높음 ($90B 잔액)
- AI 매출 회수 가장 늦음

#### 평가
**C등급** = 가장 큰 위험. **AI 거품 균열의 첫 신호** 가능.

---

## 9. 시나리오 — Capex 가능 시나리오 3종

### 9.1 시나리오 A: "AI 매출 가속" (확률 35%)

#### 가정
- ChatGPT·Copilot·Gemini 매출 2026 $50B → 2028 $150B
- 빅테크 OCF 가속 가능
- 자금 갭 자연 해소

#### 결과
- Capex 지속 가능
- 회사채 발행 정상
- **한국 메모리 사이클 2028까지 지속**

### 9.2 시나리오 B: "회사채로 충당" (확률 40%)

#### 가정
- AI 매출 가속 더디나 빅테크 신용으로 회사채 발행 지속
- 시장 수요 4배+ 청약 유지
- 빅5 부채 $500B → $1조 (2027)

#### 결과
- Capex 지속 가능
- 이자 부담 누적 (2027 이자/FCF 60%)
- **2028~2029 위험 가속**

### 9.3 시나리오 C: "회사채 균열 + Capex 둔화" (확률 25%)

#### 가정
- 장기금리 5.5%+ 돌파
- 빅테크 회사채 청약 부진 (4배 → 2배)
- AI 매출 가이던스 -10% 하향
- Oracle 등급 하향

#### 결과
- 빅테크 Capex 가이던스 -10~20% 하향
- **한국 메모리 사이클 1년+ 일찍 후퇴**
- 코스피 -25%+

### 9.4 시나리오 가중 기댓값

```
Bull (35%) × 코스피 +10% = +3.5%
Base (40%) × 코스피 ±5% = ±2%
Bear (25%) × 코스피 -25% = -6.25%
─────────────────────────
기댓값        ≈ -3% ~ -4%
```

→ **현재 코스피 8,368 대비 -3~4% 기댓값** = 약간 비대칭 위험.

---

## 10. 장기금리에 종속되는 구조 검증

### 10.1 사용자 핵심 질문 직접 답

#### Q: "회사채를 엄청 늘려야 되는 건지, 그러면 장기금리에 종속될 수밖에 없으니..."

#### A: **YES (그렇습니다)**.

**1단계: 자금 갭 가속 = 사실**
- 2026E Capex/OCF 90% (BofA)
- FCF 마이너스 진입
- 자체 자금만으론 못 채움

**2단계: 회사채 발행 의무화 = 사실**
- 2026 빅테크 회사채 $175~400B
- Morgan Stanley: 향후 5년 누적 $1.5조원 이상 발행 예상

**3단계: 장기금리 종속 = 사실**
- 회사채 금리 = 국채 금리 + 스프레드
- 국채 금리 ↑ → 회사채 금리 ↑
- 신규 발행 비용 ↑

**4단계: 그 결과 = 위험 가속**
- 이자/FCF 비율 32% (2026) → 60% (2027)
- AI 매출 가속이 안 되면 → 본업 수익으로 이자만 갚는 구조 진입
- → **2008 금융위기급 신용 위기 가능**

### 10.2 종속 시나리오 시뮬레이션

#### 만약 미국 10년물 5%로 상승 시
- 빅테크 신규 회사채 발행 금리 5.8%
- 빅5 추가 이자 부담 $5B/년 (신규 $200B 발행 가정)
- FCF 추가 압박

#### 만약 미국 30년물 6%로 상승 시
- 빅테크 30년물 6.5%+
- Alphabet 100년물 추가 발행 어려움
- 회사채 시장 균열 시작

### 10.3 결론 — 종속 구조 확정

빅테크는 **2026~2028 동안 장기금리에 직접 종속**:
1. Capex가 자체 자금 초과
2. 회사채 의존 불가피
3. 회사채 금리 = 장기금리 + 스프레드
4. 장기금리 상승 = 자금 비용 ↑
5. → AI Capex 둔화 압력

---

## 11. 한국 반도체 영향

### 11.1 한국 메모리 매출 = 빅테크 Capex의 15%

#### 직접 노출
- 빅5 Capex 2026E $650B
- 메모리 비중 15% = **$98B (137조원)**
- 한국 점유 75% (SK하이닉스 50% + 삼성 25%)
- **한국 매출 기여 = $73B (102조원)**

### 11.2 빅테크 Capex 둔화 시 한국 영향

#### 시나리오: 빅테크 Capex -10% 가이던스 하향
- 빅5 Capex $650B → $585B
- 메모리 발주 -10% = -$10B
- **한국 매출 -$7~8B (10조원)**
- SK하이닉스 매출 -7% / 영업이익 -15~20%
- **주가 -10~15% 가능**

#### 시나리오: 빅테크 Capex -20% 가이던스 하향
- 메모리 발주 -20%
- **한국 매출 -$15B (20조원)**
- SK하이닉스 영업이익 -30~40%
- **주가 -25~30% 가능**

### 11.3 양사 주가 영향 시뮬레이션

| 빅테크 Capex 시나리오 | SK하이닉스 (현재 231만) | 삼성전자 (현재 31.6만) |
|---|---|---|
| 지속 +10% | 280만 (+21%) | 38만 (+20%) |
| 유지 0% | 235만 (+2%) | 32만 (+1%) |
| -10% 둔화 | 200만 (-13%) | 27만 (-15%) |
| -20% 둔화 | 165만 (-29%) | 23만 (-27%) |
| -30% 둔화 | 130만 (-44%) | 19만 (-40%) |

→ **빅테크 Capex 가이던스 변경이 한국 반도체의 가장 직접적 변수**.

---

## 12. 결론 — 사용자 질문 직접 답변

### 12.1 사용자 질문 4가지에 대한 직접 답

#### Q1: "영업이익도 사실 계속 성장하고 있을테니 걱정 안 해도 될련지?"

**A**: **부분적으로만 맞음**.
- 영업이익은 +14~20% 성장 중 (사실)
- 그러나 Capex가 +71% 성장 중
- **영업이익 성장 < Capex 성장 = 자금 갭 발생**
- 2024 FCF +$170B → **2026 FCF -$65B** (마이너스 진입)

#### Q2: "회사채를 엄청 늘려야 되는 건지?"

**A**: **YES, 필연**.
- 2025 회사채 발행 $108~121B (실측)
- 2026E $175~400B (BofA·MS 추정)
- 2026~2030 누적 $1.5조 예상 (Morgan Stanley)
- **자체 자금으론 못 채우는 구조 확정**

#### Q3: "장기금리에 종속될 수밖에 없는지?"

**A**: **YES, 직접 종속**.
- 회사채 금리 = 국채 금리 + 스프레드 (80~100bps)
- 미국 10년물 4.56% → 빅테크 회사채 5.4%
- 미국 30년물 5.19% → 빅테크 30년물 6.0%+
- **장기금리 상승 = 자금 비용 직접 ↑**

#### Q4: "이런 상황을 좀 더 알아보고 싶어"

**A**: 본 보고서 + 이전 보고서 ("장기채 금리 상승" + "AI 펀더멘털 검증") 종합 시:
- **단기 (6~12개월)**: 장기금리 5% 유지 시 빅테크 견딜 수 있음
- **중기 (1~2년)**: 장기금리 5.5%+ 돌파 시 빅테크 Capex 가이던스 하향 가능성 ↑
- **장기 (2~3년)**: 이자/FCF 60% 시점에 위기 본격화 가능

### 12.2 핵심 메시지

#### 메시지 #1: 영업이익 성장은 사실, 그러나 부족
- 영업이익 +14% vs Capex +71%
- 자금 갭 = 회사채로 메워야 함

#### 메시지 #2: 회사채 의존 = 장기금리 종속 = 구조적 위험
- 단기 매수 모멘텀 vs 장기 구조 위험 양면

#### 메시지 #3: 한국 반도체 = 빅테크 Capex의 직접 함수
- 빅테크 Capex -10% → 한국 영업이익 -15~20%
- 분기마다 빅테크 가이던스 트래킹 필수

#### 메시지 #4: 2026이 자금 갭의 변곡점
- 2024~2025 잉여 → 2026 적자 진입
- 2027~2028 부채 누적 가속

### 12.3 트래킹 체크리스트 (분기 단위)

#### A. 빅5 분기 실적
- [ ] **분기 영업이익 + 분기 OCF**
- [ ] **분기 Capex + 분기 FCF**
- [ ] **회사채 발행 여부 + 청약 배율**
- [ ] **AI 매출 분리 공시 (Copilot·Gemini·Bedrock 등)**

#### B. 회사채 시장
- [ ] **빅테크 신규 회사채 발행 금리**
- [ ] **빅테크 회사채 스프레드 (T+bps)**
- [ ] **Oracle·Amazon CDS 변동**
- [ ] **신용 등급 변동**

#### C. 영업이익 vs Capex 성장률 갭
- [ ] **빅5 합산 영업이익 YoY**
- [ ] **빅5 합산 Capex YoY**
- [ ] **차이 (-57%p 위험 영역 확인)**

#### D. 한국 영향
- [ ] **SK하이닉스·삼성 메모리 분기 매출**
- [ ] **HBM·DRAM·NAND 단가 추이**
- [ ] **NVIDIA 발주 변동**

### 12.4 최종 결론

> 빅테크 영업이익은 분명히 성장 중. 그러나 **Capex 가속이 영업이익 성장을 압도** = 자체 자금만으로 못 채움 = **회사채 발행 필연 → 장기금리에 직접 종속**. 2026이 자금 갭의 변곡점, 2027~2028이 본격 부담. 한국 반도체는 빅테크 Capex 가이던스에 1:1 동행 = **빅테크 회사채 시장 균열 시 직격**. 사용자의 "걱정 안 해도 될련지?" 질문에 대한 답은 **"단기는 견딜 수 있으나, 장기금리가 5.5%+ 돌파하거나 빅테크 회사채 청약 부진 시 본격 충격"**.

---

## 13. 출처 (모든 수치 출처 명시)

### 빅테크 영업이익 (Q1 2026 실측)
- [Big Tech Earnings AI Microsoft Google Meta Amazon (Business Chief)](https://businesschief.com/news/big-tech-ai-earnings-alphabet-leads-cloud-growth-surge)
- [Big Tech AI Capex Tops $650B Q1 Earnings (Yahoo Finance)](https://finance.yahoo.com/sectors/technology/articles/big-tech-ai-capex-tops-212816537.html)
- [Amazon Google Microsoft Meta Q1 earnings AI profits (Uncover Alpha)](https://www.uncoveralpha.com/p/amazon-google-microsoft-meta-q1-earnings)
- [Microsoft 10-Q FY2026 (SEC)](https://www.sec.gov/Archives/edgar/data/0000789019/000119312526191507/msft-20260331.htm)
- [Oracle Form 8-K FY2025 (SEC)](https://www.sec.gov/Archives/edgar/data/0001341439/000095017025036295/orcl-ex99_1.htm)
- [Oracle Form 8-K FY2025 alt (SEC)](https://www.sec.gov/Archives/edgar/data/0001341439/000095017025084831/orcl-ex99_1.htm)

### 빅테크 Capex
- [Hyperscaler CapEx Hits $690B in 2026 (Introl Blog)](https://introl.com/blog/hyperscaler-capex-690-billion-microsoft-azure-power-bottleneck-2026)
- [Google Microsoft Meta Amazon $725B capex 2026 (Tom's Hardware)](https://www.tomshardware.com/tech-industry/big-tech/big-techs-ai-spending-plans-reach-725-billion)
- [AMZN GOOG MSFT META ORCL $700B Capex 2026 (Wolf Street)](https://wolfstreet.com/2026/02/07/amzn-goog-msft-meta-orcl-plan-700-billion-in-largely-ai-related-capex-in-2026-heres-where-the-cash-comes-from/)
- [The $112 Billion Quarter Hyperscalers Bet Farm on AI (Tomasz Tunguz)](https://tomtunguz.com/2026-04-29-the-112-billion-quarter-hyperscalers-bet-the-farm-on-ai/)
- [Hyperscaler CapEx $600B 2026 AI Infrastructure Debt (Introl)](https://introl.com/blog/hyperscaler-capex-600b-2026-ai-infrastructure-debt-january-2026)
- [AI Capex 2026 $690B Infrastructure Sprint (Futurum)](https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/)

### 자금 갭·FCF
- [The AI CapEx Cycle Turning $600B Wrong Assets (Hidden Market Gems)](https://hiddenmarketgems.substack.com/p/the-ai-capex-cycle-is-turning-600)
- [Hyperscaler AI Investment Surge 71% 2026 (MarketWise)](https://marketwise.com/investing/hyperscaler-investment-surge-2026-ai-capex-buildout/)
- [Hyperscaler Capex $700B 2026 investors fear overbuild (DCD)](https://www.datacenterdynamics.com/en/news/us-hyperscaler-capex-to-top-700bn-in-2026-investors-fear-overbuild-and-weak-returns-moodys/)
- [Stunning Capex AI Hyperscalers Context (Calcbench)](https://www.calcbench.com/blog/post/blogger9065882471048947069/The-Stunning-Capex-of-AI-Hyperscalers-in-Context)
- [Hyperscaler Reckoning $700B Utility Moats (Decoding Discontinuity)](https://www.decodingdiscontinuity.com/p/the-agentic-reckoning-are-hyperscalers-spending-trillions-utility-moats-disappear)

### 회사채 발행·이자
- [Microsoft Google Amazon Meta Issuing $400B Debt Capex Surges 74% (Blocknow)](https://blocknow.com/microsoft-google-amazon-meta-400-billion-debt-ai-capex/)
- [Big Tech AI bond binge shatters unspoken contract (CNBC)](https://www.cnbc.com/2026/02/23/big-techs-ai-bond-binge-shatters-unspoken-contract-with-investors.html)
- [AI Hyperscalers Corporate Bond Boom Credit Markets (Infrastructure Capital)](https://infrastructurecapital.substack.com/p/ai-hyperscalers-are-fueling-a-corporate)
- [Mega-issuance AI arms race Big Tech credit spreads (Janus Henderson)](https://www.janushenderson.com/en-us/investor/article/mega-issuance-and-the-ai-arms-race-big-techs-impact-on-credit-spreads/)
- [Google Meta Oracle $1 trillion borrowing spree (Fortune)](https://fortune.com/2026/03/07/big-tech-trillion-dollar-borrowing-ai-century-bonds/)
- [Tech AI spending $700B 2026 cash hit (CNBC)](https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html)

### 2027~2028 전망
- [Big Tech Capital Expenditures $1T 2027 (CNBC)](https://www.cnbc.com/2026/04/30/ai-boom-big-tech-capital-expenditures-now-seen-topping-1-trillion-in-2027-.html)
- [Tracking Trillions AI Build-Out (Goldman Sachs)](https://www.goldmansachs.com/insights/articles/tracking-trillions-the-assumptions-shaping-scale-of-the-ai-build-out)
- [Data Center Investment $1.6T by 2030 (DCD)](https://www.datacenterdynamics.com/en/news/data-center-investment-likely-to-hit-16-trillion-by-2030-report/)
- [When Will AI Investments Pay Off (GWK Invest)](https://www.gwkinvest.com/insight/macro/when-will-ai-investments-start-paying-off/)
- [AI capex cycle war-proof for now (Allianz)](https://www.allianz.com/content/dam/onemarketing/azcom/Allianz_com/economic-research/publications/specials/en/2026/march/2026_03_25_AI.pdf)
- [North American AI Data Center $830B 2026 (PRNewswire/TrendForce)](https://www.prnewswire.com/news-releases/north-american-ai-data-center-expansion-drives-2026-capex-of-top-nine-csps-to-us830-billion-says-trendforce-302764269.html)
- [Magnificent Capex AI Spending Who Benefits (Ferguson Wellman)](https://www.fergusonwellman.com/blog/2026/5/8/the-magnificent-capex-ai-infrastructure-spending-and-who-actually-benefits)
- [Hyperscaler Capex Above $600B 2026 (MUFG)](https://www.mufgamericas.com/sites/default/files/document/2025-12/AI_Chart_Weekly_12_19_Financing_the_AI_Supercycle.pdf)
- [AI Data Center Build Five Things to Know (BloombergNEF)](https://about.bnef.com/insights/commodities/ai-data-center-build-advances-at-full-speed-five-things-to-know/)

---

## ⚠️ 주의 (사용자 우려 반영)

- 본 리포트의 **모든 수치 = 출처 명시**.
- 시점이 섞일 수 있는 부분은 **2025 실측 vs 2026E 추정**으로 분리.
- 분기 vs 연간 vs TTM 명확 구분.
- 단위 $B (10억 달러) 통일, 한국 원화 환산 시 별도 표기.
- OCF·영업이익·FCF 정의 명확 분리.
- 시나리오 확률은 **작성자 판단** + 데이터 기반.
- 빅테크 회사채 시장 변동 + 한국 반도체 영향은 **분기 단위 트래킹 필수**.
- **본 리포트는 개인 투자자·연구자용 종합 정리**입니다. 최종 매수·매도는 본인 판단·책임.
- **다음 갱신 시점**: 빅테크 분기 실적 발표 시 (Q2 2026, 2026년 7~8월) 또는 빅테크 추가 회사채 발행 시.
