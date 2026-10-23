# FOMC Document Scoring: Methodology

**Dataset version**: 2.0.0 (draft, local, not published)
**Last updated**: 2026-10-23
**Scope**: FOMC minutes (1993–2026) and transcripts (1993–2020)

---

## 1. Overview

This dataset addresses a fundamental question in central bank communication research: do FOMC minutes systematically compress information relative to the underlying transcripts on which they are based? The minutes are an edited institutional document published approximately three weeks after each meeting; the transcripts are a verbatim record released with a five-year lag. If the editing process introduces systematic patterns — suppressing dissent, downplaying financial stability concerns, moderating expressed uncertainty — then the minutes present a filtered representation of Committee deliberations rather than a faithful summary.

The research is motivated by an unresolved debate about whether the Federal Reserve treats financial stability as an implicit third mandate alongside its statutory dual mandate of maximum employment and stable prices. As Cieslak and Vissing-Jorgensen (2021) observe, "we lack direct evidence on what weight the Fed places on different objectives." This dataset provides measurements relevant to this question by measuring how FOMC documents characterize economic and financial conditions, how attention is allocated across policy concerns, and where the public minutes diverge from the internal deliberative record.

**Focus.** Version 2.0.0 is organised around three priorities: price stability, maximum employment (together the statutory dual mandate) and financial stability. Every other variable (policy stance, dissent, uncertainty, spending, productivity, the dollar) is kept as context for these three, not as a priority measure. `data/derived/priority_variable_map.csv` assigns each variable to a group; the assignment is the author's judgement, not an estimated result. Components that were unvalidated or superseded (mechanism coding, the V3 discussion scoring, supplementary 2026 scores, minutes-versus-transcripts case comparisons, the correction log) were removed; see CHANGELOG [2.0.0].

To answer this question, three independent analytical methods are applied to the same document corpus. Using multiple independent methods for triangulation is essential: any single method embeds its own assumptions, and convergent findings across structurally different approaches provide stronger evidence than any one method alone. The three methods are:

- **Method A**: LLM rubric-based scoring of FOMC documents on continuous economic and policy dimensions
- **Method B**: Sentence-level classification of every sentence in the transcript and minutes corpus using a predefined policy-topic taxonomy
- **Method C**: Unsupervised topic modeling across multiple FOMC document corpora using FASTopic

All three methods share the same raw document corpus (see DATA_PROVENANCE.md) and are designed to be analytically independent of one another. Their outputs are compared in cross-method convergence analysis to assess the robustness of key findings.

---

## 2. Data Sources

### 2.1 FOMC Transcripts

FOMC meeting transcripts are declassified on a five-year rolling lag and published by the Board of Governors of the Federal Reserve System. They are available at:

> https://www.federalreserve.gov/monetarypolicy/fomc_historical.htm

Transcripts are verbatim records of meeting proceedings. They include staff economic and financial briefings (which draw on Greenbook/Tealbook materials), participant statements during the go-around and policy discussion, and formal voting.

**Coverage in this dataset**: 272 meetings with transcripts in the V4.1 discussion table and 225 in the staff table (`staff_scores_v6.csv`), spanning January 1993 through December 2020. Transcripts for meetings after 2020 are not yet publicly available due to the five-year declassification lag.

### 2.2 FOMC Minutes

FOMC meeting minutes are published approximately three weeks after each meeting. They are institutional summaries prepared by Board staff and approved by the Committee. They present synthesized descriptions of staff briefings and participant discussions using quantifier language ("most participants," "several members," "a few noted") rather than attributing views to individual members.

**Coverage in this dataset**: 270 scored minutes in each of the staff and V4.1 discussion tables (265 from 1993 to 2025 plus the five 2026 meetings), spanning 1993–2026. One duplicate copy of the 2012-10-23 minutes was removed earlier (CHANGELOG 1.1.0).

### 2.3 Other Document Types

The raw document folders also hold FOMC statements (247 files), press conference transcripts (95), congressional testimonies (62), and Federal Reserve speeches (3,011 files; 1,979 are in the scored speech manifest). These are file counts on disk, not de-duplicated documents. They are not scored in Method A. Speeches and statements enter Method B for the 2007-2009 crisis window (Section 4); there is no separate table of scores for statements, press conferences, Beige Books or speeches in this release.

### 2.4 Access and Rights

All documents are products of the United States federal government and are in the public domain. No licensing restrictions apply to the source documents. The scoring data, rubrics, and derived datasets produced by this project are released under CC-BY 4.0 unless otherwise specified.

---

## 3. Method A: LLM Rubric Scoring

Method A uses large language model (LLM) agents to score FOMC documents against structured rubrics on a set of continuous economic and policy dimensions. Two separate rubrics are applied to two distinct aspects of each meeting: the staff assessment and the participant discussion.

### 3.1 Staff Assessment Scoring (V4 rubric; `staff_scores_v6.csv`)

**What is scored**: The staff's assessment of economic and financial conditions as presented in Greenbook/Tealbook materials and reflected in meeting documents. For transcripts, this is the economic and financial briefing section; for minutes, it is the synthesized staff-report language ("the staff reported," "the Tealbook projection," "in the staff's assessment").

**Scoring instrument**: The staff table `data/primary/staff_scores_v6.csv` (495 rows: 270 minutes + 225 transcripts, with transcripts re-scored on repaired text) uses the V4 Staff Assessment Rubric. The table is mixed-vintage: the `SCORE_VERSION` column records each row's vintage and comparisons should stay within one vintage. The rubric scores 15 dimensions on a continuous 1–100 scale, where 50 represents a neutral baseline. The dimensions are organized into three tiers:

- **Tier 1 Core Economic** (5 dimensions): INFLATION_PRESSURE, OUTPUT_GAP, LABOR_TIGHTNESS, CONSUMPTION_INVESTMENT, PRODUCTIVITY
- **Tier 1 Core Financial** (6 dimensions): FINANCIAL_CONDITIONS, TREASURY_STRESS, CREDIT_SPREADS, EQUITY_VALUATION, BANKING_STRESS, DOLLAR_STRENGTH
- **Tier 2 Inflation Sub-Components** (4 dimensions): INFLATION_GOODS, INFLATION_SERVICES, INFLATION_HOUSING, INFLATION_EXPECTATIONS

**Key design features**:

*Uniform polarity*: Across all 15 dimensions, a higher score always means more of the named construct. FINANCIAL_CONDITIONS > 50 means tighter financial conditions; BANKING_STRESS > 50 means more bank stress; DOLLAR_STRENGTH > 50 means a stronger dollar. This uniform polarity convention eliminates the most common source of scoring inversion errors.

*Uncertainty bands*: Each score is accompanied by an uncertainty interval (typically ±3 to ±8 points depending on document quality and language specificity) reflecting how confidently the score can be placed. This is distinct from economic uncertainty about the outlook; it is the scorer's uncertainty about the appropriate score given the evidence.

*Confidence tiers*: Each score carries a High/Moderate/Low confidence designation based on the quantity and specificity of textual evidence. High confidence requires multiple sentences with specific data points; Low confidence is assigned when a topic is inferred from limited or indirect language.

*Bright-line polarity rules*: Six dimensions have mandatory override rules to prevent systematic errors. For example: "accommodative" or "easy" financial conditions must receive a score below 50 (not above); "well-capitalized" or "sound" banking language must receive a score below 50 for BANKING_STRESS. These bright-line rules are enforced as hard constraints and override general rubric judgment.

*Anchor calibration*: Twelve landmark meetings spanning the full era range (1993–2022) have pre-defined score ranges for key dimensions. Scorers are required to compare their scores to these anchors and document any deviations. Anchors include, for example, the 2009 deflation scare meetings (INFLATION_PRESSURE 15–20), the post-GFC near-target period (38–42), and the 2022 inflation peak (82–88). Anchors prevent era-level drift across the scoring run.

*Three-part structured output*: Each scored document produces (1) chain-of-thought reasoning, (2) evidence blocks citing specific text passages with speaker attribution for transcripts, and (3) machine-readable structured output. The evidence blocks serve as the primary reproducibility record.

**Evidence independence mandate**: The rubric's operative instruction is: "Score this document as if it is the only FOMC document you have ever seen. Do not reference, compare to, or recall scores from any other meeting." One fresh LLM agent is instantiated per document with no prior meeting context. This independence mandate is the defining methodological difference between V4 and the earlier V3 batched scoring (not shipped; see Section 3.3).

### 3.2 Participant Discussion Scoring (V4.1)

**What is scored**: The center-of-gravity of participant views in the discussion sections of each meeting. For transcripts, this is the go-around and policy discussion; for minutes, it is the synthesized participant-view language using quantifier expressions.

**Scoring instrument**: `data/primary/discussion_scores_v4_1.csv` (542 rows: 272 transcripts, 270 minutes) uses the V4.1 rubric: the 15 dimensions shared with the staff rubric plus five discussion dimensions (HAWKISH_DOVISH_LEAN, DISSENT_INTENSITY, FINANCIAL_STABILITY_EMPHASIS, FORWARD_GUIDANCE_TONE, UNCERTAINTY_EXPRESSED), on rebuilt member-discussion inputs. See `codebooks/CODEBOOK_discussion_scores_v4_1.md`.

A key interpretive rule distinguishes the discussion rubric from the staff rubric: uncertainty bands in the discussion rubric reflect the *range of participant views*, not scorer confidence. Narrow uncertainty (±3–5) indicates broad Committee agreement; wide uncertainty (±10–15) indicates substantially dispersed views.

**Applied symmetrically**: The rubric is applied to all 270 scored minutes and all 272 transcripts. For the 215 meetings with a minutes and a transcript on the same date key (224 pairs once the registry key map is used to match the two-day-meeting date conventions, Section 7), the paired design enables direct minutes-transcript comparison, with the caveat in Section 3.2.1 that the minutes rows are mostly patches, not fresh scores.

**Evidence independence mandate**: One fresh agent per transcript, no shared context, no batching. This does not hold for the V4.1 minutes rows (see Section 3.2.1).

### 3.2.1 How the V4.1 rows were produced

How the rows were produced differs by document type, and the `METHOD` column records it (277 `fresh_score`, 265 `patch_of_v4_analysis`):

- **Transcripts (272)** are fresh scores, one fresh agent per meeting. 71 of them were re-scored under the V4.1.1 clarifications; the other 201 carry the original V4.1 scores.
- **Minutes (265)** are patches of the earlier V4 analyses, not fresh scores, so cells the patch left unchanged partly rest on the earlier analysis. The patch file in use (project repository, not shipped) is `all_scores_disc_m_v411_patched_v2d.csv`, in which 2000-12-19 was re-scored on a corrected input (HAWKISH_DOVISH_LEAN 38 to 42, 19 other dimensions unchanged). Only five minutes rows (the 2026 meetings of 2026-03-18, 04-29, 06-17, 07-29 and 09-16) are fresh V4.1.1 scores.
- **36 N/A cells.** 36 minutes cells that a blind second pass scored N/A were set to N/A (24 EQUITY_VALUATION, 9 CREDIT_SPREADS, 3 others); each is logged with its old value. Use the N/A-adjusted values.
- **Scoring-vintage caveat.** The 2026 rows and the V4.1.1 re-scores were produced in October 2026. Re-scoring 44 unchanged transcripts on 2026-10-16/17 moved FINANCIAL_STABILITY_EMPHASIS by 6.0 points on average (lower), DISSENT_INTENSITY by 2.4 and UNCERTAINTY_EXPRESSED by 2.9 (CHANGELOG 1.3.0). Minutes and transcripts drift by similar amounts, so minutes-minus-transcripts gaps are largely unchanged, but levels of those three dimensions are not comparable between the 2026 rows and older rows.

All scorers are agents of one model family and no human coding exists, so no result here is an independent confirmation. Sign convention throughout this document: gaps are minutes minus transcripts, so a negative value means minutes score lower. See `codebooks/CODEBOOK_discussion_scores_v4_1.md`.

### 3.3 Why Evidence-Independent Scoring?

The original V3 batched scoring (not shipped; its files were removed in 2.0.0, see CHANGELOG) processed multiple documents sequentially using a single agent, allowing each document's scoring to be influenced by context from prior documents in the same batch. This introduced two distinct problems:

1. **Cross-meeting contamination**: Agents began referencing prior meetings in their reasoning chains. An independence audit found 260 cross-meeting contamination phrases in the old batched scoring runs and none in the reasoning text of the new independent runs (12 V4 files contain 26 references to other meetings, all quotations of source documents; a separate file-level scan flagged 84 of 266 old batched minutes files and 44 of 272 transcript files; scan scopes differ, see VALIDATION_REPORT.md Section 1).

2. **Artificial autocorrelation inflation**: Because agents "remembered" prior scores, sequential scores were more similar than the underlying economic conditions warranted. Under independent scoring, lag-1 autocorrelation decreased on the five staff dimensions reported in VALIDATION_REPORT.md Table 1.2 — for example, from 0.861 to 0.818 for FINANCIAL_CONDITIONS minutes, and from 0.977 to 0.947 for OUTPUT_GAP minutes.

3. **Inflated minutes-transcript bias**: An earlier batched-scoring figure of about +8 points (+8.1/+8.3) for the staff minutes-transcript gap was retracted as a scoring artifact and should not be used as a baseline. In `staff_scores_v6.csv` the FINANCIAL_CONDITIONS gap is -0.9 points (minutes minus transcripts; transcripts score higher; 213 of the 215 same-date pairs have both scores). The other staff gaps are also small (INFLATION_PRESSURE -2.2, OUTPUT_GAP -0.8, LABOR_TIGHTNESS -0.7, CONSUMPTION_INVESTMENT +0.3). The financial-conditions gap is small, rests on model scoring only, and has not been checked against human coding or separated from measurement differences between document types.

In the V4.1 discussion scoring, minutes score lower than transcripts by 8.3 points on DISSENT_INTENSITY, 13.3 on FINANCIAL_STABILITY_EMPHASIS and 5.0 on UNCERTAINTY_EXPRESSED (224 matched pairs, matched on the minutes meeting date and the transcript date; minutes minus transcripts). An earlier V3 discussion scoring, which is no longer shipped and whose figures are not restated here, gave gaps of the same sign and similar size, so the result is not an artifact of batching or of the earlier input defects. Both scorings use the same model family and the V4.1 minutes rows are mostly patches of earlier analyses, so this shows the result does not depend on those input defects, not that it is independent of the scoring method. It also does not show that the cause is editorial compression: nothing here separates it from differences in what the scorer can see in minutes (quantifier language) versus transcripts. Among the economic dimensions, OUTPUT_GAP shows no gap (0.0) and INFLATION_PRESSURE, CONSUMPTION_INVESTMENT and HAWKISH_DOVISH_LEAN small ones (-2.0, -1.5, -1.5); this is consistent with, but does not establish, the hypothesis that economic content is faithfully summarized while deliberative texture is compressed. See `codebooks/CODEBOOK_discussion_scores_v4_1.md`.

---

## 4. Method B: Sentence-Level Classification (CDFSG)

Method B classifies every sentence in the FOMC transcript and minutes corpus into a predefined policy-topic taxonomy, enabling direct measurement of topic-share differences between document types.

**What is classified**: Every sentence in the FOMC transcript and minutes documents, plus sentences from speeches and statements for the 2007–2009 crisis window. Total scale: 500,075 sentences across 440 dates (transcript 428,487; minutes 52,831; speech 18,544; statement 213). Transcripts run 1993–2020; the minutes in the corpus run to 2026-01-28 (the five 2026 meetings after that are scored in Method A but are not in the sentence corpus). The corpus was de-duplicated on 2026-10-17 (22,815 double-ingested rows removed) and the statements of 2007-06-28 and 2008-12-16 were added the same day.

**Taxonomy**: Each sentence is classified into one of five topics (FINANCIAL, EMPLOYMENT_OUTPUT, INFLATION, REGULATION_SUPERVISION, OTHER), and FINANCIAL sentences also receive a 1-5 stability intensity. The meeting-level aggregation (`compute_variables.py`) maps these to seven codes, referred to as the CDFSG taxonomy: FSS and FCS are split from FINANCIAL by stability intensity (3 or more versus 2 or less), and OTH and DMS are split from OTHER.

| Code | Category |
|------|----------|
| FSS | Financial Stability and Systemic Risk |
| FCS | Financial Conditions and Markets |
| INF | Inflation and Price Stability |
| EMP | Employment and Labor Markets |
| REG | Regulatory and Supervisory Matters |
| OTH | Other Economic Topics |
| DMS | Decision-Making and Meeting Structure |

**Key output**: The CDFSG index, defined as the financial stability topic share in transcripts minus the financial stability topic share in the corresponding minutes. A positive CDFSG index indicates that financial stability discussion is more prominent in the transcript than in the published minutes, consistent with editorial compression of this topic. In the data the sign is mostly the opposite: the minutes-based index (`CDFSG_minutes`, 215 meetings) has mean -0.1554 and is positive in only 14 meetings, so on average the minutes carry a larger financial-stability share than the transcripts. This sentence-share result does not support editorial compression of financial stability and runs against the direction of the Method A financial-stability-emphasis gap (Section 3.3); the two measures are not the same construct (topic share versus scored emphasis) and the difference has not been reconciled. The column named `CDFSG` in `meeting_variables.csv` is transcript minus statement and is populated for 17 meetings only (mean -0.0396).

**Classification approach**: Each sentence is classified at the sentence level using the CDFSG rubric. Most labels are presumed to come from an LLM agent, but **7,979 sentence labels (transcript 5,118, speech 2,448, minutes 413) match a keyword script, not an LLM judgement**; they are marked `keyword_script` in the `label_source` column of `classified_sentences.csv`. The other 492,096 rows are marked `llm_presumed`, which only means that no keyword-script evidence was found; it is not a verification that an LLM labelled them. `meeting_variables.csv` was computed with the keyword-labelled rows included and its CDFSG values were not re-estimated without them. The corpus mixes classifier vintages: when the speaker-turn tokenization was rebuilt (CHANGELOG 1.1.0), 96.6% of labels were carried forward by exact-text match and only 3.4% (13,732 sentences) were freshly classified. The sentence-level granularity makes this method structurally different from Method A's document-level scoring.

**Pilot validation**: Before full-corpus deployment, a 200-sentence pilot sample was independently classified by **two different language models** — a gold-standard annotator (Claude Opus 4.6, prompted as PI) and the bulk-scoring annotator (Claude Sonnet 4.6). The resulting **model-model** Cohen's kappa was 0.751 which would indicate substantial agreement. **This figure could not be reproduced**: the Sonnet labels are not shipped, and the closest recomputation from the shipped files (after merging the two financial categories) gives kappa 0.686 (77.5% raw agreement); without the merge the kappa is 0.416. The pilot used a first, six-category taxonomy, not the five-category scheme in the current corpus, so it is best read as a single un-reproduced figure. Note this is a second-model reproducibility check, **not** human validation: no human coder has labelled any portion of this corpus. See "Limitations" below.

**Coverage**: Transcript sentences cover 1993–2020 (constrained by transcript availability); minutes sentences run to 2026-01-28. 500,075 sentences, 440 dates (`meeting_variables.csv` has 440 rows).

---

## 5. Method C: FASTopic Topic Modeling

Method C uses unsupervised topic modeling to characterize the thematic content of FOMC documents and to provide an independent validation of Method A and B findings.

**Approach**: FASTopic (a neural topic model) is applied to seven corpora built from the minutes and transcripts: minutes, transcripts, minutes_decomposed (minutes split by section), transcripts_decomposed, staff_combined (staff review and briefing sections), staff_paragraphs and conference_calls. Statements, press conferences, testimonies and speeches are not topic-modeled. Each corpus is modeled independently, producing a set of topics with associated keyword distributions. BERTopic is run on the same sentences as a second model for robustness.

**Dimension mapping**: Discovered topics are mapped to 13 economic and financial categories. This mapping is performed post-hoc by inspection of topic keywords, using the investigator's own judgment to assign each topic to a substantive category (this is not independent coding). The mapped topic prevalence time series are then compared to Method A score time series and Method B sentence-share time series to assess cross-method convergence.

**Use in validation**: Method C is primarily used as an independent validation instrument rather than as a primary analytical method. The key convergence finding as reported in VALIDATION_REPORT.md is that the financial stress topic prevalence from FASTopic (Method C) correlates with the CDFSG financial stability index from Method B at Spearman rho = 0.587 [Unverified as of 2026-10-17: this correlation predates the 2026-10-17 corpus de-duplication and has not been recomputed] — a moderate correlation, consistent with both methods detecting related signals despite operating on different principles (unsupervised discovery vs. supervised classification). This is a robustness comparison on one dimension, not construct validation, and other financial pairs in the cross-method comparison do not converge (VALIDATION_REPORT.md Section 6). 

**Robustness to model choice.** In the cleaned re-run of 2026-10-07 (`data/topic_modeling/cross_method_matrix.csv`), FASTopic and BERTopic agree on the per-meeting ratio of economic to financial topic prevalence for minutes (Pearson r = 0.865, 265 meetings) and for the rebuilt staff-combined corpus (0.782, 312 meetings) but only moderately for transcripts (0.480, 225 meetings), which fails the project's r > 0.7 rule, so Method C results on transcripts should not be treated as robust to model choice. The cleaned figures reproduce from the saved per-meeting topic proportions; retraining the models was not tested. The BERTopic transcripts ratio is dominated by one catch-all cluster (53% of non-noise sentences, mapped to Treasury/Bond Markets); dropping it raises r to 0.742, and agreement is concentrated in 2008-2013 (r by period: 0.10 for 1993-99, 0.25 for 2000-07, 0.75 for 2008-13). Cross-corpus FASTopic agreement is moderate or weak: minutes vs transcripts 0.697 (215 meetings), transcripts vs staff-combined 0.700 (225; 0.6996) and minutes vs staff-combined 0.377 (257). The earlier February figures (minutes 0.916, staff 0.861, transcripts 0.13, decomposed transcripts 0.02, conference calls -0.44) are superseded. No cleaned comparison exists for minutes_decomposed, transcripts_decomposed, staff_paragraphs or conference_calls, and the staff comparison uses a new staff definition, so it is not like-for-like with February. A rerun of transcripts_decomposed on the rebuilt corpus is in progress and its results are not reported here. A correlation of a single ratio does not by itself validate topic quality.

---

## 6. Validation

Six validation procedures were applied to the scoring pipeline. Full documentation is in VALIDATION_REPORT.md; key results are summarized here.

**1. Independence audit**: Verified that independent scoring runs contain no cross-meeting contamination phrases in reasoning text (12 V4 files contain 26 source-document quotations that mention other meetings). Old batched scoring contained 260 such phrases in one scan and cross-meeting references in 32% of minutes files in another; scan scopes differ.

**2. Quality flags and corrections**: A cumulative validation pass assessed every scored dimension as VALID (±5 points of anchor), QUESTIONABLE (±6–12 points), or INCORRECT (>12 points or wrong direction). Across ~481 files, the distribution was ~73% VALID, ~22% QUESTIONABLE, ~5% INCORRECT at the dimension-check level. The INCORRECT dimension-scores were corrected in the original V4 run (564 individual corrections across 5 dimensions and 6 identified systematic errors); the correction log itself is no longer shipped (removed in 2.0.0), so these corrections cannot be inspected in this release.

**3. Staff minutes-transcript concordance (V4 independent)**: For meetings where both a minutes and a transcript are available and were scored, the correlation between minutes scores and transcript scores on the same dimension quantifies how consistently the V4 rubric scores equivalent content. Four core economic dimensions achieve r = 0.91–0.97 (INFLATION_PRESSURE 0.91, CONSUMPTION_INVESTMENT 0.93, OUTPUT_GAP 0.95, LABOR_TIGHTNESS 0.97) and FINANCIAL_CONDITIONS 0.83; PRODUCTIVITY is 0.80 on only 53 pairs (recomputed on the matched pairs in `data/primary/staff_scores_v6.csv`). Mean differences are within about 2.2 points (minutes minus transcripts), so the scores agree closely between document types. Both sets of scores come from the same model family; this is agreement, not evidence of accuracy.

**4. Reproducibility of the discussion scores (V4.1)**: 15 transcripts already scored under V4.1.1 were re-scored blind by fresh agents; the mean absolute difference over 223 scored pairs was 1.8 points on the 1–100 scale. A fresh blind score of 60 randomly drawn minutes differs from the published (patched) minutes values by a mean absolute 3.3 points, and a blind second pass by 3.8 (CHANGELOG 1.2.0). Re-scoring 44 unchanged transcripts in October 2026 shifted FINANCIAL_STABILITY_EMPHASIS, DISSENT_INTENSITY and UNCERTAINTY_EXPRESSED by 6.0, 2.4 and 2.9 points on average (Section 3.2.1). These are repeatability checks within one model family; they are not accuracy checks, and the 1.8 figure should not be read as the expected reproducibility of a new run.

**5. Inter-rater kappa (model-model)**: Two separate inter-rater exercises were conducted, **both entirely model-based**. (a) For rubric scoring: a 90-row annotation sample (30 excerpts × 3 annotator personas, which VALIDATION_REPORT.md Section 5.1 records as written in a single Claude session, so independence of the three sets is not established) tested 8 scoring dimensions; Cohen's kappa is reported as exceeding the 0.60 threshold (Shah et al. 2023) on all 8 dimensions, but the values are not shipped in this release. (b) For sentence classification: a 200-sentence pilot sample was reported as classified by two different models (Claude Opus 4.6 as PI vs. Claude Sonnet 4.6), with an overall model-model kappa of 0.751 that could not be reproduced (closest recomputation 0.686; the kappa for the financial-conditions versus financial-stability distinction is 0.416). These exercises establish that scoring is **reproducible across models and prompting configurations**; they do **not** establish alignment with human judgment, since no human annotator participated in either. The instrument designed for genuine human validation (`06_cdfsg_pipeline/validation/compute_reliability.py`, 486 lines, 2 coders × 500 sentences) has been written but never run — human coders were not recruited (the script is not part of this release).

**6. Cross-method convergence**: Method B financial stability index was correlated with Method C FASTopic financial stress topic prevalence (Spearman rho = 0.587), while the Method A (LLM scores) versus Method B (sentence index) correlation for financial stability is rho = 0.317, below the 0.50 threshold set in advance, and Method A versus C is 0.540 (VALIDATION_REPORT.md Section 6; computed from the original V4 staff scores and the February topic run, not recomputed). This partial convergence is consistent with two methods measuring related but not identical constructs; other Method A-versus-B comparisons also fail. All reliability figures in this section are model-versus-model or internal-consistency checks; no human annotator has labelled any part of this dataset.

---

## 7. Known Limitations

**LLM non-determinism**: LLM scoring with temperature > 0 is not fully reproducible in a strict computational sense. The rubrics, anchor meetings, and scored .md evidence files stored in the `scoring_evidence/` directory serve as the reproducibility mitigation strategy: they document the evidence basis for each score and allow human reviewers to assess and, if necessary, correct or re-score specific documents. The evidence files cover the discussion scores and the staff minutes rows; the staff transcript rows (re-scored on repaired text) have no shipped evidence files, and the staff v6 table is not the table the shipped staff evidence was written for.

**Sentence labels**: 7,979 of the 500,075 sentence labels are keyword-script labels, not LLM labels (Section 4), and the remaining labels are presumed, not confirmed, LLM labels. No human has checked any part of the corpus.

**Pre-2005 minutes format**: FOMC minutes published before approximately 2005 do not have clearly segmented staff and participant sections; the full meeting summary appears as a single unsegmented narrative. Section-level analyses (staff vs. discussion) rely on linguistic cues to identify staff-attributable vs. participant-attributable content in these older documents, which introduces additional uncertainty.

**Transcript coverage ceiling**: Transcripts are available only through 2020. Discussion scoring for post-2020 minutes has no transcript counterpart, so minutes-transcript gap analysis is restricted to the 1993–2020 period. The 2021–2026 minutes scores are available but can only be analyzed in isolation, and the 2026 rows were scored in a later scoring vintage (Section 3.2.1).

**CDFSG coverage ceiling**: Method B transcript sentences end in 2020, co-extensive with transcript availability, so the CDFSG index (transcript minus minutes share) exists only for 1993–2020. Minutes sentences in the corpus run to 2026-01-28 and have no transcript counterpart after 2020.

**Greenbook vs. Tealbook transition**: The staff economic forecast document was renamed from Greenbook to Tealbook in 2010. The meeting documents reflect this terminology change; the scoring rubric is designed to handle both, but earlier and later documents may have somewhat different structures for staff presentations.

**Multi-day meeting dating**: Document-name dates differ by one day for some two-day meetings. In the registry (`data/primary/meeting_registry.csv`), `meeting_date` is the document-name date: the last day for 162 of the 176 meetings with a two-day span and the first day for the other 14 (ten scheduled meetings: eight in 1996-99, 2003-09-15 and 2012-10-23; three 2008 conference calls; and the 2020-03-02 emergency meeting). `start_date` and `end_date` give the span. `data/derived/meeting_key_map.csv` maps every score-table date key to a registry meeting, and matching minutes to transcripts through it, rather than by identical date strings, gives 224 pairs instead of 215. The `special_notes` field (15 rows) records conference-call and emergency events, not date discrepancies.

---

*For data lineage, file checksums, and version history, see DATA_PROVENANCE.md.*
*For full validation evidence and QC reports, see VALIDATION_REPORT.md.*

---

## References

Cieslak, A., & Vissing-Jorgensen, A. (2021). The economics of the Fed put. *Review of Financial Studies*, 34(9), 4045–4089.

Hansen, S., McMahon, M., & Prat, A. (2018). Transparency and deliberation within the FOMC: A computational linguistics approach. *Quarterly Journal of Economics*, 133(2), 801–870.

Shah, P., Hovy, E., & Corston-Oliver, S. (2023). Evaluation of automated text annotation: A survey of best practices. *Computational Linguistics*, 49(1), 159–200.
