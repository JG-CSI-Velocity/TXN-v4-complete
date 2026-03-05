import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import rege_trend, od_limit_dist, MONTH_LABELS
from charts import bar_chart, donut_chart, grouped_bar, trend_line, stacked_bar, fmt_dollar, fmt_count, action_summary
import plotly.graph_objects as go

st.header("Reg E & Overdraft Analysis")
st.caption("10 analyses | Opt-in trends, overdraft limit distribution, revenue exposure")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Opt-In Rate", "34.2%", "+2.8pp YoY")
c2.metric("Opted-In Accounts", "11,356")
c3.metric("Avg OD Limit", "$680")
c4.metric("Revenue Exposure", "$2.4M")
st.divider()

# Opt-in trend (03)
st.subheader("Opt-In Trend Over Time")
fig = go.Figure()
fig.add_trace(go.Scatter(x=MONTH_LABELS, y=rege_trend['opted_in'], name='Opted-In',
                         fill='tozeroy', line=dict(color=GEN_COLORS['success'])))
fig.add_trace(go.Scatter(x=MONTH_LABELS, y=rege_trend['opted_out'], name='Opted-Out',
                         fill='tozeroy', line=dict(color=GEN_COLORS['muted'])))
fig.update_layout(height=380, yaxis=dict(gridcolor='#E9ECEF', title='Accounts'),
                  margin=dict(l=50, r=20, t=20, b=40))
st.plotly_chart(fig, use_container_width=True, theme=None)

# Migration (04)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        ['Opted-In -> Out', 'Opted-Out -> In', 'Net Change'],
        [-420, 1580, 1160],
        title='Opt-In Migration (Period)', text_fmt=lambda x: f'{x:+,}',
        color=[GEN_COLORS['accent'], GEN_COLORS['success'], GEN_COLORS['primary']],
    ), use_container_width=True, theme=None)

# OD limit distribution (05)
with col2:
    st.plotly_chart(bar_chart(
        od_limit_dist['limit_band'].tolist(), od_limit_dist['accounts'].tolist(),
        title='OD Limit Distribution (Opted-In)', text_fmt=fmt_count,
        color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)

# OD limit trend (06)
st.subheader("Overdraft Limit Trend")
st.plotly_chart(trend_line(
    MONTH_LABELS, np.linspace(620, 680, len(MONTH_LABELS)).tolist(),
    title='Average OD Limit Over Time', y_title='Avg OD Limit ($)',
    color=GEN_COLORS['primary'],
), use_container_width=True, theme=None)

# By demographics (07)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
        {'Opt-In %': [28, 32, 38, 36, 34, 30]},
        title='Opt-In Rate by Age Band',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
        {'Opt-In %': [48, 42, 35, 28, 15]},
        title='Opt-In Rate by Engagement Tier',
    ), use_container_width=True, theme=None)

# Revenue exposure (08) + Balance correlation (09)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        ['Current Revenue', 'If 50% Opt-In', 'If 75% Opt-In'],
        [2_400_000, 3_500_000, 5_250_000],
        title='OD Revenue Scenarios', text_fmt=fmt_dollar,
        color=[GEN_COLORS['primary'], GEN_COLORS['info'], GEN_COLORS['success']],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['$0-500', '$500-2K', '$2K-5K', '$5K-10K', '$10K+'],
        {'Opt-In %': [42, 38, 32, 28, 22], 'Avg Usage %': [52, 35, 22, 15, 8]},
        title='Opt-In & Usage by Balance Band',
    ), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Opt-In Growth', 'finding': 'Opt-in rate growing +2.8pp YoY -- positive trend continuing', 'priority': 'Low'},
    {'category': 'Revenue Opportunity', 'finding': 'Moving to 50% opt-in would add $1.1M annual revenue', 'priority': 'High'},
    {'category': 'Power Tier', 'finding': 'Power tier has 48% opt-in -- good; focus on Heavy tier (42%) for quick wins', 'priority': 'Medium'},
    {'category': 'Low Balance', 'finding': 'Low-balance accounts have highest opt-in (42%) and usage (52%) -- monitor risk', 'priority': 'Medium'},
], st)
