#!/usr/bin/env python3
"""levels 결측 보수 — 대량 수집 중 야후가 거부한 종목만 다시 받아 병합한다.

524종목을 한 번에 긁으면 일부가 429/타임아웃으로 조용히 비는데(v5.0 1차 수집에서
GOOGL·V·GE·UNP 등 대형주가 역사 배수 없음으로 빠졌다), 그 구멍은 재시도로만 메워진다.
결측 종목만 골라 느린 속도로 다시 받고, 성공한 것만 덮어쓴다.
실행: OUT_LEVELS=mp_v50_stock_levels.csv WEIGHTS=mp_v50_weights.csv python3 mp_levels_repair.py
"""
import os, math, time
import numpy as np, pandas as pd, yfinance as yf

LEV = os.environ.get('OUT_LEVELS', 'mp_v47_stock_levels.csv')
WEIGHTS = os.environ.get('WEIGHTS', 'mp_v47_weights.csv')
LAG_DAYS, SWING_WIN = 45, 20
PE_CAP, GROWTH_CAP = 0.50, 0.50

S = pd.read_csv(LEV).set_index('ticker')
W = pd.read_csv(WEIGHTS).set_index('ticker')
held = W[W.mp_weight > 0]

# 보수 대상은 **유니버스 기준**으로 잡는다. 일괄 다운로드에서 통째로 빠진 종목은
# levels 파일에 행 자체가 없어서(v5.0 1차: GOOGL·V·GE·UNP 등 28종목), 기존 행만
# 훑으면 영원히 못 찾는다.
univ = [t for t in W.index if W.mp_weight.get(t, 0) > 0 or W.bm_weight_approx.get(t, 0) > 0.3]
missing_row = [t for t in univ if t not in S.index]
incomplete = [t for t in univ if t in S.index
              and (S.loc[t, 'val_basis'] in ('none', None) or pd.isna(S.loc[t, 'val_basis'])
                   or pd.isna(S.loc[t, 'growth_1y']) or pd.isna(S.loc[t, 'target_upside']))]
need = missing_row + incomplete
print(f'보수 대상 {len(need)}종목 (행 없음 {len(missing_row)} · 결측 {len(incomplete)})')
print('행 없음:', missing_row[:30])

fixed = 0
for t in need:
    try:
        p = yf.download(t, period='5y', interval='1d', auto_adjust=True, progress=False)['Close']
        p = p.squeeze().dropna()
        if len(p) < 250: continue
        last = float(p.iloc[-1])
        tk = yf.Ticker(t); info = tk.info or {}
        upd = {}
        if t not in S.index:                       # 행 자체가 없으면 기본 레벨부터 만든다
            r_ = p.pct_change().dropna(); y = p.tail(252)
            H = y.rolling(SWING_WIN*2+1, center=True).max(); L_ = y.rolling(SWING_WIN*2+1, center=True).min()
            pk = y[(y == H) & (y > last)]; tr = y[(y == L_) & (y < last)]
            ma50 = float(p.rolling(50).mean().iloc[-1]); ma200 = float(p.rolling(200).mean().iloc[-1])
            res = float(pk.min()) if len(pk) else float(y.max())
            sup = float(tr.max()) if len(tr) else float(y.min())
            upd.update(price=last, vol_1y=float(r_.tail(252).std())*math.sqrt(252),
                       vol_3y=float(r_.tail(756).std())*math.sqrt(252),
                       ma50=ma50, ma200=ma200, px_vs_ma50=last/ma50-1, px_vs_ma200=last/ma200-1,
                       resistance=res, support=sup, upside_to_resist=res/last-1,
                       downside_to_support=sup/last-1, hi_52w=float(y.max()), lo_52w=float(y.min()),
                       val_basis='none')
        tpe, fpe = info.get('trailingPE'), info.get('forwardPE')
        try:
            ge = tk.growth_estimates
            if ge is not None and '+1y' in ge.index: upd['growth_1y'] = float(ge.loc['+1y', 'stockTrend'])
        except Exception: pass
        try:
            ap = tk.analyst_price_targets or {}
            if ap.get('median'): upd['target_upside'] = float(ap['median']) / last - 1
        except Exception: pass
        # forward P/E 역사 (보고통화 USD만)
        if (info.get('financialCurrency') or 'USD').upper() == 'USD' and fpe:
            a = tk.income_stmt
            row = next((x for x in a.index if str(x) == 'Diluted EPS'), None)
            if row is not None:
                v = a.loc[row].dropna().astype(float).sort_index()
                if len(v) >= 2:
                    eff = pd.Series(index=p.index, dtype=float); ends = list(v.index)
                    for n, (fy, val) in enumerate(v.items()):
                        fy = pd.Timestamp(fy)
                        st = pd.Timestamp(ends[n-1]) if n > 0 else fy - pd.Timedelta(days=370)
                        eff.loc[(eff.index > st) & (eff.index <= fy)] = float(val)
                    ser = (p / eff.where(eff > 0)).dropna(); ser = ser[(ser > 0) & (ser < 300)]
                    if len(ser) >= 120:
                        med = float(ser.median())
                        if float(fpe) / 6 <= med <= float(fpe) * 6:
                            upd.update(pe_hist_med=med, pe_now=float(fpe), val_basis='fwd_pe',
                                       pe_hist_p25=float(ser.quantile(.25)), pe_hist_p75=float(ser.quantile(.75)))
        if upd:
            for k, val in upd.items(): S.loc[t, k] = val
            fixed += 1
        time.sleep(1.2)          # 느리게 — 재시도는 속도보다 성공률이다
    except Exception as e:
        print(f'  {t} 실패: {type(e).__name__}')

# 파생 지표 재계산
S['growth'] = S.growth_1y.clip(-GROWTH_CAP, GROWTH_CAP)
rev_pe = S.pe_hist_med / S.pe_now - 1
rev_psr = S.ps_hist_med / S.ps_now - 1
S['pe_revert_full'] = rev_pe.fillna(rev_psr).clip(-PE_CAP, PE_CAP)
for tag, k in [('none', 0.0), ('half', 0.5), ('full', 1.0)]:
    S[f'exp_ret_{tag}'] = (1 + S.growth) * (1 + k * S.pe_revert_full) - 1
S.to_csv(LEV)
print(f'보수 완료 {fixed}/{len(need)} · val_basis 있음 {(S.val_basis!="none").sum()}/{len(S)}')
