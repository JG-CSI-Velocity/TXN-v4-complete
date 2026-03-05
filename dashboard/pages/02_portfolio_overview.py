import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, ENGAGE_PALETTE, AGE_PALETTE, AGE_ORDER
from demo_data import (monthly_trend, tier_dist, age_dist, acct_age_dist, bracket_dist,
                       hourly_heatmap, seasonal_index, growth_metrics, HOURS, DAYS, MONTH_LABELS)
from charts import (bar_chart, donut_chart, trend_line, dual_axis_bar_line, heatmap,
                    grouped_bar, stacked_bar, fmt_dollar, fmt_count)

st.header("Portfolio Overview")
st.caption("29 analyses | 33,205 accounts | 5.89M transactions | Jan 2025 - Jan 2026")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Accounts", "33,205", "+3.2%")
c2.metric("Total Transactions", "5.89M", "+8.1%")
c3.metric("Total Spend", "$498M", "+6.8%")
c4.metric("Active Rate", "88.5%", "+1.2%")
st.divider()

# --- Monthly Trend (04) ---
st.subheader("Monthly Transaction Trend")
st.plotly_chart(dual_axis_bar_line(
    monthly_trend['label'], monthly_trend['transactions'],
    monthly_trend['spend'] / 1_000_000,
    bar_name='Transactions', line_name='Spend ($M)',
), use_container_width=True, theme=None)

# --- Monthly Table (05) ---
with st.expander("Monthly Detail Table"):
    st.dataframe(monthly_trend[['label', 'transactions', 'spend', 'active_accounts', 'avg_txn']].rename(
        columns={'label': 'Month', 'transactions': 'Txns', 'spend': 'Spend',
                 'active_accounts': 'Active', 'avg_txn': 'Avg Txn'}
    ).style.format({'Txns': '{:,}', 'Spend': '${:,.0f}', 'Active': '{:,}', 'Avg Txn': '${:.2f}'}),
        use_container_width=True, hide_index=True)

# --- Bracket Analysis (07, 08, 09, 10) ---
st.subheader("Spend Bracket Analysis")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        bracket_dist['bracket'], bracket_dist['txn_count'],
        title='Transaction Count by Bracket', text_fmt=fmt_count,
        color=['#A8DADC', '#457B9D', '#2EC4B6', '#FF9F1C', '#F4A261', '#E76F51', '#E63946', '#1B2A4A'],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(donut_chart(
        bracket_dist['bracket'], bracket_dist['total_spend'],
        colors=['#A8DADC', '#457B9D', '#2EC4B6', '#FF9F1C', '#F4A261', '#E76F51', '#E63946', '#1B2A4A'],
        title='Spend Distribution by Bracket',
    ), use_container_width=True, theme=None)

# Bracket volatility (09) + trend (10)
col1, col2 = st.columns(2)
with col1:
    _vol = np.random.uniform(0.03, 0.25, len(bracket_dist))
    st.plotly_chart(bar_chart(
        bracket_dist['bracket'], _vol, title='Bracket Volatility (CoV)',
        text_fmt=lambda x: f'{x:.2f}',
        color=['#A8DADC', '#457B9D', '#2EC4B6', '#FF9F1C', '#F4A261', '#E76F51', '#E63946', '#1B2A4A'],
    ), use_container_width=True, theme=None)
with col2:
    fig = go.Figure()
    for i, bracket in enumerate(['< $1', '$10-25', '$100-500', '$500+']):
        fig.add_trace(go.Scatter(
            x=MONTH_LABELS, y=np.random.normal(100, 8, len(MONTH_LABELS)).cumsum() / 10 + 90,
            mode='lines', name=bracket,
        ))
    fig.update_layout(title='Bracket Trend Over Time', height=380,
                      yaxis=dict(gridcolor='#E9ECEF'), margin=dict(l=50, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True, theme=None)

# --- Demographics (11-15) ---
st.subheader("Age Demographics")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        age_dist['age_band'], age_dist['accounts'], title='Accounts by Age Band',
        color=[AGE_PALETTE[a] for a in age_dist['age_band']], text_fmt=fmt_count,
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        age_dist['age_band'], age_dist['avg_spend'], title='Avg Monthly Spend by Age',
        color=[AGE_PALETTE[a] for a in age_dist['age_band']], text_fmt=fmt_dollar,
    ), use_container_width=True, theme=None)

# Hourly heatmap (12)
st.subheader("Hourly Activity Heatmap")
st.plotly_chart(heatmap(
    hourly_heatmap, [f'{h:02d}:00' for h in HOURS], DAYS,
    title='Transaction Volume by Day & Hour (% of peak)',
    text_fmt=lambda x: f'{x:.0f}',
), use_container_width=True, theme=None)

# Age x time patterns (13), age spending profile (14), age bracket comparison (15)
col1, col2 = st.columns(2)
with col1:
    _age_time = np.random.uniform(5, 25, (6, 4))
    st.plotly_chart(heatmap(
        _age_time, ['Morning', 'Afternoon', 'Evening', 'Night'], AGE_ORDER,
        title='Spend by Age & Time of Day',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        AGE_ORDER,
        {'Avg Txns': age_dist['avg_txns'].tolist(), 'Avg Spend ($100s)': (age_dist['avg_spend'] / 100).tolist()},
        title='Age Band Spending Profile',
    ), use_container_width=True, theme=None)

# Biz/Personal split (16)
st.subheader("Business vs Personal Split")
col1, col2, col3 = st.columns(3)
col1.metric("Business Accounts", "4,820", "14.5%")
col2.metric("Personal Accounts", "28,385", "85.5%")
col3.metric("Business Avg Spend", "$2,550/mo", "2.7x personal")

# Engagement tiers (17-18)
st.subheader("Engagement Tier Distribution")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(donut_chart(
        tier_dist['tier'], tier_dist['accounts'],
        colors=[ENGAGE_PALETTE[t] for t in tier_dist['tier']],
        title='Accounts by Engagement Tier',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        tier_dist['tier'], tier_dist['avg_monthly_spend'],
        title='Avg Monthly Spend by Tier', text_fmt=fmt_dollar,
        color=[ENGAGE_PALETTE[t] for t in tier_dist['tier']],
    ), use_container_width=True, theme=None)

# Seasonal index (19)
st.subheader("Seasonal Spending Index")
st.plotly_chart(trend_line(
    seasonal_index['month'], seasonal_index['index'],
    title='Monthly Spending Index (100 = average)', y_title='Index',
    color=GEN_COLORS['warning'],
), use_container_width=True, theme=None)

# Merchant concentration (20)
st.subheader("Merchant Concentration")
_conc = [28, 45, 58, 68, 75, 82, 88, 92, 95, 97]
st.plotly_chart(trend_line(
    [f'Top {i}' for i in [1, 2, 3, 5, 10, 20, 50, 100, 200, 500]],
    _conc, title='Cumulative Spend by Top N Merchants', y_title='% of Total Spend',
    color=GEN_COLORS['info'],
), use_container_width=True, theme=None)

# Growth scorecard (21)
st.subheader("Growth Scorecard")
st.dataframe(growth_metrics, use_container_width=True, hide_index=True)

# Account age (23-28)
st.subheader("Account Age Analysis")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        acct_age_dist['band'], acct_age_dist['accounts'],
        title='Accounts by Account Age', text_fmt=fmt_count,
        color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        acct_age_dist['band'], acct_age_dist['avg_spend'],
        title='Avg Spend by Account Age', text_fmt=fmt_dollar,
        color=GEN_COLORS['success'],
    ), use_container_width=True, theme=None)

# Lifecycle summary (28)
st.subheader("Account Lifecycle Summary")
_lifecycle = {'New (<90d)': [1200, 68, 180], '1st Year': [5000, 75, 420],
              'Established (1-5yr)': [13500, 88, 780], 'Mature (5yr+)': [13505, 82, 720]}
st.dataframe(
    [{'Stage': k, 'Accounts': f'{v[0]:,}', 'Activation %': f'{v[1]}%', 'Avg Spend': f'${v[2]:,}'}
     for k, v in _lifecycle.items()],
    use_container_width=True, hide_index=True,
)
