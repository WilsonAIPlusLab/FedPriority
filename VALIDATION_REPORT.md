---
title: FOMC Scoring Dataset — Consolidated Validation Report
version: 1.0 (annotated 2026-10-16; patched for dataset v2.0.0 draft 2026-10-23)
date: 2026-03-30
---

# FOMC Scoring Dataset — Consolidated Validation Report

**Version:** 1.0 (original evidence as of 2026-03-30; annotated 2026-10-16 against 1.3.0 DRAFT; patched 2026-10-23 for the v2.0.0 DRAFT, local and unpublished)
**Date:** 2026-03-30

> **No human annotator has labelled any part of this dataset. Every reliability, concordance and agreement figure in this report is model-versus-model or an internal-consistency check; none is checked against human labels.** Sign convention throughout: **minutes minus transcripts** (a negative value means minutes score lower than transcripts).

> **Status for dataset v2.0.0 (draft, 2026-10-23). Read before using any number below.**
> 1. **The pilot sentence kappa of 0.751 could not be reproduced.** The closest recomputation from the shipped files is 0.686 (77.5% raw agreement, after merging FINANCIAL_CONDITIONS and FINANCIAL_STABILITY). It is not a passed check; see Section 7.2.
> 2. **Most of Sections 1-3 and 9 describe the original V4 staff run (482 documents; 486 rows after later patches), not `data/primary/staff_scores_v6.csv` (495 rows: 270 minutes + 225 transcripts).** In v6 the transcripts were re-scored on repaired text, and the CREDIT_SPREADS column is mixed-vintage. Results about the original run do not carry over automatically. Where this report recomputes on v6 (Section 3.2 and new Section 11), the numbers were recomputed directly from `data/primary/staff_scores_v6.csv` on 2026-10-23.
> 3. **Removed in v2.0.0 and no longer validated here:** the V3 discussion scoring (table, evidence, 64-file review, concordance), the mechanism coding and `analysis/`, `scoring_evidence/meeting_comparisons/`, `data/supplementary/`, `data/legacy/`, `correction_log.csv` and the `concordance_*.csv` files, and the reports `v3_validation_summary.md`, `concordance_report.md`, `deep_analysis_results.md`. Sections 2.4, 3.3, 3.4 and 4 are reduced to removal notices; other passages that cited them are marked.
> 4. Open failures kept at full prominence: cross-method A vs B for financial stability rho = 0.317 (threshold 0.50, fails); topic-model transcripts r = 0.48 (rule r > 0.7, fails); vintage drift (FINANCIAL_STABILITY_EMPHASIS -6.0, dissent -2.4, uncertainty -2.9 on 44 unchanged transcripts).

**Coverage (current v2.0.0 tables):** 495 staff documents (`staff_scores_v6.csv`: 270 minutes + 225 transcripts) and 542 discussion documents (`discussion_scores_v4_1.csv`: 270 minutes + 272 transcripts), 1993-2026
**Coverage of the original evidence in Sections 1-3 and 9:** 482 staff documents (266 minutes + 216 transcripts) of the original V4 run. The V3 discussion run (539 documents) is removed.
**Note (history):** the original V4 file later lost its duplicate 2012-10-24 minutes row and gained five 2026 minutes rows (486 rows), and was then replaced by `staff_scores_v6.csv` in v2.0.0 (`staff_scores_v4.csv` is no longer shipped; it differed from v6 in 84-139 of 486 shared rows per main dimension, CHANGELOG [2.0.0]). Statements below about "the shipped `staff_scores_v4.csv`" describe that earlier release and were not redone on v6 unless marked.
**Note (discussion):** `discussion_scores_v4_1.csv` follows the v2d patch (2000-12-19 HAWKISH_DOVISH_LEAN 42). V4.1 checks are in Section 10.

---

## Executive Summary

This report synthesizes all quality-control and validation evidence for the FOMC Scoring Dataset. The dataset provides machine-generated quantitative assessments of Federal Open Market Committee deliberations and public communications across seven dimensions of macroeconomic and financial conditions. Validation was conducted in eight procedures (several about components since removed, see the status box) spanning automated consistency checks, statistical independence tests, model-versus-model reproducibility, cross-method convergence, and an agent-based deep review (a second Claude model reviewing the first model's output). All procedures are model-versus-model or internal-consistency checks. The table below summarizes the outcome of each procedure.

| Validation Procedure | Scope | Key Metric | Result (model-vs-model) |
|---|---|---|---|
| Independence audit (V4 staff scoring) | 482 staff-scored files | 0 contamination phrases in reasoning text; lag-1 AC reduced | Pass (internal check) |
| Systematic error correction (staff V4) | 482 files, 15 dimensions | 564 corrections across 5 dimensions; 317 files corrected | Rule-based adjustment applied to the original run; `correction_log.csv` REMOVED in v2.0.0, so the corrections can no longer be audited from the release |
| Discussion score validation (V3 independent) | REMOVED in v2.0.0 (V3 table and evidence withdrawn) | Historical only: 0 direction errors in 628 checks; MAD 1.9 | Not a result for any shipped table |
| Model-model kappa (not human-validated) | 90-row annotation sample (30 excerpts x 3 persona annotations written in one Claude session, see 5.1) | 8/8 dimensions reported as κ ≥ 0.60 (values not shipped in this release; local copy 0.81 to 1.00) | Reported only; not re-derivable; independence of the three annotations not established |
| Staff score reproducibility (minutes vs. transcripts) | Original run: 171 pairs, 15 dims. Staff v6 (recomputed 2026-10-24): 215 same-date pairs, 2,166 numeric pairs | Original run: median r = 0.891 across Table 3.1 (0.888 excluding the two with N < 10). v6: core macro rows r 0.84-0.95, financial rows 0.56-0.83 (Section 11) | Agreement between two model scorings; lower on v6 than on the original run for the financial rows |
| Cross-method convergence (A vs B vs C) | 3 methods, 3 dimensions (computed 2026-03-12 from the original V4 staff scores and the February topic run; not recomputed) | Financial stability A vs B ρ = 0.317, **FAILS the 0.50 threshold set in advance**; A vs B also fails for inflation (0.312) and barely passes for employment (0.508); B vs C: ρ = 0.587–0.749 | PARTIAL (fails) |
| Sentence classification pilot kappa | 200-sentence pilot | Reported κ = 0.751 (Opus vs. Sonnet) **could not be reproduced; closest recomputation κ = 0.686**; FC/FS conditional κ = 0.416 | **NOT VERIFIED; do not cite as passed** |
| Topic model cross-method robustness | 7 corpora, 2 methods | r = 0.865 (minutes, N = 265), 0.78 (staff combined, rebuilt, N = 312), 0.48 (transcripts, N = 225; **fails the r > 0.7 rule**) after the 2026-10-07 re-run; the superseded February figures were 0.916, 0.861, 0.133, 0.016 and -0.442 | PARTIAL |

All procedures are model-versus-model or internal-consistency checks; none uses human labels. Cross-method convergence (Section 6) is partial (A-vs-B fails on two of three dimensions and passes narrowly, 0.508, on the third; the financial-stability pair is 0.317), and topic-model robustness (Section 8) holds for minutes and staff text but not for transcripts or conference calls. Section 10 summarises the V4.1 discussion checks.

---

## 1. Independence Audit (Staff V4 Scoring)

### 1.1 Background and Motivation

The original V3 staff scoring was produced by batched LLM agents that processed multiple meetings within a single context window. This architecture creates a risk of cross-meeting contamination: an agent scoring meeting $t$ may anchor its assessments to scores or language from meetings $t-1$ or $t-2$ that are still present in its context. The V4 scoring protocol addressed this by instantiating a fresh agent for each document — one meeting, one context, no shared state.

The independence audit examined whether the V4 protocol removed contamination, using four complementary tests. [Scope, 2026-10-23: this audit was run on the original V4 staff run (482 files). The v6 transcripts were re-scored on repaired text and the audit was not repeated for them.]

### 1.2 Contamination Phrase Scan

All 482 V4 staff-scored files were scanned for phrases indicative of cross-meeting agent memory — formulations such as "compared to the prior meeting," "higher than the previous session," or direct score references (e.g., "OUTPUT_GAP was 45 last time"). In 12 V4 files, phrases referencing other meetings were found in evidence blocks; these were source-document quotes — instances where the Fed's own staff materials referenced a prior projection — not agent opinions. Across all 482 files, **zero contamination phrases** were identified in LLM reasoning text, satisfying the primary test.

For comparison, the old V3 batched minutes agent contained cross-meeting references in reasoning text in 84 of 266 files (32%), and the transcript agent in 44 of 272 files (16%). The V4 protocol reduces this from a baseline of 16–32% to zero.

### 1.3 Lag-1 Autocorrelation Comparison

A secondary diagnostic tests whether batched agents produce artificially inflated serial correlation by anchoring each score to the prior document's scores. Under independence, observed autocorrelation should reflect genuine economic persistence, not scoring memory.

**Table 1.1. Lag-1 Autocorrelation in Financial Conditions (FC), Batched vs. Independent**

| Series | N | Lag-1 r |
|---|---|---|
| Old V3 batched — transcripts | 122 | 0.818 |
| V4 independent — transcripts | 175 | 0.690 |
| Old V3 batched — minutes | 193 | 0.872 |
| V4 independent — minutes | 265 | 0.821 |

The V4 independent series shows lower autocorrelation than the batched series in both document types, consistent with removal of an artificial anchoring component. Both series still show substantial positive autocorrelation because financial conditions genuinely persist across meetings; the diagnostic is the *relative* difference, not the absolute level.

[Unverified as of 2026-10-17: the V3 rows of Tables 1.1 and 1.2 come from `COMPARISON_SYNTHESIS.md` and the batched V3 files are not in the release. Recomputing lag-1 autocorrelation on the then-shipped `staff_scores_v4.csv` (now replaced by v6 and not recomputed on v6; sorted by date) gives FINANCIAL_CONDITIONS 0.812 for minutes (N = 269) and 0.758 for transcripts (N = 175), versus the 0.821 and 0.690 reported above for the original run; the minutes dimensions in Table 1.2 reproduce to within 0.01 (INFLATION_PRESSURE 0.927 vs 0.922, OUTPUT_GAP 0.947, LABOR_TIGHTNESS 0.958, CONSUMPTION_INVESTMENT 0.837). The transcript FC value differs by 0.07 because the shipped table includes later patches; the batched-versus-independent comparison itself cannot be re-run.]

For the five staff dimensions tabulated in Table 1.2, lag-1 autocorrelation is lower under V4 independent scoring (the other ten dimensions are not tabulated in this report). The largest reduction is in CONSUMPTION_INVESTMENT (AC1 from 0.944 to 0.842, Δ = −0.102), the dimension most sensitive to inter-meeting anchoring in the batched setting.

**Table 1.2. Lag-1 Autocorrelation Reduction, Staff Dimensions (Minutes)**

| Dimension | Old V3 AC1 | New V4 AC1 | Change |
|---|---|---|---|
| INFLATION_PRESSURE | 0.949 | 0.922 | −0.027 |
| OUTPUT_GAP | 0.977 | 0.947 | −0.030 |
| LABOR_TIGHTNESS | 0.977 | 0.959 | −0.018 |
| CONSUMPTION_INVESTMENT | 0.944 | 0.842 | −0.102 |
| FINANCIAL_CONDITIONS | 0.861 | 0.818 | −0.043 |

### 1.4 Runs Test

A Wald-Wolfowitz runs test provides a non-parametric check for whether the score series exhibit too few directional reversals (a signature of excessive smoothing from anchoring). Both old and new series show significantly fewer runs than expected under full independence (z-statistics between −6.55 and −10.46), reflecting genuine economic persistence rather than scoring artifacts. The V4 independent series consistently shows less extreme z-statistics than the batched counterparts (V4 transcripts: z = −6.55 vs. V3: z = −7.45; V4 minutes: z = −10.03 vs. V3: z = −10.46), indicating modestly improved statistical independence after controlling for genuine persistence.

### 1.5 Cross-Meeting Reference Classification

The independence audit found 26 cross-meeting references in V4 reasoning text and 8 in a comparison sample from the old batched series (see `validation/independence_audit_report.md`, Section 2), plus 12 (V4) and 10 (batched) in evidence blocks. The higher count in V4 does not indicate more contamination — independent review confirmed that all 26 V4 references are source-document quotations from Greenbook projections or Tealbook summaries that themselves reference prior meeting forecasts. These are legitimate evidentiary citations, not scoring contamination. The old batched series' lower count in this specific scan reflects a narrower audit sample; the broader file-level scan in Section 1.2 found contamination in 32% of old batched minutes files.

[Unverified as of 2026-10-17: the audit report tabulates the 26 V4 references under "reasoning text (potential contamination)", which sits uneasily with Section 1.2's statement of zero contamination phrases in reasoning text and with the claim above that all 26 are source quotations. The "independent review" is not documented in the audit report, and the V4 reasoning files are not in the release, so the reclassification cannot be re-checked.]

### 1.6 Conclusion

The contamination scan found no cross-meeting phrases in reasoning text, and lag-1 autocorrelation and runs-test statistics are reduced under V4 relative to batched scoring. They are not eliminated: V4 autocorrelations remain high and the runs tests still reject full independence (z = -6.5 to -10.5), which is consistent with genuine macroeconomic persistence but does not by itself separate persistence from residual anchoring. The evidence supports the claim that V4 reduced batching-induced dependence; it does not show it removed all of it.

---

## 2. Quality Flags and Systematic Error Corrections

### 2.1 Scope of V4 Staff Scoring

The V4 staff scoring as validated here covers 482 documents (266 minutes + 216 transcripts; the 1.3.0 file had 486 rows after five 2026 minutes were added; v2.0.0 ships v6 instead) with staff economic assessments, spanning 1993–2026, across 15 economic and financial dimensions. Each file was scored by a single-document Claude Opus 4.6 agent against a rubric anchored to 13 specific calibration points. A subsequent cumulative review pass (a second-model review against the rubric anchors, not validation against ground truth) by a separate Opus 4.6 agent assigned VALID, QUESTIONABLE, or INCORRECT verdicts to every scored *dimension* (not file), producing the quality distribution used in corrections. That review (`scoring_cumulative_validation_report.md`) was run against the V3 batched scoring pass and the V3 rubric, before the V4 independent rescoring existed; its own header marks it superseded in part. The distribution below therefore describes the V3 pass that was corrected, not a review of the V4 scores in the shipped file.

**Overall post-correction quality distribution (dimension-level verdicts):**

| Verdict | Count (dimension-checks) | Share |
|---|---|---|
| VALID | ~2,734 | ~73% |
| QUESTIONABLE | ~809 | ~22% |
| INCORRECT | ~183 | ~5% |

Source: `scoring_cumulative_validation_report.md` (04_scoring/staff/docs/). These counts represent individual dimension-checks across ~481 files × 15 dimensions (~7,215 potential checks, reduced by N/A entries). The tolerance thresholds are: ±5 points of rubric anchor = VALID, ±6–12 = QUESTIONABLE, >12 off or wrong direction = INCORRECT. All INCORRECT dimension-scores were adjusted by rule (Section 2.4; they were not re-scored) before inclusion in the then-canonical `staff_scores_v4.csv` (since replaced by v6, whose transcripts were re-scored).

Era-level quality shows a consistent improvement toward the most recent period: the 2024–2026 sub-period achieves 87.6% VALID and 0% INCORRECT, reflecting both improved documentation quality in recent Fed materials and a more refined scoring rubric developed iteratively over the full series.

### 2.2 Flag Categories in V4

After all corrections were applied, the V4 dataset retains 28 quality flags across 482 files (5.8% flag rate). Flag types and counts are as follows:

| Flag Type | Count | Description |
|---|---|---|
| [POLARITY?] | 20 | Score direction inconsistent with historical context (predominantly 2010–2012 BANKING_STRESS) |
| [ANCHOR] | 3 | Score outside era-appropriate calibration range |
| [CROSS] | 4 | Large within-meeting cross-dimension inconsistency (e.g., FC vs. CREDIT_SPREADS delta > 36) |
| [TREAS_OVER?] | 1 | TREASURY_STRESS elevated in non-crisis context (1998-09-29) |

The 20 POLARITY? flags are concentrated in 2010–2012, a period when banking stress was genuinely elevated relative to a "non-crisis" baseline but declining from the 2008–2009 peak. Scores in the 55–65 range during this period represent documented ongoing stress (impaired bank capital ratios, elevated loan loss provisions, continued FDIC-assisted bank failures through 2012), not scoring errors. Researchers should treat these as valid scores capturing post-crisis reversion rather than flag-warranted exclusions.

### 2.3 The Six Systematic Errors Identified and Corrected

The three-round correction process (February 27, 2026) identified six systematic scoring errors in the initial V3 production scores. [2026-10-23: the V3 scoring and the correction log were removed in v2.0.0; this subsection is retained as history of how the V4 table was built, and its counts can no longer be checked against a shipped file. The dimension names BANKING_HEALTH, DOLLAR_FX and FINANCIAL_TIGHTNESS belong to V3 and do not exist in the current tables.] Each error was diagnosed using cross-document comparison, evidence consistency cross-referencing, and historical calibration benchmarks.

**Error 1: TREASURY_STRESS Overstatement in Minutes**

Prevalence: ~65% of minutes files. The initial scorer applied the TREASURY_STRESS construct to any discussion of Treasury market conditions, including routine liquidity descriptions during non-stress periods. Corrected mean: 48.4 → 40.0 (−8.4 points). Correction mechanism: rule-based downward adjustment applied to 214 files where scored value exceeded documented liquidity events.

**Error 2: BANKING_HEALTH Polarity Confusion (renamed BANKING_STRESS)**

Prevalence: ~50% of minutes files. The dimension was originally labeled BANKING_HEALTH, creating ambiguity: a high score could indicate either strong banks or stressed banks. Approximately 50% of initial scores inverted the construct — high-stress periods were scored low and vice versa. Correction: dimension renamed BANKING_STRESS (high = more stress) with polarity standardized. 75 corrections applied. Post-correction, minutes and transcripts agree with r = 0.936 across 49 paired meetings.

**Error 3: DOLLAR_FX Polarity Inversion (renamed DOLLAR_STRENGTH)**

Prevalence: ~40% of files; classified as Critical severity. The original DOLLAR_FX dimension lacked an explicit polarity anchor. Approximately 40% of scores recorded dollar appreciation as a low value (treating weakness as the elevated condition) and 40% recorded it inversely. Correction: dimension renamed DOLLAR_STRENGTH (high = stronger dollar), polarity standardized, and 102 scale inversions corrected. The pre/post correlation between V3 and V4 for this dimension is r = 0.271, reflecting the severity of the original polarity inconsistency.

**Error 4: FINANCIAL_CONDITIONS Neutral Anchor Miscalibration (2017–2019)**

Prevalence: Moderate; most concentrated in the 2017–2019 sub-period but with residual effects in other eras. The rubric's neutral anchor (score = 50) was calibrated to the full-sample mean, causing financial conditions during tightening or easing cycles to be systematically mis-scored relative to their actual position. This error is documented but not fully corrected; scores during affected periods should be interpreted with additional caution. Two [ANCHOR] flags from the quality report (Section 9.1) illustrate the residual in other eras: `minutes_2022-06-15` (FINANCIAL_CONDITIONS = 43, expected range 55–68) and `transcript_1999-06-30` (FINANCIAL_CONDITIONS = 52, expected range 25–40).

**Error 5: LABOR_TIGHTNESS Underscoring**

Prevalence: ~60% of files; classified as Major severity. The initial scorer applied a conservative baseline that underweighted wage growth signals and employer difficulty indicators, resulting in systematically compressed scores. Direction was correct in all cases; the level was suppressed. Partial correction applied: mean shifted from 43.0 to 46.2 (+3.2 points). Level compression may persist as a residual bias, particularly in the 1997–2000 tight-labor-market period and the 2021–2023 post-pandemic period.

**Error 6: Retracted batched-scoring minutes-transcript gap (about +8 points)**

An earlier batched-scoring figure of about +8 points (minutes minus transcripts; reported in earlier versions of this report as +8.1 "across all dimensions" and elsewhere as a financial-conditions gap) is retracted as a measured baseline: it came from batched agents with cross-meeting dependence (Section 1) and its definition (all dimensions vs. financial conditions) was inconsistent across documents. In the original V4 run the FINANCIAL_CONDITIONS gap was **-1.7 points (minutes minus transcripts; 166 scored pairs, Table 3.1)**, i.e. transcripts score slightly higher (the earlier "+1.7" wording had the wrong sign). Recomputed on the earlier 486-row `staff_scores_v4.csv` (206 same-date pairs, 166 scored for this dimension) it was -1.5, and on the v6 table (215 same-date pairs, 213 scored; recomputed 2026-10-23) it is -0.9. The gap is small, rests on model scoring only, and has not been checked against human coding or separated from measurement differences between document types. The earlier statements that the residual was "confirmed as genuine editorial compression" and "robust" are withdrawn: no test that separates editorial compression from differences in what the scorer can see in minutes versus transcripts is shipped.

### 2.4 Correction Audit Trail (log removed in v2.0.0)

The original run logged 564 rule-based corrections (TREASURY_STRESS 214, LABOR_TIGHTNESS 144, DOLLAR_FX/DOLLAR_STRENGTH 102, BANKING_HEALTH/BANKING_STRESS 75, FINANCIAL_CONDITIONS 29; 317 of 482 files received at least one). `data/derived/correction_log.csv` was removed in v2.0.0 because it uses V3 dimension names that do not exist in the current tables, so these counts are historical and cannot be re-derived from the release. Whether the same corrections are reflected in the v6 table, whose transcripts were re-scored, was not checked.

---

## 3. Staff Score Reproducibility and Concordance

### 3.1 Minutes-Transcript Concordance Design

In the original run (not v6), 207 of 537 meetings had both minutes and transcripts available. After excluding 36 special-topic transcripts that are all-N/A for the standard economic dimensions (covering technical sessions on operating procedures, communication strategy, and similar non-assessment content), 171 meeting pairs were scorable on the full 15-dimension staff rubric (pairs where both documents were scored). Recomputed on the earlier 486-row staff table, 206 minutes/transcript pairs matched on meeting date. On the v6 table 215 same-date pairs match (2,231 numeric dimension pairs; Section 11). The pairing rule used for the original 171 is not documented in the shipped files. The V3 discussion concordance (187 pairs) is removed; the V4.1 discussion file has 224 pairs matched by transcript date and 215 matched on meeting date (Section 10).

Minutes represent the public-facing summary of the Committee's economic assessment — a staff-drafted, committee-approved communication to markets. Transcripts capture the actual deliberation in full: individual speaker assessments, tactical disagreements, and uncertainty hedges that the minutes condense into consensus language. Agreement between these two documents is expected to be high for objective economic conditions and moderate for deliberative dynamics.

All signed deltas use one convention throughout this report: minutes score − transcript score. Positive values indicate that minutes score higher; negative values that transcripts score higher.

### 3.2 Staff Scoring Concordance (V4, 15 Dimensions)

**Table 3.1. V4 Staff Score Concordance: Minutes vs. Transcripts (171 paired meetings in the original run; N per dimension below). Rows with N < 10 (INFLATION_SERVICES, INFLATION_HOUSING) are not interpretable.**

| Dimension | N | Pearson r | MAD | Bias (min−trans) |
|---|---|---|---|---|
| LABOR_TIGHTNESS | 165 | **0.977** | 2.2 | +0.3 |
| OUTPUT_GAP | 165 | **0.963** | 2.2 | +0.1 |
| INFLATION_PRESSURE | 164 | **0.926** | 3.2 | −0.6 |
| CONSUMPTION_INVESTMENT | 164 | **0.925** | 3.3 | +1.1 |
| BANKING_STRESS | 49 | **0.936** | 4.7 | −0.0 |
| CREDIT_SPREADS | 113 | **0.922** | 5.5 | −1.0 |
| FINANCIAL_CONDITIONS | 166 | 0.888 | 5.5 | −1.7 |
| INFLATION_EXPECTATIONS | 92 | 0.844 | 2.8 | +0.0 |
| INFLATION_GOODS | 78 | 0.843 | 6.1 | −2.1 |
| PRODUCTIVITY | 49 | 0.798 | 5.7 | −0.6 |
| TREASURY_STRESS | 63 | 0.797 | 4.9 | −0.6 |
| INFLATION_SERVICES | 9 | 0.891 | 4.3 | −0.6 |
| INFLATION_HOUSING | 8 | 0.977 | 3.4 | +1.6 |
| EQUITY_VALUATION | 114 | 0.733 | 7.3 | +3.8 |
| DOLLAR_STRENGTH | 133 | 0.715 | 7.2 | +1.6 |

Table 3.1 is the original-run output (`COMPARISON_SYNTHESIS.md`). Recomputed on the earlier `staff_scores_v4.csv` (206 same-date pairs, patched since; no longer shipped) the core rows agree to within 0.01 in r (LABOR_TIGHTNESS 0.975, OUTPUT_GAP 0.965, INFLATION_PRESSURE 0.927, CONSUMPTION_INVESTMENT 0.921, BANKING_STRESS 0.936), but several differ more: CREDIT_SPREADS r 0.917, MAD 5.8, bias -1.5 (after the CREDIT_SPREADS recheck); FINANCIAL_CONDITIONS 0.889, bias -1.5; EQUITY_VALUATION 0.741; DOLLAR_STRENGTH 0.711, bias +1.5; INFLATION_GOODS N = 77. On the v6 table (215 pairs, re-scored transcripts; recomputed again directly from `staff_scores_v6.csv` on 2026-10-23, and all values below reproduce) concordance is lower on the financial rows: FINANCIAL_CONDITIONS r 0.828 (N = 213), CREDIT_SPREADS 0.874 (187), EQUITY_VALUATION 0.631 (187), DOLLAR_STRENGTH 0.794 (194), INFLATION_PRESSURE 0.908 with bias -2.2, LABOR_TIGHTNESS 0.971. Agreement between the two document types therefore depends on the table version; the original-run Table 3.1 must not be quoted as a property of v6. The full v6 table is Section 11.

The four core macroeconomic dimensions — LABOR_TIGHTNESS, OUTPUT_GAP, INFLATION_PRESSURE, and CONSUMPTION_INVESTMENT — show exceptionally high concordance (r = 0.925–0.977) with near-zero bias. These are the most objectively anchored constructs in the rubric, drawing on numerical staff projections that appear in both document types. Financial market dimensions show somewhat lower concordance (r = 0.715–0.936; the upper end is BANKING_STRESS, N = 49), plausibly reflecting greater editorial discretion in how market conditions are presented in minutes relative to the more detailed treatment in transcripts.

### 3.3 and 3.4 Discussion concordance and era trends (V3; removed)

The V3 discussion concordance table (187 pairs, 10 dimensions) and the era-level gap trends were taken from `concordance_report.md`, which was removed in v2.0.0 together with the V3 discussion table. They are not reproduced. For the current discussion table see Section 10 and 10.1 (V4.1, 224 pairs). Era-level gap trends were not recomputed for V4.1 and none are claimed.

### 3.5 Interpretation

The pattern of concordance results is theoretically coherent and not alarming. Staff dimensions measuring objective economic conditions (OUTPUT_GAP r = 0.949-0.963; LABOR_TIGHTNESS r = 0.971-0.977; original run and v6) show very high agreement, plausibly because both documents reference the same numerical staff projections. The deliberative discussion dimensions (DISSENT_INTENSITY, FINANCIAL_STABILITY_EMPHASIS, UNCERTAINTY_EXPRESSED) have large minutes-minus-transcript gaps (Section 10.1), consistent with minutes compressing the deliberation, though the cause is not identified. This pattern is a measured difference between two model scorings of different texts; it is consistent with, but does not prove, an information gap between the public record and the internal deliberation. High agreement between minutes and transcripts shows that the scorer is consistent across document types, not that either score is accurate.

What would be alarming, and what is not observed: large biases in the economic direction dimensions (zero bias is expected; observed biases are −3 to +4 points in the original run and −4.9 to +3.0 in v6, the extremes being INFLATION_GOODS −4.9 and INFLATION_HOUSING +3.0 with N = 13), or sign reversals between minutes and transcripts on the same meeting. No sign reversals were reported in the core economic dimensions in the original analysis; no table of per-meeting sign checks is shipped, so this statement is not independently verifiable from the release.

---

## 4. Discussion Score Validation (V3; removed in v2.0.0)

This section reported a second-model review of the V3 discussion scoring (64 stratified files, 628 dimension-checks; 568 PASS, 46 MAGNITUDE_OFF, 14 EVIDENCE_MISSING, no direction errors) and a 16-file reproducibility spot-check (MAD 1.9 against a self-set target of 8). The V3 discussion table (`discussion_scores_v3.csv`), its evidence files and `v3_validation_summary.md` were removed in v2.0.0 as superseded, so these results describe no shipped table and are not reproduced. They are not evidence about V4.1. The V4.1 checks are in Section 10 (test-retest MAD 1.8 on 15 transcripts; 3.3 and 3.8 for minutes). Any text elsewhere that cites "0/628 direction errors" or "MAD = 1.9" refers to the removed V3 review.

---

## 5. Model-to-Model Reproducibility (no human annotators)

### 5.1 Procedure

Agreement across model annotators was evaluated using a 90-row annotation exercise. No human annotator participated; see §5.4. Thirty excerpts were drawn from FOMC documents spanning the full temporal range (1993–2026) and the full distribution of economic conditions, stratified to include examples from normal times, expansions, recessions, and crisis periods. Each excerpt was assessed by three annotator personas (monetarist, Keynesian, financial-stability; given fictional names such as "Dr. Sarah Chen") on eight dimensions. [Corrected 2026-10-17: earlier text called these three independent Claude Opus 4.6 agents with no shared memory. The shipped annotation file `opus_annotations_inline.csv` (90 rows, 30 per persona) and its writer script `write_inline_annotations.py` state that the scores were "derived from reading each excerpt as 3 annotator personas" in a single Claude session and typed into the script as a table; the repository also holds `generate_annotations_opus.py`, a persona-prompted API version, but its output is not in the `annotations/` folder. So the three sets are not shown to be independent runs, and the kappa below is persona-to-persona agreement inside one session.] Cohen's kappa was computed using linear weighting on the 0–100 scale, following the ordinal kappa procedure recommended by Shah et al. (2023) for continuous-scale annotation tasks.

### 5.2 Kappa Results

**Table 5.1. Linear-Weighted Cohen's Kappa by Dimension (n = 90 annotations per dimension). Per-dimension kappa values are not shipped in this release (the source file `human_kappa_summary.csv` is outside the release); only the threshold outcome is reported.**

| Dimension | κ (model-vs-model) | Landis-Koch Category (as reported) | Shah et al. (2023) Threshold | Pass (as reported) |
|---|---|---|---|---|
| LABOR_TIGHTNESS | values not shipped in this release (reported ≥ 0.60) | Substantial | 0.60 | Yes |
| OUTPUT_GAP | values not shipped in this release (reported ≥ 0.60) | Substantial | 0.60 | Yes |
| INFLATION_PRESSURE | values not shipped in this release (reported ≥ 0.60) | Substantial | 0.60 | Yes |
| CONSUMPTION_INVESTMENT | values not shipped in this release (reported ≥ 0.60) | Substantial | 0.60 | Yes |
| FINANCIAL_CONDITIONS | values not shipped in this release (reported ≥ 0.60) | Substantial | 0.60 | Yes |
| CREDIT_SPREADS | values not shipped in this release (reported ≥ 0.60) | Substantial | 0.60 | Yes |
| BANKING_HEALTH (renamed BANKING_STRESS) | values not shipped in this release (reported ≥ 0.60) | Substantial | 0.60 | Yes |
| DOLLAR_FX (renamed DOLLAR_STRENGTH) | values not shipped in this release (reported ≥ 0.60) | Substantial | 0.60 | Yes |

**Result (as reported in the original run, not re-derivable from the release): 8/8 dimensions meet κ ≥ 0.60 in model-versus-model agreement.**

[Checked 2026-10-17: a local copy of the summary exists at `04_scoring/staff/validation/analysis_output/human_kappa_summary.csv` (dated 2026-03-12; columns `human_human_kappa`, `krippendorff_alpha`; not part of the release). It lists κ between 0.806 (BANKING_HEALTH) and 1.000 (DOLLAR_FX), Krippendorff alpha 0.94 to 1.00, all rated PASS, with `llm_human_kappa` empty. I did not recompute them from the 90 annotations. Kappa this high between three personas written in one session mostly reflects shared reading of each excerpt, so it should not be read as independent reproducibility.]

### 5.3 Interpretation and Comparison to Published Norms (context only)

The Shah et al. (2023) threshold of κ ≥ 0.60 is the benchmark adopted for this exercise. For context only, human-human kappa on economic tone classification tasks typically falls in the 0.62–0.78 range (Apel and Blix Grimaldi 2014; Schmeling and Wagner 2019), with higher agreement on clearly directional assessments (expansion vs. contraction) and lower agreement on magnitude calibration.

Model-versus-model agreement at or above that level, as reported, indicates that the persona annotations of one model family agree with each other when given the rubric (see the correction in 5.1 about independence). BANKING_HEALTH (polarity sensitive) and DOLLAR_FX (direction sensitive), the most error-prone dimensions in pre-correction scoring, are reported to meet the threshold after the rubric revisions. Nothing here shows what human raters would have done, and no inference about human inter-rater disagreement can be drawn: there were no human raters.

### 5.4 Scope limitation: this is not human validation

The comparison in §5.3 is to human-human norms **reported in the published literature**,
not to human annotation of this corpus. The 90-row exercise in §5.1 used Claude annotations
written as three personas under the rubric; the sentence-classification pilot in §7
used Claude Opus 4.6 against Claude Sonnet 4.6. **No human annotator has labelled any
portion of this dataset.**

What these exercises do establish is meaningful but narrower than human validation: that
scoring is consistent across persona-prompted annotations and, in the sentence pilot and the
re-score checks of Sections 4.7 and 10, across separate model runs and a different model
family tier. The 90-row exercise cannot rule out single-session effects; the re-score checks
speak to single-run instability. It does not rule out a systematic bias shared by the
models applying the rubric, which only human adjudication could detect.

The instrument designed for that purpose — `06_cdfsg_pipeline/validation/compute_reliability.py`
(486 lines; designed for 2 independent human coders × 500 sentences, 3-way agreement with majority-vote
adjudication) — is written but has **never been run**; human coders were not recruited. Any
publication drawing on this dataset should describe its reliability evidence as
model-model reproducibility, not inter-rater agreement with human judgment.

---

## 6. Cross-Method Convergence

### 6.1 Design

The dataset was constructed using three independent measurement methods, each operationalizing economic conditions differently:

- **Method A (Rubric LLM Scoring):** A structured rubric assessing directional sentiment — whether inflation pressure, employment tightness, or financial conditions are elevated or suppressed relative to baseline. Source at the time: the original `staff_scores_v4.csv` (replaced by `staff_scores_v6.csv`; the comparison was not re-run on v6).
- **Method B (Sentence Classification Shares):** Supervised classification of individual sentences into topic categories; the meeting-level variable is the share of sentences assigned to each topic. Source: `data/sentence_classification/meeting_variables.csv`.
- **Method C (FASTopic Proportions):** A neural topic model (FASTopic) trained on FOMC text corpora; the meeting-level variable is the aggregate probability mass assigned to relevant topic clusters. Source: `data/topic_modeling/`.

Cross-method convergence was assessed using Spearman rank correlation (ρ), with the Gentzkow et al. (2019) threshold of ρ > 0.50 for each method pair.

### 6.2 Convergence Results

[Vintage note 2026-10-17: Table 6.1 reproduces from `cross_method_convergence_multidim.csv` (rounded; file dated 2026-03-12, N = 169-216 per cell). The file predates the October topic-model re-run (Section 8) and the staff patches, so Methods A and C are the earlier versions (the Method C inputs are not identified in the file; the topic-model transcript agreement itself changed from 0.133 to 0.480 in the re-run). The table has not been recomputed on the current tables.]

**Table 6.1. Cross-Method Spearman Rank Correlations**

| Dimension | A vs. B | A vs. C | B vs. C | Verdict |
|---|---|---|---|---|
| Financial | 0.317 (FAIL) | 0.540 (PASS) | 0.587 (PASS) | 2/3 PARTIAL |
| Inflation | 0.312 (FAIL) | 0.345 (FAIL) | 0.749 (PASS) | 1/3 PARTIAL |
| Employment/Output | 0.508 (PASS) | 0.357 (FAIL) | 0.683 (PASS) | 2/3 PARTIAL |

No dimension achieves full 3/3 convergence; all three dimensions achieve at least 1/3. B vs. C is the most reliable pair across all dimensions (ρ = 0.587–0.749), reflecting the fact that both methods are unsupervised prevalence measures that agree because they solve the same underlying problem (what fraction of text discusses a given topic).

### 6.3 Interpretation of A vs. B Failures

The A vs. B failures (ρ = 0.312 inflation, 0.317 financial stability; the employment pair passes narrowly at 0.508) are interpreted by the author as structural, not correctable; that interpretation is a hypothesis, not a test. The financial-stability A vs. B ρ = 0.317 fails the 0.50 threshold set in advance and remains the headline convergence failure. Method A measures *directional sentiment* — whether a condition is elevated or suppressed. Method B measures *topic prevalence* — what fraction of sentences discuss a topic. These are different constructs. A meeting can contain many sentences about inflation without signaling elevated inflation pressure (routine price-level monitoring in low-inflation environments). The two measures agree in extremes — crisis periods and high-inflation episodes — but diverge in normal times, which destroys rank correlation across the full sample. This is correctly interpreted as A and B measuring complementary aspects of Fed communication (stress direction vs. topic attention) rather than the same quantity.

### 6.4 Interpretation of Inflation A vs. C Failure

For the inflation dimension, A vs. C also fails (ρ = 0.345). Era subsample analysis confirmed this is not a zero lower bound artifact: the correlation fails in the pre-ZLB period (N = 117, ρ = 0.306), the ZLB period (N = 35, ρ = −0.007), and the post-ZLB period (N = 17, ρ = −0.009). The failure is structural. Method A averages five inflation sub-indices (goods, services, housing, expectations, and overall pressure) whereas Method C's FASTopic topics 2 and 3 capture generic inflation language — they cannot distinguish upward from downward pressure or disaggregate across sub-components. For inflation, the B vs. C pair (ρ = 0.749) is the appropriate convergence benchmark.

### 6.5 Implications for Dataset Use

The partial convergence pattern supports the following interpretive stance: Methods A and B are complementary rather than redundant measures of economic conditions in FOMC communications. Researchers using Method A (rubric scores) should treat it as a measure of assessed economic *severity*, while Method B sentence shares provide a measure of *attentional allocation*. The two measures will produce different results in regression analysis and should not be used interchangeably. Method B vs. C convergence (ρ = 0.587–0.749) is consistent with the two unsupervised methods capturing similar variation in the economic content of FOMC communications (a robustness comparison, not construct validation; the A-vs-B failures in Table 6.1 remain). The topic-to-dimension mapping is the investigator's own, not independent coding.

---

## 7. Sentence Classification Validation

### 7.1 Pilot Kappa Procedure

The sentence-level classification pipeline (CDFSG) was piloted on a seven-code scheme: FSS (Financial Stability/Systemic Risk), FCS (Financial Conditions/Markets), INF (Inflation), EMP (Employment), REG (Regulation/Supervision), OTH (Other), and DMS (Decision-Making/Structure). [Corrected 2026-10-17: the stored corpus does not use this scheme. `classified_sentences.csv` carries the five labels of classifier prompt V2 (FINANCIAL 95,556; INFLATION 59,925; EMPLOYMENT_OUTPUT 114,471; REGULATION_SUPERVISION 3,135; OTHER 226,988) plus `stability_intensity`; the seven codes are conceptual (see `codebooks/CODEBOOK_sentence_classification.md`). The shipped pilot labels `pi_labels_200.csv` use six labels, with FINANCIAL_CONDITIONS and FINANCIAL_STABILITY separate and no DMS.] Validation was conducted via a pilot inter-rater reliability test using 200 sentences stratified by Peek Financial Index match status, comparing a gold-standard annotator (Claude Opus 4.6, PI) against a bulk-scoring annotator (Claude Sonnet 4.6) on the same 200-sentence sample.

### 7.2 Pilot Results

**Reported overall kappa: 0.751** (81.0% raw agreement). **This figure could not be reproduced and must not be cited as a passed check; the closest recomputation from the shipped files is κ = 0.686 (77.5% raw agreement), see the note below.** As reported it would be "Substantial" on the Landis-Koch scale (0.61–0.80) for a 200-sentence model-versus-model pilot (Claude Opus 4.6 vs. Claude Sonnet 4.6), above a κ = 0.70 rule of thumb but below the κ ≥ 0.80 design target (Section 7.5); the recomputed 0.686 is below the 0.70 rule of thumb. The pilot does not validate the 500,075-sentence corpus, which has no human check and was labelled with the V2 prompt, not the scheme piloted here. [Unverified (re-stated for v2.0.0 on 2026-10-23 from the 2026-10-17 check; I did not re-run the recomputation): the 0.751 and 81.0% cannot be re-derived from the release. The Sonnet 4.6 labels are not shipped; `pilot_classified_inline.csv` holds V2-style labels for the same 200 sentences (annotator not identified, reasoning field "inline-annotation"), and after merging FINANCIAL_CONDITIONS and FINANCIAL_STABILITY into FINANCIAL its agreement with `pi_labels_200.csv` is 77.5% raw, κ = 0.686 (my recomputation; without the merge κ = 0.416). The pilot is therefore best read as a single un-reproduced figure with a best recomputation of 0.686.]

The most challenging distinction is between FINANCIAL_CONDITIONS (FC) and FINANCIAL_STABILITY (FS). The conditional kappa for the FC/FS distinction — computed only on sentences where at least one annotator selected either FC or FS — is **κ = 0.416** ("Moderate"), substantially lower than the overall kappa. This pattern is expected: FC and FS are related constructs (both concern financial system functioning) that are distinguished by their referent (aggregate monetary conditions vs. systemic risk), and FOMC text frequently discusses both in the same sentence or paragraph.

### 7.3 V2 Taxonomy Response

The FC/FS distinction weakness motivated the development of a V2 taxonomy that merges the two categories into a single FINANCIAL category with a 1–5 intensity scale distinguishing routine conditions monitoring from systemic stability concerns. The V2 prompt (`rubrics/sentence_classification_prompt_v2.txt`) was subsequently used to label the whole corpus (500,075 sentences, five labels plus a 1-5 `stability_intensity`). No reliability pilot of the V2 labels against a second annotator is shipped; the closest item is the inline-label comparison in 7.2, whose provenance is unclear. The merge removes the FC/FS boundary but moves the same difficulty into the `stability_intensity` score, for which no agreement figure exists.

### 7.4 Dictionary Benchmark

As an additional external validity check, three established financial text lexicons were applied to a 70,610-sentence subset (44,490 transcript, 4,063 minutes and 187 statement sentences from the 17 meetings between June 2007 and June 2009 (statements cover 15 of them), plus 21,870 sentences from speeches on 119 dates in the same window; see `data/sentence_classification/all_sentences_scored.csv`; the CHANGELOG's 70,635 is a miscount) and compared against LLM classification rates: Peek Financial Index (FI) matched 4.9% of sentences, Correa Federal Reserve Stability Scores (FSS) matched 32.4%, and Loughran-McDonald (LM) matched 50.5% (recomputed from the file: 4.87%, 32.41%, 50.47%). The file holds only dictionary counts, no LLM topic, and its `sentence_id` does not match the current corpus (join on `join_key`), so no LLM match rate can be read from it. These are match rates only, with no ground truth: the LLM classifier matches fewer sentences than the LM dictionary, which is consistent with the dictionary overmatching on general financial vocabulary, but match rates do not establish better discrimination.

### 7.5 Known Limitations

**Label provenance (new in v2.0.0).** `classified_sentences.csv` now carries `label_source`: 7,979 rows (transcript 5,118; speech 2,448; minutes 413) are `keyword_script`, meaning their labels match a keyword script rather than an LLM judgement; the other 492,096 are `llm_presumed`, i.e. no keyword-script evidence was found, which is not a verification of an LLM label. No agreement check was run on either group, and `meeting_variables.csv` was not recomputed, so the effect of the keyword-labelled rows on CDFSG is not estimated. Counts are from the CHANGELOG and README; I did not recount the file in this pass.

The full validation suite (`compute_reliability.py`, 486 lines) is designed but not yet executed. It requires two independent human coders to label a 500-sentence sample, enabling 3-way agreement analysis (Human 1 × Human 2 × LLM) with majority-vote adjudication and disagreement pattern analysis. The reported pilot kappa (κ = 0.751, not reproduced; 0.686 on recomputation) falls below the design target of κ ≥ 0.80 ("Almost Perfect"). Reliability evidence exists only for the pilot of the seven-code scheme against a second model, which is not the scheme in the stored corpus (V2 prompt, five labels); there is no human validation. Researchers should exercise particular caution with the FC/FS distinction (conditional κ = 0.416).

---

## 8. Topic Model Cross-Method Robustness

### 8.1 Design

Two independent neural topic models — FASTopic and BERTopic — were trained on the same seven FOMC document corpora (minutes, transcripts staff section, transcripts discussion section, statements, press conferences, testimonies, speeches). Each model independently discovers topic clusters from the text. Where the two models recover similar topic structures, the discovered topics are less likely to be artifacts of a particular algorithm.

### 8.2 Results

Cross-method correlation between FASTopic and BERTopic topic proportions was computed for each corpus. After the 2026-10-07 re-run (fixed PDF reader, duplicate 2012-10-24 minutes removed, rebuilt staff corpus) the minutes corpus agrees at r = 0.865 (Spearman 0.879, N = 265), the staff-combined corpus at r = 0.782 (N = 312) and full transcripts at r = 0.480 (Spearman 0.470, N = 225) (`data/topic_modeling/cross_method_matrix.csv`). The February results (minutes 0.916 on a corpus with a duplicate meeting, staff 0.861, transcripts 0.133, decomposed transcripts 0.016, conference calls -0.442, decomposed minutes 0.716, staff paragraphs 0.597) are superseded and kept in `data/topic_modeling/_superseded_2026-02-09/`; the cleaned run did not recompute decomposed transcripts, conference calls, decomposed minutes or staff paragraphs.

Source: `05_topic_modeling/07_compare_methods.py`; documented in `docs/pipeline.md`, `docs/qc_audit.md`, and `docs/lessons_learned.md`.

### 8.3 Interpretation

The high cross-method correlation on minutes (r = 0.865) and staff text (0.78) indicates that topic proportions for those corpora are not very sensitive to the choice of algorithm. For full transcripts (0.48) agreement is only moderate, and the February run found far lower agreement for decomposed transcripts and conference calls; Method C results on transcripts should not be treated as robust to model choice.

[Added 2026-10-17. The figures match `cross_method_matrix.csv` (Pearson 0.865 / 0.480 / 0.782, Spearman 0.879 / 0.470 / 0.768, N 265 / 225 / 312); the explanations below come from `05_topic_modeling/SUMMARY.md` (its verification section) and were not re-derived here. The transcripts result is partly explained: the BERTopic ratio is dominated by one catch-all cluster (53% of non-noise sentences, mapped to Treasury/Bond Markets) and dropping it raises r from 0.480 to 0.742 per that summary; why the cluster forms is not determined. The change from 0.133 to 0.480 is attributed there to BERTopic re-clustering, not to the PDF reader, because the transcript sentence text did not change. The earlier explanation of the February numbers by a "naive PDF reader" holds for minutes only. A re-run of the decomposed-transcript corpus on the rebuilt text (364,600 sentences) is in progress and does not appear in `SUMMARY.md`; no decomposed-transcript topic figure should be quoted yet. The success rule r > 0.7 fails for transcripts.] The Section 6 comparisons of Method C with Methods A and B are therefore better supported for minutes-based variables than for transcript-based ones.

---

## 9. Known Limitations and Remaining Flags

### 9.1 Post-Correction Flag Inventory

After all three correction rounds and the V4 independent rescoring, 28 quality flags remain across 482 staff-scored files (5.8%). The full list is archived in `validation/quality_report.md`. Researchers should apply the following guidance by flag type:

- **[POLARITY?] flags (20 files):** All are concentrated in 2010–2012 BANKING_STRESS. These scores are defensible as capturing genuine post-crisis stress reversion; they are not scoring errors. However, comparisons of BANKING_STRESS between 2009 (crisis peak) and 2010–2012 (post-crisis) may require analyst judgment about the appropriate baseline.
- **[ANCHOR] flags (3 files):** `minutes_2015-12-16` (CREDIT_SPREADS = 58, expected 30–42; 55 after the 2026-10-17 level-reading recheck, still outside the range), `minutes_2022-06-15` (FINANCIAL_CONDITIONS = 43, expected 55–68), and `transcript_1999-06-30` (FINANCIAL_CONDITIONS = 52, expected 25–40). These three meetings should be treated with caution; the scores are outside the era-appropriate calibration range and have not been corrected.
- **[CROSS] flags (4 files):** Three 2024–2025 minutes (2024-07-31, 2024-09-18, 2025-01-29) where FINANCIAL_CONDITIONS and CREDIT_SPREADS diverge by 36 to 40 points (all three values unchanged in the current tables), and one 2003 transcript (2003-10-28, OUTPUT_GAP 35 vs CONSUMPTION_INVESTMENT 68, delta 33) [corrected 2026-10-17 from "four 2024–2025 meetings" using `quality_report.md`]. For the 2024–2025 cases the divergence likely reflects the post-2022 environment in which aggregate financial conditions tightened while corporate credit spreads remained compressed. Users modeling this period should note the construct divergence.
- **[TREAS_OVER?] flag (1 file):** `transcript_1998-09-29` has TREASURY_STRESS = 63 in a period not characterized by broad Treasury market stress. This may reflect the LTCM/Russian default episode. Users of the September 1998 observation should verify against source text. (TREASURY_STRESS is 63 in the earlier V4 table and 57 in the v6 table, which re-scored transcripts; the v6 value was read from `staff_scores_v6.csv` on 2026-10-23.) The flag counts in 9.1 describe the original run's `quality_report.md`; they were not regenerated for v6.

### 9.2 Pre-2005 Minutes Scoring Confidence

Of the 270 minutes in the current decomposition (`03_decomposition/output_rebuild/minutes`), 128 are saved as `unsegmented_body.txt` rather than segmented sections: exactly 8 per year from 1993 to 2008 (96 of them before 2005, 32 in 2005–2008) [corrected 2026-10-17 from "127 from the pre-2005 period"; counted from the folder listing]. These are the HTML-era minutes that did not undergo the segmentation pipeline. The scorer encounters mixed staff/participant content in these files without clear section markers, reducing scoring precision. Confidence ratings for these files are lower: in the earlier `staff_scores_v4.csv`, 17.2% of their `_CONF` values were Low versus 4.7% for the other minutes (recomputed then; not redone on v6). Researchers using the 1993–2008 minutes sample should note this limitation. (Whether the staff scorer read this folder's text or a separately prepared input is not established here.)

### 9.3 Labor Tightness Residual Compression

Despite correction from a mean of 43.0 to 46.2, LABOR_TIGHTNESS may retain a level compression bias in approximately 40–60% of files. The *direction* of the scores was judged correct in the original second-model review of the (now removed) V3 discussion scoring; that result does not cover the staff table or V4.1. The *level* of scores may be systematically low by 2–4 points, particularly in the 1997–2000 tight labor market period and the 2021–2023 pandemic labor shortage period. This residual bias does not affect rank-order analysis but may affect level comparisons across eras.

### 9.4 Financial Conditions Anchor Drift (2017–2019)

The 2017–2019 FINANCIAL_CONDITIONS period has a documented calibration issue. The neutral anchor (50) was calibrated to the full-sample mean, and the 2017–2019 tightening cycle — which followed an unusually prolonged period of accommodative conditions — was underscored relative to its actual position in the historical distribution. This is documented but not fully corrected. Regression analyses covering this period should include a 2017–2019 era dummy or treat FINANCIAL_CONDITIONS with additional caution.

### 9.5 Interactively Produced Scores and Reproducibility

The 482 staff-scored files of the original run and the 539 removed V3 discussion files (original counts; see the notes at the top) were produced in individual LLM sessions. These sessions are not computationally reproducible in the strict sense: re-running the scoring pipeline on the same source text with the same rubric will produce scores that differ from the archived values, not identical values. The removed V3 spot-check gave MAD = 1.9 (16 files); V4.1 measurements are larger and depend on scoring vintage: 1.8 on 15 transcripts (blind re-score), 3.3 for fresh vs. patched minutes (60 documents), 3.8 for the blind second pass of minutes, and a vintage drift of several points on three discussion dimensions (Section 10). The correction log is no longer shipped (Section 2.4), so the staff correction chain cannot be fully audited from the release. Researchers who require bit-exact reproducibility should use the archived scored files rather than attempting to re-score from raw text.

### 9.6 Yields and Futures Alignment (External Validity Checks)

Two external validity tests were conducted as supplementary checks rather than primary validation. A yield curve event study (following Lucca and Trebbi 2009) found correct sign alignment in 10 of 14 tested policy directions using daily FRED Treasury yield data (2-year, 5-year, 10-year). Only 4 of the 14 dimension-maturity pairs have both the correct sign and p < 0.05, and the analysis script's own verdict is "FAIL: score changes do not reliably predict yields" (`event_study_yield_report.txt`, 2026-03-12). The daily close-to-close data are a plausible reason for weak p-values (intraday ±30 minute data from WRDS tick sources were not available), but that explanation was not tested. 10 of 14 correct signs is better than the 7 expected by chance only modestly (a binomial test of 10 of 14 at p = 0.5 gives about 0.09 one-sided; not tested for dependence across maturities), so it is weak support.

The rate-alignment output (`rate_alignment_results.csv`, 2026-03-12) regresses scores on same-meeting and next-meeting rate changes in basis points. The hawkishness composite gives Spearman 0.20 (same meeting, N = 265) and 0.14 (next meeting), the change in hawkishness 0.33, and the financial-stress score -0.39 (all flagged FAIL by the script's pass rule). The earlier statement that the shortfall is "attributable to ZLB contamination" and that pre-ZLB subsamples "are expected to pass" is untested: no pre-ZLB subsample result is shipped. [Unverified as of 2026-10-17: whether this output is the Fed Funds futures test described earlier; it uses realized rate changes.]

---

## 10. V4.1 Discussion Scoring Checks (added 2026-10-16)

These checks cover `data/primary/discussion_scores_v4_1.csv` (542 rows in 1.3.0: 270 minutes + 272 transcripts). All are model-versus-model; no human annotator has labelled any part of it. Transcript rows are fresh scores (one fresh agent per meeting); minutes rows are 265 patches of earlier V4 analyses plus 5 fresh 2026 rows, not fresh scores. Numbers are from CHANGELOG.md [1.2.0]/[1.3.0] and README.md (not independently re-run in the 2026-10-23 pass, except where marked recomputed); where recomputed from `data/derived`, the result is noted.

| Check | Scope | Result |
|---|---|---|
| Blind second pass of patched minutes | 381 cells (`discussion_v4_1_second_pass_check.csv`) | Mean absolute difference 3.8 points (recomputed 3.82 on the 328 cells scored in both); the CHANGELOG puts the share of checked cells that would not be scored blind at 9% (recomputed share of second-pass N/A is 12.6% of 381); 36 minutes cells were set to N/A (24 EQUITY_VALUATION, 9 CREDIT_SPREADS, 3 others) and logged |
| Fresh vs. patched minutes | 60 random minutes documents, 1,200 cells (`discussion_v4_1_minutes_fresh_sample.csv`) | Mean absolute difference 3.3 points; 4% of cells differ on scored vs. N/A (recomputed 3.37 and 5.7%). The CHANGELOG says the headline gaps are not weakened; the per-gap differences are not reproduced here |
| Transcript re-score diff | 71 transcripts re-scored under the V4.1.1 clarifications; 1,340 meeting-dimension cells in the diff file (67 meeting dates) | Mean absolute change 2.1 points on cells with both values (recomputed); EQUITY_VALUATION in the 201 transcripts scored before V4.1.1 may run about 2 points high relative to the clarified rule |
| Test-retest | 15 transcripts, blind re-score | Mean absolute difference 1.8 points; FINANCIAL_STABILITY_EMPHASIS noisiest at 3.1; sample mostly 1994-2008 |
| 2026-10 vintage control | 45 distinct unchanged transcripts re-scored on 2026-10-16/17 (the pooled summary uses 44, omitting 2004-11-10; the effect is negligible) | FINANCIAL_STABILITY_EMPHASIS 6.0 lower (se 1.0), DISSENT_INTENSITY 2.4 lower, UNCERTAINTY_EXPRESSED 2.9 lower, HAWKISH_DOVISH_LEAN 1.4 lower; economic and market dimensions moved by less than 1 point |

### 10.1 Matched-pair gaps (V4.1)

On 224 matched minutes/transcript pairs (minutes minus transcripts; recomputed 2026-10-24 from `discussion_v4_1_minutes_vs_transcripts.csv` after the 128 minutes of 1993-2008 were re-scored fresh on a discussion-only input): DISSENT_INTENSITY -10.8, UNCERTAINTY_EXPRESSED -7.2 (before: -8.3, -5.0; the 96 pairs from 2009 on are unchanged: -8.4, -9.2). On the 215 pairs matched on meeting date the gaps are -10.7 and -7.2 (recomputed 2026-10-24 from the primary table). The widening comes from the pre-2009 pairs (dissent -8.3 to -12.6, uncertainty -1.9 to -5.7) and is probably a scoring-vintage effect (Section 10.2), not new evidence. An earlier V3 scoring gave similar signs and sizes, but the V3 table is removed, its figures were recorded inconsistently, and it came from the same model family, so it is not quoted as a confirmation. The V4.1 gaps have not been checked against human coding, and the cause (editorial compression vs. differences in what the scorer sees in each document type) is not identified. The 224 pairs come from the derived file's `transcript_date` match (224 distinct meeting dates); matching on meeting date gives 215.

### 10.2 Vintage caveat

Scoring vintage matters: on 28 same-day pairs the gaps were stable across vintages (dissent -8.4 to -9.7, uncertainty -3.8 to -4.0), but levels of dissent, financial-stability emphasis and uncertainty are not comparable between the 2026 rows and older rows. The same applies to the 128 minutes of 1993-2008 re-scored on 2026-10-24: against the transcripts they sit lower by -4.3 (dissent) and -3.8 (uncertainty) than the patched minutes they replaced, about the size and direction of the -2.4 and -2.9 drift measured on unchanged text, so the gap widening in 10.1 cannot be separated from vintage.

### 10.3 Limits

All scorers are LLM agents of one model family. Minutes cells the patch left UNCHANGED partly rest on the earlier analysis. 12 transcripts were scored on Opus, and the models of the minutes-patch agents were not tracked per document. Re-scored transcripts omit Part 1 reasoning in their evidence files. The noise figures above (1.8, 3.3, 3.8) measure different things (transcript test-retest, fresh vs. patched minutes, blind second pass) and should not be interchanged.

### 10.4 Staff 2026 rows

The five fresh 2026 staff minutes rows (SCORE_VERSION `v4_new2026_minutes` in v6) are not covered by any QC procedure in Sections 1-9. Their CREDIT_SPREADS values were rechecked under the level reading on 2026-10-17 and all five were unchanged; nothing else was checked. They were scored under the V4 rubric text that contained the CREDIT_SPREADS contradiction (resolved in the v4.1 staff rubric, decisions in `04_scoring/RUBRIC_DECISIONS_2026-10-17.md`). Existing staff scores were not all re-scored for that decision: 79 cells (74 minutes rows and 5 transcript rows; count from `docs/IMPROVEMENTS_2026-10-16.md`, not recounted) were updated after the level-reading recheck, and staff-versus-discussion CREDIT_SPREADS differences should still be treated with caution.

---

## 11. Staff v6: what was recomputed and what was not (added 2026-10-23)

**Not carried over automatically.** The validation in Sections 1, 2 and 9 (independence audit, VALID/QUESTIONABLE/INCORRECT review, rule-based corrections, quality flags) was run on the original V4 staff run (482 documents). `staff_scores_v6.csv` re-scored the transcripts on repaired text and carries mixed `SCORE_VERSION` values (v4_prior 197; v4_patched_2026-10 186; v4_prior+credit_v4_1 75; v4_patched_2026-10+credit_recheck 28; v4_new2026_minutes 5; v4_patched_2026-10+credit_v4_1 4). None of those checks was repeated for v6, and no QC procedure other than the one below was run on it. v6 CREDIT_SPREADS remains mixed-vintage.

**Minutes versus transcripts on v6, recomputed from `data/derived/staff_v6_minutes_vs_transcripts.csv` on 2026-10-24** (215 same-date pairs; Pearson r, mean absolute difference, mean minutes minus transcripts; numeric pairs only; 2,166 numeric pairs). The 128 pre-2009 minutes rows were replaced on 2026-10-24 by blind scores on a staff-only input (DATA_PROVENANCE 5.5); the table of 2026-10-23 (2,231 pairs, pre-2009 minutes scored on the whole minutes body) is superseded, for example INFLATION_PRESSURE r 0.908 then and 0.843 now, CREDIT_SPREADS 0.874 and 0.748, FINANCIAL_CONDITIONS bias -0.9 and +1.6. Model-versus-model; high agreement shows consistency across document types, not accuracy.

| Dimension | N | Pearson r | MAD | Bias (min-trans) |
|---|---|---|---|---|
| LABOR_TIGHTNESS | 214 | 0.954 | 3.4 | -0.7 |
| OUTPUT_GAP | 215 | 0.943 | 2.9 | -0.3 |
| CONSUMPTION_INVESTMENT | 214 | 0.920 | 3.8 | +1.9 |
| INFLATION_HOUSING (N small) | 11 | 0.904 | 5.2 | +0.5 |
| INFLATION_SERVICES (N small) | 10 | 0.899 | 3.8 | -0.6 |
| INFLATION_PRESSURE | 214 | 0.843 | 4.8 | -2.2 |
| BANKING_STRESS | 86 | 0.830 | 7.2 | +1.7 |
| FINANCIAL_CONDITIONS | 213 | 0.789 | 7.1 | +1.6 |
| PRODUCTIVITY | 39 | 0.779 | 6.1 | 0.0 |
| INFLATION_GOODS | 103 | 0.774 | 7.3 | -2.8 |
| DOLLAR_STRENGTH | 194 | 0.771 | 6.9 | +0.6 |
| CREDIT_SPREADS (mixed vintage) | 173 | 0.748 | 8.9 | +2.4 |
| INFLATION_EXPECTATIONS | 132 | 0.703 | 3.3 | +0.2 |
| EQUITY_VALUATION | 188 | 0.569 | 7.6 | +3.4 |
| TREASURY_STRESS | 160 | 0.558 | 6.3 | +1.3 |

Reading: the core macro rows are comparable to the original run, with INFLATION_PRESSURE lower (0.843); the financial rows are lower than in Table 3.1 (for example TREASURY_STRESS 0.558 against 0.797, EQUITY_VALUATION 0.569 against 0.733), and BANKING_STRESS now has N = 86 against 49. Split by period, R2 is pre-2009 / 2009+: LABOR_TIGHTNESS 0.83 / 0.96, OUTPUT_GAP 0.81 / 0.94, INFLATION_PRESSURE 0.56 / 0.83, FINANCIAL_CONDITIONS 0.69 / 0.56, CREDIT_SPREADS 0.49 / 0.74, EQUITY_VALUATION 0.20 / 0.70, TREASURY_STRESS 0.36 / 0.34 (2009+ unchanged by the re-score). The change cannot be attributed to the re-scoring alone, because the pair set also grew from 171 to 215. The ANOMALY_FLAG and ANOMALY_NOTE columns have no numeric pairs. The minutes-minus-transcript differences are not separated into editorial compression and differences in what the scorer can see.

**Not verified in this pass:** the per-dimension figures were not compared row by row with `data/derived/staff_v6_minutes_vs_transcripts.csv` (only its 215 / 2,166 counts match); autocorrelation, runs tests and the contamination scan were not re-run on v6; the staff evidence files cover the original minutes scores, not the v6 transcripts (README, Known limits).

---

## Appendix: Validation File Inventory

| File | Location | Content |
|---|---|---|
| `qc_audit.md` | `docs/` (not shipped in this release) | Master QC catalog, 22 items |
| `v3_validation_summary.md` | REMOVED in v2.0.0 | V3 discussion score validation, 64 files |
| `independence_audit_report.md` | `dataset/validation/` | V4 contamination scan and autocorrelation tests (original run, not v6) |
| `quality_report.md` | `dataset/validation/` | 28 remaining flags, V4 post-correction (original run) |
| `staff_comparison_report.md` | `dataset/validation/` | 15-dimension minutes-transcript concordance (original V4 table, not v6) |
| `concordance_report.md` | REMOVED in v2.0.0 | V3 10-dimension discussion concordance with era trends |
| `COMPARISON_SYNTHESIS.md` | `dataset/validation/` | Batched vs. independent scoring systematic comparison (original run) |
| `EVIDENCE_SUMMARY.md`, `README.md` | `dataset/validation/` | Evidence summary; README stating which reports describe earlier tables |
| `staff_v6_minutes_vs_transcripts.csv` | `dataset/data/derived/` | v6 minutes-minus-transcript differences (215 pairs, 2,166 numeric pairs) |
| `correction_log.csv` | REMOVED in v2.0.0 | 564-entry per-correction audit trail (V3 dimension names) |
| `scoring_cumulative_validation_report.md` | `04_scoring/staff/docs/` | VALID/QUESTIONABLE/INCORRECT verdicts |
| `scoring_correction_documentation.md` | `04_scoring/staff/docs/` | Three-round correction methodology |
| `human_kappa_summary.csv` (despite its name, a model-versus-model summary; no human raters) | `04_scoring/staff/validation/analysis_output/` (not shipped in this release) | 8-dimension kappa results |
| `cross_method_convergence_multidim.csv` | `04_scoring/staff/validation/analysis_output/` | A/B/C Spearman correlations |
| `pi_labels_200.csv` | `dataset/validation/pilot_kappa/` | 200 labels from a PI-prompted Claude Opus run (not human labels); the reported kappa 0.751 was not reproduced (0.686) |

---

*Sections 1-9 cover evidence as of 2026-03-30; Section 10 and the annotations marked 1.3.0 were added 2026-10-16; the passages marked 2026-10-17 are a verification pass against the files (backup `VALIDATION_REPORT.md.bak_2026-10-17_phase8`). The v2.0.0 patch of 2026-10-23 (backup `VALIDATION_REPORT.md.bak_2026-10-23_v2`) marked removed components, flagged the unreproduced pilot kappa, scoped original-run results, and added Section 11 (v6 concordance recomputed from the data). The planned human-coder validation for sentence classification (500-sentence sample) has not been run; until it is, all reliability evidence in this report is model-versus-model.*
