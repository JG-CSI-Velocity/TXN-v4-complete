import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, AGE_ORDER, ARC_METADATA
from demo_data import (top_merchants, mcc_categories, merchant_by_age, txn_type_split,
                       MONTH_LABELS, merchant_monthly_trend,
                       mcc_monthly_trend, mcc_age_heatmap, mcc_seasonal_heatmap,
                       txn_type_trend)
from charts import (bar_chart, donut_chart, trend_line, grouped_bar, stacked_bar,
                    heatmap, scatter_plot, fmt_dollar, fmt_count, action_summary)
from components import arc_header, headline_insight, quick_take, cross_reference, impact_box

meta = ARC_METADATA['spending_patterns']
arc_header(meta['title'], meta['subtitle'], meta['objection'], meta['reality'])

headline_insight(*meta['headline'], meta['headline_severity'])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Unique Merchants", "142,800")
c2.metric("Top 5 Concentration", "38%")
c3.metric("PIN-to-SIG Gap", "$420K")
c4.metric("Contactless Growth", "+28%")

quick_take(meta['findings'])

# --- Primary Evidence ---
col1, col2 = st.columns(2)
with col1:
    _top5 = top_merchants.head(5)
    _cum = np.cumsum(_top5['total_spend']) / top_merchants['total_spend'].sum() * 100
    st.plotly_chart(trend_line(
        [f'Top {i+1}' for i in range(5)], _cum.tolist(),
        title='Cumulative Spend Concentration', y_title='% of Total',
        color=GEN_COLORS['accent'], fill=True,
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        mcc_categories['category'].head(8).tolist(),
        mcc_categories['avg_txn_size'].head(8).tolist(),
        title='Avg Txn Size by Category', text_fmt=fmt_dollar,
        color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)

cross_reference(*meta['cross_refs'][0])

st.divider()

# --- Supporting Evidence (Tabs) ---
tabs = st.tabs(["Merchants", "MCC Categories", "Transaction Types"])

with tabs[0]:
    n_show = st.slider("Merchants to display", 5, 20, 10, key='merch_slider')
    display = top_merchants.head(n_show)

    st.plotly_chart(bar_chart(
        display['merchant'][::-1].tolist(),
        (display['total_spend'][::-1] * 1_000_000).tolist(),
        text_fmt=fmt_dollar, horizontal=True, height=max(350, n_show * 38),
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(donut_chart(
            display['merchant'], display['total_spend'],
            title='Spend Share by Merchant',
        ), use_container_width=True, theme=None)
    with col2:
        _cum_all = np.cumsum(display['total_spend']) / top_merchants['total_spend'].sum() * 100
        st.plotly_chart(trend_line(
            [f'Top {i+1}' for i in range(len(display))], _cum_all.tolist(),
            title='Cumulative Spend Concentration', y_title='% of Total',
            color=GEN_COLORS['info'],
        ), use_container_width=True, theme=None)

    st.subheader("Top 5 Merchant Monthly Trends")
    fig = go.Figure()
    for m in top_merchants['merchant'].head(5):
        if m in merchant_monthly_trend.columns:
            fig.add_trace(go.Scatter(x=MONTH_LABELS, y=merchant_monthly_trend[m],
                                     mode='lines', name=m))
    fig.update_layout(title='Monthly Spend Trend ($M)', height=380)
    st.plotly_chart(fig, use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        _sorted = display.sort_values('growth_pct', ascending=True)
        _colors = [GEN_COLORS['success'] if g > 0 else GEN_COLORS['accent'] for g in _sorted['growth_pct']]
        st.plotly_chart(bar_chart(
            _sorted['merchant'].tolist(), _sorted['growth_pct'].tolist(),
            title='YoY Growth Rate', text_fmt=lambda x: f'{x:+.0f}%',
            color=_colors, horizontal=True, height=max(350, n_show * 38),
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(bar_chart(
            display['merchant'].tolist(), display['volatility'].tolist(),
            title='Spend Volatility (CoV)', text_fmt=lambda x: f'{x:.2f}',
            color=GEN_COLORS['warning'],
        ), use_container_width=True, theme=None)

    st.subheader("Merchant Lifecycle Stage")
    st.plotly_chart(bar_chart(
        ['Emerging', 'Growing', 'Mature', 'Declining'],
        [2840, 18200, 98400, 23360], text_fmt=fmt_count,
        color=[GEN_COLORS['accent'], GEN_COLORS['success'], GEN_COLORS['info'], GEN_COLORS['muted']],
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grouped_bar(
            display['merchant'].head(5).tolist(),
            {'Business ($M)': [0.8, 1.2, 0.5, 2.1, 0.3],
             'Personal ($M)': [8.4, 5.2, 3.8, 1.4, 2.8]},
            title='Top 5: Business vs Personal Spend',
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(grouped_bar(
            ['18-35', '36-55', '56+'],
            {'Amazon': [5.2, 8.1, 5.2], 'Walmart': [2.8, 5.4, 4.1], 'Target': [2.1, 3.8, 2.8]},
            title='Top 3 Merchants by Age Group ($M)',
        ), use_container_width=True, theme=None)

    st.subheader("New Merchant Entrants (Last 3 Months)")
    import pandas as pd
    st.dataframe(pd.DataFrame({
        'Merchant': ['DoorDash', 'Instacart', 'Temu', 'Shein', 'Apple Pay Cash'],
        'First Seen': ['Nov25', 'Oct25', 'Dec25', 'Nov25', 'Oct25'],
        'Accounts': [2400, 1800, 3200, 1500, 4100],
        'Avg Txn': ['$28', '$62', '$35', '$22', '$45'],
        'Growth Trend': ['Rapid', 'Rapid', 'Explosive', 'Moderate', 'Steady'],
    }), use_container_width=True, hide_index=True)

with tabs[1]:
    display_mcc = mcc_categories.head(10)

    st.plotly_chart(bar_chart(
        display_mcc['category'][::-1].tolist(),
        (display_mcc['total_spend'][::-1] * 1_000_000).tolist(),
        text_fmt=fmt_dollar, horizontal=True, height=420,
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(donut_chart(display_mcc['category'], display_mcc['total_spend'],
                                    title='Spend Share by Category'), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(bar_chart(display_mcc['category'].tolist(),
                                  display_mcc['avg_txn_size'].tolist(),
                                  title='Avg Txn Size by Category', text_fmt=fmt_dollar,
                                  color=GEN_COLORS['info']), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        _cum_mcc = np.cumsum(display_mcc['total_spend']) / mcc_categories['total_spend'].sum() * 100
        st.plotly_chart(trend_line(
            [f'Top {i+1}' for i in range(len(display_mcc))], _cum_mcc.tolist(),
            title='Category Concentration Curve', y_title='% of Total',
        ), use_container_width=True, theme=None)
    with col2:
        fig = go.Figure()
        for cat in ['Grocery', 'Gas/Fuel', 'Restaurants', 'Subscriptions']:
            if cat in mcc_monthly_trend.columns:
                fig.add_trace(go.Scatter(x=MONTH_LABELS, y=mcc_monthly_trend[cat],
                                         mode='lines', name=cat))
        fig.update_layout(title='Category Trend', height=380)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    st.subheader("Category Spend by Age Band")
    st.plotly_chart(heatmap(
        mcc_age_heatmap, AGE_ORDER,
        ['Grocery', 'Gas', 'Restaurants', 'General', 'Healthcare'],
        title='Spend Index by Category & Age',
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(grouped_bar(
            ['New (<1yr)', 'Mid (1-5yr)', 'Mature (5yr+)'],
            {'Grocery': [58, 82, 78], 'Gas': [42, 52, 38], 'Restaurants': [55, 48, 32]},
            title='Category by Account Maturity ($M)',
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(grouped_bar(
            ['Power', 'Heavy', 'Moderate', 'Light'],
            {'Grocery': [12, 8, 5, 2], 'Gas': [8, 5, 3, 1], 'Subscriptions': [2.5, 1.8, 1.2, 0.4]},
            title='Category by Engagement Tier ($M)',
        ), use_container_width=True, theme=None)

    st.plotly_chart(grouped_bar(
        display_mcc['category'].head(6).tolist(),
        {'Personal': [72, 42, 38, 28, 24, 20], 'Business': [10, 6, 4, 10, 4, 4]},
        title='Category Spend: Business vs Personal ($M)',
    ), use_container_width=True, theme=None)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(heatmap(
            mcc_seasonal_heatmap, MONTH_LABELS,
            ['Grocery', 'Gas', 'Restaurants', 'Travel', 'Entertainment'],
            title='Seasonal Index by Category',
        ), use_container_width=True, theme=None)
    with col2:
        st.plotly_chart(bar_chart(
            ['1-3', '4-6', '7-9', '10-12', '13+'],
            [4200, 8500, 9800, 6200, 4505],
            title='Category Diversity (# categories used)', text_fmt=fmt_count,
            color=GEN_COLORS['success'],
        ), use_container_width=True, theme=None)

with tabs[2]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Signature Share", "47.6%")
    c2.metric("PIN Share", "20.4%")
    c3.metric("Contactless Growth", "+28%")
    c4.metric("Online Share", "13.9%", "+4.1%")

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
        for typ in ['Signature', 'PIN', 'Contactless', 'Online']:
            if typ in txn_type_trend.columns:
                fig.add_trace(go.Scatter(x=MONTH_LABELS, y=txn_type_trend[typ],
                                         mode='lines', name=typ))
        fig.update_layout(title='Type Share Trend', height=380)
        st.plotly_chart(fig, use_container_width=True, theme=None)

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
impact_box(meta['impacts'])
st.divider()
st.subheader("Key Findings & Actions")
action_summary(meta['findings'], st)
