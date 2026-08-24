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

# 구조 정정 2회.
#  1차(λ = 콜 블록 총량): 두 목표를 동시에 못 맞춘다. 미커버 섹터를 BM대로 채우려면 복제
#     블록 36%가 필요 → 콜 블록 64% 강제 → TE 6.8%. λ를 올려 TE를 키우면 복제 블록이 눌려
#     금융이 BM 12.1% 대비 5.0%로 무너진다(섹터 중립 위배).
#  2차(κ = 콜 블록 내 집중도): 폐기. v4.8 비중 순위를 극단화해 대형주만 남고 중소형 콜
#     (COHR·TLN·BE 등 알파 원천)이 전멸했다. 커뮤니케이션이 −14.8%p로 무너졌다.
#  최종안: **대형주는 BM으로 되돌리고 중소형 콜은 절대비중을 지킨다.**
#     S&P500에선 BM 비중이 작아져 MSFT·NVDA 같은 대형주 OW가 자동으로 커진다 — 그 액티브는
#     의도한 게 아니라 BM 교체의 부산물이다. 대형주 액티브를 스케일 g로 눌러 되돌리고,
#     BM 비중이 작거나 BM 밖인 종목(진짜 알파 원천)은 그대로 둔다. TE 효율(IR)이 올라간다.
REP_TOTAL = float(R.sum())
CALL_TOTAL = 100.0 - REP_TOTAL
BIG = 0.5   # S&P500 BM 비중 이 이상이면 '대형주'로 보고 액티브를 스케일한다

#  3차 확인: 대형주 액티브를 g=0.1까지 눌러도 콜 블록이 96.6%를 먹어 복제 자리가 3.4%뿐
#     → 금융 −11%p. **콜 종목 107개의 절대비중 합이 이미 100%**라서, 미커버 섹터를 넣으려면
#     콜을 실제로 덜어내야 한다.
#  최종 구조: 복제 블록 채움 비율 ρ를 직접 정하고, 콜 블록은 (100 − 복제)를 v4.8 상대비중
#     대로 나눠 갖는다. ρ가 곧 "섹터 중립을 얼마나 지킬 것인가"이고, TE는 그 결과다.
#     TE 12%와 섹터 중립은 양립하지 않는다 — TE의 대부분이 섹터 베팅에서 나오기 때문이다.
REP_TOTAL = float(R.sum())

def build(rho):
    """ρ=1이면 미커버 섹터를 BM대로 전부 복제(섹터 중립), ρ=0이면 콜 블록만(TE 최대)."""
    rep = R * rho
    call_total = 100.0 - float(rep.sum())
    c = call.mp_weight / call.mp_weight.sum() * call_total
    w = pd.Series(0.0, index=tick)
    w[c.index] = c.values
    w[rep.index] += rep.values
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

print('\nρ 스윕 — 섹터 중립(복제 채움) vs TE 트레이드오프')
print('| ρ | 복제 블록 | 금융 액티브 | IT 액티브 | 섹터액티브 절대합 | TE | 베타 | σ |')
print('|---|--:|--:|--:|--:|--:|--:|--:|')
bm_sec_all = U.groupby('GICS Sector').bm_weight.sum()
rows_out = {}
best = None
for rho in [1.00, 0.80, 0.60, 0.50, 0.40, 0.20, 0.00]:
    w = build(rho)
    te, beta, vol, n = te_of(w)
    nz = w[w > 0]
    sec = pd.Series({t: U['GICS Sector'].get(t, 'BM외') for t in nz.index})
    ms = nz.groupby(sec).sum()
    act = (ms.reindex(bm_sec_all.index).fillna(0.0) - bm_sec_all)
    rows_out[rho] = w
    print(f'| {rho:.2f} | {float((R*rho).sum()):.1f}% | {act["Financials"]:+.1f}%p | '
          f'{act["Information Technology"]:+.1f}%p | {act.abs().sum():.1f}%p | **{te:.1%}** | {beta:.2f} | {vol:.1%} |')
    if best is None or abs(te - TE_TARGET) < abs(best[1] - TE_TARGET): best = (rho, te, w)

print('\n**TE 12%와 섹터 중립은 양립하지 않는다.** ρ=1(섹터 중립)이면 TE가 목표의 절반이고,')
print('TE 12%를 맞추려면 금융을 두 자릿수 UW해야 한다 — 그건 "대표종목 압축 복제"의 포기다.')
print('세 안을 모두 파일로 낸다: 중립(ρ=1.0) · 절충(ρ=0.5) · TE우선(ρ=0.2).')

for tag, rho in [('neutral', 1.0), ('balanced', 0.5), ('te_first', 0.2)]:
    w = rows_out[rho]; nz = w[w > 0]
    o = pd.DataFrame({'mp_weight': (nz / nz.sum() * 100).round(2)})
    o['bm_weight'] = U.bm_weight.reindex(o.index).fillna(0.0).round(3)
    o['active'] = (o.mp_weight - o.bm_weight).round(2)
    o['sector'] = U['GICS Sector'].reindex(o.index).fillna('BM외(S&P500 미편입)')
    o['block'] = ['콜' if t in call.index else '복제' for t in o.index]
    o.sort_values('mp_weight', ascending=False).to_csv(f'mp_v50_sp500_{tag}.csv')
    te, beta, vol, _ = te_of(w)
    print(f'  {tag:9s} ρ={rho:.1f} · {len(o)}종목 · TE {te:.1%} · β {beta:.2f} · σ {vol:.1%} → mp_v50_sp500_{tag}.csv')

gg, te, w = best
gg, te, w = best
print(f'\n기본 산출: 절충안 ρ=0.5')
w = rows_out[0.5]
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
