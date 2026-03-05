import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import finsvc_categories, finsvc_top_merchants, MONTH_LABELS
from charts import (bar_chart, donut_chart, trend_line, grouped_bar, heatmap,
                    waterfall, fmt_dollar, fmt_count, action_summary)
import plotly.graph_objects as go

st.header("Financial Services Analysis")
st.caption("19 analyses | Financial services transaction patterns, provider analysis")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Accounts Using FinSvc", "24,800", "74.7%")
c2.metric("Total FinSvc Spend", "$78.1M")
c3.metric("Avg Monthly/Acct", "$262")
c4.metric("Multi-Category Users", "42.3%")
st.divider()

# Category accounts bar (07) + Activity donut (08)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        finsvc_categories['category'].tolist(), finsvc_categories['accounts'].tolist(),
        title='Accounts by FinSvc Category', text_fmt=fmt_count,
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(donut_chart(
        finsvc_categories['category'], finsvc_categories['total_spend'],
        title='Spend by FinSvc Category',
    ), use_container_width=True, theme=None)

# Top merchants (09)
st.subheader("Top Financial Services Providers")
st.plotly_chart(bar_chart(
    finsvc_top_merchants['merchant'][::-1].tolist(),
    finsvc_top_merchants['accounts'][::-1].tolist(),
    text_fmt=fmt_count, horizontal=True, height=400,
    color=GEN_COLORS['info'],
), use_container_width=True, theme=None)

# Recency heatmap (10)
st.subheader("Recency by Category")
_recency = np.random.uniform(10, 90, (7, 4))
st.plotly_chart(heatmap(
    _recency, ['<30d', '30-90d', '90-180d', '180d+'],
    finsvc_categories['category'].tolist(),
    title='% of Accounts by Recency',
), use_container_width=True, theme=None)

# Monthly trend (11) + Multi-product (12)
col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    for cat in ['Banking/ATM', 'Insurance', 'Investment']:
        fig.add_trace(go.Scatter(x=MONTH_LABELS,
                                 y=np.random.normal(100, 5, len(MONTH_LABELS)).cumsum() / 8 + 85,
                                 mode='lines', name=cat))
    fig.update_layout(title='FinSvc Category Trends', height=380,
                      yaxis=dict(gridcolor='#E9ECEF'), margin=dict(l=50, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        ['1 category', '2 categories', '3 categories', '4+'],
        [14400, 6200, 2800, 1400],
        title='Multi-Category Usage', text_fmt=fmt_count, color=GEN_COLORS['success'],
    ), use_container_width=True, theme=None)

# Category combinations (13) + Leakage (14)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        ['Bank+Insurance', 'Bank+Invest', 'Insurance+Tax', 'Bank+Lending', 'Full Suite'],
        [8400, 4200, 1800, 2400, 800],
        title='Most Common Category Pairs', text_fmt=fmt_count,
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        finsvc_categories['category'].tolist(),
        np.random.uniform(15, 65, len(finsvc_categories)).round(0).tolist(),
        title='Leakage Intensity (% using competitor FinSvc)', text_fmt=lambda x: f'{x:.0f}%',
        color=GEN_COLORS['accent'],
    ), use_container_width=True, theme=None)

# Biz vs Personal (15) + Recency by category (16)
st.plotly_chart(grouped_bar(
    finsvc_categories['category'].tolist(),
    {'Personal': np.random.uniform(5, 35, len(finsvc_categories)).round(1).tolist(),
     'Business': np.random.uniform(2, 15, len(finsvc_categories)).round(1).tolist()},
    title='FinSvc Spend: Business vs Personal ($M)',
), use_container_width=True, theme=None)

# Opportunity waterfall (18)
st.subheader("Revenue Opportunity")
st.plotly_chart(waterfall(
    ['Current FinSvc\nRevenue', 'Cross-sell\nInsurance', 'Capture\nInvestment',
     'Reduce\nLeakage', 'New Lending', 'Potential\nTotal'],
    [78_100_000, 12_000_000, 8_500_000, 15_000_000, 6_200_000, 119_800_000],
    title='Financial Services Revenue Opportunity',
), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Banking Leakage', 'finding': 'Chase ATM = 8,500 accounts -- significant competitor banking relationship', 'priority': 'High'},
    {'category': 'Insurance Gap', 'finding': '74.7% of members use external FinSvc -- insurance partnership opportunity', 'priority': 'Medium'},
    {'category': 'Investment', 'finding': 'Only 15.7% use investment services through CU -- cross-sell opportunity', 'priority': 'Medium'},
    {'category': 'Multi-Category', 'finding': 'Multi-category users show 2.4x higher retention -- drive cross-category adoption', 'priority': 'High'},
], st)
