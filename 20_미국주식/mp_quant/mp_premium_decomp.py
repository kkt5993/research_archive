#!/usr/bin/env python3
"""역사 대비 비싼 종목 — 배수 프리미엄이 무엇으로 뒷받침되는가.

'역사보다 비싸다'는 그 자체로 매도 근거가 아니다. 두 경우를 갈라야 한다.
  (a) 펀더멘털은 그대로인데 배수만 올랐다        → 순수 리레이팅, 회귀 위험 실재
  (b) 사업 구조가 바뀌어 과거 배수가 다른 회사 것 → 역사 비교 자체가 함정
가르는 방법: 최근 4개 회계연도의 주가 상승을 **이익 성장 기여 vs 배수 변화 기여**로
분해하고, 매출 성장·영업마진 궤적으로 사업 구조 변화를 확인한다.
실행: ssh mini-lan 'cd ~/research_archive/20_미국주식/mp_quant && python3 mp_premium_decomp.py'
"""
import os
import numpy as np, pandas as pd

# 비중 파일은 환경변수로 갈아끼운다: WEIGHTS=mp_v48_weights.csv python3 ...
WEIGHTS = os.environ.get('WEIGHTS', 'mp_v47_weights.csv')
import yfinance as yf

S = pd.read_csv('mp_v47_stock_levels.csv').set_index('ticker')
W = pd.read_csv(WEIGHTS).set_index('ticker')
mp = W[W.mp_weight > 0]
d = mp.join(S)
tgt = d[d.pe_revert_full < 0].sort_values('mp_weight', ascending=False)

rows = []
for t in tgt.index:
    r = dict(ticker=t, mp=tgt.loc[t, 'mp_weight'],
             bm=tgt.loc[t, 'bm_weight_approx'],
             active=tgt.loc[t, 'mp_weight'] - tgt.loc[t, 'bm_weight_approx'],
             premium=tgt.loc[t, 'pe_revert_full'], sector=tgt.loc[t, 'sector'])
    try:
        tk = yf.Ticker(t); a = tk.income_stmt
        def row(name):
            k = next((x for x in a.index if str(x) == name), None)
            return a.loc[k].dropna().astype(float).sort_index() if k is not None else None
        rev, ni = row('Total Revenue'), row('Net Income')
        op = row('Operating Income')
        if rev is not None and len(rev) >= 3:
            n = len(rev) - 1
            r['rev_cagr'] = (rev.iloc[-1] / rev.iloc[0]) ** (1 / n) - 1 if rev.iloc[0] > 0 else np.nan
            r['rev_now_b'] = rev.iloc[-1] / 1e9
            if op is not None and len(op) == len(rev):
                r['opm_then'] = float(op.iloc[0] / rev.iloc[0])
                r['opm_now']  = float(op.iloc[-1] / rev.iloc[-1])
        eps = row('Diluted EPS')
        if eps is not None and len(eps) >= 3 and eps.iloc[0] > 0 and eps.iloc[-1] > 0:
            n = len(eps) - 1
            r['eps_cagr'] = (eps.iloc[-1] / eps.iloc[0]) ** (1 / n) - 1
            # 같은 구간 주가 CAGR → 배수 변화 기여 = 주가 − 이익
            px = yf.download(t, period='5y', interval='1d', auto_adjust=True, progress=False)['Close'].dropna()
            p0 = float(px[px.index <= pd.Timestamp(eps.index[0])].iloc[-1]) if len(px[px.index <= pd.Timestamp(eps.index[0])]) else np.nan
            p1 = float(px.iloc[-1])
            if p0 == p0 and p0 > 0:
                r['px_cagr'] = (p1 / p0) ** (1 / n) - 1
                r['mult_cagr'] = (1 + r['px_cagr']) / (1 + r['eps_cagr']) - 1
    except Exception as e:
        r['err'] = str(e)[:40]
    rows.append(r)

D = pd.DataFrame(rows).set_index('ticker')
D.to_csv('mp_v47_premium_decomp.csv')

def f(v, spec='{:+.0%}'):
    return '—' if v is None or v != v else spec.format(v)

L = ['# 역사 대비 비싼 종목 — 프리미엄의 출처 분해 (2026-08-25)\n',
     f'MP 108종목 중 자기 역사 forward 배수보다 비싼 종목 **{len(D)}개, 비중 {tgt.mp_weight.sum():.1f}%**.\n',
     '`배수기여`가 `이익기여`보다 크면 순수 리레이팅(회귀 위험), 반대면 이익이 배수를 따라잡은 것이다.',
     '매출 CAGR·영업마진 변화는 "과거 배수가 지금과 같은 회사의 것인가"를 본다.\n',
     '| 티커 | MP | 액티브 | 프리미엄 | 매출CAGR | 매출(B) | 영업마진 변화 | EPS CAGR | 주가CAGR | 배수기여 | 판정 |',
     '|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|']
for t, r in D.sort_values('mp', ascending=False).iterrows():
    verdict = '—'
    ec, mc = r.get('eps_cagr'), r.get('mult_cagr')
    rc, o0, o1 = r.get('rev_cagr'), r.get('opm_then'), r.get('opm_now')
    if ec == ec and mc == mc:
        if ec > 0.20 and (o1 == o1 and o0 == o0 and o1 > o0 + 0.03):
            verdict = '**구조 변화**'
        elif mc > ec:
            verdict = '리레이팅 우위'
        else:
            verdict = '이익이 견인'
    opm = f'{o0*100:.0f}→{o1*100:.0f}%' if (o0 == o0 and o1 == o1) else '—'
    L.append(f'| {t} | {r.mp:.1f} | {r.active:+.1f} | {f(r.premium)} | {f(rc)} | '
             f'{r.get("rev_now_b", float("nan")):.1f} | {opm} | {f(ec)} | {f(r.get("px_cagr"))} | '
             f'{f(mc)} | {verdict} |')
open('mp_v47_premium_decomp.md', 'w').write('\n'.join(L))
print('\n'.join(L))
