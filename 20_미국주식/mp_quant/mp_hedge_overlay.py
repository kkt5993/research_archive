#!/usr/bin/env python3
"""MP v4.7 헤지 오버레이 — 넷 익스포저 밴드별 샤프 재계산 (실측 시계열 기반).

기존 문서의 '넷 60–80%면 E[r] −2~3%p에 σ −6~8%p'는 가정이었다. 여기서는 2년 실측
일별 수익률에 QQQ 숏을 h만큼 얹어 σ·베타·MDD·VaR를 직접 계산한다.
  실행: ssh mini-lan 'cd ~/research_archive/20_미국주식/mp_quant && python3 mp_hedge_overlay.py'
"""
import math, sys
import numpy as np, pandas as pd, yfinance as yf

RF = 0.0372          # 13주 T-bill 실측 (mp_quant_metrics.py 산출)
E_MP = 0.097         # 시나리오 확률가중 기대수익 (리스크 문서 §2 — 전방 판단, 실측 대상 아님)
E_BM = 0.095         # BM 기대수익 가정 9–10% 중앙
COST = 0.004         # 헤지 실행비용 연 0.4%p (선물 롤·스프레드, 넷 100% 헤지 기준 비례)

W = pd.read_csv('mp_v47_weights.csv')
held = W[W.mp_weight > 0]
px = yf.download(list(held.ticker) + ['QQQ'], period='2y', interval='1d',
                 auto_adjust=True, progress=False)['Close']
rets = px.pct_change().dropna(how='all')
avail = [t for t in held.ticker if t in rets.columns and rets[t].notna().sum() > 250]
w = held.set_index('ticker').loc[avail, 'mp_weight']; w = w / w.sum()
both = pd.concat([(rets[avail] * w).sum(axis=1), rets['QQQ']], axis=1).dropna()
both.columns = ['p', 'b']

def mdd(s):
    cum = (1 + s).cumprod()
    return float((cum / cum.cummax() - 1).min())

rows = []
for net in [1.00, 0.80, 0.70, 0.60, 0.50]:
    h = 1 - net                                   # QQQ 숏 비율
    r = both.p - h * both.b                       # 숏 담보의 rf 수익은 아래 기대수익에서 반영
    vol = float(r.std()) * math.sqrt(252)
    beta = float(r.cov(both.b) / both.b.var())
    te = float((r - both.b).std()) * math.sqrt(252)
    er = E_MP - h * (E_BM - RF) - h * COST        # 숏은 (BM−rf)만큼 잃고 실행비용을 더 낸다
    rows.append(dict(net=net, h=h, er=er, vol=vol, beta=beta, te=te,
                     sharpe=(er - RF) / vol, mdd=mdd(r),
                     var95=float(r.quantile(0.05)), var99=float(r.quantile(0.01)),
                     real_sharpe=(((1 + r).prod() ** (252 / len(r)) - 1) - RF) / vol))

# 베타중립(실측 β 1.19 전액 헤지)도 참고로
h = 1.19
r = both.p - h * both.b
vol = float(r.std()) * math.sqrt(252)
er = E_MP - h * (E_BM - RF) - h * COST
rows.append(dict(net=1 - h, h=h, er=er, vol=vol,
                 beta=float(r.cov(both.b) / both.b.var()),
                 te=float((r - both.b).std()) * math.sqrt(252),
                 sharpe=(er - RF) / vol, mdd=mdd(r),
                 var95=float(r.quantile(0.05)), var99=float(r.quantile(0.01)),
                 real_sharpe=(((1 + r).prod() ** (252 / len(r)) - 1) - RF) / vol))

L = ['# MP v4.7 헤지 오버레이 — 넷 밴드별 실측 (2y 일별, QQQ 숏)\n',
     f'가정: rf {RF:.2%} · E[MP] {E_MP:.1%} · E[BM] {E_BM:.1%} · 헤지비용 {COST:.1%}/년(비례)',
     f'가격 커버리지 {len(avail)}/{len(held)}\n',
     '| 넷 | QQQ 숏 | E[r] | 연율 σ | 베타 | TE | **기대 샤프** | MDD(2y) | VaR95 | 실현샤프(백테스트) |',
     '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for x in rows:
    tag = '**베타중립**' if x['h'] > 1 else f"{x['net']:.0%}"
    L.append(f"| {tag} | {x['h']:.0%} | {x['er']:.1%} | {x['vol']:.1%} | {x['beta']:.2f} | "
             f"{x['te']:.1%} | **{x['sharpe']:.2f}** | {x['mdd']:.1%} | {x['var95']:.2%} | {x['real_sharpe']:.2f} |")
open('mp_v47_hedge_overlay.md', 'w').write('\n'.join(L))
print('\n'.join(L))
