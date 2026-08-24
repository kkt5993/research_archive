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
import os
import numpy as np, pandas as pd

# 비중 파일은 환경변수로 갈아끼운다: WEIGHTS=mp_v48_weights.csv python3 ...
WEIGHTS = os.environ.get('WEIGHTS', 'mp_v47_weights.csv')
import yfinance as yf

LAG_DAYS   = 45      # 회계연도 종료 후 실적 발표까지 래그
PE_CAP     = 0.50    # 배수 회귀 기여 상한 ±50% (한 종목이 포트 기대수익을 지배하지 않게)
GROWTH_CAP = 0.50    # 성장 기여 상한 ±50% — MU trail/fwd=2.5배(사이클 회복) 같은 값이 포트를 지배한다
SWING_WIN  = 20      # 로컬 극값 판정 창(거래일)

W = pd.read_csv(WEIGHTS)
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

    # --- 역사적 밸류에이션: FORWARD 기준 ---
    # trailing이 아니라 forward P/E로 본다. 시장이 값을 매기는 건 지나간 이익이 아니다.
    # 과거 forward P/E = 그 시점 가격 ÷ **그 회계연도에 실제로 실현된 EPS**.
    #   → 리포팅 래그를 두지 않고 FY 구간에 그 FY EPS를 '선행' 적용한다.
    #   → 그 시점 시장이 보던 추정치가 아니라 실현치이므로 완벽예측 편향이 있다.
    #     현재값은 컨센 forwardPE(대개 낙관)라 비교 시 현재가 싸 보이는 방향으로 치우친다.
    #     이 편향은 제거할 수 없어 명시만 한다 — 결론은 MP−BM 상대비교로만 쓴다.
    # 적자·무이익 종목은 P/E가 성립하지 않아 **역사적 PSR**로 같은 작업을 반복한다.
    pe_hist_med = pe_hist_p25 = pe_hist_p75 = pe_now = np.nan
    ps_hist_med = ps_now = np.nan
    val_basis = 'none'
    fwd_growth = growth_1y = target_upside = n_analysts = np.nan
    tgt_med = tgt_mean = None
    try:
        tk = yf.Ticker(t); info = tk.info or {}
        tpe, fpe = info.get('trailingPE'), info.get('forwardPE')
        if tpe and fpe and fpe > 0:
            fwd_growth = tpe / fpe - 1        # 참고용 — 12M 성장으로는 못 쓴다
        try:
            ge = tk.growth_estimates
            if ge is not None and '+1y' in ge.index:
                growth_1y = float(ge.loc['+1y', 'stockTrend'])
        except Exception: pass
        try:
            ap = tk.analyst_price_targets or {}
            tgt_med, tgt_mean = ap.get('median'), ap.get('mean')
            if tgt_med: target_upside = float(tgt_med) / last - 1
        except Exception: pass
        try:
            ee = tk.earnings_estimate
            if ee is not None and '+1y' in ee.index:
                n_analysts = float(ee.loc['+1y', 'numberOfAnalysts'])
        except Exception: pass

        # 분할 조정은 하지 않는다. yfinance income_stmt의 주당 항목은 **이미 현재 주식수
        # 기준으로 재작성**돼 있다(NFLX 2022 EPS 1.00 — 분할 전 실제는 9.95, 10:1 반영됨).
        # 여기에 splits로 또 나누면 이중 조정이라 P/E가 10~25배로 튀어 필터에 탈락한다.
        # NFLX·BKNG·AVGO가 그렇게 밸류 이력 없음으로 빠졌다.
        def adj(v, when):
            return v

        # 보고통화가 USD가 아니면 역사 배수를 만들 수 없다 — 가격은 USD ADR인데 재무는
        # 현지통화다(TSM: TWD). info의 forwardPE는 환산돼 있어 현재값만 유효하다.
        fin_cur = (info.get('financialCurrency') or 'USD').upper()
        if fin_cur != 'USD':
            raise ValueError(f'non-USD financials: {fin_cur}')

        def fwd_series(row_name, per_share=True):
            """FY 값을 그 FY 구간에 선행 적용한 주당 시계열."""
            a = tk.income_stmt
            row = next((x for x in a.index if str(x) == row_name), None)
            if row is None: return None
            v = a.loc[row].dropna().astype(float).sort_index()
            if len(v) < 2: return None
            eff = pd.Series(index=p.index, dtype=float)
            ends = list(v.index)
            for n, (fy_end, val) in enumerate(v.items()):
                fy_end = pd.Timestamp(fy_end)
                start = pd.Timestamp(ends[n-1]) if n > 0 else fy_end - pd.Timedelta(days=370)
                m = (eff.index > start) & (eff.index <= fy_end)
                eff.loc[m] = adj(val, fy_end)
            # 최신 FY 이후 구간(=현재 진행 회계연도)은 컨센 forward EPS로 채운다
            return eff

        # 1순위: forward P/E
        eps_eff = fwd_series('Diluted EPS')
        if eps_eff is not None:
            pos = eps_eff.where(eps_eff > 0)
            ser = (p / pos).dropna()
            ser = ser[(ser > 0) & (ser < 300)]
            if len(ser) >= 120 and fpe:
                med = float(ser.median())
                # 보고통화 불일치 방어(TSM: TWD EPS vs USD ADR)
                if float(fpe) / 6 <= med <= float(fpe) * 6:
                    pe_hist_med, pe_now, val_basis = med, float(fpe), 'fwd_pe'
                    pe_hist_p25 = float(ser.quantile(0.25)); pe_hist_p75 = float(ser.quantile(0.75))

        # 2순위: 적자·무이익이거나 P/E 실패 시 역사적 PSR (매출은 항상 양수)
        if val_basis == 'none':
            shares = info.get('sharesOutstanding')
            rev_eff = fwd_series('Total Revenue')
            psr_now = info.get('priceToSalesTrailing12Months')
            if rev_eff is not None and shares and psr_now:
                rps = rev_eff / float(shares)          # 주당매출 (분할조정은 adj가 처리)
                ser = (p / rps).dropna()
                ser = ser[(ser > 0) & (ser < 100)]
                if len(ser) >= 120:
                    med = float(ser.median())
                    if float(psr_now) / 6 <= med <= float(psr_now) * 6:
                        ps_hist_med, ps_now, val_basis = med, float(psr_now), 'psr'
                        pe_hist_p25 = float(ser.quantile(0.25)); pe_hist_p75 = float(ser.quantile(0.75))
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
                     ps_hist_med=ps_hist_med, ps_now=ps_now, val_basis=val_basis,
                     fwd_growth=fwd_growth, growth_1y=growth_1y,
                     target_median=tgt_med, target_mean=tgt_mean,
                     target_upside=target_upside, n_analysts=n_analysts))
    time.sleep(0.2)

S = pd.DataFrame(rows).set_index('ticker')

# --- 기대수익: 성장 × 배수 회귀 (둘 다 실측) ---
# 성장은 분기 YoY(earningsGrowth)가 아니라 trailingPE/forwardPE−1 — 컨센서스가 값을 매긴
# 12개월 EPS 성장이다. 분기 YoY는 기저효과로 CIEN +2383% 같은 값이 나와 연간에 못 쓴다.
S['growth'] = S.growth_1y.clip(-GROWTH_CAP, GROWTH_CAP)   # 컨센 차년도 EPS 성장
# 배수 회귀 — forward P/E가 있으면 그것으로, 적자 종목은 PSR로. 둘 다 없으면 결측.
rev_pe  = S.pe_hist_med / S.pe_now - 1
rev_psr = S.ps_hist_med / S.ps_now - 1
S['pe_revert_full'] = rev_pe.fillna(rev_psr).clip(-PE_CAP, PE_CAP)
# 배수가 1년 안에 역사적 중앙값까지 전부 돌아간다는 보장은 없다. 회귀 속도별로 셋 다 낸다.
for tag, k in [('none', 0.0), ('half', 0.5), ('full', 1.0)]:
    S[f'exp_ret_{tag}'] = (1 + S.growth) * (1 + k * S.pe_revert_full) - 1
S.to_csv(os.environ.get('OUT_LEVELS','mp_v47_stock_levels.csv'))
print(f'levels: {len(S)} tickers · fwd P/E 이력 {(S.val_basis=="fwd_pe").sum()} '
      f'· PSR 이력 {(S.val_basis=="psr").sum()} · 밸류 이력 없음 {(S.val_basis=="none").sum()} '
      f'· 컨센성장 {S.growth_1y.notna().sum()} · 목표주가 {S.target_upside.notna().sum()} '
      f'· exp_ret {S.exp_ret_half.notna().sum()}')
