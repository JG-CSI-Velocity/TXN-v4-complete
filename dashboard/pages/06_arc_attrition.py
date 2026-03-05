import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, ARC_METADATA
from demo_data import (attrition_tiers, balance_bands, pfi_tiers,
                       retention_funnel, retention_by_tier, MONTH_LABELS,
                       sankey_sources, sankey_targets, sankey_values, sankey_labels)
from charts import (bar_chart, donut_chart, trend_line, grouped_bar, scatter_plot,
                    stacked_bar, waterfall, funnel_horizontal, heatmap, sankey_flow,
                    fmt_dollar, fmt_count, action_summary)
from components import arc_header, headline_insight, quick_take, cross_reference, impact_box

meta = ARC_METADATA['attrition_cascade']
arc_header(meta['title'], meta['subtitle'], meta['objection'], meta['reality'])

headline_insight(*meta['headline'], meta['headline_severity'])

c1, c2, c3, c4 = st.columns(4)
c1.metric("At-Risk Accounts", "6,082", "18.3%")
c2.metric("Annual Spend at Risk", "$6.1M")
c3.metric("Closed Account Loss", "$12M/yr")
c4.metric("Dormant Residual", "$2.1M")

quick_take(meta['findings'])

# --- Primary Evidence ---
st.subheader("The Attrition Cascade")
st.caption("How accounts flow from active to closed -- and where to intervene")
st.plotly_chart(sankey_flow(
    sankey_labels, sankey_sources, sankey_targets, sankey_values,
    title='Account Health Flow',
), use_container_width=True, theme=None)

cross_reference(*meta['cross_refs'][0])

st.divider()

# --- Supporting Evidence (Tabs) ---
tabs = st.tabs(["Attrition Risk", "Balance & Flight", "Retention & Churn"])

with tabs[0]:
    st.subheader("Risk Tier Distribution")
    st.plotly_chart(bar_chart(
        attrition_tiers['tier'].tolist(), attrition_tiers['accounts'].tolist(),
        text_fmt=lambda x: f'{x:,.0f}',
        color=['#2EC4B6', '#FF9F1C', '#E76F51', '#E63946'],
    ), use_container_width=True, theme=None)

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

    st.subheader("Monthly Risk Tier Progression")
    _months_data = {}
    for tier, base in [('Stable', 22000), ('Slowing', 5000), ('Declining', 2500), ('Dormant', 3000)]:
        _months_data[tier] = (np.array([base] * len(MONTH_LABELS)) +
                              np.random.randint(-200, 200, len(MONTH_LABELS))).tolist()
    st.plotly_chart(stacked_bar(MONTH_LABELS, _months_data,
                                title='Risk Tier Composition Over Time'), use_container_width=True, theme=None)

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

    st.subheader("Early Warning: 2+ Risk Signals")
    np.random.seed(42)
    st.dataframe(pd.DataFrame({
        'Account': [f'***{np.random.randint(1000,9999)}' for _ in range(8)],
        'Tier': np.random.choice(['Heavy', 'Moderate', 'Power'], 8),
        'Velocity': np.random.uniform(0.1, 0.5, 8).round(2),
        'Months Declining': np.random.randint(2, 6, 8),
        'Competitor?': np.random.choice(['Yes', 'No'], 8, p=[0.6, 0.4]),
        'Est. Annual Spend': np.random.randint(2000, 15000, 8),
    }).style.format({'Velocity': '{:.2f}', 'Est. Annual Spend': '${:,}'}),
        use_container_width=True, hide_index=True)

    st.subheader("Dormancy Progression Funnel")
    st.plotly_chart(funnel_horizontal(
        ['Active', 'Slowing', 'Declining', 'Dormant'],
        [21480, 5643, 2840, 3242],
        ['#2EC4B6', '#FF9F1C', '#E76F51', '#E63946'],
    ), use_container_width=True, theme=None)

with tabs[1]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Deposits", "$277.8M")
    c2.metric("Avg Balance", "$8,363")
    c3.metric("% Zero-Balance", "8.2%")
    c4.metric("% Primary PFI", "18.4%")

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

    st.subheader("Balance vs Spend Activity")
    np.random.seed(42)
    _bal2 = np.random.lognormal(7.5, 1.5, 400).clip(100, 100_000)
    _spend2 = np.random.lognormal(6, 1.2, 400).clip(50, 20_000)
    fig = scatter_plot(_bal2, _spend2, x_title='Current Balance ($)', y_title='Monthly Spend ($)')
    fig.update_xaxes(type='log')
    fig.update_yaxes(type='log')
    st.plotly_chart(fig, use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(
            ['Low Risk', 'Watch', 'At Risk', 'Critical'],
            [18200, 6800, 5200, 3005],
            title='Deposit Flight Risk Classification', text_fmt=fmt_count,
            color=[GEN_COLORS['success'], GEN_COLORS['info'], GEN_COLORS['warning'], GEN_COLORS['accent']],
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(grouped_bar(
            ['18-35', '36-55', '56+'],
            {'Avg Balance': [3200, 8400, 12800], 'Avg Spend': [580, 920, 680]},
            title='Balance & Spend by Age Group',
        ), use_container_width=True, theme=None)

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

    st.plotly_chart(grouped_bar(
        ['Primary', 'Secondary', 'Tertiary', 'Incidental'],
        {'No Competitor': [72, 48, 32, 18],
         '1+ Competitor': [28, 52, 68, 82]},
        title='Competitor Activity by PFI Tier (%)',
    ), use_container_width=True, theme=None)

with tabs[2]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Closed Account Rate", "3.8%")
    c2.metric("Avg Tenure at Close", "4.2 yrs")
    c3.metric("At-Risk Pipeline", "7,750")
    c4.metric("Annual Spend at Risk", "$6.1M")

    st.subheader("Account Health Funnel")
    st.plotly_chart(funnel_horizontal(
        retention_funnel['status'].tolist(), retention_funnel['accounts'].tolist(),
        retention_funnel['color'].tolist(),
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(
            retention_funnel['status'].tolist(), retention_funnel['accounts'].tolist(),
            title='Accounts by Health Status', text_fmt=fmt_count,
            color=retention_funnel['color'].tolist(),
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(bar_chart(
            retention_funnel['status'].tolist(), retention_funnel['annual_spend'].tolist(),
            title='Annual Spend by Status', text_fmt=fmt_dollar,
            color=retention_funnel['color'].tolist(),
        ), use_container_width=True, theme=None)

    st.plotly_chart(bar_chart(
        retention_by_tier['tier'].tolist(), retention_by_tier['churn_rate'].tolist(),
        title='Closed Account Rate by Tier', text_fmt=lambda x: f'{x:.1f}%',
        color=[GEN_COLORS['accent'], GEN_COLORS['warning'], GEN_COLORS['info'],
               GEN_COLORS['muted'], GEN_COLORS['muted']],
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grouped_bar(
            ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
            {'Churn Rate %': [5.2, 3.1, 2.8, 3.5, 4.2, 6.8]},
            title='Churn Rate by Age Band',
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(grouped_bar(
            ['Primary', 'Secondary', 'Tertiary', 'Incidental'],
            {'Churn Rate %': [1.2, 3.5, 5.8, 8.2]},
            title='Churn Rate by PFI Tier',
        ), use_container_width=True, theme=None)

    st.plotly_chart(waterfall(
        ['Retained\nRevenue', 'At-Risk\nRevenue', 'Cooling\nRevenue', 'Lost\n(Closed)',
         'Net Portfolio\nRevenue'],
        [380_000_000, -28_000_000, -2_100_000, -12_000_000, 337_900_000],
        title='Revenue Waterfall: Retention Impact',
    ), use_container_width=True, theme=None)

    st.subheader("Early Warning Signals")
    np.random.seed(42)
    st.dataframe(pd.DataFrame({
        'Account': [f'***{np.random.randint(1000,9999)}' for _ in range(10)],
        'Tier': np.random.choice(['Power', 'Heavy', 'Moderate'], 10),
        'Status': np.random.choice(['Declining', 'Cooling'], 10, p=[0.4, 0.6]),
        'Months Declining': np.random.randint(2, 6, 10),
        'Balance Trend': np.random.choice(['Falling', 'Stable', 'Rising'], 10, p=[0.5, 0.3, 0.2]),
        'Competitor?': np.random.choice(['Yes', 'No'], 10, p=[0.6, 0.4]),
        'Est. Annual Spend': np.random.randint(3000, 18000, 10),
    }).style.format({'Est. Annual Spend': '${:,}'}),
        use_container_width=True, hide_index=True)

st.divider()
impact_box(meta['impacts'])
st.divider()
st.subheader("Key Findings & Actions")
action_summary(meta['findings'], st)
