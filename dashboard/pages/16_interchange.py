import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import interchange_monthly, pin_heavy_accounts, MONTH_LABELS
from charts import (bar_chart, donut_chart, grouped_bar, trend_line, waterfall,
                    heatmap, fmt_dollar, fmt_count, action_summary)
import plotly.graph_objects as go

st.header("Interchange Revenue Analysis")
st.caption("10 analyses | PIN/signature interchange, revenue waterfall, opportunity gap")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Est. Annual IC", "$3.8M")
c2.metric("SIG Ratio", "72.4%", "+10pp YoY")
c3.metric("PIN-to-SIG Opportunity", "$420K")
c4.metric("Avg IC/Txn", "$0.65")
st.divider()

# PIN/SIG trend (03)
st.subheader("Monthly Interchange Revenue")
fig = go.Figure()
fig.add_trace(go.Bar(x=MONTH_LABELS, y=interchange_monthly['sig_revenue'],
                     name='Signature IC', marker_color=GEN_COLORS['primary']))
fig.add_trace(go.Bar(x=MONTH_LABELS, y=interchange_monthly['pin_revenue'],
                     name='PIN IC', marker_color=GEN_COLORS['accent']))
fig.update_layout(barmode='stack', height=400,
                  yaxis=dict(gridcolor='#E9ECEF', title='Revenue ($)'),
                  margin=dict(l=50, r=20, t=20, b=40))
st.plotly_chart(fig, use_container_width=True, theme=None)

# SIG ratio trend (04)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(trend_line(
        MONTH_LABELS, interchange_monthly['sig_ratio'].tolist(),
        title='Signature Ratio Trend', y_title='SIG %', color=GEN_COLORS['success'],
    ), use_container_width=True, theme=None)

# Revenue waterfall (05)
with col2:
    st.plotly_chart(waterfall(
        ['Current\nPIN IC', 'PIN-to-SIG\nShift', 'Volume\nGrowth',
         'Rate\nImprovement', 'Potential\nTotal'],
        [1_200_000, 420_000, 180_000, 95_000, 1_895_000],
        title='Interchange Revenue Opportunity',
    ), use_container_width=True, theme=None)

# PIN heavy accounts (06)
st.subheader("PIN/SIG Account Segmentation")
st.plotly_chart(bar_chart(
    pin_heavy_accounts['segment'].tolist(), pin_heavy_accounts['accounts'].tolist(),
    text_fmt=fmt_count,
    color=[GEN_COLORS['accent'], GEN_COLORS['warning'], GEN_COLORS['muted'],
           GEN_COLORS['info'], GEN_COLORS['primary']],
), use_container_width=True, theme=None)

# By demographics (07) + merchant (08) + product (09)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
        {'SIG %': [58, 65, 72, 75, 78, 82], 'PIN %': [32, 25, 20, 18, 16, 14]},
        title='PIN vs SIG by Age Band',
    ), use_container_width=True, theme=None)
with col2:
    _merch_sig = np.random.uniform(30, 95, (5, 5))
    st.plotly_chart(heatmap(
        _merch_sig, ['Amazon', 'Walmart', 'Shell', 'Starbucks', 'Target'],
        ['Platinum', 'Gold', 'Classic', 'Student', 'Secured'],
        title='SIG Ratio by Product & Merchant (%)',
    ), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'SIG Growth', 'finding': 'SIG ratio improved 10pp YoY to 72.4% -- positive interchange trend', 'priority': 'Low'},
    {'category': 'PIN Opportunity', 'finding': '$420K annual opportunity from shifting PIN-heavy accounts to signature', 'priority': 'High'},
    {'category': 'Gas Stations', 'finding': 'Gas stations drive 62% of PIN volume -- contactless/tap promotion opportunity', 'priority': 'Medium'},
    {'category': 'Young Members', 'finding': '18-25 age band has lowest SIG ratio (58%) -- education/default routing', 'priority': 'Medium'},
], st)
