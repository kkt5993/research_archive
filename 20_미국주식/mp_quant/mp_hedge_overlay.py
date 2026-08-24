#!/usr/bin/env python3
"""MP v4.7 기대수익·샤프·헤지 오버레이 — 전부 종목별 실측에서 쌓아올린다.

시나리오 확률·수익 가정(E[r] 9.7%)을 쓰지 않는다. 대신:
  기대수익  = Σ w_i · [(1+성장_i)(1+k·배수회귀_i) − 1]
    성장_i     = trailingPE/forwardPE − 1 (컨센서스가 값 매긴 12M EPS 성장)
    배수회귀_i = 자기 역사적 P/E 중앙값/현재 P/E − 1 (분할조정·TTM 보강 시계열)
    k          = 배수 회귀 속도 0 / 0.5 / 1.0
  변동성    = 실측 일별 수익률(2y) — 종목별 변동성·상관이 그대로 들어간다
  BM        = 같은 방식으로 BM 추적분(91.2%)에 적용 → 알파도 실측
기술적 레벨(MA·지지·저항)은 기대수익 대신 **경로 리스크** 점검에 쓴다.
실행: ssh mini-lan 'cd ~/research_archive/20_미국주식/mp_quant && python3 mp_hedge_overlay.py'
"""
import math
import numpy as np, pandas as pd, yfinance as yf

RF   = 0.0372   # 13주 T-bill 실측
COST = 0.004    # 헤지 실행비용 연 0.4%p (선물 롤·스프레드), 헤지비율에 비례

W = pd.read_csv('mp_v47_weights.csv')
S = pd.read_csv('mp_v47_stock_levels.csv').set_index('ticker')
held = W[W.mp_weight > 0]

px = yf.download(list(held.ticker) + ['QQQ'], period='2y', interval='1d',
                 auto_adjust=True, progress=False)['Close']
rets = px.pct_change().dropna(how='all')
avail = [t for t in held.ticker if t in rets.columns and rets[t].notna().sum() > 250]
w = held.set_index('ticker').loc[avail, 'mp_weight']; w = w / w.sum()
both = pd.concat([(rets[avail] * w).sum(axis=1), rets['QQQ']], axis=1).dropna()
both.columns = ['p', 'b']

def _agg(weights, e):
    ok = e.notna() & np.isfinite(e)
    if not ok.any(): return np.nan, 0.0
    ww = weights[ok] / weights[ok].sum()
    return float((ww * e[ok]).sum()), float(weights[ok].sum() / weights.sum())

def exp_ret(weights, k):
    """경로 A — 컨센 차년도 EPS 성장 × 자기 역사 P/E 회귀(속도 k)."""
    d = S.reindex(weights.index)
    return _agg(weights, (1 + d.growth) * (1 + k * d.pe_revert_full) - 1)

def exp_ret_target(weights):
    """경로 B — 컨센 목표주가(중앙값) 대비 상승여력. 애널 낙관 편향이 그대로 들어간다."""
    return _agg(weights, S.reindex(weights.index).target_upside)

bmw = W[W.bm_weight_approx > 0].set_index('ticker').bm_weight_approx
mpw = held.set_index('ticker').mp_weight

def mdd(s):
    c = (1 + s).cumprod(); return float((c / c.cummax() - 1).min())

L = ['# MP v4.7 기대수익·샤프·헤지 오버레이 — 종목별 실측 기반\n',
     f'rf {RF:.2%}(13주 T-bill 실측) · 헤지비용 {COST:.1%}/년 비례 · 가격 커버리지 {len(avail)}/{len(held)}',
     '기대수익에 시나리오 확률·수익 가정을 일절 쓰지 않는다. 경로 A는 종목별 컨센 차년도\n'
     'EPS 성장 × 자기 역사 P/E 회귀, 경로 B는 컨센 목표주가 중앙값 대비 상승여력이다.\n',
     '## 1. 기대수익 — 두 독립 경로 (MP vs BM)\n',
     '| 회귀 속도 k | MP E[r] | BM E[r] | **알파** | MP 커버리지 | BM 커버리지 |',
     '|---|---:|---:|---:|---:|---:|']
ER = {}
for tag, k in [('0 (배수 그대로)', 0.0), ('0.5 (절반 회귀)', 0.5), ('1.0 (전부 회귀)', 1.0)]:
    m, mc = exp_ret(mpw, k); b, bc = exp_ret(bmw, k)
    ER[k] = (m, b)
    L.append(f'| A: 성장×회귀 k={tag} | {m:.1%} | {b:.1%} | **{m-b:+.1%}** | {mc:.0%} | {bc:.0%} |')
# 역사 배수 대비 현재 위치 — MP와 BM 중 누가 자기 역사 대비 싼가
def hist_pos(weights):
    d = S.reindex(weights.index)
    return _agg(weights, d.pe_revert_full)
hm_, hmc = hist_pos(mpw); hb_, hbc = hist_pos(bmw)

tm, tmc = exp_ret_target(mpw); tb, tbc = exp_ret_target(bmw)
ER['target'] = (tm, tb)
L.append(f'| **B: 컨센 목표주가** | {tm:.1%} | {tb:.1%} | **{tm-tb:+.1%}** | {tmc:.0%} | {tbc:.0%} |')
L.append(f'\n**자기 역사 대비 위치(forward 배수 회귀 여력)**: MP {hm_:+.1%} vs BM {hb_:+.1%} '
         f'(커버리지 MP {hmc:.0%}·BM {hbc:.0%}) — 양(+)이면 현재 배수가 자기 역사 중앙값보다 싸다.')
L.append('\n두 경로가 크게 어긋나면 어느 쪽도 단독으로 쓰지 않는다 — 알파의 부호와 크기만 본다.')

L += ['\n## 2. 헤지 오버레이 — 넷 밴드별 (σ·MDD·VaR는 실측 시계열, E[r]은 목표주가 경로)\n',
      '| 넷 | QQQ 숏 | E[r] | 연율 σ | 베타 | TE | **기대 샤프** | MDD(2y) | VaR95 |',
      '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
E_MP, E_BM = ER['target']   # 헤지 판정 기준선은 목표주가 경로(배수 회귀 가정이 없다)
band = []
for net in [1.00, 0.80, 0.70, 0.60, 0.50]:
    h = 1 - net
    r = both.p - h * both.b
    vol = float(r.std()) * math.sqrt(252)
    er = E_MP - h * (E_BM - RF) - h * COST
    sh = (er - RF) / vol
    band.append((net, h, er, vol, sh))
    L.append(f'| {net:.0%} | {h:.0%} | {er:.1%} | {vol:.1%} | '
             f'{float(r.cov(both.b)/both.b.var()):.2f} | {float((r-both.b).std())*math.sqrt(252):.1%} | '
             f'**{sh:.2f}** | {mdd(r):.1%} | {float(r.quantile(0.05)):.2%} |')
best = max(band, key=lambda x: x[4])
te_full = float((both.p - both.b).std()) * math.sqrt(252)
bm_vol  = float(both.b.std()) * math.sqrt(252)
ir      = (E_MP - E_BM) / te_full
bm_sh   = (E_BM - RF) / bm_vol
L.append(f'\n**최적 넷 {best[0]:.0%}** (샤프 {best[4]:.2f}) — 넷 100% 대비 {best[4]-band[0][4]:+.2f}.')
L += ['\n### 판정 기준 — 헤지가 샤프를 개선하는 조건은 IR > BM 샤프\n',
      '베타를 깎는 것은 BM 위험프리미엄을 버리고 알파 비중을 늘리는 거래다. 그래서 기준은',
      '알파의 절대크기가 아니라 **IR(알파/TE)이 BM 샤프보다 큰가**이다.\n',
      f'- 실측 알파 {E_MP-E_BM:+.1%} · TE {te_full:.1%} → **IR {ir:.2f}**',
      f'- BM 샤프 = ({E_BM:.1%} − {RF:.2%}) / {bm_vol:.1%} = **{bm_sh:.2f}**',
      f'- **{ir:.2f} {">" if ir > bm_sh else "<"} {bm_sh:.2f}** → 헤지는 '
      f'{"샤프를 개선한다" if ir > bm_sh else "샤프를 개선하지 못한다"}.',
      '',
      f'헤지가 정당화되려면 알파가 최소 **{bm_sh * te_full:.1%}**(= BM샤프 × TE) 필요하다.',
      f'현재 {E_MP-E_BM:+.1%}. 알파를 키우거나 TE를 줄이지 않는 한 넷을 내리는 건 샤프 손해다.',
      '',
      '**단, 샤프가 헤지의 유일한 목적은 아니다.**']
n60 = next(x for x in band if abs(x[0] - 0.60) < 1e-9)
r60 = both.p - n60[1] * both.b
L += [f'넷 60%는 MDD를 {mdd(both.p):.1%}→{mdd(r60):.1%}, VaR95를 '
      f'{float(both.p.quantile(0.05)):.2%}→{float(r60.quantile(0.05)):.2%}로 줄인다. '
      f'드로다운 한도가 계약으로 걸린 자금이라면 샤프 {n60[4]-band[0][4]:+.2f}를 내고 '
      f'MDD {abs(mdd(r60)-mdd(both.p)):.1%}p를 사는 거래가 합리적일 수 있다 — ',
      '그건 최적화가 아니라 **제약 충족**이며, 문서에도 그렇게 적어야 한다.']

L += ['\n## 3. 민감도 — 기대수익 경로가 결론을 바꾸는가\n',
      '| 경로 | MP 알파 | 넷100% 샤프 | 넷80% | 넷70% | 넷60% | 최적 |', '|---|---:|---:|---:|---:|---:|---|']
for k in [0.0, 0.5, 1.0, 'target']:
    m, b = ER[k]; row = []
    for net in [1.00, 0.80, 0.70, 0.60]:
        h = 1 - net
        r = both.p - h * both.b
        vol = float(r.std()) * math.sqrt(252)
        row.append(((m - h * (b - RF) - h * COST) - RF) / vol)
    opt = ['100%', '80%', '70%', '60%'][int(np.argmax(row))]
    lbl = '**B: 목표주가**' if k == 'target' else f'A: k={k}'
    L.append(f'| {lbl} | {m-b:+.1%} | {row[0]:.2f} | {row[1]:.2f} | {row[2]:.2f} | {row[3]:.2f} | **{opt}** |')

# --- 4. 기술적 레벨: 기대수익이 아니라 경로 리스크로 쓴다 ---
d = S.reindex(mpw.index)
mw = mpw / mpw.sum()
def wsum(mask): return float(mpw[mask.reindex(mpw.index).fillna(False)].sum())
up, _   = _agg(mpw, d.upside_to_resist)
down, _ = _agg(mpw, d.downside_to_support)
v1, _   = _agg(mpw, d.vol_1y)
v3, _   = _agg(mpw, d.vol_3y)
L += ['\n## 4. 기술적 레벨 — 경로 리스크 (기대수익에는 넣지 않는다)\n',
      '이동평균·지지·저항은 12개월 기대수익의 근거가 못 된다(추세추종은 별도 전략이다).',
      '여기서는 **지금 진입할 때의 경로 위험**을 보는 데만 쓴다.\n',
      f'- 가중 상승여력(현재가→최근접 저항): **{up:+.1%}**',
      f'- 가중 하락여력(현재가→최근접 지지): **{down:+.1%}**',
      f'- 상방/하방 비율: **{abs(up/down):.2f}** ' + ('(하방이 더 가깝다)' if abs(up) < abs(down) else '(상방이 더 가깝다)'),
      f'- MA200 위 비중: **{wsum(d.px_vs_ma200 > 0):.1f}%** · MA50 위 비중: {wsum(d.px_vs_ma50 > 0):.1f}%',
      f'- 52주 고점 −10% 이내 비중: {wsum(d.price / d.hi_52w > 0.9):.1f}%',
      f'- 가중 개별 변동성: 1y {v1:.1%} · 3y {v3:.1%} (포트 실현 σ 27.3%와의 차이가 분산효과)',
      '',
      '해석: 개별 변동성 가중평균이 포트 σ보다 훨씬 크면 상관이 낮다는 뜻이고, 가까우면',
      '한 방향으로 같이 움직인다는 뜻이다 — 후자면 헤지가 아니라 종목수를 늘려도 소용없다.']

open('mp_v47_hedge_overlay.md', 'w').write('\n'.join(L))
print('\n'.join(L))
