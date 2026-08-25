#!/usr/bin/env python3
"""MP v5.1 추천종목표 — 증권사 MP 표준 양식으로 출력.

양식은 KB증권 미국주식 추천종목(G11) 공개 페이지의 표 구성을 따른다:
  종목 · 추천등급 · 기대수익률 · 추천가 · 추천근거 · 추천사유
KB의 문장·수치는 쓰지 않는다(로그인 벽이라 본문 접근 자체가 없었다). 구성만 차용하고
내용은 전부 자체 실측이다.

추천등급은 tilt(뷰 계수)를 매핑한다:
  tilt >= 3.0 적극비중확대 · 1.5~3.0 비중확대 · 0.8~1.5 중립 · <0.8 비중축소
목표주가는 두 개를 병기한다 — 컨센(애널 중앙값)과 자체(성장×배수회귀 k=0.5).
"""
import os, math
import numpy as np, pandas as pd

W = pd.read_csv('mp_v51_weights.csv').set_index('ticker')
S = pd.read_csv(os.environ.get('OUT_LEVELS','mp_v51_stock_levels.csv')).set_index('ticker')
U = pd.read_csv('sp500_universe.csv').set_index('ticker').drop(columns=['price'])
B = pd.read_csv('mp_v51_build_detail.csv').set_index('ticker') if os.path.exists('mp_v51_build_detail.csv') else None

held = W[W.mp_weight > 0].join(S).join(U[['Security', 'GICS Sector', 'GICS Sub-Industry']])

TILT = {'NVDA':1.3,'MSFT':1.6,'AVGO':1.8,'MU':3.0,'MRVL':8.0,'ANET':6.0,'LRCX':2.0,'KLAC':2.5,
        'ORCL':3.0,'VRT':10.0,'AAPL':0.6,'META':1.5,'NFLX':2.0,'GOOGL':0.4,'AMZN':1.2,
        'V':2.5,'MA':2.5,'SPGI':4.0,'LLY':1.5,'ABBV':1.5,'UNH':1.5,'JNJ':1.0,
        'WMT':1.2,'COST':1.2,'PG':1.0,'GE':1.0,'CAT':1.0,'XOM':1.0,'CEG':4.0,'NEE':2.0}
# tilt는 build 상세 파일에서 읽는다 — 사본을 두면 어긋난다
held['tilt'] = B.tilt if B is not None else np.nan

# 추천등급은 **액티브 비중** 기준이다. tilt는 BM 대비 배수라서 BM이 큰 종목에서는
# 절대비중과 어긋난다(NVDA는 tilt 1.3인데 비중 1위). 실제로 포트가 지는 베팅은 액티브다.
def grade(a):
    if a >= 3.0: return '적극 비중확대'
    if a >= 1.0: return '비중확대'
    if a > -1.0: return '중립'
    return '비중축소'

held['active'] = held.mp_weight - held.bm_weight_approx
held['등급'] = held.active.map(grade)
held['자체목표'] = held.price * (1 + held.exp_ret_half)      # 성장×배수회귀 k=0.5
held['컨센목표'] = held.price * (1 + held.target_upside)
held['자체여력'] = held.exp_ret_half
held = held.sort_values('mp_weight', ascending=False)

def f(v, sp='{:.1f}'):
    return '—' if v is None or (isinstance(v, float) and (np.isnan(v) or not np.isfinite(v))) else sp.format(v)

L = ['# MP v5.1 미국주식 추천종목 — 30선 (2026-08-25)\n',
     '> BM: S&P 500 · 비중 합계 100.0% · 개별 상한 10%',
     '> 추천등급은 **BM 대비 액티브 비중** 기준 — 적극비중확대(+3%p↑) · 비중확대(+1~3%p) ·',
     '> 중립(−1~+1%p) · 비중축소(−1%p↓). 뷰 계수(tilt)가 아니라 실제로 지는 베팅 크기로 매긴다.',
     '> 기대수익률은 두 경로 병기: **자체**(컨센 EPS 2년 CAGR × 자기 역사 forward 배수 절반 회귀)와',
     '> **컨센**(애널리스트 목표주가 중앙값). 추천가는 2026-08-25 종가.\n',
     '| 종목 | 티커 | 비중 | 액티브 | 추천등급 | 추천가(USD) | 자체 목표가 | **자체 기대수익률** | 컨센 목표가 | 컨센 기대수익률 | 커버리지 |',
     '|---|---|--:|--:|---|--:|--:|--:|--:|--:|--:|']
for t, r in held.iterrows():
    act = r.active
    L.append(f"| {r.Security} | {t} | {r.mp_weight:.2f} | {act:+.2f} | {r.등급} | {f(r.price,'{:.2f}')} | "
             f"{f(r.자체목표,'{:.0f}')} | **{f(r.자체여력*100,'{:+.0f}%')}** | {f(r.컨센목표,'{:.0f}')} | "
             f"{f(r.target_upside*100,'{:+.0f}%')} | {f(r.n_analysts,'{:.0f}')} |")

w = held.mp_weight / held.mp_weight.sum()
def wm(c):
    x = held[c]; ok = x.notna() & np.isfinite(x)
    return float((w[ok]/w[ok].sum() * x[ok]).sum())
L += ['',
      f"**포트 가중 기대수익률: 자체 {wm('exp_ret_half')*100:+.1f}% · 컨센 {wm('target_upside')*100:+.1f}%**",
      f"가중 forward P/E {wm('pe_now'):.1f} (자기 역사 중앙값 {wm('pe_hist_med'):.1f}) · "
      f"가중 컨센 성장 {wm('growth_1y')*100:+.1f}% · 가중 애널 커버리지 {wm('n_analysts'):.0f}명"]

L += ['\n## 등급별 요약\n', '| 등급 | 종목수 | 비중 | 가중 자체 기대수익률 |', '|---|--:|--:|--:|']
for g_ in ['적극 비중확대', '비중확대', '중립', '비중축소']:
    sub = held[held.등급 == g_]
    if not len(sub): continue
    ww = sub.mp_weight / sub.mp_weight.sum()
    x = sub.exp_ret_half; ok = x.notna() & np.isfinite(x)
    er = float((ww[ok]/ww[ok].sum() * x[ok]).sum()) if ok.any() else float('nan')
    L.append(f"| {g_} | {len(sub)} | {sub.mp_weight.sum():.1f}% | {er*100:+.1f}% |")

L += ['\n## 섹터 배분\n', '| 섹터 | MP | BM(S&P500) | 액티브 | 종목수 |', '|---|--:|--:|--:|--:|']
bm_all = U.groupby('GICS Sector').bm_weight.sum()
g = held.groupby('GICS Sector').agg(mp=('mp_weight','sum'), n=('mp_weight','size'))
for sec in bm_all.sort_values(ascending=False).index:
    mp_ = float(g.mp.get(sec, 0.0)); n_ = int(g.n.get(sec, 0)); bm_ = float(bm_all[sec])
    L.append(f'| {sec} | {mp_:.2f} | {bm_:.2f} | {mp_-bm_:+.2f} | {n_} |')

open('mp_v51_recsheet.md', 'w').write('\n'.join(L))
print('\n'.join(L[:14]))
print('...')
print('\n'.join(L[-16:]))
