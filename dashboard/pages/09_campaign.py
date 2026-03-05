import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import (campaign_summary, campaign_by_wave, cohort_lift, MONTH_LABELS,
                       campaign_swipe_comparison)
from charts import (bar_chart, grouped_bar, trend_line, donut_chart,
                    fmt_dollar, fmt_count, action_summary)

st.markdown(
    '<h1 style="font-family:Outfit,sans-serif; font-size:1.8rem; '
    'letter-spacing:-0.03em; margin-bottom:2px;">Campaign Effectiveness</h1>'
    '<p style="color:#64748B; font-size:13px; margin-bottom:24px;">'
    'ARS campaign response, cohort lift, DID analysis, swipe metrics</p>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Responders", "3,720", "30.0% rate")
c2.metric("Avg Lift/Responder", "$142/mo")
c3.metric("DID Lift", "$82/acct")
c4.metric("Protected Spend", "$6.3M")

st.divider()

st.plotly_chart(grouped_bar(
    campaign_by_wave['wave'].tolist(),
    {'Mailed': campaign_by_wave['mailed'].tolist(),
     'Responded': campaign_by_wave['responded'].tolist()},
    title='Mail Volume vs Response by Wave',
), use_container_width=True, theme=None)

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

fig = go.Figure()
fig.add_trace(go.Scatter(x=MONTH_LABELS, y=cohort_lift['responder_spend'], name='Responders',
                         line=dict(color=GEN_COLORS['success'], width=3)))
fig.add_trace(go.Scatter(x=MONTH_LABELS, y=cohort_lift['non_responder_spend'], name='Non-Responders',
                         line=dict(color=GEN_COLORS['accent'], width=3)))
fig.add_trace(go.Scatter(x=MONTH_LABELS, y=cohort_lift['counterfactual'], name='Counterfactual',
                         line=dict(color=GEN_COLORS['muted'], width=2, dash='dash')))
fig.update_layout(height=400, title='Responder vs Non-Responder Spend Trajectory',
                  yaxis=dict(title='Avg Spend ($)'))
st.plotly_chart(fig, use_container_width=True, theme=None)

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

st.divider()
st.subheader("Swipe Category Analysis")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['Very High', 'High', 'Medium', 'Low', 'Inactive'],
        {'Responders %': campaign_swipe_comparison[0].tolist(),
         'Non-Responders %': campaign_swipe_comparison[1].tolist()},
        title='Swipe Category: Responder vs Non-Responder',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['Very High', 'High', 'Medium', 'Low', 'Inactive'],
        {'3-Month Swipes': campaign_swipe_comparison[2].tolist(),
         '12-Month Swipes': campaign_swipe_comparison[3].tolist()},
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
