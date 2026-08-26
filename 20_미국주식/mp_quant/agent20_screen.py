#!/usr/bin/env python3
"""AI 에이전트 생태계 20종목 — 후보 스크리닝."""
import time
import numpy as np, pandas as pd, yfinance as yf

CAND = {
 'DRAM/NAND/스토리지': ['MU','WDC','STX','SNDK','NTAP','PSTG'],
 '반도체 소부장':      ['AMAT','LRCX','KLAC','ASML','ENTG','TER','ONTO','MKSI','ACLS'],
 '클라우드(대형)':     ['MSFT','AMZN','GOOGL','ORCL'],
 '네오클라우드':       ['CRWV','NBIS','IREN','APLD','CIFR','WULF'],
 'AI 인프라':          ['NVDA','AVGO','MRVL','ANET','VRT','COHR'],
 'UW/중립 대상':       ['TSLA','SPCX'],
}
rows = []
for g, ts in CAND.items():
    for t in ts:
        try:
            i = yf.Ticker(t).info or {}
            mc, px = i.get('marketCap'), i.get('currentPrice') or i.get('regularMarketPrice')
            if not mc:
                rows.append(dict(group=g, ticker=t, note='데이터없음')); continue
            adv = (i.get('averageVolume') or 0) * (px or 0)
            rows.append(dict(group=g, ticker=t, name=(i.get('shortName') or '')[:20],
                mktcap_b=mc/1e9, price=px, fwd_pe=i.get('forwardPE'),
                psr=i.get('priceToSalesTrailing12Months'),
                opm=i.get('operatingMargins'), rev_g=i.get('revenueGrowth'),
                adv_m=adv/1e6, beta=i.get('beta'),
                exch=i.get('fullExchangeName','')[:8]))
            time.sleep(0.25)
        except Exception as e:
            rows.append(dict(group=g, ticker=t, note=str(e)[:25]))
D = pd.DataFrame(rows)
pd.set_option('display.width', 250)
print(D.round(2).to_string(index=False))
D.to_csv('agent20_candidates.csv', index=False)
