# feat: Unified Cross-Source Longitudinal Deposit Analysis

## Overview

Build a **true unified analysis layer** that fuses all three data sources (ODDD, ZAccounts, ZTrends) across three ZAccounts snapshots (Nov 2024, Jun 2025, Dec 2025) with campaign mailer timing to answer questions the current cells can't:

- "Did deposits accelerate or decelerate between snapshots — and did campaigns cause it?"
- "For the Jun25 mailer specifically, what happened to deposits before vs after?"
- "What do ZTrends OD events tell us about deposit recovery?"
- "Which accounts have deposit momentum vs which are declining?"

**The gap today:** Snapshot analysis (cells 12-13) and monthly ODDD analysis (cells 11, 19) exist in isolation. No cell aligns the 3 ZAccounts measurement points with the 17 months of ODDD monthly data AND the 6 campaign waves that fall between them. Additionally, ZTrends (56 fields) is loaded but completely unused, and ZAccounts trend indicator fields (`DepositTrendCount33`, `CashFlowTrendCount33`, etc.) are loaded but orphaned.

## Problem Statement / Motivation

### Current State

| Data Source | Fields | Status | Usage |
|---|---|---|---|
| ODDD Monthly (MTD/Spend/Swipes) | 17 months x 7 types | Heavily used | Aggregate trends (cell 11, 19), campaign segmentation (14d) |
| ZAccounts Latest Snapshot | 77 fields | Heavily used | Static KPIs, distributions, cross-source joins |
| ZAccounts Multi-Snapshot | 21 fields x 3 snapshots | Conditional use | Trajectory (cells 12, 13), delta (14i) — **isolated from ODDD** |
| ZTrends Events | 56 fields | **Never used** | Loaded in setup, orphaned |
| ZAccounts Trend Indicators | 4 fields | **Never used** | Loaded in longitudinal join, orphaned |

### What Executives Need

1. **Acceleration story**: "Are deposits growing faster or slower between measurement points? Is it the campaign or organic?"
2. **Campaign ROI with snapshot validation**: "The Jun25 campaign ran. Monthly MTD shows a bump. Does the Dec25 snapshot confirm sustained deposit growth?"
3. **Risk-deposit connection**: "Accounts that had OD events — did their deposit patterns change? Did they recover?"
4. **Momentum classification**: "Which accounts have positive deposit momentum right now?"

### The Three Snapshots (Key Dates)

```
Timeline:
  Sep24 Oct24 Nov24 Dec24 Jan25 Feb25 Mar25 Apr25 May25 Jun25 Jul25 Aug25 Sep25 Oct25 Nov25 Dec25 Jan26 Feb26
                ^                                          ^                                    ^
            Snapshot 1                                 Snapshot 2                            Snapshot 3
            (Nov 2024)                                 (Jun 2025)                            (Dec 2025)
                                            ^                   ^              ^                     ^         ^
                                         Apr25              Jun25          Aug25                 Oct25     Dec25  Feb26
                                         Mail               Mail           Mail                  Mail      Mail  Mail

  7-month gap: Nov24 → Jun25 (includes Apr25 mailer)
  6-month gap: Jun25 → Dec25 (includes Jun25, Aug25, Oct25 mailers)
```

This timeline is powerful: Snapshot 2 (Jun25) falls exactly at the Jun25 mailer wave. We can compare deposits BEFORE the mailer (using pre-Jun25 ODDD months) with the snapshot measurement, and then validate with Snapshot 3 (Dec25) 6 months later.

## Proposed Solution

### New Cells: 21-26 (6 cells, each with business mirror = 12 new files)

```
Section 23 (Personal)                       Section 24 (Business)
------------------------------------------  ------------------------------------------
21_snapshot_monthly_fusion                  21_business_snapshot_monthly_fusion
22_deposit_acceleration_profile             22_business_deposit_acceleration_profile
23_campaign_snapshot_validation             23_business_campaign_snapshot_validation
24_ztrends_od_deposit_recovery              24_business_ztrends_od_deposit_recovery
25_deposit_momentum_indicators              25_business_deposit_momentum_indicators
26_balance_deposit_dynamics                 26_business_balance_deposit_dynamics
```

---

## Technical Approach

### Cell 21: Snapshot-Monthly Fusion Timeline

**Purpose:** Align ZAccounts snapshot measurements with ODDD monthly deposits to show how monthly behavior leads up to and follows each snapshot.

**The Core Question:** "Does the monthly deposit trend from ODDD match what the snapshot says?"

**Algorithm:**

```
For each snapshot S (nov24, jun25, dec25):
  1. Get snapshot date → identify the 3 ODDD months leading up to it
     e.g., Jun25 snapshot → Apr25 MTD, May25 MTD, Jun25 MTD
  2. Get snapshot depAmt365_{label} for the account
  3. Compare: sum(3-month pre MTD) vs depAmt365 (rolling 365-day)
  4. Compute "recency ratio" = 3-month pre / (depAmt365/4)
     - Ratio > 1 = deposits accelerating recently
     - Ratio < 1 = deposits decelerating recently

For visualization:
  - X-axis: full 17-month ODDD timeline
  - Y-axis left: median monthly deposits (MTD) as line
  - Y-axis right: snapshot depAmt365 as large markers at snapshot dates
  - Vertical bands: 3-month windows leading up to each snapshot
  - Segmented by campaign status (Responder/Non-Responder/Never Mailed)
```

**Data Dependencies:**
- `deposits_personal_df` with snapshot-suffixed columns (`depAmt365_nov24`, etc.)
- `mtd_cols` from setup
- `ZA_SNAPSHOT_META` for snapshot dates and labels
- `CAMP_*` shared classification for segmentation

**Edge Cases:**
- `ZA_HAS_MULTIPLE = False`: Skip with message "requires 2+ snapshots"
- Snapshot month not in ODDD range: Use closest available months
- Account missing from a snapshot: Exclude from that snapshot's comparison

**Output:**
- Conference table: Snapshot x Group showing median depAmt365 and 3-month MTD sum
- Chart: Dual-axis timeline with snapshot markers and monthly trend lines
- Recency ratio distribution: histogram showing accelerating vs decelerating accounts

**File:** `23-deposits/21_snapshot_monthly_fusion`

---

### Cell 22: Deposit Acceleration Profile

**Purpose:** Classify every account's deposit trajectory across the 3 snapshots as Accelerating, Stable, or Decelerating. Cross-reference with spend behavior and campaign status.

**Algorithm:**

```
For each account with all 3 snapshots present:
  1. Compute inter-snapshot deltas:
     delta_1 = depAmt365_jun25 - depAmt365_nov24  (7-month change)
     delta_2 = depAmt365_dec25 - depAmt365_jun25  (6-month change)
  2. Compute acceleration = delta_2 - delta_1
     - If delta_1 > 0 AND delta_2 > delta_1: "Accelerating"
     - If delta_1 > 0 AND delta_2 > 0 AND delta_2 <= delta_1: "Stable Growth"
     - If delta_1 > 0 AND delta_2 <= 0: "Peaked & Declining"
     - If delta_1 <= 0 AND delta_2 > 0: "Recovering"
     - If delta_1 <= 0 AND delta_2 <= 0 AND delta_2 < delta_1: "Accelerating Decline"
     - If delta_1 <= 0 AND delta_2 <= 0 AND delta_2 >= delta_1: "Stable Decline"
  3. Also compute for depCount365, balance, avgdaysbetweendeposits
  4. Cross-tab: Acceleration category x Campaign Status
```

**Data Dependencies:**
- `depAmt365_{label}` for all 3 snapshots
- `depCount365_{label}`, `balance_{label}`, `avgdaysbetweendeposits_{label}`
- Campaign classification from setup

**Output:**
- Table: Acceleration category x Campaign Status with N and median depAmt365 at latest snapshot
- Chart: Stacked bar showing distribution of acceleration categories by campaign status
- Narrative: "X% of responders are accelerating vs Y% of non-responders"

**File:** `23-deposits/22_deposit_acceleration_profile`

---

### Cell 23: Campaign-Snapshot Validation

**Purpose:** For each campaign wave, validate the DiD lift (from cell 14g) against ZAccounts snapshot changes. Does the monthly MTD lift translate into real deposit growth at the next snapshot?

**The Core Question:** "The Jun25 campaign showed a $X/mo DiD lift in MTD. Did the Dec25 snapshot confirm it?"

**Algorithm:**

```
For each campaign wave W:
  1. Identify the snapshot BEFORE and AFTER the wave:
     - Apr25 wave: before=nov24, after=jun25
     - Jun25 wave: before=jun25 (or nov24), after=dec25
     - Aug25 wave: before=jun25, after=dec25
     - Oct25 wave: before=jun25, after=dec25
     - Dec25 wave: before=dec25, after=None (no later snapshot)
  2. For Responders vs Non-Responders in wave W:
     - Compute snapshot delta: depAmt365_{after} - depAmt365_{before}
     - Compute snapshot DID: resp_snapshot_delta - nonresp_snapshot_delta
  3. Compare:
     - MTD-based DID (from 14g pattern, monthly ODDD data)
     - Snapshot-based DID (from ZAccounts rolling 365-day window)
  4. Agreement score: Do both methods show positive/negative lift?

For Jun25 specifically (your cleanest case):
  - Pre-campaign MTD: Mar25, Apr25, May25 from ODDD
  - Post-campaign MTD: Jul25, Aug25, Sep25 from ODDD
  - Snapshot validation: depAmt365_jun25 → depAmt365_dec25
  - This gives BOTH monthly and snapshot confirmation
```

**Edge Cases:**
- Wave has no post-snapshot (Dec25 wave): show MTD-based DID only, note "awaiting next snapshot"
- Wave falls between same snapshot pair: multiple waves validated against same delta
- Account missing from pre/post snapshot: exclude from that wave's snapshot DID

**Output:**
- Table: Wave, MTD DID, Snapshot DID, Agreement (Yes/No), N
- Chart: Paired bar per wave showing MTD-DID vs Snapshot-DID side by side
- Callout: "Jun25 campaign: MTD shows $X/mo lift, snapshot confirms $Y annual lift"

**File:** `23-deposits/23_campaign_snapshot_validation`

---

### Cell 24: ZTrends OD-Deposit Recovery Analysis

**Purpose:** First real use of ZTrends data. Analyze deposit patterns around overdraft events — do depositors recover? How quickly? What predicts recovery?

**Algorithm:**

```
1. Join ztrends_df to deposits_personal_df on acctid
2. Filter to accounts with OD events (ztrends_df rows with PossibleFees > 0 or CollectedFees > 0)
3. For each account with OD events:
   - Count total OD events
   - Get deposit counts at event: depcount33, depcount66, depcount99
   - Get deposit totals at event: deptotal33, deptotal66, deptotal99
   - Get balance recovery: Last_Positive_Date_Balance, Next_Positive_Date_Balance
   - Get recovery timing: days between Last_Positive_Date and Next_Positive_Date
4. Classify recovery:
   - "Quick Recovery" = Next_Positive_Date within 7 days
   - "Moderate Recovery" = 8-30 days
   - "Slow Recovery" = 31-90 days
   - "No Recovery" = no Next_Positive_Date or > 90 days
5. Compare deposit metrics (from ZAccounts latest) by recovery category
6. Also cross-tab with campaign status
```

**Data Dependencies:**
- `ztrends_df` (finally used!)
- `deposits_personal_df` for account-level metrics
- Join key: `acctid` in both tables

**Edge Cases:**
- ZTrends empty or not loaded: skip with message
- No OD events in dataset: skip with "no overdraft events found"
- Multiple OD events per account: use most recent, or aggregate
- ztrends_df doesn't have matching acctid format: try HASHED_ACCOUNT fallback

**Output:**
- Summary: N accounts with OD events, recovery distribution
- Table: Recovery Category x Deposit Metrics (depAmt365, balance, deposit frequency)
- Chart: Recovery distribution donut + deposit comparison bar chart
- Narrative: "X% of OD accounts recover deposits within 30 days"

**File:** `23-deposits/24_ztrends_od_deposit_recovery`

---

### Cell 25: Deposit Momentum Indicators

**Purpose:** Use the orphaned ZAccounts trend fields to create a "deposit momentum" profile. These 33-day directional signals have been loaded but never analyzed.

**Algorithm:**

```
1. Extract trend fields (loaded in longitudinal join):
   - DepositTrendCount33: count of 33-day periods with increasing deposits
   - CashFlowTrendCount33: cash flow stability trend
   - WindfallTrendCount33: windfall (large deposit) events
   - RepaymentTrendCount33: OD repayment behavior trend
2. Create composite momentum score:
   - Positive momentum = DepositTrendCount33 > 0 AND CashFlowTrendCount33 > 0
   - Negative momentum = DepositTrendCount33 < 0 OR CashFlowTrendCount33 < 0
   - Windfall-driven = WindfallTrendCount33 > 2 (deposits spiked by large events)
3. Compare across snapshots if available:
   - Momentum at nov24 vs jun25 vs dec25
   - Did momentum predict actual deposit growth?
4. Cross-tab with campaign status and actual deposit trajectory (from cell 22)
```

**Data Dependencies:**
- `DepositTrendCount33`, `CashFlowTrendCount33`, `WindfallTrendCount33`, `RepaymentTrendCount33`
- Snapshot-suffixed versions if available (e.g., `DepositTrendCount33_nov24`)
- Campaign classification from setup

**Edge Cases:**
- Trend fields all zero or all NaN: skip with "no trend data available"
- Fields not in DataFrame (CU doesn't provide them): graceful skip per field
- Only latest snapshot has trend data: use single-snapshot analysis

**Output:**
- Table: Momentum category x Campaign Status with N, median depAmt365, median spend
- Chart: Grouped bar showing deposit metrics by momentum category
- If multi-snapshot: small-multiple showing momentum changes over time

**File:** `23-deposits/25_deposit_momentum_indicators`

---

### Cell 26: Balance-Deposit Dynamics

**Purpose:** Analyze how deposit behavior drives balance changes across snapshots. Which deposit patterns lead to balance growth vs decline?

**Algorithm:**

```
1. Compute balance trajectory across 3 snapshots:
   - balance_change = balance_dec25 - balance_nov24
   - Classify: Balance Grew (>10%), Stable (-10% to +10%), Declined (<-10%)
2. For each balance trajectory group:
   - Show deposit metrics: depAmt365, depCount365, avgdaysbetweendeposits at each snapshot
   - Show monthly MTD trend (from ODDD) — do monthly deposits predict balance direction?
   - Show card spend (from ODDD) — does spend offset deposit gains?
3. Compute "deposit efficiency ratio":
   - efficiency = balance_change / sum(all MTD deposits in period)
   - High efficiency = deposits staying in account
   - Low efficiency = deposits immediately spent/withdrawn
4. Segment by campaign status: do responders have higher deposit efficiency?
```

**Data Dependencies:**
- `balance_{label}` for all 3 snapshots
- `depAmt365_{label}`, `depCount365_{label}`
- `mtd_cols` for monthly deposit sums
- Campaign classification

**Output:**
- Table: Balance Trajectory x Deposit Efficiency x Campaign Status
- Chart: Scatter plot of balance change vs total deposits, colored by campaign status
- Narrative: "Responders with $X+ deposits grew balance Y%, vs Z% for non-responders"

**File:** `23-deposits/26_balance_deposit_dynamics`

---

## Implementation Phases

### Phase 1: Infrastructure Check (setup validation)

- [x] Verify `ZA_HAS_MULTIPLE == True` with 3 snapshots (nov24, jun25, dec25)
- [x] Verify all `_LONGITUDINAL_FIELDS` have suffixed columns in `deposits_personal_df`
- [x] Verify `ztrends_df` is loaded and has joinable `acctid` field
- [x] Verify trend indicator fields exist (`DepositTrendCount33`, etc.)
- [x] Verify `mtd_cols` spans Sep24 through Jan26 (17 months)
- [x] Document any missing fields per data source

### Phase 2: Core Fusion (cells 21-22)

- [x] Build `21_snapshot_monthly_fusion` for personal accounts
  - [x] Align snapshot dates with ODDD monthly timeline
  - [x] Compute recency ratio per account per snapshot
  - [x] Dual-axis timeline chart with snapshot markers
  - [x] Conference table with snapshot x group medians
- [x] Build `22_deposit_acceleration_profile` for personal accounts
  - [x] 3-snapshot delta and acceleration computation
  - [x] 6-category classification (Accelerating through Accelerating Decline)
  - [x] Cross-tab with campaign status
  - [x] Stacked bar chart
- [x] Build business mirrors for cells 21-22

### Phase 3: Campaign Validation + ZTrends (cells 23-24)

- [x] Build `23_campaign_snapshot_validation` for personal accounts
  - [x] Map each wave to before/after snapshot pair
  - [x] Compute snapshot-based DID alongside MTD-based DID
  - [x] Agreement analysis
  - [x] Paired bar chart
- [x] Build `24_ztrends_od_deposit_recovery` for personal accounts
  - [x] Join ztrends_df on acctid
  - [x] OD event classification and recovery timing
  - [x] Recovery category x deposit metrics
  - [x] Donut + bar chart
- [x] Build business mirrors for cells 23-24

### Phase 4: Momentum + Balance (cells 25-26)

- [x] Build `25_deposit_momentum_indicators` for personal accounts
  - [x] Trend field extraction and composite scoring
  - [x] Multi-snapshot momentum comparison (if available)
  - [x] Momentum x campaign status cross-tab
- [x] Build `26_balance_deposit_dynamics` for personal accounts
  - [x] Balance trajectory classification
  - [x] Deposit efficiency ratio computation
  - [x] Scatter plot of balance change vs deposits
- [x] Build business mirrors for cells 25-26

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Cell numbering 21-26 | Continue from existing 20 | Maintains sequential order; all cells beyond 20 are "unified analysis" |
| ZTrends join key | `acctid` first, `HASHED_ACCOUNT` fallback | ZTrends uses `acctid`; may need mapping via ZAccounts which has both |
| Acceleration classification | 6 categories | Captures direction + velocity change; "Peaked & Declining" is the executive red flag |
| Snapshot-to-wave mapping | Pre = closest snapshot before wave, Post = first snapshot after | Natural alignment; some waves share same snapshot pair |
| Deposit efficiency ratio | balance_change / sum(MTD) | Normalizes for deposit volume — a $10K depositor growing $1K is less efficient than $2K depositor growing $500 |
| Minimum N for ZTrends | 50 accounts with OD events | ZTrends rows are event-level, need critical mass for meaningful patterns |
| Business mirror threshold | `_MIN_ACCOUNTS` (existing pattern) | Consistent with all existing business cells |

## Data Source Integration Map

```
                  ┌─────────────────────────────┐
                  │          Cell 21             │
                  │   Snapshot-Monthly Fusion    │
                  │                             │
  ODDD Monthly ──►│  MTD timeline + snapshot    │◄── ZAccounts Snapshots
  (mtd_cols)      │  markers aligned on dates   │    (depAmt365_{label})
                  └─────────────────────────────┘

                  ┌─────────────────────────────┐
                  │          Cell 22             │
                  │   Acceleration Profile      │
                  │                             │
                  │  3-snapshot deltas →         │◄── ZAccounts Snapshots
  Campaign ──────►│  acceleration categories    │    (all _LONGITUDINAL_FIELDS)
  Classification  │  cross-tabbed with status   │
                  └─────────────────────────────┘

                  ┌─────────────────────────────┐
                  │          Cell 23             │
                  │   Campaign-Snapshot Valid.   │
                  │                             │
  ODDD Monthly ──►│  MTD-DID vs Snapshot-DID    │◄── ZAccounts Snapshots
  Campaign Waves─►│  per wave, agreement score  │    (depAmt365_{label})
                  └─────────────────────────────┘

                  ┌─────────────────────────────┐
                  │          Cell 24             │
                  │   ZTrends OD Recovery       │
                  │                             │
  ZTrends ───────►│  OD events + recovery time  │◄── ZAccounts Latest
  (first use!)    │  deposit patterns at OD     │    (deposit metrics)
                  └─────────────────────────────┘

                  ┌─────────────────────────────┐
                  │          Cell 25             │
                  │   Momentum Indicators       │
                  │                             │
  ZAccounts ─────►│  Trend fields → composite   │◄── ZAccounts Snapshots
  Trend Fields    │  momentum score over time   │    (suffixed trend fields)
  (first use!)    │                             │
                  └─────────────────────────────┘

                  ┌─────────────────────────────┐
                  │          Cell 26             │
                  │   Balance-Deposit Dynamics   │
                  │                             │
  ODDD Monthly ──►│  Total MTD deposits vs      │◄── ZAccounts Snapshots
  ZAccounts ─────►│  balance change trajectory  │    (balance_{label})
  Campaign ──────►│  deposit efficiency ratio   │
                  └─────────────────────────────┘
```

## Acceptance Criteria

### Functional Requirements

- [ ] Cell 21 produces dual-axis chart aligning ODDD monthly trend with snapshot measurement points
- [ ] Cell 22 classifies every multi-snapshot account into one of 6 acceleration categories
- [ ] Cell 23 compares MTD-based DID with snapshot-based DID for each campaign wave
- [ ] Cell 24 analyzes ZTrends data for the first time — OD recovery patterns
- [ ] Cell 25 uses orphaned trend indicator fields for momentum scoring
- [ ] Cell 26 connects balance trajectory to deposit behavior and campaign status
- [ ] All cells have business mirrors with `_MIN_ACCOUNTS` guards
- [ ] All cells use `GEN_COLORS`, `gen_clean_axes`, `gen_fmt_dollar`/`gen_fmt_count`
- [ ] One chart per cell (one `plt.show()` call)
- [ ] Each cell is self-contained (given `deposits_personal_df` and setup globals)
- [ ] Cells 21-23 require `ZA_HAS_MULTIPLE == True` (graceful skip otherwise)
- [ ] Cell 24 requires `ztrends_df` with joinable account identifier

### Data Quality

- [ ] Accounts missing from any snapshot excluded from that snapshot's analysis (not imputed)
- [ ] ZTrends join validated with match rate printed
- [ ] Small-N groups flagged with asterisk in tables
- [ ] Trend indicator fields checked for existence before use (CU may not provide all)

## Dependencies & Risks

| Risk | Mitigation |
|------|-----------|
| ZTrends `acctid` doesn't match ZAccounts `acctid` | Try HASHED_ACCOUNT fallback; print match rate |
| Only 2 snapshots available (not 3) | Acceleration profile degrades to 2-category (Growth/Decline); cells still work |
| Trend indicator fields all NaN | Cell 25 skips gracefully; other cells unaffected |
| Jun25 snapshot date not exactly at campaign wave | Use closest month alignment; document offset |
| Business accounts too few for OD analysis | `_MIN_ACCOUNTS` guard; ZTrends cell may skip for business |
| Snapshot 365-day windows overlap (Nov24 and Jun25 are only 7 months apart) | Document overlap; use depAmt365 as "best available" rather than independent measurement |

## References & Research

### Internal References
- Deposit setup: `23-deposits/01_deposit_setup` (sections 2-5: ZAccounts loading, section 5: longitudinal join)
- Snapshot trajectory: `23-deposits/12_snapshot_deposit_trajectory` (existing snapshot pattern)
- Monthly trend: `23-deposits/11_monthly_deposits_vs_spend` (existing ODDD monthly pattern)
- DiD framework: `23-deposits/14g_deposit_did_lift` (existing wave config + DID calculation)
- Campaign classification: `23-deposits/01_deposit_setup` (section 10: shared camp_* functions)

### Data Source Field Lists
- ODDD fields: `/Users/jgmbp/TXN-v4-complete/oddd` and `00-setup/expected-fields`
- ZAccounts fields: `/Users/jgmbp/TXN-v4-complete/zaccounts`
- ZTrends fields: `/Users/jgmbp/TXN-v4-complete/ztrends`

### Key Variables Available from Setup
- `ZA_SNAPSHOT_META`: OrderedDict with snapshot dates and labels
- `ZA_HAS_MULTIPLE`: Boolean for multi-snapshot availability
- `_LONGITUDINAL_FIELDS`: List of 21 fields tracked per snapshot
- `mtd_cols`, `spend_cols`, `swipes_cols`: ODDD monthly column maps
- `DEP_MONTHS`: Chronological list of all monthly period keys
- `CAMP_MAILER_KEYS`, `CAMP_MAIL_COLS`, `CAMP_RESP_COLS`: Campaign wave data
- `camp_is_success()`, `camp_challenge_tier()`: Classification functions
- `ztrends_df`: ZTrends DataFrame (loaded but currently unused)
