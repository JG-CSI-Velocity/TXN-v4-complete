import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, ENGAGE_PALETTE, ARC_METADATA
from demo_data import (competitor_data, comp_by_segment, finsvc_categories,
                       finsvc_top_merchants, ics_channels, MONTH_LABELS,
                       competitor_monthly_trend, competitor_segment_heatmap,
                       finsvc_recency_heatmap, finsvc_monthly_trend,
                       finsvc_leakage, finsvc_biz_personal, ics_monthly_trend)
from charts import (bar_chart, donut_chart, trend_line, grouped_bar, heatmap,
                    scatter_plot, bubble_chart, waterfall, fmt_dollar, fmt_count,
                    action_summary)
from components import arc_header, headline_insight, quick_take, cross_reference, impact_box

meta = ARC_METADATA['loyalty_myth']
arc_header(meta['title'], meta['subtitle'], meta['objection'], meta['reality'])

headline_insight(*meta['headline'], meta['headline_severity'])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Accounts w/ Competitors", "18,420", "55.5%")
c2.metric("Top Competitor", "Chase", "8,200 accts")
c3.metric("FinSvc Leakage", "$78.1M")
c4.metric("ICS 90-Day Retention", "74.8%")

quick_take(meta['findings'])

# --- Primary Evidence ---
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        competitor_data['competitor'].tolist(), competitor_data['accounts_using'].tolist(),
        title='Competitor Penetration (accounts)', text_fmt=fmt_count,
        color=[GEN_COLORS['accent'] if i == 0 else GEN_COLORS['info'] for i in range(len(competitor_data))],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        ['Apple Card', 'PayPal', 'Venmo', 'Cash App', 'Chime'],
        [2400, 3800, 2200, 1800, 1200],
        title='Non-Bank/Fintech Threats (accounts)', text_fmt=fmt_count,
        color=GEN_COLORS['warning'],
    ), use_container_width=True, theme=None)

for cr in meta['cross_refs']:
    cross_reference(*cr)

st.divider()

# --- Supporting Evidence (Tabs) ---
tabs = st.tabs(["Competition", "Financial Services", "ICS Acquisition"])

with tabs[0]:
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

    st.subheader("Competitor Activity Trend")
    fig = go.Figure()
    for comp in ['Chase', 'Bank of America', 'Capital One']:
        if comp in competitor_monthly_trend.columns:
            fig.add_trace(go.Scatter(x=MONTH_LABELS, y=competitor_monthly_trend[comp],
                                     mode='lines', name=comp))
    fig.update_layout(height=380, title='Competitor Account Trend')
    st.plotly_chart(fig, use_container_width=True, theme=None)

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

    st.plotly_chart(heatmap(
        competitor_segment_heatmap,
        ['Chase', 'BofA', 'WF', 'CapOne', 'Citi'],
        ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
        title='Competitor Penetration by Segment (%)',
    ), use_container_width=True, theme=None)

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

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(
            ['Chase Sapphire', 'Amex Gold', 'CapOne Venture', 'Citi Double Cash'],
            [3200, 1800, 2400, 1500],
            title='Material Product Threats (accounts)', text_fmt=fmt_count,
            color=GEN_COLORS['accent'],
        ), use_container_width=True, theme=None)
    with col2:
        st.multiselect("Configure Competitors", competitor_data['competitor'].tolist(),
                       default=competitor_data['competitor'].tolist())

with tabs[1]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accounts Using FinSvc", "24,800", "74.7%")
    c2.metric("Total FinSvc Spend", "$78.1M")
    c3.metric("Avg Monthly/Acct", "$262")
    c4.metric("Multi-Category Users", "42.3%")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(
            finsvc_categories['category'].tolist(), finsvc_categories['accounts'].tolist(),
            title='Accounts by FinSvc Category', text_fmt=fmt_count,
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(donut_chart(
            finsvc_categories['category'], finsvc_categories['total_spend'],
            title='Spend by FinSvc Category',
        ), use_container_width=True, theme=None)

    st.plotly_chart(bar_chart(
        finsvc_top_merchants['merchant'][::-1].tolist(),
        finsvc_top_merchants['accounts'][::-1].tolist(),
        text_fmt=fmt_count, horizontal=True, height=400, color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)

    st.plotly_chart(heatmap(
        finsvc_recency_heatmap, ['<30d', '30-90d', '90-180d', '180d+'],
        finsvc_categories['category'].tolist(),
        title='% of Accounts by Recency',
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        for cat in ['Banking/ATM', 'Insurance', 'Investment', 'Lending']:
            if cat in finsvc_monthly_trend.columns:
                fig.add_trace(go.Scatter(x=MONTH_LABELS, y=finsvc_monthly_trend[cat],
                                         mode='lines', name=cat))
        fig.update_layout(title='FinSvc Category Trends', height=380)
        st.plotly_chart(fig, use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(bar_chart(
            ['1 category', '2 categories', '3 categories', '4+'],
            [14400, 6200, 2800, 1400],
            title='Multi-Category Usage', text_fmt=fmt_count, color=GEN_COLORS['success'],
        ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(
            ['Bank+Insurance', 'Bank+Invest', 'Insurance+Tax', 'Bank+Lending', 'Full Suite'],
            [8400, 4200, 1800, 2400, 800],
            title='Most Common Category Pairs', text_fmt=fmt_count,
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(bar_chart(
            finsvc_leakage['category'].tolist(),
            finsvc_leakage['leakage_pct'].tolist(),
            title='Leakage Intensity (% using competitor FinSvc)',
            text_fmt=lambda x: f'{x:.0f}%', color=GEN_COLORS['accent'],
        ), use_container_width=True, theme=None)

    st.plotly_chart(grouped_bar(
        finsvc_biz_personal['category'].tolist(),
        {'Personal ($M)': finsvc_biz_personal['personal'].tolist(),
         'Business ($M)': finsvc_biz_personal['business'].tolist()},
        title='FinSvc Spend: Business vs Personal',
    ), use_container_width=True, theme=None)

    st.plotly_chart(waterfall(
        ['Current FinSvc\nRevenue', 'Cross-sell\nInsurance', 'Capture\nInvestment',
         'Reduce\nLeakage', 'New Lending', 'Potential\nTotal'],
        [78_100_000, 12_000_000, 8_500_000, 15_000_000, 6_200_000, 119_800_000],
        title='Financial Services Revenue Opportunity',
    ), use_container_width=True, theme=None)

with tabs[2]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("New Accounts (ICS)", "12,400")
    c2.metric("Best Channel", "Branch Referral", "78% activation")
    c3.metric("Avg 1st Month Spend", "$348")
    c4.metric("90-Day Retention", "74.8%")

    st.plotly_chart(bar_chart(
        ics_channels['channel'].tolist(), ics_channels['accounts'].tolist(),
        title='Accounts by Channel', text_fmt=fmt_count,
        color=[GEN_COLORS['primary'], GEN_COLORS['info'], GEN_COLORS['warning'],
               GEN_COLORS['muted'], GEN_COLORS['success']],
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grouped_bar(
            ics_channels['channel'].tolist(),
            {'Activation %': ics_channels['activation_rate'].tolist(),
             '90d Retention %': ics_channels['90day_retention'].tolist()},
            title='Channel Quality Metrics',
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(bar_chart(
            ics_channels['channel'].tolist(), ics_channels['avg_first_month_spend'].tolist(),
            title='Avg First Month Spend by Channel', text_fmt=fmt_dollar,
            color=GEN_COLORS['success'],
        ), use_container_width=True, theme=None)

    fig = go.Figure()
    for ch in ['Branch Referral', 'Online Application', 'Direct Mail']:
        if ch in ics_monthly_trend.columns:
            fig.add_trace(go.Scatter(x=MONTH_LABELS, y=ics_monthly_trend[ch],
                                     mode='lines+markers', name=ch))
    fig.update_layout(height=380, title='Monthly Acquisition Trend')
    st.plotly_chart(fig, use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(donut_chart(
            ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
            [5, 12, 28, 35, 20],
            title='ICS Account Engagement Distribution',
        ), use_container_width=True, theme=None)
    with col2:
        _retention = [100, 88, 82, 78, 75, 72, 70, 68, 66, 65, 64, 63]
        st.plotly_chart(trend_line(
            [f'Month {m}' for m in range(1, 13)], _retention,
            title='ICS Cohort Retention Curve', y_title='% Still Active',
            color=GEN_COLORS['accent'],
        ), use_container_width=True, theme=None)

    st.plotly_chart(grouped_bar(
        ['Avg Spend', 'Avg Txns', 'Merchants Used', 'Competitor %'],
        {'ICS Accounts': [420, 18, 8, 35], 'Portfolio Avg': [950, 32, 18, 55]},
        title='ICS Performance Gap',
    ), use_container_width=True, theme=None)

st.divider()
impact_box(meta['impacts'])
st.divider()
st.subheader("Key Findings & Actions")
action_summary(meta['findings'], st)
