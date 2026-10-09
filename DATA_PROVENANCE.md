# FOMC Document Scoring: Data Provenance

**Dataset version**: 2026-03
**Last updated**: 2026-03-30
**Scope**: FOMC minutes (1993–2026) and transcripts (1993–2020)

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
| Minutes | 265 | 1993–2026 |
| Transcripts | 273 | 1993–2020 |
| Statements | 241 | 1994–2026 |
| Press conferences | 90 | 2011–2026 |
| Testimonies | 62 | Selected |
| Speeches | ~2,886 | Selected |
| **Total raw documents** | **~3,816** | 1993–2026 |

### 1.3 Known Data Gaps and Anomalies

**Multi-day meeting dating**: Nine multi-day meetings have a date discrepancy between the minutes file (dated to the first day) and the transcript file (dated to the last day). These meetings are flagged in `meeting_registry.csv` with a `special_notes` entry. The discrepancy is ±1 day and does not affect content; the meeting registry cross-validation script uses a ±1-day tolerance to handle these cases.

**Pre-2005 minutes format**: Minutes published before approximately 2005 are not segmented into staff and participant sections. Section-level analysis relies on linguistic cues ("the staff reported," "members noted") to separate content types. This affects the precision of staff vs. discussion decomposition for early meetings.

**Emergency meetings**: Six emergency intermeeting actions are present in the corpus (September 2001, multiple 2008 actions, March 2020). These meetings have abbreviated documents. Scoring agents are instructed to use N/A liberally for such meetings and to flag them in the anomaly field.

---

## 2. Processing Pipeline

The full pipeline from raw documents to scored outputs runs through eleven stages. The table below presents the complete data lineage. Paths prefixed with `data/` or `scoring_evidence/` refer to the released dataset directory; paths like `01_acquisition/`, `02_registry/`, `03_decomposition/`, and `04_scoring/` refer to the project build environment and are not included in the dataset release.

| Stage | Input | Process | Output |
|-------|-------|---------|--------|
| 1. Acquisition | Federal Reserve website | PDF and HTML download via three acquisition scripts with rate limiting (1–2 second delay per request) | `01_acquisition/raw_documents/` (~3,816 files in 6 subfolders) |
| 2. Registry | Raw document folders | Meeting identification: scan all folders, match documents to calendar events, manual population of emergency events and rate decisions | `data/primary/meeting_registry.csv` (316 data rows) |
| 3. Decomposition | Raw documents | Section extraction by document type and era: minutes decomposed into staff_econ.txt, staff_fin.txt, participants_views.txt, policy_action.txt; transcripts into go_around_combined.txt, policy_discussion.txt; pre-2005 minutes produce unsegmented_body.txt | `03_decomposition/output/` (537 meeting folders, 18.6M tokens total) |
| 4. Cross-validation | Decomposed output + registry | Completeness check against registry, orphan detection (±1 day tolerance), metadata enrichment | `_metadata.json` for each of 537 meeting folders; 0 gaps confirmed |
| 5. Staff scoring V3 (legacy) | Meeting text files | LLM rubric V3 batched scoring — multiple documents processed sequentially by a single agent | `data/legacy/staff_scores_corrected_v3.csv` |
| 6. Correction pipeline | V3 scores | Manual audit of flagged scores; 6 systematic errors identified and corrected; correction log maintained | `data/derived/correction_log.csv` (564 corrections); corrected CSV |
| 7. Staff scoring V4 (canonical) | Meeting text files | LLM rubric V4 independent scoring — one fresh agent per document, no shared context; 15 dimensions; applied to 266 minutes and 216 transcripts | `data/primary/staff_scores_v4.csv` (482 scored documents) |
| 8. Discussion scoring V3 independent (canonical) | Meeting text files | LLM rubric V3 independent scoring — one fresh agent per document; 10 core + 10 optional dimensions; applied to 266 minutes and 273 transcripts | `data/primary/discussion_scores_v3.csv` (539 scored documents) |
| 9. Minutes-transcript comparison | Staff V4 + Discussion V3 scores | Paired gap analysis (minutes minus transcript) for all dimensions; paired t-tests; concordance correlation; era-level stratification | `data/derived/master_mechanisms.csv`, `scoring_evidence/meeting_comparisons/` |
| 10. Sentence classification (CDFSG) | Decomposed meeting text files | LLM sentence-level classifier using 7-category CDFSG taxonomy; applied to all transcripts and minutes 1993–2020 | `data/sentence_classification/classified_sentences.csv`, `meeting_variables.csv` |
| 11. Topic modeling (FASTopic) | Decomposed meeting text files | Unsupervised FASTopic modeling on 7 document corpora; topics mapped to 13 economic/financial categories | `data/topic_modeling/cross_corpus_matrix.csv`, per-corpus time series CSVs |

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

The decomposition script applies five era-specific extraction presets to handle format variation across the 33-year document history:

| Preset | Document type and era |
|--------|-----------------------|
| `greenspan_html` | Minutes 1993–2004 (HTML, unsegmented) |
| `modern_pdf` | Minutes 2005–present (PDF, segmented) |
| `transcript_regular` | Regular meeting transcripts (all eras) |
| `transcript_confcall` | Conference call transcript format |
| `transcript_emergency` | Emergency meeting transcript format |

A v2 decomposition script fixed an HTML extraction bug present in v1. All 537 output folders were regenerated using v2.

---

## 3. Version History

### 3.1 Staff Scoring

**V3 batched (superseded)**

- Location: `dataset/data/legacy/fomc_staff_scores_corrected.csv`
- Method: Single LLM agent processing multiple documents sequentially in batches
- Problem: Cross-meeting context contamination (260 contamination phrases identified in post-hoc audit); inflated minutes-transcript bias (+8.1 point mean gap, reduced to +1.7 under V4); inflated lag-1 autocorrelation
- Status: Archived. Not used in primary analyses. Retained for methodological comparison.

**V4 independent (canonical)**

- Location: `dataset/data/primary/staff_scores_v4.csv`
- Method: One fresh LLM agent per document; no shared context; no batching; 15 dimensions on 1–100 scale
- Changes from V3: New rubric with clarified anchor tables, improved bright-line rules for financial dimensions (BANKING_STRESS, TREASURY_STRESS, DOLLAR_STRENGTH), refined polarity guidance; independence mandate
- Contamination: Zero contamination phrases (verified by independence audit)
- Rubric: `dataset/rubrics/staff_scoring_rubric_v4.md`
- Evidence files: `scoring_evidence/staff_v4/batched/` (412 .md files: 194 minutes + 218 transcripts) and `scoring_evidence/staff_v4/independent/` (266 .md files, QA rescore of minutes only)
- Status: Canonical. Use this for all primary analyses.

### 3.2 Discussion Scoring

**V3 batched (superseded)**

- Location: `data/legacy/discussion_scores_v3_batched.csv`
- Method: Single LLM agent processing multiple documents sequentially
- Problem: Same contamination mechanism as V3 batched staff scoring; artificially inflated autocorrelation; subjective dimensions (DISSENT_INTENSITY, FINANCIAL_STABILITY_EMPHASIS, UNCERTAINTY_EXPRESSED) most affected
- Status: Archived. Retained for methodological comparison only.

**V3 independent (canonical)**

- Location: `dataset/data/primary/discussion_scores_v3.csv`
- Method: One fresh LLM agent per document; no shared context; 10 core + 10 optional dimensions
- Key finding: Minutes-transcript gaps in DISSENT (−9.7), FSE (−11.3), and UNCERTAINTY (−5.2) persist and strengthen under independent scoring, confirming they are real editorial compression effects
- Rubric: `dataset/rubrics/discussion_scoring_rubric_v3.md`
- Evidence files: `scoring_evidence/discussion_v3/minutes/` (266 .md files) and `scoring_evidence/discussion_v3/transcripts/` (273 .md files)
- Status: Canonical. Use this for all primary analyses.

**V4.1 (proposed recommended file for discussion scores; pending release)**

- Location: `data/primary/discussion_scores_v4_1.csv`
- Method: transcripts scored fresh, one fresh LLM agent per document, on rebuilt inputs (`member_discussion_v2`; `v2b` for 71 re-scored meetings); minutes: the earlier V4 analyses patched by one fresh agent per meeting against the rebuilt input and a text diff. 20 dimensions, including five discussion dimensions. Rubric: `rubrics/discussion_scoring_rubric_v4_1.md` plus `rubrics/discussion_scoring_clarifications_v4_1_1.md`.
- Checks: blind second pass on 381 minutes cells (`data/derived/discussion_v4_1_second_pass_check.csv`); 36 cells set to N/A afterwards. Blind re-check of the 27 first-run transcript CREDIT_SPREADS `N/A` cells under the V4.1.1 clarifications: 16 now scored at Low confidence (`CREDIT_UPDATE` column; `data/derived/discussion_v4_1_credit_update_log.csv`).
- Evidence files: `scoring_evidence/discussion_v4_1/`
- Limits: see `codebooks/CODEBOOK_discussion_scores_v4_1.md`. V3 independent remains available and unchanged.

### 3.3 Compatibility Note

V3 batched and V4/V3-independent scores are *not* interchangeable. The version transition involves both rubric improvements (V3→V4 for staff) and a methodological change (batched→independent for both). Correlation between old and new scores varies by dimension: core economic dimensions correlate at r = 0.85–0.97; financial sub-dimensions and subjective dimensions show more change due to rubric clarification and contamination removal. See `validation/COMPARISON_SYNTHESIS.md` for full dimension-level comparison statistics.

---

## 4. File Checksums (SHA-256)

The following checksums were computed from the canonical primary data files as of 2026-03-30. These allow verification that primary files have not been modified after this date.

| File | SHA-256 |
|------|---------|
| `dataset/data/primary/staff_scores_v4.csv` | `de2978e7c7c2384e2b7b101d2219a129cf426255449b5994da4d1346e471b757` |
| `dataset/data/primary/discussion_scores_v3.csv` | `a24ffc911e68b18dcc2676988b5dbe2e2f15e7daae7c27bc93e2e0c32126fcd0` |
| `dataset/data/primary/meeting_registry.csv` | `894902febbf42359749e1db92c63ff7e466be9eff263e5b5f4f373fec562c93a` |

The two files below were **republished 2026-09-27** to fix a parser bug and a missing
speaker-attribution field (see `dataset/CHANGELOG.md` [1.1.0]); their checksums reflect
that date, not 2026-03-30. Previous versions are kept alongside them as
`*.bak_2026-09-27_pre_speaker_fix`.

| File | SHA-256 |
|------|---------|
| `dataset/data/sentence_classification/classified_sentences.csv` | `d1b40931159ef5906af6cfd95e5c024bbc9930ef185f0fb52eb18ff7d82ca1aa` |
| `dataset/data/sentence_classification/meeting_variables.csv` | `0120e2bfcba14b6d6c8f549333ef1e406a6f4ab7f22e592d8276dd3241564b5c` |

The V4.1 discussion file added in 1.2.0 (checksum computed when the review package was built; recompute if the file is regenerated):

| File | SHA-256 |
|------|---------|
| `dataset/data/primary/discussion_scores_v4_1.csv` | `43659f3135e4f0948390146490b8a2c3aa48ef0ef8a6b9c11cd319f53f337a3d` |

(The checksum above was recomputed on 2026-10-08 after the CREDIT_SPREADS update; the file built for review had `383fb88d…f497`.)

To verify a file after download:

```python
import hashlib
path = "dataset/data/primary/staff_scores_v4.csv"
print(hashlib.sha256(open(path, 'rb').read()).hexdigest())
```

---

## 5. Data Quality

Full quality control evidence is documented in VALIDATION_REPORT.md. Summary metrics are provided here.

### 5.1 Staff Scoring Quality

A cumulative validation pass assessed every scored *dimension* (not file) as VALID, QUESTIONABLE, or INCORRECT using tolerance thresholds of ±5 points (VALID), ±6–12 points (QUESTIONABLE), or >12 points / wrong direction (INCORRECT). Results across ~481 files:

| Quality tier | Dimension-checks | Share | Notes |
|--------------|-----------------|-------|-------|
| VALID | ~2,734 | ~73% | Score within ±5 points of rubric anchor |
| QUESTIONABLE | ~809 | ~22% | Score within ±6–12 points; plausible but wider uncertainty |
| INCORRECT | ~183 | ~5% | Score direction or magnitude clearly unsupported; corrected |

Source: `scoring_cumulative_validation_report.md` (04_scoring/staff/docs/). All INCORRECT-flagged dimension-scores were corrected before inclusion in the canonical `staff_scores_v4.csv`. The correction log is at `data/derived/correction_log.csv` (564 corrections across 5 dimensions: TREASURY_STRESS 214, LABOR_TIGHTNESS 144, DOLLAR_STRENGTH 102, BANKING_STRESS 75, FINANCIAL_CONDITIONS 29; note: the correction log uses the original V3 column names DOLLAR_FX and BANKING_HEALTH, which were renamed in V4). Of 482 scored files, 317 received at least one correction.

### 5.1b Discussion Scoring Anomaly Flags

Anomaly flags: 167 of 538 scored discussion documents (31%) carry an anomaly flag. Anomaly flags indicate unusual meeting circumstances (emergency actions, special-topic meetings, very short documents, dominant speakers) rather than errors. Flagged documents are retained in the canonical file with the anomaly description in the `ANOMALY_NOTE` column.

### 5.2 Discussion Scoring Reproducibility

A validation audit re-scored 16 documents using independent agents to assess intra-method reproducibility:

- Mean absolute deviation (MAD): **1.9 points** on the 1–100 scale
- Direction errors (score crosses 50 in opposite direction): **zero**
- Dimension-level stability: highest MAD observed for FINANCIAL_STABILITY_EMPHASIS (7.2) and DISSENT_INTENSITY (5.7); these dimensions also carry wider uncertainty bands by rubric design, reflecting the inherently more subjective nature of these constructs

### 5.3 Independence Confirmation

The independence audit examined scored .md evidence files for phrases indicating cross-meeting memory:

| Scoring approach | Contamination phrases found |
|------------------|-----------------------------|
| Old batched (V3) | 260 phrases across scoring runs |
| New independent (V4/V3-ind) | 0 phrases (verified) |

No scored .md file from the independent runs contains language comparing the current meeting to a prior meeting, referencing prior scores, or invoking sequential reasoning across meetings.

### 5.4 Staff V4 Minutes-Transcript Concordance

For paired meetings where both minutes and transcripts were scored (N varies by dimension from 49 to 166 depending on data availability; core economic dimensions have N = 164–166):

| Dimension | r | MAD | Bias (min−trans) |
|-----------|---|-----|------------------|
| LABOR_TIGHTNESS | 0.977 | 2.2 | +0.3 |
| OUTPUT_GAP | 0.963 | 2.2 | +0.1 |
| INFLATION_PRESSURE | 0.926 | 3.2 | −0.6 |
| CONSUMPTION_INVESTMENT | 0.925 | 3.3 | +1.1 |
| FINANCIAL_CONDITIONS | 0.888 | 5.5 | −1.7 |
| CREDIT_SPREADS | 0.922 | 5.5 | −1.0 |
| BANKING_STRESS | 0.936 | 4.7 | −0.0 |

High concordance (r > 0.88) with near-zero bias across all core dimensions confirms that the V4 rubric scores the same economic content consistently regardless of whether it appears in minutes or transcript form.

---

## 6. How to Cite

### 6.1 Dataset Citation

When using this dataset in academic work, please cite as:

> Chen, Robin. (2026). *FOMC Document Scoring Dataset: LLM-Based Rubric Scoring of Federal Reserve Meeting Records, 1993–2026* [Data set]. openICPSR. https://doi.org/[DOI to be assigned upon deposit]. Dataset version 2026-03.

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
