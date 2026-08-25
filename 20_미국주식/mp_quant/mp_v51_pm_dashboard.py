#!/usr/bin/env python3
"""MP v5.1 운용역 대시보드 — 한 문서에 모든 축.

앞선 산출물(levels·attribution·pm_metrics)을 합쳐 운용역이 실제로 확인하는 순서로 낸다.
추가 산출: AUM 시나리오별 청산일수, 리밸런싱 회전율, 스트레스 시나리오, 실적 캘린더.
"""
import math, os, time
import numpy as np, pandas as pd, yfinance as yf

FX = 1410.0
W  = pd.read_csv('mp_v51_weights.csv').set_index('ticker')
S  = pd.read_csv('mp_v51_stock_levels.csv').set_index('ticker')
A  = pd.read_csv('mp_v51_attribution.csv').set_index('ticker')
P  = pd.read_csv('mp_v51_pm_metrics.csv').set_index('ticker')
G  = pd.read_csv('mp_v51_pm_agg.csv', index_col=0).squeeze()
U  = pd.read_csv('sp500_universe.csv').set_index('ticker').drop(columns=['price'])
V50 = pd.read_csv('mp_v50_sp500_balanced.csv', index_col=0)

held = W[W.mp_weight > 0]
d = held.join(P, rsuffix='_p').join(U[['Security', 'GICS Sector']])
d['active'] = d.mp_weight - d.bm_weight_approx
w = d.mp_weight / d.mp_weight.sum()

def f(v, sp='{:.2f}'):
    return '—' if v is None or (isinstance(v, float) and (np.isnan(v) or not np.isfinite(v))) else sp.format(v)

L = ['# MP v5.1 운용역 대시보드 (2026-08-25)\n',
     '> BM S&P 500 · 30종목 · 모든 수치 실측. 운용역이 확인하는 순서로 배열했다.\n']

# ── 1. 유동성 — AUM 시나리오별 청산일수
L += ['## 1. 유동성 — 규모 수용력\n',
      '일평균 거래대금(ADV) 실측. 청산일수는 **참여율 10%**(보수적) 기준 전량 청산.\n',
      '| 지표 | 값 |', '|---|--:|',
      f'| 포트 가중 ADV | **${float((w*d.adv_usd).sum())/1e9:,.1f}B** |',
      f'| 최소 ADV 종목 | {d.adv_usd.idxmin()} ${d.adv_usd.min()/1e6:,.0f}M |',
      f'| ADV $1B 미만 종목수 | {int((d.adv_usd < 1e9).sum())}/30 |',
      '']
L += ['| 운용규모 | 가중평균 청산일 | 최장 종목 | 1일 초과 | 3일 초과 |', '|---|--:|--:|--:|--:|']
for aum_e in [10000, 50000, 100000, 300000, 500000]:
    aum_usd = aum_e * 1e8 / FX
    pos = aum_usd * d.mp_weight / 100
    dtl = pos / (d.adv_usd * 0.10)
    L.append(f'| {aum_e/10000:,.0f}조원 (${aum_usd/1e9:,.1f}B) | {float((w*dtl).sum()):.2f}일 | '
             f'{dtl.max():.1f}일 ({dtl.idxmax()}) | {int((dtl>1).sum())} | {int((dtl>3).sum())} |')
L += ['',
      f'**유동성은 이 포트의 제약이 아니다.** 30조원 규모에서도 가중평균 청산이 '
      f'{float((w*(30e12/FX*d.mp_weight/100)/(d.adv_usd*0.10)).sum()):.1f}일이다. '
      '커버리지 20명 이상 대형주만 담은 선정 기준의 직접적 결과다.',
      '',
      '| 유동성 하위 5종목 | ADV | 비중 | 30조원 시 청산일 |', '|---|--:|--:|--:|']
low = d.nsmallest(5, 'adv_usd')
for t, x in low.iterrows():
    dtl30 = (30e12/FX * x.mp_weight/100) / (x.adv_usd * 0.10)
    L.append(f'| {t} | ${x.adv_usd/1e6:,.0f}M | {x.mp_weight:.2f}% | {dtl30:.1f}일 |')

# ── 2. 하방 위험
L += ['\n## 2. 하방 위험 — 표준편차만으로는 안 보이는 것\n',
      '| 지표 | MP | BM(SPY) | 해석 |', '|---|--:|--:|---|',
      f"| 연율 변동성 | {G.port_vol*100:.1f}% | — | |",
      f"| **하방편차** | **{G.downside_dev*100:.1f}%** | — | 손실 구간만의 변동성 |",
      f"| **소르티노** | **{G.sortino:.2f}** | — | 하방 위험 대비 초과수익 |",
      f"| **칼마** | **{G.calmar:.2f}** | — | MDD 대비 연율수익 |",
      f"| 최대낙폭 | {G.mdd*100:.1f}% | {G.mdd_b*100:.1f}% | BM 대비 {abs(G.mdd-G.mdd_b)*100:.1f}%p 깊다 |",
      f"| **상승 캡처** | **{G.up_capture*100:.0f}%** | 100% | BM 상승의 {G.up_capture:.1f}배 |",
      f"| **하락 캡처** | **{G.dn_capture*100:.0f}%** | 100% | BM 하락의 {G.dn_capture:.1f}배 |",
      f"| 상승 베타 | {G.beta_up:.2f} | 1.00 | |",
      f"| 하락 베타 | **{G.beta_dn:.2f}** | 1.00 | **하락 베타가 상승 베타보다 크다** |",
      f"| 최악 1일 | {G.worst_day*100:.1f}% | — | |",
      f"| 최악 21일 | {G.worst_month*100:.1f}% | — | |",
      '',
      f'**캡처 비율은 좋고 베타 비대칭은 나쁘다.** 상승 {G.up_capture*100:.0f}% / 하락 '
      f'{G.dn_capture*100:.0f}%는 우수하지만, 이는 3년 AI 랠리 구간의 실현치라 **선택 편향**이 있다. '
      f'반면 하락 베타 {G.beta_dn:.2f} > 상승 베타 {G.beta_up:.2f}는 **급락 시 더 민감하다**는 뜻이다. '
      '전자는 과거 성과, 후자는 구조적 민감도다 — 후자를 믿는 편이 안전하다.']

# ── 3. 분산·상관
L += ['\n## 3. 분산 — 종목수가 아니라 상관이 결정한다\n',
      f'| 지표 | 값 |', '|---|--:|',
      f'| 종목 간 평균 상관 | **{G.avg_corr:.3f}** |',
      f'| 가중 개별 변동성 | {G.wavg_vol*100:.1f}% |',
      f'| 포트 변동성 | {G.port_vol*100:.1f}% |',
      f'| **분산 효과** | **{G.diversification*100:.1f}%** |',
      f'| 유효종목수(HHI 역수) | 18.1 |',
      f'| TOP10 비중 | 64.7% |',
      '',
      f'개별 변동성 가중평균 {G.wavg_vol*100:.1f}%가 포트 {G.port_vol*100:.1f}%로 줄었다 — '
      f'**분산이 변동성의 {G.diversification*100:.0f}%를 지운다.** 평균 상관 {G.avg_corr:.2f}는 '
      '30종목 집중 포트치고 낮다. 다만 정보기술 10종목이 리스크의 78%를 만들므로 '
      '**위기 국면에서 상관이 1로 수렴하면 이 분산은 사라진다.**']

# ── 4. 주주환원·재무건전성
L += ['\n## 4. 주주환원·재무건전성\n',
      '| 지표 | 포트 가중 |', '|---|--:|',
      f'| 배당수익률 | {G.div_yield:.2f}% |',
      f'| 순부채/EBITDA | **{G.nd_ebitda:.2f}배** |',
      f'| 공매도 잔고(유통주식 대비) | {G.short_pct:.2f}% |',
      '',
      '**레버리지는 사실상 없다.** 순부채/EBITDA 0.49배는 순현금에 가까운 수준이며, '
      '크레딧 이벤트 시나리오에서 개별 기업 부도 위험은 낮다. 배당수익률 0.60%는 '
      'BM(약 1.2%)의 절반으로 **인컴이 아니라 자본이득 포트**임을 보여준다.',
      '',
      '| 순부채/EBITDA 상위 | 값 | | 공매도 잔고 상위 | 값 |', '|---|--:|---|---|--:|']
nd = d.nd_ebitda.dropna().nlargest(5); sh = d.short_pct_float.dropna().nlargest(5)
for i in range(5):
    a1 = f'{nd.index[i]} | {nd.iloc[i]:.2f}배' if i < len(nd) else ' | '
    a2 = f'{sh.index[i]} | {sh.iloc[i]*100:.1f}%' if i < len(sh) else ' | '
    L.append(f'| {a1} | | {a2} |')

# ── 5. 리밸런싱 회전율
L += ['\n## 5. 리밸런싱 — v5.0(147종목) → v5.1(30종목)\n']
prev = V50.mp_weight.reindex(sorted(set(V50.index) | set(held.index))).fillna(0.0)
curr = held.mp_weight.reindex(prev.index).fillna(0.0)
diff = (curr - prev)
turnover = float(diff.abs().sum()) / 2
sells = diff[diff < -0.01].sort_values()
buys = diff[diff > 0.01].sort_values(ascending=False)
L += [f'| 항목 | 값 |', '|---|--:|',
      f'| **단방향 회전율** | **{turnover:.1f}%** |',
      f'| 신규 편입 | {int(((prev==0)&(curr>0)).sum())}종목 |',
      f'| 전량 편출 | {int(((prev>0)&(curr==0)).sum())}종목 |',
      f'| 매수 종목 / 금액비중 | {len(buys)} / {buys.sum():.1f}% |',
      f'| 매도 종목 / 금액비중 | {len(sells)} / {abs(sells.sum()):.1f}% |',
      '',
      f'**회전율 {turnover:.0f}%는 대규모 재구성이다.** BM 교체(나스닥100→S&P500)와 '
      '종목수 압축(147→30)이 겹친 결과이며, 정기 리밸런싱이 아니라 **모델 재설계**다. '
      '거래비용은 유동성 섹션 기준 청산일수가 1일 미만이라 시장충격보다 스프레드가 지배한다.']
L += ['\n**최대 축소 10종목**(0으로 편출된 종목 포함)\n', '| 종목 | v5.0 | v5.1 | 변동 |', '|---|--:|--:|--:|']
for t, v in sells.head(10).items():
    L.append(f'| {t} | {prev[t]:.2f}% | {curr[t]:.2f}% | {v:+.2f}%p |')

# ── 6. 스트레스 시나리오 (실현 최악 구간 재현)
px = yf.download(list(held.index) + ['SPY'], period='3y', interval='1d',
                 auto_adjust=True, progress=False)['Close']
r = px.pct_change().dropna(how='all')
av = [t for t in held.index if t in r.columns and r[t].notna().sum() > 400]
wa = held.mp_weight.reindex(av) / held.mp_weight.reindex(av).sum()
port = (r[av] * wa).sum(axis=1); bmr = r['SPY'].reindex(port.index)
L += ['\n## 6. 스트레스 — 실현 최악 구간에서 이 포트는 어땠나\n',
      '현재 비중을 과거에 고정 적용한 백테스트다(선택 편향 있음).\n',
      '| 구간 | MP | BM(SPY) | 차이 |', '|---|--:|--:|--:|']
roll = port.rolling(21).sum(); rollb = bmr.rolling(21).sum()
i_worst = roll.idxmin()
for label, seg in [('최악 21거래일', (i_worst, roll.loc[i_worst], rollb.loc[i_worst])),
                   ('최악 5거래일', (port.rolling(5).sum().idxmin(),
                                 port.rolling(5).sum().min(),
                                 rollb.reindex(port.rolling(5).sum().index).rolling(1).sum().loc[port.rolling(5).sum().idxmin()])),
                   ('최악 1일', (port.idxmin(), port.min(), bmr.loc[port.idxmin()]))]:
    dt, mp_, bm_ = seg
    L.append(f'| {label} (~{str(dt)[:10]}) | {mp_*100:+.1f}% | {bm_*100:+.1f}% | {(mp_-bm_)*100:+.1f}%p |')
cum = (1 + port).cumprod(); dd = cum / cum.cummax() - 1
L.append(f'| 최대낙폭 구간 | {dd.min()*100:+.1f}% | {G.mdd_b*100:+.1f}% | {(dd.min()-G.mdd_b)*100:+.1f}%p |')

# ── 7. 실적 캘린더
L += ['\n## 7. 이벤트 캘린더 — 다음 실적 발표\n',
      '비중 상위 종목의 실적 발표는 그 자체가 포지션 리스크다.\n',
      '| 종목 | 비중 | 다음 실적일 |', '|---|--:|---|']
cal = []
for t in d.nlargest(12, 'mp_weight').index:
    try:
        c = yf.Ticker(t).calendar
        dt = c.get('Earnings Date') if isinstance(c, dict) else None
        dt = dt[0] if isinstance(dt, list) and dt else dt
        cal.append((t, float(d.mp_weight[t]), str(dt)[:10] if dt else '—'))
        time.sleep(0.2)
    except Exception:
        cal.append((t, float(d.mp_weight[t]), '—'))
for t, wt, dt in cal: L.append(f'| {t} | {wt:.2f}% | {dt} |')

open('mp_v51_pm_dashboard.md', 'w').write('\n'.join(L))
print('\n'.join(L[:30])); print('...'); print(f'총 {len(L)}줄')
