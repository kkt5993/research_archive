# 👑 NVIDIA Corporation (NASDAQ: NVDA) 심층 분석
**작성일: 2026-04-24 | Agent Team 취합본**

> **읽기 전**: NVIDIA는 **2026.4 기준 시총 $4.58T로 세계 1위**. Blackwell Ultra (B300) · Rubin (R100) 로드맵 + CUDA moat + 네트워킹 (Mellanox·Spectrum-X) 장악. 단, Google TPU v7·AWS Trainium·자체 ASIC 침투로 **2027–2028 추론 점유율 경쟁**이 본격화.

---

## 사후 검증 (2026-09-01)

- **HBM**: SemiAnalysis 8/25, Rubin Ultra 192GB HBM4 8-hi. 본문 Ultra는 용량 미기재(quad-stack). 국내 HBM 바텀업 384GB 가정과 충돌.
- **CUDA/커스텀 실리콘**: 8/25–26 Hot Chips. OpenAI Jalapeño가 7월 Rubin 대비 tokens/MW·perf/watt 우위라는 SemiAnalysis 실측 주장. 양산·speculative decode 전. 본문의 추론 해자 약화를 한 단계 구체화.
- **사업 모델**: 8월 NVDA가 LPS·잔존가치 보증으로 DC 금융에 개입(오하이오 OpenAI 캠퍼스, Anthropic–Lambda에서 리스 보유). 순수 칩 벤더 서사에서 이탈. 순환금융과 잔존가치 캡을 같이 볼 것.



## 사후 검증 (2026-09-01, 추가)

AMD 8/4: DC $6.7B(+107%), Helios 램프, Anthropic **MI450 최대 2GW**. TSMC 8/31: 추론 토큰 2022 대비 ~500배, 데이터 이동 최대 60%, 가속기 가동률 40% 미만. Hot Chips 8/25 TPU v8 학습/서빙 페이퍼. NVDA 추론 해자·HBM 비트 경로와 같이 볼 것. 본문 표는 그대로.


## 🔵 시장 상황 (2026-08-11)

**미국은 사상 최고** — S&P 500 **7,757.64**(8/7, 주간 +3.58%), 나스닥 26,690.62(+5.19%), SOX 약 12,049. 하이일드 스프레드 **2.70%**·VIX **15.46**으로 위험지표 평온.

**금리**: 연준 **케빈 워시** 체제 **3.50–3.75%**(7/29 FOMC 동결). IB 10곳 중 7곳이 연내 동결을 봤으나 **8/7 7월 고용 −23,000명**(예상 +8만) 쇼크로 **9월 인하 기대 부활**. 10년 4.65%·30년 5.19%·10년 실질 2.43%. 금 약 **$4,320–4,370**(주간 +7%), WTI 약 $77–82.

> ⚠️ **한·미 디커플링**: 같은 7월 한국 코스피는 **−22.19%**(사상 최대 월간 낙폭). 미국 반도체는 강세(NVDA 8월 첫주 +11.6%)인데 **한국 메모리는 약세**(SK하이닉스 −17.2%). 같은 AI 테마라도 밸류체인 위치에 따라 갈렸다.

**반도체**: 8월 첫주 NVDA +11.6%·MRVL +16.6%·ASML +6.9%·TSMC +3.9% vs SK하이닉스 −17.2%·삼성전자 −12.0%. 엔비디아 차세대 HBM 사양 재검토 보도가 한국 메모리를 눌렀다.
---

## 📌 Executive Summary

| 항목 | 수치 |
|---|---|
| 설립 | 1993 (Jensen Huang, Chris Malachowsky, Curtis Priem) |
| 시가총액 (2026-04) | **약 $4.58T** (세계 1위) |
| FY25 매출 (FYE 2025.1) | **$130.5B** (YoY +114%) |
| FY26 Q3 매출 (2025.10) | **$57.0B** (YoY +62%) |
| FY26 Q4 가이던스 | **$65B ± 2%** |
| FY26 연간 추정 | **약 $213B** |
| Non-GAAP Gross Margin | **73.6%** (Q3 FY26) |
| OP Margin | 약 66% |
| Data Center 매출 비중 | **약 90%** |
| R&D 투자 (FY25) | $12.9B → FY26–$18B |
| 직원 수 | 약 40,000명 |

**한 줄 결론**: **AI Factory $3–4T TAM** 비전 하의 절대 강자. Forward PER 24x로 밸류에이션은 합리화됐으나 **Google TPU v7 Ironwood가 Anthropic에 1M+ 배포**되며 ASIC 위협 본격화. $5T 돌파는 12–18개월 내 유력, but **추론 영역 점유율 방어**가 장기 논거의 핵심.

---

## 1️⃣ 사업 부문 분해 (FY26 Q3)

| 부문 | 매출 (Q3) | YoY | 비중 | 주요 제품 |
|---|---|---|---|---|
| **Data Center** | $51.2B | +66% | **89.8%** | B200, GB200 NVL72, H200, Spectrum-X, InfiniBand |
| Gaming | $4.3B | +30% | 7.5% | GeForce RTX 50 (Blackwell) |
| Pro Visualization | $760M | +56% | 1.3% | RTX Pro, Omniverse |
| Automotive & Robotics | $592M | +32% | 1.0% | Drive Thor, Jetson Orin, GR00T |
| OEM & Other | 약 $150M | - | 0.3% | - |
| **합계** | **$57.0B** | **+62%** | 100% | - |

Data Center 내 **Networking (Mellanox·Spectrum-X) $7.3B (+98% YoY)** — Q2 FY26 기준, 2020년 $6.9B Mellanox 인수 효과 본격화.

---

## 2️⃣ AI GPU 로드맵 — 핵심 경쟁우위

### 세대별 스펙

| 세대 | 제품 | 출시 | 프로세스 | HBM | FP8 Dense | TDP | ASP (추정) |
|---|---|---|---|---|---|---|---|
| Hopper | H100 | 2022 | TSMC 4N | 80GB HBM3 |–2 PFLOPS | 700W | $25–30K |
| Hopper | H200 | 2024 | TSMC 4N | 141GB HBM3e |–2 PFLOPS | 700W | $30–40K |
| Blackwell | B200 | 2024 Q4 | TSMC 4NP (dual) | **192GB HBM3e** | 약 4.5 PFLOPS | 1,000W | $40–50K |
| Blackwell | **GB200 NVL72** | 2025 Q2 | 4NP | 13.5TB/rack | **720 PFLOPS/rack** | 120kW/rack | $3–3.5M/rack |
| Blackwell Ultra | **B300** | 2025 H2 | 4NP | 288GB HBM3e |–15 PFLOPS (FP4) | 1,400W | $50–60K |
| **Rubin** | **R100 (VR200)** | **2026 H2** | TSMC N3 (dual) | **288GB HBM4** @ 22TB/s | **약 16 PFLOPS** / 50 FP4 |–1,800W |–$70–80K |
| Rubin Ultra | VR300 | 2027 H2 | TSMC N3P | HBM4e quad-stack | - | **약 1MW/rack** (Kyber 800V HVDC) | - |
| Feynman | - | 2028+ | TSMC N2 | custom HBM | - | - | - |

### Rubin R100 (2026 H2) 핵심
- **336B 트랜지스터**
- 288GB HBM4 (22TB/s 대역폭)
- NVL72 랙 기준 **1.2 FP8 ExaFLOPS**
- **400B 파라미터 모델 단일 GPU에서 FP4 구동 가능**

### Rubin Ultra NVL576 Kyber (2027 H2)
- 144개 쿼드-칩렛 Rubin Ultra GPU (576 compute chiplet)
- **800V HVDC 전력 아키텍처 최초 채택**
- GB300 NVL72 대비 **14배 훈련·추론 성능**

**CoWoS 매핑**: H100/200 CoWoS-S, B200/GB200 CoWoS-L, Rubin CoWoS-L (확장). 2025년 B200 CoWoS 할당 220K wafer = TSMC 전체 30%+ 소화.

---

## 3️⃣ 소프트웨어 Moat — 대체 불가능성의 원천

| 플랫폼 | 출시 | 규모 |
|---|---|---|
| **CUDA** | 2006 | **400만+ 개발자** (2025) |
| cuDNN | 2014 | 모든 주요 프레임워크 기본 |
| TensorRT / TensorRT-LLM | 2017/2023 | LLM 2–8x 추론 가속 |
| NCCL | 2015 | 멀티-GPU 학습 표준 |
| Triton | 2018 | 추론 서버 |
| **NIM** | 2024.3 | 100+ 모델 카탈로그 |
| **Omniverse** | 2019 | BMW·Ericsson·TSMC 팹 |
| **GR00T N1/N2** | 2025.3 | Figure·1X·Agility 로봇 파운데이션 모델 |
| DGX Cloud | 2023 | Azure·GCP·Oracle 배포 |
| Earth-2 | 2024 | 기후·재난 시뮬 |

**CUDA Moat의 본질**: 단순 성능 아닌 **20년+ 누적된 생태계·문헌·졸업생 엔지니어**. 다만 2026년 **OpenAI Triton, PyTorch 2.x Inductor, MLIR 컴파일러** 부상으로 **추론 영역 해자 약화** 조짐 (SemiAnalysis 지적).

---

## 4️⃣ 네트워킹 장악

| 기술 | 인수/출시 | 역할 |
|---|---|---|
| InfiniBand (Mellanox) | **2020 $6.9B 인수** | 훈련 클러스터 독점 |
| Spectrum-X | 2023 | 이더넷 (RoCE) — Arista·Cisco 잠식 |
| Quantum-X 800G | 2024–25 | InfiniBand 차세대 |
| **Quantum-X Photonics** | **2026 GTC** | **Silicon photonics 스위치 (Rubin)** |
| NVLink 5 | 2024 | 1.8TB/s per GPU (B200) |
| NVLink 6 | 2026 | 3.6TB/s (Rubin 예상) |

**FY26 Q2 네트워킹 매출 $7.3B (+98% YoY)** — Arista·Cisco·Juniper 일부 잠식 중. **800G → 1.6T 광모듈** 수혜: Coherent, Lumentum, Eoptolink, Innolight, Fabrinet.

---

## 5️⃣ ASIC·경쟁자 위협 평가

| 경쟁자 | 제품 | 2026 상태 | 위협 |
|---|---|---|---|
| **Google TPU v7 Ironwood** | 4.6 TFLOPS FP8/chip | GA 2025 말, **Anthropic 1M+ 유닛 배포**, 2026 4.3M대 목표 | **★★★★★ 최대** |
| **AWS Trainium 3** | 2.5 PFLOPS FP8 | 2026 중반 GA | ★★★★ |
| **Meta MTIA v3** | 내부용 | 2026 H2 | ★★★ |
| **MS Maia 200** | 내부용 | 2026 H2 Azure | ★★★ |
| **AMD MI350/MI400** | MI355X 288GB / MI400 (2026말) | MI350 2025말, MI400 2026말 | ★★★ (오픈 생태계 약점) |
| Cerebras WSE-3 | Wafer-scale | G42, 국방부 | ★★ (니치) |
| Groq LPU | 추론 전용 | Aramco, GroqCloud | ★★ |
| Tenstorrent | Blackhole | RISC-V | ★★ |
| Graphcore | - | 2024 Softbank 인수 후 재편 | 위협 소멸 |

**Google TPU = 최대 위협**. v7 Ironwood가 Blackwell과 격차 거의 해소, **Anthropic에 1M+ 유닛 + 1GW 이상 컴퓨트 배포** 계약. Google은 2026 4.3M → 2027 10M → 2028 35M TPU 출하 목표. 일부 분석은 **NVIDIA 추론 점유율 2028년까지 90%+ → 20–30% 급락 가능** 경고.

---

## 6️⃣ 중국 시장 — 구조적 차단

| 시점 | 조치 | 영향 |
|---|---|---|
| 2022.10 | A100/H100 금지 | A800/H800 우회 |
| 2023.10 | A800/H800·L40S 차단 | H20·L20·L2로 추가 우회 |
| **2025.4.15** | **H20 금지** (트럼프 2기) | **Q1 FY26 $4.5B 재고 상각** |
| 2025 하반기 | H200 제한적 허용 논의 | 월 출하 한도 |
| 2026.4 | H200 중국 75K 상한 + 25% 세금 | JPM "연 $16B 매출 잠재 손실" |

**중국 매출 비중**: 2023–21% → 2024 17% → **2025–13%** → 2026E <10%. 중국 DC 매출 2025 H2 기준 YoY -45%.

**중국 대체품**: **Huawei Ascend 910C** (2025 생산 100K, 910B 300K), Biren BR100, Cambricon MLU370. 910C는 H200 대비 FP8 성능–45%, 메모리 대역폭 50%. **중국 내 대형 AI 랩 기본 훈련 가속기**로 자리.

---

## 7️⃣ 재무 상세

### 분기별 추이

| 분기 | 매출 | DC | YoY | Non-GAAP GM |
|---|---|---|---|---|
| FY25 Q4 | $39.3B | $35.6B | +78% | 73.5% |
| FY26 Q1 | $44.1B | $39.1B | +69% | 61% (H20 $4.5B 상각) |
| FY26 Q2 | $46.7B | $41.1B | +56% | 72.7% |
| **FY26 Q3** | **$57.0B** | **$51.2B** | **+62%** | **73.6%** |
| FY26 Q4 가이던스 | $65.0B | - | 약 +60% |–73.5% |
| **FY26 연간 추정** | **약 $213B** | 약 $190B+ | +63% |–72% |

### 자본 배분
- **자사주 매입**: FY25 $34B, FY26 $60B+ 신규 권한
- **현금·단기투자**: FY26 Q3–$100B+ (Net Cash)
- **OpenAI 투자**: **최대 $100B 투자 약정** (컴퓨트 10GW 대가) — 역사상 최대 **순환 거래 논란**

---

## 8️⃣ 주가·밸류에이션

| 지표 | 값 (2026.4.22–23) |
|---|---|
| 주가 | **$189.31** (4.13) |
| 시가총액 | **$4.58T** |
| **TTM P/E** | **40.79** |
| **Forward P/E (12M)** | **23.97** |
| 12M 평균 대비 | -12.41% (압축 중) |
| PEG (5yr) | **약 0.8** (매력적) |
| EV/EBITDA (fwd) | 약 22x |
| **Morgan Stanley PT** | $260 기본 / $330 bull / $150 bear |
| Goldman Sachs PT | $250 (FY27 $380B 매출, 30x fwd P/E) |

**$5T 돌파 시나리오**: 2026 말–2027 초. 전제: (1) FY27 매출 $250B+, (2) Rubin 원활 ramp, (3) 중국 규제 완화, (4) ASIC 침투 완만.

---

## 9️⃣ 리스크

| 리스크 | 심각도 | 타임라인 |
|---|---|---|
| **하이퍼스케일러 ASIC 내재화** (Google/AWS/Meta/MS) | ★★★★★ | 2026–2028 단계적 |
| **CUDA 대안 부상** (Triton, Inductor, MLIR) | ★★★★ | 2027~ 추론 |
| **AI Capex 피크아웃** | ★★★★ | 2027–2028 가능성 |
| 중국 대체품 성숙 (Ascend 910C/920) | ★★★ | 진행 중 |
| 규제 (FTC·EU·중국 반독점) | ★★★ | 상시 |
| 공급망 집중 (TSMC CoWoS, HBM 3사) | ★★★ | 구조적 |
| OpenAI 순환 거래 논란 | ★★ | 회계 리스크 |
| Jensen Huang Key-man | ★★ | 장기 |

---

## 🔟 생태계·파트너십

| 영역 | 핵심 파트너 |
|---|---|
| **파운드리** | **TSMC (CoWoS-L 독점)**, Arizona Fab 21 일부 |
| **HBM** | SK하이닉스 (주), Micron (2nd), **삼성 (HBM4 인증 진행 중)** |
| ODM/서버 | Foxconn, Quanta, Wistron, Supermicro, Inventec |
| 하이퍼스케일러 | Microsoft, Google, AWS, Meta, Oracle, xAI, CoreWeave |
| 네오클라우드 | CoreWeave, Lambda, Nebius, Nscale, Crusoe |
| 자동차 | Mercedes-Benz, JLR, Volvo, BYD, 현대 (Drive Thor) |
| 로보틱스 | **Figure, 1X, Agility, Boston Dynamics**, Galbot |
| AI 모델 | **OpenAI ($100B 투자)**, Anthropic, Mistral, Meta Llama |
| Sovereign AI | Saudi Humain, UAE G42, 인도 Reliance/Tata, 프랑스 Scaleway, 한국 NAVER·KT |

---

## 1️⃣1️⃣ Jensen Huang 비전 — "AI Factory"

GTC 2026 기조연설 TAM 제시:

1. **AI Factory ($3–4T TAM by 2030)**: 일반 컴퓨팅 $1T + 가속 컴퓨팅 $3T 병렬 확장
2. **Physical AI**: 로봇(GR00T)·자율주행(Drive Thor)·디지털 트윈(Omniverse) — 2030 로봇 $100B+
3. **Sovereign AI**: 각국 자국어·자국 데이터 AI 독립 — 유럽 15, 중동 3, 아시아 주요국
4. **Agentic AI**: 훈련 대비 추론 컴퓨팅 **100–1000배 증가** (Test-time scaling) — FP4 최적화와 정합

---

## 🎯 최종 판단

NVIDIA는 2026.4 현재 **$4.58T · Fwd PER 24x**로 밸류에이션 합리화. FY27 매출 $250–300B 컨센서스면 **$5T 돌파 12–18개월 내** 현실적. 다만 **TPU v7 Anthropic 1M+ 배포** + **OpenAI-NVIDIA $100B 순환 거래** 회계 의문 상존.

### 분기 모니터링 3대 포인트
1. **네트워킹 매출 성장률** 지속 여부
2. **하이퍼스케일러 ASIC 비중** 공시
3. **Rubin R100 양산 일정** 미끄러짐

**단기 R/R 중립~긍정** (FY27 가이던스 업사이드), **중기 (2027–2028) ASIC 침투 속도 결정 변수**. Jensen의 "AI Factory $3–4T TAM" 서사 유지 시 프리미엄 정당화, but **추론 점유율 2028까지 70%+ 방어**가 장기 투자 논거 핵심.

---

## 밸류에이션 — 어떻게 평가하나 + 현재 위치

> **작성 시점:** 2026-04-28 기준 공개 자료 + 컨센서스를 바탕으로 한 추정. 실시간 시세와 차이 가능. 매매 전 IR/공시 재확인 필수.

### 이 회사(섹터)는 무슨 잣대로 보나?

**쉽게 말하면**: 동네 식당이 1년에 100만원 벌고 가격이 2,500만원이면 P/E 25배. NVIDIA는 1년에 약 $130B(약 180조원)을 벌고 시가총액이 $4.58T(약 6,400조원)이니 **TTM P/E 약 41배** — "지금 사면 41년치 이익에 해당하는 가격"이라는 뜻.

근데 NVIDIA는 **이익이 매년 60–100% 폭증** 중이에요. 그래서 "올해 이익"이 아니라 **"내년·내후년 이익"** 으로 환산해야 합니다 → **Forward P/E 24배**. 즉, "1년 후 기준으로 보면 24년치"로 떨어져요.

식당 비유로 다시: "이 식당 작년엔 100만 원 벌었지만 올해 200만 원, 내년 350만 원 벌 거 같아요"라면 가격 2,500만 원도 합리적일 수 있죠. NVIDIA는 그 식당의 글로벌 빅테크 버전.

**조금 더 들어가면**: AI 빅테크 같은 초고성장 회사는 **PEG (Price/Earnings ÷ Growth)** 가 핵심 잣대. P/E 40배여도 성장률 50%면 PEG = 0.8 → "성장 대비 싸다"고 봐요. NVIDIA는 PEG 약 0.8로 **여전히 매력 구간**.

추가로 **FCF Yield (잉여현금흐름 수익률)** — "1년에 회사가 벌어들이는 진짜 현금이 시총의 몇 %인가". NVIDIA FCF Yield 약 2.5–3% → 미국 10년물 국채 수익률(약 4%)에는 못 미치지만, 성장 프리미엄을 합치면 균형.

**전문가 관점**: NVIDIA는 **AI 슈퍼사이클의 중앙 자산** — 단일 멀티플보다 **(1) Forward P/E (2) PEG (3) EV/EBITDA (4) FCF Yield** 4축으로 동시 진단. 2024년 P/E 70–80배 → 2026.4 현재 24배로 **반토막 압축** 진행 중. 이는 주가 하락이 아니라 **이익 폭증 속도가 주가 상승을 추월**했다는 의미 (좋은 종류의 압축).

> **용어 박스**
> - **P/E (Price/Earnings):** 주가 ÷ 주당순이익. "이익 1원 사는 데 몇 원 내나?"
> - **Forward P/E:** 다음 12개월 예상 이익 기준. 성장주 평가 표준.
> - **PEG (Price/Earnings to Growth):** P/E ÷ 연평균 이익 성장률. 1 미만 = 성장 대비 저평가.
> - **EV/EBITDA:** 기업가치 ÷ "영업이익 + 감가상각" — 이자·세금·자본구조 제거한 순수 영업력 멀티플. M&A 시 표준.
> - **FCF Yield (Free Cash Flow Yield):** 잉여현금흐름 ÷ 시총. "주식 1주가 1년에 들고 오는 진짜 현금 수익률".
> - **EPS (Earnings Per Share, 주당순이익):** 연 순이익 ÷ 발행주식수. 1주당 회사가 번 돈.

### 현재 멀티플 매트릭스 (2026-04-28 기준 추정)

| 종목 | 시가총액 | TTM P/E | Forward P/E | EV/EBITDA (fwd) | P/B | ROE | 5년 평균 P/E | 현재 위치 |
|---|---|---|---|---|---|---|---|---|
| **NVIDIA (NVDA)** | **약 $4.58T** | **40.79** | **23.97** | **약 22x** | 30-40x | **90%+** | 약 40x (변동 큼) | **5년 평균 대비 -40% 압축** |
| AMD | 약 $320B |–85x |–28x |–22x |–5x | 7-9% | 약 35x | 5년 평균 부근 |
| Broadcom (AVGO) | 약 $1.2T |–55x |–30x |–25x |–10x | 30%+ | 약 25x | 5년 평균 상단 |
| TSMC | 약 $1.92T |–28x |–22-25x |–13-15x | 6-7x | 28-30% | 약 18x | 5년 평균 상단 |
| S&P500 | - | 약 28x |–20x |–14x |–4x | 18% |–22x | 평균 부근 |

> **핵심**: NVIDIA는 **Forward P/E 24x로 사상 최저 수준의 압축** 중. 동종 AI 칩 그룹(AMD 28x, AVGO 30x)보다 오히려 저렴 — "1등주가 더 싸다"는 역설.

### 역사 밴드에서 어디 있나?

**쉽게 말하면**: NVIDIA P/E 밴드는 **2020–24년 50–80배 (AI 붐 초기 프리미엄)** → **2025–26년 40배 → 24배로 압축**. **5년 평균 P/E 약 40배 대비 현재 24배는 약 -40% 디스카운트** 위치.

**왜 압축됐나?** (역설적이지만 좋은 신호):
1. **이익 폭증 속도 > 주가 상승 속도** — FY25 매출 $130.5B (+114%), FY26E $213B (+63%) — 분모(이익)가 분자(주가)보다 더 빨리 자라며 멀티플 자동 압축.
2. **TPU·Trainium 등 ASIC 위협 우려 반영** — 미래 점유율 하락 시나리오 일부 디스카운트.
3. **OpenAI $100B 순환 거래 회계 의문** — 일부 투자자 보수적 접근.

**전문가 관점**: Morgan Stanley PT **$260 (Bull $330, Bear $150)**, Goldman PT $250 (FY27 매출 $380B, 30x fwd P/E 가정). 컨센서스 평균 PT 대비 현재가 **+30% 상방 여력**. 단, 2027–28년 ASIC 침투 속도가 장기 PER 결정 변수.

### Bull / Base / Bear 멀티플 시나리오

| 시나리오 | 가정 | 적용 Forward P/E | FY27E EPS (가정) | 주가 함의 |
|---|---|---|---|---|
| **Bull** | FY27 매출 $300B+, 추론 점유율 80%+ 방어, Rubin Ultra Kyber 양산 순항, 중국 규제 부분 완화 | **35x** | $9.0 | **약 $315 (+66%)** |
| **Base** | FY27 매출 $250–280B, ASIC 침투는 점진적, Rubin 정상 ramp | **28x** | $7.5 | **약 $210 (+11%)** |
| **Bear** | TPU v7 추론 시장 30%+ 잠식, AI Capex 피크아웃 시그널, OpenAI 거래 회계 이슈 | **18x** | $6.0 | **약 $108 (-43%)** |

> **핵심 변수**: ① **하이퍼스케일러 ASIC 비중 공시** (분기별), ② **Rubin R100 양산 일정** (2026 H2), ③ **네트워킹 매출 성장률** (Mellanox·Spectrum-X), ④ **중국 H200 75K 상한 + 25% 세금 조건** 영구화 여부.

### ⚠️ 이 매트릭스를 볼 때 주의

- 본 매트릭스는 작성 시점(2026-04-28) 기준 공개치 + 컨센서스 추정. 실시간 시세와 다를 수 있음.
- NVIDIA의 P/E는 **분기별로 30–50% 출렁임** (이익 가이던스 변경 영향) — 단일 시점 멀티플은 스냅샷일 뿐.
- **OpenAI $100B 투자 약정**의 회계 처리 방식은 2026년 SEC·감사인 이슈로 부상 가능 → 발생 시 EPS 추정 재산정 필요.
- 동종 비교(AMD·AVGO·TSMC)는 **사업모델 상이** — NVIDIA의 CUDA moat·네트워킹 통합·풀스택 솔루션은 단순 멀티플로 환산 어려움.
- **AI 사이클 산업의 장기 멀티플은 "정점에서 반토막"이 흔함** — 1990–2000 닷컴, 2010–2018 반도체 사이클 모두 P/E 50x → 15x 압축 사례 존재. NVIDIA가 다르다고 보장 없음.

---

## 📚 Sources
- [NVIDIA Q3 FY26 Earnings](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-third-quarter-fiscal-2026)
- [Futurum — Q3 FY26 Record DC Revenue](https://futurumgroup.com/insights/nvidia-q3-fy-2026-record-data-center-revenue-higher-q4-guide/)
- [NVIDIA FY25 Annual Results](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2025)
- [NVIDIA CFO Commentary Q1 FY26 SEC](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000115/q1fy26cfocommentary.htm)
- [Companies Market Cap — NVIDIA](https://companiesmarketcap.com/nvidia/pe-ratio/)
- [FinanceCharts — NVDA PE Ratio](https://www.financecharts.com/stocks/NVDA/value/pe-ratio)
- [Spheron — Rubin R100 Guide](https://www.spheron.network/blog/nvidia-rubin-r100-guide/)
- [Tech-Insider — Vera Rubin Platform GTC 2026](https://tech-insider.org/nvidia-vera-rubin-platform-gtc-2026-rubin-r100-gpu/)
- [Tom's Hardware — Rubin Ultra Feynman Roadmap](https://www.tomshardware.com/pc-components/gpus/nvidia-announces-rubin-gpus-in-2026-rubin-ultra-in-2027-feynam-after)
- [NVIDIA Blog — 800V HVDC](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/)
- [Next Platform — AI System Roadmap](https://www.nextplatform.com/compute/2026/03/19/driving-down-the-ai-system-roadmap-with-nvidia/5210195)
- [SemiAnalysis — Blackwell Shipment Delays](https://newsletter.semianalysis.com/p/nvidias-blackwell-reworked-shipment)
- [SemiAnalysis — TPUv7 Google](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the)
- [Introl — Custom Silicon Inflection 2026](https://introl.com/blog/custom-silicon-inflection-2026-hyperscaler-asics-nvidia-gpu)
- [CNBC — Nvidia vs TPU vs Trainium](https://www.cnbc.com/2025/11/21/nvidia-gpus-google-tpus-aws-trainium-comparing-the-top-ai-chips.html)
- [Computer Weekly — H20 Export Ban](https://www.computerweekly.com/news/366622857/AI-chip-restrictions-limit-Nvidia-H20-China-exports)
- [Tech-Insider — H200 China 75K Cap](https://tech-insider.org/nvidia-h200-chip-sales-china-2026/)
- [AInvest — Huawei Ascend 910C](https://www.ainvest.com/news/huawei-ascend-910c-game-changer-china-ai-chip-sufficiency-drive-2504/)
- [NVIDIA NIM](https://nvidianews.nvidia.com/news/nvidia-nim-model-deployment-generative-ai-developers)
- [Morgan Stanley NVDA PT — TheStreet](https://www.thestreet.com/investing/stocks/morgan-stanley-sets-bold-new-price-target-on-nvidia-stock)
- [Goldman Sachs NVDA — TheStreet](https://www.thestreet.com/investing/stocks/goldman-sachs-sends-blunt-message-on-nvidia-stock-after-gtc)

### ⚠️ 주의
- 본 리포트는 2026-04-24 시점. NVIDIA 주가·경쟁 구도는 분기 단위 급변.
- FY26 Q4 가이던스·Rubin 램프업·중국 규제 완화 여부가 단기 변동 주요 변수.
- OpenAI $100B 순환 거래 회계 공시 방식, Google TPU v7 배포 속도, Huawei Ascend 성숙도는 현 시점 정량화 어려운 핵심 변수.


## 사후 검증 (2026-09-01, SA 8/30 네오클라우드 보안)

SemiAnalysis 8/30 ClusterMAX 3.0 보안 프리뷰. 차트·최소버전 표·말미 NVDA/AMD 함의 섹션은 페이월이라 숫자 없음.

- **설계가 병목**: 4–7월 25사 32클러스터. 단일 실수(공유 K8s 컨트롤플레인, 컨테이너-only 격리, IB 기본 파티션 잔존, Grafana 갓토큰, BMC/DPU 노출)가 크로스-테넌트 노출로 간다. Together만 유료 바운티, 나머지는 security.txt.
- **AI-CVE 폭증은 미입증**: 드라이버·CUDA·K8s·Docker·커널 시계열은 변화 없음 가설을 기각하지 못함. Glasswing 멤버만 컨트롤 대비 YoY 급증(보고 인센티브 가능).
- **NVDA 축**: BlueField 기본은 host-trusted. GPU 클라우드에서 테넌트=호스트 어드민이면 위협모델이 역전. ClusterMAX 스냅샷 본문은 CoreWeave(Gold) vs Azure 최소버전 비교 — Azure가 더 많이 통과, 미명 Bronze는 CUDA/runc/Docker/ConnectX 미달. 대시보드 숫자는 결측.
- CUDA 해자 붕괴와 별 축. 다음 관찰점은 ClusterMAX 3.0 본편.


## 사후 검증 (2026-09-02, SA 9/1 Korea Sovereign AI)

SemiAnalysis 9/1「Korea's Trillion-Dollar Sovereign AI Investment: Nvidia Wins, Hynix Loses」(Max Kan, Ray Wang, Dylan Patel). **페이월**: 차트·표·Memory Model·Datacenter Model 사이트 MW 상세 결측 — 발명 금지.

- **주장**: Sovereign AI — frontier API는 US labs+USG 자비. OSS 라이선스도 조여짐. 진정한 독립 = own pretrained model on own GPUs. NVDA는 OSS+sovereign 수요가 없으면 실질 GPU 바이어가 약 2–7로 좁아짐(SA).
- **메커니즘**: 한국 인프라 메가프로그램(7월 발표 약 $919B; 2029년까지 8.4 GW, 2035년까지 18.4 GW) + 토너먼트(정부 예산 약 $350M)가 sovereign compute 수요를 만듦. 공개 딜: **SK 5 GW 중 2 GW Rubin**; **Naver 200 MW**; Samsung 보도 **>50k GPU** Nvidia AI factory; **SKT 2 GW DSX Vera Rubin** + Hynix HBM4.
- **회의론**: **발표 GW ≠ 건설**(데스크 가설 유지). SA: 용량 상당수는 Anthropic/OpenAI에 판매될 수 있음. Phase 1 활성 사이트 3곳 합 4.4 GW — 정확한 사이트·MW ramp는 페이월.
- **2–3Q 반증조건**: SK/Naver Rubin·GPU 실주문·설치 지연; Samsung AI factory GPU 수량 하향; sovereign 승자 스케일업이 해외 클라우드 의존으로 회귀.
- **투자 번역**: NVDA 고객 다변화(sovereign/OSS) 서사 강화·단일 HS 의존 리스크 완화 논리. 단, 발표 용량의 건설·COD·실제 GPU put은 별 확인.


## 사후 검증 (2026-09-08, SA 9/7 TPU InferenceX Preview)

SemiAnalysis 9/7「TPU Inference Externalization Full Steam Ahead - InferenceX」(Alec Ibarra 외). InferenceX Official Preview — TPUv7 Ironwood 3rd-party 추론. **페이월**: Accelerator/TCO Model BOM·표 상세 결측 — 발명 금지. 공개 본문 수치만.

- **주장**: Ironwood는 B200/B300 대비 FP8 aggregated serving에서 **최대 ~50% better perf/$**. 100 tok/s/user: Ironwood ~$0.181/M tok vs B200 $0.222 · B300 $0.276 (~19% / ~34% 저가). 20 tok/s/user: tokens/$ B200 대비 +50.4%, B300 대비 +96%. **CUDA moat는 추론에서 외부 TPU 스택이 잠식 가능** — 단 FP4·disagg는 아직 NVDA 쪽.
- **메커니즘**: TorchTPU(PrivateUse1, device=`tpu`)가 TorchAX/JAX 번역 경로를 대체 → vLLM/SGLang이 PyTorch 네이티브로 TPU 서빙. Inferact·RadixArk·Red Hat 협업. private beta → **~10월 중순 PyTorch Conference OSS**. DP-attention+EP, SparseCore collective, MoE GroupedGEMM, GDN Pallas, hybrid prefix cache 등 커널·서빙 최적화. Anthropic가 2029까지 DeepMind 자체 사용을 넘는 최대 TPU 유저(SA). Google은 TPU를 임대뿐 아니라 **매각**.
- **회의론 / 범위**: (1) Ironwood **native FP4 없음** → FP4 품질 비교에서는 NVDA 우위; SA는 **TPUv8i Boardfly**가 Rubin NVL72와 경쟁 가능하다고 봄. (2) 외부 스택 **PD disagg 미성숙** — apples-to-bananas(agg TPU vs GB300 NVL72 disagg)에서 중위 e2e latency ~30% perf/$는 GB300. (3) 벤치는 주로 **8k1k** bring-up; AgentX/에이전틱은 연내 후속. (4) TPU MXU 256×256 타일 픽키함 — head dim 64/192 모델은 bring-up 비용↑. (5) 내부 TCO($1.03/chip-hr) vs 외부 TCO는 별 층 — 혼용 금지.
- **2–3Q 반증조건**: TorchTPU OSS·day-0 모델 확장이 지연/품질 실패; TPU disagg 후속이 GB300 대비 격차를 못 좁힘; Hyperscaler·랩의 실주문/설치가 GPU put으로 재집중; InferenceX AgentX TPU가 CUDA 우위 재확인.
- **투자 번역**: 데스크 워치리스트 **「CUDA vs ASIC — inference leak vs training hold」**를 SA 실측으로 한 칸 전진. NVDA Bear의 “추론 30%+ 잠식”은 **가능 경로**로 구체화됐으나, **훈련·NVL72 disagg·FP4·에이전틱**은 아직 hold. 단기 = 소프트웨어 외부화 속도 관찰; 중기 = v8i/Boardfly·disagg 후속 기사.


## 사후 검증 (2026-09-10, SA 9/9 Robot On-Device vs DC Inference)

SemiAnalysis 9/9「Where Does a Robot Think – On-Device vs Datacenter Inference」(Ivan Chiam, Zane Fong, Bryan Shan 외). **페이월**: B300 vs 56 Thor **TCO/BOM 표·Factories To Caves 전개 결측** — 발명 금지. 공개 본문 수치만.

- **주장**: Physical AI에서 **cascade(계층 분리)는 불가피**. 제너럴리스트 로봇의 무거운 planning은 데이터센터 GPU로, 고주파 action/safety는 온보드. NVDA·Google DeepMind류는 클라우드 인지 + 엣지 소형 컨트롤로 기울고, Figure Helix는 온보드, Physical Intelligence π0.7은 오프보드 H100, NVDA DreamZero(14B WAM)는 실시간용 **GB200 2장** 오프보드.
- **메커니즘**: (1) Embodiment — 로봇은 지연·대당 선투자 제약으로 모델이 하드웨어에 맞춰짐(LLM 반대). 프론티어 로봇 모델 ~**5–14B**(π0.7 5B, DreamZero 14B). (2) Hierarchical — planning은 초당 수회·비동기라 무선 RTT/지터를 흡수, action은 수백 Hz라 로컬 고정. (3) 워크로드 — 로봇 토큰은 메트로놈형(프레임→짧은 액션 청크); LLM식 KV 메모리벽과 달리 **FLOPs 바인딩**이 흔함. WAM은 비디오 디노이징으로 더 무거움. (4) Edge 한계 — Jetson Thor ≈ B200의 **1/10**, B300의 **~1/14**; DreamZero ~7Hz에 GB200 2장 ≈ Thor의 **~20×** 컴퓨트. Thor 단독이면 1Hz 미만. (5) 전력 — Blackwell ~**1.2–1.4 kW** vs Thor **40–130 W**; 휴머노이드 배터리 ~**2 kWh**. 오프로드 시 온보드 인지+무선 **20–30 W**. (6) 공급 — Jetson은 가속기 믹스에서 얇은 슬iver; Thor는 TSMC **N4**(Blackwell과 동일 노드 경쟁), 차세대는 Rubin과 함께 **N3** 추정. GM: DC GPU **mid–high 70s%** vs Jetson **mid-60s%**. 2030년 Jetson급 100만개(~400mm²) ≈ **연 1만 웨이퍼** — DC ramp 대비 반올림 오차; 수천만개/년 이후에야 타이트. **실리콘 효율 교차 ~로봇 7대/GPU**, **DRAM(LPDDR) 교차 ~5대/GPU** 이후엔 공유 DC GPU가 대당 웨이퍼·DRAM 더 적음. Thor LPDDR5X **128GB**(Orin 64 → Xavier 32). (7) 서빙 — DreamZero를 실 B300에서 WAM 최적화(CUDA graphs, DiT cache, NVFP4 등); RTT **10ms** 온프렘 가정, 청크당 **1.6s** 모션 예산. WAM은 BS1 compute-bound → **타임멀티플렉스**; VLA(π0/GR00T)는 BW-bound → 연속 배칭. **B300 1GPU당 최대 7대**(p99 **1.16s**, 예산 내). 프레임: **B300 NVL8 1대 = 56대** vs **Thor 56대** — **달러 TCO 결론은 페이월**.
- **회의론**: (1) TCO/BOM·「Factories To Caves」는 미공개 — 오프로드 우위 **미확정**. (2) RTT 10ms·공장 Wi‑Fi/5G는 가정; 연결 불량 환경은 온보드만. (3) DreamZero-Flash 재학습 없이 단일 디노이즈 — 태스크 품질 미검증. (4) 로봇 볼륨이 수년 뒤라 Jetson ramp 인센티브 약함 — 「Physical AI = 즉시 DC 수요」과잉 환산 금지. (5) 스케일링 법칙이 로봇에서도 성립하는지는 SA도 open question.
- **2–3Q 반증조건**: 페이월 TCO가 Thor 온보드 우위로 나옴; 공장 실측 glass-to-glass가 1.6s 예산을 상습 초과; 프론티어 모델이 Thor급에 맞게 축소되며 오프보드 불필요; Jetson/LPDDR 공급·마진이 DC와 분리되어 급ramp.
- **투자 번역**: Physical AI 스케일은 **Jetson ASP 스토리보다 DC GPU put + 온프렘/니어엣지 추론 랙** 쪽으로 기울 수 있음(실리콘·DRAM 효율 교차 공개). 단 **단기 DC capex 피크 관찰점(2027Q1 HS 가이던스)은 변경 없음** — 로봇 오프로드는 중기 옵션. CUDA vs ASIC 워치리스트와 직교: 로봇 WAM/VLA는 당분간 **NVDA 스택**(DreamZero/GR00T/Thor) 중심. ClusterMAX 3.0 본편·TPU disagg 후속과 별 트랙.
