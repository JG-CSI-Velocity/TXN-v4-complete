# ===========================================================================
# STORYLINE CONFIGURATION: 7 narrative decks + master export registry
# ===========================================================================
# Each storyline defines slide order, titles, cell references, KPI keys,
# and executive summary templates. Used by pptx_engine.py to build decks.

STORYLINES = {}

# ---------------------------------------------------------------------------
# Storyline 1: Executive Health Check (CORE - always present)
# ---------------------------------------------------------------------------
STORYLINES["executive_health_check"] = {
    "id": 1,
    "title": "Executive Health Check",
    "tagline": "Your Portfolio at a Glance",
    "type": "CORE",
    "audience": "CEO, Board, CFO",
    "duration_min": 15,
    "slides": [
        {
            "num": 1,
            "title": "Executive Health Check",
            "subtitle": "Your Portfolio at a Glance",
            "type": "title",
            "cell": None,
        },
        {
            "num": 2,
            "title": "Portfolio Foundation",
            "subtitle": "Key portfolio dimensions across the dataset period",
            "type": "chart",
            "cell": "01-general/02_portfolio_data",
        },
        {
            "num": 3,
            "title": "Monthly Trends",
            "subtitle": "Month-over-month portfolio activity",
            "type": "chart",
            "cell": "01-general/05_monthly_table",
        },
        {
            "num": 4,
            "title": "Executive Scorecard",
            "subtitle": "RAG status across all KPI dimensions",
            "type": "chart",
            "cell": "22-executive/02_scorecard_dashboard",
        },
        {
            "num": 5,
            "title": "RED KPI Spotlight",
            "subtitle": "KPIs requiring immediate attention",
            "type": "chart",
            "cell": "22-executive/01_scorecard_data",
            "filter": "red_only",
        },
        {
            "num": 6,
            "title": "Strategic Priorities",
            "subtitle": "Recommended focus areas ranked by impact",
            "type": "chart",
            "cell": "22-executive/03_strategic_priorities",
        },
        {
            "num": 7,
            "title": "Revenue Opportunity Waterfall",
            "subtitle": "Estimated annual impact across all analysis areas",
            "type": "chart",
            "cell": "22-executive/04_opportunity_waterfall",
        },
        {
            "num": 8,
            "title": "Competition Teaser",
            "subtitle": "Competitor presence in your member base",
            "type": "chart",
            "cell": "06-direct-competition/21_segment_summary",
        },
        {
            "num": 9,
            "title": "Attrition Teaser",
            "subtitle": "Members showing declining engagement",
            "type": "chart",
            "cell": "13-attrition/02_attrition_kpi",
        },
        {
            "num": 10,
            "title": "Relationship Teaser",
            "subtitle": "Product depth and cross-sell opportunity",
            "type": "chart",
            "cell": "18-relationship/02_relationship_kpi",
        },
        {
            "num": 11,
            "title": "Campaign ROI Teaser",
            "subtitle": "ARS mailer program effectiveness",
            "type": "chart",
            "cell": "09-ars-campaign/42_campaign_summary_slide",
        },
        {
            "num": 12,
            "title": "Segment Migration",
            "subtitle": "Engagement tier movement over time",
            "type": "chart",
            "cell": "19-segment-evolution/02_segment_kpi",
        },
        {
            "num": 13,
            "title": "Action Roadmap",
            "subtitle": "Phased implementation plan",
            "type": "chart",
            "cell": "22-executive/05_action_roadmap",
        },
        {
            "num": 14,
            "title": "Next Steps",
            "subtitle": "Immediate actions and follow-up timeline",
            "type": "text",
            "cell": None,
            "content_key": "next_steps",
        },
        {
            "num": 15,
            "title": "Data Sources & Methodology",
            "subtitle": "Dataset coverage and analytical approach",
            "type": "text",
            "cell": None,
            "content_key": "data_sources",
        },
    ],
    "exec_summary_template": (
        "Across {n_dimensions} KPI dimensions, {n_red} RED / {n_amber} AMBER. "
        "Combined annual opportunity: {total_opportunity}. "
        "Largest lever: {largest_lever}."
    ),
    "kpi_keys": [
        "scorecard_green_count",
        "scorecard_amber_count",
        "scorecard_red_count",
        "total_opportunity",
        "pct_accounts_at_risk",
        "largest_opportunity_area",
    ],
}

# ---------------------------------------------------------------------------
# Storyline 2: Competitive Threat & Wallet Share (CORE)
# ---------------------------------------------------------------------------
STORYLINES["competitive_threat"] = {
    "id": 2,
    "title": "Competitive Threat & Wallet Share",
    "tagline": "Who Else Has Your Members' Wallet?",
    "type": "CORE",
    "audience": "CEO, VP Marketing, VP Ops",
    "duration_min": 20,
    "slides": [
        {
            "num": 1,
            "title": "Competitive Threat & Wallet Share",
            "subtitle": "Who Else Has Your Members' Wallet?",
            "type": "title",
            "cell": None,
        },
        {
            "num": 2,
            "title": "Executive Summary",
            "subtitle": "Key competitive findings",
            "type": "exec_summary",
            "cell": None,
        },
        {
            "num": 3,
            "title": "Detection Methodology",
            "subtitle": "How we identify competitor transactions",
            "type": "chart",
            "cell": "06-direct-competition/01_competitor_config",
        },
        {
            "num": 4,
            "title": "Landscape Overview",
            "subtitle": "Competitor presence across the portfolio",
            "type": "chart",
            "cell": "06-direct-competition/02_competitor_detection",
        },
        {
            "num": 5,
            "title": "Wallet Share Segmentation",
            "subtitle": "Members categorized by competitor spend share",
            "type": "chart",
            "cell": "06-direct-competition/20_spend_segmentation",
        },
        {
            "num": 6,
            "title": "Segment Summary Table",
            "subtitle": "Account counts and spend by competitor tier",
            "type": "chart",
            "cell": "06-direct-competition/21_segment_summary",
        },
        {
            "num": 7,
            "title": "Top Competitors",
            "subtitle": "Most frequently detected competing institutions",
            "type": "chart",
            "cell": "06-direct-competition/22_segment_top_competitors",
        },
        {
            "num": 8,
            "title": "Category Breakdown",
            "subtitle": "Competitor activity by financial product category",
            "type": "chart",
            "cell": "06-direct-competition/23_segment_by_category",
        },
        {
            "num": 9,
            "title": "Risk Heatmap",
            "subtitle": "Competitor threat intensity by segment",
            "type": "chart",
            "cell": "06-direct-competition/24_segment_heatmap",
        },
        {
            "num": 10,
            "title": "At-Risk Accounts",
            "subtitle": "Accounts with highest competitor wallet share",
            "type": "chart",
            "cell": "06-direct-competition/25_at_risk_accounts",
        },
        {
            "num": 11,
            "title": "Spend Scatter: CU vs Competitor",
            "subtitle": "Your share vs competitor share per account",
            "type": "chart",
            "cell": "06-direct-competition/26_spend_scatter",
        },
        {
            "num": 12,
            "title": "Recency Analysis",
            "subtitle": "When members last transacted with competitors",
            "type": "chart",
            "cell": "06-direct-competition/27_recency_analysis",
        },
        {
            "num": 13,
            "title": "Wallet Share Distribution",
            "subtitle": "Distribution of competitor wallet share percentage",
            "type": "chart",
            "cell": "06-direct-competition/29_wallet_share",
        },
        {
            "num": 14,
            "title": "FinServ Leakage KPIs",
            "subtitle": "Financial services transaction leakage metrics",
            "type": "chart",
            "cell": "07-financial-services/06_kpi_dashboard",
        },
        {
            "num": 15,
            "title": "FinServ Opportunity",
            "subtitle": "Revenue opportunity from external FinServ recapture",
            "type": "chart",
            "cell": "07-financial-services/18_opportunity_waterfall",
        },
        {
            "num": 16,
            "title": "Top External Merchants",
            "subtitle": "Most popular external financial service providers",
            "type": "chart",
            "cell": "07-financial-services/09_top_merchants",
        },
        {
            "num": 17,
            "title": "FinServ Recency",
            "subtitle": "Recency of external financial transactions",
            "type": "chart",
            "cell": "07-financial-services/10_recency_heatmap",
        },
        {
            "num": 18,
            "title": "Multi-Product External",
            "subtitle": "Members using multiple external financial providers",
            "type": "chart",
            "cell": "07-financial-services/12_multi_product",
        },
        {
            "num": 19,
            "title": "Action Lists",
            "subtitle": "Exportable target lists for win-back campaigns",
            "type": "chart",
            "cell": "06-direct-competition/41_export_lists",
        },
        {
            "num": 20,
            "title": "Recommendations",
            "subtitle": "Strategic recommendations for competitive response",
            "type": "text",
            "cell": None,
            "content_key": "competitive_recommendations",
        },
    ],
    "exec_summary_template": (
        "{pct_with_competitor}% of members transact at competing FIs, "
        "{competitor_heavy_count} accounts in 'Competitor-Heavy' tier "
        "(>50% wallet share elsewhere)."
    ),
    "kpi_keys": [
        "competitors_detected",
        "pct_with_competitor_activity",
        "competitor_heavy_count",
        "pct_paying_external_finserv",
    ],
}

# ---------------------------------------------------------------------------
# Storyline 3: Member Retention & Attrition Risk (CORE)
# ---------------------------------------------------------------------------
STORYLINES["retention_attrition"] = {
    "id": 3,
    "title": "Member Retention & Attrition Risk",
    "tagline": "The Silent Departure",
    "type": "CORE",
    "audience": "VP Member Experience, CEO, Retention Team",
    "duration_min": 15,
    "slides": [
        {
            "num": 1,
            "title": "Member Retention & Attrition Risk",
            "subtitle": "The Silent Departure",
            "type": "title",
            "cell": None,
        },
        {
            "num": 2,
            "title": "Executive Summary",
            "subtitle": "Key retention findings",
            "type": "exec_summary",
            "cell": None,
        },
        {
            "num": 3,
            "title": "Attrition KPIs",
            "subtitle": "Risk at a glance",
            "type": "chart",
            "cell": "13-attrition/02_attrition_kpi",
        },
        {
            "num": 4,
            "title": "Risk Tier Distribution",
            "subtitle": "Portfolio breakdown by risk category",
            "type": "chart",
            "cell": "13-attrition/03_risk_distribution",
        },
        {
            "num": 5,
            "title": "Velocity Scatter",
            "subtitle": "Spend velocity ratio identifies declining members",
            "type": "chart",
            "cell": "13-attrition/04_velocity_scatter",
        },
        {
            "num": 6,
            "title": "Monthly Risk Progression",
            "subtitle": "How risk tiers evolve over time",
            "type": "chart",
            "cell": "13-attrition/05_monthly_progression",
        },
        {
            "num": 7,
            "title": "Risk by Demographics",
            "subtitle": "Attrition patterns across age and tenure groups",
            "type": "chart",
            "cell": "13-attrition/06_risk_by_demographics",
        },
        {
            "num": 8,
            "title": "Risk by Product",
            "subtitle": "Which products see the most attrition",
            "type": "chart",
            "cell": "13-attrition/07_risk_by_product",
        },
        {
            "num": 9,
            "title": "Risk by Competitor Activity",
            "subtitle": "Correlation between competitor presence and attrition",
            "type": "chart",
            "cell": "13-attrition/08_risk_by_competitor",
        },
        {
            "num": 10,
            "title": "Early Warning Signals",
            "subtitle": "Behavioral patterns that predict attrition",
            "type": "chart",
            "cell": "13-attrition/09_early_warning",
        },
        {
            "num": 11,
            "title": "Dormancy Progression",
            "subtitle": "Path from active to dormant accounts",
            "type": "chart",
            "cell": "13-attrition/10_dormancy_progression",
        },
        {
            "num": 12,
            "title": "Retention KPIs",
            "subtitle": "Account health classification summary",
            "type": "chart",
            "cell": "20-retention/02_retention_kpi",
        },
        {
            "num": 13,
            "title": "Churn by Segment",
            "subtitle": "Retention rates across engagement tiers",
            "type": "chart",
            "cell": "20-retention/03_churn_by_segment",
        },
        {
            "num": 14,
            "title": "Attrition Cost",
            "subtitle": "Financial impact of member departure",
            "type": "chart",
            "cell": "20-retention/04_attrition_cost",
        },
        {
            "num": 15,
            "title": "Dormancy Funnel",
            "subtitle": "Active to dormant conversion stages",
            "type": "chart",
            "cell": "20-retention/05_dormancy_funnel",
        },
        {
            "num": 16,
            "title": "Early Warning Map",
            "subtitle": "Visual map of early warning indicators",
            "type": "chart",
            "cell": "20-retention/06_early_warning",
        },
        {
            "num": 17,
            "title": "Engagement Migration KPIs",
            "subtitle": "Monthly engagement tier changes",
            "type": "chart",
            "cell": "21-engagement-migration/02_migration_kpi",
        },
        {
            "num": 18,
            "title": "Migration Matrix",
            "subtitle": "From-to movement between engagement tiers",
            "type": "chart",
            "cell": "21-engagement-migration/03_migration_matrix",
        },
        {
            "num": 19,
            "title": "Net Flow",
            "subtitle": "Monthly net migration between tiers",
            "type": "chart",
            "cell": "21-engagement-migration/04_net_flow",
        },
        {
            "num": 20,
            "title": "Migration by Segment",
            "subtitle": "Which segments gain and lose members",
            "type": "chart",
            "cell": "21-engagement-migration/05_migration_by_segment",
        },
        {
            "num": 21,
            "title": "At-Risk Export Lists",
            "subtitle": "Downloadable lists for targeted outreach",
            "type": "chart",
            "cell": "13-attrition/11_at_risk_export",
        },
        {
            "num": 22,
            "title": "Action Plan",
            "subtitle": "Recommended retention interventions",
            "type": "chart",
            "cell": "13-attrition/12_action_summary",
        },
    ],
    "exec_summary_template": (
        "{pct_at_risk}% at risk ({n_at_risk} members), "
        "{spend_at_risk} annual spend exposed. "
        "Velocity detection catches them 30-60 days before dormancy."
    ),
    "kpi_keys": [
        "pct_at_risk",
        "spend_at_risk",
        "closed_account_rate",
        "net_migration_direction",
    ],
}

# ---------------------------------------------------------------------------
# Storyline 4: Revenue Optimization (CORE)
# ---------------------------------------------------------------------------
STORYLINES["revenue_optimization"] = {
    "id": 4,
    "title": "Revenue Optimization",
    "tagline": "Finding Revenue in the Card Portfolio",
    "type": "CORE",
    "audience": "CFO, VP Card Services, VP Payments",
    "duration_min": 15,
    "slides": [
        {
            "num": 1,
            "title": "Revenue Optimization",
            "subtitle": "Finding Revenue in the Card Portfolio",
            "type": "title",
            "cell": None,
        },
        {
            "num": 2,
            "title": "Executive Summary",
            "subtitle": "Key revenue findings",
            "type": "exec_summary",
            "cell": None,
        },
        {
            "num": 3,
            "title": "Interchange KPIs",
            "subtitle": "PIN vs signature interchange overview",
            "type": "chart",
            "cell": "15-interchange/02_interchange_kpi",
        },
        {
            "num": 4,
            "title": "PIN vs SIG Trend",
            "subtitle": "Monthly interchange method trends",
            "type": "chart",
            "cell": "15-interchange/03_pin_sig_trend",
        },
        {
            "num": 5,
            "title": "SIG Ratio Analysis",
            "subtitle": "Signature transaction share over time",
            "type": "chart",
            "cell": "15-interchange/04_pin_sig_ratio",
        },
        {
            "num": 6,
            "title": "Revenue Waterfall",
            "subtitle": "Interchange revenue opportunity breakdown",
            "type": "chart",
            "cell": "15-interchange/05_revenue_waterfall",
        },
        {
            "num": 7,
            "title": "PIN-Heavy Accounts",
            "subtitle": "Accounts with highest PIN-to-SIG conversion opportunity",
            "type": "chart",
            "cell": "15-interchange/06_pin_heavy_accounts",
        },
        {
            "num": 8,
            "title": "IC by Demographics",
            "subtitle": "Interchange patterns across age and tenure",
            "type": "chart",
            "cell": "15-interchange/07_interchange_by_demographics",
        },
        {
            "num": 9,
            "title": "IC by Merchant",
            "subtitle": "Interchange revenue by top merchant categories",
            "type": "chart",
            "cell": "15-interchange/08_interchange_by_merchant",
        },
        {
            "num": 10,
            "title": "IC by Product",
            "subtitle": "Interchange performance by card product",
            "type": "chart",
            "cell": "15-interchange/09_interchange_by_product",
        },
        {
            "num": 11,
            "title": "Reg E KPIs",
            "subtitle": "Overdraft opt-in program overview",
            "type": "chart",
            "cell": "16-rege-overdraft/02_rege_kpi",
        },
        {
            "num": 12,
            "title": "Opt-In Trend",
            "subtitle": "Reg E opt-in rate over time",
            "type": "chart",
            "cell": "16-rege-overdraft/03_optin_trend",
        },
        {
            "num": 13,
            "title": "Opt-In Migration",
            "subtitle": "Members changing opt-in status",
            "type": "chart",
            "cell": "16-rege-overdraft/04_optin_migration",
        },
        {
            "num": 14,
            "title": "OD Limit Distribution",
            "subtitle": "Overdraft limit tiers across opted-in accounts",
            "type": "chart",
            "cell": "16-rege-overdraft/05_od_limit_distribution",
        },
        {
            "num": 15,
            "title": "OD Limit Trend",
            "subtitle": "Average overdraft limit over time",
            "type": "chart",
            "cell": "16-rege-overdraft/06_od_limit_trend",
        },
        {
            "num": 16,
            "title": "Reg E by Demographics",
            "subtitle": "Opt-in patterns across demographics",
            "type": "chart",
            "cell": "16-rege-overdraft/07_rege_by_demographics",
        },
        {
            "num": 17,
            "title": "Revenue Exposure",
            "subtitle": "Potential revenue impact from opt-in changes",
            "type": "chart",
            "cell": "16-rege-overdraft/08_rege_revenue_exposure",
        },
        {
            "num": 18,
            "title": "Reg E vs Balance",
            "subtitle": "Relationship between balance and opt-in status",
            "type": "chart",
            "cell": "16-rege-overdraft/09_rege_vs_balance",
        },
        {
            "num": 19,
            "title": "Payment Channel Overview",
            "subtitle": "Transaction distribution across payment channels",
            "type": "chart",
            "cell": "11-transaction-type/09_payment_channel_overview",
        },
        {
            "num": 20,
            "title": "ACH Deep Dive",
            "subtitle": "ACH transaction patterns and PFI indicators",
            "type": "chart",
            "cell": "11-transaction-type/10_ach_deep_dive",
        },
        {
            "num": 21,
            "title": "Channel Migration",
            "subtitle": "Members shifting between payment channels",
            "type": "chart",
            "cell": "11-transaction-type/12_channel_migration",
        },
        {
            "num": 22,
            "title": "Action Plan",
            "subtitle": "Revenue optimization recommendations",
            "type": "chart",
            "cell": "11-transaction-type/15_ach_chk_action_summary",
        },
    ],
    "exec_summary_template": (
        "Annual IC est. {annual_ic}, SIG ratio {sig_ratio}%. "
        "10% PIN shift = +{pin_shift_gain}/yr. "
        "Reg E opt-in {optin_rate}%."
    ),
    "kpi_keys": [
        "annual_ic_revenue",
        "sig_ratio_pct",
        "pin_shift_revenue_gain",
        "rege_optin_rate",
    ],
}

# ---------------------------------------------------------------------------
# Storyline 5: ARS Campaign Performance (SITUATIONAL)
# ---------------------------------------------------------------------------
STORYLINES["ars_campaign"] = {
    "id": 5,
    "title": "ARS Campaign Performance",
    "tagline": "Proving the Mailer Works",
    "type": "SITUATIONAL",
    "audience": "VP Marketing, CEO, Board",
    "duration_min": 15,
    "slides": [
        {
            "num": 1,
            "title": "ARS Campaign Performance",
            "subtitle": "Proving the Mailer Works",
            "type": "title",
            "cell": None,
        },
        {
            "num": 2,
            "title": "Executive Summary",
            "subtitle": "Campaign impact at a glance",
            "type": "chart",
            "cell": "09-ars-campaign/42_campaign_summary_slide",
        },
        {
            "num": 3,
            "title": "Program Reach KPIs",
            "subtitle": "Mail volume, response rates, and penetration",
            "type": "chart",
            "cell": "09-ars-campaign/02_campaign_kpi",
        },
        {
            "num": 4,
            "title": "Response Grouping",
            "subtitle": "Classification of responder vs non-responder",
            "type": "chart",
            "cell": "09-ars-campaign/03_campaign_response_grouping",
        },
        {
            "num": 5,
            "title": "Penetration",
            "subtitle": "Mailer reach across the portfolio",
            "type": "chart",
            "cell": "09-ars-campaign/04_campaign_penetration",
        },
        {
            "num": 6,
            "title": "Response by Wave",
            "subtitle": "Response rates across mailing waves",
            "type": "chart",
            "cell": "09-ars-campaign/05_response_by_wave",
        },
        {
            "num": 7,
            "title": "Response Rate Trend",
            "subtitle": "How response rates evolve over time",
            "type": "chart",
            "cell": "09-ars-campaign/06_response_rate_trend",
        },
        {
            "num": 8,
            "title": "Response Ladder",
            "subtitle": "Response tier breakdown",
            "type": "chart",
            "cell": "09-ars-campaign/07_response_ladder",
        },
        {
            "num": 9,
            "title": "Revenue Attribution",
            "subtitle": "Revenue impact attributed to mailer response",
            "type": "chart",
            "cell": "09-ars-campaign/08_response_revenue_attribution",
        },
        {
            "num": 10,
            "title": "DID Methodology Explainer",
            "subtitle": "Difference-in-Differences isolates true causal effect",
            "type": "chart",
            "cell": "09-ars-campaign/09_did_explainer",
        },
        {
            "num": 11,
            "title": "Cohort Lift KPIs",
            "subtitle": "Pre/post spend lift metrics",
            "type": "chart",
            "cell": "09-ars-campaign/11_cohort_lift_kpi",
        },
        {
            "num": 12,
            "title": "Before/After",
            "subtitle": "Responder spend trajectory pre vs post mailer",
            "type": "chart",
            "cell": "09-ars-campaign/12_cohort_before_after",
        },
        {
            "num": 13,
            "title": "DID Lift (Key Proof)",
            "subtitle": "The causal spend lift above counterfactual",
            "type": "chart",
            "cell": "09-ars-campaign/13_cohort_did_lift",
        },
        {
            "num": 14,
            "title": "Spend Persistence",
            "subtitle": "Does the lift sustain beyond initial activation?",
            "type": "chart",
            "cell": "09-ars-campaign/14_cohort_spend_persistence",
        },
        {
            "num": 15,
            "title": "Cumulative Impact (Hero Chart)",
            "subtitle": "Total cumulative spend difference since activation",
            "type": "chart",
            "cell": "09-ars-campaign/15_cohort_cumulative_spend",
        },
        {
            "num": 16,
            "title": "Counterfactual",
            "subtitle": "What would have happened without the mailer?",
            "type": "chart",
            "cell": "09-ars-campaign/16_cohort_counterfactual",
        },
        {
            "num": 17,
            "title": "Swipe KPIs + DID",
            "subtitle": "Transaction count lift analysis",
            "type": "chart",
            "cell": "09-ars-campaign/17_swipe_kpi",
        },
        {
            "num": 18,
            "title": "Swipe Migration",
            "subtitle": "Members migrating between swipe frequency tiers",
            "type": "chart",
            "cell": "09-ars-campaign/21_swipe_migration_matrix",
        },
        {
            "num": 19,
            "title": "Segment Spend Comparison",
            "subtitle": "Responder vs non-responder spend by segment",
            "type": "chart",
            "cell": "09-ars-campaign/24_segment_spend_comparison",
        },
        {
            "num": 20,
            "title": "Segment Trend Lines",
            "subtitle": "Spend trajectories by segment over time",
            "type": "chart",
            "cell": "09-ars-campaign/26_segment_spend_lines",
        },
        {
            "num": 21,
            "title": "Responder Profile",
            "subtitle": "Transaction behavior of responders",
            "type": "chart",
            "cell": "09-ars-campaign/30_responder_txn_profile",
        },
        {
            "num": 22,
            "title": "Responder Demographics",
            "subtitle": "Age and tenure profiles of top responders",
            "type": "chart",
            "cell": "09-ars-campaign/34_responder_account_age_chart",
        },
        {
            "num": 23,
            "title": "Program Effectiveness",
            "subtitle": "Overall program ROI and efficiency metrics",
            "type": "chart",
            "cell": "09-ars-campaign/37_program_effectiveness",
        },
        {
            "num": 24,
            "title": "Revenue Cascade + What-If",
            "subtitle": "Per-activation ROI and scenario modeling",
            "type": "chart",
            "cell": "09-ars-campaign/39_revenue_cascade",
        },
        {
            "num": 25,
            "title": "Opportunity Map",
            "subtitle": "Untapped segments for next campaign wave",
            "type": "chart",
            "cell": "09-ars-campaign/40_opportunity_map",
        },
    ],
    "exec_summary_template": (
        "{penetration_rate}% penetration across {n_waves} waves. "
        "DID lift: +{did_lift}/mo/acct above counterfactual. "
        "Best ROI segments: {best_segments}."
    ),
    "kpi_keys": [
        "unique_accounts_mailed",
        "penetration_rate",
        "avg_did_spend_lift",
        "persistence_rate",
    ],
}

# ---------------------------------------------------------------------------
# Storyline 6: Relationship Depth & Growth (CORE)
# ---------------------------------------------------------------------------
STORYLINES["relationship_growth"] = {
    "id": 6,
    "title": "Relationship Depth & Growth",
    "tagline": "From Single-Product to Primary FI",
    "type": "CORE",
    "audience": "VP Lending, VP Deposits, CEO, Product Team",
    "duration_min": 15,
    "slides": [
        {
            "num": 1,
            "title": "Relationship Depth & Growth",
            "subtitle": "From Single-Product to Primary FI",
            "type": "title",
            "cell": None,
        },
        {
            "num": 2,
            "title": "Executive Summary",
            "subtitle": "Key relationship findings",
            "type": "exec_summary",
            "cell": None,
        },
        {
            "num": 3,
            "title": "Relationship KPIs",
            "subtitle": "Product depth and engagement overview",
            "type": "chart",
            "cell": "18-relationship/02_relationship_kpi",
        },
        {
            "num": 4,
            "title": "Product Count Distribution",
            "subtitle": "How many products do your members hold?",
            "type": "chart",
            "cell": "18-relationship/03_product_count_bar",
        },
        {
            "num": 5,
            "title": "Single-Product Risk",
            "subtitle": "Flight risk from single-product members",
            "type": "chart",
            "cell": "18-relationship/04_single_product_risk",
        },
        {
            "num": 6,
            "title": "Cross-Sell Matrix",
            "subtitle": "Product combination affinity map",
            "type": "chart",
            "cell": "18-relationship/05_cross_sell_matrix",
        },
        {
            "num": 7,
            "title": "Value Curve",
            "subtitle": "Balance and interchange multiplier by product count",
            "type": "chart",
            "cell": "18-relationship/06_relationship_value",
        },
        {
            "num": 8,
            "title": "Leakage Opportunity",
            "subtitle": "Revenue leakage from shallow relationships",
            "type": "chart",
            "cell": "18-relationship/07_leakage_opportunity",
        },
        {
            "num": 9,
            "title": "Relationship by Demographics",
            "subtitle": "Product depth across age and tenure groups",
            "type": "chart",
            "cell": "18-relationship/08_relationship_by_demographics",
        },
        {
            "num": 10,
            "title": "Next-Best-Product",
            "subtitle": "Recommended cross-sell targets by current holdings",
            "type": "chart",
            "cell": "18-relationship/09_next_best_product",
        },
        {
            "num": 11,
            "title": "Payroll KPIs",
            "subtitle": "Direct deposit detection and PFI indicators",
            "type": "chart",
            "cell": "17-payroll/02_payroll_kpi",
        },
        {
            "num": 12,
            "title": "Payroll Distribution",
            "subtitle": "Payroll/DD presence across the portfolio",
            "type": "chart",
            "cell": "17-payroll/03_payroll_distribution",
        },
        {
            "num": 13,
            "title": "Payroll Value",
            "subtitle": "Members with payroll hold higher balances",
            "type": "chart",
            "cell": "17-payroll/04_payroll_value",
        },
        {
            "num": 14,
            "title": "Payroll by Demographics",
            "subtitle": "Direct deposit patterns across demographics",
            "type": "chart",
            "cell": "17-payroll/05_payroll_by_demographics",
        },
        {
            "num": 15,
            "title": "Payroll Processors",
            "subtitle": "Top payroll and direct deposit sources",
            "type": "chart",
            "cell": "17-payroll/06_payroll_processors",
        },
        {
            "num": 16,
            "title": "Payroll & Retention",
            "subtitle": "Payroll members show higher retention",
            "type": "chart",
            "cell": "17-payroll/07_payroll_retention",
        },
        {
            "num": 17,
            "title": "PFI Composite Score",
            "subtitle": "Multi-factor primary FI likelihood scoring",
            "type": "chart",
            "cell": "17-payroll/08_pfi_composite_score",
        },
        {
            "num": 18,
            "title": "PFI vs Competitor",
            "subtitle": "Your PFI status vs competitor positioning",
            "type": "chart",
            "cell": "17-payroll/09_pfi_vs_competitor",
        },
        {
            "num": 19,
            "title": "Balance KPIs",
            "subtitle": "Deposit balance overview",
            "type": "chart",
            "cell": "14-balance/02_balance_kpi",
        },
        {
            "num": 20,
            "title": "Balance vs Activity",
            "subtitle": "Correlation between balance and card activity",
            "type": "chart",
            "cell": "14-balance/05_balance_vs_activity",
        },
        {
            "num": 21,
            "title": "Deposit Flight Risk",
            "subtitle": "Balances at risk from declining engagement",
            "type": "chart",
            "cell": "14-balance/06_deposit_flight_risk",
        },
        {
            "num": 22,
            "title": "Action Plan",
            "subtitle": "Cross-sell and PFI growth recommendations",
            "type": "chart",
            "cell": "18-relationship/10_action_summary",
        },
    ],
    "exec_summary_template": (
        "Avg {avg_products} products/member, {pct_single_product}% single-product. "
        "3+ members = {balance_multiplier}x balance. "
        "{pct_with_payroll}% have detected payroll."
    ),
    "kpi_keys": [
        "avg_products_per_member",
        "pct_single_product",
        "balance_multiplier_3plus",
        "pct_with_payroll",
    ],
}

# ---------------------------------------------------------------------------
# Storyline 7: Portfolio Intelligence & Spending (SITUATIONAL)
# ---------------------------------------------------------------------------
STORYLINES["portfolio_intelligence"] = {
    "id": 7,
    "title": "Portfolio Intelligence & Spending",
    "tagline": "Know Your Members",
    "type": "SITUATIONAL",
    "audience": "VP Marketing, VP Ops, Branch Managers",
    "duration_min": 10,
    "slides": [
        {
            "num": 1,
            "title": "Portfolio Intelligence & Spending",
            "subtitle": "Know Your Members",
            "type": "title",
            "cell": None,
        },
        {
            "num": 2,
            "title": "Executive Summary",
            "subtitle": "Key portfolio intelligence findings",
            "type": "exec_summary",
            "cell": None,
        },
        {
            "num": 3,
            "title": "Portfolio KPIs",
            "subtitle": "Portfolio dimensions and activity metrics",
            "type": "chart",
            "cell": "01-general/02_portfolio_data",
        },
        {
            "num": 4,
            "title": "Monthly Trends",
            "subtitle": "Month-over-month activity patterns",
            "type": "chart",
            "cell": "01-general/05_monthly_table",
        },
        {
            "num": 5,
            "title": "Demographics",
            "subtitle": "Member age and demographic distribution",
            "type": "chart",
            "cell": "01-general/11_demographic_data",
        },
        {
            "num": 6,
            "title": "Age-Time Patterns",
            "subtitle": "Spending behavior across age and time",
            "type": "chart",
            "cell": "01-general/13_age_time_patterns",
        },
        {
            "num": 7,
            "title": "Age-Spending Profile",
            "subtitle": "Spend volume and ticket size by generation",
            "type": "chart",
            "cell": "01-general/14_age_spending_profile",
        },
        {
            "num": 8,
            "title": "Age Bracket Comparison",
            "subtitle": "Generational spending differences",
            "type": "chart",
            "cell": "01-general/15_age_bracket_comparison",
        },
        {
            "num": 9,
            "title": "Account Lifecycle",
            "subtitle": "Activity patterns by account age",
            "type": "chart",
            "cell": "01-general/23_account_age_data",
        },
        {
            "num": 10,
            "title": "Time to First Transaction",
            "subtitle": "How quickly new accounts activate",
            "type": "chart",
            "cell": "01-general/25_time_to_first_txn",
        },
        {
            "num": 11,
            "title": "Spend by Account Age",
            "subtitle": "Spending maturity curve",
            "type": "chart",
            "cell": "01-general/26_spend_by_account_age",
        },
        {
            "num": 12,
            "title": "New Account Profile",
            "subtitle": "Characteristics of recently opened accounts",
            "type": "chart",
            "cell": "01-general/27_new_account_profile",
        },
        {
            "num": 13,
            "title": "Lifecycle Summary",
            "subtitle": "Key lifecycle stage metrics",
            "type": "chart",
            "cell": "01-general/28_lifecycle_summary",
        },
        {
            "num": 14,
            "title": "Top Categories (MCC)",
            "subtitle": "Where your members spend the most",
            "type": "chart",
            "cell": "03-mcc-code/03_mcc_top20_bar",
        },
        {
            "num": 15,
            "title": "Category Concentration",
            "subtitle": "Portfolio spend concentration across categories",
            "type": "chart",
            "cell": "03-mcc-code/06_mcc_concentration",
        },
        {
            "num": 16,
            "title": "Category Trends",
            "subtitle": "Category spend evolution over time",
            "type": "chart",
            "cell": "03-mcc-code/07_mcc_trend",
        },
        {
            "num": 17,
            "title": "Categories by Age & Tenure",
            "subtitle": "Spending categories differ by generation",
            "type": "chart",
            "cell": "03-mcc-code/08_mcc_by_age_band",
        },
        {
            "num": 18,
            "title": "Seasonal Patterns",
            "subtitle": "Monthly and seasonal spending cycles",
            "type": "chart",
            "cell": "03-mcc-code/12_mcc_seasonal",
        },
        {
            "num": 19,
            "title": "Spending Diversity",
            "subtitle": "How many categories do members use?",
            "type": "chart",
            "cell": "03-mcc-code/13_mcc_diversity",
        },
        {
            "num": 20,
            "title": "Segment Evolution",
            "subtitle": "Engagement tier changes over time",
            "type": "chart",
            "cell": "19-segment-evolution/02_segment_kpi",
        },
        {
            "num": 21,
            "title": "Upgraders vs Degraders",
            "subtitle": "Who improved and who declined?",
            "type": "chart",
            "cell": "19-segment-evolution/05_upgraders_vs_degraders",
        },
        {
            "num": 22,
            "title": "Action Plan",
            "subtitle": "Marketing intelligence recommendations",
            "type": "chart",
            "cell": "03-mcc-code/15_mcc_action_summary",
        },
    ],
    "exec_summary_template": (
        "{total_accounts} accounts, {total_merchants} merchants, "
        "{total_categories} categories. "
        "{pct_upgraded}% upgraded engagement segments. "
        "New accounts activate within {time_to_first_txn} months."
    ),
    "kpi_keys": [
        "total_spend",
        "top_3_categories",
        "pct_upgraded_vs_degraded",
        "time_to_first_txn",
    ],
}

# ---------------------------------------------------------------------------
# Presentation order (full client review)
# ---------------------------------------------------------------------------
PRESENTATION_ORDER = [
    "executive_health_check",
    "competitive_threat",
    "retention_attrition",
    "revenue_optimization",
    "relationship_growth",
    "ars_campaign",
    "portfolio_intelligence",
]

# ---------------------------------------------------------------------------
# Classification helper
# ---------------------------------------------------------------------------
CORE_STORYLINES = [k for k, v in STORYLINES.items() if v["type"] == "CORE"]
SITUATIONAL_STORYLINES = [k for k, v in STORYLINES.items() if v["type"] == "SITUATIONAL"]


def get_all_cell_refs():
    """Return set of all cell references across all storylines."""
    cells = set()
    for storyline in STORYLINES.values():
        for slide in storyline["slides"]:
            if slide.get("cell"):
                cells.add(slide["cell"])
    return cells


def get_storyline_by_id(storyline_id):
    """Look up storyline config by numeric ID (1-7)."""
    for key, config in STORYLINES.items():
        if config["id"] == storyline_id:
            return key, config
    return None, None
