# FedPriority (FOMC Document Scoring): Data Provenance

**Dataset version**: 2.0.0 DRAFT (local working copy, not committed, pushed or published; see `CHANGELOG.md` [2.0.0])
**Last updated**: 2026-10-23 (checksums, counts and gap statistics recomputed from the shipped files on this date unless marked otherwise)

**Removed in 2.0.0** (so earlier references to them do not apply to this release): `master_mechanisms.csv` and the mechanism coding, `analysis/`, `scoring_evidence/meeting_comparisons/`, `discussion_scores_v3.csv` and its evidence, `data/legacy/`, `correction_log.csv`, `concordance_*.csv`, `data/supplementary/`, `econclasshub/` and backup files. `staff_scores_v4.csv` is replaced by `staff_scores_v6.csv`. Reasons are in `CHANGELOG.md` [2.0.0]; removed files are kept in the project repository under `publish_staging/v2.0.0_removed/` and in the public GitHub history of v1.0.0.
**Scope**: FOMC minutes (1993–2026) and transcripts (1993–2020)

**Evidence status**: No human annotator has labelled any part of this dataset. Every score and every reliability or agreement figure cited below is produced by, or compared against, LLM runs (model-versus-model or internal consistency). Gap sign convention throughout: minutes minus transcripts (negative = minutes score lower).

---

## 1. Source Data

All source documents are produced by the Board of Governors of the Federal Reserve System or the Federal Open Market Committee and are in the public domain as products of the United States federal government. No licensing restrictions apply to the source documents.

### 1.1 Federal Reserve Website Access Points

| Document type | URL pattern | Coverage |
|---------------|-------------|----------|
| FOMC historical (pre-2017) | https://www.federalreserve.gov/monetarypolicy/fomc_historical.htm | Minutes + transcripts 1993–2020 |
| FOMC calendar (2017+) | https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm | Minutes 2017–2026 |
| Statements | https://www.federalreserve.gov/newsevents/pressreleases/ | Statements 1994–2026 |
| Press conferences | https://www.federalreserve.gov/monetarypolicy/fomcpresconf.htm | Press conferences 2011–2026 |
| Testimonies | https://www.federalreserve.gov/newsevents/testimony/ | Selected 1993–2026 |
| Speeches | https://www.federalreserve.gov/newsevents/speech/ | Selected 1996–2026 |

### 1.2 Document Counts by Type

| Document type | Count | Date range |
|---------------|-------|------------|
| Minutes | 270 | 1993–2026 |
| Transcripts | 279 | 1993–2020 |
| Statements | 247 | 1994–2026 |
| Press conferences | 95 | 2011–2026 |
| Testimonies | 62 | Selected |
| Speeches | 3,006 | Selected (1,979 distinct speeches in the speech manifest) |
| **Total raw documents** | **3,959** | 1993–2026 |

Counts are files in `01_acquisition/raw_documents/`, recounted on 2026-10-17 (speeches: 1,979 htm plus 1,027 pdf files). They replace the 2026-03 counts (265 / 273 / 241 / 90 / 62 / ~2,886 / ~3,816). Of the 279 transcript files, 272 transcripts are scored. [Unverified as of 2026-10-17: the speech manifest has 1,979 rows against 3,006 speech files, so many pdf files are probably alternate copies; not checked file by file.] 347 Beige Book files are stored separately and are not in the total. `meeting_registry.csv` (320 rows) lists 270 minutes, 246 statements and 95 press conferences in its `documents_found` column.

### 1.3 Known Data Gaps and Anomalies

**Multi-day meeting dating**: `meeting_date` in `meeting_registry.csv` is the document-name date; `start_date` and `end_date` give the meeting span. Of the 176 rows spanning two days, `meeting_date` is the last day for 162 and the first day for 14 (recomputed from the shipped file on 2026-10-17). Score tables are keyed by their own document dates, which can differ from the registry by one day; `data/derived/meeting_key_map.csv` (1,477 rows: 542 `discussion_v4_1` keys, 495 `staff_patched_v6` keys, 440 `meeting_variables` keys) maps each key to a registry meeting: 1,327 exact, 33 inside the meeting span, 2 day-after-call, 115 unmatched. All 115 unmatched keys are `meeting_variables` dates (speeches without a meeting); the staff v6 and discussion V4.1 keys have 0 unmatched (recounted 2026-10-23). The file is `02_registry/meeting_key_map.csv` of the project repository filtered to the three shipped tables (the filtering step itself was not re-run here); `tools/check_keys.py` is in the project repository only. The `special_notes` column (15 non-empty rows) records conference-call and inter-meeting-action notes, not date discrepancies. `rate_decision` and `target_rate` are unfilled (no source) and `documents_expected` is unfilled for 2011–2018.

**Pre-2005 minutes format**: Minutes published before approximately 2005 are not segmented into staff and participant sections. Section-level analysis relies on linguistic cues ("the staff reported," "members noted") to separate content types. This affects the precision of staff vs. discussion decomposition for early meetings; 128 of the 270 minutes folders hold only `unsegmented_body.txt`.

**Emergency meetings**: Six registry rows have `meeting_type` = emergency (2007-08-10, 2019-10-11, 2020-03-02, 2020-03-15, 2020-03-23, 2025-08-22); a further 45 rows are conference calls and 269 are scheduled (320 rows in all). The former 2007-06-18 row was removed (that date was the 28 June 2007 statement, per the project log). These meetings have abbreviated documents. Scoring agents are instructed to use N/A liberally for such meetings and to flag them in the anomaly field.

---

## 2. Processing Pipeline

The full pipeline from raw documents to scored outputs ran through eleven stages. The table below presents the data lineage; stages 5, 6 and the V3 part of stage 8 produced files that were removed from the release in 2.0.0 and are listed only so that the stage numbers stay stable. Paths prefixed with `data/` or `scoring_evidence/` refer to the released dataset directory; paths like `01_acquisition/`, `02_registry/`, `03_decomposition/`, and `04_scoring/` refer to the project build environment and are not included in the dataset release.

| Stage | Input | Process | Output |
|-------|-------|---------|--------|
| 1. Acquisition | Federal Reserve website | PDF and HTML download via three acquisition scripts with rate limiting (1–2 second delay per request) | `01_acquisition/raw_documents/` (3,959 files in 6 subfolders) |
| 2. Registry | Raw document folders | Meeting identification: scan all folders, match documents to calendar events, manual population of emergency events and rate decisions | `data/primary/meeting_registry.csv` (320 data rows, 1993-01-06 to 2026-09-16; columns `meeting_date, start_date, end_date, meeting_type, chair, documents_found, documents_expected, rate_decision, target_rate, special_notes`) |
| 3. Decomposition | Raw documents | Section extraction by document type and era: minutes decomposed into staff_economic_review.txt, staff_financial_review.txt, staff_outlook.txt, participants_views.txt, policy_action.txt (142 meetings) or unsegmented_body.txt (128 meetings); transcripts into go_around_combined.txt, policy_discussion.txt and staff-briefing components | `03_decomposition/output_rebuild/` (live tree: 270 minutes and 272 transcript folders, 2,053 manifest rows, 17.1M tokens in the manifest; the older `output/` tree is stale and should not be used). Four transcripts (1998-11-17, 2004-06-30, 2005-06-30, 2011-11-02) have staff special sessions missing from their component files (full text complete); 42 transcript folders (1993–96) were regenerated after the footer-glued-label fix |
| 4. Cross-validation | Decomposed output + registry | Completeness check against registry, orphan detection (±1 day tolerance), metadata enrichment | `_metadata.json` for each of the 542 meeting folders; `tools/verify.py` reconciles registry and decomposition on the live tree [Unverified as of 2026-10-17: the original "0 gaps" count from March was not rerun] |
| 5. Staff scoring V3 (legacy; removed in 2.0.0) | Meeting text files | LLM rubric V3 batched scoring, several documents per agent | Output `data/legacy/staff_scores_corrected_v3.csv` no longer ships |
| 6. Correction pipeline (removed in 2.0.0) | V3 scores | Manual audit of flagged scores; correction log | `data/derived/correction_log.csv` no longer ships (it used V3 dimension names that do not exist in the current tables) |
| 7. Staff scoring V4 / v6 (canonical) | Meeting text files | LLM rubric V4 independent scoring: one fresh agent per document, no shared context; 15 dimensions. Original run: 266 minutes and 216 transcripts; later 2026-10 patches (four gutted minutes re-scored, CREDIT_SPREADS level reading, five fresh 2026 minutes, transcripts re-scored on repaired text) produced the project table `04_scoring/staff/v4_scores_patched_v6/all_scores_v4_patched_v6.csv` | `data/primary/staff_scores_v6.csv` (495 scored documents: 270 minutes + 225 transcripts, copied from that project table; `SCORE_VERSION` column marks the vintage). It replaces `staff_scores_v4.csv` (486 rows), which differed from v6 in 84-139 of 486 shared rows per main dimension |
| 8. Discussion scoring V3 independent (removed in 2.0.0) | Meeting text files | LLM rubric V3 independent scoring | `discussion_scores_v3.csv` and `scoring_evidence/discussion_v3/` no longer ship; superseded by 8b |
| 8b. Discussion scoring V4.1 (recommended for discussion analyses; unpublished) | Rebuilt member-discussion inputs | Transcripts: one fresh agent per document; minutes: earlier V4 analyses patched by one fresh agent per meeting; five 2026 minutes scored fresh (see 3.2) | `data/primary/discussion_scores_v4_1.csv` (542 scored documents: 270 minutes + 272 transcripts) |
| 9. Minutes-transcript comparison | Staff v6 + Discussion V4.1 scores | Paired gap analysis (minutes minus transcript), same-date merge | `data/derived/staff_v6_minutes_vs_transcripts.csv` (215 same-date pairs, 2,166 numeric pairs, 15 dimensions; was 2,231 before the pre-2009 staff minutes were re-scored) and `data/derived/discussion_v4_1_minutes_vs_transcripts.csv` (224 matched pairs, 3,125 rows; was 3,129). `master_mechanisms.csv` and `scoring_evidence/meeting_comparisons/` (hand-typed gap columns correlating 0.26 / 0.09 / 0.25 with the V4.1 gaps) were removed in 2.0.0 |
| 10. Sentence classification (CDFSG) | Decomposed meeting text files | LLM sentence-level classifier using 7-category CDFSG taxonomy; applied to transcripts, minutes, speeches and statements: 500,075 sentences from 440 dates (1993-01-06 to 2026-01-28; doc_type transcript 428,487 / minutes 52,831 / speech 18,544 / statement 213) after page-footer cleaning, removal of 22,815 double-ingested rows and ingestion of the 2007-06-28 and 2008-12-16 statements (26 sentences, one agent, prompt v2). `all_sentences_scored.csv` has a `join_key` column; its sentence_id does not match the final corpus | `data/sentence_classification/classified_sentences.csv`, `meeting_variables.csv`. New in 2.0.0: `classified_sentences.csv` has a `label_source` column. 7,979 rows are `keyword_script` (transcript 5,118; speech 2,448; minutes 413; statement 0): their topic, intensity and confidence reproduce the output of the project's old keyword scripts, not an LLM judgement. The other 492,096 rows are `llm_presumed`, which means only that no keyword-script evidence was found; it is not a verification that an LLM labelled them. Source of the list: `docs/keyword_labelled_rows_2026-10-17.csv` in the project repository (7,979 data rows), built by approximate window matching, so partial chunks may be missed. `meeting_variables.csv` was not recomputed and still includes the keyword-labelled rows; the effect on CDFSG was not estimated |
| 11. Topic modeling (FASTopic) | Decomposed meeting text files | Unsupervised FASTopic modeling on 7 document corpora; topics mapped to 13 economic/financial categories | `data/topic_modeling/cross_corpus_matrix.csv`, `cross_method_matrix.csv`, per-corpus time series CSVs. Cleaned re-run: FASTopic vs BERTopic r = 0.865 for minutes (N=265), 0.48 for transcripts (N=225), 0.78 for staff-combined (N=312); the r > 0.7 success rule fails for transcripts. A rerun on the rebuilt decomposed-transcript corpus is in progress; its results are not quoted here [Unverified as of 2026-10-17: the "7 document corpora" count was not rechecked] |

### 2.1 Key Scripts

| Stage | Primary script | Location |
|-------|----------------|----------|
| 1. Acquisition | `fomc_downloader.py`, `fomc_downloader_v2.py`, `fomc_additional_downloader.py` | `01_acquisition/scripts/` |
| 2. Registry | `build_registry.py` | `02_registry/` |
| 3. Decomposition | `decompose.py` | `03_decomposition/code/` |
| 4. Cross-validation | `cross_validate.py`, `enrich_metadata.py` | `02_registry/` |
| 7–8. Independent scoring | `run_v4_scoring.py`, `run_v3_scoring.py` | `04_scoring/evidence_independent_rescoring/comparison/` |
| 9. Comparison | `run_v3_scoring.py` (compare command) | `04_scoring/evidence_independent_rescoring/comparison/` |

### 2.2 Decomposition Era Handling

The decomposition script applies five era-specific validation presets (`ERA_VALIDATION` in `03_decomposition/code/config.py`) to handle format variation across the 33-year document history:

| Preset | Document type and era |
|--------|-----------------------|
| `greenspan_html` | Minutes in HTML, or non-PDF minutes dated before 2007 |
| `modern_pdf` | All other minutes (PDF) |
| `transcript_regular` | Regular meeting transcripts (all eras) |
| `transcript_confcall` | Conference call transcript format |
| `transcript_emergency` | Emergency meeting transcript format |

A v2 decomposition script fixed an HTML extraction bug present in v1. The live tree `output_rebuild/` (542 folders) also recovers four minutes that had been gutted by a notation-vote bug and carries the footer-label fix for 42 transcripts.

---

## 3. Version History

### 3.1 Staff Scoring

**V3 batched (removed in 2.0.0)**: `data/legacy/staff_scores_corrected_v3.csv` and `data/derived/correction_log.csv` no longer ship. The V3 batched method (one agent, several documents) had cross-meeting context contamination (see 5.3); an earlier batched-scoring figure of about +8 points for the minutes-transcript financial-conditions gap was retracted and is not a measured baseline.

**V4 independent, now `staff_scores_v6.csv` (canonical)**

- Location: `data/primary/staff_scores_v6.csv` (replaces `staff_scores_v4.csv`)
- Source: `04_scoring/staff/v4_scores_patched_v6/all_scores_v4_patched_v6.csv` in the project repository (v6 = v5 plus the five 2026 minutes rows; patched v1-v5 are superseded). 495 rows: 270 minutes + 225 transcripts, 1993-02-03 to 2026-09-16; 42 columns including `ANOMALY_FLAG`, `ANOMALY_NOTE` and `SCORE_VERSION`.
- `SCORE_VERSION` (recounted 2026-10-23): `v4_prior` 197, `v4_patched_2026-10` 186, `v4_prior+credit_v4_1` 75, `v4_patched_2026-10+credit_recheck` 28, `v4_new2026_minutes` 5, `v4_patched_2026-10+credit_v4_1` 4. The table is therefore mixed vintage; compare levels only within a vintage. What each label means is defined by the project's build scripts, not by this folder.
- Method: one fresh LLM agent per document; no shared context; no batching; 15 dimensions on a 1-100 scale. Transcripts were re-scored on repaired text, so they differ from the earlier V4 run (84-139 of 486 shared rows per main dimension compared).
- Changes from V3: new rubric with clarified anchor tables, improved bright-line rules for financial dimensions (BANKING_STRESS, TREASURY_STRESS, DOLLAR_STRENGTH), refined polarity guidance; independence mandate.
- Contamination: in the original V4 run, no cross-meeting references in agent reasoning text; 26 references in 12 V4 files were judged to be quotations from source documents (see 5.3). This audit covered the original run, not the re-scored v6 transcripts.
- Rubric: `rubrics/staff_scoring_rubric_v4.md`.
- Evidence files: `scoring_evidence/staff_v4/independent/` (266 .md files, QA rescore of minutes only) and `scoring_evidence/staff_v4/new_2026_minutes/` (5 files, fresh scores for the 2026 meetings). They were written for the original V4 minutes scores, not for the v6 table; no evidence files are shipped for staff transcripts.
- CREDIT_SPREADS: updated to the level reading (79 cells in the earlier v4 table: 74 minutes, 5 transcripts; log `data/derived/credit_spreads_v4_1_applied_2026-10-17.csv`). Most transcript rows still use the earlier rule, so the column is mixed-vintage and must not be differenced against the discussion CREDIT_SPREADS. The v6 `SCORE_VERSION` labels containing `credit` cover 107 rows; the 79-cell log describes the earlier table and was not re-reconciled against v6.
- Financial-conditions gap in v6 (minutes minus transcripts): +1.55 over 213 pairs (215 same-date pairs in the table; recomputed 2026-10-24 after the pre-2009 staff minutes were re-scored; it was −0.92 before, so its sign changed). It is small next to scorer noise of about 2 points per score, rests on model scoring only, and has not been checked against human coding or separated from measurement differences between document types.
- Status: canonical in the 2.0.0 release.

### 3.2 Discussion Scoring

**V3 batched and V3 independent (removed in 2.0.0)**: `data/legacy/discussion_scores_v3_batched.csv`, `data/primary/discussion_scores_v3.csv`, `CODEBOOK_discussion_scores.md` and `scoring_evidence/discussion_v3/` no longer ship; the V3 concordance and validation reports were also removed. V3 batched scoring shared the staff contamination mechanism (inflated autocorrelation, worst for DISSENT_INTENSITY, FINANCIAL_STABILITY_EMPHASIS, UNCERTAINTY_EXPRESSED). The V3 rubric `rubrics/discussion_scoring_rubric_v3.md` is still shipped. V3 gap figures are not quoted here because they were recorded inconsistently across documents.

**V4.1 (recommended file for discussion analyses; unpublished draft)**

- Location: `data/primary/discussion_scores_v4_1.csv`
- Method: transcripts scored fresh, one fresh LLM agent per document, on rebuilt inputs (`member_discussion_v2`; `v2b` for 71 re-scored meetings; `v2c` for the five fresh 2026 minutes); minutes: the earlier V4 analyses patched by one fresh agent per meeting against the rebuilt input and a text diff (137 rows, `METHOD` = `patch_of_v4_analysis`, meetings from 2009 on); the 128 minutes of 1993-2008 are fresh blind scores on a rebuilt discussion-only input (`METHOD` = `fresh_blind_split_2026-10`, `INPUT_VERSION` = `member_discussion_split_2026-10-23`, one fresh agent per document, 2026-10-24; see 5.5); the five 2026 minutes are fresh scores. 542 rows: 270 minutes + 272 transcripts (`METHOD`: 277 `fresh_score`, 137 `patch_of_v4_analysis`, 128 `fresh_blind_split_2026-10`). 20 dimensions, including five discussion dimensions. Rubric: `rubrics/discussion_scoring_rubric_v4_1.md` plus `rubrics/discussion_scoring_clarifications_v4_1_1.md`.
- Checks: blind second pass on 381 minutes cells (`data/derived/discussion_v4_1_second_pass_check.csv`); 36 cells set to N/A afterwards. Blind re-check of the 27 first-run transcript CREDIT_SPREADS `N/A` cells under the V4.1.1 clarifications: 16 now scored at Low confidence (`CREDIT_UPDATE` column; `data/derived/discussion_v4_1_credit_update_log.csv`).
- Evidence files: `scoring_evidence/discussion_v4_1/`
- Gaps (minutes minus transcripts, 224 matched pairs; recomputed 2026-10-24): DISSENT_INTENSITY −10.8, UNCERTAINTY_EXPRESSED −7.2 (before the 1993-2008 minutes were re-scored: −8.3, −5.0; the 96 pairs from 2009 on did not change). The re-scored minutes come from a later scoring session than the transcripts, and the vintage drift measured below is the same direction and size, so the widening is probably not a new finding. An earlier V3 scoring (no longer shipped) gave the same signs and similar sizes; V3 and V4.1 come from one model family, so that is not an independent confirmation, and neither has been checked against human coding. The stable sign and rough size argue against batching or input defects as the cause; they do not show that the cause is editorial compression, because nothing here separates that from differences in what the scorer can see in minutes versus transcripts.
- Scoring-vintage caveat (`CHANGELOG.md` [1.3.0]): the five 2026 rows were scored on 2026-10-16/17; re-scoring 44 unchanged transcripts on those days moved FSE by −6.0, dissent by −2.4 and uncertainty by −2.9 on average, so levels of those three dimensions are not comparable between the 2026 rows and older rows (the minutes-minus-transcripts gaps are essentially unchanged).
- Minutes patch update: the project's patched minutes table `04_scoring/discussion/v4_1_scores/minutes_patch/all_scores_disc_m_v411_patched_v2d.csv` (265 rows) re-scored 2000-12-19 on the v2d input (HAWKISH_DOVISH_LEAN 38 to 42, other dimensions unchanged). The shipped `discussion_scores_v4_1.csv` and `derived/discussion_v4_1_minutes_vs_transcripts.csv` carry the change as of 2026-10-17 (INPUT_VERSION `member_discussion_v2d`; backups `*.bak_2026-10-17_v2d`).
- Limits: see `codebooks/CODEBOOK_discussion_scores_v4_1.md`.

### 3.2b 2026 Supplementary Tables (removed in 2.0.0)

`data/supplementary/` (2026 statement, press-conference, Beige Book and speech FSAI scores; 4-61 rows each) and `CODEBOOK_supplementary.md` no longer ship: later scoring vintage, three Beige values steered by a stated rule, no review. The speech re-score (62 earlier speeches re-scored on 2026-10-17, FSAI correlation with the old scores 0.90, mean change -11.1; drift and text dilution not separable) remains a project-repository result only.

### 3.3 Compatibility Note

Batched V3 scores (not shipped) and independent scores are *not* interchangeable. The version transition involved both rubric improvements (V3→V4 for staff) and a methodological change (batched→independent). Correlation between old and new scores varied by dimension: core economic dimensions correlated at r = 0.85–0.97; financial sub-dimensions and subjective dimensions showed more change. See `validation/COMPARISON_SYNTHESIS.md` (a March 2026 report on the earlier files). Staff v4 and v6 are also not interchangeable (see 3.1).

---

## 4. File Checksums (SHA-256)

**The current checksums are in the table in Section 4a at the end of this file (recomputed 2026-10-23). The tables in this section are HISTORICAL and superseded; they are kept only to show earlier file states. `staff_scores_v4.csv` and `discussion_scores_v3.csv` named below are no longer shipped in 2.0.0.**

HISTORICAL: checksums computed from the primary data files as of 2026-03-30.

| File | SHA-256 |
|------|---------|
| `dataset/data/primary/staff_scores_v4.csv` | `de2978e7c7c2384e2b7b101d2219a129cf426255449b5994da4d1346e471b757` |
| `dataset/data/primary/discussion_scores_v3.csv` | `a24ffc911e68b18dcc2676988b5dbe2e2f15e7daae7c27bc93e2e0c32126fcd0` (does not match the current file; see 4a) |
| `dataset/data/primary/meeting_registry.csv` | `894902febbf42359749e1db92c63ff7e466be9eff263e5b5f4f373fec562c93a` |

HISTORICAL (superseded by 4a): the two files below were **republished 2026-09-27** to fix a parser bug and a missing
speaker-attribution field (see `dataset/CHANGELOG.md` [1.1.0]); their checksums reflect
that date, not 2026-03-30. Previous versions are kept alongside them as
`*.bak_2026-09-27_pre_speaker_fix`.

| File | SHA-256 |
|------|---------|
| `dataset/data/sentence_classification/classified_sentences.csv` | `d1b40931159ef5906af6cfd95e5c024bbc9930ef185f0fb52eb18ff7d82ca1aa` |
| `dataset/data/sentence_classification/meeting_variables.csv` | `0120e2bfcba14b6d6c8f549333ef1e406a6f4ab7f22e592d8276dd3241564b5c` |

HISTORICAL (superseded by 4a): the V4.1 discussion file added in 1.2.0 (checksum computed when the review package was built):

| File | SHA-256 |
|------|---------|
| `dataset/data/primary/discussion_scores_v4_1.csv` | `43659f3135e4f0948390146490b8a2c3aa48ef0ef8a6b9c11cd319f53f337a3d` |

(The checksum above was recomputed on 2026-10-08 after the CREDIT_SPREADS update; the file built for review had `383fb88d…f497`. Neither matches the current file (see 4a).)

To verify a file after download:

```python
import hashlib
path = "dataset/data/primary/staff_scores_v6.csv"
print(hashlib.sha256(open(path, 'rb').read()).hexdigest())
```

---

## 5. Data Quality

Full quality control evidence is documented in VALIDATION_REPORT.md. Summary metrics are provided here. No human validation exists: the checks below are model reviews, model re-scores or internal-consistency checks, not comparisons with human labels or ground truth. They cover the original 2026-03 files (482 staff, 539 discussion-V3 documents, neither shipped in 2.0.0); the five 2026 staff minutes, the re-scored transcripts in `staff_scores_v6.csv` and the V4.1 file are not covered by these procedures.

### 5.1 Staff Scoring Quality

A cumulative model-review pass (a second model judging scores against the rubric anchors, not validation against ground truth) assessed every scored *dimension* (not file) as VALID, QUESTIONABLE, or INCORRECT using tolerance thresholds of ±5 points (VALID), ±6–12 points (QUESTIONABLE), or >12 points / wrong direction (INCORRECT). Results across ~481 files:

| Quality tier | Dimension-checks | Share | Notes |
|--------------|-----------------|-------|-------|
| VALID | ~2,734 | ~73% | Score within ±5 points of rubric anchor |
| QUESTIONABLE | ~809 | ~22% | Score within ±6–12 points; plausible but wider uncertainty |
| INCORRECT | ~183 | ~5% | Score direction or magnitude clearly unsupported; corrected |

Source: `scoring_cumulative_validation_report.md` (04_scoring/staff/docs/). INCORRECT-flagged dimension-scores were corrected in the original V4 table (564 corrections, 317 of 482 files). The correction log was removed in 2.0.0 (it used the V3 column names DOLLAR_FX and BANKING_HEALTH); these counts are quoted from the March 2026 report and cannot be reproduced from the shipped files. The review pre-dates the re-scoring of transcripts in v6, so it does not describe `staff_scores_v6.csv`.

### 5.1b Discussion Scoring Anomaly Flags

Anomaly flags (`ANOMALY_FLAG` = Yes, recounted 2026-10-23): 251 of 542 (46%) in the V4.1 discussion file and 156 of 495 (32%) in the staff v6 file. (The 2026-10-17 count for the V4.1 file was 252; the cause of the difference of one was not traced.) Anomaly flags indicate unusual meeting circumstances (emergency actions, special-topic meetings, very short documents, dominant speakers) rather than errors. Flagged documents are retained in the canonical file with the anomaly description in the `ANOMALY_NOTE` column.

### 5.2 Discussion Scoring Reproducibility

A model re-score audit (V3 discussion scoring; the V3 table is no longer shipped) re-scored 16 documents using independent Claude agents to assess run-to-run reproducibility of one model:

- Mean absolute deviation (MAD): **1.9 points** on the 1–100 scale
- Direction errors (score crosses 50 in opposite direction): **zero**
- Dimension-level stability: the largest single-dimension deviation in the 16-document re-score was 6 points (DISSENT_INTENSITY). The figures 7.2 (FINANCIAL_STABILITY_EMPHASIS) and 5.7 (DISSENT_INTENSITY) that appeared here earlier are mean absolute differences between old batched and new independent scores (`validation/COMPARISON_SYNTHESIS.md`, Section 2b), not re-score reproducibility; these dimensions also carry wider uncertainty bands by rubric design.
- Later V4.1 noise measures use different samples and are not comparable: 1.8 (15 transcripts, blind re-score), 3.3 (60 fresh minutes versus patched minutes), 3.8 (blind second pass on minutes cells), and a scoring-vintage drift of up to 6.0 on FSE for 44 re-scored transcripts (`CHANGELOG.md` [1.2.0], [1.3.0]). The 1.9 figure should therefore not be read as the expected reproducibility of V4.1.

### 5.3 Independence Confirmation

The independence audit examined scored .md evidence files for phrases indicating cross-meeting memory. The published figures measure different things and should not be compared with one another:

| Measure | Scope | Result |
|---------|-------|--------|
| Agent-opinion cross-meeting references (`validation/COMPARISON_SYNTHESIS.md`) | Old batched scoring | 260 |
| Same measure | New independent scoring (V4 staff, V3-ind; not re-audited for v6) | 0 |
| Files with cross-meeting references in reasoning text (VALIDATION_REPORT.md 1.2) | Old batched: 84 of 266 minutes files (32%), 44 of 272 transcript files (16%) | see scope |
| Cross-meeting references in reasoning text, comparison sample (independence audit Table 2) | V4: 26 references in 12 files (judged source-document quotations, not agent memory); old batched sample: 8 | different scan scopes |

No scored .md file from the independent runs contains language comparing the current meeting to a prior meeting, referencing prior scores, or invoking sequential reasoning across meetings.

### 5.4 Staff v6 Minutes-Transcript Concordance

For paired meetings where both minutes and transcripts were scored (215 same-date pairs; N per dimension ranges from 12 to 215 depending on data availability):

| Dimension | N | r | MAD | Bias (min−trans) |
|-----------|---|---|-----|------------------|
| LABOR_TIGHTNESS | 214 | 0.954 | 3.4 | −0.7 |
| OUTPUT_GAP | 215 | 0.943 | 2.9 | −0.3 |
| INFLATION_PRESSURE | 214 | 0.843 | 4.8 | −2.2 |
| CONSUMPTION_INVESTMENT | 214 | 0.920 | 3.8 | +1.9 |
| FINANCIAL_CONDITIONS | 213 | 0.789 | 7.1 | +1.6 |
| CREDIT_SPREADS | 173 | 0.748 | 8.9 | +2.4 |
| BANKING_STRESS | 86 | 0.830 | 7.2 | +1.7 |

Recomputed 2026-10-24 from the shipped `data/derived/staff_v6_minutes_vs_transcripts.csv` (2,166 numeric pairs; r is the Pearson correlation of the two score columns, MAD the mean absolute difference), after the 128 pre-2009 staff minutes were re-scored on a staff-only input (see 5.5). The earlier version of this table (2026-10-23, 2,231 pairs, pre-2009 minutes scored on the whole minutes body) is kept in the project backups; it gave, for example, INFLATION_PRESSURE r = 0.908, FINANCIAL_CONDITIONS r = 0.828, CREDIT_SPREADS r = 0.874, bias in FINANCIAL_CONDITIONS −0.9. The CREDIT_SPREADS row mixes the earlier and level-reading rules (see 3.1). Agreement is high on the core dimensions (r > 0.84) and lower on the financial ones (0.56-0.83); TREASURY_STRESS agrees least (r = 0.558, N = 160, bias +1.3). Bias figures are within about two points of zero except EQUITY_VALUATION (+3.4), CREDIT_SPREADS (+2.4), CONSUMPTION_INVESTMENT (+1.9) and BANKING_STRESS (+1.7); scorer-to-scorer noise is about 2 points per score, so most of these gaps are small next to it. This shows that two LLM scorings of different texts agree; it is not evidence of accuracy, and it is model-versus-model with no human coding.

### 5.5 Pre-2009 minutes re-scored on separated components (2026-10-24)

**What changed.** The 128 minutes of 1993-2008 had no staff/participant split in the parse, so the earlier staff scores for them saw the whole minutes body, and the discussion-track rows were patched from earlier analyses. Both sets of rows were replaced by fresh scores: 128 staff documents and 128 discussion documents, each scored by its own fresh agent (Sonnet-class, one document per agent, 256 agents in all; 12 of them were a pilot run with the same instructions), blind to any earlier score, under opaque IDs, with no agent seeing the other component of the same meeting. Staff rubric: the v4.1 text with its v4.2 addendum and the era anchors (project repository only; the shipped `rubrics/staff_scoring_rubric_v4.md` is the earlier v4 text); discussion: `rubrics/discussion_scoring_rubric_v4_1.md` plus `rubrics/discussion_scoring_clarifications_v4_1_1.md`. Replaced rows are marked by `STAFF_TEXT_SCOPE` = `minutes_staff_sections_split_2026-10` / `SCORE_VERSION` = `v4.1_split_2026-10` (staff) and `METHOD` = `fresh_blind_split_2026-10` / `INPUT_VERSION` = `member_discussion_split_2026-10-23` (discussion). The previous rows are not shipped; they are in the project backups (`publish_staging/v2.0.0_removed/_backups/pre_resplit_2026-10-24/`).

**How the inputs were made.** Paragraphs were extracted from the raw HTML (118 documents) and, for the ten minutes that exist only as PDF (2007-10-31 to 2008-12-16), from the PDF with column ordering and paragraph repair. Each paragraph was labelled by text anchors (the economic-review opener, the staff-forecast paragraph, the participants' discussion opener, the vote record) into front matter, desk report, staff review and forecast, participants' discussion, policy discussion, votes, directive, other business. The staff input is the staff review of the economy and of financial developments and the staff forecast. The discussion input is the participants' discussion, the policy discussion, the vote record and the decision text. The directive text is in neither input. Checks: every paragraph has exactly one label in all 128 documents; the two inputs share no sentence of six words or more; the boundary paragraphs of all 128 documents were read; recall against the raw source has median 1.000 (0.953-0.985 for the ten PDF documents). These are rule-based checks plus a read of each boundary, not a sentence-by-sentence human audit.

**Residual.** The staff input is not free of Committee content. The opening paragraph of the staff's financial review begins with a sentence recalling the previous meeting's directive, and some sentences name the Committee's views (about 5.3% of staff words; the strict version of the input removes them). 127 of 128 staff scorers flagged this in `ANOMALY_NOTE` (22 of 128 discussion scorers flagged something, mostly extraction artefacts). Most staff scorers said they ignored it; about 22 said they used market facts from the same paragraph. Where a scorer ignored the whole paragraph, a dimension whose only mention sat in it became N/A.

**Test of the residual (20 random meetings).** Each was scored twice more by fresh blind agents: once on the same staff input, once on the stricter input (Committee-attributing sentences removed). Mean absolute difference between scores, original vs repeat (scorer noise) / original vs strict / repeat vs strict: INFLATION_PRESSURE 3.05 / 2.45 / 2.30; OUTPUT_GAP 1.55 / 1.60 / 1.35; FINANCIAL_CONDITIONS 1.80 / 2.60 / 1.80. The mean shift from the full to the strict input was −0.7 (inflation), +0.1 (output gap), −0.6 (financial conditions). So the inputs differ by about as much as two scorings of the same input, and no contamination effect was detectable in this sample; with 20 meetings an effect of a few points on a single dimension cannot be excluded. Scorer noise of about 2 points per score applies to every pre-2009 score. The strict input is not cleaner in every respect: 16 of 20 scorers still flagged an anomaly, and removing sentences left some paragraphs without an antecedent.

**Changes against the previous rows.** Staff, 128 meetings: mean level 44.7 vs 44.8 (inflation), 47.0 vs 46.1 (output gap), 46.1 vs 41.3 (financial conditions); correlation of new with previous 0.89 / 0.95 / 0.91. Minutes-minus-transcript R² pre-2009 / 2009+: inflation pressure 0.56 / 0.83 (was 0.76 pre-2009), financial conditions 0.69 / 0.56 (0.79), credit spreads 0.49 / 0.74 (0.79), labour tightness 0.83 / 0.96 (0.90), output gap 0.81 / 0.94 (0.86). The pre-2009 CREDIT_SPREADS rows are now fresh scores under the level reading and have fewer scored cells (80 pairs against 94). Discussion: see the gaps in 3.2, which widen in the same direction as the vintage drift.

**Not done.** The scorers were not allowed to open other files, so none ran `tools/bright_line_check.py`; it was run on the finished tables (0 hard failures; 11 soft flags on the staff table, 27 on the discussion table; a coarse keyword screen over text that still contains the recap sentences). No human validation. One agent (2006-09-20 discussion) was stopped by an API safeguard error and the document was re-run with the same instructions. Code and outputs: project folder `15_minutes_split/` (`SPLIT_REPORT.md`, `rescore/`, `analyze_strict.py`, `apply_to_dataset.py`); not shipped.

---

## 6. How to Cite

### 6.1 Dataset Citation

When using this dataset in academic work, please cite as:

> Chen, Robin. (2026). *FedPriority: Model-Scored Measures of Federal Reserve Priorities, 1993-2026* [Data set]. openICPSR. https://doi.org/[DOI to be assigned upon deposit]. Dataset version 2.0.0 (draft, 2026-10-23).

### 6.2 Methodology Reference

If citing the scoring methodology specifically:

> Chen, Robin. (2026). Do FOMC Minutes Compress Information? Evidence from Three Independent Methods. *[Journal/Working Paper Series]*. [DOI/URL to be assigned].

### 6.3 Source Documents

The underlying FOMC documents are publications of the Board of Governors of the Federal Reserve System and require no citation for use. However, researchers should note the source:

> Board of Governors of the Federal Reserve System. FOMC Meeting Transcripts and Minutes, 1993–2026. Retrieved from https://www.federalreserve.gov/monetarypolicy/fomc_historical.htm

### 6.4 Rubric and Scoring Evidence

The scoring rubrics and per-document evidence files are released alongside the dataset. If the rubrics are used or adapted for other research:

> Chen, Robin. (2026). *FOMC Staff Assessment Scoring Rubric v4* and *FOMC Participant Discussion Scoring Rubric v3 (Independent)*. Supplementary materials to: [Paper citation above].

### 6.5 Funding

This dataset was developed with support from a Research Sponsorship Program (RSP) Capacity Building Grant at the University of Northern Iowa for the project "Revealed Federal Reserve Priorities: Developing AI Methods to Measure Policy Responses to Financial Conditions."

---

*For methodological details, including scoring design rationale and validation procedures, see METHODOLOGY.md.*
*For full validation evidence and QC reports, see VALIDATION_REPORT.md.*

## 4a. CURRENT checksums (2.0.0 DRAFT; recomputed 2026-10-23 with Python hashlib SHA-256; local working copy, not committed)

Files new or changed since the 1.3.0 table (2026-10-17): `staff_scores_v6.csv` (replaces `staff_scores_v4.csv`), `classified_sentences.csv` (`label_source` column added), and the new `meeting_key_map.csv`, `priority_variable_map.csv` and `staff_v6_minutes_vs_transcripts.csv`. The `meeting_registry.csv` and `meeting_variables.csv` hashes are identical to the 2026-10-17 table. **The `discussion_scores_v4_1.csv` hash differs from the 2026-10-17 value (`4492f8c4…ec837`)** although `CHANGELOG.md` [2.0.0] lists no change to it; the cause was not traced, so do not assume the file equals the 1.3.0 draft byte for byte (its row count is unchanged at 542). `discussion_v4_1_minutes_vs_transcripts.csv` was not hashed in earlier tables; its current hash is given for completeness. Backup copies (`*.bak*`) are not part of the release.

| File | SHA-256 |
|------|---------|
| `dataset/data/primary/staff_scores_v6.csv` | `33a75d462b4bdf763f72cad865c5fe0a69ba681bfef07a946767fd1fa1e51170` |
| `dataset/data/primary/discussion_scores_v4_1.csv` | `9909e71b9e736d8bdb5c63f407f985a169886fa1a49f1769a1bed734034c08cd` |
| `dataset/data/primary/meeting_registry.csv` | `6687fe5c0b46926019957e0742b26d51fd882c6e63f903071bb7905728548343` |
| `dataset/data/sentence_classification/classified_sentences.csv` | `c4f710a9d15a3c126be35885b5edb8c226f1811d22496340bf4ef3a20eced739` |
| `dataset/data/sentence_classification/meeting_variables.csv` | `7d79826292147909fd3b2c947edb5441561c690af1a555b81f97c42fb20df3a7` |
| `dataset/data/derived/meeting_key_map.csv` | `c1b714d95b8717e919650b2dbcd8ee8aadac9c2e2d928f51e8f57d1fbfd8d4e2` |
| `dataset/data/derived/priority_variable_map.csv` | `bda68b1a0728d1f931ed069c70ec416a951e57bd519883985ab26977783e2e9b` |
| `dataset/data/derived/staff_v6_minutes_vs_transcripts.csv` | `80ed8007b3f0f385c5f80e3628f6bca3e63724f5a53ef0df4ab7e98c31309c6d` |
| `dataset/data/derived/discussion_v4_1_minutes_vs_transcripts.csv` | `6af500fe3b3204d7b4bb93e0cc04c1a44aa151e952c2946acddcd026c5970804` |

### Added in 2.0.0: derived files and their sources

| File | Source and construction | Check |
|------|-------------------------|-------|
| `data/derived/priority_variable_map.csv` | Author's judgement: each score column assigned to price stability, maximum employment, financial stability or context (`priority_group`, `focus_role`). Not an estimated result | 22 variables |
| `data/derived/meeting_key_map.csv` | `02_registry/meeting_key_map.csv` (project repository) filtered to the shipped tables | 1,477 rows; see 1.3 |
| `data/derived/staff_v6_minutes_vs_transcripts.csv` | Same-date merge of minutes and transcript rows of `staff_scores_v6.csv`; diff = minutes minus transcript | 215 dates, 2,166 numeric pairs, 15 dimensions |
