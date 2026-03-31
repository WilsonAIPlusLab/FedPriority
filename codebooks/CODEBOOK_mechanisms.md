---
title: Codebook — Master Mechanisms File
version: 1.0
created: 2026-03-30
---

## Overview

This codebook covers `master_mechanisms.csv`, the primary analytical dataset for studying editorial compression in FOMC communication. The file contains meeting-level rubric scores and qualitative mechanism labels produced by comparing verbatim FOMC meeting transcripts against the corresponding published meeting minutes. For each meeting, an LLM-based scorer applies structured rubrics to both documents independently and records the gap scores and the specific compression mechanisms observed.

The research purpose is to document how — not merely whether — the FOMC's published minutes systematically differ from the underlying discussion. Three substantive dimensions are scored: dissent and disagreement, financial stability emphasis, and expressed uncertainty. For each dimension the file records a gap score (transcript minus minutes), the specific editorial mechanisms producing the gap, and qualitative evidence including vocabulary terms and a one-sentence description of the most consequential omission.

## Unit of Observation

One row per FOMC meeting with minutes-versus-transcript comparison data. The dataset covers 216 meetings for which both a verbatim transcript and a published set of minutes are available, spanning 1993 through 2020.

---

## Variable Definitions

| Variable | Type | Valid Values | Description |
|----------|------|-------------|-------------|
| DATE | date | YYYY-MM-DD | Meeting date. Primary key. |
| CHAIR | string | Greenspan, Bernanke, Yellen, Powell | Federal Reserve Chair presiding over the meeting. |
| REGIME | categorical | calm, pre-crisis, crisis, recovery | Economic regime classification. See definitions below. |
| DISSENT_GAP | integer | unconstrained | Transcript DISSENT_INTENSITY rubric score minus the corresponding minutes score. Positive values indicate the transcript records more dissent or disagreement than the published minutes. |
| DISSENT_MECHANISMS | string | semicolon-separated codes | One or more compression mechanisms that explain the DISSENT_GAP. Codes are drawn from the Dissent Mechanism Taxonomy below. Multiple mechanisms are separated by semicolons. Set to `NONE` when no compression is observed. |
| NAMED_DISSENTERS_TRANSCRIPT | integer | ≥ 0 | Count of FOMC participants individually named in the transcript as expressing dissent or strong opposition to the policy decision or economic outlook. |
| NAMED_IN_MINUTES | integer | ≥ 0 | Count of individually named dissenters in the published minutes. Almost always 0; the minutes convention is to anonymize individual positions. |
| CONSENSUS_MANUFACTURING | categorical | NONE, MILD, STRONG | Degree to which the minutes editorially construct an appearance of consensus that is not present in the transcript. NONE = no evidence of artificial consensus; MILD = some smoothing of disagreement; STRONG = substantial disagreement converted to apparent agreement. |
| FSE_GAP | integer | unconstrained | Transcript FSE (Financial Stability Emphasis) rubric score minus the corresponding minutes score. Positive values indicate the transcript contains substantially more financial stability discussion than the published minutes. This is the rubric-based analogue to `CDFSG` in `meeting_variables.csv`. |
| FSE_MECHANISMS | string | semicolon-separated codes | One or more compression mechanisms explaining the FSE_GAP. Drawn from the FSE Mechanism Taxonomy below. Set to `NONE` when no compression is observed. |
| FSE_PARTICIPANTS | integer | ≥ 0 | Estimated count of distinct FOMC participants who discussed financial stability topics in the transcript. |
| FSE_MINUTES_SENTENCES | integer | ≥ 0 | Estimated count of sentences in the published minutes that address financial stability. Provides a baseline for the denominator of FSE coverage in the minutes. |
| FORESHADOWING | categorical | YES, NO | Whether the transcript contained early-warning content — specific signals of emerging financial risk — that was compressed away in the published minutes. YES indicates foreshadowing language present in the transcript is absent or substantially weakened in the minutes. |
| UNCERTAINTY_GAP | integer | unconstrained | Transcript UNCERTAINTY_EXPRESSED rubric score minus the corresponding minutes score. Positive values indicate the transcript records more genuine uncertainty among participants than the published minutes convey. Negative values indicate the minutes amplify uncertainty language relative to the underlying discussion. |
| UNCERTAINTY_MECHANISMS | string | semicolon-separated codes | One or more compression mechanisms explaining the UNCERTAINTY_GAP. Drawn from the Uncertainty Mechanism Taxonomy below. Set to `NONE` when no compression is observed. |
| META_UNCERTAINTY | categorical | YES, NO | Whether participants expressed second-order (model) uncertainty in the transcript — uncertainty about the reliability of their own analytical frameworks or forecasting models — as distinct from first-order uncertainty about economic outcomes. |
| CONFIDENCE_PROJECTION | categorical | YES, NO | Whether the published minutes inserted language expressing confidence or certainty that is not present in or supported by the underlying transcript discussion. Distinct from mere softening; this captures active addition of confident framing. |
| REASSURANCE_INSERTED | categorical | YES, NO | Whether the published minutes added reassuring language — calming assessments, positive forward guidance, or stability affirmations — that is absent from the transcript. |
| VOCABULARY_FILTERED | string | free text | Description of specific strong or vivid vocabulary terms used in the transcript that are absent from the published minutes. Provides qualitative evidence of the lexical dimension of compression. Set to `none identified` when no notable vocabulary filtering is observed. |
| MOST_CONSEQUENTIAL_OMISSION | string | free text | One-sentence description of the single most important piece of content present in the transcript that is absent from or substantially weakened in the published minutes. Captures the substantive significance of compression beyond the quantitative gap scores. |

### Regime Definitions

| Code | Label | Description |
|------|-------|-------------|
| calm | Stable non-crisis | Periods of normal macroeconomic and financial conditions with no acute stress. |
| pre-crisis | Pre-crisis lead-up | The 2006–2008 period leading into the Global Financial Crisis, characterized by emerging financial imbalances not yet at acute stress levels. |
| crisis | Acute crisis | Periods of acute economic or financial stress: the 2001 recession, the 2007–2009 Global Financial Crisis, and the 2020 COVID-19 shock. |
| recovery | Post-crisis expansion | Post-crisis recovery periods characterized by below-trend growth and unconventional policy but no acute stress. |

---

## Compression Mechanism Taxonomy

The following taxonomies define all valid codes that appear in the `DISSENT_MECHANISMS`, `FSE_MECHANISMS`, and `UNCERTAINTY_MECHANISMS` columns. Multiple mechanisms may co-occur within a single meeting.

### Dissent Mechanisms

| Code | Name | Definition |
|------|------|------------|
| ANONYMIZATION | Anonymization | A named dissenter or named group of dissenters in the transcript is converted to an anonymous collective ("some participants", "a few members") in the published minutes, eliminating individual attribution. |
| QUANTIFIER_DOWNGRADE | Quantifier downgrade | The quantifier describing the size of a dissenting group is reduced in the minutes: "many" becomes "some", "most" becomes "a few", or a specific count is replaced with a vague qualifier implying a smaller group. |
| QUASI_DISSENT_OMISSION | Quasi-dissent omission | A position that constitutes visible dissent or strong alternative advocacy in the transcript is entirely absent from the published minutes, with no mention even in anonymized form. |
| REFRAME_AS_UNCERTAINTY | Reframe as uncertainty | Dissent — a participant preferring a different policy path — is reframed in the minutes as general uncertainty about the outlook rather than as a substantive policy disagreement. |
| VOTE_DISCUSSION_GAP | Vote-discussion gap | The minutes record a formal dissenting vote but omit or substantially compress the substantive discussion and reasoning behind that dissent as it appeared in the transcript. |

### Financial Stability Emphasis (FSE) Mechanisms

| Code | Name | Definition |
|------|------|------------|
| TOPIC_OMISSION | Topic omission | An entire financial stability topic discussed by multiple transcript participants is absent from the published minutes. |
| SPECIFICITY_STRIPPING | Specificity stripping | Specific financial instruments, institutions, market segments, or mechanisms named in the transcript are replaced with generic language ("financial conditions", "credit markets") in the minutes. |
| MECHANISM_STRIPPING | Mechanism stripping | Causal chains, feedback loops, or transmission mechanisms articulated in the transcript are omitted from the minutes, which retain only the conclusion. |
| INTENSITY_REDUCTION | Intensity reduction | The severity or urgency of financial stability concerns is reduced: strong language ("severe", "alarming", "systemic") is replaced with mild language ("some concerns", "developments were monitored"). |
| SESSION_ERASURE | Session erasure | Financial stability discussion concentrated in one session of a two-day meeting (typically FOMC1) is absent from the minutes, which present a single undifferentiated record. |

### Uncertainty Mechanisms

| Code | Name | Definition |
|------|------|------------|
| MODIFIER_SOFTENING | Modifier softening | Hedging language in the transcript is either added around confident statements in the minutes, or — more commonly — strong hedging language in the transcript is weakened in the minutes. |
| EPISTEMIC_LAUNDERING | Epistemic laundering | Genuine expressed uncertainty in the transcript — "we don't know", "we are uncertain", "our models may be wrong" — is converted in the minutes to a confident or resolved framing that does not reflect the underlying discussion. |
| CONFIDENCE_PROJECTION | Confidence projection | The minutes assert confidence or certainty about the economic outlook or policy path that is not present in the transcript. Distinguished from EPISTEMIC_LAUNDERING by being an active addition rather than a conversion of existing language. |
| CONDITIONAL_INSERTION | Conditional insertion | Conditional qualifications are added in the minutes to statements that were made unconditionally in the transcript, or unconditional confidence is inserted where the transcript was conditional. |

---

## Notes on Missing Values

- All 20 columns are populated for every row; there are no structurally missing values in this file.
- `DISSENT_MECHANISMS`, `FSE_MECHANISMS`, and `UNCERTAINTY_MECHANISMS` are set to `NONE` (not blank) when no compression mechanism is identified for that dimension.
- `VOCABULARY_FILTERED` is set to the string `none identified` (not blank) when no filtered vocabulary is documented.
- Integer gap scores (`DISSENT_GAP`, `FSE_GAP`, `UNCERTAINTY_GAP`) may be negative; negative values indicate the minutes show higher scores on the relevant dimension than the transcript, which can occur in some uncertainty and financial conditions dimensions.
- `NAMED_IN_MINUTES` is almost always 0 due to the FOMC's standard practice of not individually attributing positions in published minutes. Non-zero values occur only when a formal dissenting vote is recorded (which minutes do name).

---

## Related Files

| File | Relationship |
|------|-------------|
| `data/sentence_classification/meeting_variables.csv` | Sentence-classification-based meeting-level aggregates. `CDFSG` is the sentence-level counterpart to `FSE_GAP` here. |
| `codebooks/CODEBOOK_sentence_classification.md` | Codebook for classified_sentences.csv and meeting_variables.csv. Includes full definition of CDFSG and topic taxonomy. |
| `rubrics/sentence_classification_prompt_v2.txt` | The V2 classifier prompt whose output underlies the CDFSG index in meeting_variables.csv. |
| `scoring_evidence/` | Directory containing the raw LLM scoring outputs and evidence excerpts used to construct the gap scores and mechanism labels in this file. |
