## Overview

Fix cell 14 and add new cells for campaign responder analysis in Sections 23 + 24:

1. **Cell 14** — Response Types: Per-mailer SO/MO × SR/MR breakdown with deposit/spend metrics. Filter `Response Grouping` (which contains offer×response cross-tab labels like SO-SR, MO-MR). Exclude NU 1-4 as non-responders.
2. **New cell 16** — NU 1-4 Conversion Journey: Track partial activators across periods via `MmmYY Segmentation` columns. Show who graduated from NU 1-4 to TH-* or NU 5+ in later waves, with deposit behavior changes.
3. **New cell 17** — Ladder Movement: Multi-period responders moving up/down challenge tiers over time.

All changes mirrored to Section 24 (Business) with `_MIN_ACCOUNTS` guard.

## Context

Section 23 tells a narrowing funnel story: all personal accounts → open → active depositors → recent depositors → **ARS campaign responders**. Cell 14 is the capstone showing whether successful responders also deposit more.

- ARS = debit card rewards program incentivizing swipes
- Success = NU 5+ (non-user activated 5+ swipes) or TH-* (hit spending threshold)
- NU 1-4 = partial activation, NOT responders, but their conversion journey matters

## Data Structure

**Response Grouping** (col 436): Contains offer × response cross-tab labels — SO-SR, SO-MR, MO-SR, MO-MR type values.

**Three column families per period** (from ODDD):

| Family | Pattern | Values |
|---|---|---|
| Mail | `MmmYY Mail` | SO (Single Offer), MO (Multiple Offer) |
| Resp | `MmmYY Resp` | SR (Single Response), MR (Multiple Response) |
| Segmentation | `MmmYY Segmentation` | TH-10, TH-15, TH-20, TH-25, NU 5+, NU 1-4 |

Additional: `# of Offers` (col 434), `# of Responses` (col 435)

---

## Cell 14: Response Types (fix existing)

### Changes

1. **Filter Response Grouping**: Exclude any group containing NU 1-4 values. Only show true responder groups (SO-SR, MO-MR, etc. where the response indicates actual success).

2. **Per-mailer response rate table** (already done with Mail/Resp pairs) — keep as-is with offer/resp type transparency.

3. **Response Grouping metric comparison**: Bar chart comparing deposit/spend/swipe medians across SO-SR, SO-MR, MO-SR, MO-MR groups.

4. **Monthly spend trend** (already done) — keep, but only for true responder groups.

### Files
- `23-deposits/14_campaign_responder_deposits`
- `24-business-deposits/14_business_campaign_responder_deposits`

---

## New Cell 16: NU 1-4 Conversion Journey

Track whether partial activators (NU 1-4) eventually convert to true responders.

### Analysis

1. **Discover Segmentation columns** alongside Mail/Resp:
   ```python
   _seg_pattern = re.compile(r'^([A-Z][a-z]{2}\d{2})\s+Segmentation$')
   ```

2. **Build per-account timeline**: For each account, track their Segmentation value across periods. Identify accounts that were NU 1-4 in any period.

3. **Conversion funnel**:
   - Total NU 1-4 accounts (ever)
   - How many later became NU 5+ or TH-*
   - Conversion rate by original NU period (earlier NU 1-4 → more time to convert)

4. **Deposit behavior**: Compare deposit metrics (depAmt365, depCount365) for:
   - NU 1-4 who converted → true responder
   - NU 1-4 who never converted
   - Never-mailed baseline

5. **Charts**:
   - Conversion funnel bar (total NU 1-4 → converted → never converted)
   - Deposit comparison grouped bars (converters vs non-converters)

### Reference Pattern
Existing logic in `09-ars-campaign/03_campaign_response_grouping` already does NU conversion analysis — adapt for deposits context.

### Files
- `23-deposits/16_nu_conversion_journey` (new)
- `24-business-deposits/16_business_nu_conversion_journey` (new)

---

## New Cell 17: Ladder Movement

For accounts that responded in 2+ periods, did they move up, down, or stay same?

### Analysis

1. **Challenge tier mapping** (from Section 09 pattern):
   ```python
   def _challenge_tier(val):
       v = str(val).strip().upper()
       if v.startswith('TH-'):
           return int(v.replace('TH-', ''))  # 10, 15, 20, 25
       if v in ('NU 5+', 'NU5+'):
           return 1
       return 0
   ```

2. **Movement classification**: Compare tier in consecutive response periods:
   - Up = higher tier than previous response
   - Same = same tier
   - Down = lower tier

3. **Deposit correlation**: Do accounts moving up the ladder also deposit more?

4. **Charts**:
   - Donut: first-time vs repeat responders
   - Horizontal bar: Up / Same / Down movement distribution
   - Deposit comparison by movement direction

### Reference Pattern
Existing logic in `09-ars-campaign/07_response_ladder` — adapt for deposits context.

### Files
- `23-deposits/17_response_ladder_deposits` (new)
- `24-business-deposits/17_business_response_ladder_deposits` (new)

---

## Acceptance Criteria

### Cell 14
- [ ] Response Grouping filtered — NU 1-4 excluded from responder groups
- [ ] SO-SR, MO-MR etc. groups shown with deposit/spend/swipe medians
- [ ] Per-mailer response rate table retained (Mail/Resp pairs)
- [ ] Monthly spend trend retained for true responder groups only

### Cell 16
- [ ] NU 1-4 conversion funnel with rates by originating period
- [ ] Deposit behavior comparison: converters vs non-converters
- [ ] Conference-format data table + chart

### Cell 17
- [ ] Ladder movement for repeat responders (Up/Same/Down)
- [ ] Deposit metrics by movement direction
- [ ] Conference-format data table + chart

### Both Sections
- [ ] All cells mirrored to Section 24 with `_MIN_ACCOUNTS` guard
- [ ] Uses existing helper functions (gen_fmt_dollar, gen_fmt_count, gen_clean_axes, GEN_COLORS)
