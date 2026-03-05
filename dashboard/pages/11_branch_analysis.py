import streamlit as st
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS
from demo_data import branch_data, MONTH_LABELS
from charts import bar_chart, grouped_bar, heatmap, trend_line, fmt_dollar, fmt_count, action_summary
import plotly.graph_objects as go

st.header("Branch Analysis")
st.caption("10 analyses | Branch-level transaction analysis, top branch ranking")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Branches", "15")
c2.metric("Top Branch Spend", f"${branch_data.iloc[0]['total_spend']/1e6:.1f}M")
c3.metric("Avg Txns/Branch", f"{branch_data['avg_txns'].mean():.0f}/mo")
c4.metric("Spread (Max/Min)", f"{branch_data['total_spend'].max()/branch_data['total_spend'].min():.1f}x")
st.divider()

# Top bar (03)
st.subheader("Branch Ranking by Total Spend")
st.plotly_chart(bar_chart(
    branch_data['branch'][::-1].tolist(),
    branch_data['total_spend'][::-1].tolist(),
    text_fmt=fmt_dollar, horizontal=True, height=500,
), use_container_width=True, theme=None)

# Spend comparison (04) + Concentration (05)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(grouped_bar(
        branch_data['branch'].head(8).tolist(),
        {'Accounts': (branch_data['accounts'].head(8) / 100).tolist(),
         'Avg Txns': branch_data['avg_txns'].head(8).tolist()},
        title='Branch Accounts (hundreds) & Avg Txns',
    ), use_container_width=True, theme=None)
with col2:
    _cum = np.cumsum(branch_data['total_spend']) / branch_data['total_spend'].sum() * 100
    st.plotly_chart(trend_line(
        branch_data['branch'].tolist(), _cum.tolist(),
        title='Cumulative Spend by Branch', y_title='% of Total',
    ), use_container_width=True, theme=None)

# Merchant heatmap (06)
st.subheader("Top Merchants by Branch")
_merch_branch = np.random.uniform(2, 25, (8, 5))
st.plotly_chart(heatmap(
    _merch_branch, ['Amazon', 'Walmart', 'Target', 'Shell', 'Starbucks'],
    branch_data['branch'].head(8).tolist(),
    title='Spend Share % by Merchant & Branch',
), use_container_width=True, theme=None)

# Monthly trend (07)
st.subheader("Branch Monthly Trends")
fig = go.Figure()
for br in branch_data['branch'].head(5):
    fig.add_trace(go.Scatter(x=MONTH_LABELS,
                             y=np.random.normal(100, 8, len(MONTH_LABELS)),
                             mode='lines', name=br))
fig.update_layout(height=380, yaxis=dict(gridcolor='#E9ECEF'),
                  margin=dict(l=50, r=20, t=20, b=40))
st.plotly_chart(fig, use_container_width=True, theme=None)

# Biz/Personal mix (08) + Spend profile (09)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(
        branch_data['branch'].head(10).tolist(),
        branch_data['pct_business'].head(10).tolist(),
        title='% Business Accounts by Branch', text_fmt=lambda x: f'{x:.1f}%',
        color=GEN_COLORS['info'],
    ), use_container_width=True, theme=None)
with col2:
    st.plotly_chart(bar_chart(
        branch_data['branch'].head(10).tolist(),
        branch_data['avg_balance'].head(10).tolist(),
        title='Avg Balance by Branch', text_fmt=fmt_dollar,
        color=GEN_COLORS['success'],
    ), use_container_width=True, theme=None)

st.divider()
st.subheader("Key Findings & Actions")
action_summary([
    {'category': 'Top Branch', 'finding': f'{branch_data.iloc[0]["branch"]} leads with ${branch_data.iloc[0]["total_spend"]/1e6:.1f}M spend', 'priority': 'Low'},
    {'category': 'Concentration', 'finding': 'Top 5 branches = 52% of total spend -- geographic concentration risk', 'priority': 'Medium'},
    {'category': 'Underperformers', 'finding': 'Bottom 3 branches have <$3M each -- review staffing and merchant mix', 'priority': 'Medium'},
], st)
