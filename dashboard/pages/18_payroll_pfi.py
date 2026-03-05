import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import payroll_processors, MONTH_LABELS
from charts import (bar_chart, donut_chart, grouped_bar, scatter_plot, trend_line,
                    fmt_dollar, fmt_count, action_summary)

st.header("Payroll & PFI Analysis")
st.caption("10 analyses | Payroll detection, processor analysis, PFI composite scoring")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Accounts w/ Payroll", "9,340", "28.1%")
c2.metric("Avg Deposit", "$2,480/mo")
c3.metric("Monthly Frequency", "62%")
c4.metric("Primary PFI %", "18.4%")
st.divider()

# Distribution (03)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(donut_chart(
        ['Has Payroll', 'No Payroll'], [9340, 23865],
        title='Payroll Detection', colors=[GEN_COLORS['success'], GEN_COLORS['muted']],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(donut_chart(
        ['Monthly', 'Biweekly', 'Irregular'], [5831, 3549, 960],
        title='Payroll Frequency Distribution',
    ), use_container_width=True, theme=None)

# Value (04)
st.subheader("Payroll Account Value")
st.plotly_chart(grouped_bar(
    ['Has Payroll', 'No Payroll'],
    {'Avg Monthly Spend': [1420, 680],
     'Avg Balance ($K)': [8.4, 3.2],
     'Avg Txns': [42, 22]},
    title='Payroll vs Non-Payroll Account Metrics',
), use_container_width=True, theme=None)

# By demographics (05)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
        [18, 32, 38, 35, 28, 12],
        title='Payroll Detection Rate by Age', text_fmt=lambda x: f'{x}%',
        color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
        {'Payroll %': [52, 42, 28, 15, 5]},
        title='Payroll Rate by Engagement Tier',
    ), use_container_width=True, theme=None)

# Processors (06)
st.subheader("Payroll Processor Distribution")
st.plotly_chart(bar_chart(
    payroll_processors['processor'][::-1].tolist(),
    payroll_processors['accounts'][::-1].tolist(),
    text_fmt=fmt_count, horizontal=True, height=380,
    color=GEN_COLORS['primary'],
), use_container_width=True, theme=None)

# Retention (07)
st.subheader("Payroll Impact on Retention")
st.plotly_chart(grouped_bar(
    ['Active', 'Cooling', 'Dormant', 'Closed'],
    {'With Payroll': [88, 8, 3, 1], 'Without Payroll': [68, 15, 12, 5]},
    title='Health Status: Payroll vs Non-Payroll (%)',
), use_container_width=True, theme=None)

# PFI composite (08) + vs competitor (09)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(donut_chart(
        ['Primary', 'Secondary', 'Tertiary', 'Incidental'],
        [6100, 8400, 9200, 9505],
        title='PFI Tier Distribution',
        colors=[GEN_COLORS['success'], GEN_COLORS['info'], GEN_COLORS['warning'], GEN_COLORS['muted']],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        ['Primary', 'Secondary', 'Tertiary', 'Incidental'],
        {'Has Payroll %': [65, 32, 18, 8],
         'Competitor Activity %': [18, 42, 62, 82]},
        title='PFI Tier: Payroll & Competition',
    ), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'PFI Gap', 'finding': 'Only 18.4% primary PFI -- payroll/DD capture is key to deepening relationships', 'priority': 'High'},
    {'category': 'Retention Impact', 'finding': 'Payroll accounts are 5x less likely to close (1% vs 5%)', 'priority': 'High'},
    {'category': 'ADP Dominance', 'finding': 'ADP = 30% of detected payroll -- partnership opportunity', 'priority': 'Medium'},
    {'category': 'Age Gap', 'finding': '65+ age band only 12% payroll detection -- many may be retired/pension', 'priority': 'Low'},
    {'category': 'Spend Multiplier', 'finding': 'Payroll accounts spend 2.1x more and hold 2.6x higher balances', 'priority': 'Low'},
], st)
