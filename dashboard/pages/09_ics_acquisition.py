import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import ics_channels, MONTH_LABELS
from charts import bar_chart, grouped_bar, trend_line, donut_chart, fmt_dollar, fmt_count, action_summary
import plotly.graph_objects as go

st.header("ICS Acquisition Analysis")
st.caption("10 analyses | Acquisition source analysis, channel performance")

c1, c2, c3, c4 = st.columns(4)
c1.metric("New Accounts (ICS)", "12,400")
c2.metric("Best Channel", "Branch Referral", "78% activation")
c3.metric("Avg 1st Month Spend", "$348")
c4.metric("90-Day Retention", "74.8%")
st.divider()

# Channel comparison (03)
st.subheader("Acquisition Channel Comparison")
st.plotly_chart(bar_chart(
    ics_channels['channel'].tolist(), ics_channels['accounts'].tolist(),
    title='Accounts by Channel', text_fmt=fmt_count,
    color=[GEN_COLORS['primary'], GEN_COLORS['info'], GEN_COLORS['warning'],
           GEN_COLORS['muted'], GEN_COLORS['success']],
), use_container_width=True, theme=None)

# Merchant preferences (04) + Spend profile (05)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ics_channels['channel'].tolist(),
        {'Activation %': ics_channels['activation_rate'].tolist(),
         '90d Retention %': ics_channels['90day_retention'].tolist()},
        title='Channel Quality Metrics',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        ics_channels['channel'].tolist(), ics_channels['avg_first_month_spend'].tolist(),
        title='Avg First Month Spend by Channel', text_fmt=fmt_dollar,
        color=GEN_COLORS['success'],
    ), use_container_width=True, theme=None)

# Monthly trend (06)
st.subheader("Monthly Acquisition Trend")
fig = go.Figure()
for ch in ['Branch Referral', 'Online Application', 'Direct Mail']:
    fig.add_trace(go.Scatter(x=MONTH_LABELS,
                             y=np.random.randint(200, 500, len(MONTH_LABELS)),
                             mode='lines+markers', name=ch))
fig.update_layout(height=380, yaxis=dict(gridcolor='#E9ECEF', title='New Accounts'),
                  margin=dict(l=50, r=20, t=20, b=40))
st.plotly_chart(fig, use_container_width=True, theme=None)

# Engagement (07) + Retention (08)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(donut_chart(
        ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
        [5, 12, 28, 35, 20],
        title='ICS Account Engagement Distribution',
    ), use_container_width=True, theme=None)
with col2:
    _months = list(range(1, 13))
    _retention = [100, 88, 82, 78, 75, 72, 70, 68, 66, 65, 64, 63]
    st.plotly_chart(trend_line(
        [f'Month {m}' for m in _months], _retention,
        title='ICS Cohort Retention Curve', y_title='% Still Active',
        color=GEN_COLORS['accent'],
    ), use_container_width=True, theme=None)

# Vs portfolio (09)
st.subheader("ICS Accounts vs Portfolio Average")
st.plotly_chart(grouped_bar(
    ['Avg Spend', 'Avg Txns', 'Merchants Used', 'Competitor %'],
    {'ICS Accounts': [420, 18, 8, 35], 'Portfolio Avg': [950, 32, 18, 55]},
    title='ICS Performance Gap',
), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Branch Referral', 'finding': 'Branch referrals have 78% activation and 88% retention -- best channel', 'priority': 'High'},
    {'category': 'Online Gap', 'finding': 'Online apps have 13pp lower retention than branch -- improve onboarding flow', 'priority': 'High'},
    {'category': 'Direct Mail', 'finding': 'Direct mail lowest activation (52%) -- review targeting criteria', 'priority': 'Medium'},
    {'category': 'Engagement', 'finding': '55% of ICS accounts in Light/Dormant -- early engagement program needed', 'priority': 'High'},
], st)
