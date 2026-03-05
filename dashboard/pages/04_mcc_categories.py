import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, AGE_ORDER
from demo_data import mcc_categories, MONTH_LABELS
from charts import bar_chart, donut_chart, trend_line, grouped_bar, heatmap, fmt_dollar, fmt_count, action_summary

st.header("MCC Category Analysis")
st.caption("15 analyses | Category spend by demographics, trends, diversity")

c1, c2, c3, c4 = st.columns(4)
c1.metric("MCC Categories", "248")
c2.metric("Top 5 Concentration", "56.8%")
c3.metric("Avg Category Diversity", "8.2/acct")
c4.metric("Fastest Growing", "Subscriptions", "+28%")
st.divider()

display = mcc_categories.head(10)

# Top 20 bar (03)
st.subheader("Top MCC Categories by Spend")
st.plotly_chart(bar_chart(
    display['category'][::-1].tolist(), (display['total_spend'][::-1] * 1_000_000).tolist(),
    text_fmt=fmt_dollar, horizontal=True, height=420,
), use_container_width=True, theme=None)

# Donut (04) + Three panel (05)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(donut_chart(display['category'], display['total_spend'],
                                title='Spend Share by Category'), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(display['category'].tolist(), display['avg_txn_size'].tolist(),
                              title='Avg Transaction Size by Category', text_fmt=fmt_dollar,
                              color=GEN_COLORS['info']), use_container_width=True, theme=None)

# Concentration (06)
col1, col2 = st.columns(2)
with col1:
    _cum = np.cumsum(display['total_spend']) / mcc_categories['total_spend'].sum() * 100
    st.plotly_chart(trend_line(
        [f'Top {i+1}' for i in range(len(display))], _cum.tolist(),
        title='Category Concentration Curve', y_title='% of Total',
    ), use_container_width=True, theme=None)

# Trend (07)
with col2:
    import plotly.graph_objects as go
    fig = go.Figure()
    for cat in ['Grocery', 'Gas/Fuel', 'Restaurants', 'Subscriptions']:
        fig.add_trace(go.Scatter(x=MONTH_LABELS,
                                 y=np.random.normal(100, 5, len(MONTH_LABELS)).cumsum() / 10 + 90,
                                 mode='lines', name=cat))
    fig.update_layout(title='Category Trend', height=380,
                      yaxis=dict(gridcolor='#E9ECEF'), margin=dict(l=50, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True, theme=None)

# By age band (08)
st.subheader("Category Spend by Age Band")
_cat_age = np.random.uniform(5, 30, (5, 6))
st.plotly_chart(heatmap(_cat_age, AGE_ORDER,
                        ['Grocery', 'Gas', 'Restaurants', 'General', 'Healthcare'],
                        title='Spend Index by Category & Age'), use_container_width=True, theme=None)

# By account age (09) + engagement (10)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['New (<1yr)', 'Mid (1-5yr)', 'Mature (5yr+)'],
        {'Grocery': [58, 82, 78], 'Gas': [42, 52, 38], 'Restaurants': [55, 48, 32]},
        title='Category by Account Maturity ($M)',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['Power', 'Heavy', 'Moderate', 'Light'],
        {'Grocery': [12, 8, 5, 2], 'Gas': [8, 5, 3, 1], 'Subscriptions': [2.5, 1.8, 1.2, 0.4]},
        title='Category by Engagement Tier ($M)',
    ), use_container_width=True, theme=None)

# Biz/Personal (11)
st.subheader("Business vs Personal Category Mix")
st.plotly_chart(grouped_bar(
    display['category'].head(6).tolist(),
    {'Personal': [72, 42, 38, 28, 24, 20], 'Business': [10, 6, 4, 10, 4, 4]},
    title='Category Spend: Business vs Personal ($M)',
), use_container_width=True, theme=None)

# Seasonal (12) + Diversity (13) + Spend profile (14)
col1, col2 = st.columns(2)
with col1:
    _seasonal = np.random.uniform(80, 130, (5, len(MONTH_LABELS)))
    st.plotly_chart(heatmap(_seasonal, MONTH_LABELS,
                            ['Grocery', 'Gas', 'Restaurants', 'Travel', 'Entertainment'],
                            title='Seasonal Index by Category'), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        ['1-3', '4-6', '7-9', '10-12', '13+'],
        [4200, 8500, 9800, 6200, 4505],
        title='Category Diversity (# categories used)', text_fmt=fmt_count,
        color=GEN_COLORS['success'],
    ), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Grocery Dominance', 'finding': 'Grocery = 16.5% of spend, stable across all demographics', 'priority': 'Low'},
    {'category': 'Subscription Growth', 'finding': 'Recurring subscriptions +28% YoY, now 5th largest category', 'priority': 'Medium'},
    {'category': 'Travel Recovery', 'finding': 'Travel spend rebounding +18% but still below 2019 baseline', 'priority': 'Low'},
    {'category': 'Healthcare', 'finding': 'Healthcare avg txn $133 -- high value, investigate insurance linkage', 'priority': 'Medium'},
], st)
