import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, ENGAGE_PALETTE, AGE_PALETTE, AGE_ORDER, ARC_METADATA
from demo_data import (monthly_trend, tier_dist, age_dist, acct_age_dist, bracket_dist,
                       hourly_heatmap, seasonal_index, growth_metrics, HOURS, DAYS, MONTH_LABELS,
                       biz_personal_split, biz_top_merchants, personal_top_merchants,
                       product_dist, product_cross_sell, next_best_product,
                       bracket_volatility, bracket_trend, age_time_heatmap,
                       product_monthly_trend, product_merchant_heatmap)
from charts import (bar_chart, donut_chart, trend_line, dual_axis_bar_line, heatmap,
                    grouped_bar, stacked_bar, waterfall, action_summary, fmt_dollar, fmt_count)
from components import arc_header, headline_insight, quick_take, cross_reference, impact_box

meta = ARC_METADATA['portfolio_illusions']
arc_header(meta['title'], meta['subtitle'], meta['objection'], meta['reality'])

headline_insight(*meta['headline'], meta['headline_severity'])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Accounts", "33,205", "+3.2%")
c2.metric("Total Transactions", "5.89M", "+8.1%")
c3.metric("Single-Product %", "34.8%", "-1.2%")
c4.metric("Avg Products/Member", "2.31")

quick_take(meta['findings'])

# --- Primary Evidence ---
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        [str(x) for x in product_cross_sell['product_count']],
        product_cross_sell['churn_risk'].tolist(),
        title='Churn Risk by Product Count (%)', text_fmt=lambda x: f'{x:.1f}%',
        color=['#F87171', '#FBBF24', '#34D399', '#60A5FA', '#6EE7B7'],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        [str(x) for x in product_cross_sell['product_count']],
        product_cross_sell['avg_spend'].tolist(),
        title='Avg Monthly Spend by Product Count', text_fmt=fmt_dollar,
        color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)

cross_reference(*meta['cross_refs'][0])

st.divider()

# --- Supporting Evidence (Tabs) ---
tabs = st.tabs(["Portfolio Overview", "Business Accounts", "Personal Accounts", "Product Mix"])

with tabs[0]:
    st.plotly_chart(dual_axis_bar_line(
        monthly_trend['label'], monthly_trend['transactions'],
        monthly_trend['spend'] / 1_000_000,
        bar_name='Transactions', line_name='Spend ($M)',
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(
            bracket_dist['bracket'], bracket_dist['txn_count'],
            title='Transaction Count by Bracket', text_fmt=fmt_count,
            color=['#A8DADC', '#457B9D', '#2EC4B6', '#FF9F1C', '#F4A261', '#E76F51', '#E63946', '#1B2A4A'],
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(donut_chart(
            bracket_dist['bracket'], bracket_dist['total_spend'],
            colors=['#A8DADC', '#457B9D', '#2EC4B6', '#FF9F1C', '#F4A261', '#E76F51', '#E63946', '#1B2A4A'],
            title='Spend Distribution by Bracket',
        ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(
            bracket_dist['bracket'], bracket_volatility.tolist(),
            title='Bracket Volatility (CoV)', text_fmt=lambda x: f'{x:.2f}',
            color=['#A8DADC', '#457B9D', '#2EC4B6', '#FF9F1C', '#F4A261', '#E76F51', '#E63946', '#1B2A4A'],
        ), use_container_width=True, theme=None)
    with col2:
        import plotly.graph_objects as go
        fig = go.Figure()
        for br in bracket_trend.columns[1:]:
            fig.add_trace(go.Scatter(x=MONTH_LABELS, y=bracket_trend[br], mode='lines', name=br))
        fig.update_layout(title='Bracket Trend Over Time', height=380)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_chart(
            age_dist['age_band'], age_dist['accounts'], title='Accounts by Age Band',
            color=[AGE_PALETTE[a] for a in age_dist['age_band']], text_fmt=fmt_count,
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(bar_chart(
            age_dist['age_band'], age_dist['avg_spend'], title='Avg Monthly Spend by Age',
            color=[AGE_PALETTE[a] for a in age_dist['age_band']], text_fmt=fmt_dollar,
        ), use_container_width=True, theme=None)

    st.plotly_chart(heatmap(
        hourly_heatmap, [f'{h:02d}:00' for h in HOURS], DAYS,
        title='Transaction Volume by Day & Hour (% of peak)',
        text_fmt=lambda x: f'{x:.0f}',
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(heatmap(
            age_time_heatmap, ['Morning', 'Afternoon', 'Evening', 'Night'], AGE_ORDER,
            title='Spend by Age & Time of Day',
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(grouped_bar(
            AGE_ORDER,
            {'Avg Txns': age_dist['avg_txns'].tolist(),
             'Avg Spend ($100s)': (age_dist['avg_spend'] / 100).tolist()},
            title='Age Band Spending Profile',
        ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(donut_chart(
            tier_dist['tier'], tier_dist['accounts'],
            colors=[ENGAGE_PALETTE[t] for t in tier_dist['tier']],
            title='Engagement Tier Distribution',
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(bar_chart(
            tier_dist['tier'], tier_dist['avg_monthly_spend'],
            title='Avg Monthly Spend by Tier', text_fmt=fmt_dollar,
            color=[ENGAGE_PALETTE[t] for t in tier_dist['tier']],
        ), use_container_width=True, theme=None)

    st.plotly_chart(trend_line(
        seasonal_index['month'], seasonal_index['index'],
        title='Seasonal Spending Index (100 = average)', y_title='Index',
        color=GEN_COLORS['warning'],
    ), use_container_width=True, theme=None)

    st.dataframe(growth_metrics, use_container_width=True, hide_index=True)

with tabs[1]:
    c1, c2, c3 = st.columns(3)
    c1.metric("Business Accounts", "4,820", "14.5%")
    c2.metric("Business Avg Spend", "$2,550/mo", "2.7x personal")
    c3.metric("Business Avg Txns", "68/mo", "2.1x personal")

    st.plotly_chart(bar_chart(
        biz_top_merchants['merchant'], biz_top_merchants['total_spend'],
        title='Top 10 Business Merchants ($M)', text_fmt=fmt_dollar,
        color=GEN_COLORS['info'], horizontal=True,
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(donut_chart(
            biz_top_merchants['merchant'], biz_top_merchants['total_spend'],
            title='Business Spend Concentration',
        ), use_container_width=True, theme=None)
    with col2:
        import plotly.graph_objects as go
        fig = go.Figure()
        for m in biz_top_merchants['merchant'][:3]:
            from demo_data import biz_merchant_monthly
            if m in biz_merchant_monthly.columns:
                fig.add_trace(go.Scatter(x=MONTH_LABELS, y=biz_merchant_monthly[m], mode='lines', name=m))
        fig.update_layout(title='Top Business Merchant Trends', height=380)
        st.plotly_chart(fig, use_container_width=True, theme=None)

with tabs[2]:
    c1, c2, c3 = st.columns(3)
    c1.metric("Personal Accounts", "28,385", "85.5%")
    c2.metric("Personal Avg Spend", "$950/mo")
    c3.metric("Personal Avg Txns", "32/mo")

    st.plotly_chart(bar_chart(
        personal_top_merchants['merchant'], personal_top_merchants['total_spend'],
        title='Top 10 Personal Merchants ($M)', text_fmt=fmt_dollar,
        color=GEN_COLORS['primary'], horizontal=True,
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(donut_chart(
            personal_top_merchants['merchant'], personal_top_merchants['total_spend'],
            title='Personal Spend Concentration',
        ), use_container_width=True, theme=None)
    with col2:
        import plotly.graph_objects as go
        fig = go.Figure()
        from demo_data import personal_merchant_monthly
        for m in personal_top_merchants['merchant'][:3]:
            if m in personal_merchant_monthly.columns:
                fig.add_trace(go.Scatter(x=MONTH_LABELS, y=personal_merchant_monthly[m], mode='lines', name=m))
        fig.update_layout(title='Top Personal Merchant Trends', height=380)
        st.plotly_chart(fig, use_container_width=True, theme=None)

with tabs[3]:
    st.plotly_chart(bar_chart(
        product_dist['product'], product_dist['accounts'],
        title='Product Distribution', text_fmt=fmt_count, color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(donut_chart(
            product_dist['product'], product_dist['accounts'],
            title='Product Share',
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(grouped_bar(
            product_dist['product'][:5].tolist(),
            {'Avg Spend': product_dist['avg_spend'][:5].tolist(),
             'Avg Txns x10': (product_dist['avg_txns'][:5] * 10).tolist()},
            title='Product Performance',
        ), use_container_width=True, theme=None)

    import plotly.graph_objects as go
    fig = go.Figure()
    for prod in product_monthly_trend.columns[1:]:
        fig.add_trace(go.Scatter(x=MONTH_LABELS, y=product_monthly_trend[prod], mode='lines', name=prod))
    fig.update_layout(title='Product Spend Trend', height=380)
    st.plotly_chart(fig, use_container_width=True, theme=None)

    _prods_short = ['Platinum', 'Gold', 'Classic', 'Student', 'Biz Plat']
    _merchs_short = ['Amazon', 'Walmart', 'Target', 'Shell', 'Starbucks']
    st.plotly_chart(heatmap(
        product_merchant_heatmap, _merchs_short, _prods_short,
        title='Product x Merchant Mix (%)', text_fmt=lambda x: f'{x:.0f}%',
    ), use_container_width=True, theme=None)

st.divider()
impact_box(meta['impacts'])
st.divider()
st.subheader("Key Findings & Actions")
action_summary(meta['findings'], st)
