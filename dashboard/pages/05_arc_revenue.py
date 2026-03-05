import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, ARC_METADATA
from demo_data import (interchange_monthly, pin_heavy_accounts, rege_trend,
                       od_limit_dist, payroll_processors, MONTH_LABELS,
                       interchange_merchant_sig)
from charts import (bar_chart, donut_chart, trend_line, grouped_bar, waterfall,
                    heatmap, comparison_metric, fmt_dollar, fmt_count, action_summary)
from components import arc_header, headline_insight, quick_take, cross_reference, impact_box

meta = ARC_METADATA['revenue_missing']
arc_header(meta['title'], meta['subtitle'], meta['objection'], meta['reality'])

headline_insight(*meta['headline'], meta['headline_severity'])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Est. Annual IC", "$3.8M")
c2.metric("PIN-to-SIG Opportunity", "$420K")
c3.metric("Reg E Opt-In Rate", "34.2%")
c4.metric("Payroll Detection", "28.1%")

quick_take(meta['findings'])

# --- Primary Evidence ---
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(comparison_metric(
        ['Payroll Detection', 'PFI Rate', 'Reg E Opt-In'],
        [28.1, 18.4, 34.2],
        [50.0, 35.0, 55.0],
        title='You vs Industry Benchmark (%)',
        your_label='CoastHills', bench_label='Industry Avg',
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(waterfall(
        ['Current\nIC Revenue', 'PIN->SIG\nShift', 'Volume\nGrowth',
         'Rate\nImprovement', 'Potential\nTotal'],
        [3_800_000, 420_000, 180_000, 95_000, 4_495_000],
        title='Interchange Revenue Opportunity',
    ), use_container_width=True, theme=None)

cross_reference(*meta['cross_refs'][0])

st.divider()

# --- Supporting Evidence (Tabs) ---
tabs = st.tabs(["Interchange", "Reg E & Overdraft", "Payroll & PFI"])

with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SIG Ratio", "72.4%", "+10pp YoY")
    c2.metric("PIN-to-SIG Opportunity", "$420K")
    c3.metric("Avg IC/Txn", "$0.65")
    c4.metric("SIG Growth", "+10pp YoY")

    st.subheader("Monthly Interchange Revenue")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=MONTH_LABELS, y=interchange_monthly['sig_revenue'],
                         name='Signature IC', marker_color=GEN_COLORS['primary']))
    fig.add_trace(go.Bar(x=MONTH_LABELS, y=interchange_monthly['pin_revenue'],
                         name='PIN IC', marker_color=GEN_COLORS['accent']))
    fig.update_layout(barmode='stack', height=400,
                      yaxis=dict(title='Revenue ($)'))
    st.plotly_chart(fig, use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(trend_line(
            MONTH_LABELS, interchange_monthly['sig_ratio'].tolist(),
            title='Signature Ratio Trend', y_title='SIG %', color=GEN_COLORS['success'],
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(waterfall(
            ['Current\nPIN IC', 'PIN-to-SIG\nShift', 'Volume\nGrowth',
             'Rate\nImprovement', 'Potential\nTotal'],
            [1_200_000, 420_000, 180_000, 95_000, 1_895_000],
            title='PIN IC Revenue Opportunity',
        ), use_container_width=True, theme=None)

    st.plotly_chart(bar_chart(
        pin_heavy_accounts['segment'].tolist(), pin_heavy_accounts['accounts'].tolist(),
        title='PIN/SIG Account Segmentation', text_fmt=fmt_count,
        color=[GEN_COLORS['accent'], GEN_COLORS['warning'], GEN_COLORS['muted'],
               GEN_COLORS['info'], GEN_COLORS['primary']],
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grouped_bar(
            ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
            {'SIG %': [58, 65, 72, 75, 78, 82], 'PIN %': [32, 25, 20, 18, 16, 14]},
            title='PIN vs SIG by Age Band',
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(heatmap(
            interchange_merchant_sig,
            ['Amazon', 'Walmart', 'Shell', 'Starbucks', 'Target'],
            ['Platinum', 'Gold', 'Classic', 'Student', 'Secured'],
            title='SIG Ratio by Product & Merchant (%)',
        ), use_container_width=True, theme=None)

with tabs[1]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Opt-In Rate", "34.2%", "+2.8pp YoY")
    c2.metric("Opted-In Accounts", "11,356")
    c3.metric("Avg OD Limit", "$680")
    c4.metric("Revenue Exposure", "$2.4M")

    st.subheader("Opt-In Trend Over Time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=MONTH_LABELS, y=rege_trend['opted_in'], name='Opted-In',
                             fill='tozeroy', line=dict(color=GEN_COLORS['success'])))
    fig.add_trace(go.Scatter(x=MONTH_LABELS, y=rege_trend['opted_out'], name='Opted-Out',
                             fill='tozeroy', line=dict(color=GEN_COLORS['muted'])))
    fig.update_layout(height=380, yaxis=dict(title='Accounts'))
    st.plotly_chart(fig, use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(
            ['Opted-In -> Out', 'Opted-Out -> In', 'Net Change'],
            [-420, 1580, 1160],
            title='Opt-In Migration (Period)', text_fmt=lambda x: f'{x:+,}',
            color=[GEN_COLORS['accent'], GEN_COLORS['success'], GEN_COLORS['primary']],
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(bar_chart(
            od_limit_dist['limit_band'].tolist(), od_limit_dist['accounts'].tolist(),
            title='OD Limit Distribution (Opted-In)', text_fmt=fmt_count,
            color=GEN_COLORS['info'],
        ), use_container_width=True, theme=None)

    st.plotly_chart(trend_line(
        MONTH_LABELS, np.linspace(620, 680, len(MONTH_LABELS)).tolist(),
        title='Average OD Limit Over Time', y_title='Avg OD Limit ($)',
        color=GEN_COLORS['primary'],
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grouped_bar(
            ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
            {'Opt-In %': [28, 32, 38, 36, 34, 30]},
            title='Opt-In Rate by Age Band',
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(grouped_bar(
            ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
            {'Opt-In %': [48, 42, 35, 28, 15]},
            title='Opt-In Rate by Engagement Tier',
        ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(
            ['Current Revenue', 'If 50% Opt-In', 'If 75% Opt-In'],
            [2_400_000, 3_500_000, 5_250_000],
            title='OD Revenue Scenarios', text_fmt=fmt_dollar,
            color=[GEN_COLORS['primary'], GEN_COLORS['info'], GEN_COLORS['success']],
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(grouped_bar(
            ['$0-500', '$500-2K', '$2K-5K', '$5K-10K', '$10K+'],
            {'Opt-In %': [42, 38, 32, 28, 22], 'Avg Usage %': [52, 35, 22, 15, 8]},
            title='Opt-In & Usage by Balance Band',
        ), use_container_width=True, theme=None)

with tabs[2]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accounts w/ Payroll", "9,340", "28.1%")
    c2.metric("Avg Deposit", "$2,480/mo")
    c3.metric("Primary PFI %", "18.4%")
    c4.metric("Industry Benchmark", "50%")

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

    st.plotly_chart(grouped_bar(
        ['Has Payroll', 'No Payroll'],
        {'Avg Monthly Spend': [1420, 680],
         'Avg Balance ($K)': [8.4, 3.2],
         'Avg Txns': [42, 22]},
        title='Payroll vs Non-Payroll Account Metrics',
    ), use_container_width=True, theme=None)

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

    st.plotly_chart(bar_chart(
        payroll_processors['processor'][::-1].tolist(),
        payroll_processors['accounts'][::-1].tolist(),
        text_fmt=fmt_count, horizontal=True, height=380, color=GEN_COLORS['primary'],
    ), use_container_width=True, theme=None)

    st.plotly_chart(grouped_bar(
        ['Active', 'Cooling', 'Dormant', 'Closed'],
        {'With Payroll': [88, 8, 3, 1], 'Without Payroll': [68, 15, 12, 5]},
        title='Health Status: Payroll vs Non-Payroll (%)',
    ), use_container_width=True, theme=None)

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
impact_box(meta['impacts'])
st.divider()
st.subheader("Key Findings & Actions")
action_summary(meta['findings'], st)
