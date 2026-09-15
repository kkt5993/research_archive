# semianalysis-theinformation — next-chat handoff
Read this first via `gh` from public `kkt5993/research_archive`. Do not clone. Do not dump old chats.

## Role
SemiAnalysis (and SA-primary only) AI-infra briefs in Korean house format: claim / mechanism / skeptic / 2–3Q falsifiers / investment translation.
Report status/results/blockers to **orchestrator**, not advisor.

## Do-nots
- News articles (The Information, Reuters, Bloomberg, TechTimes, etc.)
- Git clone; overwrite or full-rewrite of archive notes; extra dated parallel notes; extra folder layers
- Data-center satellite (데이터센터 감시 봇); tweet scraping (x-scraper); lab P&L core (AI 모델 수익성); HBM bottom-up (AI 메모리 수요)
- Wait on the user for topic/account/routine confirmation if public SA-primary work remains
- Ping the datacenter bot

## Archive to read first
- `10_국내주식/22_반도체/AI_Capex_피크시그널.md`
- `10_국내주식/22_반도체/HBM_완전정복_개념구조작동원리세대.md`
- `10_국내주식/22_반도체/HBM_바텀업_가격매출이익모델.md`
- `10_국내주식/22_반도체/CoWoS_첨단패키징병목_완전해부.md`
- `10_국내주식/22_반도체/구글TPU_향후전망_다각도분석.md`
- `NVIDIA` path: `20_미국주식/4530_반도체와반도체장비/NVIDIA_분석리포트.md`
- `01_거시전략/AI데이터센터_전력병목_생산유통사용_1편.md` (and 2–3편)
- `20_미국주식/4510_소프트웨어와서비스/소프트웨어와서비스_산업구조.md`

## Watchlist
- Weekday 08:30 KST ai-infra routine (source stack: archive → SA primary → OpenAI/Anthropic/xAI blogs → x-scraper)
- 2027Q1 HS capex guidance (peak-out observation point, not token-OP start)
- CUDA vs ASIC inference leak vs training hold
- NVDA financier / LPS-shell vs GPU put (PORTS-Pike)

## Open hypotheses
- Announced GW ≠ construction (Epoch dirt-started vs live IT)
- 2028 in archive is capex/COD/depreciation, not HS token-factory OP start
- Labs-capture vs China OSS is mix/SKU, not a dated OP break

## Next actions
1. Next SA-primary brief on whatever new SA piece exists; if none, stay quiet (routine).
2. Append only deltas into existing sector files. En dash, not tilde. KR=WI26 `10_국내주식`, US=GICS25 `20_미국주식`.

## Last confirmed (date these)
- Routine ai-infra weekday 08:30 KST armed as folder `ai-infra-08-30-weekday-brief` (2026-09-01 evening KST)
- CUDA vs ASIC, NVDA financier, Epoch satellite overlay shipped in chat 2026-09-01
- SA 8/30 neocloud-security (ClusterMAX 3.0 preview) absorbed into NVIDIA 사후 검증 2026-09-01; Jalapeño already in the earlier NVIDIA block
- SA 9/1 Korea sovereign AI (Nvidia Wins, Hynix Loses) absorbed into NVIDIA / SK하이닉스 / AI_Capex 사후 검증 **2026-09-02**; paywalled Memory·Datacenter Model detail missing — not invented
- **2026-09-07 08:30 KST routine:** newsletter archive + feed checked — no SA-primary newer than Korea 9/1; **ClusterMAX 3.0 full still NOT out**; quiet (no brief, no user ping)
- **2026-09-08 08:30 KST routine:** SA 9/7「TPU Inference Externalization Full Steam Ahead - InferenceX」흡수 — NVIDIA / 구글TPU / AI_Capex 사후 검증 append. Ironwood FP8 agg vs B200/B300 최대 ~50% perf/$; TorchTPU OSS ~10월 중순; FP4·외부 disagg는 아직 NVDA; ClusterMAX 3.0 본편 still NOT out. TCO/Accelerator Model 표 페이월 — 발명 안 함.
- **2026-09-10 08:30 KST routine:** SA 9/9「Where Does a Robot Think – On-Device vs Datacenter Inference」흡수 — NVIDIA / 휴머노이드 / AI_Capex 사후 검증 append. Cascade(planning DC + action onboard) 불가피; Thor≈B200 1/10·B300 ~1/14; silicon/DRAM 교차 ~7/~5 robots/GPU; B300×7 robots(p99 1.16s). **B300 vs 56 Thor TCO·Factories To Caves 페이월** — 발명 안 함. ClusterMAX 3.0 본편 still NOT out.
- **2026-09-11 08:30 KST routine:** SA 9/10「What is So Hard About Behind-The-Meter Power For Datacenters? Part 1」흡수 — 전력병목 3편(본문)·1편(교차)·AI_Capex 사후 검증 append. binding BTM ~75GW(Q2 ~20GW); YE US BTM IT ~3GW; 터빈 매진→레시프/Bloom/EaaS; Jupiter NM stay·Green Chile 지연. **Energy/Datacenter Model 표 페이월** — 발명 안 함. ClusterMAX 3.0 본편 still NOT out.
- **2026-09-14 08:30 KST routine:** SA 9/11「Nvidia’s Backstop Universe」+ SA 9/13「Long Live the Short King: Why 4-hi HBM Wins」흡수 — NVIDIA / AI_Capex / HBM_완전정복 / HBM_바텀업 / SK하이닉스 사후 검증 append. Backstop: 오프BS $530B·PORTS-Pike LPS $108.5B(4.25GW)·AICP $36B(일시중단)·residual ≤25%. 4-hi: Rubin Ultra 192GB·대역폭 불변·추론 $/BW 최적; Memory Model 공급사 표 페이월 — 발명 안 함. **ClusterMAX 3.0 본편 still NOT out**; BTM Part 2 still NOT out.
- **2026-09-15 08:30 KST routine:** SA 9/14「Rubin NVL72 Agentic Inference: 67x better Performance per Dollar」+ SA 9/14「A Brain Too Big to Carry」(Robot Think 개정) 흡수 — NVIDIA / AI_Capex / 휴머노이드 사후 검증 append. Rubin AgentX: owning 170 TPS ~67× vs GB300 TRTLLM(실서빙 60–100 TPS는 1.4–3×); ~7× tok/s/MW vs Jensen 3× 샌드백; GW당 모형이익 +42%(75 TPS); DSX MaxLPS; Vera tray LPDDR 1.5TB(반감 상세 페이월). Robot 개정: 공개 TCO로 오프로드 ~46% TCO/PFLOP(산업)·손익분기 ~5 robots/B300·B300 12 robots/GPU; BD System2=TPU. **ClusterMAX 3.0 본편 still NOT out**; BTM Part 2 still NOT out.
- **2026-09-16 08:30 KST routine:** SA 9/15「Everyone Says Datacenter Moratoriums Are Killing the US Buildout. We Mapped All 300 of Them」흡수 — AI_Capex / 전력병목 1편(교차) / 전력병목 3편 사후 검증 append. 공개: 2027 인도 IT +38GW(22GW 수직); 정책 지연 ~2.3GW(로컬 1.525GW·3프로젝트 + NY ~0.8GW); 노출~20GW≠지연; TX 큐 pause→BTM 순증; 주법 13건 사망. **프로젝트 전수·승자/패자·Model 표 페이월** — 발명 안 함. **ClusterMAX 3.0 본편 still NOT out**; BTM Part 2 still NOT out.
- Paywalled SA/Dwarkesh fetches were sign-in pages — treat those tables as missing unless SA-primary/archive
- Next SA triggers: **ClusterMAX 3.0 본편**; BTM Part 2 / winners-losers if unlocked; TPU disagg vs GB300 NVL72 follow-up; AgentX TPU; vLLM/SGLang Rubin AgentX; TorchTPU OSS (~PyTorch Conference); PowerX/MaxLPS finer GW; Vera LPDDR 반감·수명주기 레비뉴 if unlocked; Backstop Model charts / AICP restart; 4-hi Memory Model supplier tables if unlocked; Moratoriums Tab project deep-dives / winners if unlocked
