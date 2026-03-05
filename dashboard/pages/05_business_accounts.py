import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import biz_top_merchants, MONTH_LABELS
from charts import bar_chart, donut_chart, trend_line, grouped_bar, fmt_dollar, fmt_count, action_summary
import plotly.graph_objects as go

st.header("Business Account Analysis")
st.caption("14 analyses | Business merchant patterns, spend concentration, trends")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Business Accounts", "4,820", "14.5% of portfolio")
c2.metric("Business Spend", "$148M", "29.7% of total")
c3.metric("Avg Spend/Acct", "$2,550/mo", "2.7x personal")
c4.metric("Avg Txn Count", "68/mo", "2.1x personal")
st.divider()

# Top 20 (03)
st.subheader("Top 10 Business Merchants")
st.plotly_chart(bar_chart(
    biz_top_merchants['merchant'][::-1].tolist(),
    (biz_top_merchants['total_spend'][::-1] * 1_000_000).tolist(),
    text_fmt=fmt_dollar, horizontal=True, height=400,
), use_container_width=True, theme=None)

# Donut (04) + Concentration (05)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(donut_chart(biz_top_merchants['merchant'], biz_top_merchants['total_spend'],
                                title='Business Merchant Spend Share'), use_container_width=True, theme=None)
with col2:
    _cum = np.cumsum(biz_top_merchants['total_spend']) / biz_top_merchants['total_spend'].sum() * 100
    st.plotly_chart(trend_line(
        [f'Top {i+1}' for i in range(len(biz_top_merchants))], _cum.tolist(),
        title='Concentration Curve', y_title='% of Business Spend',
    ), use_container_width=True, theme=None)

# Trend (06) + Growth (07)
col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    for m in biz_top_merchants['merchant'].head(3):
        fig.add_trace(go.Scatter(x=MONTH_LABELS,
                                 y=np.random.normal(100, 8, len(MONTH_LABELS)),
                                 mode='lines', name=m))
    fig.update_layout(title='Top 3 Business Merchant Trends', height=380,
                      yaxis=dict(gridcolor='#E9ECEF'), margin=dict(l=50, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True, theme=None)
with col2:
    _growth = [15, 8, 12, 6, -3, 4, -2, 18, 5, 2]
    _colors = [GEN_COLORS['success'] if g > 0 else GEN_COLORS['accent'] for g in _growth]
    st.plotly_chart(bar_chart(
        biz_top_merchants['merchant'].tolist(), _growth,
        title='YoY Growth Rate', text_fmt=lambda x: f'{x:+.0f}%', color=_colors,
    ), use_container_width=True, theme=None)

# Volatility (08) + Lifecycle (09)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        biz_top_merchants['merchant'].tolist(),
        np.random.uniform(0.05, 0.3, len(biz_top_merchants)).round(2).tolist(),
        title='Spend Volatility', text_fmt=lambda x: f'{x:.2f}', color=GEN_COLORS['warning'],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        ['Emerging', 'Growing', 'Mature', 'Declining'],
        [320, 1400, 2800, 300], title='Business Merchant Lifecycle', text_fmt=fmt_count,
        color=[GEN_COLORS['accent'], GEN_COLORS['success'], GEN_COLORS['info'], GEN_COLORS['muted']],
    ), use_container_width=True, theme=None)

# Vs portfolio (10)
st.subheader("Business vs Portfolio Comparison")
st.plotly_chart(grouped_bar(
    ['Avg Spend', 'Avg Txns', 'Avg Merchants', 'Power %'],
    {'Business': [2550, 68, 24, 18], 'Portfolio Avg': [950, 32, 18, 9]},
    title='Business Account Profile vs Portfolio Average',
), use_container_width=True, theme=None)

# By age (11) + engagement (12) + new entrants (13)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['18-35', '36-55', '56+'],
        {'Accounts': [680, 2400, 1740], 'Avg Spend': [1800, 2800, 2400]},
        title='Business Accounts by Age',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['Power', 'Heavy', 'Moderate', 'Light'],
        {'% of Tier': [18, 16, 12, 8]},
        title='Business % by Engagement Tier',
    ), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'High Value', 'finding': 'Business accounts are 14.5% of portfolio but 29.7% of spend', 'priority': 'High'},
    {'category': 'Amazon Business', 'finding': 'Amazon Business dominates at $8.2M -- investigate B2B card programs', 'priority': 'Medium'},
    {'category': 'Growth', 'finding': 'Business new account activation at 82% vs 68% portfolio avg', 'priority': 'Low'},
], st)
