#!/usr/bin/env python3
"""MP v4.7 종목별 실측 — 개별 변동성·역사적 P/E·이동평균·지지/저항.

기대수익을 시나리오 가정(E[r] 9.7%)이 아니라 **종목별 실측**에서 쌓아올린다.
  1. 역사적 P/E: 보고된 회계연도 EPS를 리포팅 래그 45일 뒤부터 적용한 일별 P/E 시계열.
     (그 시점에 실제로 알 수 있던 EPS만 쓴다 — 선견 편향 제거)
  2. 배수 회귀: 현재 P/E 대비 그 종목 자체의 역사적 중앙값까지의 거리.
  3. 성장: 실측 EPS 성장(윈저 ±100%).
  4. 기술: MA50/MA200, 52주 고저, 최근 1년 스윙 고/저(로컬 극값)로 저항·지지.
실행: ssh mini-lan 'cd ~/research_archive/20_미국주식/mp_quant && python3 mp_stock_levels.py'
"""
import math, sys, time
import numpy as np, pandas as pd, yfinance as yf

LAG_DAYS   = 45      # 회계연도 종료 후 실적 발표까지 래그
PE_CAP     = 0.50    # 배수 회귀 기여 상한 ±50% (한 종목이 포트 기대수익을 지배하지 않게)
GROWTH_CAP = 0.50    # 성장 기여 상한 ±50% — MU trail/fwd=2.5배(사이클 회복) 같은 값이 포트를 지배한다
SWING_WIN  = 20      # 로컬 극값 판정 창(거래일)

W = pd.read_csv('mp_v47_weights.csv')
UNIV = list(dict.fromkeys(list(W[W.mp_weight > 0].ticker) + list(W[W.bm_weight_approx > 0].ticker)))

px = yf.download(UNIV, period='5y', interval='1d', auto_adjust=True, progress=False)['Close']

rows = []
for t in UNIV:
    if t not in px.columns: continue
    p = px[t].dropna()
    if len(p) < 250: continue
    last = float(p.iloc[-1])
    r = p.pct_change().dropna()

    # --- 개별 변동성 (1y / 3y) ---
    vol1 = float(r.tail(252).std()) * math.sqrt(252)
    vol3 = float(r.tail(756).std()) * math.sqrt(252)

    # --- 역사적 P/E (리포팅 래그 반영 + 현재 trailingPE로 앵커링) ---
    # 앵커링이 없으면 액면분할(NFLX 10:1 → 31.7 vs 실제 25.2)과 최신 분기 미반영
    # (MU 117 vs 실제 20.2)이 시계열을 통째로 깨뜨린다. 우리가 필요한 건 절대 배수가
    # 아니라 "현재 배수가 자기 역사 대비 어디인가"이므로 끝점을 실제값에 맞춰 스케일한다.
    pe_hist_med = pe_hist_p25 = pe_hist_p75 = pe_now = np.nan
    fwd_growth = np.nan
    try:
        tk = yf.Ticker(t); info = tk.info or {}
        tpe, fpe = info.get('trailingPE'), info.get('forwardPE')
        if tpe and fpe and fpe > 0:
            fwd_growth = tpe / fpe - 1        # 컨센서스 기반 12M EPS 성장 — 시장 실측치
        a = tk.income_stmt
        eps_row = next((x for x in a.index if str(x) == 'Diluted EPS'), None)
        if eps_row is not None:
            eps = a.loc[eps_row].dropna().astype(float)
            eps = eps[eps > 0].sort_index()          # 적자 연도는 P/E 무의미 — 제외
            if len(eps) >= 2:
                eff = pd.Series(index=p.index, dtype=float)
                for fy_end, v in eps.items():
                    eff.loc[eff.index >= pd.Timestamp(fy_end) + pd.Timedelta(days=LAG_DAYS)] = v
                pe_series = (p / eff).dropna()
                pe_series = pe_series[(pe_series > 0) & (pe_series < 300)]
                if len(pe_series) >= 120:
                    k = (tpe / float(pe_series.iloc[-1])) if tpe else 1.0
                    if not (0.05 < k < 20): k = 1.0      # 앵커가 비정상이면 스케일하지 않는다
                    pe_series = pe_series * k
                    pe_hist_med = float(pe_series.median())
                    pe_hist_p25 = float(pe_series.quantile(0.25))
                    pe_hist_p75 = float(pe_series.quantile(0.75))
                    pe_now = float(tpe) if tpe else float(pe_series.iloc[-1])
    except Exception:
        pass

    # --- 이동평균 ---
    ma50  = float(p.rolling(50).mean().iloc[-1])
    ma200 = float(p.rolling(200).mean().iloc[-1]) if len(p) >= 200 else np.nan

    # --- 지지/저항: 최근 1년 로컬 극값 + 52주 고저 ---
    y = p.tail(252)
    hi = y.rolling(SWING_WIN * 2 + 1, center=True).max()
    lo = y.rolling(SWING_WIN * 2 + 1, center=True).min()
    peaks   = y[(y == hi) & (y > last)]     # 현재가 위의 스윙 고점 = 저항
    troughs = y[(y == lo) & (y < last)]     # 현재가 아래 스윙 저점 = 지지
    resist  = float(peaks.min())   if len(peaks)   else float(y.max())
    support = float(troughs.max()) if len(troughs) else float(y.min())

    rows.append(dict(ticker=t, price=last, vol_1y=vol1, vol_3y=vol3,
                     pe_now=pe_now, pe_hist_med=pe_hist_med,
                     pe_hist_p25=pe_hist_p25, pe_hist_p75=pe_hist_p75,
                     ma50=ma50, ma200=ma200,
                     px_vs_ma50=last/ma50 - 1, px_vs_ma200=last/ma200 - 1 if ma200 == ma200 else np.nan,
                     resistance=resist, support=support,
                     upside_to_resist=resist/last - 1, downside_to_support=support/last - 1,
                     hi_52w=float(y.max()), lo_52w=float(y.min()),
                     fwd_growth=fwd_growth))
    time.sleep(0.2)

S = pd.DataFrame(rows).set_index('ticker')

# --- 기대수익: 성장 × 배수 회귀 (둘 다 실측) ---
# 성장은 분기 YoY(earningsGrowth)가 아니라 trailingPE/forwardPE−1 — 컨센서스가 값을 매긴
# 12개월 EPS 성장이다. 분기 YoY는 기저효과로 CIEN +2383% 같은 값이 나와 연간에 못 쓴다.
S['growth'] = S.fwd_growth.clip(-GROWTH_CAP, GROWTH_CAP)
S['pe_revert_full'] = (S.pe_hist_med / S.pe_now - 1).clip(-PE_CAP, PE_CAP)
# 배수가 1년 안에 역사적 중앙값까지 전부 돌아간다는 보장은 없다. 회귀 속도별로 셋 다 낸다.
for tag, k in [('none', 0.0), ('half', 0.5), ('full', 1.0)]:
    S[f'exp_ret_{tag}'] = (1 + S.growth) * (1 + k * S.pe_revert_full) - 1
S.to_csv('mp_v47_stock_levels.csv')
print(f'levels: {len(S)} tickers · P/E 이력 {S.pe_hist_med.notna().sum()} '
      f'· 성장 {S.growth.notna().sum()} · exp_ret {S.exp_ret_half.notna().sum()}')
