import streamlit as st

st.set_page_config(
    page_title="TXN Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -- Inject fonts + dark executive CSS --
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,500;0,9..40,700;1,9..40,400&family=Outfit:wght@300;400;600;700&display=swap');

/* ---- Base typography ---- */
html, body, [class*="css"] {
    font-family: 'DM Sans', 'Outfit', system-ui, -apple-system, sans-serif !important;
}
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Outfit', 'DM Sans', sans-serif !important;
    color: #E2E8F0 !important;
    letter-spacing: -0.02em;
}
h1 { font-weight: 700 !important; font-size: 1.75rem !important; }
h2 { font-weight: 600 !important; font-size: 1.35rem !important; color: #CBD5E1 !important; }
h3 { font-weight: 600 !important; font-size: 1.1rem !important; color: #94A3B8 !important; }

/* ---- Page container ---- */
.block-container {
    padding-top: 1.5rem !important;
    max-width: 100% !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}

/* ---- Metric cards: glass effect ---- */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(30,41,59,0.7) 0%, rgba(15,23,42,0.5) 100%) !important;
    border: 1px solid rgba(110,231,183,0.12) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    border-color: rgba(110,231,183,0.3) !important;
    box-shadow: 0 0 20px rgba(110,231,183,0.06);
}
div[data-testid="stMetric"] label {
    font-size: 11px !important;
    font-weight: 500 !important;
    color: #94A3B8 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-family: 'Outfit', sans-serif !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #E2E8F0 !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
    font-size: 12px !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricDelta"] svg { display: inline; }
div[data-testid="stMetricDelta"][style*="color: green"],
div[data-testid="stMetricDelta"] span[style*="color: green"] {
    color: #34D399 !important;
}

/* ---- Sidebar styling ---- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #0B1120 100%) !important;
    border-right: 1px solid rgba(110,231,183,0.08);
}
section[data-testid="stSidebar"] > div { padding-top: 1rem; }
section[data-testid="stSidebar"] .stMarkdown p {
    color: #94A3B8 !important;
    font-size: 13px;
}
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #6EE7B7 !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
}

/* Sidebar nav links */
section[data-testid="stSidebar"] a {
    color: #94A3B8 !important;
    transition: color 0.15s ease;
}
section[data-testid="stSidebar"] a:hover {
    color: #6EE7B7 !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNavItems"] li[aria-selected="true"] a {
    color: #6EE7B7 !important;
    font-weight: 600;
}

/* ---- Tabs ---- */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #1E293B; }
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    border-radius: 8px 8px 0 0;
    padding: 8px 16px;
    font-weight: 500;
    color: #94A3B8 !important;
    border-bottom: 2px solid transparent;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #6EE7B7 !important;
    border-bottom: 2px solid #6EE7B7;
    background: rgba(110,231,183,0.05) !important;
}

/* ---- Dividers ---- */
hr { border-color: #1E293B !important; opacity: 0.6; }

/* ---- Expander ---- */
details { border: 1px solid #1E293B !important; border-radius: 8px; }
details summary { color: #94A3B8 !important; }

/* ---- Info boxes ---- */
div[data-testid="stAlert"] {
    background: rgba(96,165,250,0.06) !important;
    border: 1px solid rgba(96,165,250,0.15) !important;
    border-radius: 8px !important;
    color: #94A3B8 !important;
}

/* ---- DataFrame ---- */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* ---- Plotly chart containers ---- */
div[data-testid="stPlotlyChart"] {
    border-radius: 12px;
    background: rgba(30,41,59,0.25);
    border: 1px solid rgba(148,163,184,0.06);
    padding: 8px;
}

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0B1120; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }

/* ---- Caption ---- */
.stCaption, div[data-testid="stCaptionContainer"] p {
    color: #475569 !important;
    font-size: 12px !important;
    letter-spacing: 0.02em;
}

/* ---- Entry animations ---- */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
div[data-testid="stMetric"],
div[data-testid="stPlotlyChart"],
div[data-testid="stAlert"] {
    animation: fadeSlideUp 0.35s ease-out both;
}
div[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.05s; }
div[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.10s; }
div[data-testid="stMetric"]:nth-child(4) { animation-delay: 0.15s; }
</style>
""", unsafe_allow_html=True)

# -- Sidebar branding --
with st.sidebar:
    st.markdown("### TXN Dashboard")
    st.markdown("""
<div style="
    margin: 8px 0 16px 0;
    padding: 12px 14px;
    background: linear-gradient(135deg, rgba(110,231,183,0.08) 0%, rgba(96,165,250,0.06) 100%);
    border: 1px solid rgba(110,231,183,0.12);
    border-radius: 10px;
    font-size: 13px;
    line-height: 1.6;
">
    <span style="color:#6EE7B7; font-weight:600;">CoastHills FCU</span><br>
    <span style="color:#94A3B8;">Jan 2025 -- Jan 2026</span><br>
    <span style="color:#94A3B8;">33,205 accounts</span><br>
    <span style="color:#94A3B8;">5.89M transactions</span>
</div>
""", unsafe_allow_html=True)
    st.divider()

# Navigation -- Story Arc Structure + Full Analysis
pages = {
    "Overview": [
        st.Page("pages/00_data_upload.py", title="Data Upload"),
        st.Page("pages/01_executive_close.py", title="The Bottom Line", default=True),
    ],
    "Story Arcs": [
        st.Page("pages/02_arc_portfolio.py", title="Portfolio Illusions"),
        st.Page("pages/03_arc_spending.py", title="Where the Money Goes"),
        st.Page("pages/04_arc_loyalty.py", title="The Loyalty Myth"),
        st.Page("pages/05_arc_revenue.py", title="The Revenue You're Missing"),
        st.Page("pages/06_arc_attrition.py", title="The Attrition Cascade"),
        st.Page("pages/07_arc_deepening.py", title="Deepening or Decline"),
    ],
    "Operations": [
        st.Page("pages/08_branch.py", title="Branch Performance"),
        st.Page("pages/09_campaign.py", title="Campaign Effectiveness"),
    ],
    "Detailed Analysis": [
        st.Page("pages/01_executive_summary.py", title="Executive Summary"),
        st.Page("pages/02_portfolio_overview.py", title="Portfolio Overview"),
        st.Page("pages/03_merchant_analysis.py", title="Merchant Analysis"),
        st.Page("pages/04_mcc_categories.py", title="MCC Categories"),
        st.Page("pages/05_business_accounts.py", title="Business Accounts"),
        st.Page("pages/06_personal_accounts.py", title="Personal Accounts"),
        st.Page("pages/07_competition.py", title="Competition"),
        st.Page("pages/08_financial_services.py", title="Financial Services"),
        st.Page("pages/09_ics_acquisition.py", title="ICS Acquisition"),
        st.Page("pages/10_campaign_analysis.py", title="Campaign Analysis"),
        st.Page("pages/11_branch_analysis.py", title="Branch Analysis"),
        st.Page("pages/12_transaction_type.py", title="Transaction Type"),
        st.Page("pages/13_product_mix.py", title="Product Mix"),
        st.Page("pages/14_attrition_risk.py", title="Attrition Risk"),
        st.Page("pages/15_balance_analysis.py", title="Balance Analysis"),
        st.Page("pages/16_interchange.py", title="Interchange"),
        st.Page("pages/17_rege_overdraft.py", title="Reg E & Overdraft"),
        st.Page("pages/18_payroll_pfi.py", title="Payroll & PFI"),
        st.Page("pages/19_relationship.py", title="Relationship Depth"),
        st.Page("pages/20_segment_evolution.py", title="Segment Evolution"),
        st.Page("pages/21_retention.py", title="Retention & Churn"),
        st.Page("pages/22_engagement_migration.py", title="Engagement Migration"),
    ],
    "Export": [
        st.Page("pages/10_export.py", title="Export Deck"),
    ],
}

pg = st.navigation(pages)
pg.run()
