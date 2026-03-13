# feat: Enrich Deposit Cells with Underutilized ZAccounts/ZTrends Fields

## Enhancement Summary

**Deepened on:** 2026-03-13
**Review agents used:** pattern-recognition-specialist, code-simplicity-reviewer, architecture-strategist, spec-flow-analyzer, performance-oracle
**Sections enhanced:** All

### Key Improvements from Review
1. Dropped 4 low-value tasks (mobile RDI, tier RDI, ZTrends scoring components, FeestoDepositsOverrideCount33) — reduces scope by ~35% while retaining ~90% of value
2. Resolved critical gap: `analysis_date` undefined — use latest snapshot date from `ZA_SNAPSHOT_META`
3. Added explicit `lastdepdate` parsing specification with `pd.to_datetime(errors='coerce')`
4. Added shared helper functions (dep_safe_median, signal_color) to eliminate cross-cell duplication
5. Collapsed 5 phases → 2 phases (setup is the only real dependency)
6. Added concrete density thresholds: max 8 table columns, max 6 KPI cards, max 3 subplot rows
7. Specified edge case handling: NaN for division-by-zero, "Nx" format for intensity ratio

### Tasks Dropped (with rationale)
- **Task 2c (cell 07 mobile RDI):** Cannot isolate mobile-specific returns from aggregate RDI33 — the field counts ALL returned deposits regardless of channel. Adds noise, not insight.
- **Task 2d (cell 09 tier RDI):** Cell 09 already has 4+ metric panels across 9 tiers. Adding 2 more panels would overcrowd. Defer to future "deposit risk profile" cell if needed.
- **Task 5c (cell 24 ZTrends scoring components):** These are model internals (DepC_Component, DepT_Component, etc.) from a different join source (ZTrends, not ZAccounts). Belongs in a scoring model interpretability section, not deposit analysis. Different data path would confuse implementation pattern.
- **FeestoDepositsOverrideCount33 from Task 0a:** No downstream consumer — pure YAGNI.

---

## Overview

Sections 23 and 24 have 22 deposit fields loaded per snapshot via `_LONGITUDINAL_FIELDS` but most cells only use 3-4 of them (depAmt365, depCount365, avgdaysbetweendeposits, balance). Several powerful fields are completely untapped: `lastdepdate`, `RDI33/RDIAmt33` (Return Deposit Items — bounced checks/returned ACH), nested deposit windows (DepAmt33/66/99), and trend indicators. This plan enriches existing cells with these fields — no new cells needed.

## Problem Statement

Current state of field utilization across 23-deposits cells:

| Field | Cells Using | Target |
|-------|-------------|--------|
| depAmt365, depCount365 | 6 each | — (already well-used) |
| DepAmt33 | 1 (cell 04) | 5+ |
| lastdepdate | 0 | 5+ |
| RDI33, RDIAmt33 | 0 | 6+ |
| DepositTrendCount33 | 1 (cell 25) | 3+ |
| RepaymentTrendCount33 | 0 | 1+ |

## Proposed Solution

Enhance existing cells by weaving in underutilized fields. Each cell gets targeted additions that match its analytical purpose. Two phases: setup prerequisites, then independent cell enrichments.

## Field Glossary

- **RDI33** — Return Deposit Item count (33d). Bounced checks, returned ACH. High = unreliable deposits.
- **RDIAmt33** — Dollar amount of returned deposits (33d).
- **lastdepdate** — Date of most recent deposit. Enables days-since-last-deposit recency.
- **DepAmt33/66/99** — Deposit dollars in 33/66/99-day windows. Nested windows show acceleration.
- **DepositTrendCount33** — Count of 33-day periods with increasing deposit activity.
- **CashFlowTrendCount33** — Cash flow stability trend signal.
- **WindfallTrendCount33** — Large/irregular deposit frequency signal.
- **RepaymentTrendCount33** — OD repayment behavior trend signal.
- **AvgCollectedBalance** — Average collected (available) balance, excludes holds.

---

## Implementation Phases

### Phase 0: Setup Prerequisites

#### Task 0a: Add missing fields to `_LONGITUDINAL_FIELDS`
**File:** `23-deposits/01_deposit_setup`

Currently `_LONGITUDINAL_FIELDS` (line 229) loads 22 fields per snapshot but is missing:
- `lastdepdate` — needed for recency calculations
- `RDI33` — return deposit item count
- `RDIAmt33` — return deposit item amount

Add these 3 fields so they're available with snapshot suffixes for longitudinal comparison.

**Note:** `lastdepdate` is a date, not a rolling window — but it IS useful longitudinally. Comparing `lastdepdate_nov24` vs `lastdepdate_dec25` answers "did this account deposit more recently by the second snapshot?"

#### Task 0b: Add computed helper columns and shared utilities
**File:** `23-deposits/01_deposit_setup`
**Insert:** Between section 5 (longitudinal join, ending ~line 315) and section 6 (ODDD column discovery, ~line 318)

**Step 1: Define `ANALYSIS_DATE` from latest snapshot:**
```python
ANALYSIS_DATE = ZA_SNAPSHOT_META[sorted(ZA_SNAPSHOT_META.keys())[-1]]['date']
```

**Step 2: Parse `lastdepdate` to datetime:**
```python
if 'lastdepdate' in deposits_df.columns:
    deposits_df['lastdepdate'] = pd.to_datetime(
        deposits_df['lastdepdate'], errors='coerce'
    )
    # Also parse all snapshot-suffixed versions
    for _sk in _snapshot_keys_sorted:
        _lbl = ZA_SNAPSHOT_META[_sk]['label']
        _col = f'lastdepdate_{_lbl}'
        if _col in deposits_df.columns:
            deposits_df[_col] = pd.to_datetime(
                deposits_df[_col], errors='coerce'
            )
```

**Step 3: Compute derived columns using `np.where` (vectorized, no `.apply()`):**
```python
# Days since last deposit (relative to latest snapshot, not today)
if 'lastdepdate' in deposits_df.columns:
    deposits_df['days_since_last_dep'] = (
        ANALYSIS_DATE - deposits_df['lastdepdate']
    ).dt.days

# RDI rate: % of deposits that were returned (bounced)
# NaN when DepCount33 == 0 (no deposits = no meaningful RDI rate)
if 'RDI33' in deposits_df.columns and 'DepCount33' in deposits_df.columns:
    deposits_df['rdi_rate'] = np.where(
        deposits_df['DepCount33'] > 0,
        deposits_df['RDI33'] / deposits_df['DepCount33'],
        np.nan
    )
```

**Column naming convention:** Use `snake_case` without leading underscore for setup-computed columns (`days_since_last_dep`, `rdi_rate`). Leading underscore is reserved for cell-local variables per existing codebase convention.

**Step 4: Validation (print warnings for low-data fields):**
```python
for _derived, _min in [('rdi_rate', 50), ('days_since_last_dep', 50)]:
    if _derived in deposits_df.columns:
        _valid = deposits_df[_derived].notna().sum()
        if _valid < _min:
            print(f"    WARNING: {_derived} has only {_valid} valid values")
        else:
            print(f"    {_derived}: {_valid:,} valid values")
```

**Step 5: Add shared helper functions (new section 5b):**
```python
def dep_safe_median(df, field):
    """Return median of field if it exists and has data, else np.nan."""
    if field not in df.columns:
        return np.nan
    return df[field].dropna().median()

def dep_signal_color(value, thresholds, colors=None):
    """Return signal color based on threshold breakpoints.
    thresholds: (green_max, yellow_max) -- above yellow_max = red.
    colors: optional override tuple (green, yellow, red).
    """
    if colors is None:
        colors = (GEN_COLORS['success'], GEN_COLORS['warning'], GEN_COLORS['danger'])
    if pd.isna(value):
        return GEN_COLORS['muted']
    if value <= thresholds[0]:
        return colors[0]
    if value <= thresholds[1]:
        return colors[1]
    return colors[2]
```

#### Task 0c: Refresh personal/business DFs
Already handled by existing section 7 in setup (lines 390-397). The derived columns computed on `deposits_df` will propagate automatically when section 7 rebuilds `deposits_personal_df` and `deposits_business_df` from `deposits_df`. No code change needed — just verify propagation.

#### Task 0d: Harmonize business cell 14 before enriching
**File:** `24-business-deposits/14_business_campaign_responder_deposits`

Before enriching cell 14 (Task 1g), refactor business cell 14 to:
1. Remove dead `_mtd_cols` / `_mtd_pattern` code (lines ~33-38)
2. Remove local `_is_success()` / `_is_nu_partial()` re-implementations (lines ~59-73)
3. Use shared `CAMP_MAIL_COLS`, `CAMP_RESP_COLS`, `CAMP_MAILER_KEYS`, `camp_is_success()`, `camp_is_nu_partial()` from setup — same as personal cell 14 already does
4. Remove local `_mail_pattern` / `_resp_pattern` / `_mail_cols` / `_resp_cols` regex discovery (lines ~30-53)

This eliminates ~40 lines of divergent code and ensures Task 1g's enrichment works identically in both files.

---

### Phase 1: Cell Enrichments (all independent, any order)

**Density thresholds (apply to all tasks):**
- Max 8 data columns in a conference-format comparison table
- Max 6 KPI cards in a panel
- Max 3 subplot rows per chart figure
- Prefer adding table columns/rows over new chart panels
- If a cell would exceed limits, add a supplemental table below rather than widening

#### Task 1a: Enrich cell 02 (KPIs)
**File:** `23-deposits/02_deposit_kpis`
**Mirror:** `24-business-deposits/02_business_deposit_kpis`

**Add to KPI card panel (expand grid from 2x2 to 3x2):**
- **New KPI card:** "Deposit Quality" — median `rdi_rate` among depositors (DepCount33 > 0), colored with `dep_signal_color(val, (0.02, 0.05))` — green (<2%), yellow (2-5%), red (>5%)
- **New KPI card:** "Days Since Last Deposit" — median `days_since_last_dep` among accounts with valid lastdepdate, colored with `dep_signal_color(val, (15, 45))` — green (<15d), yellow (15-45d), red (>45d)

**Layout change:** Increase left panel from 2x2 to 3x2 grid. Increase figure height proportionally to maintain card readability. Left panel stays at ~30% width.

**Edge cases:**
- Scope "Days Since Last Deposit" to accounts where `days_since_last_dep` is not NaN (accounts with at least one deposit). Otherwise the KPI is meaningless for never-deposited accounts.
- RDI color thresholds should be defined as constants at top of cell for per-client tuning.

**Fields used:** rdi_rate (derived), days_since_last_dep (derived)

#### Task 1b: Enrich cell 03 (Velocity) with amount-based velocity
**File:** `23-deposits/03_deposit_velocity`
**Mirror:** `24-business-deposits/03_business_deposit_velocity`

Currently velocity is count-only: `(DepCount33/33) / (depCount365/365)`. Add:
- **Amount velocity** computed inline in the cell: `(DepAmt33/33) / (depAmt365/365)` — NOT a setup-derived column since only this cell uses it and cell 03 already computes the count version
- Accounts can have stable count velocity but accelerating amount velocity (bigger deposits, same frequency)
- Add a second row to the summary table: "Amount Velocity" below existing "Count Velocity"
- In the chart, show grouped bars: count-based vs amount-based classification side by side

**Implementation note:** Use `np.where(depAmt365 > 0, ...)` for the division guard, same pattern as count velocity.

**Fields used:** DepAmt33, depAmt365

#### Task 1c: Enrich cell 04 (Frequency) with deposit quality
**File:** `23-deposits/04_deposit_frequency`
**Mirror:** `24-business-deposits/04_business_deposit_frequency`

Currently shows frequency bands with median DepAmt33. Add to the summary table:
- **Median RDI rate** per frequency band — do high-frequency depositors have more bounced deposits?
- **Median days since last deposit** per band — validates that "weekly" depositors actually deposited recently

Add as new columns in the existing text table only (no chart changes).

**Fields used:** rdi_rate (derived), days_since_last_dep (derived)

#### Task 1d: Enrich cell 05 (Auto-Deposit Impact)
**File:** `23-deposits/05_autodeposit_impact`
**Mirror:** `24-business-deposits/05_business_autodeposit_impact`

Current grid is 2x3 (6 panels, all filled). Do NOT add new subplot panels.

Instead, add to the conference-format summary table (text output above the chart):
- **Median RDI rate** — hypothesis: auto-deposit accounts should have near-zero RDI (ACH doesn't bounce like checks)
- **Median days since last deposit** — auto-depositors should show shorter recency

**Fields used:** rdi_rate (derived), days_since_last_dep (derived)

#### Task 1e: Enrich cell 12 (Deposit Count Trajectory) with RDI trajectory
**File:** `23-deposits/12_snapshot_deposit_trajectory`
**Mirror:** `24-business-deposits/12_business_snapshot_deposit_trajectory`

Currently shows depCount365 per snapshot. Add:
- **Second grouped bar or overlay line:** median `rdi_rate` per snapshot (is deposit quality improving over time?)
- Requires at least 2 snapshots with non-null RDI33 data; skip RDI overlay if fewer

**Implementation note:** Compute `rdi_rate` per snapshot using the suffixed fields: `RDI33_{label} / DepCount33_{label}` at runtime. The setup-computed `rdi_rate` uses the latest snapshot only.

**Fields used:** RDI33_{label}, DepCount33_{label} (snapshot-suffixed)

#### Task 1f: Enrich campaign comparison tables (cells 14, 14b, 14e)
**File:** `23-deposits/14_campaign_responder_deposits`
**File:** `23-deposits/14b_nu_conversion_journey`
**File:** `23-deposits/14e_ladder_movement_deposits`
**Mirrors:** `24-business-deposits/14_business_*`, `14b_business_*`, `14e_business_*`

Add to the `_compare` list in each cell (table columns only, no chart changes):
- `('rdi_rate', 'RDI Rate', gen_fmt_pct)` — responders should have lower RDI (better deposit quality)
- `('days_since_last_dep', 'Days Since Dep', gen_fmt_count)` — responders should show more recent deposits

**Check table width:** The _compare list in cell 14 currently has 6 fields. Adding 2 makes 8 — at the max threshold. Do not add more beyond these 2.

**Formatter for rdi_rate:** Use `gen_fmt_pct` (displays as "2.3%"). This is appropriate since it IS a percentage (proportion of deposits returned).

**Why this matters:** If responders have HIGH RDI, the campaign may be driving unreliable deposit behavior (e.g., depositing bad checks to hit the threshold). If responders have LOW RDI, the campaign is driving real deposit growth.

**Fields used:** rdi_rate (derived), days_since_last_dep (derived)

#### Task 1g: Enrich cell 16 (Repayment Health) with deposit context
**File:** `23-deposits/16_repayment_health`
**Mirror:** `24-business-deposits/16_business_repayment_health`

Currently only shows median depCount365 per repayment tier. Add to the comparison:
- **depAmt365** — deposit AMOUNT by repayment tier (not just count)
- **RDI rate** — do low-repayment accounts also have high RDI? (double signal of unreliable funding)
- **DepositTrendCount33** — are poor-repayment accounts showing improving or worsening deposit trends?

**Fields used:** depAmt365, rdi_rate (derived), DepositTrendCount33

#### Task 1h: Enrich cell 20 (Summary) with new narrative elements
**File:** `23-deposits/20_deposit_summary`
**Mirror:** `24-business-deposits/20_business_deposit_summary`

Add narrative paragraphs for:
- **Deposit quality:** "X% of depositors have RDI rate > 5% (unreliable deposits)"
- **Recency:** "Median days since last deposit: X days (among accounts with deposit history)"
- **Trend signals:** "X% show positive deposit trend, X% negative" (using DepositTrendCount33)

Scope recency and RDI stats to accounts with valid data (not the full portfolio including never-deposited).

**Fields used:** rdi_rate (derived), days_since_last_dep (derived), DepositTrendCount33

#### Task 1i: Enrich cell 25 (Momentum) with RDI quality overlay
**File:** `23-deposits/25_deposit_momentum_indicators`
**Mirror:** `24-business-deposits/25_business_deposit_momentum_indicators`

Do NOT add RepaymentTrendCount33 as a 4th momentum signal — repayment behavior is conceptually different from deposit momentum and would conflate the two.

Instead, add:
- **RDI rate** as a quality overlay on momentum segments — high momentum + high RDI = risky growth
- Add `rdi_rate` to the comparison table alongside existing fields (depAmt365, etc.)

**Fields used:** rdi_rate (derived)

---

## Acceptance Criteria

### Functional
- [x] `_LONGITUDINAL_FIELDS` in setup includes lastdepdate, RDI33, RDIAmt33
- [x] `ANALYSIS_DATE` defined from latest snapshot in ZA_SNAPSHOT_META
- [x] `lastdepdate` parsed to datetime with `pd.to_datetime(errors='coerce')` — including snapshot-suffixed versions
- [x] Setup computes `days_since_last_dep` and `rdi_rate` using `np.where` (vectorized)
- [x] Derived columns use `snake_case` naming (no leading underscore)
- [x] `dep_safe_median()` and `dep_signal_color()` helpers added to setup
- [x] Business cell 14 harmonized to use shared CAMP_* utilities (dead code removed)
- [x] Personal/business DFs refreshed with new computed columns
- [x] All 10 cell enrichments applied (Section 23)
- [x] All 10 business mirrors applied identically (Section 24)
- [x] Each cell handles missing fields gracefully with `if field in _df.columns` guards
- [x] No new `plt.show()` calls added — one chart per cell rule maintained

### Quality
- [x] Every derived field validated in setup (warning printed if <50 valid values)
- [x] `rdi_rate` is NaN when DepCount33 == 0 (not zero — semantically different)
- [x] `days_since_last_dep` scoped to depositors only in KPI cards (not full portfolio)
- [x] RDI color thresholds defined as constants at top of cell 02 for per-client tuning
- [x] Conference tables stay at max 8 data columns
- [x] KPI panel stays at max 6 cards (expanded to 3x2 from 2x2)
- [x] No new subplot panels added to already-full chart grids — use table enrichment instead
- [x] Amount velocity in cell 03 computed inline (not a setup-derived column)
- [x] All business mirrors match personal logic exactly (different title/df only)

### Performance
- [x] All derived columns computed with `np.where` or vectorized pandas (no `.apply()`)
- [x] `lastdepdate` parsing happens once in setup, not repeated per cell
- [x] Memory impact negligible (~24 MB additional at 200K rows)

---

## Dependencies & Risks

**Dependencies:**
- `lastdepdate` format must be parseable by `pd.to_datetime(errors='coerce')`. Handles ISO strings, YYYYMMDD, MM/DD/YYYY. Will silently produce NaT for epoch integers — **check actual data before implementing.**
- RDI33/RDIAmt33 must exist in client's ZAccounts export (field availability varies by client)
- At least 2 snapshots needed for RDI trajectory in cell 12 (skip overlay if fewer)

**Risks:**
- **`lastdepdate` format unknown (BLOCKING):** Must inspect actual ZAccounts CSV before implementing Task 0b. If epoch integer, parsing logic changes. Add `infer_datetime_format=True` as fallback.
- **Field availability:** Not all clients export all ZAccounts fields. Every enhancement MUST have a graceful skip. The `dep_safe_median()` helper handles this consistently.
- **Chart density:** Concrete thresholds now set (8 table cols, 6 KPI cards, 3 subplot rows). Tasks adjusted to stay within limits.
- **Business cell 14 divergence:** Task 0d harmonizes this before enrichment to prevent drift.

**Not risks (per performance review):**
- Memory: +24 MB at 200K rows is negligible (~10% increase)
- CPU: +42 median calls adds ~210ms total across entire notebook
- Longitudinal join: 3 additional fields x 3 snapshots = 9 new columns, merge cost dominated by join key lookup (unchanged)

---

## Task Summary

| Phase | Tasks | Files Modified (x2 for mirrors) | Priority |
|-------|-------|----------------------------------|----------|
| 0 (Setup) | 0a, 0b, 0c, 0d | setup (1) + biz cell 14 harmonize (1) | Prerequisite |
| 1 (Enrichment) | 1a-1i | 02, 03, 04, 05, 12, 14, 14b, 14e, 16, 20, 25 (20 files) | All independent |

**Total: 22 files modified (11 personal + 10 business + 1 setup), 13 tasks**

*Reduced from original: 30 files / 17 tasks → 22 files / 13 tasks (-27% files, -24% tasks, ~90% value retained)*

---

## References

- Setup file: `23-deposits/01_deposit_setup:229` (`_LONGITUDINAL_FIELDS`)
- ZAccounts schema: `/Users/jgmbp/TXN-v4-complete/zaccounts` (77 fields)
- ZTrends schema: `/Users/jgmbp/TXN-v4-complete/ztrends` (56 fields)
- Prior fix commit: `c4537c2` (MTD→deposit data model correction)
- Plan: `plans/refactor-deposit-analysis-section-23.md` (field inventory at line 13-72)
- RDI definition: Return Deposit Item = bounced checks, returned ACH (deposit quality signal)
