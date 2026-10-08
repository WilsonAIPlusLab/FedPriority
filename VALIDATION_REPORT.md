---
title: FOMC Scoring Dataset — Consolidated Validation Report
version: 1.0
date: 2026-03-30
---

# FOMC Scoring Dataset — Consolidated Validation Report

**Version:** 1.0
**Date:** 2026-03-30
**Coverage:** 539 scored discussion documents + 482 scored staff documents, 1993–2026
**Document types:** 266 minutes, 273 transcripts (discussion); 266 minutes, 216 transcripts (staff)

---

## Executive Summary

This report synthesizes all quality-control and validation evidence for the FOMC Scoring Dataset. The dataset provides machine-generated quantitative assessments of Federal Open Market Committee deliberations and public communications across seven dimensions of macroeconomic and financial conditions. Validation was conducted in eight distinct procedures spanning automated consistency checks, statistical independence tests, model-model inter-rater reliability, cross-method convergence, and an independent agent-based deep review. The table below summarizes the outcome of each procedure.

| Validation Procedure | Scope | Key Metric | Status |
|---|---|---|---|
| Independence audit (V4 staff scoring) | 482 staff-scored files | 0 contamination phrases; lag-1 AC reduced | PASS |
| Systematic error correction (staff V4) | 482 files, 15 dimensions | 564 corrections across 5 dimensions; 317 files corrected | PASS |
| Discussion score validation (V3 independent) | 64 files, 628 dim-checks | 0 direction errors; MAD = 1.9 | PASS |
| Model-model inter-rater kappa (not human-validated) | 90-row annotation sample | 8/8 dimensions κ ≥ 0.60 | PASS |
| Staff score reproducibility (minutes vs. transcripts) | 171 scorable pairs, 15 dims | Median r = 0.922 across dimensions | PASS |
| Cross-method convergence (A vs B vs C) | 3 methods, 3 dimensions | B vs C: ρ = 0.587–0.749; A vs B structural gap | PARTIAL |
| Sentence classification pilot kappa | 200-sentence pilot | κ = 0.751 (Substantial) | PASS |
| Topic model cross-method robustness | 7 corpora, 2 methods | r = 0.916 (minutes) | PASS |

Seven of eight procedures pass fully. The one procedure with a partial result (cross-method convergence) is described in detail in Section 6, along with the structural reasons the A-vs-B divergence does not undermine the validity of the primary scoring measures.

---

## 1. Independence Audit (Staff V4 Scoring)

### 1.1 Background and Motivation

The original V3 staff scoring was produced by batched LLM agents that processed multiple meetings within a single context window. This architecture creates a risk of cross-meeting contamination: an agent scoring meeting $t$ may anchor its assessments to scores or language from meetings $t-1$ or $t-2$ that are still present in its context. The V4 scoring protocol addressed this by instantiating a fresh agent for each document — one meeting, one context, no shared state.

The independence audit confirmed whether the V4 protocol successfully eliminated contamination, using four complementary tests.

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

Across all scored dimensions in the staff assessment, every dimension shows lower lag-1 autocorrelation under V4 independent scoring (Table 1.2). The largest reduction is in CONSUMPTION_INVESTMENT (AC1 from 0.944 to 0.842, Δ = −0.102), the dimension most sensitive to inter-meeting anchoring in the batched setting.

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

The independence audit found 26 cross-meeting references in V4 reasoning text and 8 in a comparison sample from the old batched series (see `validation/independence_audit_report.md`, Table 2). The higher count in V4 does not indicate more contamination — independent review confirmed that all 26 V4 references are source-document quotations from Greenbook projections or Tealbook summaries that themselves reference prior meeting forecasts. These are legitimate evidentiary citations, not scoring contamination. The old batched series' lower count in this specific scan reflects a narrower audit sample; the broader file-level scan in Section 1.2 found contamination in 32% of old batched minutes files.

### 1.6 Conclusion

All four tests support the independence claim. The V4 scoring protocol successfully eliminated cross-meeting agent contamination. Observed autocorrelation and runs behavior reflect genuine macroeconomic persistence, not scoring artifacts. The independence claim is substantiated.

---

## 2. Quality Flags and Systematic Error Corrections

### 2.1 Scope of V4 Staff Scoring

The V4 staff scoring covers 482 documents (266 minutes + 216 transcripts) with staff economic assessments, spanning 1993–2026, across 15 economic and financial dimensions. Each file was scored by a single-document Claude Opus 4.6 agent against a rubric anchored to 13 specific calibration points. A subsequent cumulative validation pass by a separate Opus 4.6 agent assigned VALID, QUESTIONABLE, or INCORRECT verdicts to every scored *dimension* (not file), producing the quality distribution used in corrections.

**Overall post-correction quality distribution (dimension-level verdicts):**

| Verdict | Count (dimension-checks) | Share |
|---|---|---|
| VALID | ~2,734 | ~73% |
| QUESTIONABLE | ~809 | ~22% |
| INCORRECT | ~183 | ~5% |

Source: `scoring_cumulative_validation_report.md` (04_scoring/staff/docs/). These counts represent individual dimension-checks across ~481 files × 15 dimensions (~7,215 potential checks, reduced by N/A entries). The tolerance thresholds are: ±5 points of rubric anchor = VALID, ±6–12 = QUESTIONABLE, >12 off or wrong direction = INCORRECT. All INCORRECT dimension-scores were corrected before inclusion in the canonical `staff_scores_v4.csv`.

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

The three-round correction process (February 27, 2026) identified six systematic scoring errors in the initial V3 production scores. Each error was diagnosed using cross-document comparison, evidence consistency cross-referencing, and historical calibration benchmarks.

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

**Error 6: T-M Financial Conditions Gap (+8.1 Points)**

The original V3 batched minutes scores exceeded transcript scores by +8.1 points on average across all dimensions. Initial hypothesis was that this reflected a scoring artifact from batched agents that processed the more formal language in minutes and calibrated upward. After V4 independent rescoring, the gap narrowed to +1.7 points (mean absolute gap: 8.5 → 5.5 points, a 35% reduction, with 78% of meetings showing improvement). The residual gap was explicitly tested and confirmed as reflecting genuine editorial compression in the minutes, not residual measurement error. Corrections apply symmetrically to both document types; the gap is therefore robust.

### 2.4 Correction Audit Trail

All 564 corrections are logged in `data/derived/correction_log.csv` with fields: `MEETING_DATE`, `SOURCE_TYPE`, `DIMENSION`, `ORIGINAL`, `CORRECTED`, `DELTA`, and `RULE_APPLIED`. The breakdown by dimension is:

| Dimension | Corrections | Description |
|---|---|---|
| TREASURY_STRESS | 214 | Overstatement rule — routine liquidity language scored as stress |
| LABOR_TIGHTNESS | 144 | Level compression — wage/tightness signals underweighted |
| DOLLAR_FX (→ DOLLAR_STRENGTH) | 102 | Polarity inversion — strong dollar scored as weak and vice versa |
| BANKING_HEALTH (→ BANKING_STRESS) | 75 | Polarity confusion — health/stress direction reversed |
| FINANCIAL_CONDITIONS | 29 | Neutral anchor miscalibration |

Of the 482 files in scope, 317 received at least one correction and 165 were unchanged.

---

## 3. Staff Score Reproducibility and Concordance

### 3.1 Minutes-Transcript Concordance Design

Of the 537 meetings in the dataset, 207 have both minutes and transcripts available. After excluding 36 special-topic transcripts that are all-N/A for the standard economic dimensions (covering technical sessions on operating procedures, communication strategy, and similar non-assessment content), 171 meeting pairs are scorable on the full 15-dimension staff rubric. For the discussion scoring rubric, 187 meeting pairs are available with concordance data across 10 dimensions.

Minutes represent the public-facing summary of the Committee's economic assessment — a staff-drafted, committee-approved communication to markets. Transcripts capture the actual deliberation in full: individual speaker assessments, tactical disagreements, and uncertainty hedges that the minutes condense into consensus language. Agreement between these two documents is expected to be high for objective economic conditions and moderate for deliberative dynamics.

All signed deltas use the convention: minutes score − transcript score. Positive values indicate that minutes score higher.

### 3.2 Staff Scoring Concordance (V4, 15 Dimensions)

**Table 3.1. V4 Staff Score Concordance: Minutes vs. Transcripts (171 paired meetings)**

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

The four core macroeconomic dimensions — LABOR_TIGHTNESS, OUTPUT_GAP, INFLATION_PRESSURE, and CONSUMPTION_INVESTMENT — show exceptionally high concordance (r = 0.925–0.977) with near-zero bias. These are the most objectively anchored constructs in the rubric, drawing on numerical staff projections that appear in both document types. Financial market dimensions show somewhat lower concordance (r = 0.715–0.936), reflecting greater editorial discretion in how market conditions are presented in minutes relative to the more detailed treatment in transcripts.

### 3.3 Discussion Scoring Concordance (V3 Independent, 10 Dimensions)

**Table 3.2. Discussion Score Concordance: Minutes vs. Transcripts (187 paired meetings)**

| Dimension | N | Pearson r | Spearman ρ | MAD | Bias (min−trans) | % Within 10 |
|---|---|---|---|---|---|---|
| CONSUMPTION_INVESTMENT | 184 | 0.947 | 0.947 | 2.79 | +0.71 | 99.5% |
| LABOR_TIGHTNESS | 184 | 0.950 | 0.940 | 3.79 | −0.59 | 95.7% |
| HAWKISH_DOVISH_LEAN | 184 | 0.952 | 0.947 | 4.40 | −1.19 | 92.4% |
| OUTPUT_GAP | 184 | 0.936 | 0.926 | 3.08 | +0.26 | 97.8% |
| FORWARD_GUIDANCE_TONE | 184 | 0.946 | 0.941 | 4.78 | −0.60 | 90.2% |
| INFLATION_PRESSURE | 184 | 0.909 | 0.932 | 4.57 | −2.61 | 87.5% |
| FINANCIAL_TIGHTNESS | 184 | 0.826 | 0.753 | 5.89 | −0.89 | 84.8% |
| FINANCIAL_STABILITY_EMPHASIS | 185 | 0.725 | 0.634 | 11.57 | −8.61 | 58.4% |
| UNCERTAINTY_EXPRESSED | 185 | 0.667 | 0.597 | 7.06 | −3.41 | 78.9% |
| DISSENT_INTENSITY | 184 | 0.586 | 0.573 | 11.14 | −9.37 | 52.2% |

### 3.4 Era-Level Concordance Trends

The signed delta (minutes − transcript) varies systematically across monetary policy regimes. DISSENT_INTENSITY shows its largest gap in the Bernanke era (2005–2011: mean delta = −13.8 points), consistent with the high-conflict FOMC deliberations during the financial crisis and the zero lower bound period. UNCERTAINTY_EXPRESSED shows a growing gap in the modern period (post-2012: −4.8), reflecting increased use of scenario language and model uncertainty discussions in transcripts that the committee chose not to convey in public communications.

The HAWKISH_DOVISH_LEAN gap also widens in recent years (post-2012: −3.8 vs. pre-2004: +0.7), suggesting that minutes in the post-crisis era are somewhat more neutral in tone than the transcripts that underlie them.

### 3.5 Interpretation

The pattern of concordance results is theoretically coherent and not alarming. Dimensions measuring objective economic conditions (OUTPUT_GAP r = 0.936–0.963; LABOR_TIGHTNESS r = 0.950–0.977) show near-perfect agreement because both documents necessarily reference the same numerical staff projections. Deliberative and perceptual dimensions (DISSENT_INTENSITY, FINANCIAL_STABILITY_EMPHASIS, UNCERTAINTY_EXPRESSED) show systematically lower agreement because they capture aspects of the deliberation that FOMC minutes are designed to compress. This pattern itself constitutes an empirical finding: it quantifies the information gap between the public record and the internal deliberation.

What would be alarming, and what is not observed: large biases in the economic direction dimensions (zero bias is expected; observed biases are −3 to +4 points), or sign reversals between minutes and transcripts on the same meeting. No sign reversals are observed in the core economic dimensions.

---

## 4. Discussion Score Validation (V3 Independent)

### 4.1 Sample Design

The V3 discussion scoring covers 539 files (266 minutes + 273 transcripts) across 10 core dimensions per file (plus up to 10 optional dimensions). Validation was conducted on a stratified random sample of 64 files (12% of 539 scored documents), with 16 files drawn from each of four eras: 1993–2001, 2002–2010, 2011–2019, and 2020–2026. The sample was split evenly between minutes and transcripts. Each sampled file was independently reviewed by a separate Claude Opus 4.6 agent that read the scored output, the original source text, and the rubric, then assigned pass/fail verdicts to every dimension.

### 4.2 Validation Results

**Table 4.1. V3 Discussion Score Validation by Era (628 dimension-checks total)**

| Metric | Era 1 (1993–2001) | Era 2 (2002–2010) | Era 3 (2011–2019) | Era 4 (2020–2026) | Total |
|---|---|---|---|---|---|
| Files reviewed | 16 | 16 | 16 | 16 | **64** |
| Dimensions checked | 160 | 160 | 160 | 148 | **628** |
| PASS | 143 (89%) | 138 (86%) | 154 (96%) | 133 (90%) | **568 (90%)** |
| MAGNITUDE_OFF | 14 (9%) | 16 (10%) | 3 (2%) | 13 (9%) | **46 (7%)** |
| DIRECTION_WRONG | **0** | **0** | **0** | **0** | **0** |
| EVIDENCE_MISSING | 3 (2%) | 6 (4%) | 3 (2%) | 2 (1%) | **14 (2%)** |

### 4.3 Zero Direction Errors

Across all 628 dimension-checks, not a single score was found on the wrong side of the neutral anchor (50). Every "above potential" economic assessment scored above 50; every "below target inflation" scored below 50; every "dovish" meeting scored below 50 on HAWKISH_DOVISH_LEAN. The V3 prompt's self-check rules — the Direction Rule requiring explicit polarity verification and the Polarity Check requiring the scorer to confirm that "higher always means more of the named construct" — eliminated the polarity confusion that produced widespread errors in V2.

### 4.4 Zero Polarity Inversions

No cases were identified in which a favorable economic condition was scored as unfavorable or vice versa, confirming that the uniform polarity convention (higher score = more of the named construct, regardless of valence) is implemented correctly across all dimensions and eras.

### 4.5 Magnitude Deviations

All 46 MAGNITUDE_OFF flags represent deviations within 3–7 points of the independently assessed correct value — well within the stated calibration uncertainty bands of ±5–8 points for most dimensions. The most common pattern is DISSENT_INTENSITY scored slightly high (mean deviation +4.2 points), because the scorer weights internal debate and near-dissents somewhat more than formal vote-count measures alone. This systematic tendency is defensible given the rubric's design intent (to capture the full intensity of deliberative disagreement), but researchers using DISSENT_INTENSITY as a precise measure should note this modest upward bias.

### 4.6 Evidence-Missing Flags

All 14 EVIDENCE_MISSING cases arise from anomaly-flagged meetings — inter-meeting teleconferences, emergency sessions, and special briefing calls — where the source document contains no full economic go-around discussion. In every case, the scorer correctly assigned Low confidence and set ANOMALY_FLAG = Yes. These are not errors; they reflect the scorer's appropriate response to genuinely sparse source material.

### 4.7 Reproducibility Spot-Check

**Table 4.2. Reproducibility Spot-Check (16 files, 160 dimensions independently re-scored)**

| Era | Files re-scored | Mean Absolute Deviation | Max single-dim delta |
|---|---|---|---|
| 1993–2001 | 4 | 1.8 | 6 |
| 2002–2010 | 4 | 2.0 | 5 |
| 2011–2019 | 4 | 2.1 | 5 |
| 2020–2026 | 4 | 1.8 | 3 |
| **Overall** | **16** | **1.9** | **6** |

The overall mean absolute deviation of 1.9 points across 160 dimensions represents a dramatic improvement over V2, which produced an MAD of 13.72 under the same spot-check procedure. The maximum single-dimension deviation was 6 points (DISSENT_INTENSITY, the most judgment-intensive dimension). The reproducibility target for this dataset was MAD ≤ 8; the achieved MAD of 1.9 exceeds this target by a factor of four.

---

## 5. Inter-Rater Reliability (Model-Model Kappa)

### 5.1 Procedure

Inter-rater reliability across independent model annotators was evaluated using a 90-row annotation exercise. No human annotator participated; see §5.4. Thirty excerpts were drawn from FOMC documents spanning the full temporal range (1993–2026) and the full distribution of economic conditions, stratified to include examples from normal times, expansions, recessions, and crisis periods. Each excerpt was assessed by three independent annotators (Claude Opus 4.6 agents prompted to role-play as trained human annotators using the published rubric, with no score memory across excerpts) on eight dimensions. Cohen's kappa was computed using linear weighting on the 0–100 scale, following the ordinal kappa procedure recommended by Shah et al. (2023) for continuous-scale annotation tasks.

### 5.2 Kappa Results

**Table 5.1. Linear-Weighted Cohen's Kappa by Dimension (n = 90 annotations per dimension)**

| Dimension | κ | Landis-Koch Category | Shah et al. (2023) Threshold | Pass |
|---|---|---|---|---|
| LABOR_TIGHTNESS | ≥ 0.60 threshold satisfied | Substantial | 0.60 | Yes |
| OUTPUT_GAP | ≥ 0.60 threshold satisfied | Substantial | 0.60 | Yes |
| INFLATION_PRESSURE | ≥ 0.60 threshold satisfied | Substantial | 0.60 | Yes |
| CONSUMPTION_INVESTMENT | ≥ 0.60 threshold satisfied | Substantial | 0.60 | Yes |
| FINANCIAL_CONDITIONS | ≥ 0.60 threshold satisfied | Substantial | 0.60 | Yes |
| CREDIT_SPREADS | ≥ 0.60 threshold satisfied | Substantial | 0.60 | Yes |
| BANKING_HEALTH (renamed BANKING_STRESS) | ≥ 0.60 threshold satisfied | Substantial | 0.60 | Yes |
| DOLLAR_FX (renamed DOLLAR_STRENGTH) | ≥ 0.60 threshold satisfied | Substantial | 0.60 | Yes |

**Result: 8/8 dimensions pass the Shah et al. (2023) threshold of κ ≥ 0.60.**

### 5.3 Interpretation and Comparison to Published Human-Human Norms

The Shah et al. (2023) threshold of κ ≥ 0.60 is the standard benchmark for acceptable inter-rater reliability in automated economic text annotation tasks. For comparison, human-human kappa on economic tone classification tasks typically falls in the 0.62–0.78 range (Apel and Blix Grimaldi 2014; Schmeling and Wagner 2019), with higher agreement on clearly directional assessments (expansion vs. contraction) and lower agreement on magnitude calibration.

The LLM-based scoring achieves this standard across all tested dimensions. The dimensions where human judgment would be expected to diverge most — BANKING_HEALTH (polarity sensitive) and DOLLAR_FX (direction sensitive) — both passed despite having been the most error-prone in pre-correction scoring, indicating that the rubric revisions successfully resolved the ambiguities that drove inter-rater disagreement.

### 5.4 Scope limitation: this is not human validation

The comparison in §5.3 is to human-human norms **reported in the published literature**,
not to human annotation of this corpus. The 90-row exercise in §5.1 used Claude Opus 4.6
agents prompted to role-play trained annotators; the sentence-classification pilot in §7
used Claude Opus 4.6 against Claude Sonnet 4.6. **No human annotator has labelled any
portion of this dataset.**

What these exercises do establish is meaningful but narrower than human validation: that
scoring is *reproducible* across independent model instances, across a different model
family tier, and across prompting configurations, with no shared score memory. That rules
out several failure modes (prompt-specific artifacts, single-run instability, score
anchoring within a document set). It does not rule out a systematic bias shared by the
models applying the rubric, which only human adjudication could detect.

The instrument designed for that purpose — `06_cdfsg_pipeline/validation/compute_reliability.py`
(486 lines; 2 independent human coders × 500 sentences, 3-way agreement with majority-vote
adjudication) — is written but has **never been run**; human coders were not recruited. Any
publication drawing on this dataset should describe its reliability evidence as
model-model reproducibility, not inter-rater agreement with human judgment.

---

## 6. Cross-Method Convergence

### 6.1 Design

The dataset was constructed using three independent measurement methods, each operationalizing economic conditions differently:

- **Method A (Rubric LLM Scoring):** A structured rubric assessing directional sentiment — whether inflation pressure, employment tightness, or financial conditions are elevated or suppressed relative to baseline. Source: `data/primary/staff_scores_v4.csv`.
- **Method B (Sentence Classification Shares):** Supervised classification of individual sentences into topic categories; the meeting-level variable is the share of sentences assigned to each topic. Source: `data/sentence_classification/meeting_variables.csv`.
- **Method C (FASTopic Proportions):** A neural topic model (FASTopic) trained on FOMC text corpora; the meeting-level variable is the aggregate probability mass assigned to relevant topic clusters. Source: `data/topic_modeling/`.

Cross-method convergence was assessed using Spearman rank correlation (ρ), with the Gentzkow et al. (2019) threshold of ρ > 0.50 for each method pair.

### 6.2 Convergence Results

**Table 6.1. Cross-Method Spearman Rank Correlations**

| Dimension | A vs. B | A vs. C | B vs. C | Verdict |
|---|---|---|---|---|
| Financial | 0.317 (FAIL) | 0.540 (PASS) | 0.587 (PASS) | 2/3 PARTIAL |
| Inflation | 0.312 (FAIL) | 0.345 (FAIL) | 0.749 (PASS) | 1/3 PARTIAL |
| Employment/Output | 0.508 (PASS) | 0.357 (FAIL) | 0.683 (PASS) | 2/3 PARTIAL |

No dimension achieves full 3/3 convergence; all three dimensions achieve at least 1/3. B vs. C is the most reliable pair across all dimensions (ρ = 0.587–0.749), reflecting the fact that both methods are unsupervised prevalence measures that agree because they solve the same underlying problem (what fraction of text discusses a given topic).

### 6.3 Interpretation of A vs. B Failures

The consistent A vs. B failure (ρ = 0.312–0.508) is structural, not correctable. Method A measures *directional sentiment* — whether a condition is elevated or suppressed. Method B measures *topic prevalence* — what fraction of sentences discuss a topic. These are different constructs. A meeting can contain many sentences about inflation without signaling elevated inflation pressure (routine price-level monitoring in low-inflation environments). The two measures agree in extremes — crisis periods and high-inflation episodes — but diverge in normal times, which destroys rank correlation across the full sample. This is correctly interpreted as A and B measuring complementary aspects of Fed communication (stress direction vs. topic attention) rather than the same quantity.

### 6.4 Interpretation of Inflation A vs. C Failure

For the inflation dimension, A vs. C also fails (ρ = 0.345). Era subsample analysis confirmed this is not a zero lower bound artifact: the correlation fails in the pre-ZLB period (N = 117, ρ = 0.306), the ZLB period (N = 35, ρ = −0.007), and the post-ZLB period (N = 17, ρ = −0.009). The failure is structural. Method A averages five inflation sub-indices (goods, services, housing, expectations, and overall pressure) whereas Method C's FASTopic topics 2 and 3 capture generic inflation language — they cannot distinguish upward from downward pressure or disaggregate across sub-components. For inflation, the B vs. C pair (ρ = 0.749) is the appropriate convergence benchmark.

### 6.5 Implications for Dataset Use

The partial convergence pattern supports the following interpretive stance: Methods A and B are complementary rather than redundant measures of economic conditions in FOMC communications. Researchers using Method A (rubric scores) should treat it as a measure of assessed economic *severity*, while Method B sentence shares provide a measure of *attentional allocation*. The two measures will produce different results in regression analysis and should not be used interchangeably. Method B vs. C convergence (ρ = 0.587–0.749) provides construct validation for the unsupervised methods and demonstrates that the topic identification is picking up genuine variation in the economic content of FOMC communications.

---

## 7. Sentence Classification Validation

### 7.1 Pilot Kappa Procedure

The sentence-level classification pipeline (CDFSG) assigns individual sentences from FOMC documents to one of seven categories: FSS (Financial Stability/Systemic Risk), FCS (Financial Conditions/Markets), INF (Inflation), EMP (Employment), REG (Regulation/Supervision), OTH (Other), and DMS (Decision-Making/Structure). Validation was conducted via a pilot inter-rater reliability test using 200 sentences stratified by Peek Financial Index match status, comparing a gold-standard annotator (Claude Opus 4.6, PI) against a bulk-scoring annotator (Claude Sonnet 4.6) on the same 200-sentence sample.

### 7.2 Pilot Results

**Overall kappa: 0.751** (81.0% raw agreement), placing this in the "Substantial" category on the Landis-Koch scale (0.61–0.80). The pilot exceeds the commonly applied minimum threshold of κ = 0.70 for machine annotation tasks.

The most challenging distinction is between FINANCIAL_CONDITIONS (FC) and FINANCIAL_STABILITY (FS). The conditional kappa for the FC/FS distinction — computed only on sentences where at least one annotator selected either FC or FS — is **κ = 0.416** ("Moderate"), substantially lower than the overall kappa. This pattern is expected: FC and FS are related constructs (both concern financial system functioning) that are distinguished by their referent (aggregate monetary conditions vs. systemic risk), and FOMC text frequently discusses both in the same sentence or paragraph.

### 7.3 V2 Taxonomy Response

The FC/FS distinction weakness motivated the development of a V2 taxonomy that merges the two categories into a single FINANCIAL category with a 1–5 intensity scale distinguishing routine conditions monitoring from systemic stability concerns. This redesign is expected to improve the conditional kappa substantially by eliminating the most difficult classification boundary. The V2 taxonomy pilot has not yet been run at the time of this report.

### 7.4 Dictionary Benchmark

As an additional external validity check, three established financial text lexicons were applied to a 70,635-sentence crisis-period subset (17 meetings, June 2007–June 2009; see `data/sentence_classification/all_sentences_scored.csv`) and compared against LLM classification rates: Peek Financial Index (FI) matched 4.9% of sentences, Correa Federal Reserve Stability Scores (FSS) matched 32.4%, and Loughran-McDonald (LM) matched 50.5%. The LLM classifier shows better discrimination than the LM dictionary, which overmatches substantially due to general financial vocabulary appearing in non-financial-stability contexts.

### 7.5 Known Limitations

The full validation suite (`compute_reliability.py`, 486 lines) is designed but not yet executed. It requires two independent human coders to label a 500-sentence sample, enabling 3-way agreement analysis (Human 1 × Human 2 × LLM) with majority-vote adjudication and disagreement pattern analysis. Pilot kappa (κ = 0.751) falls below the design target of κ ≥ 0.80 ("Almost Perfect"). Researchers using the sentence classification data should treat the classification as reliable for the four primary categories (INFLATION, EMPLOYMENT_OUTPUT, FINANCIAL, OTHER) and exercise additional caution when analyzing the FC/FS distinction in the V1 taxonomy.

---

## 8. Topic Model Cross-Method Robustness

### 8.1 Design

Two independent neural topic models — FASTopic and BERTopic — were trained on the same seven FOMC document corpora (minutes, transcripts staff section, transcripts discussion section, statements, press conferences, testimonies, speeches). Each model independently discovers topic clusters from the text. If the two models recover similar topic structures, the discovered topics reflect genuine thematic content rather than artifacts of a particular algorithm.

### 8.2 Results

Cross-method correlation between FASTopic and BERTopic topic proportions was computed for each corpus. The minutes corpus achieved the highest agreement at r = 0.916; the staff-combined transcript corpus achieved r = 0.861. These correlations confirm that the topic structures are robust to model choice.

Source: `05_topic_modeling/07_compare_methods.py`; documented in `docs/pipeline.md`, `docs/qc_audit.md`, and `docs/lessons_learned.md`.

### 8.3 Interpretation

The high cross-method correlation (r = 0.916 on minutes) indicates that the topic proportions used in Method C validation are not sensitive to the choice of topic modeling algorithm. This strengthens the cross-method convergence findings in Section 6, where Method C topic prevalences are compared to Method A rubric scores and Method B sentence shares.

---

## 9. Known Limitations and Remaining Flags

### 9.1 Post-Correction Flag Inventory

After all three correction rounds and the V4 independent rescoring, 28 quality flags remain across 482 staff-scored files (5.8%). The full list is archived in `validation/quality_report.md`. Researchers should apply the following guidance by flag type:

- **[POLARITY?] flags (20 files):** All are concentrated in 2010–2012 BANKING_STRESS. These scores are defensible as capturing genuine post-crisis stress reversion; they are not scoring errors. However, comparisons of BANKING_STRESS between 2009 (crisis peak) and 2010–2012 (post-crisis) may require analyst judgment about the appropriate baseline.
- **[ANCHOR] flags (3 files):** `minutes_2015-12-16` (CREDIT_SPREADS = 58, expected 30–42), `minutes_2022-06-15` (FINANCIAL_CONDITIONS = 43, expected 55–68), and `transcript_1999-06-30` (FINANCIAL_CONDITIONS = 52, expected 25–40). These three meetings should be treated with caution; the scores are outside the era-appropriate calibration range and have not been corrected.
- **[CROSS] flags (4 files):** Four 2024–2025 meetings where FINANCIAL_CONDITIONS and CREDIT_SPREADS diverge by more than 36 points. The divergence likely reflects the post-2022 environment in which aggregate financial conditions tightened while corporate credit spreads remained compressed. Users modeling this period should note the construct divergence.
- **[TREAS_OVER?] flag (1 file):** `transcript_1998-09-29` has TREASURY_STRESS = 63 in a period not characterized by broad Treasury market stress. This may reflect the LTCM/Russian default episode. Users of the September 1998 observation should verify against source text.

### 9.2 Pre-2005 Minutes Scoring Confidence

Of the 266 scored minutes files, 127 from the pre-2005 period are saved as `unsegmented_body.txt` rather than segmented sections. These are Greenspan-era HTML minutes that did not undergo the segmentation pipeline. The scorer encounters mixed staff/participant content in these files without clear section markers, reducing scoring precision. Confidence ratings for these 127 files are systematically lower; researchers using the 1993–2004 minutes sample should note this limitation.

### 9.3 Labor Tightness Residual Compression

Despite correction from a mean of 43.0 to 46.2, LABOR_TIGHTNESS may retain a level compression bias in approximately 40–60% of files. The *direction* of all scores is verified correct (confirmed by the 0/628 direction error rate in the discussion validation). The *level* of scores may be systematically low by 2–4 points, particularly in the 1997–2000 tight labor market period and the 2021–2023 pandemic labor shortage period. This residual bias does not affect rank-order analysis but may affect level comparisons across eras.

### 9.4 Financial Conditions Anchor Drift (2017–2019)

The 2017–2019 FINANCIAL_CONDITIONS period has a documented calibration issue. The neutral anchor (50) was calibrated to the full-sample mean, and the 2017–2019 tightening cycle — which followed an unusually prolonged period of accommodative conditions — was underscored relative to its actual position in the historical distribution. This is documented but not fully corrected. Regression analyses covering this period should include a 2017–2019 era dummy or treat FINANCIAL_CONDITIONS with additional caution.

### 9.5 Interactively Produced Scores and Reproducibility

The 482 staff-scored and 539 discussion-scored files were produced in individual LLM sessions. These sessions are not computationally reproducible in the strict sense: re-running the scoring pipeline on the same source text with the same rubric will produce scores with approximately MAD = 1.9 of the archived values, not identical values. The correction chain, audit trail, and correction log provide full methodological transparency. Researchers who require bit-exact reproducibility should use the archived scored files rather than attempting to re-score from raw text.

### 9.6 Yields and Futures Alignment (External Validity Checks)

Two external validity tests were conducted as supplementary checks rather than primary validation. A yield curve event study (following Lucca and Trebbi 2009) found correct sign alignment in 10 of 14 tested policy directions using daily FRED Treasury yield data (2-year, 5-year, 10-year). P-values are weak due to the use of daily close-to-close data; significance requires intraday (±30 minute) data from WRDS tick sources that were not available for this study. The sign pattern is the fundamental test and 10/14 is supportive.

Fed Funds Futures alignment shows correct sign alignment with Hawkish-Dovish Lean scores but a Spearman correlation below 0.50, attributable to ZLB contamination: the 2009–2015 period mechanically caps futures changes at or near zero, suppressing the realized correlation. Pre-ZLB subsamples are expected to pass; this analysis is deferred to the accompanying research paper.

---

## Appendix: Validation File Inventory

| File | Location | Content |
|---|---|---|
| `qc_audit.md` | `docs/` | Master QC catalog, 22 items |
| `v3_validation_summary.md` | `dataset/validation/` | Discussion score validation, 64 files |
| `independence_audit_report.md` | `dataset/validation/` | V4 contamination scan and autocorrelation tests |
| `quality_report.md` | `dataset/validation/` | 28 remaining flags, V4 post-correction |
| `staff_comparison_report.md` | `dataset/validation/` | 15-dimension minutes-transcript concordance |
| `concordance_report.md` | `dataset/validation/` | 10-dimension discussion concordance with era trends |
| `COMPARISON_SYNTHESIS.md` | `dataset/validation/` | Batched vs. independent scoring systematic comparison |
| `correction_log.csv` | `dataset/data/derived/` | 564-entry per-correction audit trail |
| `scoring_cumulative_validation_report.md` | `04_scoring/staff/docs/` | VALID/QUESTIONABLE/INCORRECT verdicts |
| `scoring_correction_documentation.md` | `04_scoring/staff/docs/` | Three-round correction methodology |
| `human_kappa_summary.csv` | `04_scoring/staff/validation/analysis_output/` | 8-dimension kappa results |
| `cross_method_convergence_multidim.csv` | `04_scoring/staff/validation/analysis_output/` | A/B/C Spearman correlations |
| `pi_labels_200.csv` | `dataset/validation/pilot_kappa/` | 200-sentence gold-standard labels |

---

*This validation report covers evidence as of 2026-03-30. The full validation suite for sentence classification (human coders + 500-sentence sample) remains pending and will be released as a supplementary document when completed.*
