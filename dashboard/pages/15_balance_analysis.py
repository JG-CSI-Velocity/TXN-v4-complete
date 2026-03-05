import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import balance_bands, pfi_tiers, MONTH_LABELS
from charts import (bar_chart, donut_chart, grouped_bar, scatter_plot, trend_line,
                    fmt_dollar, fmt_count, action_summary)

st.header("Balance Analysis")
st.caption("10 analyses | Balance bands, trends, PFI scoring, flight risk")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Deposits", "$277.8M")
c2.metric("Avg Balance", "$8,363")
c3.metric("% Zero-Balance", "8.2%")
c4.metric("% Primary PFI", "18.4%")
st.divider()

# Distribution (03) + Bands bar (04)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        balance_bands['band'].tolist(), balance_bands['accounts'].tolist(),
        title='Accounts by Balance Band', text_fmt=fmt_count,
        color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        balance_bands['band'].tolist(), (balance_bands['total_balance'] * 1_000_000).tolist(),
        title='Total Balance by Band', text_fmt=fmt_dollar,
        color=GEN_COLORS['primary'],
    ), use_container_width=True, theme=None)

# Balance vs activity (05)
st.subheader("Balance vs Spend Activity")
np.random.seed(42)
_bal = np.random.lognormal(7.5, 1.5, 400).clip(100, 100_000)
_spend = np.random.lognormal(6, 1.2, 400).clip(50, 20_000)
fig = scatter_plot(_bal, _spend, x_title='Current Balance ($)', y_title='Monthly Spend ($)')
fig.update_xaxes(type='log')
fig.update_yaxes(type='log')
st.plotly_chart(fig, use_container_width=True, theme=None)

# Deposit flight risk (06)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        ['Low Risk', 'Watch', 'At Risk', 'Critical'],
        [18200, 6800, 5200, 3005],
        title='Deposit Flight Risk Classification', text_fmt=fmt_count,
        color=[GEN_COLORS['success'], GEN_COLORS['info'], GEN_COLORS['warning'], GEN_COLORS['accent']],
    ), use_container_width=True, theme=None)

# Demographics (07)
with col2:
    st.plotly_chart(grouped_bar(
        ['18-35', '36-55', '56+'],
        {'Avg Balance': [3200, 8400, 12800], 'Avg Spend': [580, 920, 680]},
        title='Balance & Spend by Age Group',
    ), use_container_width=True, theme=None)

# PFI scoring (08)
st.subheader("PFI (Primary Financial Institution) Tiers")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(donut_chart(
        pfi_tiers['tier'], pfi_tiers['accounts'],
        title='Accounts by PFI Tier',
        colors=[GEN_COLORS['success'], GEN_COLORS['info'], GEN_COLORS['warning'], GEN_COLORS['muted']],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(grouped_bar(
        pfi_tiers['tier'].tolist(),
        {'Avg Balance ($K)': (pfi_tiers['avg_balance'] / 1000).tolist(),
         'Avg Spend ($100)': (pfi_tiers['avg_spend'] / 100).tolist()},
        title='PFI Tier Profile',
    ), use_container_width=True, theme=None)

# Balance vs competitor (09)
st.plotly_chart(grouped_bar(
    ['Primary', 'Secondary', 'Tertiary', 'Incidental'],
    {'No Competitor': [72, 48, 32, 18],
     '1+ Competitor': [28, 52, 68, 82]},
    title='Competitor Activity by PFI Tier (%)',
), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Zero Balance', 'finding': '8.2% of accounts have zero balance -- reactivation opportunity', 'priority': 'Medium'},
    {'category': 'PFI Gap', 'finding': 'Only 18.4% are primary PFI -- 81.6% have deeper relationship elsewhere', 'priority': 'High'},
    {'category': 'Flight Risk', 'finding': '8,205 accounts classified as At Risk or Critical for deposit flight', 'priority': 'High'},
    {'category': 'High Balance', 'finding': '$50K+ accounts = 3% of portfolio but 30% of deposits -- retention priority', 'priority': 'High'},
], st)
