#!/usr/bin/env python3
"""AI 에이전트 생태계 20종목 포트폴리오 — 구성·전 지표 산출.

설계 지시(2026-08-25):
  · CPU 최대한 축소 → INTC·AMD·ARM **전량 미보유**
  · 스토리지·NAND·DRAM·소부장·클라우드(대형)·네오클라우드 **비중 상향**
  · GOOGL 언더웨이트 · TSLA 언더웨이트(미보유) · SPCX 중립(시총 비중 수준)
BM은 S&P 500. ASML·ENTG·CRWV·NBIS·IREN·SPCX는 BM 밖이다.
"""
import math, time, json
import numpy as np, pandas as pd, yfinance as yf

FX, RF = 1410.0, 0.0372

PORT = [
    # (티커, 비중, 그룹)
    ('MU',   9.0, 'DRAM·NAND'),   ('SNDK', 5.5, 'DRAM·NAND'),
    ('WDC',  4.0, '스토리지'),     ('STX',  4.0, '스토리지'),  ('NTAP', 2.0, '스토리지'),
    ('AMAT', 5.0, '소부장'),       ('LRCX', 5.0, '소부장'),    ('KLAC', 4.0, '소부장'),
    ('ASML', 4.0, '소부장'),       ('ENTG', 2.0, '소부장'),
    ('MSFT',10.0, '클라우드(대형)'),('AMZN', 8.0, '클라우드(대형)'),
    ('ORCL', 5.0, '클라우드(대형)'),('GOOGL',3.0, '클라우드(대형)'),
    ('CRWV', 4.0, '네오클라우드'),  ('NBIS', 4.0, '네오클라우드'), ('IREN', 3.0, '네오클라우드'),
    ('NVDA',10.0, 'AI 인프라'),    ('AVGO', 6.0, 'AI 인프라'),
    ('SPCX', 2.5, '우주·중립'),   # 시총 비중 2.46% = 중립
]
EXCLUDED = {'INTC': 'CPU', 'AMD': 'CPU', 'ARM': 'CPU', 'TSLA': '언더웨이트 지시'}

P = pd.DataFrame(PORT, columns=['ticker', 'weight', 'group']).set_index('ticker')
assert abs(P.weight.sum() - 100) < 1e-6, P.weight.sum()
U = pd.read_csv('sp500_universe.csv').set_index('ticker')
P['bm'] = U.bm_weight.reindex(P.index).fillna(0.0)
P['active'] = P.weight - P.bm
SP500_MC = float(U.mktcap.sum())

# ── 종목별 실측
rows = []
for t in list(P.index) + list(EXCLUDED):
    try:
        tk = yf.Ticker(t); i = tk.info or {}
        px = i.get('currentPrice') or i.get('regularMarketPrice')
        adv = (i.get('averageVolume') or 0) * (px or 0)
        g2 = np.nan
        try:
            ee = tk.earnings_estimate
            if ee is not None and '0y' in ee.index and '+1y' in ee.index:
                b_, y1_ = float(ee.loc['0y', 'yearAgoEps']), float(ee.loc['+1y', 'avg'])
                if b_ > 0 and y1_ > 0: g2 = (y1_ / b_) ** 0.5 - 1
                n_an = float(ee.loc['+1y', 'numberOfAnalysts'])
        except Exception: n_an = np.nan
        tgt = np.nan
        try:
            ap = tk.analyst_price_targets or {}
            if ap.get('median') and px: tgt = float(ap['median']) / px - 1
        except Exception: pass
        rows.append(dict(ticker=t, name=(i.get('shortName') or '')[:24], price=px,
            mktcap=i.get('marketCap'), fwd_pe=i.get('forwardPE'),
            psr=i.get('priceToSalesTrailing12Months'), pbr=i.get('priceToBook'),
            opm=i.get('operatingMargins'), gpm=i.get('grossMargins'),
            roe=i.get('returnOnEquity'), rev_g=i.get('revenueGrowth'),
            growth_2y=g2, target_upside=tgt, n_analysts=n_an,
            beta_i=i.get('beta'), div_yield=i.get('dividendYield'),
            total_debt=i.get('totalDebt'), total_cash=i.get('totalCash'),
            ebitda=i.get('ebitda'), fcf=i.get('freeCashflow'),
            short_pct=i.get('shortPercentOfFloat'), adv_usd=adv,
            sector=i.get('sector', '')))
        time.sleep(0.25)
    except Exception as e:
        rows.append(dict(ticker=t, err=str(e)[:40]))
M = pd.DataFrame(rows).set_index('ticker')
M['net_debt'] = M.total_debt.fillna(0) - M.total_cash.fillna(0)
M['nd_ebitda'] = M.net_debt / M.ebitda.replace(0, np.nan)
D = P.join(M)

# ── 가격 기반 위험 지표
px = yf.download(list(P.index) + ['SPY'], period='3y', interval='1d',
                 auto_adjust=True, progress=False)['Close']
r = px.pct_change().dropna(how='all')
av = [t for t in P.index if t in r.columns and r[t].notna().sum() > 200]
short_hist = [t for t in P.index if t not in av]
wa = P.weight.reindex(av) / P.weight.reindex(av).sum()
R = r[av].dropna()
bm = r['SPY'].reindex(R.index)
port = (R * wa).sum(axis=1)
both = pd.concat([port, bm], axis=1).dropna(); both.columns = ['p', 'b']
ann = lambda s: (1 + s).prod() ** (252 / len(s)) - 1
dsd = lambda s: float(np.sqrt((s[s < 0] ** 2).mean())) * math.sqrt(252)
cum = (1 + both.p).cumprod(); dd = cum / cum.cummax() - 1
cumb = (1 + both.b).cumprod(); ddb = cumb / cumb.cummax() - 1
up, dn = both[both.b > 0], both[both.b < 0]
corr = R.corr(); iu = np.triu_indices_from(corr.values, 1)
w_all = P.weight / P.weight.sum()
for t in av:
    x = r[t].dropna()
    D.loc[t, 'vol_3y'] = float(x.std()) * math.sqrt(252)
    j = pd.concat([x, r['SPY']], axis=1).dropna(); j.columns = ['p', 'b']
    D.loc[t, 'beta_spy'] = float(j.p.cov(j.b) / j.b.var())
    D.loc[t, 'corr_spy'] = float(j.p.corr(j.b))

def wm(col, src=None):
    s = (src if src is not None else D)[col]
    ok = s.notna() & np.isfinite(s)
    ww = w_all[ok]
    return float((ww / ww.sum() * s[ok]).sum()) if ok.any() else np.nan

AGG = dict(
    te=float((both.p - both.b).std()) * math.sqrt(252),
    beta=float(both.p.cov(both.b) / both.b.var()),
    vol=float(both.p.std()) * math.sqrt(252),
    dsd=dsd(both.p), mdd=float(dd.min()), mdd_b=float(ddb.min()),
    var95=float(both.p.quantile(0.05)), var99=float(both.p.quantile(0.01)),
    p_ann=ann(both.p), b_ann=ann(both.b),
    # 캡처 비율: 상승/하락일의 **평균 수익률 비**. 상승일만 연율화하면 값이 폭발한다
    # (초안에서 1622%가 나왔다) — 표준 정의대로 평균 대 평균으로 잰다.
    up_cap=float(up.p.mean() / up.b.mean()), dn_cap=float(dn.p.mean() / dn.b.mean()),
    beta_up=float(up.p.cov(up.b) / up.b.var()), beta_dn=float(dn.p.cov(dn.b) / dn.b.var()),
    avg_corr=float(corr.values[iu].mean()),
    wavg_vol=wm('vol_3y'), worst_day=float(both.p.min()),
    worst_21=float(both.p.rolling(21).sum().min()),
    hhi=float((P.weight ** 2).sum() / 10000), top10=float(P.weight.nlargest(10).sum()),
    fwd_pe=wm('fwd_pe'), psr=wm('psr'), opm=wm('opm'), gpm=wm('gpm'), roe=wm('roe'),
    growth_2y=wm('growth_2y'), target_upside=wm('target_upside'),
    n_analysts=wm('n_analysts'), div_yield=wm('div_yield'),
    nd_ebitda=wm('nd_ebitda'), short_pct=wm('short_pct'),
    adv_wavg=wm('adv_usd'), bm_out=float(P[P.bm == 0].weight.sum()),
    cpu_uw=float(-U.bm_weight.reindex(['INTC', 'AMD']).fillna(0).sum()),
    tsla_uw=float(-U.bm_weight.get('TSLA', 0)),
    spcx_mc_share=float(M.mktcap.get('SPCX', np.nan) / SP500_MC * 100),
)
AGG['sortino'] = (AGG['p_ann'] - RF) / AGG['dsd']
AGG['calmar'] = AGG['p_ann'] / abs(AGG['mdd'])
AGG['diversification'] = 1 - AGG['vol'] / AGG['wavg_vol']
AGG['sharpe'] = (AGG['p_ann'] - RF) / AGG['vol']

D.to_csv('agent20_holdings.csv')
pd.Series(AGG).to_csv('agent20_agg.csv')
json.dump({'short_hist': short_hist}, open('agent20_meta.json', 'w'))
print(f'20종목 · 합계 {P.weight.sum():.1f}% · BM외 {AGG["bm_out"]:.1f}%')
print(f'가격이력 부족(3년 미만): {short_hist}')
for k, v in AGG.items(): print(f'  {k:16s} {v:,.4f}')
