# Self-Service Analysis & PowerPoint Generation Platform

## Enhancement Summary

**Deepened on:** 2026-03-19
**Research agents used:** 10 (Architecture Strategist, Performance Oracle, Security Sentinel, Code Simplicity, Kieran Python, Pattern Recognition, Matplotlib Leak Learning, Hardcoded Values Learning, Executive Data Presentation Skill, Agent-Native Architecture)

### Key Improvements from Deepening
1. **Scope reduced from 8 weeks to 3-4 weeks** -- sections 01-22 are already refactored as 35 modules in the monorepo. Only section 23 (deposits) needs refactoring.
2. **4 pages reduced to 2 pages** -- Select+Run merged, Review page cut (CSMs can delete slides in PowerPoint).
3. **No new `SectionResult` type** -- unify the 4 existing `AnalysisResult` definitions instead of adding a 5th.
4. **Performance roadmap added** -- local file staging, eliminate double chart rendering, worker pool for concurrency.
5. **Presentation design rules added** -- conclusion headlines (not labels), chart selection matrix, deck narrative flow.
6. **Refactoring checklist added** -- catch hardcoded y-axis limits and hardcoded year lists during deposit cell migration.
7. **Agent-native patterns added** -- `--format json` on CLI and `serialize_result()` for future AI agent access.

### Critical Corrections
- The plan originally proposed refactoring 376 notebook cells. **Sections 01-22 are already done** in `txn_analysis` (35 registered modules, 597 tests). Only ~50 deposit cells remain.
- The plan proposed building a 4-page Streamlit app. **A 12-page app already exists** in `platform_app`. Extend it, don't rebuild.
- `SectionResult` would have been a 5th competing result type. **Unify AnalysisResult first** (Tier 3.1).

---

## Overview

Build an internally hosted Streamlit UI that lets non-technical CSMs go from "I need a presentation for my client" to a finished, polished PowerPoint deck in under 30 minutes. Zero command line, zero Python knowledge required.

The platform extends the existing `analysis_platform/platform_app` (which already has 12 pages, an orchestrator, and 35+ registered modules) by adding: deck builders for TXN and Deposits, a simplified client selection flow, and PPTX generation as a first-class output.

## Problem Statement

Today, creating a client analysis deck requires:
1. A developer manually editing `02-file-config` with client details
2. Running notebook cells in sequence in Jupyter
3. Manually screening which sections produced useful output
4. Manually building a PowerPoint from screenshots/exports
5. ~2-4 hours of combined developer + analyst time per client

There are ~50 clients, monthly review cycles, and 10-20 CSMs who need decks. The current process does not scale.

**Goal:** Any CSM can produce a client deck without developer involvement. Under 30 minutes, start to finish.

---

## Technical Approach

### Architecture (Simplified from Deepening)

```
CSM Browser
    |
    v
Existing Streamlit App (platform_app -- 12 pages already built)
    |
    +-- Page: Client Selector (NEW -- simplified from existing Workspace)
    |     - CSM dropdown (from clients_config.json)
    |     - Month picker
    |     - Client dropdown (filtered by CSM + month)
    |     - Product selector (TXN / ARS / Deposits)
    |     - Auto-detect data files on M: drive
    |     - Pre-flight validation + "Run" button
    |     - Inline progress bar (no separate Run page)
    |
    +-- Page: Results + Download (NEW -- simplified from existing Outputs)
          - One-click PPTX download (primary, prominent)
          - ZIP of all outputs (secondary)
          - Run logged to history
```

### Research Insight: 2 Pages, Not 4

> The "Run" page as a standalone concept is empty -- it is a progress bar. That is a component, not a page. The "Review" page (slide toggles) replicates what CSMs can do in PowerPoint in 2 seconds. Both are scope creep. -- Simplicity Reviewer

### Data Flow

```
clients_config.json (M: drive)
    --> CSM + Client selection
    --> Auto-resolve file paths (file_resolver.py)

File paths --> orchestrator.run_pipeline() (ALREADY EXISTS)
    --> ars_analysis.runner / txn_analysis.runner / deposits runner (NEW)
    --> dict[str, AnalysisResult] (ALREADY EXISTS)

AnalysisResult[] --> Deck Builder (NEW)
    --> CSI template + chart PNGs + data tables
    --> {client_id}-{client_name}-{product}-{month}.pptx
```

### Research Insight: What Already Exists vs. What's New

| Component | Status | Work Needed |
|-----------|--------|-------------|
| Streamlit app with 12 pages | EXISTS | Add 2 simplified pages |
| Orchestrator dispatching to pipelines | EXISTS | Add deposits pipeline |
| 35 TXN analysis modules | EXISTS | Write deck builder only |
| 8 ARS analysis modules + deck builder | EXISTS | Wire PPTX output to download page |
| Module registry with ModuleInfo | EXISTS | Add deposits modules |
| PipelineContext, AnalysisResult | EXISTS (4 competing versions) | Unify into 1 |
| Run logging (JSONL) | EXISTS | No changes |
| Progress callback pattern | EXISTS | Use as-is |
| Deposits analysis cells | EXISTS (50 cells in TXN-v4-complete) | Refactor into ~15 functions |
| TXN Deck Builder | DOES NOT EXIST | ~150 LOC, follows ARS pattern |
| Deposits Deck Builder | DOES NOT EXIST | ~150 LOC, follows ARS pattern |
| Client config integration | DOES NOT EXIST | Parse clients_config.json |
| File path resolver | PARTIALLY EXISTS (session_manager.py) | Extend with month logic |

---

### Implementation Phases (Revised: 3-4 Weeks)

#### Phase 1: End-to-End for ARS (Week 1-2)

**Goal:** CSM can select a client, run ARS analysis, download a PPTX deck.

- [ ] `clients_config.json` integration
  - Parse the existing config at `M:\ARS\Config\clients_config.json` (~50 clients)
  - Build CSM-to-client mapping
  - Client name auto-populates (no free text typos)
  - `platform_app/core/client_config.py`

- [ ] Month/period selector
  - Scan ODD directory for available months per client
  - Store in session state, use on PPTX title slide
  - Extend `platform_app/pages/workspace.py` or create `select_client.py`

- [ ] File path resolver
  - ODD path: `M:\ARS\Incoming\ODDD Files\{csm}\{YYYY.MM}\{client_id}\`
  - TXN path: `M:\ARS\Incoming\Transaction Files\{client_id} - {client_name}\`
  - Z accounts: search client data directory for `*zaccounts*` files
  - Extend existing `session_manager.py` auto-detect logic
  - `platform_app/core/file_resolver.py`

- [ ] Wire ARS pipeline to PPTX download
  - ARS deck builder already exists (`ars_deck` module in registry)
  - Template path in `platform.yaml` (ship template in repo)
  - One-click download button on results page

- [ ] Local file staging from M: drive
  - Copy input files to local temp dir before processing
  - Eliminates network I/O contention for concurrent users
  - `platform_app/core/file_staging.py`

**Deliverable:** CSM selects client, runs ARS, downloads PPTX. 1 page to start, 1 page to download.

#### Phase 2: TXN + Deposits Deck Builders (Week 3-4)

**Goal:** TXN and Deposits products also produce PPTX decks.

- [ ] Unify AnalysisResult (Tier 3.1)
  - Single definition in `shared/types.py` as superset of all 4 existing versions
  - Fields: `name`, `title`, `data: dict[str, DataFrame]`, `charts: list[Path]`, `error: str | None`, `summary`, `metadata: dict`, `sheet_name: str`
  - Update each package's runner to emit unified type directly
  - Remove `_convert_results` bridge functions

- [ ] TXN Deck Builder (~150 LOC)
  - Accepts `dict[str, AnalysisResult]` from existing `run_pipeline("txn", ...)`
  - For each result with chart paths: insert PNG into template slide
  - Section dividers between major sections
  - Title slide with client name, month, CSI branding
  - `txn_analysis/deck_builder.py`

- [ ] Refactor deposits cells into callable modules
  - ~50 cells in section 23 -> ~15-20 analysis functions
  - Group: dep_data (01-04), dep_blocks (05-15), dep_campaign (16-21), dep_segments (22-24), dep_trajectory (25-32), dep_lift (19a-g), dep_presentation (98-99)
  - Each returns unified `AnalysisResult`
  - Add to module registry with `Product.DEPOSITS`
  - Wire into orchestrator

- [ ] Deposits Deck Builder (~150 LOC)
  - Same pattern as TXN deck builder
  - ~15-20 slides: executive summary, response summary, cohort lift, deposit lift by segment, trajectory charts

- [ ] User-friendly error handling
  - `FileNotFoundError` -> "Could not find the file. Is the M: drive connected?"
  - `KeyError` -> "The data file is missing the '[column]' column."
  - `MemoryError` -> "This client's data is too large. Contact the analytics team."
  - `platform_app/core/error_handler.py`

**Deliverable:** All three products (ARS, TXN, Deposits) produce downloadable PPTX decks.

---

## Refactoring Checklist (from Documented Learnings)

When refactoring the ~50 deposit cells into functions, check for these known bugs:

### Matplotlib Figure Memory Leaks
- **Source:** `docs/solutions/performance-issues/matplotlib-figure-memory-leak-dctr-20260207.md`
- **Pattern:** Every chart must use `try/finally: plt.close(fig)` or the context manager:
  ```python
  @contextmanager
  def create_figure(figsize=(14, 7)):
      fig, ax = plt.subplots(figsize=figsize)
      try:
          yield fig, ax
      finally:
          plt.close(fig)
  ```
- **Rule:** Never store live `Figure` objects in result containers. Render to bytes/path immediately.

### Hardcoded Y-Axis Limits
- **Source:** `docs/solutions/logic-errors/hardcoded-ylim-dctr-charts-20260207.md`
- **Pattern:** Grep for `set_ylim`, `set_xlim`. Replace hardcoded values with data-driven bounds.
- **Test:** Assert that axis limits encompass all plotted values.

### Hardcoded Year Lists
- **Source:** `docs/solutions/logic-errors/hardcoded-year-lists-dctr-20260207.md`
- **Pattern:** Grep for `isin([20`, explicit year integers. Replace with `datetime.now().year - N` or `yr // 10 * 10` arithmetic.
- **Test:** Test with future-dated data (year 2030) to verify no silent data loss.

---

## PPTX Design Rules (from Executive Data Presentation Skill)

### Slide Structure: Three Layers
1. **Top -- Conclusion headline** (complete sentence, not a label)
   - BAD: "Debit Card Penetration by Branch"
   - GOOD: "Three branches account for 62% of debit growth, led by Main Office at 23%"
2. **Middle -- Data visual** (chart or table)
3. **Bottom -- Business implication** ("so what" annotation or speaker note)

### Headline Rules
- Include **metric, magnitude, and direction**
- Translate percentages into operational equivalents: "12% attrition" -> "equivalent to losing Branch X entirely"
- Quantify the **opportunity**, not just the problem
- Active voice, one finding per headline

### Chart Selection
| Insight Type | Correct Chart | Avoid |
|---|---|---|
| Comparison (ranking) | Horizontal bar, sorted | Pie chart with 5+ slices |
| Trend (over time) | Line chart | Bar chart for time series |
| Composition (parts) | Stacked bar; donut for 2-3 | Pie with many slices |
| Single KPI | Hero number + delta | Full chart for one number |

### Chart Rendering Rules
- Figure aspect ratio must match slide dimensions: `figsize=(14, 8)` for 16:9
- Direct labels on data points instead of legends
- Highlight focal series at full opacity; mute everything else to alpha=0.3
- Remove gridlines, borders, decorative elements that don't encode data
- One focal color per chart; consistent color mapping across deck

### Deck Narrative Flow (5-section arc)
1. **How Big Is This?** -- Program scope, volume, penetration
2. **Where Does Growth Come From?** -- Sources, channels, acquisition mix
3. **How Engaged Are Members?** -- Activity, trends, concentration
4. **Where Are We Losing?** -- Closures, attrition, decay
5. **What Should We Do?** -- Recommendations, priorities, next steps

### Color System
| Color | Hex | Usage |
|---|---|---|
| Navy | `#1B365D` | Primary data, emphasis, titles |
| Green | `#27AE60` | Growth, positive change |
| Red/Coral | `#E74C3C` | Decline, negative change |
| Amber | `#F39C12` | Warning, caution |
| Gray | `#95A5A6` | Inactive, neutral, de-emphasized |

---

## Performance Roadmap (from Performance Oracle)

### Quick Wins (Day 1)

| Action | Impact | Effort |
|--------|--------|--------|
| Local file staging from M: drive | -5 to -20 min per run | 2 hours |
| Eliminate double chart rendering (kaleido renders twice) | -30 to -60 sec | 1 hour |
| Enable pandas Copy-on-Write in TXN data_loader | -400 MB RAM/run | 30 min |
| Apply matplotlib `try/finally` to all chart code | Prevents OOM | 2 hours |

### Medium-Term (Week 3-4)

| Action | Impact | Effort |
|--------|--------|--------|
| Parquet caching (re-runs skip file loading) | -10 to -30 sec on re-runs | 4 hours |
| Column subsetting for ODDD (`usecols`) | -40% load time | 2 hours |
| Parallel transaction file loading (ThreadPoolExecutor) | -2 to -5 sec | 1 hour |

### If Scaling Beyond 10 Users

| Action | Impact | Effort |
|--------|--------|--------|
| Worker pool (ProcessPoolExecutor or Celery) | Enables 20 concurrent users | 2-3 days |
| Parallel analysis tiers | -30 to -60% analysis time | 1 day |
| Session concurrency limits | Prevents thrash | 2 hours |

### Concurrency Projections

| Users | RAM (current) | RAM (with fixes) | Viable? |
|-------|--------------|-------------------|---------|
| 1 | 2-4 GB | 1-2 GB | Yes |
| 5 | 10-20 GB | 5-10 GB | Yes |
| 10 | 20-40 GB | 10-20 GB | Yes (with staging + CoW) |
| 20 | 40-80 GB | 20-40 GB | Needs worker pool |

---

## Security Requirements (from Security Sentinel)

### Must-Fix Before Multi-User Deployment

| # | Finding | Severity | Fix |
|---|---------|----------|-----|
| 1 | **No authentication** | CRITICAL | Add `streamlit-authenticator` or corporate SSO. Any machine on the network has full access to all client financial data. |
| 2 | **No authorization** | CRITICAL | Add CSM-to-client mapping. Currently CSM Alice can access CSM Bob's clients. Filter `discover_csm_folders()` by logged-in user. |
| 3 | **Arbitrary file path read** | CRITICAL | Users can type any server path in the data ingestion page. Add an allowlist of base directories (`M:\ARS`, `/data`) and validate all paths resolve under them. |
| 4 | **Temp files persist with PII** | HIGH | Uploads use `delete=False` and are never cleaned. Use session-scoped temp directories with cleanup on session end. |
| 5 | **Stack traces shown to users** | HIGH | Full Python tracebacks displayed in browser, revealing server paths and code structure. Show generic error + log details server-side. |
| 6 | **Account numbers unmasked** | HIGH | Data preview (`st.dataframe(df.head(10))`) shows raw account numbers. Mask to last 4 digits in preview. Verify source data is pre-hashed. |

### Path Validation Pattern

```python
ALLOWED_ROOTS = [Path("M:/ARS").resolve(), Path("/data").resolve()]

def validate_path(user_path: str) -> Path:
    p = Path(user_path).resolve()
    if not any(is_subpath(p, root) for root in ALLOWED_ROOTS):
        raise ValueError("Access denied: path outside allowed directories")
    return p
```

Apply at every point where user-supplied paths are used: `data_ingestion.py`, `workspace.py`, `batch_workflow.py`, `run_analysis.py`, `file_input.py`.

### Security Phases

- **Phase 1 (before go-live):** Authentication, authorization, path validation
- **Phase 2 (first sprint):** Temp file cleanup, hide tracebacks, mask account numbers, filter run history by CSM
- **Phase 3 (hardening):** HTTPS, HTML-escape `unsafe_allow_html` strings, file locking on run logger, memory guards

---

## Agent-Native Considerations (from Agent-Native Architecture Review)

The platform is already 70% agent-ready. Low-effort additions:

### Phase 1 Addition
- Add `--format json` to the CLI's `run` command
- Add `serialize_result()` to `shared/types.py` (JSON-serializable AnalysisResult)
- This gives AI agents CLI access immediately with zero new infrastructure

### Phase 2 Addition
- Make the deck builder accept a slide manifest dict (which slides to include/exclude)
- Add `list-modules --format json` CLI command for discoverability
- Strengthen `run_id` with random suffix for addressability

### Architectural Rule
**One orchestrator, multiple frontends.** Streamlit, CLI, and (future) API all call the same `run_pipeline()`. Never duplicate orchestration logic in the UI layer.

---

## Patterns to Reuse (from Pattern Recognition)

| Pattern | Where | Description |
|---------|-------|-------------|
| Registry Pattern | `core/module_registry.py` | `ModuleInfo` frozen dataclass, lazy-cached `get_registry()` |
| Context Object | `shared/context.py` | `PipelineContext` replaces raw dicts |
| Immutable Result | `shared/types.py` | Frozen `AnalysisResult` as output envelope |
| Strategy + Lazy Import | `orchestrator.py` | if/elif dispatch with deferred imports |
| Workspace Resolution | `core/session_manager.py` | `auto_detect_files()` with pattern matching |
| Progress Callback | `components/progress.py` | `Callable[[str], None]` injected through context |
| Session State Namespace | `pages/*.py` | `uap_` prefix on all Streamlit session keys |

## Anti-Patterns to Avoid

| Anti-Pattern | Where Found | Fix |
|---|---|---|
| `dir()` checks for variable existence | Notebook cells | Pass dependencies explicitly through function params |
| Hardcoded Windows paths | `02-file-config`, `99_build_pptx` | Environment variables or `PathResolver` protocol |
| Silent `except: pass` | `run_analysis.py` | Always log exceptions |
| Global mutable state | Notebook cells | `PipelineContext` as single conduit |
| Duplicated chart boilerplate | `99_build_pptx` (3 locations, 70% overlap) | Extract `build_bar_chart()` helper |
| If/elif pipeline dispatch | `orchestrator.py` | Registry-based dispatch with `importlib` |

---

## Acceptance Criteria

### Functional Requirements
- [ ] CSM selects their name from a dropdown (populated from clients_config.json)
- [ ] CSM selects a month and client (filtered by their assignment)
- [ ] CSM chooses a product (TXN, ARS, Deposits)
- [ ] System auto-detects data files on M: drive based on client + month
- [ ] Analysis runs with visible progress ("Section 6 of 22")
- [ ] PPTX deck is generated automatically using CSI template
- [ ] CSM downloads PPTX with one click
- [ ] End-to-end time under 30 minutes for a single product
- [ ] Client name on PPTX title slide matches config (no typos)
- [ ] PPTX headlines are conclusion sentences, not topic labels

### Non-Functional Requirements
- [ ] Works on Windows machines with Python 3.13
- [ ] Handles M: drive paths (network drive) with local staging
- [ ] 10 concurrent users without performance degradation
- [ ] Friendly error messages for common failures (no raw tracebacks)

### Quality Gates
- [ ] Existing test suite (2,318 tests) still passes
- [ ] Each refactored deposit function produces identical output to notebook cell
- [ ] PPTX output reviewed by at least one CSM before team rollout

---

## Dependencies & Prerequisites

| Dependency | Status | Notes |
|------------|--------|-------|
| `analysis_platform` monorepo | EXISTS | 12-page Streamlit app, orchestrator, registries |
| 35 TXN analysis modules | EXISTS | Already refactored from notebook cells |
| 8 ARS modules + deck builder | EXISTS | PPTX generation works |
| `clients_config.json` | EXISTS | ~50 clients on M: drive |
| CSI PPTX template | EXISTS | On work PC, needs to be added to repo |
| Unified `AnalysisResult` | BLOCKED (T3.1) | 4 competing definitions, Phase 2 prerequisite |
| Deposits cells | EXISTS | 50 cells in TXN-v4-complete, not yet in monorepo |

**Key insight from deepening:** The `AnalysisResult` unification is NOT a blocker for Phase 1 (ARS already has its own working deck builder). It IS a prerequisite for Phase 2 (TXN + Deposits deck builders need a common result type).

---

## Risk Analysis & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| 30-min SLA exceeded | Medium | High | Local file staging (P0), column subsetting, Parquet cache |
| PPTX charts look different from notebook | Medium | Medium | Visual regression tests during Phase 2 |
| M: drive unavailable | Medium | High | Clear error message + manual upload fallback |
| 20+ concurrent users exhaust memory | Medium | High | Worker pool (scale trigger), CoW, column subsetting |
| Matplotlib memory leaks | High | Medium | Context manager pattern, `try/finally` on all charts |
| Hardcoded years/axis limits in deposit cells | High | Low | Refactoring checklist grep checks |

---

## Future Considerations

- **Scheduled runs:** Cron-based monthly batch for all clients (overnight)
- **Email delivery:** Auto-email finished PPTX to CSM when batch completes
- **Comparison mode:** "Show me how this client changed since last month"
- **ICS product:** Fourth pipeline for interchange analysis (same deck builder pattern)
- **API layer:** Thin FastAPI wrapper around orchestrator for agent/programmatic access
- **Client portal:** Read-only view for credit union clients to see their own data

---

## References

### Internal
- Analysis platform monorepo: `/Users/jgmbp/Desktop/analysis_platform/`
- Platform app: `packages/platform_app/src/platform_app/app.py`
- Orchestrator: `packages/platform_app/src/platform_app/orchestrator.py`
- Module registry: `packages/platform_app/src/platform_app/core/module_registry.py`
- Shared types: `packages/shared/src/shared/types.py`
- Existing PPTX builder: `23-deposits/99_build_pptx`
- Client config: `M:\ARS\Config\clients_config.json`
- CSI template: `C:\Users\james.gilmore\analysis-platform\2025-CSI-PPT-Template.pptx`
- Roadmap: `analysis_platform/plans/feat-platform-enhancement-roadmap.md`
- Matplotlib leak doc: `analysis_platform/docs/solutions/performance-issues/matplotlib-figure-memory-leak-dctr-20260207.md`
- Hardcoded ylim doc: `analysis_platform/docs/solutions/logic-errors/hardcoded-ylim-dctr-charts-20260207.md`
- Hardcoded years doc: `analysis_platform/docs/solutions/logic-errors/hardcoded-year-lists-dctr-20260207.md`

### External
- Streamlit multi-page apps: https://docs.streamlit.io/develop/concepts/multipage-apps
- Streamlit caching: https://docs.streamlit.io/develop/concepts/architecture/caching
- Streamlit deployment (Docker): https://docs.streamlit.io/deploy/tutorials/docker
- python-pptx docs: https://python-pptx.readthedocs.io/en/stable/
- Refactoring notebooks: https://ploomber.io/blog/refactor-nb-i/

### Related Issues / PRs
- PR #17 (`feat/platform-enhancement`) -- platform app wiring (OPEN)
- PR #18 (`chore/consolidate-moving-parts`) -- ARS CLI fixes
- Issue #14 -- Platform App wiring (Tier 4 roadmap)
- Tier 3.1 -- Unified AnalysisResult (blocks Phase 2)
