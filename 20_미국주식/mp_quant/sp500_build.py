#!/usr/bin/env python3
"""S&P 500 기준 MP 구축 (v5.0) — 콜 이식 + 미커버 섹터 대표종목 압축 복제.

설계 결정(2026-08-25 지시):
  · 미커버 섹터(금융·헬스케어·산업재·에너지·소재·리츠 등)는 **대표종목 압축 복제** —
    섹터 BM 비중은 맞추되 종목수를 줄여 시총 상위 대형주로 담는다. 섹터 액티브 0.
  · 기술·AI 축은 **TE 12% 내외**를 목표로 v4.8 절대비중에 계수 λ를 곱해 조정한다.
    (나스닥100에선 기술 BM 60%라 OW 여지가 좁았으나 S&P500은 33%라 그대로 두면 TE 폭증)
λ 스윕으로 TE를 실측해 목표에 가장 가까운 값을 고른다.
실행: ssh mini-lan 'cd ~/research_archive/20_미국주식/mp_quant && python3 sp500_build.py'
"""
import math
import numpy as np, pandas as pd, yfinance as yf

TE_TARGET = 0.12
TOPN = {'Financials': 8, 'Health Care': 8, 'Industrials': 6, 'Consumer Staples': 5,
        'Energy': 4, 'Materials': 3, 'Real Estate': 3, 'Utilities': 3}

U = pd.read_csv('sp500_universe.csv').set_index('ticker')
V = pd.read_csv('mp_v48_weights.csv').set_index('ticker')
call = V[V.mp_weight > 0].copy()                    # v4.8 콜 블록 107종목

# --- 1. 콜 블록이 이미 커버하는 섹터 비중을 GICS 기준으로 집계 ---
call_in = [t for t in call.index if t in U.index]
covered = U.loc[call_in].groupby('GICS Sector').bm_weight.sum()

# --- 2. 미커버 잔여를 섹터별 대표종목으로 압축 복제 ---
rep = {}
for sec, n in TOPN.items():
    sec_bm = float(U[U['GICS Sector'] == sec].bm_weight.sum())
    resid = sec_bm - float(covered.get(sec, 0.0))
    if resid <= 0.05: continue
    pool = U[(U['GICS Sector'] == sec) & (~U.index.isin(call_in))].nlargest(n, 'bm_weight')
    if not len(pool): continue
    share = pool.bm_weight / pool.bm_weight.sum()
    for t, s in share.items(): rep[t] = resid * float(s)
R = pd.Series(rep, name='rep_weight')
print(f'압축 복제 {len(R)}종목 · 합계 {R.sum():.1f}%')
for sec in TOPN:
    sub = [t for t in R.index if U.loc[t, 'GICS Sector'] == sec]
    if sub: print(f'  {sec:24s} {R[sub].sum():5.2f}% / {len(sub)}종목  {", ".join(sub)}')

# --- 3. 가격 데이터 (콜 블록 + 복제 블록 + BM 프록시 SPY) ---
tick = sorted(set(list(call.index) + list(R.index)))
px = yf.download(tick + ['SPY'], period='2y', interval='1d', auto_adjust=True, progress=False)['Close']
rets = px.pct_change().dropna(how='all')
ok = lambda t: t in rets.columns and rets[t].notna().sum() > 250
bm = rets['SPY']

def build(lam):
    """콜 블록에 λ를 곱하고 복제 블록으로 나머지를 채운 뒤 100%로 정규화."""
    w = pd.Series(0.0, index=tick)
    w[call.index] = call.mp_weight * lam
    w[R.index] += R.values
    if w.sum() > 100:                                   # 콜이 넘치면 복제 블록을 비례 축소
        over = w.sum() - 100
        cut = min(over, float(w[R.index].sum()))
        w[R.index] *= (1 - cut / float(w[R.index].sum()))
    return w / w.sum() * 100

def te_of(w):
    av = [t for t in w.index if w[t] > 0 and ok(t)]
    ww = w[av] / w[av].sum()
    port = (rets[av] * ww).sum(axis=1)
    both = pd.concat([port, bm], axis=1).dropna(); both.columns = ['p', 'b']
    te = float((both.p - both.b).std()) * math.sqrt(252)
    beta = float(both.p.cov(both.b) / both.b.var())
    vol = float(both.p.std()) * math.sqrt(252)
    return te, beta, vol, len(av)

print('\nλ 스윕 — 콜 블록 배율에 따른 TE')
print('| λ | 콜 블록 | 복제 블록 | TE | 베타 | σ |')
print('|---|--:|--:|--:|--:|--:|')
best = None
for lam in [1.00, 0.85, 0.70, 0.60, 0.50, 0.45, 0.40]:
    w = build(lam)
    te, beta, vol, n = te_of(w)
    cb = float(w[call.index].sum()); rb = float(w[[t for t in R.index if t in w.index]].sum())
    print(f'| {lam:.2f} | {cb:.1f}% | {rb:.1f}% | **{te:.1%}** | {beta:.2f} | {vol:.1%} |')
    if best is None or abs(te - TE_TARGET) < abs(best[1] - TE_TARGET): best = (lam, te, w)

lam, te, w = best
print(f'\n선택 λ={lam:.2f} · TE {te:.1%} (목표 {TE_TARGET:.0%})')
out = pd.DataFrame({'mp_weight': w[w > 0].round(2)})
out['bm_weight'] = U.bm_weight.reindex(out.index).fillna(0.0).round(3)
out['active'] = (out.mp_weight - out.bm_weight).round(2)
out['sector'] = U['GICS Sector'].reindex(out.index)
out['block'] = ['콜' if t in call.index else '복제' for t in out.index]
out.sort_values('mp_weight', ascending=False).to_csv('mp_v50_sp500_weights.csv')
print(f'종목수 {len(out)} · 합계 {out.mp_weight.sum():.1f}%')
print(f'BM외(S&P500 미편입) {out[out.bm_weight==0].mp_weight.sum():.1f}% / {int((out.bm_weight==0).sum())}종목')
print('\n섹터 비중 (MP vs BM):')
g = out.groupby('sector').agg(mp=('mp_weight','sum'), bm=('bm_weight','sum'))
g['active'] = g.mp - g.bm
print(g.round(2).sort_values('mp', ascending=False).to_string())
