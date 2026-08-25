#!/usr/bin/env python3
"""MP v5.1 운용역 지표 수집 — 기존 자료에 없던 축을 채운다.

기존(밸류·성장·수익성·TE/베타/MDD·기여도·기술레벨) 외에 운용역이 실제로 보는 것:
  유동성·청산일수 / 주주환원 / 재무건전성 / 숏인터레스트 / 실적일정 /
  하방위험(하방편차·소르티노·칼마·상승하락캡처) / 팩터노출 / 상관·분산
실행: ssh mini-lan 'cd ~/research_archive/20_미국주식/mp_quant && python3 mp_v51_pm_metrics.py'
"""
import math, os, time
import numpy as np, pandas as pd, yfinance as yf

WEIGHTS = os.environ.get('WEIGHTS', 'mp_v51_weights.csv')
AUM_KRW = float(os.environ.get('AUM_KRW', 1000e8))     # 가정 운용규모 1,000억원
FX = float(os.environ.get('FX', 1410.0))               # 원/달러
AUM_USD = AUM_KRW / FX
PARTICIPATION = 0.20                                    # 일 거래대금 참여율 20% 가정

W = pd.read_csv(WEIGHTS).set_index('ticker')
held = W[W.mp_weight > 0]
print(f'보유 {len(held)}종목 · 가정 AUM {AUM_KRW/1e8:,.0f}억원(${AUM_USD/1e6:,.0f}M) · 참여율 {PARTICIPATION:.0%}')

rows = []
for t in held.index:
    try:
        tk = yf.Ticker(t); i = tk.info or {}
        px = i.get('currentPrice') or i.get('regularMarketPrice')
        vol = i.get('averageVolume') or i.get('averageDailyVolume10Day')
        adv = (vol or 0) * (px or 0)                    # 일평균 거래대금(USD)
        pos = AUM_USD * float(held.mp_weight[t]) / 100   # 이 종목 포지션 금액
        rows.append(dict(
            ticker=t, price=px, mktcap=i.get('marketCap'),
            adv_usd=adv, position_usd=pos,
            days_to_liq=(pos / (adv * PARTICIPATION)) if adv else np.nan,
            # 주주환원
            div_yield=i.get('dividendYield'), payout=i.get('payoutRatio'),
            buyback_yield=None,
            # 재무건전성
            total_debt=i.get('totalDebt'), total_cash=i.get('totalCash'),
            ebitda=i.get('ebitda'), debt_to_equity=i.get('debtToEquity'),
            current_ratio=i.get('currentRatio'), fcf=i.get('freeCashflow'),
            # 숏 인터레스트
            short_pct_float=i.get('shortPercentOfFloat'), short_ratio=i.get('shortRatio'),
            # 밸류·퀄리티 팩터 원자료
            pbr=i.get('priceToBook'), roe=i.get('returnOnEquity'),
            op_margin=i.get('operatingMargins'), rev_growth=i.get('revenueGrowth'),
        ))
        time.sleep(0.25)
    except Exception as e:
        rows.append(dict(ticker=t, err=str(e)[:40]))

M = pd.DataFrame(rows).set_index('ticker')
M['net_debt'] = (M.total_debt.fillna(0) - M.total_cash.fillna(0))
M['nd_ebitda'] = M.net_debt / M.ebitda.replace(0, np.nan)

# --- 가격 기반: 하방위험·팩터·상관 ---
px = yf.download(list(held.index) + ['SPY'], period='3y', interval='1d',
                 auto_adjust=True, progress=False)['Close']
r = px.pct_change().dropna(how='all')
av = [t for t in held.index if t in r.columns and r[t].notna().sum() > 400]
bm = r['SPY']

def downside_dev(x, mar=0.0):
    d = x[x < mar]
    return float(np.sqrt((d ** 2).mean())) * math.sqrt(252) if len(d) else np.nan

for t in av:
    x = r[t].dropna()
    j = pd.concat([x, bm], axis=1).dropna(); j.columns = ['p', 'b']
    up, dn = j[j.b > 0], j[j.b < 0]
    M.loc[t, 'mom_12_1'] = float(px[t].iloc[-21] / px[t].iloc[-252] - 1) if len(px[t].dropna()) > 252 else np.nan
    M.loc[t, 'vol_3y'] = float(x.std()) * math.sqrt(252)
    M.loc[t, 'downside_dev'] = downside_dev(x)
    M.loc[t, 'beta_up'] = float(up.p.cov(up.b) / up.b.var()) if len(up) > 30 else np.nan
    M.loc[t, 'beta_dn'] = float(dn.p.cov(dn.b) / dn.b.var()) if len(dn) > 30 else np.nan
    M.loc[t, 'corr_spy'] = float(j.p.corr(j.b))

M.to_csv('mp_v51_pm_metrics.csv')

# --- 포트 집계 ---
w = held.mp_weight.reindex(M.index) / held.mp_weight.sum()
R = r[av].dropna()
wa = (held.mp_weight.reindex(av) / held.mp_weight.reindex(av).sum())
port = (R * wa).sum(axis=1)
both = pd.concat([port, bm.reindex(R.index)], axis=1).dropna(); both.columns = ['p', 'b']
ann = lambda s: (1 + s).prod() ** (252 / len(s)) - 1
cum = (1 + both.p).cumprod(); dd = cum / cum.cummax() - 1
cumb = (1 + both.b).cumprod(); ddb = cumb / cumb.cummax() - 1
RF = 0.0372
p_ann, b_ann = ann(both.p), ann(both.b)
p_vol = float(both.p.std()) * math.sqrt(252)
p_dd = downside_dev(both.p)
up, dn = both[both.b > 0], both[both.b < 0]

corr_m = R.corr()
iu = np.triu_indices_from(corr_m.values, 1)
avg_corr = float(corr_m.values[iu].mean())
wavg_vol = float((w.reindex(av) / w.reindex(av).sum() * M.vol_3y.reindex(av)).sum())

agg = dict(
    days_to_liq_wavg=float((w * M.days_to_liq).sum(skipna=True)),
    days_to_liq_max=float(M.days_to_liq.max()),
    div_yield=float((w * M.div_yield.fillna(0)).sum()),
    nd_ebitda=float((w * M.nd_ebitda.clip(-5, 10)).sum(skipna=True)),
    short_pct=float((w * M.short_pct_float.fillna(0)).sum()) * 100,
    downside_dev=p_dd, sortino=(p_ann - RF) / p_dd if p_dd else np.nan,
    calmar=p_ann / abs(float(dd.min())) if dd.min() else np.nan,
    up_capture=float(ann(up.p) / ann(up.b)) if len(up) > 30 else np.nan,
    dn_capture=float(ann(dn.p) / ann(dn.b)) if len(dn) > 30 else np.nan,
    beta_up=float(up.p.cov(up.b) / up.b.var()), beta_dn=float(dn.p.cov(dn.b) / dn.b.var()),
    avg_corr=avg_corr, wavg_vol=wavg_vol, port_vol=p_vol,
    diversification=1 - p_vol / wavg_vol,
    p_ann=p_ann, b_ann=b_ann, mdd=float(dd.min()), mdd_b=float(ddb.min()),
    worst_day=float(both.p.min()), worst_month=float(both.p.rolling(21).sum().min()),
)
pd.Series(agg).to_csv('mp_v51_pm_agg.csv')
for k, v in agg.items(): print(f'  {k:20s} {v:.4f}')
