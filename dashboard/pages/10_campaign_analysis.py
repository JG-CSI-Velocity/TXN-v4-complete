import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import campaign_summary, campaign_by_wave, cohort_lift, MONTH_LABELS
from charts import (bar_chart, grouped_bar, trend_line, donut_chart, stacked_bar,
                    heatmap, fmt_dollar, fmt_count, action_summary)
import plotly.graph_objects as go

st.header("ARS Campaign Analysis")
st.caption("25 analyses | Campaign response, cohort lift, DID analysis, swipe metrics")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Responders", "3,720", "30.0% rate")
c2.metric("Avg Lift/Responder", "$142/mo")
c3.metric("DID Lift", "$82/acct")
c4.metric("Protected Spend", "$6.3M")
st.divider()

# Response trend (03)
st.subheader("Campaign Response by Wave")
st.plotly_chart(grouped_bar(
    campaign_by_wave['wave'].tolist(),
    {'Mailed': campaign_by_wave['mailed'].tolist(),
     'Responded': campaign_by_wave['responded'].tolist()},
    title='Mail Volume vs Response by Wave',
), use_container_width=True, theme=None)

# Responder vs Non (04)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        campaign_by_wave['wave'].tolist(), campaign_by_wave['response_rate'].tolist(),
        title='Response Rate by Wave', text_fmt=lambda x: f'{x:.1f}%',
        color=GEN_COLORS['success'],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        campaign_by_wave['wave'].tolist(), campaign_by_wave['avg_lift'].tolist(),
        title='Avg Monthly Lift by Wave ($)', text_fmt=fmt_dollar,
        color=GEN_COLORS['primary'],
    ), use_container_width=True, theme=None)

# Merchant preferences (05) + Spend impact (06)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['Amazon', 'Walmart', 'Target', 'Gas', 'Restaurants'],
        {'Responders': [2800, 1800, 1200, 1400, 1600],
         'Non-Responders': [1200, 1400, 800, 1100, 900]},
        title='Merchant Preferences: Resp vs Non-Resp ($)',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['Before Campaign', 'After (Responders)', 'After (Non-Resp)'],
        {'Avg Monthly Spend': [680, 822, 692]},
        title='Spend Impact',
    ), use_container_width=True, theme=None)

# Campaign by engagement (08) + channel (09)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
        {'Response Rate %': [42, 38, 30, 22, 12],
         'Avg Lift $': [180, 165, 142, 98, 45]},
        title='Campaign Performance by Engagement Tier',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(donut_chart(
        ['Mail Only', 'Mail + Email', 'Mail + Phone', 'Digital Only'],
        [42, 28, 18, 12], title='Response by Channel Mix',
    ), use_container_width=True, theme=None)

st.divider()
st.subheader("Cohort Lift Analysis")

# Cohort before/after (13)
st.plotly_chart(trend_line(
    MONTH_LABELS, cohort_lift['responder_spend'].tolist(),
    title='Responder vs Non-Responder Spend Trajectory', y_title='Avg Monthly Spend ($)',
    color=GEN_COLORS['success'],
), use_container_width=True, theme=None)
# Overlay non-responder
fig = go.Figure()
fig.add_trace(go.Scatter(x=MONTH_LABELS, y=cohort_lift['responder_spend'], name='Responders',
                         line=dict(color=GEN_COLORS['success'], width=3)))
fig.add_trace(go.Scatter(x=MONTH_LABELS, y=cohort_lift['non_responder_spend'], name='Non-Responders',
                         line=dict(color=GEN_COLORS['accent'], width=3)))
fig.add_trace(go.Scatter(x=MONTH_LABELS, y=cohort_lift['counterfactual'], name='Counterfactual',
                         line=dict(color=GEN_COLORS['muted'], width=2, dash='dash')))
fig.update_layout(height=400, yaxis=dict(gridcolor='#E9ECEF', title='Avg Spend ($)'),
                  margin=dict(l=50, r=20, t=20, b=40))
st.plotly_chart(fig, use_container_width=True, theme=None)

# DID lift (14) + Cumulative (15)
col1, col2 = st.columns(2)
with col1:
    _did = (cohort_lift['responder_spend'] - cohort_lift['counterfactual']).tolist()
    st.plotly_chart(bar_chart(
        MONTH_LABELS, _did, title='DID Lift per Month ($)',
        text_fmt=lambda x: f'${x:.0f}', color=GEN_COLORS['primary'],
    ), use_container_width=True, theme=None)
with col2:
    _cum = np.cumsum(cohort_lift['responder_spend'] - cohort_lift['counterfactual']).tolist()
    st.plotly_chart(trend_line(
        MONTH_LABELS, _cum, title='Cumulative DID Lift ($)',
        y_title='Cumulative $ Lift', color=GEN_COLORS['success'], fill=True,
    ), use_container_width=True, theme=None)

# Penetration growth (16) + Persistence (17)
col1, col2 = st.columns(2)
with col1:
    _pen = np.linspace(62, 78, len(MONTH_LABELS)).tolist()
    st.plotly_chart(trend_line(
        MONTH_LABELS, _pen, title='Responder Merchant Penetration Growth',
        y_title='Unique Merchants', color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)
with col2:
    _persist = [100, 92, 88, 85, 82, 80, 78, 77, 76, 75, 74, 73, 72]
    st.plotly_chart(trend_line(
        MONTH_LABELS, _persist, title='Lift Persistence (% of initial lift retained)',
        y_title='% Retained', color=GEN_COLORS['warning'],
    ), use_container_width=True, theme=None)

# Swipe KPIs (21) + Response (22) + Trend (23) + 3vs12 (24)
st.divider()
st.subheader("Swipe Category Analysis")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['Very High', 'High', 'Medium', 'Low', 'Inactive'],
        {'Responders %': [18, 28, 32, 15, 7], 'Non-Responders %': [8, 18, 28, 28, 18]},
        title='Swipe Category: Responder vs Non-Responder',
    ), use_container_width=True, theme=None)
with col2:
    _3mo = np.random.uniform(20, 80, 5).round(0)
    _12mo = np.random.uniform(30, 90, 5).round(0)
    st.plotly_chart(grouped_bar(
        ['Very High', 'High', 'Medium', 'Low', 'Inactive'],
        {'3-Month Swipes': _3mo.tolist(), '12-Month Swipes': _12mo.tolist()},
        title='Swipe Category: 3-Month vs 12-Month',
    ), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Campaign ROI', 'finding': '30% response rate with $142/mo avg lift -- strong positive ROI', 'priority': 'High'},
    {'category': 'DID Lift', 'finding': 'True causal lift of $82/acct after controlling for counterfactual', 'priority': 'High'},
    {'category': 'Persistence', 'finding': '72% of initial lift persists at month 13 -- durable behavior change', 'priority': 'Low'},
    {'category': 'Targeting', 'finding': 'TH10 wave has highest response (35%) but lowest lift ($168) -- optimize thresholds', 'priority': 'Medium'},
    {'category': 'Engagement Gap', 'finding': 'Light/Dormant tiers have 17% response rate -- different campaign needed', 'priority': 'Medium'},
], st)
