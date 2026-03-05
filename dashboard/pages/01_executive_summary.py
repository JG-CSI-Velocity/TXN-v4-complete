import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, CAT_COLORS, ENGAGE_PALETTE
from demo_data import scorecard_df, monthly_trend, tier_dist
from charts import trend_line, donut_chart, waterfall

st.header("Executive Scorecard")
st.caption("5 analyses | Portfolio health at a glance -- RAG status across all sections")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Accounts", "33,205", "+3.2%")
c2.metric("Total Transactions", "5.89M", "+8.1%")
c3.metric("Avg Txn/Account", "177", "+4.7%")
c4.metric("Active Rate", "88.5%", "+1.2%")
st.divider()

# --- RAG Scorecard Grid ---
st.subheader("KPI Scorecard (22 metrics across 9 categories)")

RAG_COLORS = {'Green': '#34D399', 'Amber': '#FBBF24', 'Red': '#F87171'}
RAG_BG = {
    'Green': 'rgba(52,211,153,0.12)',
    'Amber': 'rgba(251,191,36,0.12)',
    'Red': 'rgba(248,113,113,0.12)',
}

categories = scorecard_df['category'].unique()
cols_per_row = 3

for i in range(0, len(categories), cols_per_row):
    batch = categories[i:i + cols_per_row]
    cols = st.columns(len(batch))
    for col, cat in zip(cols, batch):
        cat_rows = scorecard_df[scorecard_df['category'] == cat]
        cat_color = CAT_COLORS.get(cat, GEN_COLORS['primary'])
        with col:
            st.markdown(
                f'<div style="background:linear-gradient(135deg, {cat_color}, {cat_color}dd); '
                f'color:white; padding:10px 14px; '
                f'border-radius:10px 10px 0 0; font-weight:700; font-size:14px; '
                f'letter-spacing:0.02em; font-family:Outfit,sans-serif;">{cat}</div>',
                unsafe_allow_html=True,
            )
            for _, row in cat_rows.iterrows():
                rag_color = RAG_COLORS.get(row['rag'], '#64748B')
                rag_bg = RAG_BG.get(row['rag'], 'rgba(100,116,139,0.1)')
                st.markdown(
                    f'<div style="border:1px solid #1E293B; border-top:none; padding:12px 14px; '
                    f'background:#111827;">'
                    f'<span style="color:#64748B; font-size:11px; text-transform:uppercase; '
                    f'letter-spacing:0.04em;">{row["metric"]}</span><br>'
                    f'<span style="font-size:24px; font-weight:700; color:#E2E8F0; '
                    f'font-family:Outfit,sans-serif;">{row["value"]}</span>'
                    f'&nbsp;<span style="background:{rag_bg}; color:{rag_color}; padding:3px 10px; '
                    f'border-radius:6px; font-size:11px; font-weight:700; '
                    f'border:1px solid {rag_color}33;">{row["rag"]}</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown("")

st.divider()

# --- Strategic Priorities ---
st.subheader("Strategic Priorities")
priorities = [
    ("Reduce competitor wallet share", "Competition", "High", "$61M recoverable"),
    ("Deepen single-product relationships", "Relationship", "High", "11,560 accounts"),
    ("Increase Reg E opt-in rate", "Reg E", "High", "$1.1M revenue upside"),
    ("Capture payroll/direct deposit", "Payroll", "High", "Only 28.1% detected"),
    ("Reactivate dormant accounts", "Retention", "Medium", "3,650 dormant"),
    ("Shift PIN to signature", "Interchange", "Medium", "$420K opportunity"),
    ("Protect Power tier from downgrade", "Engagement", "Medium", "18% downgrade rate"),
]
for action, category, priority, impact in priorities:
    color = {'High': '#F87171', 'Medium': '#FBBF24', 'Low': '#34D399'}[priority]
    bg = {'High': 'rgba(248,113,113,0.08)', 'Medium': 'rgba(251,191,36,0.08)',
          'Low': 'rgba(52,211,153,0.08)'}[priority]
    st.markdown(
        f'<div style="padding:10px 14px; margin-bottom:4px; border-radius:8px; '
        f'background:{bg}; border-left:3px solid {color};">'
        f'<span style="color:{color}; font-size:10px; font-weight:700; '
        f'text-transform:uppercase; letter-spacing:0.5px;">{priority}</span>&nbsp;&nbsp;'
        f'<span style="color:#E2E8F0; font-weight:600;">{action}</span> '
        f'<span style="color:#64748B;">({category})</span> '
        f'<span style="color:#94A3B8;">-- {impact}</span></div>',
        unsafe_allow_html=True,
    )

st.divider()

# --- Opportunity Waterfall ---
st.subheader("Revenue Opportunity Waterfall")
st.plotly_chart(waterfall(
    ['Current\nPortfolio', 'Recover\nCompetitor $', 'Cross-sell\nProducts',
     'Reg E\nOpt-in', 'PIN->SIG\nShift', 'Reduce\nAttrition', 'Potential\nTotal'],
    [498_000_000, 61_000_000, 18_000_000, 1_100_000, 420_000, 6_100_000, 584_620_000],
    title='Annualized Revenue Opportunity',
), use_container_width=True, theme=None)

# --- Engagement Donut + Trend ---
col_a, col_b = st.columns(2)
with col_a:
    st.plotly_chart(donut_chart(
        tier_dist['tier'], tier_dist['accounts'],
        colors=[ENGAGE_PALETTE[t] for t in tier_dist['tier']],
        title='Engagement Distribution',
    ), use_container_width=True, theme=None)
with col_b:
    st.plotly_chart(trend_line(
        monthly_trend['label'], monthly_trend['transactions'],
        title='Monthly Transaction Trend', y_title='Transactions',
        color=GEN_COLORS['primary'],
    ), use_container_width=True, theme=None)

# --- RAG Summary ---
st.divider()
n_green = (scorecard_df['rag'] == 'Green').sum()
n_amber = (scorecard_df['rag'] == 'Amber').sum()
n_red = (scorecard_df['rag'] == 'Red').sum()
c1, c2, c3 = st.columns(3)
c1.markdown(
    f'<div style="text-align:center; padding:20px; '
    f'background:linear-gradient(135deg, rgba(52,211,153,0.15), rgba(52,211,153,0.05)); '
    f'border:1px solid rgba(52,211,153,0.2); '
    f'border-radius:12px; font-family:Outfit,sans-serif;">'
    f'<div style="font-size:36px; font-weight:700; color:#34D399;">{n_green}</div>'
    f'<div style="font-size:12px; color:#64748B; text-transform:uppercase; '
    f'letter-spacing:0.08em; margin-top:4px;">Green</div></div>',
    unsafe_allow_html=True)
c2.markdown(
    f'<div style="text-align:center; padding:20px; '
    f'background:linear-gradient(135deg, rgba(251,191,36,0.15), rgba(251,191,36,0.05)); '
    f'border:1px solid rgba(251,191,36,0.2); '
    f'border-radius:12px; font-family:Outfit,sans-serif;">'
    f'<div style="font-size:36px; font-weight:700; color:#FBBF24;">{n_amber}</div>'
    f'<div style="font-size:12px; color:#64748B; text-transform:uppercase; '
    f'letter-spacing:0.08em; margin-top:4px;">Amber</div></div>',
    unsafe_allow_html=True)
c3.markdown(
    f'<div style="text-align:center; padding:20px; '
    f'background:linear-gradient(135deg, rgba(248,113,113,0.15), rgba(248,113,113,0.05)); '
    f'border:1px solid rgba(248,113,113,0.2); '
    f'border-radius:12px; font-family:Outfit,sans-serif;">'
    f'<div style="font-size:36px; font-weight:700; color:#F87171;">{n_red}</div>'
    f'<div style="font-size:12px; color:#64748B; text-transform:uppercase; '
    f'letter-spacing:0.08em; margin-top:4px;">Red</div></div>',
    unsafe_allow_html=True)
