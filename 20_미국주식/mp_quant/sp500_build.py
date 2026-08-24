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

# 구조 정정: λ(콜 블록 총량)로는 두 목표를 동시에 못 맞춘다.
#   미커버 섹터를 BM대로 채우려면 복제 블록 36%가 필요 → 콜 블록은 64%로 강제 → TE 7.8%.
#   λ를 올려 TE를 키우면 복제 블록이 눌려 금융이 BM 12.1% 대비 5.0%로 무너진다(섹터 중립 위배).
# 따라서 **콜 블록 총량은 고정하고, 그 안의 집중도 κ로 TE를 조절**한다.
#   κ>1이면 상위 종목에 더 몰아주고 꼬리를 잘라 같은 총량으로 TE를 높인다.
REP_TOTAL = float(R.sum())
CALL_TOTAL = 100.0 - REP_TOTAL

def build(kappa, floor=0.05):
    """콜 블록 CALL_TOTAL%를 v4.8 비중의 κ제곱으로 배분(집중도 조절), 복제 블록은 BM 그대로."""
    c = call.mp_weight.astype(float) ** kappa
    c = c / c.sum() * CALL_TOTAL
    c = c[c >= floor]                                   # 꼬리 절단 — 관리 불가능한 미세 비중 제거
    c = c / c.sum() * CALL_TOTAL
    w = pd.Series(0.0, index=tick)
    w[c.index] = c.values
    w[R.index] += R.values
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

print(f'\n복제 블록 {REP_TOTAL:.1f}% 고정 · 콜 블록 {CALL_TOTAL:.1f}%')
print('κ 스윕 — 콜 블록 내 집중도에 따른 TE (총량은 불변, 섹터 중립 유지)')
print('| κ | 종목수 | TOP10 | TE | 베타 | σ |')
print('|---|--:|--:|--:|--:|--:|')
best = None
for kap in [1.0, 1.3, 1.6, 2.0, 2.4, 2.8, 3.2]:
    w = build(kap)
    te, beta, vol, n = te_of(w)
    nz = w[w > 0]
    print(f'| {kap:.1f} | {len(nz)} | {nz.nlargest(10).sum():.1f}% | **{te:.1%}** | {beta:.2f} | {vol:.1%} |')
    if best is None or abs(te - TE_TARGET) < abs(best[1] - TE_TARGET): best = (kap, te, w)

kap, te, w = best
print(f'\n선택 κ={kap:.1f} · TE {te:.1%} (목표 {TE_TARGET:.0%})')
w = w[w > 0]
w = (w / w.sum() * 100)
out = pd.DataFrame({'mp_weight': w.round(2)})
out['mp_weight'] = out.mp_weight * 100 / out.mp_weight.sum()   # 반올림 후 재정규화
out['mp_weight'] = out.mp_weight.round(2)
out['bm_weight'] = U.bm_weight.reindex(out.index).fillna(0.0).round(3)
out['active'] = (out.mp_weight - out.bm_weight).round(2)
out['sector'] = U['GICS Sector'].reindex(out.index)
out['block'] = ['콜' if t in call.index else '복제' for t in out.index]
out.sort_values('mp_weight', ascending=False).to_csv('mp_v50_sp500_weights.csv')
print(f'종목수 {len(out)} · 합계 {out.mp_weight.sum():.1f}%')
print(f'BM외(S&P500 미편입) {out[out.bm_weight==0].mp_weight.sum():.1f}% / {int((out.bm_weight==0).sum())}종목')
print('\n섹터 비중 — BM은 **S&P500 전체** 기준이다(보유분만 세면 액티브가 왜곡된다):')
mp_sec = out.groupby('sector').mp_weight.sum()
bm_sec = U.groupby('GICS Sector').bm_weight.sum()
g = pd.DataFrame({'MP': mp_sec, 'BM(S&P500)': bm_sec}).fillna(0.0)
g['액티브'] = g.MP - g['BM(S&P500)']
print(g.round(2).sort_values('MP', ascending=False).to_string())
print(f"\n섹터 액티브 절대합 {g['액티브'].abs().sum():.1f}%p")
