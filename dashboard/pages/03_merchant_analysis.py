import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, ENGAGE_PALETTE, AGE_PALETTE, AGE_ORDER
from demo_data import top_merchants, MONTH_LABELS
from charts import bar_chart, donut_chart, trend_line, grouped_bar, scatter_plot, fmt_dollar, fmt_count

st.header("Merchant Analysis")
st.caption("14 analyses | Top merchant aggregation, spend concentration, trends")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Unique Merchants", "142,800")
c2.metric("Top 10 Concentration", "62.4%")
c3.metric("Avg Merchants/Acct", "18.3")
c4.metric("New Merchants", "2,840", "+12%")
st.divider()

n_show = st.slider("Merchants to display", 5, 20, 10)
display = top_merchants.head(n_show)

# Top 20 bar (03)
st.subheader(f"Top {n_show} Merchants by Spend")
st.plotly_chart(bar_chart(
    display['merchant'][::-1].tolist(), (display['total_spend'][::-1] * 1_000_000).tolist(),
    text_fmt=fmt_dollar, horizontal=True, height=max(350, n_show * 38),
), use_container_width=True, theme=None)

# Donut (04)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(donut_chart(
        display['merchant'], display['total_spend'],
        title='Spend Share by Merchant',
    ), use_container_width=True, theme=None)

# Concentration (05)
with col2:
    _cum = np.cumsum(display['total_spend']) / top_merchants['total_spend'].sum() * 100
    st.plotly_chart(trend_line(
        [f'Top {i+1}' for i in range(len(display))], _cum.tolist(),
        title='Cumulative Spend Concentration', y_title='% of Total',
        color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)

# Trend (06)
st.subheader("Top 5 Merchant Monthly Trends")
fig = go.Figure()
colors = [GEN_COLORS['primary'], GEN_COLORS['accent'], GEN_COLORS['success'],
          GEN_COLORS['warning'], GEN_COLORS['info']]
for i, merchant in enumerate(display['merchant'].head(5)):
    _trend = np.random.normal(display.iloc[i]['total_spend'], display.iloc[i]['total_spend'] * 0.08, len(MONTH_LABELS))
    fig.add_trace(go.Scatter(x=MONTH_LABELS, y=_trend, mode='lines', name=merchant,
                             line=dict(color=colors[i], width=2)))
fig.update_layout(height=380, yaxis=dict(gridcolor='#E9ECEF', title='Spend ($M)'),
                  margin=dict(l=50, r=20, t=20, b=40))
st.plotly_chart(fig, use_container_width=True, theme=None)

# Growth (07)
col1, col2 = st.columns(2)
with col1:
    _sorted = display.sort_values('growth_pct', ascending=True)
    _colors = [GEN_COLORS['success'] if g > 0 else GEN_COLORS['accent'] for g in _sorted['growth_pct']]
    st.plotly_chart(bar_chart(
        _sorted['merchant'].tolist(), _sorted['growth_pct'].tolist(),
        title='YoY Growth Rate', text_fmt=lambda x: f'{x:+.0f}%',
        color=_colors, horizontal=True, height=max(350, n_show * 38),
    ), use_container_width=True, theme=None)

# Volatility (08)
with col2:
    st.plotly_chart(bar_chart(
        display['merchant'].tolist(), display['volatility'].tolist(),
        title='Spend Volatility (CoV)', text_fmt=lambda x: f'{x:.2f}',
        color=GEN_COLORS['warning'],
    ), use_container_width=True, theme=None)

# Lifecycle (09)
st.subheader("Merchant Lifecycle Stage")
_stages = ['Emerging', 'Growing', 'Mature', 'Declining']
_stage_counts = [2840, 18200, 98400, 23360]
st.plotly_chart(bar_chart(_stages, _stage_counts, text_fmt=fmt_count,
                          color=[GEN_COLORS['accent'], GEN_COLORS['success'],
                                 GEN_COLORS['info'], GEN_COLORS['muted']]),
                use_container_width=True, theme=None)

# By biz/personal (10)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        display['merchant'].head(5).tolist(),
        {'Business': np.random.uniform(0.5, 3, 5).round(1).tolist(),
         'Personal': np.random.uniform(2, 12, 5).round(1).tolist()},
        title='Top 5: Business vs Personal Spend ($M)',
    ), use_container_width=True, theme=None)

# By age (11)
with col2:
    st.plotly_chart(grouped_bar(
        ['18-35', '36-55', '56+'],
        {'Amazon': [5.2, 8.1, 5.2], 'Walmart': [2.8, 5.4, 4.1], 'Target': [2.1, 3.8, 2.8]},
        title='Top 3 Merchants by Age Group ($M)',
    ), use_container_width=True, theme=None)

# By engagement (12)
st.subheader("Merchant Penetration by Engagement Tier")
_pen_data = {t: np.random.uniform(20, 80, 5).round(0).tolist() for t in ['Power', 'Heavy', 'Moderate']}
st.plotly_chart(grouped_bar(
    display['merchant'].head(5).tolist(), _pen_data,
    title='% of Tier Using Merchant',
), use_container_width=True, theme=None)

# New entrants (13)
st.subheader("New Merchant Entrants (Last 3 Months)")
import pandas as pd
st.dataframe(pd.DataFrame({
    'Merchant': ['DoorDash', 'Instacart', 'Temu', 'Shein', 'Apple Pay Cash'],
    'First Seen': ['Nov25', 'Oct25', 'Dec25', 'Nov25', 'Oct25'],
    'Accounts': [2400, 1800, 3200, 1500, 4100],
    'Avg Txn': ['$28', '$62', '$35', '$22', '$45'],
    'Growth Trend': ['Rapid', 'Rapid', 'Explosive', 'Moderate', 'Steady'],
}), use_container_width=True, hide_index=True)

# Action summary (14)
st.divider()
st.subheader("Key Findings & Actions")
from charts import action_summary
action_summary([
    {'category': 'Concentration', 'finding': 'Top 10 merchants = 62.4% of spend -- moderate concentration risk', 'priority': 'Medium'},
    {'category': 'Growth', 'finding': 'DoorDash/Instacart growing 35-42% -- digital delivery accelerating', 'priority': 'Low'},
    {'category': 'Emerging', 'finding': 'Temu penetration exploding (3,200 accounts in 2 months)', 'priority': 'Medium'},
    {'category': 'Decline', 'finding': 'Gas station spend declining 3-5% -- EV/remote work impact', 'priority': 'Low'},
], st)
