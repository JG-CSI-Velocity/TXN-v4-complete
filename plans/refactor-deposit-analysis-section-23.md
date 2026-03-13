# Refactor: Deposit Analysis — Section 23 (Personal) & Section 24 (Business)

## Problem Statement

Section 23 (deposits) has grown to 26 cells with excessive sub-numbering (3a-3d, 4a-4h, 5a-5e). Many cells show derivative views of the same data, some combine multiple charts per cell, and the most interesting analytical insight -- deposit velocity using nested windows -- doesn't exist yet.

The section needs a clean restructure: sequential numbering, one chart per cell, every chart telling a distinct story, and new analyses that cross deposit behavior with spend/swipe data from the ODDD.

**Key decision:** Personal and Business deposits do NOT get compared. Each gets its own standalone section with a full independent analysis. Section 23 = Personal. Section 24 = Business.

---

## Data Sources — Full Field Inventory

### ODDD (rewards_df) — Account-Level Behavioral Backbone

**~47K accounts** | Loaded in `00-setup/08-import-oddd` | Business/Personal split in `00-setup/09-oddd-account-type`

| Category | Fields | Notes |
|----------|--------|-------|
| **Identity** | `Acct ID`, `Acct Number`, `Acct Mask`, `Branch` | Join key to ZAccounts via `Acct Number` ↔ `HASHED_ACCOUNT` |
| **Account Status** | `Business?`, `Stat Code`, `Stat Desc`, `Prod Code`, `Prod Desc`, `Debit?` | `Business?` drives personal/business split; `Stat Code` = 'O' filters open accounts |
| **Dates** | `DOB`, `Date Opened`, `Date Closed` | `Account Holder Age`, `Account Age` are derived |
| **Balances** | `Avg Bal`, `Curr Bal` | Account-level current state |
| **Monthly OD Items (MTD)** | `{Mon}{YY} MTD` (e.g., `Sep24 MTD` through `Feb26 MTD`) | ~17 months of monthly overdraft item counts (NOT deposits); auto-discovered as `od_mtd_cols` |
| **Monthly Spend** | `{Mon}{YY} Spend` (e.g., `Sep24 Spend` through `Feb26 Spend`) | Auto-discovered as `spend_cols` |
| **Monthly Swipes** | `{Mon}{YY} Swipes` | Auto-discovered as `swipes_cols` |
| **Monthly PIN $/#** | `{Mon}{YY} PIN $`, `{Mon}{YY} PIN #` | Auto-discovered as `pin_amt_cols`, `pin_cnt_cols` |
| **Monthly Sig $/#** | `{Mon}{YY} Sig $`, `{Mon}{YY} Sig #` | Auto-discovered as `sig_amt_cols`, `sig_cnt_cols` |
| **Spend Aggregates** | `Total Spend`, `Total Swipes`, `last 3-mon spend/swipes`, `last 12-mon spend/swipes`, `Total Items`, `Last 12-mon Items`, `Last 3-mon Items` | Cross-analysis: deposit behavior vs card usage |
| **Monthly Averages** | `MonthlySwipes12/3`, `MonthlySpend12/3`, `MonthlyItems12/3` | Pre-computed rolling averages |
| **Swipe Categories** | `SwipeCat12`, `SwipeCat3` | Engagement tier labels |
| **Campaign (ARS)** | `Mailable?`, `{Mon}{YY} Mail`, `{Mon}{YY} Resp`, `# of Offers`, `# of Responses`, `Response Grouping` | Bimonthly mail/response tracking |
| **Segmentation** | `{Mon}{YY} Segmentation` (bimonthly) | Tracks segment migration over time |
| **Reg E** | `{Mon}{YY} Reg E Code/Desc` | Monthly Reg E opt-in status |
| **OD Limits** | `{Mon}{YY} OD Limit` | Monthly overdraft limit history |
| **Eligibility** | `{Mon}{YY} Elig`, `{Mon}{YY} Prog` | Program eligibility flags |

### ZAccounts (zaccounts_df) — Deposit Depth Layer

**~27K accounts per snapshot** | Up to 3 snapshots (e.g., Nov 2024, Jun 2025, Dec 2025) | Loaded in `23-deposits/01_deposit_setup`

| Category | Fields | Notes |
|----------|--------|-------|
| **Deposit Windows** | `DepCount33/66/99`, `depCount365`, `DepAmt33/66/99`, `depAmt365` | Nested windows: 33 ⊂ 66 ⊂ 99 ⊂ 365. Core of velocity analysis |
| **Deposit Behavior** | `avgdaysbetweendeposits`, `autodeposit`, `Mobile_Deposits_90`, `lastdepdate` | Frequency, channel, recency |
| **Risk Metrics** | `avgrepaymentrate`, `nsfodfeestodepositsratio90days`, `fdicoccasionsrolling12months`, `ytdnsfodaltpayratio`, `ytdnsfodpayratio` | Fee pressure, repayment health |
| **Trend Indicators** | `RepaymentTrendCount33`, `DepositTrendCount33`, `WindfallTrendCount33`, `CashFlowTrendCount33`, `FeestoDepositsOverrideCount33` | 33-day directional signals |
| **OD/Decline** | `CanOverdraft`, `ODLimit`, `AvgODLimit`, `MinODLimit`, `MaxODLimit`, `InitODLimit`, `UniqueODLimit`, `StdevODLimit`, `ParallelODLimit`, `RegEOptinvalue`, `odstatuscode`, `sixty_od`, `declines_365`, `declines_amt_365` | Overdraft profile |
| **Swipe Data** | `SIG_365`, `PIN_365` | 365-day signature and PIN transaction counts |
| **Items/Returns** | `items365`, `PD_365`, `PD_Amt_365`, `RT_365`, `RT_Amt_365`, `Refund_365`, `Refund_Amt_365` | Presentments, returns, refunds |
| **Fees** | `PossibleFees365`, `CollectedFees365` | Fee collection efficiency |
| **Balances** | `balance`, `AvgCollectedBalance` | Point-in-time and rolling average |
| **Chargeoff** | `Chargeoff_Account`, `Chargeoff_Date`, `Chargeoff_Amt_365`, `Recovery_Amt_365` | Loss/recovery tracking |
| **Account Info** | `acctid`, `branch`, `branchname`, `opendate`, `closeddate`, `acctstatus`, `prodcode`, `accttype`, `IsPersonal`, `employee` | Account metadata |
| **Other** | `RDI33`, `RDIAmt33`, `WindfallRatio`, `Strategic_Refunds`, `MRPC_Eligible`, `MRPC_Loan_Eligible`, `OutstandingLoanAmount`, `ODLOCAmount`, `Mobile_Deposits_90`, `Institution` | Specialty fields |

### ZTrends (ztrends_df) — Event-Level OD Behavior

**Variable row count** | One row per OD event | Loaded in `23-deposits/01_deposit_setup`

| Category | Fields | Notes |
|----------|--------|-------|
| **Event** | `acctid`, `noticedate`, `noticeid` | Event identity and timing |
| **Items** | `Items`, `PD`, `Item_Amts`, `PossibleFees`, `CollectedFees`, `Min_Bal` | Event-level financials |
| **Transaction Types** | `ACH`, `ATM`, `CHK`, `INT`, `CSR`, `BPY`, `OTH`, `POS` | What caused the OD |
| **Deposits at Event** | `depcount33/66/99/124`, `deptotal33/66/99/124`, `depcount60co`, `deptotal60co` | Deposit state at time of OD |
| **Limits** | `limit`, `parallel_limit` | OD limit at time of event |
| **Scoring Components** | `DepC_Component`, `DepT_Component`, `Age_Component`, `CashFlow_Component`, `DepositRegularity_Component`, `ExcessiveOverdraft_Component`, `MonthlyDeclines_Component`, `MonthlyDepositsODRatio_Component`, `ODRepayment_Component`, `Overrides_Component`, `Windfall_Component`, `ACB_Component`, `Dep365_Component`, `CanOverdraftFalse` | Model scoring breakdown |
| **Balance Recovery** | `Last_Positive_Date`, `Last_Positive_Date_Balance`, `Last_Positive_Date_Limit`, `Next_Positive_Date`, `Next_Positive_Date_Balance`, `Next_Positive_Date_Limit` | How quickly account recovers |
| **Fee Ratios** | `NSFODFeesToDepositsRatio90Days`, `NSFODFeesToDepositsRatioRolling12Months` | Fee pressure at event time |
| **Other** | `WaiverReason`, `MCC`, `ItemDesc`, `exported` | Event context |

### The Join — Where the Richness Lives

```
ODDD (rewards_df)                    ZAccounts (zaccounts_df)
  Acct Number          ←— JOIN —→     HASHED_ACCOUNT
                       ↓
              deposits_df (merged)
                       ↓
         ┌─────────────┴─────────────┐
   deposits_personal_df        deposits_business_df
   (acct_type = Personal)      (acct_type = Business)
```

The merged `deposits_df` gives every cell access to:
- **ODDD monthly time series** (spend, swipes, OD items, PIN/Sig) for trend analysis
- **ZAccounts deposit windows** (33/66/99/365) for velocity and acceleration
- **ZAccounts risk signals** (repayment, fee ratios, trend indicators)
- **ODDD campaign data** (response grouping, segmentation) for responder analysis
- **ODDD demographics** (age, account age, branch) for segmentation
- **ZAccounts channel data** (auto-deposit, mobile deposits) for engagement analysis

---

## Key Analytical Concepts

### Nested Window Velocity
33 days is a subset of 66, which is a subset of 99, which is a subset of 365. Computing a daily deposit rate for each window reveals acceleration or deceleration:
- `rate_33 = DepCount33 / 33`
- `rate_66 = DepCount66 / 66`
- `rate_99 = DepCount99 / 99`
- `rate_365 = depCount365 / 365`

If `rate_33 > rate_365`, deposits are **accelerating**. If `rate_33 < rate_365`, deposits are **decelerating**.

### Mobile Deposit Share
`Mobile_Deposits_90` is a count of mobile deposits in 90 days. `DepCount99` is total deposits in 99 days (~similar window). Comparing these shows what share of deposits are mobile vs other channels.

### Deposits-Spend-Swipes Triangle
Three related behaviors from two data sources: how much they deposit (ZAccounts), how much they spend (ODDD monthly Spend), how often they swipe (ODDD monthly Swipes). Members who deposit heavily but don't spend are underutilizing the card program. Members who spend more than they deposit are potentially at risk.

---

## Chart Theme & Formatting Standards

All cells inherit from `01-general/01_general_theme`. Every chart must use these helpers consistently.

### Colors
```python
GEN_COLORS = {
    'primary':   '#1B2A4A',   # deep navy (main bars, headers)
    'accent':    '#E63946',   # signal red (highlights, alerts)
    'success':   '#2EC4B6',   # teal (positive, auto-deposit)
    'warning':   '#FF9F1C',   # amber (caution, medium risk)
    'info':      '#457B9D',   # steel blue (secondary data)
    'light_bg':  '#F8F9FA',   # off-white (card backgrounds)
    'dark_text': '#1B2A4A',   # titles, labels
    'muted':     '#6C757D',   # secondary text, inactive
    'grid':      '#E9ECEF',   # gridlines, borders
}
```

### Formatters
| Function | Use For | Example Output |
|----------|---------|----------------|
| `gen_fmt_dollar(x, _)` | Dollar amounts on axes | `$1.2M`, `$45K`, `$300` |
| `gen_fmt_count(x, _)` | Counts on axes | `1.2M`, `45K`, `12` |
| `gen_fmt_pct(x, _)` | Percentages | `12.3%` |
| `gen_fmt_index(x, _)` | Plain integers | `100` |
| `gen_clean_axes(ax)` | Remove top/right spines, disable grid | Conference-clean |

### Palettes Available
| Palette | Use For |
|---------|---------|
| `BRACKET_PALETTE` (8 colors) | Ordered bins (spending, deposit amount tiers) |
| `AGE_PALETTE` / `AGE_ORDER` | Age band breakdowns |
| `ENGAGE_PALETTE` / `ENGAGE_ORDER` | Engagement tiers (Power/Heavy/Moderate/Light/Dormant) |
| `ACCT_AGE_PALETTE` / `ACCT_AGE_ORDER` | Account age bands |
| `SPEND_TIER_PALETTE` / `SPEND_TIER_ORDER` | Spend tier breakdowns |

### Design Rules (5,000-Person Conference Room)
- Titles: **22pt bold**, `GEN_COLORS['dark_text']`
- Subtitles/axis labels: **16pt bold**
- Tick labels: **14pt**
- Bar value annotations: **14pt bold**
- KPI card values: **28pt bold**
- Figure DPI: **150** inline, **300** export
- Always call `gen_clean_axes(ax)` on every axis
- Always call `plt.tight_layout()` before `plt.show()`
- FancyBboxPatch for KPI cards with `light_bg` fill and colored border (linewidth=3)
- No chart clutter: no gridlines, no top/right spines
- High-contrast colors only -- must be readable from the back of a conference hall

---

## Section Architecture

**Section 23 = Personal Accounts.** All cells use `deposits_personal_df`. Every chart title includes "Personal Accounts" label.

**Section 24 = Business Accounts.** Mirror of section 23 using `deposits_business_df`. Same cells, same analysis, clearly labeled "Business Accounts." Can be a lighter section if business account count is small (auto-skip cells if < 50 business accounts).

**No comparison between Personal and Business.** Each section stands alone with its own KPIs and narrative.

Cell 01 (setup) lives in section 23 and creates both DataFrames. Section 24 references `deposits_business_df` from the same setup.

---

## Section 23: Personal Account Deposits

Working DataFrame: `deposits_personal_df` (open accounts, `acct_type == 'Personal'`)

### Setup
| Cell | Name | Purpose | Data Source | Key Fields |
|------|------|---------|-------------|------------|
| 01 | `deposit_setup` | Load Z files, join to ODDD, filter open accounts, split personal/business, build monthly column maps | ODDD + ZAccounts + ZTrends | All join/filter fields |

### Portfolio Overview
| Cell | Name | Purpose | Data Source | Key Fields |
|------|------|---------|-------------|------------|
| 02 | `deposit_kpis` | Personal account KPI cards: account count, deposits (33d/365d), median frequency, avg deposit amount, median balance, auto-deposit rate, mobile depositors, repayment rate | ZAccounts + ODDD | `depCount365`, `depAmt365`, `avgdaysbetweendeposits`, `balance`, `autodeposit`, `Mobile_Deposits_90`, `avgrepaymentrate` |

### Deposit Velocity & Patterns
| Cell | Name | Purpose | Data Source | Key Fields |
|------|------|---------|-------------|------------|
| 03 | `deposit_velocity` | **NEW.** Acceleration vs deceleration using nested windows. Compute daily rate per window, classify each account as accelerating/stable/decelerating, show distribution. | ZAccounts | `DepCount33`, `DepCount66`, `DepCount99`, `depCount365` |
| 04 | `deposit_frequency` | Distribution of days between deposits. Segment into weekly (<=7d), biweekly (8-16d), monthly (17-35d), infrequent (36d+). Horizontal bar chart showing segment sizes. | ZAccounts | `avgdaysbetweendeposits` |

### Deposit Engagement Features
| Cell | Name | Purpose | Data Source | Key Fields |
|------|------|---------|-------------|------------|
| 05 | `autodeposit_impact` | Auto-deposit vs no auto-deposit: side-by-side median comparison of deposit count, amount, frequency, balance, collected balance. | ZAccounts | `autodeposit`, `depCount365`, `depAmt365`, `avgdaysbetweendeposits`, `balance`, `AvgCollectedBalance` |
| 06 | `autodeposit_spend` | **NEW.** Cross-source: do auto-deposit users spend more on their cards? Compare median Total Spend, Total Swipes, MonthlySpend12 for auto vs non-auto. | ZAccounts + ODDD | `autodeposit`, `Total Spend`, `Total Swipes`, `MonthlySpend12` |
| 07 | `mobile_deposit_share` | **NEW.** What share of deposits are mobile? Compute `Mobile_Deposits_90 / DepCount99` per account. Show distribution and median share. | ZAccounts | `Mobile_Deposits_90`, `DepCount99` |
| 08 | `mobile_deposit_spend` | **NEW.** Cross-source: do mobile depositors spend more? Split accounts into mobile-depositor / non-mobile. Compare median Total Spend, Total Swipes. | ZAccounts + ODDD | `Mobile_Deposits_90`, `Total Spend`, `Total Swipes` |

### Deposits vs Spend & Swipes (Cross-Source Analysis)
| Cell | Name | Purpose | Data Source | Key Fields |
|------|------|---------|-------------|------------|
| 09 | `deposits_vs_fees_vs_swipes` | **NEW.** The triangle: 365-day deposit amount vs fee ratio vs swipe count. Grouped bar or multi-metric view. | ZAccounts + ODDD | `depAmt365`, `nsfodfeestodepositsratio90days`, `SIG_365`, `PIN_365` |
| 10 | `deposit_spend_correlation` | Scatter: annual deposit amount (ZAccounts) vs annual spend (ODDD). Color by velocity tier. Are heavy depositors heavy spenders? | ZAccounts + ODDD | `depAmt365`, `Total Spend` |
| 11 | `monthly_deposits_vs_spend` | Grouped bar: deposit amounts (depAmt365) at each ZAccounts snapshot vs cumulative card spend in the same trailing-365 window. Shows whether deposits and spend move together. | ZAccounts + ODDD | `depAmt365_{label}`, `spend_cols` |

### Longitudinal (Conditional — only if `ZA_HAS_MULTIPLE == True`)
| Cell | Name | Purpose | Data Source | Key Fields |
|------|------|---------|-------------|------------|
| 12 | `snapshot_deposit_trajectory` | Deposit count (365d) trajectory across snapshots with change annotation. Line chart or grouped bar showing each snapshot's median depCount365. | ZAccounts (multi-snapshot) | `depCount365_{label}` per snapshot via `ZA_SNAPSHOT_META` |
| 13 | `snapshot_frequency_trajectory` | Days between deposits trajectory across snapshots. Shows whether deposit frequency is improving or deteriorating. | ZAccounts (multi-snapshot) | `avgdaysbetweendeposits_{label}` per snapshot |

### Campaign Response (Cross-Source)
| Cell | Name | Purpose | Data Source | Key Fields |
|------|------|---------|-------------|------------|
| 14 | `campaign_responder_deposits` | ARS campaign responders vs non-responders: do responders deposit more frequently, larger amounts, better repayment? Grouped bar comparison. | ZAccounts + ODDD | `Response Grouping`, `depCount365`, `depAmt365`, `avgdaysbetweendeposits`, `avgrepaymentrate` |

### Risk Signals & Early Warning
| Cell | Name | Purpose | Data Source | Key Fields |
|------|------|---------|-------------|------------|
| 15 | `fee_pressure` | NSF/OD fees to deposits ratio distribution. Histogram with risk thresholds. Who is under fee pressure? | ZAccounts | `nsfodfeestodepositsratio90days` |
| 16 | `repayment_health` | Repayment rate distribution. Segment into low (<0.5), moderate (0.5-0.8), strong (>0.8). Horizontal bar with segment sizes and median deposit count per segment. | ZAccounts | `avgrepaymentrate`, `depCount365` |
| 17 | `deposit_risk_profile` | **NEW.** Composite risk score: deceleration + high fees + low repayment = high risk. Classify accounts into risk tiers, show distribution as donut or bar. | ZAccounts | `DepCount33`, `depCount365`, `nsfodfeestodepositsratio90days`, `avgrepaymentrate` |
| 18 | `closed_account_patterns` | **NEW.** Compare closed/chargeoff vs open accounts' deposit velocity, fee ratio, and repayment BEFORE closure. Validates whether velocity + fee signals predicted closure. Uses `deposits_closed_df` from cell 01. | ZAccounts + ODDD | `Stat Code`, `Date Closed`, velocity fields, fee/repayment fields |

### Monthly Trends
| Cell | Name | Purpose | Data Source | Key Fields |
|------|------|---------|-------------|------------|
| 19 | ~~`monthly_deposit_trend`~~ | **DELETED.** MTD columns are overdraft items, not deposits. Monthly deposit trends are impossible without monthly deposit data. Deposit trends are covered by snapshot-based cells (12, 21). | -- | -- |

### Summary
| Cell | Name | Purpose | Data Source | Key Fields |
|------|------|---------|-------------|------------|
| 20 | `deposit_summary` | Key findings as formatted text with mini-KPIs. No chart -- styled text output summarizing the story from cells 02-19. | All prior cells | Aggregated metrics |

---

## Section 24: Business Account Deposits

Working DataFrame: `deposits_business_df` (open accounts, `acct_type == 'Business'`)

### Architecture
- Mirror of section 23 cells, using `deposits_business_df` instead of `deposits_personal_df`
- All chart titles labeled **"Business Accounts"**
- Every cell begins with a business account count check: if < 50 accounts, auto-skip with a printed message
- Cell 01 is lightweight: confirms business account count, sets working DataFrame alias

### Cell Map
| Cell | Name | Notes |
|------|------|-------|
| 01 | `business_deposit_setup` | Lightweight: confirm business account count from `deposits_business_df`, print summary, set `_df = deposits_business_df`, set `_ACCT_LABEL = "Business Accounts"`, set `_MIN_ACCOUNTS = 50` |
| 02 | `business_deposit_kpis` | Same as S23 cell 02, using `deposits_business_df` |
| 03 | `business_deposit_velocity` | Same as S23 cell 03 |
| 04 | `business_deposit_frequency` | Same as S23 cell 04 |
| 05 | `business_autodeposit_impact` | Same as S23 cell 05 |
| 06 | `business_autodeposit_spend` | Same as S23 cell 06 |
| 07 | `business_mobile_deposit_share` | Same as S23 cell 07 |
| 08 | `business_mobile_deposit_spend` | Same as S23 cell 08 |
| 09 | `business_deposits_vs_fees_vs_swipes` | Same as S23 cell 09 |
| 10 | `business_deposit_spend_correlation` | Same as S23 cell 10 |
| 11 | `business_monthly_deposits_vs_spend` | Same as S23 cell 11 |
| 12 | `business_snapshot_deposit_trajectory` | Same as S23 cell 12 (conditional) |
| 13 | `business_snapshot_frequency_trajectory` | Same as S23 cell 13 (conditional) |
| 14 | `business_campaign_responder_deposits` | Same as S23 cell 14 |
| 15 | `business_fee_pressure` | Same as S23 cell 15 |
| 16 | `business_repayment_health` | Same as S23 cell 16 |
| 17 | `business_deposit_risk_profile` | Same as S23 cell 17 |
| 18 | `business_closed_account_patterns` | Same as S23 cell 18 |
| 19 | ~~`business_monthly_deposit_trend`~~ | **DELETED** (same as S23 cell 19) |
| 20 | `business_deposit_summary` | Same as S23 cell 20 |

---

## Cells Being Removed / Replaced

| Old Cell | Reason |
|----------|--------|
| 03a (window averages) | Replaced by cell 03 velocity analysis |
| 03b (frequency distribution) | Replaced by cell 04 (cleaner segmentation) |
| 03c (scatter frequency vs amount) | Low analytical value, not a clear story |
| 03d (window completion) | Overlaps with velocity analysis |
| 04 (trend data) + 04a-04d (4 snapshot cells) | Condensed to cells 12 + 13 (two focused trajectory cells) |
| 04e-04h (4 monthly cells) | Condensed to cell 19 (one monthly trend cell) |
| 05a (auto-deposit) | Replaced by cell 05 (cleaner) + cell 06 (cross-source) |
| 05b (mobile deposit) | Replaced by cell 07 + 08 (more insightful) |
| 05c (trend indicators) | Dropped -- confusing, unclear data semantics |
| 05e (repayment + fees combined) | Split into cells 15 + 16 (one chart each) |
| 06-07 (swipe + spend correlation) | Condensed to cells 09 + 10 + 11 (focused, one chart each) |
| 08-09 (ARS response + segmentation) | Condensed to cell 14 (one focused comparison) |
| 10 (ICS analysis) | Dropped -- conditional data, low priority |
| 11 (OD events) | Dropped for now -- ZTrends is secondary data source |
| 12 (summary dashboard) | Replaced by cell 20 (text-focused summary) |

## New Analyses Added

1. **Deposit Velocity** (cell 03) -- acceleration/deceleration from nested windows
2. **Auto-Deposit x Spend** (cell 06) -- cross-source: do auto-depositors spend more on their cards?
3. **Mobile Deposit Share** (cell 07) -- what % of deposits are mobile?
4. **Mobile Deposit x Spend** (cell 08) -- cross-source: do mobile depositors spend more?
5. **Deposits vs Fees vs Swipes** (cell 09) -- the triangle relationship across ZAccounts + ODDD
6. **Monthly Deposits vs Spend** (cell 11) -- dual trend comparison from ODDD monthly columns
7. **Deposit Risk Profile** (cell 17) -- composite risk score from velocity + fees + repayment
8. **Closed Account Patterns** (cell 18) -- validate early warning by comparing closed vs open deposit behavior
9. **Section 24 (Business)** -- full mirror of section 23 for business accounts

---

## Data Dependency Chain

```
00-setup/08-import-oddd
  → rewards_df (ODDD, ~47K accounts)

00-setup/09-oddd-account-type
  → business_flag on combined_df
  → business_df, personal_df (transaction-level splits)

23-deposits/01_deposit_setup
  → Loads ZAccounts (multi-snapshot) + ZTrends
  → Joins ZAccounts to rewards_df → deposits_df
  → Filters open accounts (Stat Code = 'O')
  → Preserves deposits_closed_df BEFORE filter (for cell 18)
  → Splits: deposits_personal_df, deposits_business_df
  → Auto-discovers monthly column maps (od_mtd_cols, spend_cols, etc.)
  → Builds longitudinal snapshot metadata (ZA_SNAPSHOT_META)
  |
  +-- deposits_personal_df (Section 23, cells 02-20)
  +-- deposits_business_df (Section 24, cells 01-20)
  +-- deposits_closed_df (Section 23 cell 18, Section 24 cell 18)
  |
  +-- Cells 12-13: conditional on ZA_HAS_MULTIPLE
  +-- Monthly columns: od_mtd_cols (OD items), spend_cols, swipes_cols, pin_amt_cols, etc.
```

---

## Cell 01 Updates Needed

Cell 01 needs one addition before the open-account filter: preserve closed/chargeoff accounts for cell 18:

```python
# Preserve pre-filter data for closed account analysis (cell 18)
deposits_closed_df = deposits_df[
    deposits_df['Stat Code'].astype(str).str.strip().str.upper() != 'O'
].copy()
print(f"    Closed/chargeoff accounts preserved: {len(deposits_closed_df):,}")
```

---

## Standards (Every Cell)

- Print data decisions before any chart (fields used, account counts, caps, exclusions)
- One chart per cell output (except cell 20 which is text summary)
- Handle missing fields gracefully (skip with descriptive warning)
- Section 23 cells use `deposits_personal_df`; Section 24 cells use `deposits_business_df`
- Every chart title includes account type label ("Personal Accounts" or "Business Accounts")
- Reference `GEN_COLORS`, `gen_clean_axes()`, formatters from `01-general/01_general_theme`
- Sequential numbering: `01_deposit_setup`, `02_deposit_kpis`, etc.
- No sub-letters (a, b, c, d, e, f, g, h)
- Figure sizes: `(16, 8)` for single charts, `(18, 6)` for side-by-side, `(18, 10)` for 2x3 grids
- Conference-ready: large fonts, bold colors, zero clutter, high contrast

## Implementation Order

1. Update cell 01 (add `deposits_closed_df` preservation before open-account filter)
2. Write Section 23 cells 02-04 (KPIs + velocity + frequency)
3. Write Section 23 cells 05-08 (engagement: auto-deposit + mobile deposit)
4. Write Section 23 cells 09-11 (deposits vs spend/swipes — cross-source)
5. Write Section 23 cells 12-13 (longitudinal — conditional)
6. Write Section 23 cell 14 (campaign response — cross-source)
7. Write Section 23 cells 15-18 (risk signals + early warning)
8. Write Section 23 cell 19 (monthly trend)
9. Write Section 23 cell 20 (summary)
10. Delete all old cells from section 23
11. Create `24-business-deposits/` directory
12. Write Section 24 cells 01-20 (business mirror)
13. Commit and push
