#!/usr/bin/env python3
"""MP v4.7 미국 종목 밸류에이션·재무 정밀 수집 + 포트폴리오 퀀트 지표.

클라우드에서는 egress 정책(403)으로 야후·미니 API 접근이 막혀 있어 **미니에서 실행**한다.
  cd ~/research_archive/20_미국주식/mp_quant && python3 mp_quant_metrics.py
입력: mp_v47_weights.csv (108종목 + 제외 15종의 BM 비중)
출력: mp_v47_fundamentals.csv (종목별 밸류·재무), mp_v47_portfolio_metrics.md (가중 지표)

의존: yfinance, pandas, numpy (미니 체인 환경에 이미 설치됨)
주의: CBRS(세레브라스)는 티커 미확정 — 실패 시 건너뛰고 커버리지에 기록된다.
"""
import csv, math, os, sys, time
import numpy as np
import pandas as pd
import yfinance as yf

# 비중 파일은 환경변수로 갈아끼운다: WEIGHTS=mp_v48_weights.csv python3 ...
WEIGHTS = os.environ.get('WEIGHTS', 'mp_v47_weights.csv')

MINI_API = 'https://benopenclaws-mac-mini.taile4cc1e.ts.net'

def probe():
    """실행 전 소스 도달성 점검 — 어느 경로가 열렸는지 먼저 확인한다."""
    import urllib.request
    for name, url in [('mini', MINI_API + '/api/source'),
                      ('yahoo', 'https://query1.finance.yahoo.com/v8/finance/chart/AAPL?range=5d&interval=1d')]:
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                print(f'[probe] {name}: {r.status}')
        except Exception as e:
            print(f'[probe] {name}: FAIL {type(e).__name__} {str(e)[:60]}')

if '--probe' in sys.argv:
    probe(); sys.exit(0)
probe()

W = pd.read_csv(WEIGHTS)
held = W[W.mp_weight > 0].copy()

# --reuse: 이미 뽑아둔 mp_v47_fundamentals.csv 를 다시 쓴다(지표 계산만 재실행할 때).
REUSE = '--reuse' in sys.argv
rows, miss = [], []
# 수집 대상 = MP 보유 ∪ BM 비중 보유(제외 15종) — BM 가중 지표를 통념치가 아니라 실측으로 비교한다.
UNIV = list(dict.fromkeys(list(held.ticker) + list(W[W.bm_weight_approx > 0].ticker)))
for t in ([] if REUSE else UNIV):
    try:
        tk = yf.Ticker(t); info = tk.info or {}
        rows.append({
            'ticker': t,
            'price': info.get('currentPrice'),
            'mktcap_b': (info.get('marketCap') or 0)/1e9,
            'fwd_pe': info.get('forwardPE'), 'trail_pe': info.get('trailingPE'),
            'psr': info.get('priceToSalesTrailing12Months'), 'pbr': info.get('priceToBook'),
            'ev_ebitda': info.get('enterpriseToEbitda'), 'peg': info.get('pegRatio'),
            'rev_growth': info.get('revenueGrowth'), 'eps_growth': info.get('earningsGrowth'),
            'gross_margin': info.get('grossMargins'), 'op_margin': info.get('operatingMargins'),
            'fcf_b': (info.get('freeCashflow') or 0)/1e9, 'roe': info.get('returnOnEquity'),
            'debt_to_equity': info.get('debtToEquity'), 'beta': info.get('beta'),
            'div_yield': info.get('dividendYield'),
        })
        time.sleep(0.3)
    except Exception as e:
        miss.append((t, str(e)[:80]))

if REUSE:
    F = pd.read_csv('mp_v47_fundamentals.csv').set_index('ticker')
else:
    F = pd.DataFrame(rows).set_index('ticker')
    F.to_csv('mp_v47_fundamentals.csv')

M = held.set_index('ticker').join(F)
wts = M.mp_weight / M.mp_weight.sum()

# 비율 지표는 회계 이벤트 한 종목이 전체를 지배한다(MSTR 영업이익률 −6808% → BM 마진 −29.9%p).
# 마진·ROE는 ±100%로 윈저화한 뒤 가중한다. 배수(P/E 등)는 조화평균이 이미 극단치에 둔감하다.
WINSOR = {'gross_margin', 'op_margin', 'roe', 'rev_growth', 'eps_growth'}

def _clip(col, s):
    return s.clip(-1.0, 1.0) if col in WINSOR else s

def wavg(col, harmonic=False, cover_min=0.5):
    s = _clip(col, M[col]); ok = s.notna() & np.isfinite(s)
    if harmonic: ok &= s > 0
    cov = wts[ok].sum()
    if cov < cover_min: return None, cov
    w = wts[ok] / wts[ok].sum()
    val = 1.0/ (w / s[ok]).sum() if harmonic else (w * s[ok]).sum()
    return val, cov

lines = ['# MP v4.7 포트폴리오 퀀트 지표 (실측)\n', f'수집 종목 {len(F)}/{len(held)} · 실패: {miss}\n']
for label, col, hm, pct in [
    ('가중 Fwd P/E(조화)', 'fwd_pe', True, False), ('가중 PSR(조화)', 'psr', True, False),
    ('가중 EV/EBITDA(조화)', 'ev_ebitda', True, False), ('가중 PEG', 'peg', False, False),
    
    ('가중 매출총이익률', 'gross_margin', False, True), ('가중 영업이익률', 'op_margin', False, True),
    ('가중 ROE', 'roe', False, True), ('가중 베타', 'beta', False, False),
    ('가중 배당수익률', 'div_yield', False, False),   # yfinance dividendYield는 이미 % 단위(PEP 4.13) — 100 곱하지 않는다
]:
    v, cov = wavg(col, harmonic=hm)
    if v is None: lines.append(f'- {label}: 커버리지 부족({cov:.0%})')
    elif col == 'div_yield': lines.append(f'- {label}: {v:.2f}% (커버리지 {cov:.0%})')
    else: lines.append(f'- {label}: {v*100:.1f}% (커버리지 {cov:.0%})' if pct else f'- {label}: {v:.2f} (커버리지 {cov:.0%})')

# 성장률은 분기 기저효과 아웃라이어(CIEN +2383%, DDOG +1499% 등)가 가중평균을 지배한다.
# ±100%로 윈저화한 값과 가중중앙값을 함께 적어 어느 쪽을 읽어야 하는지 남긴다.
def wmedian(col):
    s = M[col]; ok = s.notna() & np.isfinite(s)
    if not ok.any(): return None
    d = pd.DataFrame({'v': s[ok], 'w': wts[ok]}).sort_values('v')
    c = d.w.cumsum() / d.w.sum()
    return float(d.v[c >= 0.5].iloc[0])

for label, col in [('매출성장', 'rev_growth'), ('EPS성장', 'eps_growth')]:
    s = M[col]; ok = s.notna() & np.isfinite(s)
    w = wts[ok] / wts[ok].sum()
    wins = float((w * s[ok].clip(-1.0, 1.0)).sum())
    med = wmedian(col)
    lines.append(f'- 가중 {label}(윈저화 ±100%): {wins*100:.1f}% · 가중중앙값 {med*100:.1f}% (커버리지 {wts[ok].sum():.0%})')

# 2년 일별 수익률로 TE·베타 실측 (BM: QQQ)
try:
    tickers = list(held.ticker) + ['QQQ']
    px = yf.download(tickers, period='2y', interval='1d', auto_adjust=True, progress=False)['Close']
    rets = px.pct_change().dropna(how='all')
    avail = [t for t in held.ticker if t in rets.columns and rets[t].notna().sum() > 250]
    w2 = held.set_index('ticker').loc[avail, 'mp_weight']; w2 = w2/w2.sum()
    port = (rets[avail] * w2).sum(axis=1)
    bm = rets['QQQ']; both = pd.concat([port, bm], axis=1).dropna(); both.columns=['p','b']
    te = (both.p - both.b).std() * math.sqrt(252)
    beta = both.p.cov(both.b) / both.b.var()
    vol = both.p.std()*math.sqrt(252)
    lines += [f'- 실측 TE(2y, vs QQQ): {te:.1%}', f'- 실측 베타: {beta:.2f}', f'- 연율 변동성: {vol:.1%}',
              f'- 가격 커버리지: {len(avail)}/{len(held)} (신규 상장 제외 시 축소 복제 가정)']

    # 샤프 비율: rf는 ^IRX(13주 T-bill) 최근값, 실패 시 4.0% 고정
    try:
        rf = float(yf.download('^IRX', period='5d', progress=False)['Close'].dropna().iloc[-1]) / 100
    except Exception:
        rf = 0.04
    ann_ret_p = (1 + both.p).prod() ** (252 / len(both)) - 1
    ann_ret_b = (1 + both.b).prod() ** (252 / len(both)) - 1
    bvol = both.b.std() * math.sqrt(252)
    lines += [f'- 무위험수익률(rf): {rf:.2%}',
              f'- 실현 샤프(2y): MP {(ann_ret_p-rf)/vol:.2f} vs QQQ {(ann_ret_b-rf)/bvol:.2f}',
              f'- 정보비율(IR, 2y): {(ann_ret_p-ann_ret_b)/te:.2f}',
              '- 주의: 실현 샤프는 백테스트(현재 비중 고정)라 선택 편향 있음 — 기대 샤프가 아니다']

    # MDD: 백테스트 포트 vs QQQ (2y)
    def mdd(series):
        cum = (1 + series).cumprod(); peak = cum.cummax()
        dd = cum/peak - 1
        return dd.min(), dd
    mp_mdd, mp_dd = mdd(both.p); bm_mdd, _ = mdd(both.b)
    lines += [f'- 실측 MDD(2y): MP {mp_mdd:.1%} vs QQQ {bm_mdd:.1%}',
              f'- 현재 드로다운(고점 대비): {mp_dd.iloc[-1]:.1%}',
              f'- 일간 VaR95/99(역사적): {both.p.quantile(0.05):.2%} / {both.p.quantile(0.01):.2%}']
except Exception as e:
    lines.append(f'- TE/베타/샤프/MDD 실측 실패: {e}')

# BM(추적분) 가중 지표 — 같은 조화/산술 방식으로 계산해 MP와 직접 비교한다.
B = W[W.bm_weight_approx > 0].set_index('ticker').join(F)
bw = B.bm_weight_approx / B.bm_weight_approx.sum()

def bwavg(col, harmonic=False):
    s2 = _clip(col, B[col]); ok = s2.notna() & np.isfinite(s2)
    if harmonic: ok &= s2 > 0
    if not ok.any(): return None, 0.0
    w = bw[ok] / bw[ok].sum()
    return (1.0/(w/s2[ok]).sum() if harmonic else (w*s2[ok]).sum()), bw[ok].sum()

lines.append(f'\n## BM(추적분 {W.bm_weight_approx.sum():.1f}% / NDX) 실측 비교')
for label, col, hm, pct in [('Fwd P/E(조화)','fwd_pe',True,False), ('PSR(조화)','psr',True,False),
                            ('EV/EBITDA(조화)','ev_ebitda',True,False), ('PEG','peg',False,False),
                            ('매출총이익률','gross_margin',False,True), ('영업이익률','op_margin',False,True),
                            ('ROE','roe',False,True), ('베타','beta',False,False)]:
    mv, mc = wavg(col, harmonic=hm); bv, bc = bwavg(col, harmonic=hm)
    if mv is None or bv is None: lines.append(f'- {label}: 커버리지 부족'); continue
    f = (lambda x: f'{x*100:.1f}%') if pct else (lambda x: f'{x:.2f}')
    lines.append(f'- {label}: MP {f(mv)} vs BM {f(bv)} (커버리지 MP {mc:.0%}·BM {bc:.0%})')
for label, col in [('매출성장(윈저 ±100%)','rev_growth'), ('EPS성장(윈저 ±100%)','eps_growth')]:
    ms = M[col]; mok = ms.notna() & np.isfinite(ms)
    bs = B[col]; bok = bs.notna() & np.isfinite(bs)
    mv = float(((wts[mok]/wts[mok].sum()) * ms[mok].clip(-1,1)).sum())
    bv = float(((bw[bok]/bw[bok].sum()) * bs[bok].clip(-1,1)).sum())
    lines.append(f'- {label}: MP {mv*100:.1f}% vs BM {bv*100:.1f}%')

open('mp_v47_portfolio_metrics.md','w').write('\n'.join(lines))
print('\n'.join(lines))
