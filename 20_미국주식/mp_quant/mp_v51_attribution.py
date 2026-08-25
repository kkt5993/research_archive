#!/usr/bin/env python3
"""MP v5.1 기여도 분해 — 알파·리스크를 종목·섹터 단위로 쪼갠다.

증권사 MP 리포트가 요구하는 세부 수치를 전부 산출한다:
  · 알파 기여도 = 액티브 비중 × (종목 기대수익률 − BM 기대수익률)
  · 리스크 기여도 = 종목이 포트 TE에 기여하는 몫 (한계기여도 × 액티브)
  · 섹터 집계, 상위/하위 기여 종목, 집중도 지표
실행: ssh mini-lan 'cd ~/research_archive/20_미국주식/mp_quant && python3 mp_v51_attribution.py'
"""
import math, os
import numpy as np, pandas as pd, yfinance as yf

W = pd.read_csv('mp_v51_weights.csv').set_index('ticker')
S = pd.read_csv(os.environ.get('OUT_LEVELS', 'mp_v51_stock_levels.csv')).set_index('ticker')
U = pd.read_csv('sp500_universe.csv').set_index('ticker').drop(columns=['price'])
B = pd.read_csv('mp_v51_build_detail.csv').set_index('ticker')

held = W[W.mp_weight > 0]
d = held.join(S).join(U[['Security', 'GICS Sector']])
d['active'] = d.mp_weight - d.bm_weight_approx
d['tilt'] = B.tilt

# BM 기대수익률(목표주가 경로) — 미보유 종목까지 포함한 전체 BM 가중
bmw = W[W.bm_weight_approx > 0].bm_weight_approx
bm_er_s = S.target_upside.reindex(bmw.index)
ok = bm_er_s.notna() & np.isfinite(bm_er_s)
BM_ER = float((bmw[ok] / bmw[ok].sum() * bm_er_s[ok]).sum())

# --- 알파 기여도: 액티브 × (종목 기대수익 − BM 기대수익) ---
d['alpha_contrib'] = d.active / 100 * (d.target_upside - BM_ER) * 100      # %p
d['alpha_contrib_self'] = d.active / 100 * (d.exp_ret_half - BM_ER) * 100

# --- 리스크 기여도: 공분산 기반 한계기여도 ---
px = yf.download(list(held.index) + ['SPY'], period='2y', interval='1d',
                 auto_adjust=True, progress=False)['Close']
r = px.pct_change().dropna(how='all')
av = [t for t in held.index if t in r.columns and r[t].notna().sum() > 250]
act = (d.active.reindex(av) / 100).astype(float)                # 액티브 비중(소수)
R = r[av].dropna()
bm_r = r['SPY'].reindex(R.index)
# 액티브 포트 수익률 = Σ(액티브 × 종목수익) — BM은 액티브 합이 0에 가까워 근사
act_ret = (R * act).sum(axis=1)
cov = R.apply(lambda c: c.cov(act_ret))                          # 각 종목과 액티브 포트 공분산
te = float(act_ret.std()) * math.sqrt(252)
d['risk_contrib'] = (act * cov / (act_ret.var() if act_ret.var() > 0 else np.nan) * te * 100).reindex(d.index)

d = d.sort_values('alpha_contrib', ascending=False)
tot_alpha = d.alpha_contrib.sum(); tot_risk = d.risk_contrib.sum()

def f(v, sp='{:+.2f}'):
    return '—' if v is None or (isinstance(v, float) and (np.isnan(v) or not np.isfinite(v))) else sp.format(v)

L = [f'# MP v5.1 기여도 분해 (2026-08-25)\n',
     f'BM 기대수익률(컨센 목표주가 경로) **{BM_ER*100:.1f}%** · 포트 TE(액티브 기준) {te:.1%}',
     f'알파 기여 합계 **{tot_alpha:+.2f}%p** · 리스크 기여 합계 {tot_risk:.2f}%p\n',
     '| 종목 | 티커 | 비중 | 액티브 | 기대수익(컨센) | **알파기여(%p)** | 리스크기여(%p) | 알파/리스크 | 섹터 |',
     '|---|---|--:|--:|--:|--:|--:|--:|---|']
for t, x in d.iterrows():
    ratio = x.alpha_contrib / x.risk_contrib if (x.risk_contrib == x.risk_contrib and abs(x.risk_contrib) > 0.01) else np.nan
    L.append(f"| {x.Security} | {t} | {x.mp_weight:.2f} | {x.active:+.2f} | {f(x.target_upside*100,'{:+.0f}%')} | "
             f"**{f(x.alpha_contrib)}** | {f(x.risk_contrib,'{:.2f}')} | {f(ratio,'{:.2f}')} | {x['GICS Sector']} |")

L += ['\n## 섹터별 기여\n', '| 섹터 | MP | BM | 액티브 | 알파기여 | 리스크기여 | 종목수 |', '|---|--:|--:|--:|--:|--:|--:|']
bm_sec = U.groupby('GICS Sector').bm_weight.sum()
g = d.groupby('GICS Sector').agg(mp=('mp_weight','sum'), a=('alpha_contrib','sum'),
                                 rk=('risk_contrib','sum'), n=('mp_weight','size'))
for sec in bm_sec.sort_values(ascending=False).index:
    mp_ = float(g.mp.get(sec, 0)); bm_ = float(bm_sec[sec])
    L.append(f"| {sec} | {mp_:.2f} | {bm_:.2f} | {mp_-bm_:+.2f} | {f(g.a.get(sec, 0.0))} | "
             f"{f(g.rk.get(sec, 0.0),'{:.2f}')} | {int(g.n.get(sec, 0))} |")

top5 = d.nlargest(5, 'alpha_contrib'); bot5 = d.nsmallest(5, 'alpha_contrib')
L += ['\n## 집중도\n',
      f"- 알파 기여 상위 5종목: {', '.join(top5.index)} → 합계 **{top5.alpha_contrib.sum():+.2f}%p** "
      f"(전체의 {top5.alpha_contrib.sum()/tot_alpha*100:.0f}%)",
      f"- 알파 기여 하위 5종목: {', '.join(bot5.index)} → 합계 {bot5.alpha_contrib.sum():+.2f}%p",
      f"- 리스크 기여 상위 5종목: {', '.join(d.nlargest(5,'risk_contrib').index)} → "
      f"합계 {d.nlargest(5,'risk_contrib').risk_contrib.sum():.2f}%p (전체의 {d.nlargest(5,'risk_contrib').risk_contrib.sum()/tot_risk*100:.0f}%)",
      f"- TOP10 비중 {d.nlargest(10,'mp_weight').mp_weight.sum():.1f}% · "
      f"HHI {(d.mp_weight**2).sum()/10000:.4f} · 유효종목수 {10000/(d.mp_weight**2).sum():.1f}"]

d.to_csv('mp_v51_attribution.csv')
open('mp_v51_attribution.md','w').write('\n'.join(L))
print('\n'.join(L[:12])); print('...'); print('\n'.join(L[-8:]))
