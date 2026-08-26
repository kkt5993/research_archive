#!/usr/bin/env python3
"""AI 에이전트 20종목 — 비중 차트 (파이 2종 + 액티브 막대)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd, numpy as np

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

D = pd.read_csv('agent20_holdings.csv').set_index('ticker')
g = D.groupby('group').weight.sum().sort_values(ascending=False)

ORDER = ['DRAM·NAND', '스토리지', '소부장', '클라우드(대형)', '네오클라우드', 'AI 인프라', '우주·중립']
g = g.reindex([x for x in ORDER if x in g.index])
COL = ['#1f4e79', '#2e75b6', '#8faadc', '#c00000', '#e8743b', '#548235', '#a6a6a6']

fig = plt.figure(figsize=(13.5, 5.6))

# 1) 그룹별 파이
ax1 = fig.add_subplot(1, 3, 1)
wedges, _, at = ax1.pie(g.values, labels=None, autopct='%1.1f%%', startangle=90,
                        colors=COL[:len(g)], pctdistance=0.72,
                        wedgeprops=dict(width=0.55, edgecolor='white', linewidth=1.6),
                        textprops=dict(color='white', fontsize=9, weight='bold'))
ax1.set_title('테마별 비중', fontsize=12, weight='bold', pad=14)
ax1.legend(wedges, [f'{k}  {v:.1f}%' for k, v in g.items()],
           loc='center left', bbox_to_anchor=(-0.28, -0.06), fontsize=8.5, frameon=False)

# 2) 종목별 파이 (상위 10 + 기타)
top = D.weight.sort_values(ascending=False)
head, tail = top.head(10), top.tail(len(top) - 10)
vals = list(head.values) + [tail.sum()]
labs = list(head.index) + [f'기타 {len(tail)}종목']
ax2 = fig.add_subplot(1, 3, 2)
cmap = plt.cm.Blues(np.linspace(0.85, 0.30, len(vals)))
w2, _, _ = ax2.pie(vals, labels=labs, autopct='%1.1f%%', startangle=90, colors=cmap,
                   textprops=dict(fontsize=8), pctdistance=0.78,
                   wedgeprops=dict(edgecolor='white', linewidth=1.2))
ax2.set_title('종목별 비중 (상위 10 + 기타)', fontsize=12, weight='bold', pad=14)

# 3) 액티브 비중 막대
ax3 = fig.add_subplot(1, 3, 3)
# 미보유 종목의 UW도 액티브다 — CPU(INTC·AMD)와 TSLA는 0% 보유가 곧 최대 UW다.
U = pd.read_csv('sp500_universe.csv').set_index('ticker')
zero_uw = pd.Series({t: -float(U.bm_weight.get(t, 0)) for t in ['TSLA', 'AMD', 'INTC']})
act = pd.concat([D.active, zero_uw]).sort_values()
act = pd.concat([act.head(6), act.tail(8)])
colors = ['#c00000' if v < 0 else '#1f4e79' for v in act.values]
labels = [f'{t}*' if t in ('TSLA','AMD','INTC') else t for t in act.index]
ax3.barh(range(len(act)), act.values, color=colors, height=0.68)
ax3.set_yticks(range(len(act))); ax3.set_yticklabels(labels, fontsize=9)
ax3.axvline(0, color='#333', lw=0.9)
ax3.set_xlabel('BM(S&P500) 대비 액티브 비중 (%p)   * = 미보유', fontsize=8.5)
ax3.set_title('액티브 비중 상·하위', fontsize=12, weight='bold', pad=14)
for i, v in enumerate(act.values):
    ax3.text(v + (0.25 if v >= 0 else -0.25), i, f'{v:+.1f}', va='center',
             ha='left' if v >= 0 else 'right', fontsize=8)
ax3.spines[['top', 'right']].set_visible(False)
ax3.margins(x=0.18)

plt.tight_layout(w_pad=2.2)
plt.savefig('agent20_charts.png', dpi=200, bbox_inches='tight', facecolor='white')
print('agent20_charts.png 생성 · 테마 구성:', dict(g.round(1)))
