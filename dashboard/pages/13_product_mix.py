import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import product_dist, MONTH_LABELS
from charts import bar_chart, donut_chart, grouped_bar, heatmap, trend_line, stacked_bar, fmt_dollar, fmt_count, action_summary
import plotly.graph_objects as go

st.header("Product Mix Analysis")
st.caption("10 analyses | Product code analysis, product mix performance")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Product Types", "8")
c2.metric("Top Product", "Platinum Rewards", "8,200 accts")
c3.metric("Avg Spend Spread", "15.8x", "Platinum vs Secured")
c4.metric("Business Products", "15.1%")
st.divider()

# Distribution (03) + Donut (04)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        product_dist['product'].tolist(), product_dist['accounts'].tolist(),
        title='Accounts by Product', text_fmt=fmt_count,
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(donut_chart(
        product_dist['product'], product_dist['accounts'],
        title='Product Distribution',
    ), use_container_width=True, theme=None)

# Spend profile (05)
st.subheader("Product Spend & Activity Profile")
st.plotly_chart(grouped_bar(
    product_dist['product'].tolist(),
    {'Avg Spend ($)': product_dist['avg_spend'].tolist(),
     'Avg Txns (x10)': (product_dist['avg_txns'] * 10).tolist()},
    title='Average Monthly Spend & Activity by Product',
), use_container_width=True, theme=None)

# Monthly trend (06)
fig = go.Figure()
for prod in product_dist['product'].head(4):
    fig.add_trace(go.Scatter(x=MONTH_LABELS,
                             y=np.random.normal(100, 5, len(MONTH_LABELS)).cumsum() / 8 + 90,
                             mode='lines', name=prod))
fig.update_layout(title='Product Trend', height=380,
                  yaxis=dict(gridcolor='#E9ECEF'), margin=dict(l=50, r=20, t=40, b=40))
st.plotly_chart(fig, use_container_width=True, theme=None)

# Merchant heatmap (07)
st.subheader("Top Merchants by Product")
_prod_merch = np.random.uniform(5, 30, (5, 5))
st.plotly_chart(heatmap(
    _prod_merch, ['Amazon', 'Walmart', 'Target', 'Shell', 'Starbucks'],
    product_dist['product'].head(5).tolist(),
    title='Spend Share by Product & Merchant',
), use_container_width=True, theme=None)

# Biz/Personal (08) + Engagement (09)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(stacked_bar(
        product_dist['product'].tolist(),
        {'Personal': [7200, 7000, 6500, 2400, 800, 400, 1400, 1685],
         'Business': [1000, 500, 300, 0, 2400, 1400, 100, 120]},
        title='Product: Business vs Personal',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
        {'Platinum': [42, 28, 18, 8, 4],
         'Gold': [28, 25, 22, 15, 10],
         'Classic': [12, 18, 25, 28, 17]},
        title='Product Mix by Engagement Tier (%)',
    ), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Platinum Performance', 'finding': 'Platinum Rewards = 24.7% of accounts but generates highest avg spend ($1,420)', 'priority': 'Low'},
    {'category': 'Upgrade Opportunity', 'finding': '20.5% on Classic product could be upgraded based on activity levels', 'priority': 'High'},
    {'category': 'Student Engagement', 'finding': 'Student accounts avg only 12 txns/mo -- lifecycle engagement program needed', 'priority': 'Medium'},
    {'category': 'Secured Pipeline', 'finding': '1,500 secured card holders -- 68% eligible for product graduation', 'priority': 'Medium'},
], st)
