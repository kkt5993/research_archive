# 🕸️ AI 데이터센터 풀 스택 가치사슬 맵 (메타 분석)
**작성일: 2026-04-24 | 1GW AI DC 1기 = 무엇이 필요한가**

> **이 리포트는 무엇인가**: 지금까지 쓴 개별 리포트들 (반도체·전력기기·NAND·한국카본·삼성전기·Navitas·Ondas·방산·조선)이 사실 **AI DC 생태계의 조각들**. 이 리포트는 그것들을 **14개 Layer로 꿰어서 한 눈에 보는 지도**. AI 인프라 투자의 구조를 이해하고 **어느 레이어에 한국이 강하고 약한지**를 명확히 하기 위한 메타 분석.

---

## 🟢 시장 상황 (2026-08-28) — 최신

**KOSPI 6,788.88 · KOSPI200 1,065.70 · KOSDAQ 838.41** (2026-08-28 종가).
1개월 전(2026-07-29) 대비 KOSPI +19.9% · KOSPI200 +20.1% ·
KOSDAQ +26.5%. 7월의 사상 최대 낙폭 뒤 되돌림이 진행 중이다 —
수집 구간(6/1–8/28) 안에서 코스피는 2026-07-30 **5,593.56** 가 저점,
2026-06-22 **9,114.55** 가 고점이고 지금은 저점 대비
+21.4%, 고점 대비
-25.5% 다.

**이 폴더의 종목 표와 컨센서스는 2026-08-28 기준으로 다시 만들었다** —
`_시총상위_종목표.md` 와 `<업종>_코스피200_종목분석.md`. 업종 축은 **WI26** 이고
배정은 미니 PG `sector_map`(QuantiWise WI26)을 그대로 따른다.
전체 유니버스와 이동 내역은 [`_코스피200_유니버스.md`](../_코스피200_유니버스.md).

> **주가는 2026-08-28, QuantiWise 컨센서스는 2026-07-30 다.** 그 사이 한 달의 시차가 있다.
> 선행 배수가 낮아 보이는 종목 중 일부는 컨센이 아직 안 내려온 것이다.

## 시장 상황 (2026-08-11) — 이전 스냅샷

**2026년 7월 코스피 −22.19%(사상 최대 월간 낙폭), 코스닥 −21.44%.** 6월 고점 9,385 → 7/30 5,593 붕괴 → **7/31 하루 +17.91% 사상 최대 반등** → 8/10 코스피 **6,306.33** / 코스닥 **807.66**. 7/7·7/28–29 서킷브레이커.

**원인**: 메타 네오클라우드 발표("AI 연산 과잉 → 메모리 수요 종료" 해석) · CXMT 상장 · 미 국채금리 급등(10년 4.65%·30년 5.19%) · 레버리지 청산.

**역설**: 같은 분기 실적은 사상 최대 — 삼성전자 2Q 영업이익 **89.5조**(+1,813.8%, DS 99.7%), SK하이닉스 **60.5조**(OPM 76%). **이익이 아니라 이익의 지속성에 매겨진 멀티플이 무너졌다.**

**구조 변화**: 2026-06-22 **SK하이닉스가 시총 1위**(25년 7개월 만) · 8월 첫주 대순환매(SK하이닉스 −17.2%·삼성전자 −12.0% vs KAI +21.1%·한화에어로 +19.6%) · 원/달러 1,548.8→1,409.9 · 공매도 2025-03-31 전면 재개 · MSCI 2026-06-23 신흥시장 유지. **미국은 사상 최고(S&P 7,757.64), 하이일드 2.70%·VIX 15.46 — 시스템 위기가 아닌 한국 고유 쏠림 해소.**

> **본문의 주가·목표가·밸류에이션은 전부 재확인 대상.** 실측은 아래 표 참조. 출처: `90_정기발간/W32·W33`, FRED, KRX.

**반도체**: 엔비디아 차세대 HBM 사양 재검토 보도로 SK하이닉스 압박. 미국 반도체(NVDA +11.6%, MRVL +16.6%)와 디커플링. 이 폴더의 `메모리반도체_급락_다각도해석_2026-07` 등 함께 볼 것.
---

## 🟢 2026-09-01 갱신 — Layer 2–3 메모리 (가속기·HBM·호스트 DRAM)

> 전력·DC 건설·1GW BOM의 GPU 장수는 이 파일 원문 유지. 아래는 **램이 레이어에서 하는 일**만 고침. Feynman GB 미공시.

### Layer 2 가속기 메모리 사다리 (NVIDIA 1차)

| 랙 | HBM | 호스트 LPDDR | fast memory |
|---|---|---|---|
| GB200 NVL72 | 13.4 TB HBM3E | 17 TB | ~30 TB |
| GB300 NVL72 | **20 TB HBM3E** (데이터시트) | 17 TB | **37 TB** |
| Vera Rubin NVL72 | **20.7 TB HBM4** (preliminary) | **54 TB** (36× Vera 1.5 TB) | **75 TB** (DGX) |

Rubin vs **직전 GB300**: HBM **+4%**, LPDDR **+218%**. “세대마다 HBM GB가 뛴다”는 2024–25 스토리의 연장이 아님.

**연산당 비트 [산수]:** Ultra 288 GB / 15 PF NVFP4 = 19.2 GB/PF. Rubin 288 GB / 50 PF = **5.76 GB/PF** (↓ 3.3×). 용량 플랫, 연산만 3.3×.

### Layer 3가 HBM만이 아님

NVIDIA가 동시에 파는 세 통:

1. **핫 KV = HBM4 288 GB** — “unnecessary offload 없이” (Rubin 블로그).
2. **콜드 KV = Vera LPDDR 1.5 TB** — NVLink-C2C로 단일 주소, KV offload (플랫폼 블로그). 마이크론 SOCAMM2 **192 GB 양산**, CPU당 최대 2 TB / 1.2 TB/s (2026-03-16 IR).
3. **더 긴 KV = BlueField-4 ICMS 플래시** — CES: “KV cache cannot be stored on GPUs long term.” 에이전트 세션을 HBM에 안 남김.

**Groq 3 LPX** (nvidia.com/lpx, NVL72 페이지): 256 LPU, SRAM은 **랙 합 128 GB**(칩당 ~500 MB) + **DDR5 12 TB/랙**. 디코드 FFN/MoE → SRAM, 어텐션/KV는 Rubin HBM. 12 TB DRAM = 32 trays × (fabric 최대 256 GB + 호스트 최대 128 GB) ([LPX 블로그](https://developer.nvidia.com/blog/inside-nvidia-groq-3-lpx-the-low-latency-inference-accelerator-for-the-nvidia-vera-rubin-platform/)). HBM을 없애지 않고 DDR5를 **추가**.

### 세션당 비트 vs 연산당 비트 (섞지 말 것)

- Llama 3 70B GQA-8: ~320 KiB/token → 128k KV ≈ 42 GB, 1M ≈ 328 GB BF16. 1M BF16는 Rubin 288에 안 들어감. FP8/NVFP4면 들어감.
- NVIDIA 제품 페이지: 에이전트 “전통 앱 대비 최대 **15× 토큰**”, 티어에 32K/128K/**400K KV**.
- 반대 힘: Llama 4 Scout 10M은 **청크 8192**(10M dense KV 아님). DeepSeek MLA KV **−93.3%**(V2 논문). NVFP4 KV는 FP8 대비 **최대 50%**(NVIDIA).

학습은 여전히 HBM-bound(파라미터당 ~18B + activation, HuggingFace). Rubin은 10T MoE를 Blackwell 대비 **1/4 GPU**로 학습한다고 함 → **같은 잡의 HBM 비트는 줄어들 수 있음**. 산업 비트는 **GPU 대수 × 스택**이 받쳐 줘야 함. AWS는 2027–28에 Blackwell Ultra·Rubin·Rubin Ultra **200만장 추가**(Feynman은 그 문장에 없음).

## 📌 Executive Summary

2026 하이퍼스케일러 4사 + Oracle + xAI/CoreWeave/Nebius 합산 Capex **약 $700B (+36% YoY)**, 이 중 **AI 인프라 $450B**.

**1GW AI DC 1기** 구성에 필요한 것:
- GPU **약 72,000장** (Rubin/B300급)
- HBM **약 28만 stack**
- CoWoS-L **약 8,000장**
- TC 본더 **약 40대**
- 변압기 **약 400기**
- 1.6T 광모듈 **약 24,000개**
- 냉각 용량 **약 1,000 MW 상당 DLC**
- 연간 전력 **14–16 TWh**

```
[Layer 1]  하이퍼스케일러·AI 모델
   │
[Layer 2]  GPU·AI 가속기 ─── (HBM 수요) ───┐
   │                                        │
[Layer 3]  HBM·DDR5·eSSD ◄──────────────────┘
   │
[Layer 4]  CoWoS·OSAT·TC본더 (한미반도체)
   │
[Layer 5]  Foundry (TSMC 2nm/3nm)
   │
[Layer 6]  ASML·LAM·Wafer·GOES
   │
[Layer 7]  Server ODM (MGX·NVL72)
   │
[Layer 8]  FCBGA·MLCC·수동부품
   │
[Layer 9]  전력·변압기 ★최대 병목★
   │
[Layer 10] 냉각 (DLC·Immersion)
   │
[Layer 11] 전력 생성 (SMR·Gas·재생)
   │
[Layer 12] 네트워킹·광모듈·케이블
   │
[Layer 13] DC 부동산·건설
   │
[Layer 14] 사이버보안
```

---

## Layer 1 — 하이퍼스케일러·AI 모델

| 구분 | 핵심 기업 | 2026 Capex | 한국 연결고리 |
|---|---|---|---|
| Top 4 Hyperscaler | Microsoft, Google, Amazon, Meta | **$480B** | 삼성·SK HBM 납품 |
| Oracle | Stargate 주축 | 약 $80B | - |
| Neocloud | CoreWeave, Nebius, Crusoe, Lambda | $80B+ | 한국 IDC 임대 수요 견인 |
| 독립 AI랩 | OpenAI (Stargate), Anthropic, xAI, DeepMind | - | Anthropic-삼성 파트너십 |
| 동남아·중동 | G42(UAE), Humain(KSA) | $50B+ | HD현대일렉 중동 변압기 수주 |

**병목**: Capex 실제 집행률 80–85%에 불과 (변압기·GPU·부지 승인 제약)
**핵심**: OpenAI Stargate ($500B, 5년) = 공급망 전반 발주 피크

---

## Layer 2 — AI 가속기·GPU

| Tier | 기업 | 2026 주력 | 출하(E) |
|---|---|---|---|
| 1 | **NVIDIA** | H200 / B200 / **B300 (Blackwell Ultra)** / **Rubin R100 (2026 H2)** | 650–720만 |
| 2 | **AMD** | MI350 (H1) / MI400 (Q4) | 80–100만 |
| ASIC | Google TPU v7 (Ironwood) | - | 250만 |
| ASIC | AWS Trainium 2/3, Inferentia | - | 150만 |
| ASIC | Meta MTIA v3, MSFT Maia 2 | - | 80만+ |

**HBM 수요 매핑**:
- Rubin: HBM4 8-stack × 36GB = **288GB/unit**
- B300: HBM3E 12-Hi × 8 = 288GB
- TPU v7: HBM3E × 8 = 192GB
- **2026 글로벌 HBM bit +58% YoY**

**ASIC 비중**: 2024 8% → **2026 22%** → Broadcom·Marvell 대수혜

---

## Layer 3 — 메모리 (HBM·DDR5·eSSD) — **한국 독점 영역**

| 세그먼트 | 글로벌 1·2·3위 | 한국 밸류체인 |
|---|---|---|
| **HBM4** | SK하이닉스 **52%** > 삼성 32% > Micron 16% | 한미반도체(TC본더), 피에스케이홀딩스, 이오테크닉스 |
| DDR5 서버 | 삼성 42% > SK 36% > Micron 22% | 심텍·대덕전자(기판) |
| **eSSD (QLC)** | Samsung > Solidigm(SK) > Kioxia/SanDisk | SK하이닉스·삼성전자 |

**→ 🔗 관련 리포트**: [메모리 반도체 공급 병목](메모리반도체_공급병목분석리포트.md), [낸드플래시 심층](낸드플래시_분석리포트.md)

---

## Layer 4 — 후공정·패키징 — **한미반도체 독점 축**

| 공정 | 핵심 기업 | 점유율 |
|---|---|---|
| **CoWoS-L / CoWoS-S** | TSMC | **100% 독점**, 2026 75k wpm |
| SoIC | TSMC | 독점, Rubin·MI400 |
| OSAT | ASE, Amkor, JCET, PTI | - |
| **HBM TC 본더** | **한미반도체** | SK·Micron 독점 (삼성은 + 한화정밀기계) |
| HBM 테스터 | Teradyne, Advantest | - |

**병목**: CoWoS-L 캐파 10–15% 부족 (2026), NVIDIA+AMD+Google 수요 대비
**투자**: 한미반도체 HBM TC 본더 독점, 한화정밀기계 (삼성 2nd source), 이오테크닉스

---

## Layer 5 — 파운드리·로직

| 노드 | TSMC | Samsung | Intel |
|---|---|---|---|
| 2nm (2026) | N2 양산 (Apple·Rubin-Next) | SF2 (H2) | **18A (H1)** |
| 3nm (주력) | N3E/N3P (NVIDIA·AMD·Apple) | SF3 (퀄컴·Tesla Dojo) | - |

TSMC가 AI 가속기 로직 **90%+** 점유. 삼성은 Tesla Dojo·Qualcomm·Preferred Networks 확보. Intel 18A는 MSFT·AWS ASIC 타진.

---

## Layer 6 — 핵심 장비·소재 — **POSCO GOES가 숨은 키**

| 카테고리 | 기업 |
|---|---|
| **EUV·High-NA EUV** | **ASML 독점** (2026 High-NA 약 20대) |
| Etch·Deposition | Lam, AMAT, TEL |
| Metrology | KLA |
| **Wafer (300mm)** | 신에츠, SUMCO, SK실트론 |
| **GOES** (전기강판) | **POSCO**, Nippon Steel, JFE |
| Photoresist | JSR, TOK, Shin-Etsu |
| 한국 소부장 | 원익IPS, 주성, 동진쎄미켐, SK엔펄스 |

**병목**: High-NA EUV 리드타임 30개월 + GOES 2028까지 타이트
**투자**: POSCO GOES 증설 (광양 50만→80만톤) = **Layer 9 변압기 병목 해소 레버**

---

## Layer 7 — 서버 시스템·ODM

| 기업 | 역할 |
|---|---|
| Supermicro | DLC 랙 선도 |
| Dell, HPE | 엔터프라이즈 |
| **Foxconn** | NVIDIA 최대 ODM, GB200/GB300 NVL72 |
| Quanta, Wistron, Inventec | 하이퍼스케일러 ODM |

NVIDIA **MGX** = 오픈 모듈러 표준. NVL72 (랙당 72 GPU, 120–140kW). **Rubin NVL144 랙당 230kW+**.

한국: 제이케이(섀시·칠러), 이엘씨(전원·커넥터), 케이아이엔엑스, 삼성SDS/LG CNS

---

## Layer 8 — 기판·수동부품 — **삼성전기 수혜**

| 부품 | Top 기업 | 한국 |
|---|---|---|
| **FCBGA (AI GPU)** | Ibiden, Unimicron, Shinko, AT&S | **삼성전기 (세계 3위)**, 대덕전자, 심텍 |
| **MLCC** | Murata, **삼성전기**, TDK, Taiyo Yuden, Yageo | - |
| 파워 인덕터 | Vishay, Murata, TDK | 삼성전기 (신사업) |

AI 서버 1대당 MLCC **3–4만개** (일반 서버 ×3–4배), GPU당 파워 인덕터 50–80개. **Rubin 130×130mm 초대형 FCBGA** 요구.

**→ 🔗 관련 리포트**: [삼성전기 심층 분석](../21_IT하드웨어/삼성전기_분석리포트.md)

---

## Layer 9 — 전력·변압기 ⭐⭐ **AI DC 최대 병목 + 한국 최대 강점**

### GSU 변압기
| 기업 | 국가 | 2026 수주잔고 |
|---|---|---|
| **HD현대일렉트릭** | KR | **$5.5B+** (AI DC +80% YoY) |
| **효성중공업** | KR | $4B+ |
| **LS ELECTRIC** | KR | $3B+ |
| Hitachi Energy | CH/JP | - |
| Siemens Energy GT | DE | - |
| GE Vernova | US | - |

### UPS·배전반
Vertiv · Eaton · Schneider · LS ELECTRIC · Delta

### 800V HVDC 아키텍처 (NVIDIA 2025.5)
Rubin Ultra / Kyber 랙부터 **800V DC** 채택 → GaN/SiC Power 수혜
- **GaN**: Navitas Semi, Power Integrations, Infineon
- **SiC**: Infineon, onsemi, STMicro, Wolfspeed

**병목**: 변압기 리드타임 **2–3년** → 신규 DC 착공 최대 장애
**투자**: 한국 3사 수주잔고 **2028년까지 완판**, 2026 ASP +15–20% 반영

**→ 🔗 관련 리포트**: [전력기기 v2 (글로벌 경쟁력)](../06_기계/전력기기_산업분석리포트_v2.md), [Navitas 분석](../../20_미국주식/4530_반도체와반도체장비/Navitas_분석리포트.md)

---

## Layer 10 — 냉각 (Cooling) — **2025 $5B → 2028 $22B (CAGR 60%)**

| 방식 | 기업 | 한국 |
|---|---|---|
| **DLC** | Vertiv, Motivair, CoolIT, Asetek, Boyd | 한양이엔지, GST |
| Immersion | GRC, LiquidStack, Submer | SK엔무브 |
| **CDU** | Vertiv, Boyd, Delta, Motivair | **산일전기**, 한양이엔지 |
| Cold Plate | Cooler Master, AVC | - |
| 칠러 | Johnson Controls, Trane, **LG전자 HVAC** | LG전자 |

NVL72 **순수 공냉 불가** → 랙 DLC 필수. Rubin NVL144 (230kW+) → **100% DLC**.

**LG전자 HVAC** (ES 부문) DC 칠러·터보냉각기 전략 피봇.

---

## Layer 11 — 전력 생성·PPA — **두산에너빌리티 + 한국카본 수혜**

| 전원 | 핵심 기업 | 2030 AI DC 기여 |
|---|---|---|
| **SMR** | NuScale, X-energy, Rolls-Royce, TerraPower, **두산에너빌리티**, Oklo | 10–30GW |
| 가스터빈 | **GE Vernova**, Siemens Energy, Mitsubishi Power | **50GW+** (최대) |
| LNG | Cheniere, Venture Global | **한국카본** Mark III 간접 수혜 |
| 재생E | NextEra, Orsted | 30GW |
| ESS | Tesla Megapack, Fluence, **LG엔솔, 삼성SDI** | 100GWh+ |

**→ 🔗 관련 리포트**: [SMR 산업 분석](../06_기계/SMR_산업분석리포트.md), [한국카본 v2](../07_조선/한국카본_분석리포트_v2.md)

---

## Layer 12 — 네트워킹·광모듈·케이블

| 카테고리 | Top 기업 |
|---|---|
| 스위치·라우터 | Arista, Cisco, Juniper, NVIDIA (Spectrum-X·Quantum-X) |
| **광 트랜시버 (1.6T)** | Coherent, Lumentum, InnoLight, Eoptolink, Accelink |
| DSP | Broadcom, Marvell |
| DAC·AOC | Amphenol, TE Connectivity, Luxshare |
| **파워/데이터 케이블** | Prysmian, Nexans, **LS전선·LS마린솔루션** |
| CPO (2027~) | TSMC + Broadcom + NVIDIA |

Rubin NVL144 기준 **800G → 1.6T** 광모듈, 랙 간 구리 → 광 전환. LS전선 해저 케이블 + 미 버지니아 지중 공장.

---

## Layer 13 — DC 부동산·건설

| 기업 | 성격 |
|---|---|
| **Digital Realty (DLR)** | 글로벌 DC REIT 1위 |
| **Equinix (EQIX)** | 인터커넥션 허브 |
| **AirTrunk** (Blackstone) | 아·태 하이퍼스케일 |
| NTT GDC, CyrusOne | - |
| EPC | Turner, AECOM, Fluor, Jacobs |
| 한국 | SK에코플랜트 DC, KT IDC, 네이버각, 카카오 안산, 삼성물산·현대건설·GS건설 |

**2026 글로벌 DC 착공 52GW** (CBRE), 북미 주요 허브 공실률 **<1%** 지속.

---

## Layer 14 — 사이버보안

Palo Alto, CrowdStrike, Zscaler, Wiz (Google 인수), 한국: 안랩, SK쉴더스

---

## 🇰🇷 한국 기업이 가장 강한 7개 Layer — 요약표

| 순위 | Layer | 핵심 한국 기업 | 글로벌 위상 |
|:---:|---|---|---|
| **1** | Layer 3 HBM | SK하이닉스, 삼성전자 | **Top 2 합산–84%** |
| **2** | Layer 9 전력·변압기 | HD현대일렉, 효성중, LS ELECTRIC | 북미 초고압 Top 3 |
| **3** | Layer 4 HBM 후공정 | **한미반도체**, 한화정밀, 이오테크닉스 | **독점** |
| **4** | Layer 8 기판·MLCC | **삼성전기**, LG이노텍, 대덕전자 | FCBGA Top 5, MLCC Top 2 |
| **5** | Layer 11 SMR·LNG | **두산에너빌리티**, 한국카본, LS마린 | SMR 주단조 세계 최대급 |
| **6** | Layer 6 소재 | **POSCO (GOES)**, SK실트론, 동진쎄미켐 | GOES Top 3 |
| **7** | Layer 12 케이블 | **LS전선**, 대한전선 | 해저·지중 Top 5 |

**추가**: Layer 10 (냉각)에서 **LG전자 HVAC·산일전기·한양이엔지** 2026–2027 리레이팅 후보

---

## 🎯 투자 시사점

### 1GW AI DC 1기를 가동하려면 한국 밸류체인에서:
1. **GPU 72,000장 + HBM 28만 stack** → SK·삼성 (Layer 3)
2. **CoWoS-L 8,000장 + TC 본더 40대** → 한미반도체 (Layer 4)
3. **변압기 400기 + UPS 120MW** → HD현대일렉·효성·LS (Layer 9)
4. **DLC CDU 200대** → 산일전기·한양이엔지·LG전자 (Layer 10)
5. **SMR 300MW or 가스 500MW PPA** → 두산에너빌리티 (Layer 11)
6. **1.6T 광모듈 24,000개 + 지중케이블 200km** → LS전선 (Layer 12)

### 리레이팅 우선순위
1. **🥇 Layer 4 한미반도체** — CoWoS 패키징 독점 축, 대체 불가
2. **🥈 Layer 9 HD현대일렉트릭** — 2028년까지 수주 예약, 반도체 cycle 독립
3. **🥉 Layer 11 두산에너빌리티** — SMR 주단조 독점, 2026–2030 폭발
4. **Layer 3 SK하이닉스** — HBM M/S 1위 (이미 시장 반영)
5. **Layer 8 삼성전기** — FCBGA AI 가속기 2차 공급자 (최근 급등)

### 핵심 트래킹
- **CoWoS capacity 증설 속도** (TSMC 분기 실적)
- **HBM4 양산 수율** (SK/삼성/Micron)
- **변압기 납기** (현재 128주, 정상화 시점)
- **전력기기·SMR 신규 계약** (분기별 공시)

---

## 📚 Sources

- [Morgan Stanley AI Infrastructure Capex 2026](https://www.morganstanley.com/ideas)
- [Goldman Sachs Research — Hyperscaler Capex](https://www.goldmansachs.com/insights)
- [SemiAnalysis — AI Accelerator Model 2026](https://www.semianalysis.com)
- [SemiAnalysis — CoWoS Capacity Update](https://www.semianalysis.com)
- [TrendForce — HBM Market Report 2026](https://www.trendforce.com)
- [DigiTimes — FCBGA & ABF Substrate 2026](https://www.digitimes.com)
- [IEA — Electricity 2026, Data Centres and AI](https://www.iea.org/reports/electricity-2026)
- [Dell'Oro — Data Center Liquid Cooling 2026](https://www.delloro.com)
- [CBRE — Global Data Center Trends 2026](https://www.cbre.com)
- [NVIDIA GTC 2025 Keynote — 800V HVDC Architecture](https://www.nvidia.com/gtc)
- [ASML Investor Presentation Q4 2025](https://www.asml.com/en/investors)
- [TSMC Q4 2025 Earnings](https://investor.tsmc.com)
- [SK hynix IR Q4 2025](https://www.skhynix.com/eng/ir)
- [HD Hyundai Electric IR](https://www.hd-hyundaielectric.com)
- [한미반도체 IR](https://www.hanmisemi.com)
- [두산에너빌리티 IR](https://www.doosanenerbility.com)
- [LS전선 IR](https://www.lscns.com)
- [삼성전기 IR](https://www.samsungsem.com)
- [Reuters — Global transformer shortage through 2028](https://www.reuters.com)
- [Bloomberg NEF — Data Center Power Demand 2030](https://about.bnef.com)

---

### ⚠️ 주의
- 본 메타 분석은 2026-04-24 시점. 하이퍼스케일러 Capex·GPU 로드맵·공급 병목은 분기 단위 변동.
- Layer별 M/S·수주잔고·가격은 민간 리서치 (Wood Mackenzie, SemiAnalysis, TrendForce) 추정치 포함.
- 각 Layer는 개별 리포트를 통해 심층 분석되어 있으므로, 특정 테마 집중 시 해당 리포트 참조.
