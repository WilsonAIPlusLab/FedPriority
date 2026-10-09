---
title: "FOMC Participant Discussion Scores, V4.1 (discussion_scores_v4_1.csv)"
version: 1.2.0
source_file: data/primary/discussion_scores_v4_1.csv
rubric_file: rubrics/discussion_scoring_rubric_v4_1.md (+ rubrics/discussion_scoring_clarifications_v4_1_1.md)
---

## Overview

Meeting-level scores of what FOMC participants said, from the minutes (participants' views and the vote record) and the transcripts (all member and participant turns, staff turns removed, roll call appended). One row is one meeting document, keyed by `MEETING_DATE` and `SOURCE_TYPE`. The file has 272 transcript rows and 265 minutes rows.

**Read this before using the minutes rows.** Transcript rows are fresh scores. Minutes rows are a *patch* of the earlier V4 minutes analyses, made one fresh LLM agent per meeting against the rebuilt input and a text diff; they are not independent fresh scores. The earlier analyses often cited evidence that appears in neither the old nor the new input, so many old cells were corrected (see `data/derived/discussion_v4_1_minutes_patch_log.csv`). After a blind second pass, 36 patched cells that the second pass scored N/A were set to N/A (`NA_DECISION_CELLS`, `data/derived/discussion_v4_1_na_decision_log.csv`).

## Variables

| Variable | Description |
|---|---|
| MEETING_DATE | ISO date. Meeting start date for minutes. Transcripts carry the date of the transcript file, which for some two-day meetings is the end date; match minutes to transcripts within one day (`data/derived/discussion_v4_1_minutes_vs_transcripts.csv` does this). |
| SOURCE_TYPE | `minutes` or `transcript`. (Working files use `discussion_m` / `discussion`.) |
| `<DIM>`, `<DIM>_UNC`, `<DIM>_CONF` | Score 1 to 100 (50 neutral, never 0) or `N/A`; uncertainty band written `+-N`; confidence `High`, `Moderate` or `Low`. When the score is `N/A`, so are `_UNC` and `_CONF`. The four inflation sub-components carry a score only. |
| METHOD | `fresh_score` (transcripts) or `patch_of_v4_analysis` (minutes). |
| RUBRIC_VERSION | `v4.1.1` where the row was re-scored with the V4.1.1 clarifications (71 transcripts), else `v4.1`. Minutes rows are `v4.1`; the second pass used v4.1.1 but did not replace patched values except as described above. |
| INPUT_VERSION | `member_discussion_v2`, or `member_discussion_v2b` (First Vice Presidents and acting presidents added; transcripts only). |
| MODEL_EXCEPTION | `opus` for the 12 transcripts scored on Opus instead of the default Sonnet agent. Minutes-patch agents' models were not tracked per document. |
| NA_DECISION_CELLS | Semicolon list of dimensions in this minutes row set to N/A by the 2026-10-07 decision. |
| CREDIT_UPDATE | `v411_blind_check_2026-10-08` on the 16 transcript rows whose CREDIT_SPREADS, `_UNC` and `_CONF` were replaced after a blind re-check under the V4.1.1 clarifications (first run: `N/A`); blank elsewhere. The other dimensions of those rows keep their first-run values. See `data/derived/discussion_v4_1_credit_update_log.csv`. |
| ANOMALY_FLAG, ANOMALY_NOTE | Agent's own flag and note. `Yes` on most transcript rows (framework sessions, missing staff answers, empty turns), so it does not discriminate. |

## Dimensions (from the rubric)

| No. | Dimension | Scale | Tier | Lowest anchor | Highest anchor |
|---|---|---|---|---|---|
| 1 | INFLATION_PRESSURE | 1-100 | Tier 1 | 1-10: Deflationary spiral underway; "falling price level"; "deflation risk is acute" | 91-100: Extreme/unprecedented inflation; wage-price spiral; unanchored expectations |
| 2 | OUTPUT_GAP | 1-100 | Tier 1 | 1-15: Catastrophic contraction; GDP collapsing; "worst since Depression" | 86-100: Extreme overheating; historically unprecedented demand-supply imbalance |
| 3 | LABOR_TIGHTNESS | 1-100 | Tier 1 | 1-15: Depression-level unemployment; massive layoffs; "hemorrhaging jobs" | 81-100: Historically unprecedented tightness |
| 4 | CONSUMPTION_INVESTMENT | 1-100 | Tier 1 | 1-15: Collapsing; "freefall"; spending/investment halted | 81-100: Extreme; historically unprecedented spending surge |
| 5 | PRODUCTIVITY | 1-100 or N/A | Tier 1 | 1-20: Deteriorating productivity; shrinking potential output | 81-100: Exceptional/unprecedented gains |
| 6 | FINANCIAL_CONDITIONS | 1-100 | Tier 1 | 1-15: Extremely loose; "excessive liquidity"; "bubble conditions"; "easy credit" | 81-100: Extremely tight/crisis; "credit frozen"; "systemic stress"; "panic" |
| 7 | TREASURY_STRESS | 1-100 or N/A | Tier 1 | 1-20: Exceptionally smooth functioning; low volatility; "well-functioning" | 91-100: Complete market breakdown |
| 8 | CREDIT_SPREADS | 1-100 | Tier 1 | 1-15: Extremely compressed; underpriced risk; "historically narrow"; "risk-on" | 81-100: Severely wide; credit rationing; lending freeze; "markets seized" |
| 9 | EQUITY_VALUATION | 1-100 or N/A | Tier 1 | 1-15: Extreme overvaluation concern; "bubble"; "irrational exuberance"; "frothy" | 81-100: Extreme undervaluation; fire-sale prices; panic selling |
| 10 | BANKING_STRESS | 1-100 or N/A | Tier 1 | 1-15: Excessive risk-taking/leverage (different problem, but low-stress direction) | 81-100: Severe systemic stress; multiple failures; "crisis"; solvency concerns |
| 11 | DOLLAR_STRENGTH | 1-100 or N/A | Tier 1 | 1-15: Extreme weakness; "sharply depreciating"; "dollar under pressure" | 81-100: Extreme strength; "DXY at multi-decade highs"; "severe headwind" |
| D1 | HAWKISH_DOVISH_LEAN | 1-100 | Tier 3 (discussion) | 1-10: Emergency dovish: immediate large-scale easing, QE launch, "do whatever it takes" | 91-100: Emergency hawkish: near-unanimous calls for most aggressive tightening possible |
| D2 | DISSENT_INTENSITY | 1-100 | Tier 3 (discussion) | 1-15: Near-consensus: unanimous vote, all express similar views | 91-100: Near-irreconcilable: 3+ dissents, sharp personal exchanges |
| D3 | FINANCIAL_STABILITY_EMPHASIS | 1-100 | Tier 3 (discussion) | 1-5: No mention of financial stability or financial conditions | 95-100: Overwhelming concern; financial stability IS the meeting |
| D4 | FORWARD_GUIDANCE_TONE | 1-100 | Tier 3 (discussion) | 1-5: Strongest easing commitment: threshold-based or date-based guidance promising near-zero rates (e.g., Evans Rule, "at least through 2015") | 91-100: Strong tightening commitment: explicit aggressive further tightening |
| D5 | UNCERTAINTY_EXPRESSED | 1-100 | Tier 3 (discussion) | 1-15: High confidence: strong conviction, narrow forecast ranges, clear signals | 91-100: Extreme/Knightian: distribution of outcomes itself unknown; "cannot bound the range" |
| S1 | INFLATION_GOODS | 1-100 or N/A | Tier 2 (inflation sub-component) |  |  |
| S2 | INFLATION_SERVICES | 1-100 or N/A | Tier 2 (inflation sub-component) |  |  |
| S3 | INFLATION_HOUSING | 1-100 or N/A | Tier 2 (inflation sub-component) |  |  |
| S4 | INFLATION_EXPECTATIONS | 1-100 or N/A | Tier 2 (inflation sub-component) |  |  |

## Conventions and limits

- Special-topic documents (no policy vote and no stance discussion: framework, repo-facility, swap-line or briefing-only calls) carry `N/A` for HAWKISH_DOVISH_LEAN and DISSENT_INTENSITY; 20 transcripts are in that state and 19 of them have no minutes document. Borderline calls: 1993-11-09, 1994-03-24, 1994-12-30, 1995-01-13, 2008-07-24, 2009-01-16, 2010-10-15, 2011-11-28.
- CREDIT_SPREADS: most scores, especially in the minutes, rest on credit-availability wording only (Low confidence, wide band), as the V4.1.1 clarifications allow when no spread wording exists. Of the 201 transcripts scored before the clarifications, 27 had CREDIT_SPREADS `N/A`; a blind re-check (the same procedure as the 60-transcript sample that sized the rule difference: EQUITY_VALUATION and CREDIT_SPREADS agreed within a mean absolute difference of 3.0 and 2.3 points where both were scored) scored 16 of them, all Low confidence (values 33 to 57, uncertainty +-10 or +-12), and kept 11 at `N/A`. Every kept `N/A` is a short call (4,600 words or fewer); every newly scored one is 6,574 words or longer. These 16 cells are marked in `CREDIT_UPDATE`. The check agents saw the clarifications and the first-run agents did not; both are the same model family. Transcript CREDIT_SPREADS scores that already existed (174 of the 201) were not changed.
- EQUITY_VALUATION: a wealth-effect mention alone is `N/A`; a price move alone is scored 45 to 55 with Low confidence.
- All scorers are LLM agents of one model family. There is no human coding and no inter-coder agreement. Agreement between passes shows repeatability, not accuracy.
- Scorer noise (test-retest, 2026-10-08): 15 transcripts already scored under V4.1.1 were re-scored by fresh agents on the same input, rubric and instructions, blind to the earlier score. Across 223 scored pairs the mean absolute difference was 1.8 points (standard deviation of the difference 2.5; 95.5% within 5 points; none above 10). By dimension the mean absolute difference ranges from 0.6 (INFLATION_EXPECTATIONS) to 3.1 (FINANCIAL_STABILITY_EMPHASIS, where 67% of pairs were within 5 points); HAWKISH_DOVISH_LEAN 1.5, UNCERTAINTY_EXPRESSED 1.6, FORWARD_GUIDANCE_TONE 2.2, DISSENT_INTENSITY 2.3. Whether a cell was scored or `N/A` changed in 6 of 300 cells, all in rarely mentioned dimensions (TREASURY_STRESS, BANKING_STRESS, INFLATION_SERVICES); INFLATION_HOUSING and INFLATION_SERVICES have few pairs and low correlations (0.70 and 0.86). The sample is small and mostly 1994 to 2008 (13 of 15), with no document above 30,000 words, so noise on later and longer meetings is not measured. This is repeatability within one model family, not accuracy. The retest outputs are not part of this release.
- Rule effect on EQUITY_VALUATION: in the 60-transcript blind check of the first-run transcripts, EQUITY_VALUATION under the V4.1.1 clarifications ran about 1.7 points lower than the first run (mean absolute difference 3.0 against retest noise of 1.1), which suggests a small systematic effect of about 2 points on the 201 transcripts scored before the clarifications. It was not corrected.
- The re-scored transcripts omit the rubric's Part 1 reasoning (the API safeguard stopped many runs that wrote it); their evidence files hold Parts 2 and 3. The first-run transcript evidence files include Part 1.
- Minutes-minus-transcript gaps on 224 matched pairs: HAWKISH_DOVISH_LEAN -1.5 (sd 4.12, n=224); DISSENT_INTENSITY -8.3 (sd 6.89, n=224); FINANCIAL_STABILITY_EMPHASIS -13.3 (sd 9.61, n=224); FORWARD_GUIDANCE_TONE -2.5 (sd 5.85, n=224); UNCERTAINTY_EXPRESSED -5.0 (sd 8.91, n=224).
