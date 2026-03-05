# feat: Visual Upgrade & Analysis Gap Fill

## Overview

The dashboard has a strong narrative foundation (6 story arcs, OEIA pattern, dark executive theme) but needs visual polish and analysis depth to match the notebook's quality. The notebook analysis (`/tmp/txn-visual-test/`) has **extensive built-out theming** (7 color palettes, conference-safe formatting, clean axes helpers) and a **sophisticated competition config** (multi-client layered structure with universal competitors, Fed District Top 25, client-specific CUs/banks, ecosystem detection). The dashboard should leverage these instead of reimplementing.

## Problem Statement

**Visual issues:**
1. `st.plotly_chart` calls lack `theme=None` -- Streamlit overrides our custom `txn_dark` Plotly template
2. No sparklines in KPI cards -- metrics show numbers without trend context
3. No "so what?" annotations on charts -- informational but not persuasive
4. 16 Detailed Analysis pages have `plot_bgcolor='white'` breaking dark theme
5. Remaining inline `np.random` calls in page files produce non-deterministic output
6. Cross-reference links are not clickable (text only, no navigation)
7. Muted text color (`#64748B`) borderline WCAG AA on dark background for small text

**Missing analysis (from notebook but not in dashboard):**
1. **Competition deep dive** -- notebook has 41 cells: threat quadrant, wallet share, material threats scatter, segment-level competitor analysis, recency analysis, spend vs frequency, category leaders, non-bank threats, account detail tables. Dashboard's `04_arc_loyalty.py` only surfaces ~30% of this.
2. **Seasonality decomposition** -- month-over-month pattern overlay
3. **Cohort/vintage analysis** -- new account tracking over time
4. **Day-of-week/hour-of-day heatmap** -- exists in notebook but not prominent in dashboard
5. **Peer benchmarks** -- comparison_metric exists but underused (only 3 metrics)
6. **Sections 23-24** -- gap in the analysis numbering (notebook goes 22 -> 25)

**Notebook theming not leveraged:**
- `GEN_COLORS` (7 palettes: bracket, age, engagement, account age, spend tier, swipe, competition category)
- `gen_clean_axes()`, `gen_fmt_pct()`, `gen_fmt_count()`, `gen_fmt_dollar()` -- conference-safe formatters
- `COMPETITOR_MERCHANTS` config with `tag_competitors()` function
- `CATEGORY_PALETTE` for competition visualization
- All of these are defined in the notebook cells but dashboard's `config.py` only partially mirrors them

## Proposed Solution

### Phase 1: Quick Visual Fixes (Low Effort, High Impact)

#### 1.1 Add `theme=None` to all `st.plotly_chart` calls
Search-and-replace across all page files. This ensures our `txn_dark` Plotly template renders as designed.

```python
# Before
st.plotly_chart(fig, use_container_width=True)

# After
st.plotly_chart(fig, use_container_width=True, theme=None)
```

**Files:** All 31 page files in `/private/tmp/txn-visual-test/dashboard/pages/`

#### 1.2 Remove `plot_bgcolor='white'` from Detailed Analysis pages
16 files have explicit white background overrides. Remove these so charts inherit the dark template.

**Files:** `02_portfolio_overview.py`, `03_merchant_analysis.py`, `04_mcc_categories.py`, `05_business_accounts.py`, `06_personal_accounts.py`, `07_competition.py`, `08_financial_services.py`, `09_ics_acquisition.py`, `10_campaign_analysis.py`, `11_branch_analysis.py`, `12_transaction_type.py`, `13_product_mix.py`, `16_interchange.py`, `17_rege_overdraft.py`, `20_segment_evolution.py`, `22_engagement_migration.py`

#### 1.3 Make cross-references clickable
Update `components.py:cross_reference()` to use `st.page_link()` for navigation between arcs.

```python
# components.py
def cross_reference(text, target_page, icon="arrow_forward"):
    st.page_link(f"pages/{target_page}", label=text, icon=f":material/{icon}:")
```

**File:** `components.py:96-113`, plus update all arc page calls to pass the target page filename

#### 1.4 Bump muted text color for WCAG AA
Change `#64748B` to `#94A3B8` in `config.py` for `GEN_COLORS['muted']` and in `app.py` CSS where used at small sizes.

**Files:** `config.py`, `app.py`

#### 1.5 Add CSS entry animations
Add `fadeSlideUp` keyframe animation with `prefers-reduced-motion` guard.

```css
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: no-preference) {
    div[data-testid="stMetric"] { animation: fadeSlideUp 0.3s ease-out; }
}
```

**File:** `app.py` CSS block

### Phase 2: Sync Notebook Theming into Dashboard

#### 2.1 Import all notebook palettes into `config.py`

The notebook's `01_general_theme` defines 7 palettes that the dashboard only partially has. Sync:

- `BRACKET_PALETTE` (8 spending bins)
- `AGE_PALETTE` + `AGE_ORDER` (6 age bands)
- `ACCT_AGE_PALETTE` + `ACCT_AGE_ORDER` (9 account age bands)
- `SPEND_TIER_PALETTE` + `SPEND_TIER_ORDER` (4 spend tiers)
- `SWIPE_PALETTE` + `SWIPE_ORDER` (5 swipe categories)
- `CATEGORY_PALETTE` from competition theme (9 competitor categories)

**Source:** `/tmp/txn-visual-test/01-general/01_general_theme` lines 21-98
**Source:** `/tmp/txn-visual-test/06-direct-competition/06_conference_theme` lines 6-16
**Target:** `/private/tmp/txn-visual-test/dashboard/config.py`

#### 2.2 Import competitor config structure

The notebook's `01_competitor_config` has a full multi-client competitor detection system with:
- `UNIVERSAL_COMPETITORS` (big nationals, digital banks)
- `UNIVERSAL_ECOSYSTEMS` (wallets, P2P, BNPL)
- `FED_DISTRICT_TOP_25` (12 districts, ~16 banks each)
- `CLIENT_CONFIGS` (per-client CUs, local banks)
- `tag_competitors()` function
- `discover_unmatched_financial()` function

Create a new `competitor_config.py` in the dashboard that imports/adapts this structure.

**Source:** `/tmp/txn-visual-test/06-direct-competition/01_competitor_config`
**Target:** `/private/tmp/txn-visual-test/dashboard/competitor_config.py` (new)

### Phase 3: Competition Dashboard Enhancement (Deep Dive)

The notebook's Section 06 has **41 cells** of competition analysis. The dashboard's `04_arc_loyalty.py` only surfaces ~30% of this. Full inventory below.

#### Competition Cell Inventory (41 cells)

**Already in dashboard (11 cells):** 01-06 (config/setup), 08 (top competitors bar), 09 (category donut), 10 (biz vs personal), 12 (bubble chart), 13 (threat quadrant), 22 (segment top competitors), 24 (segment heatmap), 33 (non-bank threats)

**NOT in dashboard -- HIGH PRIORITY (12 cells):**

| Cell | Visualization | Why It Matters | Chart Type |
|------|--------------|----------------|------------|
| 07 | KPI Dashboard | 4 headline cards: % accounts w/ competitors, % transactions, competitor count, avg txn/account. Currently no competition KPI row. | FancyBboxPatch cards |
| 14 | Engagement Scatter | Activity-per-account vs growth rate. Shows which competitors are **deepening** not just growing. | Scatter with quadrant lines |
| 15 | Momentum (diverging bar) | Growing competitors (red, right) vs declining (green, left). Top 8 growers + top 7 decliners. | Diverging horizontal bar |
| 16 | Opportunity Analysis | Bubble chart of DECLINING competitors. These are winback targets -- accounts ready to consolidate back. | Bubble scatter |
| 17 | Engagement Depth | Stacked bar: Heavy/Moderate/Light users per competitor. NEW metric showing how entrenched competitors are. | Stacked horizontal bar |
| 25 | At-Risk Accounts | Top 20 accounts where >50% spend goes to a single competitor. Per-competitor deep dive. Actionable retention targets. | Stacked horizontal bar |
| 26 | Spend Scatter | CU spend (x) vs competitor spend (y) per account. 50/50 diagonal. Quadrants: Winning/High Risk/Big Spenders/Low Value. | Scatter with colorbar |
| 27 | Recency Analysis | Days since last competitor transaction. Distribution + 30/90/180-day windows. Shows how RECENT the threat is. | Histogram with ref lines |
| 28 | Spend vs Frequency | Transaction count vs total spend per competitor, colored by recency. Engagement profile per competitor. | Scatter with colorbar |
| 29 | Wallet Share | CU spend + competitor spend stacked bar for top 20 accounts. Shows exact wallet split visually. | Stacked horizontal bar |
| 30 | Category Leaders | #1 competitor per category by total spend. Who dominates Big Nationals? Digital Banks? CUs? | Horizontal bar |
| 40 | Account Detail Tables | Top 25 accounts per competitor with metrics (total spend, txn count, recency, segment). | Interactive table |

**Partially in dashboard (5 cells):** 11 (monthly trend), 18 (competition aggregate), 23 (segment by category), 31 (spend ranking), 32 (material threats)

#### Implementation: Restructured Competition Tabs

Restructure `04_arc_loyalty.py` to have **5 tabs** (up from 3):

```
Competition | Wallet & Winback | Ecosystem Threats | Financial Services | ICS
```

**Tab 1: Competition** (existing + enhancements)
- Objection banner + headline insight (keep)
- Competition KPI row (NEW from cell 07): 4 metrics
- Threat Quadrant as hero chart (keep, already exists)
- Engagement Scatter (NEW from cell 14): activity vs growth
- Momentum diverging bar (NEW from cell 15): growers vs decliners
- Material Threats scatter (enhance from cell 32)
- Category Leaders bar (NEW from cell 30)
- Engagement Depth stacked bar (NEW from cell 17)

**Tab 2: Wallet & Winback** (NEW tab)
- Wallet Share bars (NEW from cell 29): CU vs competitor spend
- At-Risk Accounts (NEW from cell 25): per-competitor top 20
- Spend Scatter (NEW from cell 26): CU vs competitor quadrant
- Spend vs Frequency (NEW from cell 28): engagement profiles
- Recency Analysis (NEW from cell 27): how recent is the threat
- Opportunity Analysis (NEW from cell 16): declining competitors = winback targets

**Tab 3: Ecosystem Threats** (NEW tab, split from Financial Services)
- Non-Bank Threats bar (from cell 33)
- BNPL breakdown (Affirm, Klarna, Afterpay)
- Digital wallet penetration (Apple Pay, Venmo, Cash App)
- P2P volume (Zelle)
- Monthly ecosystem trend lines

**Tab 4: Financial Services** (keep existing)
**Tab 5: ICS Acquisition** (keep existing)

#### New Chart Functions for `charts.py`

```python
def diverging_bar(labels, positive_values, negative_values,
                  pos_label='Growing', neg_label='Declining',
                  pos_color='#F87171', neg_color='#34D399',
                  title='', height=400):
    """Diverging horizontal bar chart (e.g., momentum growers vs decliners)."""

def wallet_share_bar(labels, cu_values, comp_values,
                     cu_label='Your CU', comp_label='Competitor',
                     title='', height=400):
    """Stacked horizontal bar showing CU spend + competitor spend per account."""

def quadrant_scatter(data, x_col, y_col, size_col, color_col,
                     x_mid=None, y_mid=None,
                     quadrant_labels=('Watch', 'Defend', 'Monitor', 'Act Now'),
                     title='', height=500):
    """2x2 quadrant scatter with median crosshairs, sized bubbles, category colors."""

def engagement_depth_bar(labels, heavy, moderate, light,
                         title='Engagement Depth by Competitor', height=400):
    """Stacked horizontal bar showing Heavy/Moderate/Light user breakdown."""

def recency_histogram(values, reference_lines=[30, 90, 180],
                      title='Recency Distribution', height=350):
    """Histogram of days-since-last-activity with reference lines."""
```

#### New Demo Data for `demo_data.py`

```python
# Competition deep-dive data
competitor_engagement_depth = pd.DataFrame(...)  # Heavy/Moderate/Light per competitor
competitor_momentum = pd.DataFrame(...)          # Growth rate per competitor (positive + negative)
competitor_wallet_share = pd.DataFrame(...)      # CU spend vs competitor spend per account
competitor_recency = pd.DataFrame(...)           # Days since last competitor transaction
competitor_category_leaders = pd.DataFrame(...)  # Top competitor per category
competitor_opportunity = pd.DataFrame(...)       # Declining competitors (winback targets)
competitor_at_risk_accounts = pd.DataFrame(...)  # Top 20 accounts per competitor
```

#### Source Files

| Dashboard Target | Notebook Source |
|-----------------|----------------|
| Competition KPIs | `06-direct-competition/07_kpi_dashboard` |
| Engagement Scatter | `06-direct-competition/14_engagement_scatter` |
| Momentum Bar | `06-direct-competition/15_momentum` |
| Opportunity Bubbles | `06-direct-competition/16_opportunity` |
| Engagement Depth | `06-direct-competition/17_total_spend` |
| At-Risk Accounts | `06-direct-competition/25_at_risk_accounts` |
| Spend Scatter | `06-direct-competition/26_spend_scatter` |
| Recency Histogram | `06-direct-competition/27_recency_analysis` |
| Spend vs Frequency | `06-direct-competition/28_spend_vs_frequency` |
| Wallet Share | `06-direct-competition/29_wallet_share` |
| Category Leaders | `06-direct-competition/30_category_leaders` |
| Account Tables | `06-direct-competition/40_account_detail_table` |
| Competitor Config | `06-direct-competition/01_competitor_config` |
| Competition Palette | `06-direct-competition/06_conference_theme` |

### Phase 4: New Chart Types

#### 4.1 Sparkline KPI cards
Add to `charts.py`:
```python
def kpi_sparkline(label, value, delta, trend_data, color='#6EE7B7', height=160):
    """Plotly Indicator + mini trend line in a compact card."""
```

Replace top-of-page `st.metric` calls in arc pages with sparkline versions (where trend data exists in `demo_data.py`).

#### 4.2 Treemap for MCC categories
```python
def treemap(labels, parents, values, title='', height=450):
    """Hierarchical treemap for category breakdowns."""
```

Add to `03_arc_spending.py` MCC tab as the hero chart (replaces the flat donut).

#### 4.3 Radar chart for multi-factor risk
```python
def risk_radar(categories, values, benchmark=None, title='', height=380):
    """Spider/radar chart for multi-dimensional risk or performance profile."""
```

Add to `01_executive_close.py` as a "Portfolio Health" profile (replaces or supplements the gauge).

#### 4.4 "So what?" annotation helper
```python
def annotate_insight(fig, x, y, text, color='#6EE7B7'):
    """Add a callout annotation with arrow to any Plotly figure."""
```

Apply to the hero chart on each arc page (6 charts total).

### Phase 5: Missing Analysis Sections

#### 5.1 Section 23: Seasonality & Temporal Patterns
New analysis section and dashboard page combining:
- Month-over-month overlay (same month across years)
- Day-of-week transaction heatmap (already in notebook)
- Hour-of-day patterns
- Seasonal index visualization

**Files:**
- `/tmp/txn-visual-test/23-seasonality/` (new analysis cells)
- `/private/tmp/txn-visual-test/dashboard/pages/23_seasonality.py` (new page, added to Detailed Analysis nav)

#### 5.2 Section 24: Peer Benchmarks & Industry Comparison
New analysis section with:
- Cards per member vs NCUA average
- Interchange income per card vs peer group
- Active card ratio vs asset-class peers
- Transaction frequency benchmarks
- Payroll detection vs industry (already partially in Arc 4)

Uses `comparison_metric` and new `benchmark_bar` chart type (lollipop-style).

**Files:**
- `/tmp/txn-visual-test/24-peer-benchmarks/` (new analysis cells)
- `/private/tmp/txn-visual-test/dashboard/pages/24_peer_benchmarks.py` (new page)

### Phase 6: Infrastructure

#### 6.1 Move remaining `np.random` calls to `demo_data.py`
Audit all page files, move any inline random data generation to `demo_data.py` with `np.random.seed(42)`.

#### 6.2 Add `.streamlit/config.toml` dark theme + fonts
```toml
[theme]
base = "dark"
primaryColor = "#6EE7B7"
backgroundColor = "#0B1120"
secondaryBackgroundColor = "#111827"
textColor = "#E2E8F0"
font = "sans serif"
```

#### 6.3 Add `st.cache_data` to demo_data.py
Wrap DataFrame constructors to prevent re-creation on every page load.

#### 6.4 Fix `23_export.py` crash
The file imports `SECTIONS` from `config.py` which doesn't exist. Either delete this file (the arc-based `10_export.py` replaces it) or fix the import.

---

## Acceptance Criteria

### Phase 1 (Quick Fixes)
- [ ] All `st.plotly_chart` calls include `theme=None`
- [ ] No `plot_bgcolor='white'` in any file
- [ ] Cross-reference components navigate to target pages
- [ ] Muted text passes WCAG AA at 12px on `#0B1120`
- [ ] Entry animation on metric cards with reduced-motion guard

### Phase 2 (Theming Sync)
- [ ] All 7 notebook palettes available in `config.py`
- [ ] `competitor_config.py` with full competitor detection structure
- [ ] `CATEGORY_PALETTE` used in competition charts

### Phase 3 (Competition Enhancement -- 12 new visualizations)
- [ ] Competition KPI row (4 cards: % accounts, % txns, count, avg per account)
- [ ] Engagement Scatter (activity vs growth rate)
- [ ] Momentum diverging bar (growers vs decliners)
- [ ] Opportunity analysis (winback targets from declining competitors)
- [ ] Engagement depth stacked bar (Heavy/Moderate/Light per competitor)
- [ ] At-Risk Accounts detail (top 20 per competitor)
- [ ] Spend Scatter (CU vs competitor quadrant)
- [ ] Recency histogram (days since last competitor activity)
- [ ] Spend vs Frequency profiles
- [ ] Wallet Share bars (CU + competitor stacked)
- [ ] Category Leaders bar (#1 per category)
- [ ] Account detail tables (top 25 per competitor)
- [ ] New "Wallet & Winback" tab in `04_arc_loyalty.py`
- [ ] New "Ecosystem Threats" tab in `04_arc_loyalty.py`
- [ ] 5 new chart functions in `charts.py` (diverging_bar, wallet_share_bar, quadrant_scatter, engagement_depth_bar, recency_histogram)
- [ ] 7 new demo DataFrames in `demo_data.py`
- [ ] `competitor_config.py` with full layered detection structure from notebook

### Phase 4 (New Charts)
- [ ] KPI sparkline cards on at least 3 arc pages
- [ ] MCC treemap in Spending arc
- [ ] Risk radar on Executive Close
- [ ] "So what?" annotations on 6 hero charts

### Phase 5 (Missing Analysis)
- [ ] Section 23 (Seasonality) created with analysis cells + dashboard page
- [ ] Section 24 (Peer Benchmarks) created with analysis cells + dashboard page
- [ ] Both added to Detailed Analysis nav group

### Phase 6 (Infrastructure)
- [ ] Zero inline `np.random` in page files
- [ ] `config.toml` with dark theme
- [ ] `st.cache_data` on demo_data constructors
- [ ] `23_export.py` crash fixed

---

## Implementation Sequence

| Phase | Effort | Impact | Dependencies |
|-------|--------|--------|-------------|
| 1. Quick Visual Fixes | 2-3 hours | High | None |
| 2. Theme Sync | 1-2 hours | Medium | None |
| 3. Competition Enhancement (12 new viz) | 6-8 hours | Very High | Phase 2 (palettes) |
| 4. New Chart Types | 3-4 hours | High | Phase 1 (theme=None) |
| 5. Missing Analysis | 4-6 hours | Medium | Phase 2 |
| 6. Infrastructure | 2-3 hours | Medium | None |

**Recommended order:** Phase 1 -> Phase 6 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5

Phases 1, 6, and 2 can run in parallel as they touch different files.

---

## References

### Internal
- Notebook theme: `/tmp/txn-visual-test/01-general/01_general_theme`
- Competition config: `/tmp/txn-visual-test/06-direct-competition/01_competitor_config`
- Competition palette: `/tmp/txn-visual-test/06-direct-competition/06_conference_theme`
- Threat quadrant: `/tmp/txn-visual-test/06-direct-competition/13_threat_quadrant`
- Wallet share: `/tmp/txn-visual-test/06-direct-competition/29_wallet_share`
- Material threats: `/tmp/txn-visual-test/06-direct-competition/32_material_threats`
- Dashboard config: `/private/tmp/txn-visual-test/dashboard/config.py`
- Dashboard charts: `/private/tmp/txn-visual-test/dashboard/charts.py`
- Dashboard components: `/private/tmp/txn-visual-test/dashboard/components.py`

### External
- [Plotly Templates](https://plotly.com/python/templates/)
- [Streamlit Theming](https://docs.streamlit.io/develop/concepts/configuration/theming)
- [Plotly Indicators/Gauges](https://plotly.com/python/indicator/)
- [Plotly Treemaps](https://plotly.com/python/treemaps/)
- [Callahan CU Analytics](https://callahan.com/data-and-analytics-for-credit-unions/)
