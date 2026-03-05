import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, ENGAGE_PALETTE
from demo_data import competitor_data, comp_by_segment, MONTH_LABELS
from charts import (bar_chart, donut_chart, trend_line, grouped_bar, scatter_plot,
                    bubble_chart, heatmap, fmt_dollar, fmt_count, action_summary)

st.header("Direct Competition Analysis")
st.caption("35 analyses | Competitor detection, wallet share, threat assessment, segmentation")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Accounts w/ Competitors", "18,420", "55.5%")
c2.metric("Top Competitor", "Chase", "8,200 accts")
c3.metric("Avg Wallet Share Lost", "14.2%")
c4.metric("Exclusive to CU", "44.5%")
st.divider()

# Top competitors bar (08)
st.subheader("Competitor Penetration")
st.plotly_chart(bar_chart(
    competitor_data['competitor'].tolist(), competitor_data['accounts_using'].tolist(),
    text_fmt=fmt_count,
    color=[GEN_COLORS['accent'] if i == 0 else GEN_COLORS['info'] for i in range(len(competitor_data))],
), use_container_width=True, theme=None)

# Category donut (09) + Biz vs Personal (10)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(donut_chart(
        competitor_data['competitor'], competitor_data['wallet_share'],
        title='Wallet Share by Competitor',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        competitor_data['competitor'].head(5).tolist(),
        {'Business': [1200, 800, 600, 420, 280],
         'Personal': [7000, 5300, 4200, 3480, 1820]},
        title='Business vs Personal Penetration',
    ), use_container_width=True, theme=None)

# Monthly trend (11)
st.subheader("Competitor Activity Trend")
fig = go.Figure()
for comp in competitor_data['competitor'].head(4):
    fig.add_trace(go.Scatter(
        x=MONTH_LABELS, y=np.random.normal(100, 5, len(MONTH_LABELS)).cumsum() / 10 + 90,
        mode='lines', name=comp,
    ))
fig.update_layout(height=380, yaxis=dict(gridcolor='#E9ECEF'),
                  margin=dict(l=50, r=20, t=20, b=40))
st.plotly_chart(fig, use_container_width=True, theme=None)

# Bubble chart (12) + Threat quadrant (13)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bubble_chart(
        competitor_data['accounts_using'].tolist(),
        competitor_data['wallet_share'].tolist(),
        competitor_data['avg_competitor_spend'].tolist(),
        competitor_data['competitor'].tolist(),
        title='Accounts vs Wallet Share (bubble = avg spend)',
        x_title='Accounts Using', y_title='Wallet Share %',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(scatter_plot(
        competitor_data['accounts_using'].tolist(),
        competitor_data['threat_score'].tolist(),
        title='Threat Assessment Quadrant',
        x_title='Penetration (accounts)', y_title='Threat Score',
    ), use_container_width=True, theme=None)

# Engagement scatter (14) + Momentum (15)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        comp_by_segment['segment'].tolist(),
        {'% With Competitor': comp_by_segment['pct_with_competitor'].tolist(),
         'Avg Wallet Share': comp_by_segment['avg_wallet_share'].tolist()},
        title='Competition by Engagement Tier',
    ), use_container_width=True, theme=None)
with col2:
    _mom = competitor_data[['competitor', 'monthly_trend']].copy()
    _colors = [GEN_COLORS['accent'] if m > 0 else GEN_COLORS['success'] for m in _mom['monthly_trend']]
    st.plotly_chart(bar_chart(
        _mom['competitor'].tolist(), _mom['monthly_trend'].tolist(),
        title='Competitor Momentum (monthly % change)',
        text_fmt=lambda x: f'{x:+.1f}%', color=_colors,
    ), use_container_width=True, theme=None)

# Opportunity (16) + Total spend (17)
st.subheader("Competitive Opportunity Analysis")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        competitor_data['competitor'].tolist(),
        (competitor_data['accounts_using'] * competitor_data['avg_competitor_spend']).tolist(),
        title='Recoverable Annual Spend ($)', text_fmt=fmt_dollar,
        color=GEN_COLORS['success'],
    ), use_container_width=True, theme=None)
with col2:
    _total = competitor_data['accounts_using'] * competitor_data['avg_competitor_spend'] * 12
    st.plotly_chart(bar_chart(
        competitor_data['competitor'].tolist(), _total.tolist(),
        title='Annualized Competitor Spend ($)', text_fmt=fmt_dollar,
    ), use_container_width=True, theme=None)

# Segment summary (21-24)
st.subheader("Competitor Segmentation")
_seg_heatmap = np.random.uniform(5, 35, (5, 5))
st.plotly_chart(heatmap(
    _seg_heatmap, ['Chase', 'BofA', 'WF', 'CapOne', 'Citi'],
    ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
    title='Competitor Penetration by Segment (%)',
), use_container_width=True, theme=None)

# At risk accounts (25) + Wallet share (29)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        ['0%', '1-10%', '10-25%', '25-50%', '50-75%', '75%+'],
        [14785, 5200, 4800, 4200, 2800, 1420],
        title='Wallet Share Distribution', text_fmt=fmt_count,
        color=[GEN_COLORS['success'], GEN_COLORS['success'], GEN_COLORS['info'],
               GEN_COLORS['warning'], GEN_COLORS['accent'], GEN_COLORS['accent']],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        ['Low Risk', 'Watch', 'At Risk', 'Critical'],
        [18200, 6800, 5200, 3005],
        title='Competitive Risk Classification', text_fmt=fmt_count,
        color=[GEN_COLORS['success'], GEN_COLORS['info'], GEN_COLORS['warning'], GEN_COLORS['accent']],
    ), use_container_width=True, theme=None)

# Material threats (32) + Non-bank (33)
st.subheader("Emerging Threats")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        ['Apple Card', 'PayPal', 'Venmo', 'Cash App', 'Chime'],
        [2400, 3800, 2200, 1800, 1200],
        title='Non-Bank/Fintech Threats (accounts)', text_fmt=fmt_count,
        color=GEN_COLORS['warning'],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        ['Chase Sapphire', 'Amex Gold', 'CapOne Venture', 'Citi Double Cash'],
        [3200, 1800, 2400, 1500],
        title='Material Product Threats (accounts)', text_fmt=fmt_count,
        color=GEN_COLORS['accent'],
    ), use_container_width=True, theme=None)

# Editable competitor list
st.divider()
st.subheader("Configure Competitors")
st.multiselect("Local competitor list", competitor_data['competitor'].tolist(),
               default=competitor_data['competitor'].tolist())
st.button("Rerun Competition Analysis", type="primary", disabled=True)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Chase Dominance', 'finding': 'Chase present in 24.7% of accounts with 18.5% wallet share', 'priority': 'High'},
    {'category': 'Moderate Tier Leakage', 'finding': '62% of Moderate tier has competitor activity -- highest risk segment', 'priority': 'High'},
    {'category': 'Capital One Momentum', 'finding': 'Capital One growing +2.1%/month -- fastest growing competitor', 'priority': 'Medium'},
    {'category': 'Fintech Disruption', 'finding': 'Non-bank threats (PayPal, Venmo, Cash App) = 7,800 accounts combined', 'priority': 'Medium'},
    {'category': 'Wallet Recovery', 'finding': '$61M annualized spend recoverable from top 5 competitors', 'priority': 'High'},
], st)
