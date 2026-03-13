# feat: Robust Campaign Response & Deposit Impact Analysis

## Overview

Build a causal deposit impact framework for Sections 23 (Personal) and 24 (Business) that answers the question credit union executives actually care about: **"Did the campaign cause members to deposit more, and did it last?"**

The current 14-series cells (14-14f) show correlational comparisons -- responders have higher deposits than non-responders. But they never prove the campaign *caused* the increase. Section 09 already has a Difference-in-Differences (DiD) framework for card spend (`10_cohort_lift_data`, `14_cohort_spend_persistence`). This plan ports that methodology to deposits and extends it with longitudinal snapshot analysis, per-tier breakdowns, and a clean SO-SR cohort deep dive.

## Problem Statement / Motivation

**What exists today:**
- Cell 14: Static median comparison (Responder vs Non-Responder vs Never Mailed) using point-in-time ZAccounts fields
- Cell 14b: NU 1-4 conversion funnel
- Cell 14c: First-time vs repeat responder ladder
- Cell 14d: Monthly MTD/Spend trend by campaign status (visual only, no formal lift calculation)
- Cell 14e: Ladder movement direction deposits
- Cell 14f: Response Grouping breakout (SO-SR, MO-MR, etc.)

**What is missing:**
1. **No causal attribution** -- Responders may have already been high depositors before the campaign. No pre/post comparison exists.
2. **No DiD framework for deposits** -- Section 09 has this for spend but nothing equivalent for deposits.
3. **No persistence analysis** -- Does the deposit lift last 1/3/6 months? Or do members deposit to hit the threshold then stop?
4. **No longitudinal snapshot comparison by campaign status** -- The infrastructure exists (suffixed ZAccounts fields like `depAmt365_dec25`) but is never segmented by Responder/Non-Responder.
5. **No per-tier deposit analysis** -- All responders are lumped together. TH-25 members may behave very differently from NU 5+ members.
6. **No clean-cohort deep dive** -- SO-SR accounts (single offer, single response) are the cleanest signal of campaign effectiveness, but they only appear as one bar in 14f's grouped chart.

**Why it matters:**
- The current analysis can't answer "should we continue this program?" because it can't isolate campaign impact from selection bias
- Executives need incremental deposit dollars per reward dollar to justify program costs
- The data to do this properly already exists (36 months of ODDD MTD columns + multiple ZAccounts snapshots)

## Proposed Solution

### New Cells (5 total, each with personal + business mirror = 10 files)

```
Section 23 (Personal)                    Section 24 (Business)
-----------------------------------------  -----------------------------------------
14g_deposit_did_lift                      14g_business_deposit_did_lift
14h_deposit_persistence                   14h_business_deposit_persistence
14i_snapshot_deposit_change               14i_business_snapshot_deposit_change
14j_per_tier_deposits                     14j_business_per_tier_deposits
14k_so_sr_deposit_deep_dive               14k_business_so_sr_deposit_deep_dive
```

### Shared Infrastructure: Extract Classification to Setup

Before building new cells, extract the duplicated `_is_success()`, `_is_nu_partial()`, Mail/Resp column discovery, and `_challenge_tier()` into `01_deposit_setup`. Currently these are copy-pasted into every cell (14, 14b, 14c, 14d, 14e, 14f = 6 copies each). Adding 5 more cells would make 11 copies.

**Add to `01_deposit_setup` after the longitudinal join:**

```python
# 23-deposits/01_deposit_setup (new section ~line 380)

# ---------------------------------------------------------------------------
# 10. Campaign classification utilities (shared across 14-series cells)
# ---------------------------------------------------------------------------
import re as _re_camp

_camp_mail_pattern = _re_camp.compile(r'^([A-Z][a-z]{2}\d{2})\s+Mail$')
_camp_resp_pattern = _re_camp.compile(r'^([A-Z][a-z]{2}\d{2})\s+Resp$')

CAMP_MAIL_COLS = {}
CAMP_RESP_COLS = {}
for _col in deposits_personal_df.columns:
    _m = _camp_mail_pattern.match(_col)
    if _m:
        CAMP_MAIL_COLS[_m.group(1)] = _col
    _m = _camp_resp_pattern.match(_col)
    if _m:
        CAMP_RESP_COLS[_m.group(1)] = _col

def _month_sort_key(k):
    _mo = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,
           'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    return (int(k[3:])+2000, _mo.get(k[:3], 0))

CAMP_MAILER_KEYS = sorted(
    [k for k in CAMP_MAIL_COLS if k in CAMP_RESP_COLS],
    key=_month_sort_key
)

def camp_is_success(val):
    """True if response value indicates successful challenge completion."""
    if pd.isna(val):
        return False
    v = str(val).strip().upper()
    if v.startswith('TH'):
        return True
    if v in ('NU 5+', 'NU5+', 'NU 5', 'NU 6', 'NU 7', 'NU 8', 'NU 9', 'NU 10'):
        return True
    return False

def camp_is_nu_partial(val):
    """True if response value is NU 1-4 (active but missed goal)."""
    if pd.isna(val):
        return False
    v = str(val).strip().upper()
    return v in ('NU 1-4', 'NU1-4')

def camp_challenge_tier(val):
    """Extract numeric challenge tier from response value. 0 = not a success."""
    if pd.isna(val):
        return 0
    v = str(val).strip().upper()
    if v.startswith('TH-'):
        try:
            return int(v.replace('TH-', ''))
        except ValueError:
            return 5
    if v in ('NU 5+', 'NU5+', 'NU 5'):
        return 1
    return 0

CAMP_RESP_COL_LIST = [CAMP_RESP_COLS[k] for k in CAMP_MAILER_KEYS]
CAMP_MAIL_COL_LIST = [CAMP_MAIL_COLS[k] for k in CAMP_MAILER_KEYS]

HAS_CAMPAIGN_DATA = len(CAMP_MAILER_KEYS) >= 1

print(f"\n    Campaign data: {len(CAMP_MAILER_KEYS)} mailer periods")
if CAMP_MAILER_KEYS:
    print(f"    Periods: {CAMP_MAILER_KEYS[0]} to {CAMP_MAILER_KEYS[-1]}")
```

---

## Technical Approach

### Cell 14g: Deposit DiD Lift Analysis

**Purpose:** For each mailer wave, compute the incremental deposit impact attributable to the campaign using Difference-in-Differences methodology.

**Algorithm (mirrors `09-ars-campaign/10_cohort_lift_data`):**

```
For each mailer wave W:
  1. Identify accounts mailed in wave W (Mail col non-null)
  2. Classify: Responder (Resp = TH-* or NU 5+) vs Non-Responder (mailed but no success)
  3. Define pre-period: 3 MTD months before wave W's mail date
  4. Define post-period: 3 MTD months after wave W's mail date
  5. For each account, compute:
     - pre_avg = mean of pre-period MTD values (exclude NaN months)
     - post_avg = mean of post-period MTD values
     - delta = post_avg - pre_avg
  6. Compute DID:
     - resp_delta = median(delta) for Responders
     - nonresp_delta = median(delta) for Non-Responders
     - DID_lift = resp_delta - nonresp_delta
```

**Data dependencies:**
- `deposits_personal_df` with ODDD MTD columns (`mtd_cols` from setup)
- `CAMP_MAILER_KEYS`, `CAMP_MAIL_COLS`, `CAMP_RESP_COLS` from setup
- `camp_is_success()` from setup

**Edge cases:**
- Wave has <20 responders: skip wave, print warning
- Pre-period extends before data start: use available months only, require minimum 2
- Account NaN in all pre-period months: exclude from that wave (not yet open)
- NaN in MTD treated as 0 only if account has non-NaN in adjacent months (otherwise exclude)

**Output:**
- Conference-format table: Wave, Mailed, Responded, Resp Rate, Resp Pre->Post, NonResp Pre->Post, DID Lift, DID Lift %
- Single chart: Grouped bar per wave showing DID lift in dollars, with n= annotations
- Exports: `DEPOSIT_WAVE_DID` DataFrame for cell 14h

**File:** `23-deposits/14g_deposit_did_lift`

### Cell 14h: Deposit Persistence

**Purpose:** Does the deposit lift persist at 1, 3, and 6 months post-response? Or do members deposit to hit the threshold then revert?

**Algorithm (mirrors `09-ars-campaign/14_cohort_spend_persistence`):**

```
For each mailer wave W:
  1. Reuse wave classification from 14g (or re-derive independently)
  2. Compute post-period windows:
     - 1mo: first MTD month after wave
     - 3mo: months 1-3 after wave
     - 6mo: months 1-6 after wave
  3. For each window, compute DID lift (same as 14g)
  4. Persistence ratio = DID_lift_at_Nmo / DID_lift_at_1mo
```

**Edge cases:**
- Later waves (Dec25, Feb26) lack 6-month post data: show only available windows
- Require minimum 4 months of data for 6mo window (matching Section 09 pattern)

**Output:**
- Table: Wave x Window (1mo, 3mo, 6mo) showing DID lift and persistence ratio
- Chart: Heatmap or grouped bar showing lift decay across windows
- Narrative callout: "X% of deposit lift persists at 6 months" (aggregate across waves)

**File:** `23-deposits/14h_deposit_persistence`

### Cell 14i: Longitudinal Snapshot Deposit Change

**Purpose:** Use ZAccounts snapshots to show how deposit behavior changed between measurement points, segmented by campaign status.

**Algorithm:**

```
1. Check ZA_HAS_MULTIPLE and ZA_SNAPSHOT_META
2. For each account, compute delta between earliest and latest snapshot:
   - depAmt365_delta = depAmt365_{latest} - depAmt365_{earliest}
   - depCount365_delta = depCount365_{latest} - depCount365_{earliest}
   - balance_delta = balance_{latest} - balance_{earliest}
   - avgdays_delta = avgdaysbetweendeposits_{latest} - avgdaysbetweendeposits_{earliest}
3. Classify accounts by campaign status (Responder/Non-Responder/Never Mailed)
4. Compare median deltas across groups
5. Filter to accounts open before earliest snapshot (avoid account-age confound)
```

**Edge cases:**
- `ZA_HAS_MULTIPLE = False`: Show single-snapshot summary with message "trajectory requires 2+ snapshots"
- Snapshots <3 months apart: Warn that 365-day windows overlap significantly
- Account has NaN in one snapshot but not the other: exclude from delta calculation

**Output:**
- Table: Campaign Status x Metric showing median change per group
- Chart: Grouped bar of median deposit change (Responder vs Non-Responder vs Never Mailed)
- Annotation: snapshot date labels and window coverage from `ZA_SNAPSHOT_META`

**File:** `23-deposits/14i_snapshot_deposit_change`

### Cell 14j: Per-Tier Deposit Analysis

**Purpose:** Break deposit metrics by specific challenge tier instead of lumping all responders together. Do TH-25 members deposit more than TH-10 members?

**Algorithm:**

```
1. For each responder, determine their tier assignment:
   - Use MOST RECENT successful response tier (matching 14f's _last_success pattern)
   - camp_challenge_tier() extracts numeric tier from Resp value
2. Group responders by tier: NU 5+ (1), TH-10, TH-15, TH-20, TH-25
3. Compare deposit metrics per tier: depAmt365, depCount365, balance, avgdaysbetweendeposits, card spend, card swipes
4. Also show N and share per tier
```

**Edge cases:**
- Tier has <10 accounts: show in table with asterisk, omit from chart
- No TH-25 responders (common for smaller CUs): show available tiers only
- Tier ordering must follow hierarchy: NU 5+ < TH-10 < TH-15 < TH-20 < TH-25

**Output:**
- Table: Tier x Metric with N, share, and median values
- Chart: Grouped bar with one cluster per metric, bars colored by tier
- Narrative: "TH-25 members deposit Xx more than NU 5+ members"

**File:** `23-deposits/14j_per_tier_deposits`

### Cell 14k: SO-SR Deposit Deep Dive

**Purpose:** Single Offer, Single Response accounts are the cleanest attribution signal. They received one offer, responded once. Analyze their deposit behavior with maximum rigor.

**Algorithm:**

```
1. Filter to accounts where Response Grouping = 'SO-SR' (or equivalent value)
2. Identify the single wave they were mailed in
3. Compute mini-DID for this cohort:
   - Pre: 3 months of MTD before their mail wave
   - Post: 3 months of MTD after
   - Control: Non-responders from the same wave
4. Show deposit metrics (ZAccounts) vs. all other response groups
5. Show monthly MTD trend (pre/post) for SO-SR Responders vs SO-SR Non-Responders
```

**Edge cases:**
- `Response Grouping` column not present: skip with message
- <20 SO-SR accounts: skip DID, show only static comparison
- SO-SR value may be labeled differently in data: check for exact string match

**Output:**
- Summary: N accounts, single wave identified, response rate
- Table: SO-SR Responder vs SO-SR Non-Responder on deposit metrics
- Chart 1: Monthly deposit trend (pre/post with vertical line at mail date)
- DID callout: "SO-SR responders increased deposits by $X/month vs non-responders"

**File:** `23-deposits/14k_so_sr_deposit_deep_dive`

---

## Implementation Phases

### Phase 1: Infrastructure (shared setup)

- [x] Extract `camp_is_success()`, `camp_is_nu_partial()`, `camp_challenge_tier()` to `23-deposits/01_deposit_setup`
- [x] Extract `CAMP_MAIL_COLS`, `CAMP_RESP_COLS`, `CAMP_MAILER_KEYS`, `CAMP_RESP_COL_LIST`, `CAMP_MAIL_COL_LIST` to setup
- [x] Add `HAS_CAMPAIGN_DATA` flag
- [x] Update existing cells 14-14f to use shared functions (remove duplicated definitions)
- [x] Verify nothing breaks after refactor

### Phase 2: Core DiD Framework (14g + 14h)

- [x] Build `14g_deposit_did_lift` for personal accounts
  - [x] Wave discovery and pre/post window computation
  - [x] Per-wave DID calculation with NaN handling
  - [x] Conference-format table
  - [x] DID lift bar chart (one bar per wave)
  - [x] Export `DEPOSIT_WAVE_DID` DataFrame
- [x] Build `14h_deposit_persistence` for personal accounts
  - [x] Multi-window (1mo/3mo/6mo) DID computation
  - [x] Persistence ratio calculation
  - [x] Heatmap or grouped bar chart
- [x] Build business mirrors: `14g_business_deposit_did_lift`, `14h_business_deposit_persistence`
  - [x] Add `_MIN_ACCOUNTS` guards (threshold: 20 for DID)

### Phase 3: Snapshot + Tier Analysis (14i + 14j)

- [x] Build `14i_snapshot_deposit_change` for personal accounts
  - [x] Snapshot delta computation with account-age filter
  - [x] Campaign status segmentation
  - [x] Grouped bar chart
- [x] Build `14j_per_tier_deposits` for personal accounts
  - [x] Tier assignment via most-recent-success
  - [x] Per-tier median comparison table
  - [x] Tier-colored grouped bar chart
- [x] Build business mirrors: `14i_business_snapshot_deposit_change`, `14j_business_per_tier_deposits`

### Phase 4: SO-SR Deep Dive (14k)

- [x] Build `14k_so_sr_deposit_deep_dive` for personal accounts
  - [x] Response Grouping filter to SO-SR
  - [x] Single-wave DID computation
  - [x] Monthly trend chart with pre/post line
- [x] Build business mirror: `14k_business_so_sr_deposit_deep_dive`

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| MTD columns = monthly deposit dollars | Confirmed | Cell 14d already uses MTD with `gen_fmt_dollar`; column name "Month-To-Date" in deposit context means total deposits for that month |
| 14g builds its own wave config | Independent | Matches self-contained pattern of all existing 14-series cells; avoids cross-section dependency on Section 09 |
| NaN in MTD for accounts not yet open | Exclude account-wave pair | Account must have non-NaN in at least 2 of 3 pre-period months to be included in that wave's analysis |
| Multi-period responder tier assignment | Most recent success | Matches `14f`'s `_last_success` pattern and represents current tier standing |
| Pre/post window | 3 months each | Matches Section 09's `10_cohort_lift_data` pattern; deposits are monthly enough for 3-month windows |
| Minimum N for DID | 20 per group | Higher than existing 10 threshold because DID requires more statistical power |
| Minimum N for tier/group comparisons | 10 per group | Matches existing cells 14b/14e threshold |
| Never Mailed in 14g | Secondary reference, not in DID | DID compares Responder vs Non-Responder (both mailed); Never Mailed shown as reference line only |
| 14h dependency on 14g | Independent (re-derives) | Following the self-contained cell pattern, even though it duplicates wave computation |

## Acceptance Criteria

### Functional Requirements

- [ ] 14g produces per-wave DID deposit lift with conference-format table and bar chart
- [ ] 14h shows persistence at 1/3/6 months post-response
- [ ] 14i compares snapshot-to-snapshot deposit change by campaign status
- [ ] 14j breaks deposit metrics by challenge tier (NU 5+, TH-10, TH-15, TH-20, TH-25)
- [ ] 14k provides SO-SR focused DID with monthly pre/post trend
- [ ] All cells have business mirrors with `_MIN_ACCOUNTS` guards
- [ ] All cells use `GEN_COLORS`, `gen_clean_axes`, `gen_fmt_dollar`/`gen_fmt_count` formatting
- [ ] One chart per cell (one `plt.show()` call)
- [ ] Each cell is self-contained (can run independently given `deposits_personal_df` and setup globals)
- [ ] Shared classification functions extracted to `01_deposit_setup`

### Data Quality

- [ ] NU 1-4 never counted as success anywhere
- [ ] Account-wave pairs with insufficient pre-period data excluded
- [ ] Small-N groups flagged with asterisk in tables, omitted from charts
- [ ] Snapshot deltas filtered to accounts open before earliest snapshot

---

## Dependencies & Risks

| Risk | Mitigation |
|------|-----------|
| MTD columns may not be total deposit dollars | Validate with known account data before building full framework |
| Business accounts too few for per-wave DID | `_MIN_ACCOUNTS = 20` guard; may skip most waves |
| Response Grouping column missing for some CUs | 14k has graceful skip; other cells unaffected |
| Only 1 ZAccounts snapshot available | 14i degrades to single-point summary (no delta) |
| Seasonality confound in DID | DiD methodology inherently controls for common time trends; both responders and non-responders experience the same seasonal forces |

## References & Research

### Internal References
- Section 09 DiD framework: `09-ars-campaign/10_cohort_lift_data`
- Section 09 persistence: `09-ars-campaign/14_cohort_spend_persistence`
- Deposit setup: `23-deposits/01_deposit_setup` (lines 205-296 longitudinal join)
- Response Grouping: `23-deposits/14f_response_grouping_deposits`
- Tier extraction: `09-ars-campaign/07_response_ladder` (`_challenge_tier` function)
- Snapshot trajectory pattern: `23-deposits/12_snapshot_deposit_trajectory`

### Related Work
- Previous plan: `plans/fix-cell-14-response-filtering-segmentation.md`
- Previous plan: `plans/refactor-deposit-analysis-section-23.md`
- Closed issues: #56 (23-14 metrics), #58 (14-B NU fix), #54/#55 (snapshot 0 fix)

### Methodology
- Difference-in-Differences: `DID = (Resp_post - Resp_pre) - (NonResp_post - NonResp_pre)`
- Controls for selection bias (responders were already different) and time trends (deposits change for everyone)
- Balance persistence = % of deposited funds still in account after 30/60/90 days
- Tier graduation rate = % of TH-N completers who complete TH-(N+5) in subsequent period
