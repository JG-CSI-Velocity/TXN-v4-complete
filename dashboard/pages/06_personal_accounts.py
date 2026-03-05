import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import personal_top_merchants, MONTH_LABELS
from charts import bar_chart, donut_chart, trend_line, grouped_bar, fmt_dollar, fmt_count, action_summary
import plotly.graph_objects as go

st.header("Personal Account Analysis")
st.caption("14 analyses | Personal merchant patterns, spend concentration, trends")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Personal Accounts", "28,385", "85.5%")
c2.metric("Personal Spend", "$350M", "70.3%")
c3.metric("Avg Spend/Acct", "$950/mo")
c4.metric("Avg Txn Count", "32/mo")
st.divider()

st.subheader("Top 10 Personal Merchants")
st.plotly_chart(bar_chart(
    personal_top_merchants['merchant'][::-1].tolist(),
    (personal_top_merchants['total_spend'][::-1] * 1_000_000).tolist(),
    text_fmt=fmt_dollar, horizontal=True, height=400,
), use_container_width=True, theme=None)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(donut_chart(personal_top_merchants['merchant'], personal_top_merchants['total_spend'],
                                title='Personal Merchant Spend Share'), use_container_width=True, theme=None)
with col2:
    _cum = np.cumsum(personal_top_merchants['total_spend']) / personal_top_merchants['total_spend'].sum() * 100
    st.plotly_chart(trend_line(
        [f'Top {i+1}' for i in range(len(personal_top_merchants))], _cum.tolist(),
        title='Concentration Curve', y_title='% of Personal Spend',
    ), use_container_width=True, theme=None)

col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    for m in personal_top_merchants['merchant'].head(3):
        fig.add_trace(go.Scatter(x=MONTH_LABELS,
                                 y=np.random.normal(100, 8, len(MONTH_LABELS)),
                                 mode='lines', name=m))
    fig.update_layout(title='Top 3 Trends', height=380,
                      yaxis=dict(gridcolor='#E9ECEF'), margin=dict(l=50, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True, theme=None)
with col2:
    _growth = [12, 5, 8, -3, 18, 2, 1, 15, 22, -5]
    _colors = [GEN_COLORS['success'] if g > 0 else GEN_COLORS['accent'] for g in _growth]
    st.plotly_chart(bar_chart(
        personal_top_merchants['merchant'].tolist(), _growth,
        title='YoY Growth Rate', text_fmt=lambda x: f'{x:+.0f}%', color=_colors,
    ), use_container_width=True, theme=None)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        personal_top_merchants['merchant'].tolist(),
        np.random.uniform(0.03, 0.2, len(personal_top_merchants)).round(2).tolist(),
        title='Spend Volatility', text_fmt=lambda x: f'{x:.2f}', color=GEN_COLORS['warning'],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['Avg Spend', 'Avg Txns', 'Avg Merchants'],
        {'Personal': [950, 32, 16], 'Portfolio Avg': [950, 32, 18]},
        title='Personal vs Portfolio Average',
    ), use_container_width=True, theme=None)

st.plotly_chart(grouped_bar(
    ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
    {'Amazon': [4.2, 5.8, 3.2, 2.8, 1.8, 0.8],
     'Walmart': [2.1, 3.2, 3.8, 2.4, 1.8, 1.2],
     'Target': [1.8, 2.4, 2.8, 1.6, 0.8, 0.4]},
    title='Top 3 Merchants by Age Band ($M)',
), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Amazon', 'finding': 'Amazon = 14.2M personal spend, 22K accounts -- dominant channel', 'priority': 'Low'},
    {'category': 'Starbucks', 'finding': 'Starbucks has highest frequency (390K txns) -- loyalty card integration opportunity', 'priority': 'Medium'},
    {'category': 'Digital Growth', 'finding': 'Online merchants growing 3x faster than brick-and-mortar', 'priority': 'Medium'},
], st)
