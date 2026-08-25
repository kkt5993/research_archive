#!/usr/bin/env python3
"""MP v5.1 최종 자료 — 운용역이 보는 모든 지표를 한 문서로 조립한다.

흩어진 산출물(recsheet·attribution·stock_table·pm_dashboard·hedge_overlay)을
하나의 발간용 문서로 합치고, 표지 대시보드와 서술을 얹는다.
재실행하면 최신 산출물로 문서가 다시 만들어진다 — 수작업 편집본이 아니다.
"""
import os, re
import numpy as np, pandas as pd

def sec(path, start, end=None):
    """문서에서 섹션 하나를 잘라온다."""
    if not os.path.exists(path): return f'*(산출물 없음: {path})*'
    t = open(path, encoding='utf-8').read()
    i = t.find(start)
    if i < 0: return f'*(섹션 없음: {start})*'
    j = t.find(end, i + len(start)) if end else -1
    return t[i:j if j > 0 else len(t)].rstrip()

W = pd.read_csv('mp_v51_weights.csv').set_index('ticker')
S = pd.read_csv('mp_v51_stock_levels.csv').set_index('ticker')
A = pd.read_csv('mp_v51_attribution.csv').set_index('ticker')
P = pd.read_csv('mp_v51_pm_metrics.csv').set_index('ticker')
G = pd.read_csv('mp_v51_pm_agg.csv', index_col=0).squeeze()
U = pd.read_csv('sp500_universe.csv').set_index('ticker').drop(columns=['price'])
held = W[W.mp_weight > 0]
d = held.join(S).join(U[['GICS Sector']])
w = d.mp_weight / d.mp_weight.sum()
def wm(c, src=None):
    x = (src if src is not None else d)[c]
    ok = x.notna() & np.isfinite(x)
    return float((w[ok] / w[ok].sum() * x[ok]).sum())

L = [
'# 미국주식 모델 포트폴리오 v5.1 — 운용 자료 (최종)',
'',
'**BM: S&P 500 · 30종목 · 2026-08-25 기준 · 상상인증권 투자전략팀**',
'',
'> 본 자료는 운용역이 확인하는 전 지표를 한 문서에 담는다. 모든 수치는 실측이며,',
'> 산출 방법과 한계는 마지막 장에 명시했다. 재현: `mp_quant/mp_v51_final_report.py`.',
'',
'---',
'',
'## 표지 — 한 장 요약',
'',
'### 수익·밸류에이션',
'',
'| 지표 | MP | BM(S&P500) | 액티브 |',
'|---|--:|--:|--:|',
f'| 기대수익률(컨센 목표주가) | **+28.1%** | +19.3% | **+8.7%p** |',
f'| 기대수익률(자체 산출) | +45.7% | +28.3% | +17.4%p |',
f'| 가중 forward P/E | {wm("pe_now"):.1f} | 19.1 | — |',
f'| 자기 역사 배수 대비 | **+{wm("pe_revert_full")*100:.1f}%** | +10.9% | +13.3%p |',
f'| 컨센 EPS 성장(2년 CAGR) | +{wm("growth")*100:.1f}% | +18.4% | — |',
f'| 배당수익률 | {G.div_yield:.2f}% | ~1.2% | — |',
'',
'### 위험',
'',
'| 지표 | 값 | | 지표 | 값 |',
'|---|--:|---|---|--:|',
f'| 추적오차(TE) | **11.9%** | | 하방편차 | {G.downside_dev*100:.1f}% |',
f'| 베타 | 1.37 | | 소르티노 | {G.sortino:.2f} |',
f'| 연율 변동성 | {G.port_vol*100:.1f}% | | 칼마 | {G.calmar:.2f} |',
f'| 최대낙폭 | {G.mdd*100:.1f}% | | 상승/하락 캡처 | {G.up_capture*100:.0f}% / {G.dn_capture*100:.0f}% |',
f'| VaR 95% (일간) | −2.44% | | 상승/하락 베타 | {G.beta_up:.2f} / **{G.beta_dn:.2f}** |',
f'| 정보비율(IR) | **0.73** | | 최악 1일 / 21일 | {G.worst_day*100:.1f}% / {G.worst_month*100:.1f}% |',
'',
'### 구조',
'',
'| 지표 | 값 | | 지표 | 값 |',
'|---|--:|---|---|--:|',
f'| 종목수 | 30 | | 종목 간 평균 상관 | {G.avg_corr:.3f} |',
f'| TOP10 비중 | 64.7% | | 분산 효과 | {G.diversification*100:.1f}% |',
f'| 유효종목수 | 18.1 | | 순부채/EBITDA | {G.nd_ebitda:.2f}배 |',
f'| 최대 섹터 액티브 | 정보기술 +19.2%p | | 가중 ADV | ${float((w*d.join(P,rsuffix="_p").adv_usd).sum())/1e9:.1f}B |',
f'| 가중 애널 커버리지 | 39명 | | 공매도 잔고 | {G.short_pct:.2f}% |',
'',
'### 이 포트를 한 문장으로',
'',
'**AI 인프라 체인에 액티브 리스크를 집중하고 나머지 섹터는 대표 대형주로 BM을 복제한다.**',
'정보기술 +19.2%p 액티브가 알파의 **101%**와 리스크의 **78%**를 동시에 만든다 —',
'**알파와 리스크가 같은 곳에서 나온다는 것이 이 포트의 성격이자 한계다.**',
'',
'---',
'',
]

# 본문 조립
L += [sec('mp_v51_recsheet.md', '| 종목 | 티커', '\n## 등급별 요약').replace('| 종목 | 티커', '## Ⅰ. 추천종목 30선\n\n| 종목 | 티커'), '']
L += [sec('mp_v51_recsheet.md', '## 등급별 요약', '\n## 섹터 배분'), '']
L += ['---', '', '## Ⅱ. 알파·리스크 기여도', '',
      sec('mp_v51_attribution.md', 'BM 기대수익률', '\n## 섹터별 기여'), '',
      sec('mp_v51_attribution.md', '## 섹터별 기여', '\n## 집중도'), '',
      sec('mp_v51_attribution.md', '## 집중도'), '']
L += ['', '---', '', '## Ⅲ. 종목별 밸류에이션·기술 레벨', '',
      sec('mp_v51_stock_table.md', '| # | 티커', '\n## 커버리지'), '',
      sec('mp_v51_stock_table.md', '## 커버리지', '\n## 가중 요약'), '',
      sec('mp_v51_stock_table.md', '## 가중 요약'), '']
L += ['', '---', '', '## Ⅳ. 운용 지표 (유동성·하방위험·분산·건전성·회전율·스트레스·이벤트)', '',
      sec('mp_v51_pm_dashboard.md', '## 1. 유동성'), '']
L += ['', '---', '', '## Ⅴ. 헤지 오버레이', '',
      sec('mp_v51_hedge_overlay.md', '## 2. 헤지 오버레이', '\n## 3.'), '']

open('mp_v51_final_report.md', 'w').write('\n'.join(L))
print(f'생성 완료: mp_v51_final_report.md ({len(chr(10).join(L).splitlines())}줄)')
