#!/usr/bin/env python3
"""S&P 500 유니버스 + 시총 가중 비중 산출.

구성종목: GitHub datasets/s-and-p-500-companies (GICS 섹터 포함, 503종목).
비중: yfinance 시총 기준 정규화 — **부동주 조정(float-adjusted)이 아니다.**
      실제 지수는 유동주식만 세므로 창업자·정부 보유가 큰 종목에서 과대 계상된다.
      절대 비중이 아니라 액티브 비중 계산의 기준선으로만 쓴다.
실행: ssh mini-lan 'cd ~/research_archive/20_미국주식/mp_quant && python3 sp500_universe.py'
"""
import io, time, urllib.request
import pandas as pd, numpy as np, yfinance as yf

UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) research/1.0'}
URL = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv'
raw = urllib.request.urlopen(urllib.request.Request(URL, headers=UA), timeout=30).read()
C = pd.read_csv(io.BytesIO(raw))
C['ticker'] = C.Symbol.str.replace('.', '-', regex=False)   # BRK.B → BRK-B (yfinance 표기)
print(f'구성종목 {len(C)}종목 · 섹터 {C["GICS Sector"].nunique()}개')

rows, miss = [], []
for n, t in enumerate(C.ticker, 1):
    try:
        i = yf.Ticker(t).info or {}
        mc = i.get('marketCap')
        if not mc: miss.append(t); continue
        rows.append(dict(ticker=t, mktcap=float(mc), price=i.get('currentPrice'),
                         fwd_pe=i.get('forwardPE'), beta=i.get('beta')))
        time.sleep(0.15)
    except Exception:
        miss.append(t)
    if n % 100 == 0: print(f'  {n}/{len(C)}')

M = pd.DataFrame(rows).set_index('ticker')
U = C.set_index('ticker').join(M, how='inner')
U['bm_weight'] = U.mktcap / U.mktcap.sum() * 100
U = U.sort_values('bm_weight', ascending=False)
U[['Security', 'GICS Sector', 'GICS Sub-Industry', 'mktcap', 'price', 'bm_weight']].to_csv('sp500_universe.csv')

print(f'시총 확보 {len(U)}/{len(C)} · 실패 {len(miss)}: {miss[:10]}')
print('\n섹터 비중:')
s = U.groupby('GICS Sector').bm_weight.sum().sort_values(ascending=False)
for k, v in s.items(): print(f'  {k:28s} {v:5.2f}%')
print('\nTOP15:')
print(U.head(15)[['Security', 'GICS Sector', 'bm_weight']].round(2).to_string())
