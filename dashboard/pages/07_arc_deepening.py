import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, ENGAGE_PALETTE, ARC_METADATA
from demo_data import (product_cross_sell, next_best_product, seg_order,
                       seg_migration, seg_net_flow, migration_matrix,
                       migration_monthly, MONTH_LABELS, segment_projection,
                       campaign_swipe_comparison)
from charts import (bar_chart, donut_chart, trend_line, grouped_bar, stacked_bar,
                    heatmap, waterfall, fmt_dollar, fmt_count, action_summary)
from components import arc_header, headline_insight, quick_take, cross_reference, impact_box

meta = ARC_METADATA['deepening_decline']
arc_header(meta['title'], meta['subtitle'], meta['objection'], meta['reality'])

headline_insight(*meta['headline'], meta['headline_severity'])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Upgrade:Degrade Ratio", "1.4:1")
c2.metric("Single-Product %", "34.8%")
c3.metric("Dormant Recovery", "4%")
c4.metric("Campaign Multiplier", "2x")

quick_take(meta['findings'])

# --- Primary Evidence ---
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        [str(x) for x in product_cross_sell['product_count']],
        product_cross_sell['churn_risk'].tolist(),
        title='Churn Risk by Product Count (%)', text_fmt=lambda x: f'{x:.1f}%',
        color=['#F87171', '#FBBF24', '#34D399', '#60A5FA', '#6EE7B7'],
    ), use_container_width=True, key='primary_churn_risk', theme=None)
with col2:
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
    fig.update_layout(barmode='relative', height=400, title='Monthly Net Migration Flow',
                      yaxis=dict(title='Accounts'))
    st.plotly_chart(fig, use_container_width=True, key='primary_net_migration', theme=None)

cross_reference(*meta['cross_refs'][0])

st.divider()

# --- Supporting Evidence (Tabs) ---
tabs = st.tabs(["Relationship Depth", "Segment Evolution", "Engagement Migration"])

with tabs[0]:
    st.subheader("Product Count Distribution")
    st.plotly_chart(bar_chart(
        [str(x) for x in product_cross_sell['product_count']],
        product_cross_sell['accounts'].tolist(),
        title='Accounts by Number of Products Held', text_fmt=fmt_count,
        color=[GEN_COLORS['accent'], GEN_COLORS['warning'], GEN_COLORS['info'],
               GEN_COLORS['success'], GEN_COLORS['primary']],
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(
            [str(x) for x in product_cross_sell['product_count']],
            product_cross_sell['churn_risk'].tolist(),
            title='Churn Risk by Product Count (%)', text_fmt=lambda x: f'{x:.1f}%',
            color=['#F87171', '#FBBF24', '#34D399', '#60A5FA', '#6EE7B7'],
        ), use_container_width=True, key='tab_churn_risk', theme=None)
    with col2:
        st.plotly_chart(bar_chart(
            [str(x) for x in product_cross_sell['product_count']],
            product_cross_sell['avg_spend'].tolist(),
            title='Avg Monthly Spend by Product Count', text_fmt=fmt_dollar,
            color=GEN_COLORS['info'],
        ), use_container_width=True, theme=None)

    st.subheader("Product Cross-Sell Matrix")
    _products = ['Checking', 'Savings', 'Credit Card', 'Auto Loan', 'Mortgage', 'Investment']
    np.random.seed(42)
    _cross = np.random.uniform(5, 65, (6, 6))
    np.fill_diagonal(_cross, 100)
    st.plotly_chart(heatmap(
        _cross, _products, _products,
        title='% of Product A Holders Also Having Product B',
        text_fmt=lambda x: f'{x:.0f}%',
    ), use_container_width=True, theme=None)

    st.subheader("Relationship Value Curve")
    st.plotly_chart(grouped_bar(
        [str(x) for x in product_cross_sell['product_count']],
        {'Avg Spend ($)': product_cross_sell['avg_spend'].tolist(),
         'Avg Balance ($K)': (np.array(product_cross_sell['avg_balance']) / 1000).tolist()},
        title='Account Value by Relationship Depth',
    ), use_container_width=True, theme=None)

    st.plotly_chart(waterfall(
        ['Current\nRelationship\nRevenue', 'Cross-sell\nCredit Card', 'Cross-sell\nAuto Loan',
         'Deepen\nSavings', 'Add\nInvestment', 'Potential\nTotal'],
        [42_000_000, 8_000_000, 5_200_000, 3_800_000, 1_200_000, 60_200_000],
        title='Relationship Revenue Opportunity',
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grouped_bar(
            ['18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
            {'Avg Products': [1.4, 2.1, 2.8, 2.5, 2.2, 1.8]},
            title='Avg Products by Age Band',
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(grouped_bar(
            ['Power', 'Heavy', 'Moderate', 'Light', 'Dormant'],
            {'Avg Products': [3.2, 2.8, 2.2, 1.6, 1.2]},
            title='Avg Products by Engagement Tier',
        ), use_container_width=True, theme=None)

    st.subheader("Next Best Product Recommendations")
    st.dataframe(
        next_best_product.rename(columns={
            'current_products': 'Current Products', 'recommended': 'Recommended Next',
            'propensity': 'Propensity Score', 'accounts_eligible': 'Eligible Accounts',
        }).style.format({
            'Propensity Score': '{:.0%}',
            'Eligible Accounts': '{:,}',
        }),
        use_container_width=True, hide_index=True,
    )

with tabs[1]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Upgrade:Degrade Ratio", "1.4:1")
    c2.metric("% Upgraded", "12.3%")
    c3.metric("% Degraded", "8.7%")
    c4.metric("% Stable", "79.0%")

    st.subheader("Current Segment Distribution")
    _seg_counts = [2987, 5640, 9300, 10120, 5158]
    st.plotly_chart(bar_chart(
        seg_order, _seg_counts, text_fmt=fmt_count,
        color=[ENGAGE_PALETTE[s] for s in seg_order],
    ), use_container_width=True, theme=None)

    st.subheader("Segment Migration Matrix")
    st.plotly_chart(heatmap(
        seg_migration, seg_order, seg_order,
        title='Starting Tier -> Ending Tier (%)',
        text_fmt=lambda x: f'{x:.1f}%',
        colorscale=[[0, '#0B1120'], [0.3, '#1E3A5F'], [0.5, '#2563EB'], [0.7, '#38BDF8'], [1, '#6EE7B7']],
    ), use_container_width=True, key='seg_migration_heatmap', theme=None)
    st.info("Diagonal = stable. Above diagonal = upgrades. Below = downgrades.")

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

    st.plotly_chart(grouped_bar(
        seg_order,
        {'Responder Upgrade %': [0, 12, 18, 15, 6],
         'Non-Responder Upgrade %': [0, 6, 10, 8, 3],
         'Never Mailed Upgrade %': [0, 5, 8, 7, 2]},
        title='Upgrade Rate by Campaign Status',
    ), use_container_width=True, theme=None)

    st.subheader("Segment Projection (Next 6 Months)")
    fig = go.Figure()
    months_proj = segment_projection['month'].tolist()
    for seg in seg_order:
        if seg in segment_projection.columns:
            fig.add_trace(go.Scatter(x=months_proj, y=segment_projection[seg],
                                     mode='lines', name=seg,
                                     line=dict(color=ENGAGE_PALETTE[seg])))
    fig.update_layout(height=380, title='Segment Projection')
    st.plotly_chart(fig, use_container_width=True, theme=None)

with tabs[2]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Net Migration/Month", "+142", "positive")
    c2.metric("Tier Stability Rate", "75.2%")
    c3.metric("Power Tier Growth", "+2.1%", "+63 accts")
    c4.metric("Dormant Recovery Rate", "4.2%")

    st.subheader("Tier Migration Matrix (Start -> End)")
    st.plotly_chart(heatmap(
        migration_matrix.values, seg_order, seg_order,
        title='% of Starting Tier -> Ending Tier',
        text_fmt=lambda x: f'{x:.1f}%',
        colorscale=[[0, '#0B1120'], [0.3, '#1E3A5F'], [0.5, '#2563EB'], [0.7, '#38BDF8'], [1, '#6EE7B7']],
    ), use_container_width=True, key='migration_matrix_heatmap', theme=None)

    st.subheader("Monthly Net Migration Flow")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=MONTH_LABELS, y=migration_monthly['upgrades'],
                         name='Upgrades', marker_color=GEN_COLORS['success']))
    fig.add_trace(go.Bar(x=MONTH_LABELS, y=-migration_monthly['downgrades'],
                         name='Downgrades', marker_color=GEN_COLORS['accent']))
    fig.add_trace(go.Scatter(x=MONTH_LABELS, y=migration_monthly['net'],
                             mode='lines+markers', name='Net Flow',
                             line=dict(color=GEN_COLORS['primary'], width=3),
                             marker=dict(size=7)))
    fig.add_hline(y=0, line_dash='dash', line_color=GEN_COLORS['muted'])
    fig.update_layout(barmode='relative', height=400, yaxis=dict(title='Accounts'))
    st.plotly_chart(fig, use_container_width=True, key='tab_net_migration', theme=None)

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

    st.subheader("Swipe Category: Responder vs Non-Responder")
    st.plotly_chart(grouped_bar(
        ['Very High', 'High', 'Medium', 'Low', 'Inactive'],
        {'Responders %': campaign_swipe_comparison[0].tolist(),
         'Non-Responders %': campaign_swipe_comparison[1].tolist()},
        title='Swipe Category Distribution',
    ), use_container_width=True, theme=None)

st.divider()
impact_box(meta['impacts'])
st.divider()
st.subheader("Key Findings & Actions")
action_summary(meta['findings'], st)
