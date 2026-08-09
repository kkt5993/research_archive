# 👑 NVIDIA Corporation (NASDAQ: NVDA) 심층 분석
**작성일: 2026-04-24 | Agent Team 취합본**

> **읽기 전**: NVIDIA는 **2026.4 기준 시총 $4.58T로 세계 1위**. Blackwell Ultra (B300) · Rubin (R100) 로드맵 + CUDA moat + 네트워킹 (Mellanox·Spectrum-X) 장악. 단, Google TPU v7·AWS Trainium·자체 ASIC 침투로 **2027~2028 추론 점유율 경쟁**이 본격화.

---

## 📌 Executive Summary

| 항목 | 수치 |
|---|---|
| 설립 | 1993 (Jensen Huang, Chris Malachowsky, Curtis Priem) |
| 시가총액 (2026-04) | **~$4.58T** (세계 1위) |
| FY25 매출 (FYE 2025.1) | **$130.5B** (YoY +114%) |
| FY26 Q3 매출 (2025.10) | **$57.0B** (YoY +62%) |
| FY26 Q4 가이던스 | **$65B ± 2%** |
| FY26 연간 추정 | **~$213B** |
| Non-GAAP Gross Margin | **73.6%** (Q3 FY26) |
| OP Margin | ~66% |
| Data Center 매출 비중 | **~90%** |
| R&D 투자 (FY25) | $12.9B → FY26 ~$18B |
| 직원 수 | ~40,000명 |

**한 줄 결론**: **AI Factory $3~4T TAM** 비전 하의 절대 강자. Forward PER 24x로 밸류에이션은 합리화됐으나 **Google TPU v7 Ironwood가 Anthropic에 1M+ 배포**되며 ASIC 위협 본격화. $5T 돌파는 12~18개월 내 유력, but **추론 영역 점유율 방어**가 장기 논거의 핵심.

---

## 1️⃣ 사업 부문 분해 (FY26 Q3)

| 부문 | 매출 (Q3) | YoY | 비중 | 주요 제품 |
|---|---|---|---|---|
| **Data Center** | $51.2B | +66% | **89.8%** | B200, GB200 NVL72, H200, Spectrum-X, InfiniBand |
| Gaming | $4.3B | +30% | 7.5% | GeForce RTX 50 (Blackwell) |
| Pro Visualization | $760M | +56% | 1.3% | RTX Pro, Omniverse |
| Automotive & Robotics | $592M | +32% | 1.0% | Drive Thor, Jetson Orin, GR00T |
| OEM & Other | ~$150M | - | 0.3% | - |
| **합계** | **$57.0B** | **+62%** | 100% | - |

Data Center 내 **Networking (Mellanox·Spectrum-X) $7.3B (+98% YoY)** — Q2 FY26 기준, 2020년 $6.9B Mellanox 인수 효과 본격화.

---

## 2️⃣ AI GPU 로드맵 — 핵심 경쟁우위

### 세대별 스펙

| 세대 | 제품 | 출시 | 프로세스 | HBM | FP8 Dense | TDP | ASP (추정) |
|---|---|---|---|---|---|---|---|
| Hopper | H100 | 2022 | TSMC 4N | 80GB HBM3 | ~2 PFLOPS | 700W | $25~30K |
| Hopper | H200 | 2024 | TSMC 4N | 141GB HBM3e | ~2 PFLOPS | 700W | $30~40K |
| Blackwell | B200 | 2024 Q4 | TSMC 4NP (dual) | **192GB HBM3e** | ~4.5 PFLOPS | 1,000W | $40~50K |
| Blackwell | **GB200 NVL72** | 2025 Q2 | 4NP | 13.5TB/rack | **720 PFLOPS/rack** | 120kW/rack | $3~3.5M/rack |
| Blackwell Ultra | **B300** | 2025 H2 | 4NP | 288GB HBM3e | ~15 PFLOPS (FP4) | 1,400W | $50~60K |
| **Rubin** | **R100 (VR200)** | **2026 H2** | TSMC N3 (dual) | **288GB HBM4** @ 22TB/s | **~16 PFLOPS** / 50 FP4 | ~1,800W | ~$70~80K |
| Rubin Ultra | VR300 | 2027 H2 | TSMC N3P | HBM4e quad-stack | - | **~1MW/rack** (Kyber 800V HVDC) | - |
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
| TensorRT / TensorRT-LLM | 2017/2023 | LLM 2~8x 추론 가속 |
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
| Quantum-X 800G | 2024~25 | InfiniBand 차세대 |
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

**Google TPU = 최대 위협**. v7 Ironwood가 Blackwell과 격차 거의 해소, **Anthropic에 1M+ 유닛 + 1GW 이상 컴퓨트 배포** 계약. Google은 2026 4.3M → 2027 10M → 2028 35M TPU 출하 목표. 일부 분석은 **NVIDIA 추론 점유율 2028년까지 90%+ → 20~30% 급락 가능** 경고.

---

## 6️⃣ 중국 시장 — 구조적 차단

| 시점 | 조치 | 영향 |
|---|---|---|
| 2022.10 | A100/H100 금지 | A800/H800 우회 |
| 2023.10 | A800/H800·L40S 차단 | H20·L20·L2로 추가 우회 |
| **2025.4.15** | **H20 금지** (트럼프 2기) | **Q1 FY26 $4.5B 재고 상각** |
| 2025 하반기 | H200 제한적 허용 논의 | 월 출하 한도 |
| 2026.4 | H200 중국 75K 상한 + 25% 세금 | JPM "연 $16B 매출 잠재 손실" |

**중국 매출 비중**: 2023 ~21% → 2024 17% → **2025 ~13%** → 2026E <10%. 중국 DC 매출 2025 H2 기준 YoY -45%.

**중국 대체품**: **Huawei Ascend 910C** (2025 생산 100K, 910B 300K), Biren BR100, Cambricon MLU370. 910C는 H200 대비 FP8 성능 ~45%, 메모리 대역폭 50%. **중국 내 대형 AI 랩 기본 훈련 가속기**로 자리.

---

## 7️⃣ 재무 상세

### 분기별 추이

| 분기 | 매출 | DC | YoY | Non-GAAP GM |
|---|---|---|---|---|
| FY25 Q4 | $39.3B | $35.6B | +78% | 73.5% |
| FY26 Q1 | $44.1B | $39.1B | +69% | 61% (H20 $4.5B 상각) |
| FY26 Q2 | $46.7B | $41.1B | +56% | 72.7% |
| **FY26 Q3** | **$57.0B** | **$51.2B** | **+62%** | **73.6%** |
| FY26 Q4 가이던스 | $65.0B | - | ~+60% | ~73.5% |
| **FY26 연간 추정** | **~$213B** | ~$190B+ | +63% | ~72% |

### 자본 배분
- **자사주 매입**: FY25 $34B, FY26 $60B+ 신규 권한
- **현금·단기투자**: FY26 Q3 ~$100B+ (Net Cash)
- **OpenAI 투자**: **최대 $100B 투자 약정** (컴퓨트 10GW 대가) — 역사상 최대 **순환 거래 논란**

---

## 8️⃣ 주가·밸류에이션

| 지표 | 값 (2026.4.22~23) |
|---|---|
| 주가 | **$189.31** (4.13) |
| 시가총액 | **$4.58T** |
| **TTM P/E** | **40.79** |
| **Forward P/E (12M)** | **23.97** |
| 12M 평균 대비 | -12.41% (압축 중) |
| PEG (5yr) | **~0.8** (매력적) |
| EV/EBITDA (fwd) | ~22x |
| **Morgan Stanley PT** | $260 기본 / $330 bull / $150 bear |
| Goldman Sachs PT | $250 (FY27 $380B 매출, 30x fwd P/E) |

**$5T 돌파 시나리오**: 2026 말~2027 초. 전제: (1) FY27 매출 $250B+, (2) Rubin 원활 ramp, (3) 중국 규제 완화, (4) ASIC 침투 완만.

---

## 9️⃣ 리스크

| 리스크 | 심각도 | 타임라인 |
|---|---|---|
| **하이퍼스케일러 ASIC 내재화** (Google/AWS/Meta/MS) | ★★★★★ | 2026~2028 단계적 |
| **CUDA 대안 부상** (Triton, Inductor, MLIR) | ★★★★ | 2027~ 추론 |
| **AI Capex 피크아웃** | ★★★★ | 2027~2028 가능성 |
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

1. **AI Factory ($3~4T TAM by 2030)**: 일반 컴퓨팅 $1T + 가속 컴퓨팅 $3T 병렬 확장
2. **Physical AI**: 로봇(GR00T)·자율주행(Drive Thor)·디지털 트윈(Omniverse) — 2030 로봇 $100B+
3. **Sovereign AI**: 각국 자국어·자국 데이터 AI 독립 — 유럽 15, 중동 3, 아시아 주요국
4. **Agentic AI**: 훈련 대비 추론 컴퓨팅 **100~1000배 증가** (Test-time scaling) — FP4 최적화와 정합

---

## 🎯 최종 판단

NVIDIA는 2026.4 현재 **$4.58T · Fwd PER 24x**로 밸류에이션 합리화. FY27 매출 $250~300B 컨센서스면 **$5T 돌파 12~18개월 내** 현실적. 다만 **TPU v7 Anthropic 1M+ 배포** + **OpenAI-NVIDIA $100B 순환 거래** 회계 의문 상존.

### 분기 모니터링 3대 포인트
1. **네트워킹 매출 성장률** 지속 여부
2. **하이퍼스케일러 ASIC 비중** 공시
3. **Rubin R100 양산 일정** 미끄러짐

**단기 R/R 중립~긍정** (FY27 가이던스 업사이드), **중기 (2027~2028) ASIC 침투 속도 결정 변수**. Jensen의 "AI Factory $3~4T TAM" 서사 유지 시 프리미엄 정당화, but **추론 점유율 2028까지 70%+ 방어**가 장기 투자 논거 핵심.

---

## 밸류에이션 — 어떻게 평가하나 + 현재 위치

> **작성 시점:** 2026-04-28 기준 공개 자료 + 컨센서스를 바탕으로 한 추정. 실시간 시세와 차이 가능. 매매 전 IR/공시 재확인 필수.

### 이 회사(섹터)는 무슨 잣대로 보나?

**쉽게 말하면**: 동네 식당이 1년에 100만원 벌고 가격이 2,500만원이면 P/E 25배. NVIDIA는 1년에 약 $130B(약 180조원)을 벌고 시가총액이 $4.58T(약 6,400조원)이니 **TTM P/E 약 41배** — "지금 사면 41년치 이익에 해당하는 가격"이라는 뜻.

근데 NVIDIA는 **이익이 매년 60~100% 폭증** 중이에요. 그래서 "올해 이익"이 아니라 **"내년·내후년 이익"** 으로 환산해야 합니다 → **Forward P/E 24배**. 즉, "1년 후 기준으로 보면 24년치"로 떨어져요.

식당 비유로 다시: "이 식당 작년엔 100만 원 벌었지만 올해 200만 원, 내년 350만 원 벌 거 같아요"라면 가격 2,500만 원도 합리적일 수 있죠. NVIDIA는 그 식당의 글로벌 빅테크 버전.

**조금 더 들어가면**: AI 빅테크 같은 초고성장 회사는 **PEG (Price/Earnings ÷ Growth)** 가 핵심 잣대. P/E 40배여도 성장률 50%면 PEG = 0.8 → "성장 대비 싸다"고 봐요. NVIDIA는 PEG ~0.8로 **여전히 매력 구간**.

추가로 **FCF Yield (잉여현금흐름 수익률)** — "1년에 회사가 벌어들이는 진짜 현금이 시총의 몇 %인가". NVIDIA FCF Yield 약 2.5~3% → 미국 10년물 국채 수익률(약 4%)에는 못 미치지만, 성장 프리미엄을 합치면 균형.

**전문가 관점**: NVIDIA는 **AI 슈퍼사이클의 중앙 자산** — 단일 멀티플보다 **(1) Forward P/E (2) PEG (3) EV/EBITDA (4) FCF Yield** 4축으로 동시 진단. 2024년 P/E 70~80배 → 2026.4 현재 24배로 **반토막 압축** 진행 중. 이는 주가 하락이 아니라 **이익 폭증 속도가 주가 상승을 추월**했다는 의미 (좋은 종류의 압축).

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
| **NVIDIA (NVDA)** | **~$4.58T** | **40.79** | **23.97** | **~22x** | 30-40x | **90%+** | 약 40x (변동 큼) | **5년 평균 대비 -40% 압축** |
| AMD | ~$320B | ~85x | ~28x | ~22x | ~5x | 7-9% | 약 35x | 5년 평균 부근 |
| Broadcom (AVGO) | ~$1.2T | ~55x | ~30x | ~25x | ~10x | 30%+ | 약 25x | 5년 평균 상단 |
| TSMC | ~$1.92T | ~28x | ~22-25x | ~13-15x | 6-7x | 28-30% | 약 18x | 5년 평균 상단 |
| S&P500 | - | ~28x | ~20x | ~14x | ~4x | 18% | ~22x | 평균 부근 |

> **핵심**: NVIDIA는 **Forward P/E 24x로 사상 최저 수준의 압축** 중. 동종 AI 칩 그룹(AMD 28x, AVGO 30x)보다 오히려 저렴 — "1등주가 더 싸다"는 역설.

### 역사 밴드에서 어디 있나?

**쉽게 말하면**: NVIDIA P/E 밴드는 **2020~24년 50~80배 (AI 붐 초기 프리미엄)** → **2025~26년 40배 → 24배로 압축**. **5년 평균 P/E 약 40배 대비 현재 24배는 약 -40% 디스카운트** 위치.

**왜 압축됐나?** (역설적이지만 좋은 신호):
1. **이익 폭증 속도 > 주가 상승 속도** — FY25 매출 $130.5B (+114%), FY26E $213B (+63%) — 분모(이익)가 분자(주가)보다 더 빨리 자라며 멀티플 자동 압축.
2. **TPU·Trainium 등 ASIC 위협 우려 반영** — 미래 점유율 하락 시나리오 일부 디스카운트.
3. **OpenAI $100B 순환 거래 회계 의문** — 일부 투자자 보수적 접근.

**전문가 관점**: Morgan Stanley PT **$260 (Bull $330, Bear $150)**, Goldman PT $250 (FY27 매출 $380B, 30x fwd P/E 가정). 컨센서스 평균 PT 대비 현재가 **+30% 상방 여력**. 단, 2027~28년 ASIC 침투 속도가 장기 PER 결정 변수.

### Bull / Base / Bear 멀티플 시나리오

| 시나리오 | 가정 | 적용 Forward P/E | FY27E EPS (가정) | 주가 함의 |
|---|---|---|---|---|
| **Bull** | FY27 매출 $300B+, 추론 점유율 80%+ 방어, Rubin Ultra Kyber 양산 순항, 중국 규제 부분 완화 | **35x** | $9.0 | **~$315 (+66%)** |
| **Base** | FY27 매출 $250~280B, ASIC 침투는 점진적, Rubin 정상 ramp | **28x** | $7.5 | **~$210 (+11%)** |
| **Bear** | TPU v7 추론 시장 30%+ 잠식, AI Capex 피크아웃 시그널, OpenAI 거래 회계 이슈 | **18x** | $6.0 | **~$108 (-43%)** |

> **핵심 변수**: ① **하이퍼스케일러 ASIC 비중 공시** (분기별), ② **Rubin R100 양산 일정** (2026 H2), ③ **네트워킹 매출 성장률** (Mellanox·Spectrum-X), ④ **중국 H200 75K 상한 + 25% 세금 조건** 영구화 여부.

### ⚠️ 이 매트릭스를 볼 때 주의

- 본 매트릭스는 작성 시점(2026-04-28) 기준 공개치 + 컨센서스 추정. 실시간 시세와 다를 수 있음.
- NVIDIA의 P/E는 **분기별로 30~50% 출렁임** (이익 가이던스 변경 영향) — 단일 시점 멀티플은 스냅샷일 뿐.
- **OpenAI $100B 투자 약정**의 회계 처리 방식은 2026년 SEC·감사인 이슈로 부상 가능 → 발생 시 EPS 추정 재산정 필요.
- 동종 비교(AMD·AVGO·TSMC)는 **사업모델 상이** — NVIDIA의 CUDA moat·네트워킹 통합·풀스택 솔루션은 단순 멀티플로 환산 어려움.
- **AI 사이클 산업의 장기 멀티플은 "정점에서 반토막"이 흔함** — 1990~2000 닷컴, 2010~2018 반도체 사이클 모두 P/E 50x → 15x 압축 사례 존재. NVIDIA가 다르다고 보장 없음.

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
