#!/usr/bin/env python3
"""MP v4.7 종목별 실측 표 — 108종목 전부, 밸류에이션·기술 레벨 한 장.

`mp_stock_levels.py` 산출물을 사람이 읽는 표로 낸다. 커버리지 구멍은 숨기지 않고 표시한다.
"""
import os
import numpy as np, pandas as pd

# 비중 파일은 환경변수로 갈아끼운다: WEIGHTS=mp_v48_weights.csv python3 ...
WEIGHTS = os.environ.get('WEIGHTS', 'mp_v47_weights.csv')

S = pd.read_csv(os.environ.get('OUT_LEVELS','mp_v47_stock_levels.csv')).set_index('ticker')
W = pd.read_csv(WEIGHTS).set_index('ticker')
mp = W[W.mp_weight > 0].sort_values('mp_weight', ascending=False)

def f(v, spec='{:.1f}', pct=False):
    if v is None or (isinstance(v, float) and (np.isnan(v) or not np.isfinite(v))): return '—'
    return spec.format(v * 100 if pct else v)

LABEL = os.environ.get('LABEL', 'MP v4.7')
L = [f'# {LABEL} 종목별 실측 — 밸류에이션·기술 레벨\n',
     '**밸류에이션은 forward 기준이다.** 현재 배수는 컨센 forward P/E, 역사 배수는 그 시점',
     '가격 ÷ 그 회계연도 실현 EPS(FY 구간 선행 적용)의 5년 일별 시계열 중앙값·사분위다.',
     '적자·무이익 종목은 P/E가 성립하지 않아 **역사적 PSR**로 같은 계산을 한다(기준 열 표시).\n',
     '지지·저항은 최근 1년 일별에서 창 41일 로컬 극값 중 현재가 위/아래 최근접값이다.\n',
     '| # | 티커 | 비중 | 현재가 | 기준 | 현재배수 | 역사중앙 | 역사 25~75% | 회귀 | 컨센성장 | 목표상승 | σ(1y) | MA200 | 지지 | 저항 | 상방 | 하방 |',
     '|--:|---|--:|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|']

for n, (t, r) in enumerate(mp.iterrows(), 1):
    if t not in S.index:
        L.append(f'| {n} | {t} | {r.mp_weight:.1f} | — | **미수집** | — | — | — | — | — | — | — | — | — | — | — | — |')
        continue
    d = S.loc[t]
    basis = {'fwd_pe': 'fwd P/E', 'psr': 'PSR', 'none': '**없음**'}.get(d.val_basis, d.val_basis)
    now  = d.pe_now  if d.val_basis == 'fwd_pe' else d.ps_now
    med  = d.pe_hist_med if d.val_basis == 'fwd_pe' else d.ps_hist_med
    band = f'{f(d.pe_hist_p25)}~{f(d.pe_hist_p75)}' if med == med else '—'
    L.append(f'| {n} | {t} | {r.mp_weight:.1f} | {f(d.price)} | {basis} | {f(now)} | {f(med)} | {band} | '
             f'{f(d.pe_revert_full, "{:+.0f}%", pct=True)} | {f(d.growth_1y, "{:+.0f}%", pct=True)} | '
             f'{f(d.target_upside, "{:+.0f}%", pct=True)} | {f(d.vol_1y, "{:.0f}%", pct=True)} | '
             f'{f(d.px_vs_ma200, "{:+.0f}%", pct=True)} | {f(d.support)} | {f(d.resistance)} | '
             f'{f(d.upside_to_resist, "{:+.0f}%", pct=True)} | {f(d.downside_to_support, "{:+.0f}%", pct=True)} |')

d = S.reindex(mp.index)
w = mp.mp_weight / mp.mp_weight.sum()
def wm(col, mask=None):
    x = d[col]; ok = x.notna() & np.isfinite(x)
    if mask is not None: ok &= mask
    return float((w[ok] / w[ok].sum() * x[ok]).sum()), float(w[ok].sum())

L += ['\n## 커버리지 — 숨기지 않는다\n', '| 항목 | 종목수 | MP 비중 |', '|---|--:|--:|']
for lbl, m in [('forward P/E 역사 있음', d.val_basis == 'fwd_pe'),
               ('PSR 역사로 대체(적자·무이익)', d.val_basis == 'psr'),
               ('**역사 배수 없음**', (d.val_basis == 'none') | d.val_basis.isna()),
               ('지지·저항·MA·변동성', d.support.notna()),
               ('컨센 성장률', d.growth_1y.notna()),
               ('컨센 목표주가', d.target_upside.notna())]:
    mm = m.fillna(False)
    L.append(f'| {lbl} | {int(mm.sum())}/{len(d)} | {float(mp.mp_weight[mm].sum()):.1f}% |')

nomult = list(d.index[(d.val_basis == 'none') | d.val_basis.isna()])
L.append(f'\n역사 배수 없는 종목: {", ".join(nomult) if nomult else "없음"} — '
         'TSM은 재무가 TWD인데 가격은 USD ADR이라 구조적으로 역사 배수를 만들 수 없다'
         '(현재 forward P/E는 환산돼 있어 유효하다). 나머지는 5년 이력 부족.')

L += ['\n## 가중 요약\n', '| 지표 | 가중값 | 커버리지 |', '|---|--:|--:|']
for lbl, col, pct in [('현재 forward P/E', 'pe_now', False), ('역사 forward P/E 중앙값', 'pe_hist_med', False),
                      ('배수 회귀 여력', 'pe_revert_full', True), ('컨센 차년도 성장', 'growth_1y', True),
                      ('목표주가 상승여력', 'target_upside', True), ('개별 변동성 1y', 'vol_1y', True),
                      ('MA200 대비 위치', 'px_vs_ma200', True),
                      ('상방(→저항)', 'upside_to_resist', True), ('하방(→지지)', 'downside_to_support', True)]:
    v, c = wm(col)
    L.append(f'| {lbl} | {v*100:+.1f}% | {c:.0%} |' if pct else f'| {lbl} | {v:.1f} | {c:.0%} |')

open(os.environ.get('OUT_TABLE','mp_v47_stock_table.md'), 'w').write('\n'.join(L))
print(f'표 산출: {len(mp)}종목')
print('\n'.join(L[-16:]))
