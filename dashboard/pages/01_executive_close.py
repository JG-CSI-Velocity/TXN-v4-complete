import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import GEN_COLORS, CAT_COLORS, ARC_METADATA
from demo_data import (scorecard_df, monthly_trend, tier_dist,
                       sankey_sources, sankey_targets, sankey_values, sankey_labels)
from charts import (trend_line, donut_chart, waterfall, risk_gauge,
                    sankey_flow, action_summary)
from components import headline_insight, impact_box, quick_take

st.markdown(
    '<h1 style="font-family:Outfit,sans-serif; font-size:2rem; '
    'letter-spacing:-0.03em; margin-bottom:2px;">The Bottom Line</h1>'
    '<p style="color:#64748B; font-size:13px; margin-bottom:24px;">'
    'Portfolio health, top findings, and what to do first</p>',
    unsafe_allow_html=True,
)

# --- Portfolio Health Gauge ---
n_green = (scorecard_df['rag'] == 'Green').sum()
n_amber = (scorecard_df['rag'] == 'Amber').sum()
n_red = (scorecard_df['rag'] == 'Red').sum()
health_score = int((n_green * 100 + n_amber * 60 + n_red * 20) / len(scorecard_df))

col_gauge, col_rag = st.columns([1, 2])
with col_gauge:
    st.plotly_chart(risk_gauge(health_score), use_container_width=True, theme=None)
with col_rag:
    c1, c2, c3 = st.columns(3)
    c1.markdown(
        f'<div style="text-align:center; padding:16px; '
        f'background:rgba(52,211,153,0.1); border:1px solid rgba(52,211,153,0.2); '
        f'border-radius:12px;">'
        f'<div style="font-size:32px; font-weight:700; color:#34D399; font-family:Outfit;">{n_green}</div>'
        f'<div style="font-size:11px; color:#64748B; text-transform:uppercase; letter-spacing:0.06em;">Green</div>'
        f'</div>', unsafe_allow_html=True)
    c2.markdown(
        f'<div style="text-align:center; padding:16px; '
        f'background:rgba(251,191,36,0.1); border:1px solid rgba(251,191,36,0.2); '
        f'border-radius:12px;">'
        f'<div style="font-size:32px; font-weight:700; color:#FBBF24; font-family:Outfit;">{n_amber}</div>'
        f'<div style="font-size:11px; color:#64748B; text-transform:uppercase; letter-spacing:0.06em;">Amber</div>'
        f'</div>', unsafe_allow_html=True)
    c3.markdown(
        f'<div style="text-align:center; padding:16px; '
        f'background:rgba(248,113,113,0.1); border:1px solid rgba(248,113,113,0.2); '
        f'border-radius:12px;">'
        f'<div style="font-size:32px; font-weight:700; color:#F87171; font-family:Outfit;">{n_red}</div>'
        f'<div style="font-size:11px; color:#64748B; text-transform:uppercase; letter-spacing:0.06em;">Red</div>'
        f'</div>', unsafe_allow_html=True)

st.divider()

# --- 5 Headline Findings ---
st.subheader("The 5 Things You Need to Know")

headline_insight("Competitor Penetration", "55.5%",
                 "of members use a competitor card -- $61M recoverable annually", "danger")

col1, col2 = st.columns(2)
with col1:
    headline_insight("Single-Product Members", "34.8%",
                     "with 18.5% churn risk -- 3x higher than multi-product", "warning")
with col2:
    headline_insight("Payroll Detection", "28.1%",
                     "vs 50% industry -- each capture adds $2,480 in deposits", "warning")

col1, col2 = st.columns(2)
with col1:
    headline_insight("Accounts At Risk", "18.3%",
                     "declining or dormant -- $4.2M annual spend at risk", "danger")
with col2:
    headline_insight("PIN-to-SIG Gap", "$420K",
                     "annual interchange left on the table", "info")

st.divider()

# --- Revenue Opportunity Waterfall ---
st.subheader("Revenue Opportunity Waterfall")
st.plotly_chart(waterfall(
    ['Current\nPortfolio', 'Recover\nCompetitor $', 'Cross-sell\nProducts',
     'Reg E\nOpt-in', 'PIN->SIG\nShift', 'Reduce\nAttrition', 'Potential\nTotal'],
    [498_000_000, 61_000_000, 18_000_000, 1_100_000, 420_000, 6_100_000, 584_620_000],
    title='Annualized Revenue Opportunity',
), use_container_width=True, theme=None)

# --- Attrition Cascade Sankey ---
st.subheader("The Attrition Cascade")
st.caption("How accounts flow from active to closed -- and where to intervene")
st.plotly_chart(sankey_flow(
    sankey_labels, sankey_sources, sankey_targets, sankey_values,
    title='Account Health Flow',
), use_container_width=True, theme=None)

st.divider()

# --- What To Do First ---
st.subheader("What To Do First")
roadmap = [
    ("Launch win-back for competitor-active accounts", "$61M", "High", "Medium", "Q2"),
    ("Cross-sell campaign: single-product members", "$18M", "High", "Medium", "Q2"),
    ("Payroll capture campaign (Switch DD)", "$8.2M deposits", "High", "Low", "Q1"),
    ("Reg E opt-in push for low-opt-in segments", "$1.1M", "High", "Low", "Q1"),
    ("PIN-to-SIG routing optimization", "$420K", "Medium", "Low", "Q1"),
    ("Dormant reactivation program", "$2.1M", "High", "Medium", "Q2"),
    ("Power tier retention early-warning", "Protect $380M", "High", "Medium", "Q1"),
]

st.markdown(
    '<div style="display:grid; grid-template-columns:1fr auto auto auto auto; gap:0; '
    'font-size:13px; border:1px solid #1E293B; border-radius:10px; overflow:hidden;">'
    '<div style="padding:10px 14px; background:#1E293B; color:#94A3B8; font-weight:700;">Action</div>'
    '<div style="padding:10px 14px; background:#1E293B; color:#94A3B8; font-weight:700; text-align:center;">Impact</div>'
    '<div style="padding:10px 14px; background:#1E293B; color:#94A3B8; font-weight:700; text-align:center;">Priority</div>'
    '<div style="padding:10px 14px; background:#1E293B; color:#94A3B8; font-weight:700; text-align:center;">Effort</div>'
    '<div style="padding:10px 14px; background:#1E293B; color:#94A3B8; font-weight:700; text-align:center;">Timeline</div>'
    + ''.join(
        f'<div style="padding:10px 14px; border-top:1px solid #1E293B; color:#E2E8F0;">{action}</div>'
        f'<div style="padding:10px 14px; border-top:1px solid #1E293B; color:#6EE7B7; text-align:center; font-weight:600;">{impact}</div>'
        f'<div style="padding:10px 14px; border-top:1px solid #1E293B; text-align:center;">'
        f'<span style="background:{"rgba(248,113,113,0.12)" if pri=="High" else "rgba(251,191,36,0.12)"}; '
        f'color:{"#F87171" if pri=="High" else "#FBBF24"}; padding:2px 8px; border-radius:4px; '
        f'font-size:11px; font-weight:700;">{pri}</span></div>'
        f'<div style="padding:10px 14px; border-top:1px solid #1E293B; color:#94A3B8; text-align:center;">{effort}</div>'
        f'<div style="padding:10px 14px; border-top:1px solid #1E293B; color:#94A3B8; text-align:center;">{timeline}</div>'
        for action, impact, pri, effort, timeline in roadmap
    )
    + '</div>',
    unsafe_allow_html=True,
)

st.divider()

# --- RAG Scorecard (in expander) ---
with st.expander("Full RAG Scorecard (22 metrics across 9 categories)"):
    RAG_COLORS = {'Green': '#34D399', 'Amber': '#FBBF24', 'Red': '#F87171'}
    RAG_BG = {'Green': 'rgba(52,211,153,0.12)', 'Amber': 'rgba(251,191,36,0.12)',
              'Red': 'rgba(248,113,113,0.12)'}
    categories = scorecard_df['category'].unique()
    for i in range(0, len(categories), 3):
        batch = categories[i:i + 3]
        cols = st.columns(len(batch))
        for col, cat in zip(cols, batch):
            cat_rows = scorecard_df[scorecard_df['category'] == cat]
            cat_color = CAT_COLORS.get(cat, GEN_COLORS['primary'])
            with col:
                st.markdown(
                    f'<div style="background:{cat_color}; color:white; padding:8px 12px; '
                    f'border-radius:8px 8px 0 0; font-weight:700; font-size:13px;">{cat}</div>',
                    unsafe_allow_html=True)
                for _, row in cat_rows.iterrows():
                    rc = RAG_COLORS.get(row['rag'], '#64748B')
                    rb = RAG_BG.get(row['rag'], 'rgba(100,116,139,0.1)')
                    st.markdown(
                        f'<div style="border:1px solid #1E293B; border-top:none; padding:10px 12px; background:#111827;">'
                        f'<span style="color:#64748B; font-size:11px; text-transform:uppercase;">{row["metric"]}</span><br>'
                        f'<span style="font-size:22px; font-weight:700; color:#E2E8F0;">{row["value"]}</span>'
                        f'&nbsp;<span style="background:{rb}; color:{rc}; padding:2px 8px; border-radius:4px; '
                        f'font-size:11px; font-weight:700; border:1px solid {rc}33;">{row["rag"]}</span></div>',
                        unsafe_allow_html=True)
                st.markdown("")
