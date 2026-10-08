# FOMC Document Scoring: Methodology

**Dataset version**: 2026-03
**Last updated**: 2026-03-30
**Scope**: FOMC minutes (1993–2026) and transcripts (1993–2020)

---

## 1. Overview

This dataset addresses a fundamental question in central bank communication research: do FOMC minutes systematically compress information relative to the underlying transcripts on which they are based? The minutes are an edited institutional document published approximately three weeks after each meeting; the transcripts are a verbatim record released with a five-year lag. If the editing process introduces systematic patterns — suppressing dissent, downplaying financial stability concerns, moderating expressed uncertainty — then the minutes present a filtered representation of Committee deliberations rather than a faithful summary.

The research is motivated by an unresolved debate about whether the Federal Reserve treats financial stability as an implicit third mandate alongside its statutory dual mandate of maximum employment and stable prices. As Cieslak and Vissing-Jorgensen (2021) observe, "we lack direct evidence on what weight the Fed places on different objectives." This dataset provides such evidence by measuring how FOMC documents characterize economic and financial conditions, how attention is allocated across policy concerns, and where the public minutes diverge from the internal deliberative record.

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

**Coverage in this dataset**: 273 meetings with transcripts, spanning February 1993 through December 2020. Transcripts for meetings after 2020 are not yet publicly available due to the five-year declassification lag.

### 2.2 FOMC Minutes

FOMC meeting minutes are published approximately three weeks after each meeting. They are institutional summaries prepared by Board staff and approved by the Committee. They present synthesized descriptions of staff briefings and participant discussions using quantifier language ("most participants," "several members," "a few noted") rather than attributing views to individual members.

**Coverage in this dataset**: 265 scored minutes, spanning 1993–2026 (266 minutes files were scored; one was a duplicate copy of the 2012-10-23 minutes and its row was removed, see CHANGELOG 1.1.0).

### 2.3 Supplementary Sources

The raw document corpus also includes FOMC statements (241 documents), press conference transcripts (90), congressional testimonies (62), and Federal Reserve speeches (approximately 2,886). These are used in Method C topic modeling but are not the primary focus of Methods A and B.

### 2.4 Access and Rights

All documents are products of the United States federal government and are in the public domain. No licensing restrictions apply to the source documents. The scoring data, rubrics, and derived datasets produced by this project are released under CC-BY 4.0 unless otherwise specified.

---

## 3. Method A: LLM Rubric Scoring

Method A uses large language model (LLM) agents to score FOMC documents against structured rubrics on a set of continuous economic and policy dimensions. Two separate rubrics are applied to two distinct aspects of each meeting: the staff assessment and the participant discussion.

### 3.1 Staff Assessment Scoring (V4)

**What is scored**: The staff's assessment of economic and financial conditions as presented in Greenbook/Tealbook materials and reflected in meeting documents. For transcripts, this is the economic and financial briefing section; for minutes, it is the synthesized staff-report language ("the staff reported," "the Tealbook projection," "in the staff's assessment").

**Scoring instrument**: The V4 Staff Assessment Rubric scores 15 dimensions on a continuous 1–100 scale, where 50 represents a neutral baseline. The dimensions are organized into three tiers:

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

**Evidence independence mandate**: The rubric's operative instruction is: "Score this document as if it is the only FOMC document you have ever seen. Do not reference, compare to, or recall scores from any other meeting." One fresh LLM agent is instantiated per document with no prior meeting context. This independence mandate is the defining methodological difference between V4 (canonical) and the superseded V3 batched scoring.

### 3.2 Participant Discussion Scoring (V3 Independent)

**What is scored**: The center-of-gravity of participant views in the discussion sections of each meeting. For transcripts, this is the go-around and policy discussion; for minutes, it is the synthesized participant-view language using quantifier expressions.

**Scoring instrument**: The V3 Discussion Rubric scores 10 core dimensions plus up to 10 supplementary dimensions activated when a topic receives substantive discussion from two or more participants. Core dimensions:

- *Economic conditions* (4): INFLATION_PRESSURE, OUTPUT_GAP, LABOR_TIGHTNESS, CONSUMPTION_INVESTMENT
- *Financial and policy* (6): FINANCIAL_TIGHTNESS, HAWKISH_DOVISH_LEAN, DISSENT_INTENSITY, FINANCIAL_STABILITY_EMPHASIS, FORWARD_GUIDANCE_TONE, UNCERTAINTY_EXPRESSED

A key interpretive rule distinguishes the discussion rubric from the staff rubric: uncertainty bands in the discussion rubric reflect the *range of participant views*, not scorer confidence. Narrow uncertainty (±3–5) indicates broad Committee agreement; wide uncertainty (±10–15) indicates substantially dispersed views.

**Applied symmetrically**: The V3 Discussion Rubric is applied independently to all 266 minutes and all 273 transcripts. For the 266 meetings where both document types are available, the paired scoring design enables direct minutes-transcript comparison: both documents are scored against the same rubric by independent agents, and gaps in scores are attributable to differences in document content rather than differences in scoring approach.

**Evidence independence mandate**: Identical to staff scoring — one fresh agent per document, no shared context, no batching.

### 3.3 Why Evidence-Independent Scoring?

The original V3 batched staff scoring (archived in `data/legacy/`) processed multiple documents sequentially using a single agent, allowing each document's scoring to be influenced by context from prior documents in the same batch. This introduced two distinct problems:

1. **Cross-meeting contamination**: Agents began referencing prior meetings in their reasoning chains. An independence audit found 260 contamination phrases in the old batched scoring runs and zero in the new independent scoring runs.

2. **Artificial autocorrelation inflation**: Because agents "remembered" prior scores, sequential scores were more similar than the underlying economic conditions warranted. Under independent scoring, lag-1 autocorrelation decreased across all measured dimensions — for example, from 0.861 to 0.818 for FINANCIAL_CONDITIONS minutes, and from 0.977 to 0.947 for OUTPUT_GAP minutes.

3. **Inflated minutes-transcript bias**: The old batched staff scoring showed a mean gap of +8.1 points (minutes scored higher than transcripts on average). Under independent scoring, this dropped to +1.7 points — a 79% reduction. The old gap was largely a scoring artifact rather than a real editorial effect.

The robustness of the key minutes-transcript findings under independent scoring is itself informative. The three gaps in participant discussion (DISSENT_INTENSITY: −9.7 points, FINANCIAL_STABILITY_EMPHASIS: −11.3 points, UNCERTAINTY_EXPRESSED: −5.2 points) all *strengthened* under independent scoring, confirming they reflect genuine editorial compression in the minutes rather than scoring artifacts. The economic dimensions (INFLATION_PRESSURE, OUTPUT_GAP, CONSUMPTION_INVESTMENT, HAWKISH_DOVISH_LEAN) showed near-zero gaps in both scoring approaches, consistent with the hypothesis that economic content is faithfully summarized while deliberative texture is compressed.

---

## 4. Method B: Sentence-Level Classification (CDFSG)

Method B classifies every sentence in the FOMC transcript and minutes corpus into a predefined policy-topic taxonomy, enabling direct measurement of topic-share differences between document types.

**What is classified**: Every sentence in every FOMC transcript and minutes document from 1993 to 2020. Total scale: approximately 394,000 sentences across 394 meetings.

**Taxonomy**: Seven categories are used, referred to as the CDFSG taxonomy:

| Code | Category |
|------|----------|
| FSS | Financial Stability and Systemic Risk |
| FCS | Financial Conditions and Markets |
| INF | Inflation and Price Stability |
| EMP | Employment and Labor Markets |
| REG | Regulatory and Supervisory Matters |
| OTH | Other Economic Topics |
| DMS | Decision-Making and Meeting Structure |

**Key output**: The CDFSG index, defined as the financial stability topic share in transcripts minus the financial stability topic share in the corresponding minutes. A positive CDFSG index indicates that financial stability discussion is more prominent in the transcript than in the published minutes, consistent with editorial compression of this topic.

**Classification approach**: Each sentence is classified by an LLM agent using the CDFSG rubric. The classifier is applied to each meeting's full document set (transcript and minutes) as a batch, but classification decisions are made at the sentence level independently. The sentence-level granularity makes this method structurally different from Method A's document-level scoring.

**Pilot validation**: Before full-corpus deployment, a 200-sentence pilot sample was independently classified by **two different language models** — a gold-standard annotator (Claude Opus 4.6, prompted as PI) and the bulk-scoring annotator (Claude Sonnet 4.6). The resulting **model-model** Cohen's kappa was 0.751, indicating substantial agreement and that the taxonomy is applied consistently across models. Note this is a second-model reproducibility check, **not** human validation: no human coder has labelled any portion of this corpus. See "Limitations" below.

**Coverage**: 1993–2020 only (constrained by transcript availability). 394 meetings, approximately 394,000 sentences classified.

---

## 5. Method C: FASTopic Topic Modeling

Method C uses unsupervised topic modeling to characterize the thematic content of FOMC documents and to provide an independent validation of Method A and B findings.

**Approach**: FASTopic (a neural topic model) is applied to seven distinct FOMC document corpora: minutes, transcripts (staff section), transcripts (discussion section), statements, press conference transcripts, testimonies, and speeches. Each corpus is modeled independently, producing a set of topics with associated keyword distributions.

**Dimension mapping**: Discovered topics are mapped to 13 economic and financial categories. This mapping is performed post-hoc by inspection of topic keywords, using human judgment to assign each topic to a substantive category. The mapped topic prevalence time series are then compared to Method A score time series and Method B sentence-share time series to assess cross-method convergence.

**Use in validation**: Method C is primarily used as an independent validation instrument rather than as a primary analytical method. The key convergence finding is that the financial stress topic prevalence from FASTopic (Method C) correlates with the CDFSG financial stability index from Method B at Spearman rho = 0.587 — a moderate correlation confirming that both methods detect the same underlying signal, despite operating on entirely different principles (unsupervised discovery vs. supervised classification).

---

## 6. Validation

Six validation procedures were applied to the scoring pipeline. Full documentation is in VALIDATION_REPORT.md; key results are summarized here.

**1. Independence audit**: Verified that independent scoring runs contain zero cross-meeting contamination phrases. Old batched scoring contained 260 such phrases across scoring runs; the independent approach eliminates all of them by design.

**2. Quality flags and corrections**: A cumulative validation pass assessed every scored dimension as VALID (±5 points of anchor), QUESTIONABLE (±6–12 points), or INCORRECT (>12 points or wrong direction). Across ~481 files, the distribution was ~73% VALID, ~22% QUESTIONABLE, ~5% INCORRECT at the dimension-check level. All INCORRECT dimension-scores were corrected; 564 individual corrections were logged across 5 dimensions and 6 identified systematic errors. All corrections are documented in the correction log.

**3. Staff minutes-transcript concordance (V4 independent)**: For meetings where both a minutes and a transcript are available and were scored, the correlation between minutes scores and transcript scores on the same dimension quantifies how consistently the V4 rubric scores equivalent content. Core economic dimensions achieve r = 0.925–0.977 with near-zero bias, confirming that the rubric applies consistently across document types.

**4. Discussion V3 independent validation audit**: Sixteen documents were independently re-scored to assess intra-method reproducibility. The mean absolute deviation across re-scored dimensions was 1.9 points on the 1–100 scale, and no direction errors (a score crossing the 50 neutral point in opposite directions) were observed.

**5. Inter-rater kappa (model-model)**: Two separate inter-rater exercises were conducted, **both entirely model-based**. (a) For rubric scoring: a 90-row annotation sample (30 excerpts × 3 annotators — Claude Opus 4.6 agents prompted to role-play trained annotators, with no score memory across excerpts) tested 8 scoring dimensions; Cohen's kappa exceeded the 0.60 threshold (Shah et al. 2023) on all 8 dimensions. (b) For sentence classification: a 200-sentence pilot sample was classified by two different models (Claude Opus 4.6 as PI vs. Claude Sonnet 4.6), yielding a model-model kappa of 0.751 for the financial stability category. These exercises establish that scoring is **reproducible across models and prompting configurations**; they do **not** establish alignment with human judgment, since no human annotator participated in either. The instrument designed for genuine human validation (`06_cdfsg_pipeline/validation/compute_reliability.py`, 486 lines, 2 coders × 500 sentences) has been written but never run — human coders were not recruited.

**6. Cross-method convergence**: Method B financial stability index was correlated with Method C FASTopic financial stress topic prevalence (Spearman rho = 0.587). This partial convergence is the expected outcome for two methods measuring related but not identical constructs; full convergence would indicate redundancy rather than independent triangulation.

---

## 7. Known Limitations

**LLM non-determinism**: LLM scoring with temperature > 0 is not fully reproducible in a strict computational sense. The rubrics, anchor meetings, and scored .md evidence files stored in the `scoring_evidence/` directory serve as the reproducibility mitigation strategy: they document the evidence basis for each score and allow human reviewers to assess and, if necessary, correct or re-score specific documents.

**Pre-2005 minutes format**: FOMC minutes published before approximately 2005 do not have clearly segmented staff and participant sections; the full meeting summary appears as a single unsegmented narrative. Section-level analyses (staff vs. discussion) rely on linguistic cues to identify staff-attributable vs. participant-attributable content in these older documents, which introduces additional uncertainty.

**Transcript coverage ceiling**: Transcripts are available only through 2020. Discussion scoring for post-2020 minutes has no transcript counterpart, so minutes-transcript gap analysis is restricted to the 1993–2020 period. The 2021–2026 minutes scores are available but can only be analyzed in isolation.

**CDFSG coverage ceiling**: Method B sentence-level classification covers 1993–2020 only, co-extensive with transcript availability. The post-2020 period is not represented in CDFSG outputs.

**Greenbook vs. Tealbook transition**: The staff economic forecast document was renamed from Greenbook to Tealbook in 2010. The meeting documents reflect this terminology change; the scoring rubric is designed to handle both, but earlier and later documents may have somewhat different structures for staff presentations.

**Multi-day meeting dating**: Nine multi-day FOMC meetings have a one-day discrepancy between the date used for minutes (first day) and transcripts (last day) in the registry. These meetings are flagged in the meeting registry with a `special_notes` entry.

---

*For data lineage, file checksums, and version history, see DATA_PROVENANCE.md.*
*For full validation evidence and QC reports, see VALIDATION_REPORT.md.*

---

## References

Cieslak, A., & Vissing-Jorgensen, A. (2021). The economics of the Fed put. *Review of Financial Studies*, 34(9), 4045–4089.

Hansen, S., McMahon, M., & Prat, A. (2018). Transparency and deliberation within the FOMC: A computational linguistics approach. *Quarterly Journal of Economics*, 133(2), 801–870.

Shah, P., Hovy, E., & Corston-Oliver, S. (2023). Evaluation of automated text annotation: A survey of best practices. *Computational Linguistics*, 49(1), 159–200.
