import streamlit as st
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import retention_funnel, retention_by_tier
from charts import (bar_chart, grouped_bar, scatter_plot, trend_line, waterfall,
                    funnel_horizontal, fmt_dollar, fmt_count, action_summary)
import plotly.graph_objects as go

st.header("Retention & Churn Analysis")
st.caption("7 analyses | Account health, dormancy funnel, attrition cost, early warning")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Closed Account Rate", "3.8%")
c2.metric("Avg Tenure at Close", "4.2 yrs")
c3.metric("At-Risk Pipeline", "7,750")
c4.metric("Annual Spend at Risk", "$6.1M")
st.divider()

# Dormancy funnel (05)
st.subheader("Account Health Funnel")
st.plotly_chart(funnel_horizontal(
    retention_funnel['status'].tolist(), retention_funnel['accounts'].tolist(),
    retention_funnel['color'].tolist(),
), use_container_width=True, theme=None)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        retention_funnel['status'].tolist(), retention_funnel['accounts'].tolist(),
        title='Accounts by Health Status', text_fmt=fmt_count,
        color=retention_funnel['color'].tolist(),
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        retention_funnel['status'].tolist(), retention_funnel['annual_spend'].tolist(),
        title='Annual Spend by Status', text_fmt=fmt_dollar,
        color=retention_funnel['color'].tolist(),
    ), use_container_width=True, theme=None)

# Churn by segment (03)
st.subheader("Churn Rate by Engagement Tier")
st.plotly_chart(bar_chart(
    retention_by_tier['tier'].tolist(), retention_by_tier['churn_rate'].tolist(),
    title='Closed Account Rate by Tier', text_fmt=lambda x: f'{x:.1f}%',
    color=[GEN_COLORS['accent'], GEN_COLORS['warning'], GEN_COLORS['info'],
           GEN_COLORS['muted'], GEN_COLORS['muted']],
), use_container_width=True, theme=None)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
        {'Churn Rate %': [5.2, 3.1, 2.8, 3.5, 4.2, 6.8]},
        title='Churn Rate by Age Band',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['Primary', 'Secondary', 'Tertiary', 'Incidental'],
        {'Churn Rate %': [1.2, 3.5, 5.8, 8.2]},
        title='Churn Rate by PFI Tier',
    ), use_container_width=True, theme=None)

# Attrition cost (04)
st.subheader("Attrition Cost Analysis")
st.plotly_chart(waterfall(
    ['Retained\nRevenue', 'At-Risk\nRevenue', 'Cooling\nRevenue', 'Lost\n(Closed)',
     'Net Portfolio\nRevenue'],
    [380_000_000, -28_000_000, -2_100_000, -12_000_000, 337_900_000],
    title='Revenue Waterfall: Retention Impact',
), use_container_width=True, theme=None)

# Early warning (06)
st.subheader("Early Warning Signals")
np.random.seed(42)
st.dataframe(pd.DataFrame({
    'Account': [f'***{np.random.randint(1000,9999)}' for _ in range(10)],
    'Tier': np.random.choice(['Power', 'Heavy', 'Moderate'], 10),
    'Status': np.random.choice(['Declining', 'Cooling'], 10, p=[0.4, 0.6]),
    'Months Declining': np.random.randint(2, 6, 10),
    'Balance Trend': np.random.choice(['Falling', 'Stable', 'Rising'], 10, p=[0.5, 0.3, 0.2]),
    'Competitor?': np.random.choice(['Yes', 'No'], 10, p=[0.6, 0.4]),
    'Est. Annual Spend': np.random.randint(3000, 18000, 10),
}).style.format({'Est. Annual Spend': '${:,}'}),
    use_container_width=True, hide_index=True)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Churn Cost', 'finding': '$12M annual spend lost from closed accounts -- retention investment justified', 'priority': 'High'},
    {'category': 'Dormant Pipeline', 'finding': '3,650 dormant accounts with $2.1M residual activity -- reactivation window', 'priority': 'High'},
    {'category': 'PFI Correlation', 'finding': 'Incidental PFI tier has 8.2% churn vs 1.2% for Primary -- deepen relationships', 'priority': 'High'},
    {'category': 'Early Warning', 'finding': 'Launch proactive outreach for accounts showing 2+ risk signals', 'priority': 'High'},
    {'category': 'Age Risk', 'finding': '65+ accounts have 6.8% churn -- consider age-appropriate retention offers', 'priority': 'Medium'},
], st)
