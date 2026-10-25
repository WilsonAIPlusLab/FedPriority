---
title: Codebook — Sentence Classification Files
version: 2.0
created: 2026-03-30
updated: 2026-10-23
---

## Overview

This codebook covers two related files (plus a third, `all_sentences_scored.csv`, described under Related Files) produced by the FOMC sentence-classification pipeline. The pipeline applies a large-language-model classifier (prompt version 2; see `rubrics/sentence_classification_prompt_v2.txt`) to sentences drawn from FOMC meeting transcripts, published meeting minutes, post-meeting statements, and selected Fed speeches spanning 440 distinct dates from January 1993 through January 2026 (see Unit of Observation for what a "date" means by document type).

> **Not every label is an LLM label (dataset 2.0.0, 2026-10-24).** The column `label_source` marks 7,979 of the 500,075 rows as `keyword_script`: their `topic` / `stability_intensity` values match the output of keyword scripts, not an LLM judgement (transcript 5,118; speech 2,448; minutes 413). The other 492,096 rows are `llm_presumed`: no keyword-script evidence was found, so they are presumed to be LLM labels. That is the absence of contrary evidence, **not a verification** that each row was labelled by the LLM. `meeting_variables.csv` was NOT recomputed after this flag was added; it still includes the keyword-labelled rows, and the effect on its shares and on CDFSG was not estimated. An analysis that wants LLM labels only can filter `label_source == "llm_presumed"` (and should still treat even that as unverified).

> **Current as of 2026-10-23** (dataset [2.0.0]): the corpus has **500,075 sentences on 440 dates** (verified against the file on 2026-10-23). It was rebuilt on 2026-09-27 (speech-parser duplication, label carry-forward, speaker attribution for transcripts), corrected on 2026-10-16 (footer-glued speaker labels, page-artifact removal, double-ingestion removal), and extended on 2026-10-17 with the 2007-06-28 and 2008-12-16 statements (26 sentences, classified by one agent with prompt v2). `meeting_variables.csv` was recomputed after those changes but **not** after the `label_source` flag was added in 2.0.0. Earlier row counts (526,516; 500,049) are superseded. See `CHANGELOG.md`.

The dataset focuses on financial stability (topic `FINANCIAL` with `stability_intensity`) alongside the two dual-mandate topics, `INFLATION` and `EMPLOYMENT_OUTPUT`; `REGULATION_SUPERVISION` and `OTHER` are context categories. The primary research purpose is to measure how financial-stability emphasis varies across document types — in particular, whether FOMC transcripts devote systematically more attention to financial-stability concerns than the corresponding published minutes. The sentence-level classifications support the CDFSG gap measures and allow comparison against the rubric-based scores in `data/primary/discussion_scores_v4_1.csv` (see Related Files).

## Unit of Observation

**classified_sentences.csv** — one row per sentence (500,075 total rows; `sentence_id` S000001–S500075, unique). By `doc_type`: transcript 428,487; minutes 52,831; speech 18,544; statement 213. Each row represents a single classified sentence extracted from one of four document types. `meeting_date` is the FOMC meeting date for transcripts, minutes and statements, but **the speech date for speech rows** (119 dates; not all are FOMC meeting dates). Coverage by `doc_type`: transcripts 272 dates, minutes 265, statements 17, speeches 119; 440 distinct dates overall, 1993-01-06 to 2026-01-28 (the latest dates come from minutes).

**meeting_variables.csv** — one row per `meeting_date` (440 total rows; this includes speech-only dates and dates through 2026-01-28; only 215 dates have both a transcript and minutes). Each row aggregates the sentence-level classifications for all documents associated with that meeting date.

---

## Variable Definitions — classified_sentences.csv

| Variable | Type | Valid Values | Description |
|----------|------|-------------|-------------|
| sentence_id | string | S000001 … S999999 | Unique sentence identifier, zero-padded to 6 digits, assigned in corpus order. |
| meeting_date | date | YYYY-MM-DD | Date of the FOMC meeting with which this document is associated (for `doc_type = speech`: the date of the speech). Range 1993-01-06 to 2026-01-28. |
| doc_type | categorical | transcript, minutes, statement, speech | Document source. `transcript` = verbatim meeting transcript; `minutes` = published FOMC minutes; `statement` = post-meeting press statement; `speech` = Fed official speech. |
| section | categorical | See below | Meeting session or document section; never blank. Transcripts: go_around_combined, policy_discussion, questions_for_staff, FOMC1, staff_economic_briefing, FOMC2, staff_financial_briefing, staff_outlook_briefing, policy_vote. Minutes: unsegmented_body, participants_views, policy_action, staff_financial_review, staff_economic_review, staff_outlook, staff_econ, participants, staff_fin. Statements: body, vote. Speeches: body. `FOMC1` = first day, `FOMC2` = second day of a two-day meeting; these two values occur for only 17 meetings (all other transcripts use the other labels). |
| speaker | string | Surname (upper-case for transcripts, e.g. BERNANKE; title-case for speeches, e.g. Kroszner) | Speaker surname for transcript sentences (present for all transcript rows as of the 2026-09-27 rebuild; previously blank for non-crisis-era transcripts). Set to the document's primary attributed author for speeches. Empty or NA for minutes and statements, which are not attributed to individual speakers. |
| speaker_role | categorical | Chair, Chairman, Vice Chair, Vice Chairman, Member, Governor, President (Voting), President (Nonvoting), (blank) (`Chairman`/`Vice Chairman` are source-convention variants of `Chair`/`Vice Chair`, not normalised; speech rows are only Governor or Chair) | Role of the speaker at the time of the meeting. Granularity varies by source convention: crisis-era transcripts and post-rebuild structured-header transcripts carry richer roles (e.g. Governor, President (Voting)); other transcripts carry only the coarse Chair/Vice Chair/Member scheme, since no richer role data exists in that source convention. Blank for minutes and statements. |
| text | string | free text | The verbatim sentence text as extracted from the source document. |
| word_count | integer | ≥ 5 (observed range 5–581) | Number of whitespace-delimited tokens in `text`. |
| speech_title | string | free text or (blank) | Title of the speech, for rows where `doc_type = speech`. Blank for all other document types. |
| speech_venue | string | free text or (blank) | Venue or occasion of the speech, for rows where `doc_type = speech`. Blank for all other document types. |
| topic | categorical | FINANCIAL, INFLATION, EMPLOYMENT_OUTPUT, REGULATION_SUPERVISION, OTHER | Topic label assigned by the sentence classifier (prompt V2). One label per sentence. Counts: OTHER 226,988; EMPLOYMENT_OUTPUT 114,471; FINANCIAL 95,556; INFLATION 59,925; REGULATION_SUPERVISION 3,135. The 7-code scheme below (FSS, FCS, etc.) is NOT stored in the file. |
| stability_intensity | integer | 1 – 5 or (blank) | Financial stability concern intensity score. Assigned for every sentence with `topic = FINANCIAL` (1: 56,457; 2: 23,271; 3: 10,850; 4: 3,843; 5: 1,135); blank for all other topics. See intensity scale below. |
| confidence | categorical | HIGH, MEDIUM, LOW | Classifier self-reported confidence in the topic assignment, normalized to a category. For rows whose original confidence was a raw numeric score (see `confidence_raw`), this is derived via ≥0.8 → HIGH, 0.6–0.79 → MEDIUM, <0.6 → LOW. |
| confidence_raw | string | HIGH/MEDIUM/LOW or a 0–1 decimal | The classifier's original confidence value, verbatim. Added 2026-09-27: an earlier pipeline era recorded confidence as a raw numeric score rather than a category for a subset of rows; both forms are preserved here unmodified so no information is lost, with `confidence` giving the normalized category for every row regardless of source form. |
| label_source | categorical | keyword_script, llm_presumed | Provenance flag added in 2.0.0 (last column; the file has 15 columns, header verified 2026-10-23). `keyword_script` (7,979 rows: transcript 5,118; speech 2,448; minutes 413; no statements): the label matches a keyword script, not an LLM judgement. By topic these rows are OTHER 5,168; FINANCIAL 1,557; EMPLOYMENT_OUTPUT 681; INFLATION 528; REGULATION_SUPERVISION 45 (FINANCIAL intensity 1: 1,090; 2: 140; 3: 271; 4: 8; 5: 48). `llm_presumed` (492,096 rows): no keyword-script evidence was found, so the label is presumed to come from the LLM classifier; this is not a verification. The flag shows where labels match keyword-script output; it does not say which labels are correct. Source list: project `docs/keyword_labelled_rows_2026-10-17.csv` (not shipped in this folder). The keyword rows are 1.6% of the file and 1,557 of the 95,556 FINANCIAL rows (1.6%), so their effect on corpus-wide shares is probably small, but meeting-level shares and CDFSG were not re-checked. |

### Topic Category Definitions

> **Note (verified 2026-10-17):** the 7-category scheme below is a conceptual taxonomy only. The file stores the five prompt labels (see `topic` above); no sentence is labelled FSS, FCS, INF, EMP, REG, OTH or DMS, and no post-processing split of `FINANCIAL` into FSS/FCS was applied. In `meeting_variables.csv`, `FSS_*` is the share of **all** FINANCIAL sentences (intensity 1-5), `FCS_*` is always 0, and `DMS_*` has no sentence-level source (see that section).

The conceptual taxonomy derived from the five categories in the V2 prompt; the prompt's `FINANCIAL` category could be split into two codes based on the `stability_intensity` score:

| Code | Label | Description |
|------|-------|-------------|
| FSS | Financial Stability / Stress | Financial markets, institutions, or instruments discussed as a stability concern in their own right. Covers systemic risk, contagion, bank failures, leverage cycles, fire sales, too-big-to-fail, financial fragility, and acute stress episodes. Corresponds to `stability_intensity` 3 – 5 in the prompt. |
| FCS | Financial Conditions / Stance | Financial variables discussed primarily as a transmission channel to the real economy — credit conditions affecting investment, lending standards affecting spending, interest-rate pass-through, wealth effects. Corresponds to `stability_intensity` 1 – 2 in the prompt. |
| INF | Inflation | Price stability, inflation expectations, inflation dynamics, deflation risk, inflation targeting, commodity prices affecting consumer prices, PCE/CPI movements, Phillips curve, wage-price dynamics. |
| EMP | Employment / Output | Labor markets, unemployment, output gaps, GDP growth, recession risk, productivity, business investment, consumer spending, aggregate demand and supply. |
| REG | Regulation / Supervision | Prudential regulation, supervisory tools, macroprudential policy, stress tests, capital requirements, Basel standards, bank examination, regulatory rules. |
| OTH | Other / General | International economy (trade, exchange rates, foreign growth), fiscal policy, payment systems, procedural or administrative content, Fed operations, boilerplate statements, bibliographic references, or genuinely unclassifiable sentences. |
| DMS | Decision-Making / Structure | Committee process, vote mechanics, procedural discussions about how the FOMC reaches decisions, meeting administration. |

Note (as designed; not applied in the data files): The classifier prompt (V2) uses `FINANCIAL`, `INFLATION`, `EMPLOYMENT_OUTPUT`, `REGULATION_SUPERVISION`, and `OTHER` as output labels. The `FINANCIAL` label is mapped to `FSS` or `FCS` in post-processing based on whether `stability_intensity` is ≥ 3 (FSS) or ≤ 2 (FCS). `EMPLOYMENT_OUTPUT` is stored as `EMP`; `REGULATION_SUPERVISION` as `REG`; `OTHER` and `DMS` are assigned during post-processing.

### Stability Intensity Scale (FINANCIAL sentences only)

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
| n_transcript | integer | ≥ 0 | Total sentence count from the meeting transcript. Zero if no transcript is available for this date (168 of 440 dates). |
| n_minutes | integer | ≥ 0 | Total sentence count from the published meeting minutes. Zero for 175 of 440 dates. |
| n_statement | integer | ≥ 0 | Total sentence count from the post-meeting press statement. Zero if no statement is in the corpus (423 of 440 dates; statements exist for 17 dates). The 2007-06-28 (9 sentences) and 2008-12-16 (17 sentences) statements were ingested on 2026-10-17, so all 17 FOMC1/FOMC2 meetings now have a statement and a `CDFSG` value. Statements for 2007-08-17 and 2020-08-27 are not yet downloaded (pending approval). |
| n_speech | integer | ≥ 0 | Total sentence count from Fed speeches associated with this meeting date. Zero if no speeches are linked. |
| n_FOMC1 | integer | ≥ 0 | Sentence count from the first day (FOMC1 section) of the transcript. Zero for single-day meetings or if `section` coding is unavailable. |
| n_FOMC2 | integer | ≥ 0 | Sentence count from the second day (FOMC2 section) of the transcript. Zero for single-day meetings. |
| {TOPIC}_transcript | float | 0 – 1 | Share of transcript sentences classified as `{TOPIC}`. Computed as (count of transcript sentences with the mapped label) / n_transcript. **Blank (not zero) if n_transcript = 0.** `{TOPIC}` takes seven column prefixes, but the mapping is: FSS = share of all `FINANCIAL` sentences (not the stability-only subset with intensity ≥ 3); FCS = always 0 (no sentence is mapped to it); INF = INFLATION; EMP = EMPLOYMENT_OUTPUT; REG = REGULATION_SUPERVISION; OTH = OTHER; **DMS has no sentence-level source** (non-zero in 258 dates, up to 0.68, and not part of the label shares). FSS+INF+EMP+REG+OTH sum to 1 (within 0.0002 rounding) wherever the document exists; adding DMS makes row sums exceed 1. |
| {TOPIC}_minutes | float | 0 – 1 | Share of minutes sentences classified as `{TOPIC}`. Computed analogously using n_minutes as denominator; blank if n_minutes = 0. |
| {TOPIC}_statement | float | 0 – 1 | Share of statement sentences classified as `{TOPIC}`. Blank if n_statement = 0. |
| {TOPIC}_speech | float | 0 – 1 | Share of speech sentences classified as `{TOPIC}`. Blank if n_speech = 0. |
| FSS_FOMC1 | float | 0 – 1 | Share of FOMC1 transcript sentences classified as FSS. Blank if session-level section coding is unavailable. |
| FSS_FOMC2 | float | 0 – 1 | Share of FOMC2 transcript sentences classified as FSS. Blank if session-level section coding is unavailable. |
| within_gap | float | unconstrained | **FSS_FOMC1 minus FSS_FOMC2** (sign as stored in the file and in `code/compute_variables.py`; e.g. 2007-06-28: 0.2981 − 0.0393 = +0.2588). A positive value means more financial discussion on day 1 than day 2. Populated for only 17 meetings (those with FOMC1/FOMC2 section coding); blank otherwise, as are `FSS_FOMC1` and `FSS_FOMC2`. |
| CDFSG | float | unconstrained | **As stored in the file: FSS_transcript minus FSS_statement** (17 non-blank values; the two added 2026-10-17 are 2007-06-28 = 0.0380 and 2008-12-16 = -0.2292). NOT the transcript-minus-minutes gap; for that use `CDFSG_minutes`. See explanation below. |
| CDFSG_minutes | float | unconstrained | **As stored in the file: FSS_transcript minus FSS_minutes** (215 non-blank values; verified to 6e-17). This is the transcript-versus-minutes emphasis gap and the column to use for it. Blank unless both documents exist. |
| CDFSG_speech | float | unconstrained | FSS_transcript minus FSS_speech. Captures emphasis gap between transcripts and associated speeches. Blank unless both exist (1 non-blank value). |

### The CDFSG Index

**CDFSG** (Cross-Document Financial Stability Gap) is the family of sentence-level gap measures. The transcript-versus-minutes version, the one intended to measure compression of financial stability content, is stored in the column **`CDFSG_minutes`**:

```
CDFSG_minutes = FSS_transcript − FSS_minutes      (215 meetings)
CDFSG         = FSS_transcript − FSS_statement    (17 meetings)
CDFSG_speech  = FSS_transcript − FSS_speech       (1 meeting)
```

(Column names are as stored; an earlier version of this codebook had the first two definitions swapped.) Each component is the share of sentences with topic `FINANCIAL` (all intensity levels; see the mapping note under `{TOPIC}_transcript`) in the respective document, not a stability-only share.

**Interpretation:**

- A value of **0** indicates that financial stability receives the same proportional emphasis in the transcript and the published minutes.
- A **positive** value indicates that the transcript devotes a larger share of sentences to financial content than the minutes (the hypothesised compression direction).
- A **negative** value indicates that the minutes devote a larger share to financial content than the transcript. **Observed:** `CDFSG_minutes` is negative in 201 of 215 meetings (positive in 14; mean −0.155), so the negative sign is the norm in this data, not an exception. A possible explanation is the minutes' prepared staff financial/economic review sections and the transcripts' length on other topics; this is not tested. The sign pattern has not been validated against human coding.

`CDFSG_minutes` was originally designed as the sentence-classification counterpart of a rubric-based `FSE_GAP` in `master_mechanisms.csv`. That file and its codebook were removed from the dataset in 2.0.0 (see `CHANGELOG.md`), so the comparison cannot be reproduced from this folder; the figures here are historical. Recomputed on 215 matched meetings (2026-10-17): Spearman 0.0645 (p=0.3465), Pearson 0.1547 (p=0.0233), i.e. no meaningful agreement. `FSE_GAP` was a 0-23 rubric score (never negative), so "signs differ" referred to the sign of the mean level (sentence share higher in minutes; rubric score higher in transcripts), not to a meeting-level correlation. The current rubric-based minutes-versus-transcripts gap table is `data/derived/discussion_v4_1_minutes_vs_transcripts.csv`; no agreement with `CDFSG_minutes` was computed for it in this pass. `CDFSG_minutes` is negative in 201 and positive in 14 of 215 meetings (6.5%). A stability-only variant (FINANCIAL with intensity >= 3, transcript minus minutes) has mean -0.010 but is positive in 103 of 215 meetings (47.9%), so its sign is not a robust pattern; that variant is not stored in the files. [Unverified (not recomputed since 2026-10-17): the Spearman/Pearson and stability-only figures were not recomputed in this pass; the `CDFSG_minutes` counts and mean were.] No validation evidence for either measure should be inferred from this comparison.

---

## Notes on Missing Values

- Blank cells in `classified_sentences.csv` for `stability_intensity` indicate the sentence was not classified as FINANCIAL; this is expected and does not represent missing data.
- Blank cells for `speaker` and `speaker_role` in minutes and statement rows are expected; those documents are not attributed to individual speakers.
- Blank cells for `speech_title` and `speech_venue` in non-speech rows are expected.
- In `meeting_variables.csv`, blank cells for `{TOPIC}_statement`, `{TOPIC}_speech`, `FSS_FOMC1`, `FSS_FOMC2`, `within_gap`, `CDFSG_minutes`, and `CDFSG_speech` indicate that no documents of the relevant type are associated with that date (and, for `{TOPIC}_transcript`/`{TOPIC}_minutes`, that n_transcript/n_minutes = 0). These should be treated as structurally missing (not applicable) rather than zero.
- A value of `0` for `n_transcript` or `n_minutes` indicates a meeting for which the document was not available at time of data construction (some early transcripts were released with a lag or remain restricted).

---

## Related Files

| File | Relationship |
|------|-------------|
| `rubrics/sentence_classification_prompt_v2.txt` | The exact classifier prompt used to produce `topic`, `stability_intensity`, and `confidence` in classified_sentences.csv. |
| `data/primary/discussion_scores_v4_1.csv`, `data/derived/discussion_v4_1_minutes_vs_transcripts.csv` | Current rubric-based (V4.1) discussion scores and their minutes-versus-transcripts gaps; the rubric-based comparison point for `CDFSG_minutes`. `master_mechanisms.csv` and `CODEBOOK_mechanisms.md` were removed in 2.0.0. |
| `data/sentence_classification/all_sentences_scored.csv` | Third file: 70,610 rows (transcript 44,490; speech 21,870; minutes 4,063; statement 187). Columns (17): the first ten classified_sentences columns (`sentence_id` to `speech_venue`), then `peek_fi_count`, `peek_fi_binary`, `correa_fss_pos`, `correa_fss_neg`, `lm_positive`, `lm_negative` (dictionary term-match counts; no `topic`), and `join_key`. Dictionary columns are case-insensitive, word-boundary regex matches with no stemming (terms files in `dictionaries/`; the scoring script `score_dictionaries.py` is not in this folder, so the counts cannot be regenerated from here). `peek_fi_count` = matches of the 36 terms in `peek_fi_35.txt` (the file name says 35; it holds 36; Peek, Rosengren and Tootell 2016); `peek_fi_binary` = 1 if `peek_fi_count` > 0; `correa_fss_pos` / `correa_fss_neg` = matches of the 96 positive / 295 negative terms of the Correa et al. financial-stability lexicon; `lm_positive` / `lm_negative` = matches of the 354 positive / 2,355 negative Loughran-McDonald terms. Share of sentences with at least one match: Peek 4.87%, Correa 32.41%, LM 50.47%. **Warning:** `sentence_id` in this file (Feb 2026 build) does NOT match `sentence_id` in `classified_sentences.csv`: all 70,610 ids exist in the current file but the text agrees for 0 of them. Join on `join_key` = `meeting_date`, `doc_type` and the first 12 hex characters of the md5 of the lower-cased, stripped text, joined with a vertical bar; it is computed the same way from `classified_sentences.csv` text, and 67,288 of 70,610 scored rows (95.3%) find a key in the current corpus. Keys repeat (repeated short sentences): 2,844 keys occur more than once in the scored file and 490 in the corpus, so de-duplicate before a many-to-one join. |

---

## Limits (2.0.0)

- No human validation of the sentence labels exists in this folder; `llm_presumed` is not a verification.
- `meeting_variables.csv` was not recomputed after `label_source` was added; its shares and CDFSG include the 7,979 keyword-labelled rows.
- Most keyword-labelled rows are OTHER (5,168 of 7,979); 1,557 are FINANCIAL.
