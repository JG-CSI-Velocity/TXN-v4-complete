# Section 23: Deposit Relationship & ARS Impact -- Presenter Guide

45 cells. Every comparison is WITHIN the same challenge cohort: members assigned TH-15 who responded vs members assigned TH-15 who didn't. Never Mailed as the baseline.

---

## DATA PIPELINES (Cells 00-04) -- Run first, don't present

| Cell | What it does |
|------|-------------|
| 00 | Section notes (hardcoded client values) |
| 01 | Loads 3 zaccounts snapshots, joins to ODDD, builds matched cohort |
| 02 | Builds response journey from Mail/Resp columns |
| 03 | Monthly spend/deposit timeline aggregation (optional, needs Spend columns) |
| 04 | Downloads NCUA 5300 + FRED economic data (needs internet) |

## INSTITUTIONAL CONTEXT (Cells 05-10) -- Set the stage

| Cell | Title | One-line |
|------|-------|----------|
| 05 | Total Deposits Over Time | USF FCU vs FL peer median |
| 06 | Membership Growth | Are deposits from new members or deepening? |
| 07 | Fee Income Trend | Institution-level fee revenue |
| 08 | Net Worth Ratio | Capital adequacy backdrop |
| 09 | FRED Macro Context | FL unemployment, Fed Funds, CPI |
| 10 | Peer Comparison | QoQ deposit growth vs peers |

---

## CHALLENGE COHORT ENGINE (Cell 11) -- Run after 01-02, don't present

Parses Mail column to get challenge assignment (NU, TH-10/15/20/25). Classifies each mailed account as Hit / Near Miss / No Response. Computes pre/post spend, MTD, deposits. Builds `challenge_cohort_df`.

---

## BLOCK A: Campaign Overview (Cells 12-15)

**Talk track:** "Here's who we mailed, what challenges they received, and the response rates."

| Cell | Title | Talk Track |
|------|-------|-----------|
| 12 | Challenge Distribution | "X accounts mailed across 5 challenge levels." |
| 13 | Response Rate by Challenge | "TH-10 hits at X%, NU at Y% -- lower challenges are easier to hit." |
| 14 | Response Rate by Wave | "Response rates are [improving/stable/declining] wave over wave." |
| 15 | Portfolio KPIs | "Six headline numbers for the deposit portfolio." |

---

## BLOCK B: Spend Proof (Cells 16-19)

**Talk track:** "Within the SAME challenge cohort, did responding lift card spend?"

| Cell | Title | Talk Track |
|------|-------|-----------|
| 16 | **Spend Change by Challenge** | "For TH-15: responders lifted spend by $X/mo, non-responders by $Y. That's a $Z DID lift -- same challenge, two outcomes." |
| 17 | Spend Persistence | "The lift holds at +3 and +6 months -- this isn't a one-month spike." |
| 18 | Monthly Spend Timeline | "Full timeline. Dotted lines = mailer waves. Green = responded, gray = didn't." |
| 19 | Card Activation Rate | "X% of responders have card activity each month vs Y% of non-responders." |

---

## BLOCK C: Deposit Proof (Cells 20-24)

**Talk track:** "Same cohort comparison on deposits -- the metric that matters most to the credit union."

| Cell | Title | Talk Track |
|------|-------|-----------|
| 20 | **Deposit Balance by Challenge** | "Responders carry $X more in deposits than non-responders in the same challenge. Dashed line = never mailed." |
| 21 | Deposit Amount (365d) | "Responders deposited $X over the year vs $Y for non-responders." |
| 22 | Deposit Count (365d) | "Responders deposit X times per year vs Y -- it's frequency, not just amount." |
| 23 | Deposit Acceleration | "33-day deposit velocity is [accelerating/decelerating] for responders across our 3 snapshots." |
| 24 | Direct Deposit Rate | "X% of responders have direct deposit vs Y% -- the stickiest relationship signal." |

---

## BLOCK D: Activity & Risk (Cells 25-28)

**Talk track:** "Beyond spend and deposits, are responders healthier accounts?"

| Cell | Title | Talk Track |
|------|-------|-----------|
| 25 | MTD Items by Challenge | "More MTD items = more account activity. Responders show [more/less] activity." |
| 26 | Fee Revenue by Challenge | "Responders generate $X in annual fees vs $Y for non-responders." |
| 27 | Repayment Rate | "When responders overdraft, they repay X% faster." |
| 28 | OD Frequency | "Responders go negative X times/year vs Y for non-responders." |

---

## BLOCK E: NU Deep Dive (Cells 29-31)

**Talk track:** "The NU accounts are the activation story. These are non-users who got mailed -- zero card activity. Three outcomes: activated (5+), almost there (1-4), or nothing."

| Cell | Title | Talk Track |
|------|-------|-----------|
| 29 | **NU: Three Outcomes** | "Same target group, same mailer. NU 5+ shows $X more in deposits, $Y more in spend. Even NU 1-4 shows improvement." |
| 30 | NU Conversion Pipeline | "X accounts started as NU 1-4 and later crossed to NU 5+ in subsequent waves. Persistence works." |
| 31 | **Activation Funnel** | "From X mailed non-users, Y activated their card, Z sustained spending, W are now active depositors." |

---

## BLOCK F: Demographics & Predictors (Cells 32-35)

**Talk track:** "Who should we target? What predicts success?"

| Cell | Title | Talk Track |
|------|-------|-----------|
| 32 | Response by Account Tenure | "X-year accounts respond at the highest rate." |
| 33 | Response by Member Age | "The [age range] demographic responds best." |
| 34 | Deposit Behavior by Age | "The deposit lift is [stronger/similar/weaker] for younger vs older members." |
| 35 | DD as Predictor | "Direct deposit members respond at Xx the rate. Target them first." |

---

## BLOCK G: Longitudinal & Risk (Cells 36-39)

**Talk track:** "Over time, across snapshots, and including accounts that left."

| Cell | Title | Talk Track |
|------|-------|-----------|
| 36 | Balance Trajectory | "Same accounts, 3 snapshots. Responders grew deposits X% while non-responders grew Y%." |
| 37 | Wave Persistence | "X% of wave responders responded again in subsequent waves." |
| 38 | Closed Accounts | "Accounts that closed had $X lower deposits -- deposit deceleration is a warning signal." |
| 39 | **Total Member Value** | "Deposits + spend + fees: a responder is worth $X/year. A non-responder in the same challenge is worth $Y." |

---

## BLOCK H: Executive Summary (Cells 40-45)

| Cell | Title | When to Use |
|------|-------|-------------|
| 40 | Exec Dashboard: Institutional | One slide for macro context |
| 41 | Exec Dashboard: Campaign Proof | One slide for same-challenge spend + deposit proof |
| 42 | Exec Dashboard: Activation | One slide for NU funnel + member value |
| 43 | Profile Table | Leave-behind: all metrics by challenge × outcome |
| 44 | Benchmark Findings | NCUA/FRED connected to account-level results |
| 45 | **Action Summary** | Strategic findings + recommended actions. Closes the section. |

---

## RECOMMENDED PRESENTATION FLOWS

**Full presentation (25-30 minutes):**
Cells 40, 12, 13, 15, 16, 17, 20, 21, 22, 23, 25, 29, 31, 32, 35, 36, 39, 41, 42, 45

**Same-challenge proof (15 minutes):**
Cells 40, 41, 16, 20, 25, 29, 31, 39, 42, 45

**Executive briefing (5 minutes):**
Cells 41, 42, 45

**NU activation story (10 minutes):**
Cells 15, 29, 30, 31, 19, 23, 42, 45
