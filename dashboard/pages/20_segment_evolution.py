import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, ENGAGE_PALETTE
from demo_data import seg_order, seg_migration, seg_net_flow, MONTH_LABELS
from charts import (bar_chart, grouped_bar, heatmap, stacked_bar, trend_line,
                    fmt_dollar, fmt_count, action_summary)
import plotly.graph_objects as go

st.header("Segment Evolution Analysis")
st.caption("8 analyses | Bimonthly segmentation migration, campaign segment impact")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Upgrade:Degrade Ratio", "1.4:1")
c2.metric("% Upgraded", "12.3%")
c3.metric("% Degraded", "8.7%")
c4.metric("% Stable", "79.0%")
st.divider()

# Distribution (03)
st.subheader("Current Segment Distribution")
_seg_counts = [2987, 5640, 9300, 10120, 5158]
st.plotly_chart(bar_chart(
    seg_order, _seg_counts, text_fmt=fmt_count,
    color=[ENGAGE_PALETTE[s] for s in seg_order],
), use_container_width=True, theme=None)

# Migration matrix (04)
st.subheader("Segment Migration Matrix")
st.plotly_chart(heatmap(
    seg_migration, seg_order, seg_order,
    title='Starting Tier -> Ending Tier (%)',
    text_fmt=lambda x: f'{x:.1f}%',
    colorscale=[[0, '#FFFFFF'], [0.3, '#A8DADC'], [0.5, '#457B9D'], [0.7, '#2EC4B6'], [1, '#1B2A4A']],
), use_container_width=True, theme=None)
st.info("Diagonal = stable. Above diagonal = upgrades. Below = downgrades.")

# Upgraders vs degraders (05)
st.subheader("Net Migration by Segment")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        seg_net_flow['segment'].tolist(),
        {'Upgraded': seg_net_flow['upgraded'].tolist(),
         'Degraded': seg_net_flow['degraded'].tolist()},
        title='Upgraders vs Degraders by Starting Segment',
    ), use_container_width=True, theme=None)
with col2:
    _net_colors = [GEN_COLORS['success'] if n > 0 else GEN_COLORS['accent'] for n in seg_net_flow['net']]
    st.plotly_chart(bar_chart(
        seg_net_flow['segment'].tolist(), seg_net_flow['net_pct'].tolist(),
        title='Net Flow (%)', text_fmt=lambda x: f'{x:+.1f}%', color=_net_colors,
    ), use_container_width=True, theme=None)

# Segment vs campaign (06)
st.subheader("Campaign Impact on Segment Migration")
st.plotly_chart(grouped_bar(
    seg_order,
    {'Responder Upgrade %': [0, 12, 18, 15, 6],
     'Non-Responder Upgrade %': [0, 6, 10, 8, 3],
     'Never Mailed Upgrade %': [0, 5, 8, 7, 2]},
    title='Upgrade Rate by Campaign Status',
), use_container_width=True, theme=None)

# Prediction (07)
st.subheader("Segment Projection (Next 6 Months)")
fig = go.Figure()
months_proj = [f'Month {i}' for i in range(1, 7)]
for seg, base in zip(seg_order, _seg_counts):
    _proj = np.array([base] * 6) + np.cumsum(np.random.randint(-50, 80, 6))
    fig.add_trace(go.Scatter(x=months_proj, y=_proj.tolist(), mode='lines',
                             name=seg, line=dict(color=ENGAGE_PALETTE[seg])))
fig.update_layout(height=380, yaxis=dict(gridcolor='#E9ECEF'),
                  margin=dict(l=50, r=20, t=20, b=40))
st.plotly_chart(fig, use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Portfolio Health', 'finding': 'Upgrade:degrade ratio 1.4:1 -- moderate positive momentum', 'priority': 'Medium'},
    {'category': 'Campaign Effect', 'finding': 'Responders upgrade 2x more than non-responders -- campaigns driving real tier movement', 'priority': 'High'},
    {'category': 'Light Tier Risk', 'finding': 'Light tier has 16.5% degradation rate -- target for retention', 'priority': 'High'},
    {'category': 'Dormant Recovery', 'finding': 'Only 4% of Dormant upgrade -- different intervention needed', 'priority': 'Medium'},
], st)
