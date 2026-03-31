---
title: Codebook — Sentence Classification Files
version: 1.0
created: 2026-03-30
---

## Overview

This codebook covers two related files produced by the FOMC sentence-classification pipeline. The pipeline applies a large-language-model classifier (prompt version 2; see `rubrics/sentence_classification_prompt_v2.txt`) to every sentence drawn from FOMC meeting transcripts, published meeting minutes, post-meeting statements, and selected Fed speeches spanning 394 meetings from February 1993 through December 2020.

The primary research purpose is to measure how financial-stability emphasis varies across document types — in particular, whether FOMC transcripts devote systematically more attention to financial-stability concerns than the corresponding published minutes. The sentence-level classifications support the construction of the CDFSG composite index, which captures this emphasis gap, and enable cross-method triangulation against the rubric-based discussion scoring in `master_mechanisms.csv`.

## Unit of Observation

**classified_sentences.csv** — one row per sentence (~394,000 total rows). Each row represents a single classified sentence extracted from one of four document types associated with a specific FOMC meeting date.

**meeting_variables.csv** — one row per FOMC meeting (394 total rows). Each row aggregates the sentence-level classifications for all documents associated with that meeting date.

---

## Variable Definitions — classified_sentences.csv

| Variable | Type | Valid Values | Description |
|----------|------|-------------|-------------|
| sentence_id | string | S000001 … S999999 | Unique sentence identifier, zero-padded to 6 digits, assigned in corpus order. |
| meeting_date | date | YYYY-MM-DD | Date of the FOMC meeting with which this document is associated. |
| doc_type | categorical | transcript, minutes, statement, speech | Document source. `transcript` = verbatim meeting transcript; `minutes` = published FOMC minutes; `statement` = post-meeting press statement; `speech` = Fed official speech. |
| section | categorical | FOMC1, FOMC2, (others) | Meeting session or document section. `FOMC1` = first day of a two-day meeting; `FOMC2` = second day. May be blank or a section label for minutes and statements. |
| speaker | string | Surname or UNKNOWN | Speaker surname for transcript sentences. Set to the document's primary attributed author for speeches. Empty or NA for minutes and statements, which are not attributed to individual speakers. |
| speaker_role | categorical | Chair, Vice Chair, Governor, President, Staff, OTHER, (blank) | Role of the speaker at the time of the meeting. Blank for minutes and statements. |
| text | string | free text | The verbatim sentence text as extracted from the source document. |
| word_count | integer | ≥ 1 | Number of whitespace-delimited tokens in `text`. |
| speech_title | string | free text or (blank) | Title of the speech, for rows where `doc_type = speech`. Blank for all other document types. |
| speech_venue | string | free text or (blank) | Venue or occasion of the speech, for rows where `doc_type = speech`. Blank for all other document types. |
| topic | categorical | See below | CDFSG 7-category topic assigned by the sentence classifier. One category is assigned per sentence. |
| stability_intensity | integer | 1 – 5 or (blank) | Financial stability concern intensity score. Assigned only when `topic = FSS`; blank for all other topics. See intensity scale below. |
| confidence | categorical | HIGH, MEDIUM, LOW | Classifier self-reported confidence in the topic assignment. |

### Topic Category Definitions

The classifier uses a 7-category taxonomy derived from the five categories in the V2 prompt. The prompt's `FINANCIAL` category is post-hoc split into two codes based on the `stability_intensity` score:

| Code | Label | Description |
|------|-------|-------------|
| FSS | Financial Stability / Stress | Financial markets, institutions, or instruments discussed as a stability concern in their own right. Covers systemic risk, contagion, bank failures, leverage cycles, fire sales, too-big-to-fail, financial fragility, and acute stress episodes. Corresponds to `stability_intensity` 3 – 5 in the prompt. |
| FCS | Financial Conditions / Stance | Financial variables discussed primarily as a transmission channel to the real economy — credit conditions affecting investment, lending standards affecting spending, interest-rate pass-through, wealth effects. Corresponds to `stability_intensity` 1 – 2 in the prompt. |
| INF | Inflation | Price stability, inflation expectations, inflation dynamics, deflation risk, inflation targeting, commodity prices affecting consumer prices, PCE/CPI movements, Phillips curve, wage-price dynamics. |
| EMP | Employment / Output | Labor markets, unemployment, output gaps, GDP growth, recession risk, productivity, business investment, consumer spending, aggregate demand and supply. |
| REG | Regulation / Supervision | Prudential regulation, supervisory tools, macroprudential policy, stress tests, capital requirements, Basel standards, bank examination, regulatory rules. |
| OTH | Other / General | International economy (trade, exchange rates, foreign growth), fiscal policy, payment systems, procedural or administrative content, Fed operations, boilerplate statements, bibliographic references, or genuinely unclassifiable sentences. |
| DMS | Decision-Making / Structure | Committee process, vote mechanics, procedural discussions about how the FOMC reaches decisions, meeting administration. |

Note: The classifier prompt (V2) uses `FINANCIAL`, `INFLATION`, `EMPLOYMENT_OUTPUT`, `REGULATION_SUPERVISION`, and `OTHER` as output labels. The `FINANCIAL` label is mapped to `FSS` or `FCS` in post-processing based on whether `stability_intensity` is ≥ 3 (FSS) or ≤ 2 (FCS). `EMPLOYMENT_OUTPUT` is stored as `EMP`; `REGULATION_SUPERVISION` as `REG`; `OTHER` and `DMS` are assigned during post-processing.

### Stability Intensity Scale (FSS / FCS sentences only)

| Score | Label | Description |
|-------|-------|-------------|
| 1 | Pure transmission channel | Financial variable discussed solely for its effect on inflation or employment. Example: "Lower mortgage rates were expected to support household spending." |
| 2 | Mostly transmission, minor stability undertone | Transmission channel is primary; a secondary stability concern is present but not the focus. |
| 3 | Mixed | Both a stability concern and a transmission channel are evident in the sentence. |
| 4 | Mostly stability concern | Financial system health is the primary frame; some real-economy framing is present. |
| 5 | Pure stability concern | Financial system health discussed as an independent concern, regardless of effects on inflation or employment. Example: "The failure of Bear Stearns highlighted vulnerabilities in the triparty repo market." |

---

## Variable Definitions — meeting_variables.csv

| Variable | Type | Valid Values | Description |
|----------|------|-------------|-------------|
| meeting_date | date | YYYY-MM-DD | FOMC meeting date. Primary key. |
| n_transcript | integer | ≥ 0 | Total sentence count from the meeting transcript. Zero if no transcript is available for this meeting. |
| n_minutes | integer | ≥ 0 | Total sentence count from the published meeting minutes. |
| n_statement | integer | ≥ 0 | Total sentence count from the post-meeting press statement. Zero if no statement was released. |
| n_speech | integer | ≥ 0 | Total sentence count from Fed speeches associated with this meeting date. Zero if no speeches are linked. |
| n_FOMC1 | integer | ≥ 0 | Sentence count from the first day (FOMC1 section) of the transcript. Zero for single-day meetings or if `section` coding is unavailable. |
| n_FOMC2 | integer | ≥ 0 | Sentence count from the second day (FOMC2 section) of the transcript. Zero for single-day meetings. |
| {TOPIC}_transcript | float | 0 – 1 | Share of transcript sentences classified as `{TOPIC}`. Computed as (count of transcript sentences with topic = TOPIC) / n_transcript. Zero if n_transcript = 0. `{TOPIC}` takes each of the seven values: FSS, FCS, INF, EMP, REG, OTH, DMS. |
| {TOPIC}_minutes | float | 0 – 1 | Share of minutes sentences classified as `{TOPIC}`. Computed analogously using n_minutes as denominator. |
| {TOPIC}_statement | float | 0 – 1 | Share of statement sentences classified as `{TOPIC}`. Blank if n_statement = 0. |
| {TOPIC}_speech | float | 0 – 1 | Share of speech sentences classified as `{TOPIC}`. Blank if n_speech = 0. |
| FSS_FOMC1 | float | 0 – 1 | Share of FOMC1 transcript sentences classified as FSS. Blank if session-level section coding is unavailable. |
| FSS_FOMC2 | float | 0 – 1 | Share of FOMC2 transcript sentences classified as FSS. Blank if session-level section coding is unavailable. |
| within_gap | float | unconstrained | FSS_FOMC2 minus FSS_FOMC1. Captures the within-meeting escalation of financial stability discussion across days. Blank when either session share is unavailable. |
| CDFSG | float | unconstrained | **Primary composite index.** FSS_transcript minus FSS_minutes. See full explanation below. |
| CDFSG_minutes | float | unconstrained | FSS_minutes minus FSS_statement. Captures emphasis gap between minutes and the post-meeting statement. Blank when n_statement = 0. |
| CDFSG_speech | float | unconstrained | FSS_transcript minus FSS_speech. Captures emphasis gap between transcripts and associated speeches. Blank when n_speech = 0. |

### The CDFSG Index

**CDFSG** (Cross-Document Financial Stability Gap) is the primary sentence-level measure of compression of financial stability content between the verbatim transcript and the published minutes.

It is defined as:

```
CDFSG = FSS_transcript − FSS_minutes
```

where each component is the share of sentences classified as FSS (Financial Stability / Stress) in the respective document.

**Interpretation:**

- A value of **0** indicates that financial stability receives the same proportional emphasis in the transcript and the published minutes.
- A **positive** value indicates that the transcript devotes a larger share of sentences to financial stability than the minutes — the canonical case of downward compression.
- A **negative** value indicates that the minutes actually devote a larger share of sentences to financial stability than the transcript. This can occur when the transcript is dominated by routine economic discussion while the minutes incorporate prepared background summaries of financial conditions.

CDFSG is the sentence-classification analogue to the rubric-based `FSE_GAP` variable in `master_mechanisms.csv`. Both measure the same underlying construct — the minutes-versus-transcript financial stability emphasis gap — but use different methodologies (automated sentence classification vs. LLM-based rubric scoring of the full discussion). Cross-method agreement between CDFSG and FSE_GAP provides validation evidence for both measures.

---

## Notes on Missing Values

- Blank cells in `classified_sentences.csv` for `stability_intensity` indicate the sentence was not classified as FSS or FCS; this is expected and does not represent missing data.
- Blank cells for `speaker` and `speaker_role` in minutes and statement rows are expected; those documents are not attributed to individual speakers.
- Blank cells for `speech_title` and `speech_venue` in non-speech rows are expected.
- In `meeting_variables.csv`, blank cells for `{TOPIC}_statement`, `{TOPIC}_speech`, `FSS_FOMC1`, `FSS_FOMC2`, `within_gap`, `CDFSG_minutes`, and `CDFSG_speech` indicate that no documents of the relevant type are associated with that meeting date. These should be treated as structurally missing (not applicable) rather than zero.
- A value of `0` for `n_transcript` or `n_minutes` indicates a meeting for which the document was not available at time of data construction (some early transcripts were released with a lag or remain restricted).

---

## Related Files

| File | Relationship |
|------|-------------|
| `rubrics/sentence_classification_prompt_v2.txt` | The exact classifier prompt used to produce `topic`, `stability_intensity`, and `confidence` in classified_sentences.csv. |
| `data/derived/master_mechanisms.csv` | Meeting-level rubric-based scoring. `FSE_GAP` in that file is the rubric counterpart to `CDFSG` here. |
| `codebooks/CODEBOOK_mechanisms.md` | Codebook for master_mechanisms.csv, including definitions of FSE_GAP and all compression mechanism variables. |
