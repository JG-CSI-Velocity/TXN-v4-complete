# feat: Internal Team Dashboard (Streamlit)

Convert the 301-cell Jupyter notebook into an internal team web dashboard for credit union data analysts.

## Overview

The TXN-v4-complete notebook produces conference-quality debit card transaction analysis across 23 sections (301 cells). Today, running the analysis requires Jupyter expertise and manual cell execution. This plan converts it into a self-service Streamlit web app where team members can upload data, run analysis, explore results interactively, and export PPTX decks -- all from a browser.

## Problem Statement

- Only notebook-literate analysts can run the pipeline
- Cell execution is manual, sequential, and error-prone (301 cells, ~10 min runtime)
- No parameterization without editing code (client config, thresholds, competitor lists)
- No multi-user access -- one person runs the notebook at a time
- Chart output is static images; no interactive exploration
- PPTX export requires a separate manual process

## Proposed Solution: Streamlit Multi-Page App

**Why Streamlit:**
- Lowest learning curve for a Python team
- Largest ecosystem (972K downloads/month) -- problems are Google-able
- `st.navigation` with dictionary grouping handles 23 sections cleanly
- `@st.cache_resource` makes 5.8M rows feasible (shared memory, no per-session copies)
- `@st.fragment` solves partial-page-update needs
- Docker deployment behind nginx for internal access
- OIDC or `streamlit-authenticator` for team auth

**Alternatives considered:**
- **Panel**: Better large-data perf (Datashader), but steeper learning curve, smaller community
- **Marimo**: Closest to notebook feel, but younger project, less production-proven
- **Voila**: Zero migration effort but ~2GB RAM per user -- doesn't scale
- **Dash**: Callback paradigm too far from notebook mental model
- **FastAPI+React**: Massively overengineered for 5-10 internal users

---

## Technical Approach

### Architecture

```
txn-dashboard/
    app.py                          # Entrypoint: st.navigation + global sidebar
    config.py                       # GEN_COLORS, palettes, constants
    data_loader.py                  # @st.cache_resource loaders
    pages/
        00_data_upload.py           # File upload + validation + pipeline trigger
        01_executive_summary.py     # Scorecard grid (from 22-executive)
        02_portfolio_overview.py    # From 01-general
        03_merchant_analysis.py     # From 02-merchant
        04_mcc_categories.py        # From 03-mcc-code
        05_business_accounts.py     # From 04-business-accts
        06_personal_accounts.py     # From 05-personal-accts
        07_competition.py           # From 06-direct-competition
        08_financial_services.py    # From 07-financial-services
        09_ics_acquisition.py       # From 08-ics-acquisition
        10_campaign_analysis.py     # From 09-ars-campaign
        11_branch_analysis.py       # From 10-branch
        12_transaction_type.py      # From 11-transaction-type
        13_product_mix.py           # From 12-product
        14_attrition_risk.py        # From 13-attrition
        15_balance_analysis.py      # From 14-balance
        16_interchange.py           # From 15-interchange
        17_rege_overdraft.py        # From 16-rege-overdraft
        18_payroll_pfi.py           # From 17-payroll
        19_relationship.py          # From 18-relationship
        20_segment_evolution.py     # From 19-segment-evolution
        21_retention.py             # From 20-retention
        22_engagement_migration.py  # From 21-engagement-migration
        23_export.py                # PPTX/PDF export page
    pipelines/
        setup.py                    # Wraps 00-setup logic
        general.py                  # Wraps 01-general
        merchants.py                # Wraps 02-merchant data pipeline
        ...                         # One module per section's _data cell
    utils/
        charts.py                   # Reusable chart builders (KPI cards, bars, heatmaps)
        formatters.py               # gen_fmt_dollar, gen_fmt_pct, etc.
        export_pptx.py              # PPTX generation with python-pptx
        theme.py                    # Streamlit theme + CSS overrides
    assets/
        logo.png
        template.pptx               # Branded slide template
    .streamlit/
        config.toml                 # Server config (maxUploadSize, theme)
    Dockerfile
    requirements.txt
```

### Data Flow

```
Upload Files (CSV + ODDD Excel)
    |
    v
Pipeline Runner (setup.py)
    |-- Loads transaction CSVs -> combined_df (5.8M rows)
    |-- Loads ODDD Excel -> rewards_df (33K rows, 235+ cols)
    |-- Merchant consolidation
    |-- Business/personal split
    |-- Stores in st.session_state
    |
    v
Section Pipelines (run on demand per page)
    |-- Each page calls its pipeline module
    |-- Pipeline checks session_state for upstream DataFrames
    |-- Produces section-specific DataFrames (cached)
    |
    v
Visualization (per page)
    |-- KPI cards (Plotly or matplotlib via st.pyplot)
    |-- Interactive charts (Plotly via st.plotly_chart)
    |-- Styled tables (st.dataframe with pandas Styler)
    |-- Action summary tables
```

### Key Design Decisions

1. **Parquet intermediate format**: After initial CSV/Excel load, save as Parquet for 10-20x faster subsequent loads. First run is slow (~60s); subsequent runs load from Parquet in ~3s.

2. **`@st.cache_resource` for raw data**: The 5.8M-row `combined_df` is loaded once into shared memory. All sessions reference the same object. No per-user copies.

3. **Lazy section execution**: Section pipelines run only when the user navigates to that page, not all 23 at startup. The executive scorecard page triggers all pipelines since it aggregates everything.

4. **Plotly for new charts, matplotlib for legacy**: Migrate the 10 most-used chart types to Plotly for interactivity. Keep remaining matplotlib charts via `st.pyplot()` for v1 speed.

5. **Fragment-based interactivity**: Each chart section wrapped in `@st.fragment` so slider/filter changes don't reload the entire page.

---

## Implementation Phases

### Phase 1: Foundation (Week 1-2)

**Goal**: Working app that loads data and shows the executive scorecard.

- [ ] `app.py` -- Streamlit entrypoint with `st.navigation` sidebar groups
- [ ] `config.py` -- Port `GEN_COLORS`, all palettes, constants from `01-general/01_general_theme`
- [ ] `data_loader.py` -- File upload + Parquet caching + `@st.cache_resource` loader
- [ ] `pipelines/setup.py` -- Port `00-setup` cells (data loading, merchant consolidation, ODDD merge, business/personal split)
- [ ] `pages/00_data_upload.py` -- File upload page with validation:
  - Transaction CSV/TXT upload (or select from server directory)
  - ODDD Excel upload
  - Client ID/Name selection dropdown
  - Progress bar during pipeline execution
  - Data quality summary (row counts, date range, missing values)
- [ ] `pages/01_executive_summary.py` -- Port `22-executive` scorecard as the landing page
- [ ] `utils/formatters.py` -- Port `gen_fmt_dollar`, `gen_fmt_pct`, `gen_fmt_count`
- [ ] `.streamlit/config.toml` -- Theme colors, maxUploadSize=1024, wide layout
- [ ] `Dockerfile` + `requirements.txt`

**Acceptance criteria:**
- [ ] User can upload CSV + ODDD files from browser
- [ ] Pipeline runs with progress indicator (~60s for 5.8M rows)
- [ ] Executive scorecard renders with RAG indicators
- [ ] Subsequent page loads use cached data (instant)
- [ ] Works in Docker

### Phase 2: Core Sections (Week 3-4)

**Goal**: All 23 sections navigable with existing chart logic.

- [ ] Port each section's `_data` cell into `pipelines/<section>.py`
- [ ] Port each section's visualization cells into `pages/<section>.py`
- [ ] Initial approach: use `st.pyplot(fig)` for all matplotlib charts (static but fast to migrate)
- [ ] Port styled HTML tables to `st.dataframe()` with pandas Styler
- [ ] Port action summary tables
- [ ] Add section-level data guards (show "Run pipeline first" message if data missing)
- [ ] Add sidebar navigation groups:
  - **Overview**: Executive Summary, Portfolio Overview
  - **Spending Analysis**: Merchants, MCC Categories, Business, Personal
  - **Competition & Growth**: Competition, Financial Services, ICS Acquisition
  - **Campaign & Engagement**: Campaign, Segment Evolution, Engagement Migration
  - **Risk & Revenue**: Attrition, Balance, Interchange, Retention
  - **Operations**: Branch, Transaction Type, Product, Reg E, Payroll, Relationship
  - **Export**: PPTX Export

**Acceptance criteria:**
- [ ] All 23 sections render their charts and tables
- [ ] Navigation between sections preserves data state
- [ ] Each section shows KPI cards + charts + action summary
- [ ] Pages that need upstream sections show clear dependency messages

### Phase 3: Interactivity & Parameters (Week 5-6)

**Goal**: Users can adjust analysis parameters without editing code.

- [ ] Global sidebar widgets:
  - Date range filter (applied to all sections)
  - Business/Personal/All toggle
  - Client selector dropdown
- [ ] Section-specific widgets:
  - **Competition**: Editable local competitor lists (multiselect + text input)
  - **Campaign**: Responder threshold adjustment
  - **Engagement**: Tier percentile sliders (Power/Heavy/Moderate/Light/Dormant)
  - **Attrition**: Velocity threshold adjustment
  - **Executive**: RAG threshold editors
- [ ] Migrate top 10 charts to Plotly for hover/zoom:
  - Monthly trend lines (portfolio, competition, campaign)
  - Scatter plots (attrition velocity, early warning)
  - Heatmaps (migration matrix, hourly activity)
  - Bar charts (top merchants, branch comparison)
- [ ] Wrap interactive chart sections in `@st.fragment`

**Acceptance criteria:**
- [ ] Date range filter updates all downstream charts
- [ ] Competitor list changes flow through competition analysis
- [ ] Engagement tier adjustments recompute tier assignments
- [ ] Plotly charts support hover tooltips and zoom

### Phase 4: Export & Polish (Week 7-8)

**Goal**: Conference-ready PPTX export and production polish.

- [ ] `utils/export_pptx.py` -- PPTX generation pipeline:
  - Branded template with logo, fonts, colors
  - Section selector (choose which sections to include)
  - One slide per KPI dashboard (4-card layout)
  - One slide per key chart (conclusion headline, not label)
  - Executive summary slide (scorecard grid)
  - Action roadmap slide
  - Speaker notes with key findings
- [ ] `pages/23_export.py` -- Export page:
  - Section checkbox selector
  - Preview mode (thumbnail grid of selected slides)
  - `st.download_button` for PPTX download
  - CSV data export (filtered data tables)
- [ ] Authentication:
  - `streamlit-authenticator` with YAML credentials for <20 users
  - OR OIDC integration if team uses Google/Azure AD SSO
- [ ] Error handling:
  - Graceful pipeline failure messages (which step failed, why)
  - Data validation warnings (unexpected columns, missing months, NaN rates)
  - Session timeout handling (auto-save state to disk)
- [ ] Performance tuning:
  - Profile and optimize slowest pipeline steps
  - Add Parquet auto-save after first CSV load
  - Memory monitoring (`st.sidebar` memory usage indicator)

**Acceptance criteria:**
- [ ] PPTX export produces conference-quality deck
- [ ] Slides follow executive-data-presentation guidelines (conclusion headlines, direct labels)
- [ ] Authentication gate prevents unauthorized access
- [ ] No unhandled errors -- all failures show actionable messages
- [ ] App works reliably with 5-10 concurrent users

---

## User Flows

### Flow 1: First-Time Data Load

```
Login -> Data Upload page -> Upload transaction CSVs + ODDD Excel
    -> Select Client ID from dropdown (auto-populates name)
    -> Click "Run Pipeline"
    -> Progress bar: Loading files... Consolidating merchants... Merging ODDD...
    -> Success: "Loaded 5,885,334 transactions across 33,205 accounts (Jan25-Jan26)"
    -> Auto-redirect to Executive Summary
```

### Flow 2: Returning User (Cached Data)

```
Login -> Executive Summary (instant, data cached from last session)
    -> Navigate sections via sidebar
    -> Adjust parameters (date range, thresholds)
    -> Charts update in-place
```

### Flow 3: Multi-Client Switch

```
Sidebar -> Client dropdown -> Select new client
    -> Prompt: "Switch to [ClientName]? Current analysis will be replaced."
    -> Confirm -> Data upload page with new client context
    -> Upload new client's files -> Pipeline runs -> New analysis
```

### Flow 4: PPTX Export

```
Export page -> Select sections (checkboxes, default: all)
    -> Click "Generate Deck"
    -> Progress: Building slides... (10-30s)
    -> Preview: thumbnail grid of generated slides
    -> "Download PPTX" button
    -> File saves to browser downloads
```

### Flow 5: Parameter Adjustment

```
Competition page -> Sidebar: "Local Competitors" multiselect
    -> Add/remove competitors from list
    -> Click "Rerun Analysis"
    -> Competition charts update with new competitor set
    -> Changes persist in session (not saved to disk unless user clicks "Save Config")
```

---

## Technical Considerations

### Performance

- **Initial load**: ~60s for 5.8M CSV rows. Mitigated by Parquet cache (3s on subsequent loads).
- **Per-page render**: <5s per section (cached pipeline + chart render).
- **Memory**: ~2GB for `combined_df` + `rewards_df`. With `@st.cache_resource`, shared across all sessions. Total server RAM: 8GB minimum, 16GB recommended.
- **Concurrency**: Streamlit handles 30-50 concurrent users. For 5-10 team members, this is ample.

### Data Validation on Upload

- Check transaction CSV columns match expected schema (13 columns from `00-setup/04-define-data-func`)
- Check ODDD Excel has required column families (`* Spend`, `* Swipes`, `Acct Number`)
- Warn on unexpected column names (fuzzy match suggestions)
- Report NaN rates per column
- Validate date ranges make sense (no future dates, no gaps > 2 months)

### Multi-Client Architecture

- `CLIENT_CONFIGS` dictionary (from `06-direct-competition/01_competitor_config`) already supports multi-client
- Extend to a YAML config file per client: competitor lists, thresholds, file paths
- Session state keys prefixed with client ID to prevent cross-contamination
- Server directory structure: `/data/{client_id}/` with transaction and ODDD files

### Security

- No raw data exposed in browser (only aggregations and charts)
- File uploads stored in temp directory, cleaned after pipeline completion
- Authentication required before any page access
- No secrets in code -- config via environment variables

---

## Dependencies & Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Matplotlib charts look different in Streamlit | Medium | Test all 23 sections; use `plt.close(fig)` to prevent memory leaks |
| 5.8M row load time frustrates users | High | Parquet cache after first load; show progress bar |
| Plotly migration breaks chart styling | Medium | Migrate incrementally; keep matplotlib fallback |
| Team unfamiliar with Streamlit | Low | 1-day workshop; Streamlit's API is small |
| PPTX export quality doesn't match manual decks | High | Use branded template; follow executive-data-presentation guidelines |
| Session state lost on server restart | Medium | Auto-save Parquet files; re-load on restart |

---

## Success Metrics

- All 23 sections render correctly in the browser
- Pipeline completes in <90s for 5.8M rows (first load), <5s cached
- PPTX export produces deck equivalent to manual process
- 5+ team members actively using within 2 weeks of launch
- Zero unhandled errors in first month of production use

---

## References

### Internal

- Repository README: `/private/tmp/txn-visual-test/README.md`
- Theme system: `/private/tmp/txn-visual-test/01-general/01_general_theme`
- Data loader: `/private/tmp/txn-visual-test/00-setup/04-define-data-func`
- Client config: `/private/tmp/txn-visual-test/00-setup/02-file-config`
- Multi-client competitor config: `/private/tmp/txn-visual-test/06-direct-competition/01_competitor_config`
- Executive scorecard: `/private/tmp/txn-visual-test/22-executive/01_scorecard_data`
- Expected ODDD fields: `/private/tmp/txn-visual-test/00-setup/expected-fields`

### External

- [Streamlit Multi-Page Apps](https://docs.streamlit.io/develop/concepts/multipage-apps)
- [Streamlit Caching](https://docs.streamlit.io/develop/concepts/architecture/caching)
- [Streamlit Fragments](https://docs.streamlit.io/develop/api-reference/control-flow/fragment)
- [Streamlit Authentication](https://docs.streamlit.io/develop/concepts/connections/authentication)
- [Streamlit Docker Deployment](https://docs.streamlit.io/deploy/tutorials/docker)
- [python-pptx Documentation](https://python-pptx.readthedocs.io/en/latest/)
