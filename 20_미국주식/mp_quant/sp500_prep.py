#!/usr/bin/env python3
"""v5.0 balanced 비중을 기존 파이프라인 표준 형식으로 변환.

표준 컬럼: ticker, mp_weight, bm_weight_approx, sector
BM은 S&P500 **전체 503종목**을 담는다 — 미보유 종목도 BM 비중이 있어야 액티브가 맞다.
"""
import pandas as pd

B = pd.read_csv('mp_v50_sp500_balanced.csv', index_col=0)
U = pd.read_csv('sp500_universe.csv').set_index('ticker')

allt = sorted(set(B.index) | set(U.index))
out = pd.DataFrame(index=allt)
out.index.name = 'ticker'
out['mp_weight'] = B.mp_weight.reindex(allt).fillna(0.0)
out['bm_weight_approx'] = U.bm_weight.reindex(allt).fillna(0.0)
out['sector'] = U['GICS Sector'].reindex(allt).fillna(
    B.sector.reindex(allt)).fillna('BM외(S&P500 미편입)')
out = out.reset_index()
out.to_csv('mp_v50_weights.csv', index=False)
print(f'{len(out)}행 · MP 보유 {(out.mp_weight>0).sum()}종목 {out.mp_weight.sum():.1f}% · '
      f'BM {(out.bm_weight_approx>0).sum()}종목 {out.bm_weight_approx.sum():.1f}%')
print(f'BM외 보유 {out[(out.mp_weight>0)&(out.bm_weight_approx==0)].mp_weight.sum():.1f}%')
print(f'미보유 BM 종목 {int(((out.mp_weight==0)&(out.bm_weight_approx>0)).sum())}개 '
      f'= BM 비중 {out[(out.mp_weight==0)].bm_weight_approx.sum():.1f}% (자동 UW)')
