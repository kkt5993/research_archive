#!/usr/bin/env python3
"""MP v4.7 기대수익·샤프·헤지 오버레이 — 전부 종목별 실측에서 쌓아올린다.

시나리오 확률·수익 가정(E[r] 9.7%)을 쓰지 않는다. 대신:
  기대수익  = Σ w_i · [(1+성장_i)(1+k·배수회귀_i) − 1]
    성장_i     = trailingPE/forwardPE − 1 (컨센서스가 값 매긴 12M EPS 성장)
    배수회귀_i = 자기 역사적 P/E 중앙값/현재 P/E − 1 (분할조정·TTM 보강 시계열)
    k          = 배수 회귀 속도 0 / 0.5 / 1.0
  변동성    = 실측 일별 수익률(2y) — 종목별 변동성·상관이 그대로 들어간다
  BM        = 같은 방식으로 BM 추적분(91.2%)에 적용 → 알파도 실측
기술적 레벨(MA·지지·저항)은 기대수익 대신 **경로 리스크** 점검에 쓴다.
실행: ssh mini-lan 'cd ~/research_archive/20_미국주식/mp_quant && python3 mp_hedge_overlay.py'
"""
import math
import numpy as np, pandas as pd, yfinance as yf

RF   = 0.0372   # 13주 T-bill 실측
COST = 0.004    # 헤지 실행비용 연 0.4%p (선물 롤·스프레드), 헤지비율에 비례

W = pd.read_csv('mp_v47_weights.csv')
S = pd.read_csv('mp_v47_stock_levels.csv').set_index('ticker')
held = W[W.mp_weight > 0]

px = yf.download(list(held.ticker) + ['QQQ'], period='2y', interval='1d',
                 auto_adjust=True, progress=False)['Close']
rets = px.pct_change().dropna(how='all')
avail = [t for t in held.ticker if t in rets.columns and rets[t].notna().sum() > 250]
w = held.set_index('ticker').loc[avail, 'mp_weight']; w = w / w.sum()
both = pd.concat([(rets[avail] * w).sum(axis=1), rets['QQQ']], axis=1).dropna()
both.columns = ['p', 'b']

def exp_ret(weights, k):
    """가중 기대수익 — 실측 성장·배수회귀만 쓴다. 커버리지도 같이 돌려준다."""
    d = S.reindex(weights.index)
    e = (1 + d.growth) * (1 + k * d.pe_revert_full) - 1
    ok = e.notna() & np.isfinite(e)
    ww = weights[ok] / weights[ok].sum()
    return float((ww * e[ok]).sum()), float(weights[ok].sum() / weights.sum())

bmw = W[W.bm_weight_approx > 0].set_index('ticker').bm_weight_approx
mpw = held.set_index('ticker').mp_weight

def mdd(s):
    c = (1 + s).cumprod(); return float((c / c.cummax() - 1).min())

L = ['# MP v4.7 기대수익·샤프·헤지 오버레이 — 종목별 실측 기반\n',
     f'rf {RF:.2%}(13주 T-bill 실측) · 헤지비용 {COST:.1%}/년 비례 · 가격 커버리지 {len(avail)}/{len(held)}',
     '기대수익은 시나리오 가정이 아니라 종목별 (컨센 fwd 성장 × 자기 역사 P/E 회귀)의 가중합이다.\n',
     '## 1. 배수 회귀 속도별 기대수익 — MP vs BM\n',
     '| 회귀 속도 k | MP E[r] | BM E[r] | **알파** | MP 커버리지 | BM 커버리지 |',
     '|---|---:|---:|---:|---:|---:|']
ER = {}
for tag, k in [('0 (배수 그대로)', 0.0), ('0.5 (절반 회귀)', 0.5), ('1.0 (전부 회귀)', 1.0)]:
    m, mc = exp_ret(mpw, k); b, bc = exp_ret(bmw, k)
    ER[k] = (m, b)
    L.append(f'| {tag} | {m:.1%} | {b:.1%} | **{m-b:+.1%}** | {mc:.0%} | {bc:.0%} |')

L += ['\n## 2. 헤지 오버레이 — 넷 밴드별 (σ·MDD·VaR는 실측 시계열, k=0.5 기준)\n',
      '| 넷 | QQQ 숏 | E[r] | 연율 σ | 베타 | TE | **기대 샤프** | MDD(2y) | VaR95 |',
      '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
E_MP, E_BM = ER[0.5]
band = []
for net in [1.00, 0.80, 0.70, 0.60, 0.50]:
    h = 1 - net
    r = both.p - h * both.b
    vol = float(r.std()) * math.sqrt(252)
    er = E_MP - h * (E_BM - RF) - h * COST
    sh = (er - RF) / vol
    band.append((net, h, er, vol, sh))
    L.append(f'| {net:.0%} | {h:.0%} | {er:.1%} | {vol:.1%} | '
             f'{float(r.cov(both.b)/both.b.var()):.2f} | {float((r-both.b).std())*math.sqrt(252):.1%} | '
             f'**{sh:.2f}** | {mdd(r):.1%} | {float(r.quantile(0.05)):.2%} |')
best = max(band, key=lambda x: x[4])
L.append(f'\n**최적 넷 {best[0]:.0%}** (샤프 {best[4]:.2f}) — 넷 100% 대비 '
         f'{best[4]-band[0][4]:+.2f}.')

L += ['\n## 3. 회귀 속도 민감도 — k가 결론을 바꾸는가\n',
      '| k | MP 알파 | 넷100% 샤프 | 넷80% | 넷70% | 넷60% | 최적 |', '|---|---:|---:|---:|---:|---:|---|']
for k in [0.0, 0.5, 1.0]:
    m, b = ER[k]; row = []
    for net in [1.00, 0.80, 0.70, 0.60]:
        h = 1 - net
        r = both.p - h * both.b
        vol = float(r.std()) * math.sqrt(252)
        row.append(((m - h * (b - RF) - h * COST) - RF) / vol)
    opt = ['100%', '80%', '70%', '60%'][int(np.argmax(row))]
    L.append(f'| {k} | {m-b:+.1%} | {row[0]:.2f} | {row[1]:.2f} | {row[2]:.2f} | {row[3]:.2f} | **{opt}** |')

open('mp_v47_hedge_overlay.md', 'w').write('\n'.join(L))
print('\n'.join(L))
