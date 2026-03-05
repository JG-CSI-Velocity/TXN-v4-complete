import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, ENGAGE_PALETTE
from demo_data import migration_matrix, migration_monthly, seg_order, MONTH_LABELS
from charts import (bar_chart, grouped_bar, heatmap, stacked_bar,
                    fmt_dollar, fmt_count, action_summary)

st.header("Engagement Migration Analysis")
st.caption("6 analyses | Tier-to-tier movement, net flow, migration by segment")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Net Migration/Month", "+142", "positive")
c2.metric("Tier Stability Rate", "75.2%")
c3.metric("Power Tier Growth", "+2.1%", "+63 accts")
c4.metric("Dormant Recovery Rate", "4.2%")
st.divider()

# Migration matrix heatmap (03)
st.subheader("Tier Migration Matrix (Start -> End)")
st.plotly_chart(heatmap(
    migration_matrix.values, seg_order, seg_order,
    title='% of Starting Tier -> Ending Tier',
    text_fmt=lambda x: f'{x:.1f}%',
    colorscale=[[0, '#FFFFFF'], [0.3, '#A8DADC'], [0.5, '#457B9D'], [0.7, '#2EC4B6'], [1, '#1B2A4A']],
), use_container_width=True, theme=None)
st.info("Diagonal = stable. Above diagonal = upgrades. Below = downgrades.")

# Net flow (04)
st.subheader("Monthly Net Migration Flow")
fig = go.Figure()
fig.add_trace(go.Bar(
    x=MONTH_LABELS, y=migration_monthly['upgrades'],
    name='Upgrades', marker_color=GEN_COLORS['success'],
))
fig.add_trace(go.Bar(
    x=MONTH_LABELS, y=-migration_monthly['downgrades'],
    name='Downgrades', marker_color=GEN_COLORS['accent'],
))
fig.add_trace(go.Scatter(
    x=MONTH_LABELS, y=migration_monthly['net'],
    mode='lines+markers', name='Net Flow',
    line=dict(color=GEN_COLORS['primary'], width=3), marker=dict(size=7),
))
fig.add_hline(y=0, line_dash='dash', line_color=GEN_COLORS['muted'])
fig.update_layout(barmode='relative', height=400,
                  yaxis=dict(title='Accounts', gridcolor='#E9ECEF'),
                  margin=dict(l=50, r=20, t=20, b=40))
st.plotly_chart(fig, use_container_width=True, theme=None)

# Tier stability (stacked bar)
st.subheader("Tier Stability Rates")
stability = pd.DataFrame({
    'tier': seg_order,
    'stable': [82.0, 72.0, 70.0, 68.0, 84.0],
    'upgraded': [0, 8.0, 12.0, 12.5, 4.0],
    'downgraded': [18.0, 20.0, 18.0, 19.5, 12.0],
})
st.plotly_chart(stacked_bar(
    stability['tier'].tolist(),
    {'Stable': stability['stable'].tolist(),
     'Upgraded': stability['upgraded'].tolist(),
     'Downgraded': stability['downgraded'].tolist()},
    title='Movement Rate by Starting Tier (%)',
), use_container_width=True, theme=None)

# Migration by segment (05)
st.subheader("Migration Rates by Demographics")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['Responder', 'Non-Responder', 'Never Mailed'],
        {'Net Upgrade %': [8.2, 2.1, 1.5]},
        title='Net Migration by Campaign Status',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
        {'Net Upgrade %': [5.2, 4.8, 3.2, 1.8, -0.5, -2.1]},
        title='Net Migration by Age Band',
    ), use_container_width=True, theme=None)

st.plotly_chart(grouped_bar(
    ['Primary', 'Secondary', 'Tertiary', 'Incidental'],
    {'Net Upgrade %': [6.8, 3.2, 0.5, -3.8]},
    title='Net Migration by PFI Tier',
), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Positive Momentum', 'finding': 'Net +142 accounts/month migrating upward -- portfolio improving', 'priority': 'Low'},
    {'category': 'Campaign Impact', 'finding': 'Responders migrate 4x faster than non-responders -- campaigns driving real tier changes', 'priority': 'High'},
    {'category': 'Dormant Stickiness', 'finding': '84% of Dormant remain Dormant -- need aggressive reactivation program', 'priority': 'High'},
    {'category': 'Age Divergence', 'finding': '65+ members show net downward migration (-2.1%) -- age-specific engagement needed', 'priority': 'Medium'},
    {'category': 'Power Retention', 'finding': '18% of Power tier downgraded -- protect highest-value members', 'priority': 'High'},
], st)
