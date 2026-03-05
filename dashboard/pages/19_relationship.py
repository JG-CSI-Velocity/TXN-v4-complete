import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import product_cross_sell, next_best_product
from charts import (bar_chart, donut_chart, grouped_bar, heatmap, scatter_plot,
                    waterfall, fmt_dollar, fmt_count, action_summary)

st.header("Relationship Depth Analysis")
st.caption("10 analyses | Product cross-holdings, relationship value, next-best-product")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Products/Member", "2.31")
c2.metric("Single-Product %", "34.8%")
c3.metric("Cross-Sell Opportunity", "11,560 accts")
c4.metric("Relationship Revenue Lift", "$18M")
st.divider()

# Product count bar (03)
st.subheader("Product Count Distribution")
st.plotly_chart(bar_chart(
    [str(x) for x in product_cross_sell['product_count']],
    product_cross_sell['accounts'].tolist(),
    title='Accounts by Number of Products Held', text_fmt=fmt_count,
    color=[GEN_COLORS['accent'], GEN_COLORS['warning'], GEN_COLORS['info'],
           GEN_COLORS['success'], GEN_COLORS['primary']],
), use_container_width=True, theme=None)

# Single product risk (04)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        [str(x) for x in product_cross_sell['product_count']],
        product_cross_sell['churn_risk'].tolist(),
        title='Churn Risk by Product Count (%)', text_fmt=lambda x: f'{x:.1f}%',
        color=[GEN_COLORS['accent'], GEN_COLORS['warning'], GEN_COLORS['info'],
               GEN_COLORS['success'], GEN_COLORS['primary']],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        [str(x) for x in product_cross_sell['product_count']],
        product_cross_sell['avg_spend'].tolist(),
        title='Avg Monthly Spend by Product Count', text_fmt=fmt_dollar,
        color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)

# Cross-sell matrix (05)
st.subheader("Product Cross-Sell Matrix")
_products = ['Checking', 'Savings', 'Credit Card', 'Auto Loan', 'Mortgage', 'Investment']
_cross = np.random.uniform(5, 65, (6, 6))
np.fill_diagonal(_cross, 100)
st.plotly_chart(heatmap(
    _cross, _products, _products,
    title='% of Product A Holders Also Having Product B',
    text_fmt=lambda x: f'{x:.0f}%',
), use_container_width=True, theme=None)

# Relationship value (06)
st.subheader("Relationship Value Curve")
st.plotly_chart(grouped_bar(
    [str(x) for x in product_cross_sell['product_count']],
    {'Avg Spend ($)': product_cross_sell['avg_spend'].tolist(),
     'Avg Balance ($K)': (np.array(product_cross_sell['avg_balance']) / 1000).tolist()},
    title='Account Value by Relationship Depth',
), use_container_width=True, theme=None)

# Leakage opportunity (07)
st.plotly_chart(waterfall(
    ['Current\nRelationship\nRevenue', 'Cross-sell\nCredit Card', 'Cross-sell\nAuto Loan',
     'Deepen\nSavings', 'Add\nInvestment', 'Potential\nTotal'],
    [42_000_000, 8_000_000, 5_200_000, 3_800_000, 1_200_000, 60_200_000],
    title='Relationship Revenue Opportunity',
), use_container_width=True, theme=None)

# By demographics (08)
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

# Next best product (09)
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

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Single Product', 'finding': '34.8% are single-product members with 18.5% churn risk -- highest priority for cross-sell', 'priority': 'High'},
    {'category': 'Revenue Curve', 'finding': 'Each additional product adds ~$340/mo avg spend and reduces churn by 6pp', 'priority': 'High'},
    {'category': 'Credit Card Gap', 'finding': '4,800 checking-only members have 42% propensity for credit card', 'priority': 'High'},
    {'category': 'Young Members', 'finding': '18-25 avg 1.4 products -- early cross-sell critical for retention', 'priority': 'Medium'},
], st)
