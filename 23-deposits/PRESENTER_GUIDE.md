# Section 23: Deposit Relationship & ARS Impact -- Presenter Guide

46 cells. You do NOT need to present all of them. The executive dashboards (cells 42-46) summarize each block. Use the individual cells when you want to drill deeper on a specific point.

---

## BLOCK A: Data Pipelines (Cells 01-04)

**Run these first. Do not present them.** They load data and build all the DataFrames that downstream cells use. No charts.

| Cell | What it does | Notes |
|------|-------------|-------|
| **01** | Loads 3 zaccounts snapshot files (Nov24, Jun25, Dec25). Filters to open accounts only. Joins to ODDD via HASHED_ACCOUNT. Builds matched cohort (accounts in all 3 snapshots). | Configure filenames in SNAPSHOT_CONFIG |
| **02** | Classifies every account's response history across all mailer waves. Builds the response tier ladder, direction, first/repeat responder flags. | Must run after section 09 (ARS campaign) |
| **03** | Computes monthly spend/swipes per response group. Builds per-wave pre/post spend deltas. Aligns 12-month spend windows to each deposit snapshot. | Must run after cell 02 |
| **04** | Downloads NCUA 5300 Call Report data for 5 quarters. Pulls FRED economic data (FL unemployment, Fed Funds, CPI). Builds peer group. | Requires internet access. Uses FRED API key. |

---

## BLOCK B: Setting the Stage -- Institutional Context (Cells 05-10)

**Talk track:** "Before we look at individual accounts, let's understand where the credit union sits. This is the macro context that our deposit analysis lives within."

| Cell | Title | Talk Track | When to Use |
|------|-------|-----------|-------------|
| **05** | **Total Deposits Over Time** | "Here's USF FCU's total deposit base from the NCUA call reports -- [X quarters]. The orange line is the median for similar-sized Florida credit unions. We're [above/below] peers." | Always. Sets the baseline. |
| **06** | **Membership Growth** | "Member count is [growing/flat/declining] at [X]% per quarter. The question is: is our deposit growth coming from new members walking in the door, or are existing members depositing more? If deposits are growing faster than membership, it's deepening -- and that's where the campaign story gets interesting." | Use when deposit growth > member growth |
| **07** | **Fee Income Trend** | "This is fee income from the call report -- OD/NSF fees. We'll come back to this when we look at per-account fee data. The institutional number tells us the total; the account data tells us who's paying it." | Optional. Use if fee story is strong. |
| **08** | **Net Worth Ratio** | "Capital adequacy. We're well-capitalized at [X]%, comfortably above the 7% threshold. This means the deposit base is supporting healthy capital levels." | Optional. Use for board/executive audience. |
| **09** | **FRED Macro Context** | "The economic backdrop. Florida unemployment was [X] when we took our first snapshot and [X] when we took our last. The vertical lines mark our snapshot dates. This matters because if deposits are declining, we need to know: is it the economy or is it our members?" | Use when economic conditions changed between snapshots |
| **10** | **Peer Comparison** | "Quarter over quarter, here's our deposit growth rate side by side with the FL peer median. We're [outperforming/underperforming] by [X] percentage points. Now let's find out what's driving that." | Always. The bridge to the campaign analysis. |

**Executive Dashboard: Cell 42** -- All 4 key institutional metrics on one slide. Use this if you only have 1 slide for context.

---

## BLOCK C: The ARS Campaign Landscape (Cells 11-17)

**Talk track:** "Now let's look at the ARS campaign itself. Who are we mailing, how are they responding, and is it getting better over time?"

| Cell | Title | Talk Track | When to Use |
|------|-------|-----------|-------------|
| **11** | **Response Tier Distribution** | "This is every account's best response tier ever achieved. The ladder runs from Never Mailed at the bottom to TH-25 at the top. [X]% of mailed accounts have responded at some level. [X] accounts are stuck at NU 1-4 -- that's our conversion opportunity." | Always. The foundational chart. |
| **12** | **Response Rate by Wave** | "Wave over wave, here's the success rate -- green is NU 5+ and Threshold combined. The amber line is NU 1-4, the 'almost there' group. The trend is [improving/stable/declining]. The dashed line is TH-only -- our most engaged cardholders." | Always. Shows campaign momentum. |
| **13** | **Wave Tier Composition** | "Same data, different view. For each wave, this is the full breakdown of everyone we mailed. You can see how the response mix shifts -- are we getting more Threshold responders in recent waves? Is the No Response segment shrinking?" | Use when the mix is shifting meaningfully |
| **14** | **Time to First Response** | "Of everyone who eventually responded, how many waves did it take? [X]% responded on their first mailing. But [X]% took 3+ waves. The red line is average deposit balance -- notice that accounts who respond quickly tend to have [higher/lower] deposits. Patience with the non-responders pays off." | Use to justify continued mailing |
| **15** | **Response Consistency** | "Not all responders are equal. [X] accounts respond 80%+ of the time they're mailed -- these are your consistent responders. [X] responded just once. Look at the deposit balances -- consistent responders carry [X] more in deposits." | Use to segment future targeting |
| **16** | **Best vs Latest Tier Retention** | "Of accounts that reached each tier, how many are still there? [X]% of TH-25 accounts are holding. But only [X]% of NU 5+ accounts are maintaining that level. This tells us which tiers are sticky and which need reinforcement." | Use when retention varies by tier |
| **17** | **Tier Retention Overall** | "Zooming out: of all responders, [X]% are holding their best tier, [X]% have slipped. The ones holding have [higher/lower] deposits -- maintaining response tier correlates with deposit health." | Always. Clean headline number. |

**Executive Dashboard: Cell 43** -- Campaign performance on one slide: group distribution, response rate trend, repeat vs one-time, direction.

---

## BLOCK D: Deposit Profile by Response Group (Cells 18-23)

**Talk track:** "Now the core question: do ARS responders have better deposit relationships? Let's look at the data."

| Cell | Title | Talk Track | When to Use |
|------|-------|-----------|-------------|
| **18** | **Deposit KPI Cards** | "Six headline numbers for the deposit portfolio: [total accounts], [total deposits], [direct deposit rate], [median days between deposits], [repayment rate], [avg annual deposits]. These are all open accounts from the latest snapshot." | Always. Opens the deposit block. |
| **19** | **Balance by Response Group** | "This is the headline chart. Average balance by response group. Threshold responders carry a mean of [X] (median [X]). Never Mailed accounts carry [X]. That's a [X]% gap. The median tells you the typical member, not just the average pulled up by a few large accounts." | Always. The money chart. |
| **20** | **Direct Deposit Rate** | "Direct deposit is the stickiest relationship signal. [X]% of Threshold responders have direct deposit set up vs [X]% of non-responders. A [X] percentage point gap. Members with direct deposit are already depositing regularly -- they're your most engaged." | Always. Strong signal. |
| **21** | **Deposit Frequency** | "How often do they deposit? Threshold responders: median [X] days between deposits. Non-responders: [X] days. Lower is better -- more frequent depositors are more engaged with the institution." | Use when the frequency gap is meaningful |
| **22** | **Profile Summary Table** | "Here's the full picture in one table -- mean and median for every deposit metric, by response group. Hand this to your analyst team." | Use as a leave-behind or appendix |
| **23** | **Tier Deposit Heatmap** | "This is the full 8-tier view -- not collapsed to 5 groups. Green = healthier, red = weaker. Read across a row to see one tier's deposit profile. Read down a column to see how a metric changes as you go up the ladder. The pattern should be clear: higher tiers, healthier deposits." | Use for data-oriented audiences |

**Executive Dashboard: Cell 44** -- Balance, direct deposit, trajectory, and growth on one slide.

---

## BLOCK E: Longitudinal Proof -- Same Accounts Over Time (Cells 24-30)

**Talk track:** "Cross-sectional data shows a correlation. But does the campaign actually *cause* deposit growth? To answer that, we tracked the same accounts across all three snapshots."

| Cell | Title | Talk Track | When to Use |
|------|-------|-----------|-------------|
| **24** | **Balance Trajectory** | "Same accounts, three snapshots. Solid line is the mean, dashed is the median. Threshold responders went from [X] to [X] -- that's [X]% growth. Non-responders went from [X] to [X]. The gap is widening. This is the matched cohort -- these are the exact same people." | Always. The proof chart. |
| **25** | **Deposit Amount Trajectory** | "Same view, but for annual deposit volume -- how much money flowed in over the trailing 12 months at each snapshot. Responders are depositing [more/less] over time." | Use when deposit volume tells a different story than balance |
| **26** | **Deposit Count Trajectory** | "And frequency -- how many deposits in the trailing 12 months. Are responders depositing more often? This answers: is it bigger deposits or more deposits driving the growth?" | Use to distinguish amount vs frequency |
| **27** | **Deposit Growth Rate** | "Per-account growth rates. Not group averages -- we computed the % change for each individual account, then took the mean and median of those growth rates. Repeat responders: mean [X]%, median [X]%. Never responded: [X]%. The median is the story of the typical member." | Always. Individual-level proof. |
| **28** | **First-Time vs Repeat** | "Accounts that responded once vs multiple times. Repeat responders carry [X] more in deposits. Sustained engagement with the campaign deepens the deposit relationship." | Use when repeat premium is significant |
| **29** | **NU 1-4 vs NU 5+** | "The conversion story. Accounts that peaked at NU 1-4 vs those that crossed to NU 5+. Over time, the NU 5+ accounts [grew/maintained] deposits while NU 1-4 [declined/stagnated]. Crossing that 5-swipe threshold matters for the deposit relationship too." | Always. The conversion proof. |
| **30** | **Ladder Direction Balance** | "Accounts that improved on the response ladder vs stayed flat vs declined. Improvers carry [X] in deposits. Decliners carry [X]. Moving up the ladder correlates with stronger deposits." | Use when direction differences are significant |

---

## BLOCK F: Spend + Deposits Unified (Cells 31-35)

**Talk track:** "We have 36 months of card spend data and 3 deposit snapshots. Let's put them on the same timeline."

| Cell | Title | Talk Track | When to Use |
|------|-------|-----------|-------------|
| **31** | **Monthly Spend Timeline** | "Every month's average card spend, by response group. The dotted vertical lines are mailer waves. The red dashed lines are our deposit snapshot dates. You can see spend [lifting/dipping] after mailers, and you can see where our deposit data anchors." | Always. The unified view. |
| **32** | **Wave Spend Pre/Post** | "For each mailer wave: did spend go up? This is the 3-month average before vs after. Above zero means spend lifted. Responders consistently [lift/don't lift] more than non-responders." | Use when pre/post lift varies by wave |
| **33** | **Card Activation Rate** | "What percentage of each group has any card spend at all each month? This is the activation question. If the campaign is working, we should see the activation rate climbing for NU and Threshold groups -- dormant cards waking up." | Always. Critical for NU segments. |
| **34** | **Spend-Deposit Aligned** | "Now the alignment. At each snapshot, the solid line is deposit balance and the dashed line is the 12-month card spend matched to that same window. When both go up, the member is becoming more valuable across the board. When they diverge, something interesting is happening." | Always. The correlation proof. |
| **35** | **Spend vs Deposit Growth** | "The punchline. Side by side: % growth in deposits vs % growth in card spend, by response group. Are they moving together? For Threshold responders: deposits grew [X]% and spend grew [X]%. For non-responders: deposits [X]%, spend [X]%. The campaign is [lifting both / lifting spend but not deposits / etc.]." | Always. The executive takeaway. |

**Executive Dashboard: Cell 45** -- Monthly spend, activation, alignment, and growth on one slide.

---

## BLOCK G: OD/Fee Impact (Cells 36-39)

**Talk track:** "Beyond deposits and spend, there's a third dimension of member value: overdraft and fee behavior."

| Cell | Title | Talk Track | When to Use |
|------|-------|-----------|-------------|
| **36** | **Collected Fees by Group** | "Average annual fees collected per account. Responders pay [more/less] in OD/NSF fees than non-responders. Mean [X], median [X]. This is fee revenue the credit union is generating -- or not." | Use when fee income story matters |
| **37** | **Fee Pressure Ratio** | "Fees as a percentage of deposits. This is the health metric -- a high ratio means the member is paying a lot of fees relative to what they're depositing. Lower is healthier. Responders: [X]%. Non-responders: [X]%." | Use to show deposit health holistically |
| **38** | **Repayment Rate** | "When a member overdrafts, how quickly do they repay? Higher is better. Responders: [X]%. Non-responders: [X]%. Faster repayment means less risk and more depositor reliability." | Use when repayment varies significantly |
| **39** | **FDIC Occasions** | "How many times did the account go negative in the past 12 months? Lower is better. Responders average [X] occasions. Non-responders: [X]. Fewer OD events means a more stable deposit base." | Use when OD frequency varies |

**Executive Dashboard: Cell 46** -- All 4 OD/fee metrics on one slide.

---

## BLOCK H: Conclusion (Cells 40-41)

| Cell | Title | Talk Track | When to Use |
|------|-------|-----------|-------------|
| **40** | **Benchmark Summary** | "This table connects the institutional NCUA data and economic context back to the ARS campaign. Column 3 tells you how each external finding relates to what we found at the account level." | Always. Ties the bow. |
| **41** | **Action Summary** | "Six findings with priority levels, and six recommended actions. This is the strategic takeaway for the credit union." | Always. Closes the section. |

---

## EXECUTIVE DASHBOARDS (Cells 42-46)

If you need to present the entire section in 5 slides:

| Cell | Dashboard | One-Line Summary |
|------|-----------|-----------------|
| **42** | Institutional Context | Total deposits, members, net worth, FL unemployment |
| **43** | Campaign Performance | Response groups, rate trend, repeat vs one-time, direction |
| **44** | Deposit Value | Balance by group, DD rate, trajectory, growth % |
| **45** | Spend + Deposits | Monthly spend, activation, aligned dual-axis, growth comparison |
| **46** | OD/Fee Impact | Fees, fee ratio, repayment, FDIC occasions |

Follow with cell 41 (Action Summary) for the strategic close.

---

## RECOMMENDED PRESENTATION FLOWS

**Full presentation (20-25 minutes):**
Cells 42, 11, 12, 18, 19, 20, 24, 27, 29, 31, 34, 35, 44, 46, 41

**Medium presentation (10-15 minutes):**
Cells 42, 43, 44, 45, 46, 41

**Executive briefing (5 minutes):**
Cells 44, 45, 41
