import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import attrition_tiers, MONTH_LABELS
from charts import bar_chart, grouped_bar, scatter_plot, trend_line, heatmap, fmt_dollar, fmt_count, action_summary

st.header("Attrition Risk Analysis")
st.caption("12 analyses | Spend velocity, early warning signals, dormancy progression")

c1, c2, c3, c4 = st.columns(4)
c1.metric("At-Risk Accounts", "6,082", "18.3%")
c2.metric("Spend at Risk", "$4.2M/yr")
c3.metric("Avg Velocity (Declining)", "0.42x")
c4.metric("Dormant (3mo+)", "3,242")
st.divider()

# Risk distribution (03)
st.subheader("Risk Tier Distribution")
st.plotly_chart(bar_chart(
    attrition_tiers['tier'].tolist(), attrition_tiers['accounts'].tolist(),
    text_fmt=lambda x: f'{x:,.0f}',
    color=['#2EC4B6', '#FF9F1C', '#E76F51', '#E63946'],
), use_container_width=True, theme=None)

# Velocity scatter (04)
st.subheader("Spend Velocity vs Balance")
np.random.seed(42)
n = 600
_vel = np.concatenate([
    np.random.normal(1.0, 0.2, 350).clip(0.3, 1.8),
    np.random.normal(0.4, 0.15, 130).clip(0.01, 0.8),
    np.random.normal(0.05, 0.03, 120).clip(0, 0.15),
])
_bal = np.random.lognormal(7.5, 1.2, n).clip(100, 100_000)
_tiers = ['Stable'] * 350 + ['Declining'] * 130 + ['Dormant'] * 120
_colors = {'Stable': '#2EC4B6', 'Declining': '#E76F51', 'Dormant': '#E63946'}
fig = scatter_plot(_bal, _vel, _tiers, _colors,
                   x_title='Current Balance ($)', y_title='Spend Velocity')
fig.update_xaxes(type='log')
fig.add_hrect(y0=0, y1=0.5, fillcolor='rgba(230,57,70,0.08)', line_width=0)
st.plotly_chart(fig, use_container_width=True, theme=None)

# Monthly progression (05)
st.subheader("Monthly Risk Tier Progression")
_months_data = {}
for tier, base in [('Stable', 22000), ('Slowing', 5000), ('Declining', 2500), ('Dormant', 3000)]:
    _months_data[tier] = (np.array([base] * len(MONTH_LABELS)) +
                          np.random.randint(-200, 200, len(MONTH_LABELS))).tolist()
from charts import stacked_bar
st.plotly_chart(stacked_bar(MONTH_LABELS, _months_data, title='Risk Tier Composition Over Time'), use_container_width=True, theme=None)

# Risk by demographics (06) + product (07) + competitor (08)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
        {'At-Risk %': [22, 15, 12, 18, 20, 28]},
        title='At-Risk Rate by Age Band',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['Platinum', 'Gold', 'Classic', 'Student', 'Secured'],
        {'At-Risk %': [8, 14, 22, 18, 35]},
        title='At-Risk Rate by Product',
    ), use_container_width=True, theme=None)

st.plotly_chart(grouped_bar(
    ['No Competitor', '1 Competitor', '2+ Competitors'],
    {'At-Risk %': [10, 22, 38], 'Avg Velocity': [1.02, 0.72, 0.48]},
    title='Attrition Risk by Competitor Activity',
), use_container_width=True, theme=None)

# Early warning (09)
st.subheader("Early Warning: 2+ Risk Signals")
st.dataframe(pd.DataFrame({
    'Account': [f'***{np.random.randint(1000,9999)}' for _ in range(8)],
    'Tier': np.random.choice(['Heavy', 'Moderate', 'Power'], 8),
    'Velocity': np.random.uniform(0.1, 0.5, 8).round(2),
    'Months Declining': np.random.randint(2, 6, 8),
    'Competitor?': np.random.choice(['Yes', 'No'], 8, p=[0.6, 0.4]),
    'Est. Annual Spend': np.random.randint(2000, 15000, 8),
}).style.format({'Velocity': '{:.2f}', 'Est. Annual Spend': '${:,}'}),
    use_container_width=True, hide_index=True)

# Dormancy progression (10)
st.subheader("Dormancy Progression Funnel")
from charts import funnel_horizontal
st.plotly_chart(funnel_horizontal(
    ['Active', 'Slowing', 'Declining', 'Dormant'],
    [21480, 5643, 2840, 3242],
    ['#2EC4B6', '#FF9F1C', '#E76F51', '#E63946'],
), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'At-Risk Pipeline', 'finding': '18.3% of portfolio showing disengagement -- $4.2M annual spend at risk', 'priority': 'High'},
    {'category': 'Competitor Correlation', 'finding': 'Accounts with 2+ competitors are 3.8x more likely to be at-risk', 'priority': 'High'},
    {'category': 'Age Pattern', 'finding': '65+ accounts have highest at-risk rate (28%) -- consider tailored outreach', 'priority': 'Medium'},
    {'category': 'Early Warning', 'finding': '842 accounts show 2+ risk signals -- prioritize for intervention', 'priority': 'High'},
    {'category': 'Product Risk', 'finding': 'Secured card holders have 35% at-risk rate -- graduation may help retention', 'priority': 'Medium'},
], st)
