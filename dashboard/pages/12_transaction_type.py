import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import txn_type_split, MONTH_LABELS
from charts import bar_chart, donut_chart, grouped_bar, trend_line, stacked_bar, fmt_dollar, fmt_count, action_summary
import plotly.graph_objects as go

st.header("Transaction Type Analysis")
st.caption("8 analyses | PIN vs signature, transaction type distribution")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Signature Share", "47.6%")
c2.metric("PIN Share", "20.4%")
c3.metric("Contactless Growth", "+28%")
c4.metric("Online Share", "13.9%", "+4.1%")
st.divider()

# Split (03)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        txn_type_split['type'].tolist(), txn_type_split['txn_count'].tolist(),
        title='Transaction Count by Type', text_fmt=fmt_count,
        color=[GEN_COLORS['primary'], GEN_COLORS['accent'], GEN_COLORS['success'],
               GEN_COLORS['info'], GEN_COLORS['warning']],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(donut_chart(
        txn_type_split['type'], txn_type_split['total_spend'],
        title='Spend by Transaction Type',
        colors=[GEN_COLORS['primary'], GEN_COLORS['accent'], GEN_COLORS['success'],
                GEN_COLORS['info'], GEN_COLORS['warning']],
    ), use_container_width=True, theme=None)

# By merchant (04) + Trend (05)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        ['Amazon', 'Walmart', 'Target', 'Shell', 'Starbucks'],
        {'Signature': [85, 42, 68, 12, 72],
         'PIN': [8, 45, 22, 78, 5],
         'Contactless': [5, 10, 8, 8, 20]},
        title='Transaction Type by Top Merchants (%)',
    ), use_container_width=True, theme=None)
with col2:
    fig = go.Figure()
    for typ, col in [('Signature', GEN_COLORS['primary']), ('PIN', GEN_COLORS['accent']),
                     ('Contactless', GEN_COLORS['success']), ('Online', GEN_COLORS['info'])]:
        fig.add_trace(go.Scatter(x=MONTH_LABELS,
                                 y=np.random.normal(100, 3, len(MONTH_LABELS)).cumsum() / 10 + 90,
                                 mode='lines', name=typ, line=dict(color=col)))
    fig.update_layout(title='Type Share Trend', height=380,
                      yaxis=dict(gridcolor='#E9ECEF'), margin=dict(l=50, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True, theme=None)

# By bracket (06) + age (07)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(stacked_bar(
        ['< $10', '$10-50', '$50-100', '$100-500', '$500+'],
        {'Signature': [35, 48, 52, 58, 65],
         'PIN': [40, 28, 22, 18, 12],
         'Other': [25, 24, 26, 24, 23]},
        title='Type Mix by Spend Bracket (%)',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(stacked_bar(
        ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
        {'Signature': [38, 42, 48, 52, 55, 58],
         'PIN': [22, 20, 22, 25, 28, 30],
         'Contactless': [25, 22, 18, 12, 8, 5],
         'Online': [15, 16, 12, 11, 9, 7]},
        title='Type Mix by Age Band (%)',
    ), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'SIG Ratio', 'finding': 'Signature at 47.6% -- room to grow for interchange optimization', 'priority': 'Medium'},
    {'category': 'Contactless', 'finding': 'Contactless growing 28% YoY, strongest in 18-35 age band', 'priority': 'Low'},
    {'category': 'PIN Heavy', 'finding': '20.4% PIN -- gas stations and grocery drive PIN usage', 'priority': 'Medium'},
    {'category': 'Online Growth', 'finding': 'Online transactions 13.9% and growing -- digital card features opportunity', 'priority': 'Low'},
], st)
