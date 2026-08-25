#!/usr/bin/env python3
"""MP v5.1 — 30종목 집중 + 금융 뷰 (BM = S&P500)

선정 원칙 (2026-08-25 지시):
  · **애널리스트 커버리지가 두꺼운 종목 위주** — n_analysts 20+ 를 원칙으로 한다.
    정보 신뢰도와 유동성의 대리변수이고, 30종목 집중 포트에서는 개별 종목 사고가
    포트를 흔들기 때문에 "아무도 안 보는 종목"을 담을 여유가 없다.
  · 데이터 커버리지 완비(역사 forward 배수·컨센 성장·목표주가 전부 있음).
  · 종목수 30. v5.0의 147종목에서 압축하므로 섹터 중립은 포기한다 — 그 대가는 TE다.

비중: **BM 비중 × 뷰 계수(tilt)** 후 정규화. tilt가 곧 리서치 뷰이고 근거는 문서에 있다.
실행: ssh mini-lan 'cd ~/research_archive/20_미국주식/mp_quant && python3 mp_v51_build.py'
"""
import math, os
import numpy as np, pandas as pd, yfinance as yf

# tilt = 1.0 이 BM 중립. 근거는 MP_v5.1 문서 각 절.
TILT = {
    # --- AI·반도체 축 (기존 컨빅션 이식) ---
    'NVDA': 1.3, 'MSFT': 1.6, 'AVGO': 1.8, 'MU': 3.0, 'MRVL': 8.0,
    'ANET': 6.0, 'LRCX': 2.0, 'KLAC': 2.5, 'ORCL': 3.0, 'VRT': 10.0,
    'AAPL': 0.6,                                  # UW — 성장 8%·목표 8%, 역사보다 비싸다
    # --- 커뮤니케이션 ---
    'META': 1.5, 'NFLX': 2.0, 'GOOGL': 0.4,       # GOOGL UW 유지(검색 잠식 논거)
    # --- 경기소비 ---
    'AMZN': 1.2,
    # --- 금융: 은행 0, 통과세 OW (v5.1 신규 뷰) ---
    'V': 2.5, 'MA': 2.5, 'SPGI': 4.0,
    # --- 헬스케어 ---
    'LLY': 1.5, 'ABBV': 1.5, 'UNH': 1.5, 'JNJ': 1.0,
    # --- 필수소비 ---
    'WMT': 1.2, 'COST': 1.2, 'PG': 1.0,
    # --- 산업재 ---
    'GE': 1.0, 'CAT': 1.0,
    # --- 에너지 ---
    'XOM': 1.0,
    # --- 유틸·전력 (AI 전력 수요 콜) ---
    'CEG': 4.0, 'NEE': 2.0,
}

U = pd.read_csv('sp500_universe.csv').set_index('ticker').drop(columns=['price'])
S = pd.read_csv('mp_v50_stock_levels.csv').set_index('ticker')
F = U.join(S)

sel = pd.Series(TILT, name='tilt')
bm = U.bm_weight.reindex(sel.index)
w = (bm * sel)
w = w / w.sum() * 100

out = pd.DataFrame({'mp_weight': w.round(2), 'bm_weight_approx': bm.round(3), 'tilt': sel})
out['active'] = (out.mp_weight - out.bm_weight_approx).round(2)
out['sector'] = U['GICS Sector'].reindex(sel.index)
out['n_analysts'] = F.n_analysts.reindex(sel.index)
out = out.sort_values('mp_weight', ascending=False)
out.index.name = 'ticker'
print(f'{len(out)}종목 · 합계 {out.mp_weight.sum():.1f}% · BM 커버 {bm.sum():.1f}%')
print(f'애널 커버리지 20+ : {int((out.n_analysts >= 20).sum())}/{len(out)} · '
      f'결측 {int(out.n_analysts.isna().sum())} (수집 실패 — 실제로는 두껍다)')
print(out[['mp_weight', 'bm_weight_approx', 'active', 'tilt', 'sector', 'n_analysts']].to_string())

# 전체 BM(502종목)을 담은 표준 비중 파일 — 미보유분도 액티브에 반영돼야 한다
allt = sorted(set(out.index) | set(U.index))
std = pd.DataFrame(index=allt); std.index.name = 'ticker'
std['mp_weight'] = out.mp_weight.reindex(allt).fillna(0.0)
std['bm_weight_approx'] = U.bm_weight.reindex(allt).fillna(0.0)
std['sector'] = U['GICS Sector'].reindex(allt).fillna('BM외')
std.reset_index().to_csv('mp_v51_weights.csv', index=False)

# 섹터 액티브
print('\n섹터 (MP vs S&P500 전체):')
g = pd.DataFrame({'MP': out.groupby('sector').mp_weight.sum(),
                  'BM': U.groupby('GICS Sector').bm_weight.sum()}).fillna(0.0)
g['액티브'] = g.MP - g.BM
print(g.round(2).sort_values('MP', ascending=False).to_string())
print(f"섹터 액티브 절대합 {g['액티브'].abs().sum():.1f}%p")

# TE·베타 실측
px = yf.download(list(out.index) + ['SPY'], period='2y', interval='1d',
                 auto_adjust=True, progress=False)['Close']
r = px.pct_change().dropna(how='all')
av = [t for t in out.index if t in r.columns and r[t].notna().sum() > 250]
ww = out.mp_weight[av] / out.mp_weight[av].sum()
both = pd.concat([(r[av] * ww).sum(axis=1), r['SPY']], axis=1).dropna(); both.columns = ['p', 'b']
te = float((both.p - both.b).std()) * math.sqrt(252)
beta = float(both.p.cov(both.b) / both.b.var())
vol = float(both.p.std()) * math.sqrt(252)
cum = (1 + both.p).cumprod(); mdd = float((cum / cum.cummax() - 1).min())
cumb = (1 + both.b).cumprod(); mddb = float((cumb / cumb.cummax() - 1).min())
print(f'\n실측(2y vs SPY): TE {te:.1%} · 베타 {beta:.2f} · σ {vol:.1%} · '
      f'MDD {mdd:.1%}(SPY {mddb:.1%}) · VaR95 {float(both.p.quantile(0.05)):.2%} · 커버 {len(av)}/{len(out)}')
