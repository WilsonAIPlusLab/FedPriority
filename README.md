# FOMC Minutes-Transcript Scoring Dataset, 1993–2020

## Overview
This dataset contains LLM-generated scores of Federal Open Market Committee (FOMC) meeting documents — both the published minutes and the underlying transcripts — enabling systematic measurement of editorial compression in FOMC communication. The central finding is that transcripts show systematically more dissent (−9.7 pts), financial stability emphasis (−11.3 pts), and expressed uncertainty (−5.2 pts) than published minutes across 216 matched meeting pairs from 1993–2020 (V3 scoring). The V4.1 re-scoring (see `data/primary/discussion_scores_v4_1.csv`) gives the same direction on 224 matched pairs: minutes minus transcripts of -8.3 (dissent), -13.3 (financial stability emphasis) and -5.0 (uncertainty); both scorings use the same model family, so they are not independent confirmations.

## Dataset at a Glance

| Item | Value |
|------|-------|
| Meetings covered (matched pairs) | 216 |
| Staff assessment scores | 481 documents (265 minutes + 216 transcripts), 15 dimensions |
| Discussion scores (V3) | 538 documents (265 minutes + 273 transcripts), 10 core + 10 optional dimensions |
| Discussion scores (V4.1) | 537 documents (272 transcripts + 265 minutes), 20 dimensions |
| Classified sentences | 526,516 sentences, 440 meetings |
| Compression mechanism coding | 216 meetings, 20 columns |
| Temporal coverage (minutes) | 1993–2026 |
| Temporal coverage (transcripts) | 1993–2020 |
| FOMC chairs | Greenspan (1993–2006), Bernanke (2006–2014), Yellen (2014–2018), Powell (2018–2026) |

## Folder Structure

```
dataset/
├── data/primary/          ← Start here: 3 canonical CSVs
├── data/derived/          ← Analytical outputs (mechanisms, concordance, corrections)
├── data/sentence_classification/ ← Method B: ~527K classified sentences
├── data/topic_modeling/   ← Method C: FASTopic outputs
├── data/legacy/           ← Superseded V3 batched scores (audit trail)
├── scoring_evidence/      ← ~1,433 .md files with LLM reasoning behind each score
├── rubrics/               ← The scoring instruments used
├── validation/            ← QC reports and inter-rater reliability evidence
├── analysis/              ← Deep pattern analysis and synthesis documents
├── codebooks/             ← Variable-level documentation for each CSV
├── code/                  ← Scoring and classification scripts
└── dictionaries/          ← Text analysis dictionaries (Correa FSS, LM, Peek FI)
```

## Primary Data Files

| File | Rows | Description | Codebook |
|------|------|-------------|----------|
| data/primary/staff_scores_v4.csv | 481 | Staff assessment scores, 15 dims, minutes + transcripts | codebooks/CODEBOOK_staff_scores.md |
| data/primary/discussion_scores_v3.csv | 538 | Participant discussion scores, 10+10 dims (V3; kept) | codebooks/CODEBOOK_discussion_scores.md |
| data/primary/discussion_scores_v4_1.csv | 537 | Participant discussion scores, V4.1: 20 dims; transcripts fresh, minutes patched | codebooks/CODEBOOK_discussion_scores_v4_1.md |
| data/primary/meeting_registry.csv | 316 | FOMC event registry | codebooks/CODEBOOK_meeting_registry.md |

## Derived and Supplementary Data Files

| File | Rows | Description | Codebook |
|------|------|-------------|----------|
| data/derived/master_mechanisms.csv | 216 | Per-meeting compression mechanism coding | codebooks/CODEBOOK_mechanisms.md |
| data/derived/correction_log.csv | 564 | Audit trail for all score corrections | — |
| data/derived/minutes_vs_transcripts.csv | 1,532 | Staff score gaps (long format: ~170 meetings × 9 dimensions) | — |
| data/derived/discussion_v4_1_minutes_vs_transcripts.csv | 3,129 | Discussion V4.1 gaps (long format, 224 matched pairs × 20 dimensions) | — |
| data/derived/discussion_v4_1_minutes_patch_log.csv | 5,300 | Per-cell log of the minutes patch (UNCHANGED / FILLED / CORRECTED) | — |
| data/derived/discussion_v4_1_second_pass_check.csv | 381 | Blind second pass versus patched minutes values | — |
| data/derived/discussion_v4_1_transcript_rescore_diff.csv | 1,340 | V4.1 versus V4.1.1 transcript re-score, by meeting and dimension | — |
| data/derived/discussion_v4_1_na_decision_log.csv | 36 | Minutes cells set to N/A after the second pass | — |
| data/derived/discussion_v4_1_credit_update_log.csv | 27 | Transcript CREDIT_SPREADS cells that were N/A in the first run and were re-checked blind: 16 now scored (Low confidence), 11 kept N/A | — |
| data/sentence_classification/classified_sentences.csv | 526,516 | Sentence-level CDFSG topic classification | codebooks/CODEBOOK_sentence_classification.md |
| data/sentence_classification/meeting_variables.csv | 440 | Meeting-level CDFSG index | codebooks/CODEBOOK_sentence_classification.md |
| data/topic_modeling/cross_corpus_matrix.csv | — | Topic model corpus-level comparison | — |

## Scoring Evidence Files

The scoring_evidence/ folder contains ~1,433 Markdown files — one per scored document — preserving the LLM's chain-of-thought reasoning, verbatim evidence quotes, and structured output behind every CSV row. These files are the primary audit trail.

| Subfolder | Count | Contents |
|-----------|-------|----------|
| scoring_evidence/staff_v4/batched/ | 412 | Staff V4 scores (canonical source for staff_scores_v4.csv) |
| scoring_evidence/staff_v4/independent/ | 266 | Independent QA rescore (minutes only) |
| scoring_evidence/discussion_v3/minutes/ | 266 | Discussion scores for minutes |
| scoring_evidence/discussion_v3/transcripts/ | 273 | Discussion scores for transcripts |
| scoring_evidence/discussion_v4_1/transcripts/ | 272 | V4.1 / V4.1.1 transcript scores (re-scored files omit the Part 1 reasoning) |
| scoring_evidence/discussion_v4_1/minutes_patched/ | 265 | V4.1 minutes patch analyses |
| scoring_evidence/discussion_v4_1/second_pass/ | 216 | Blind second-pass cell scores |
| scoring_evidence/discussion_v4_1/credit_update/ | 27 + procedure | Blind CREDIT_SPREADS / EQUITY_VALUATION check outputs for the 27 first-run N/A transcripts (`PROCEDURE.md` is the instruction file) |
| scoring_evidence/meeting_comparisons/ | 216 | Side-by-side minutes-vs-transcript comparisons |

The two minutes folders (`discussion_v3/minutes/`, `staff_v4/independent/`) hold 266 files each, one more than the 265 minutes rows in the primary tables: `minutes_2012-10-24.md` scores a duplicate copy of the 2012-10-23 minutes, and its row was removed from the primary tables in 1.1.0.

## Methodology Summary

Three independent methods were used for triangulation:

- **Method A (LLM Rubric Scoring)**: Each document scored by a fresh LLM agent (no cross-meeting context) using a calibrated rubric with 15 staff dimensions and 10+10 discussion dimensions. Scores are continuous 1–100 with uncertainty bands and confidence tiers.
- **Method B (CDFSG Sentence Classification)**: 526,516 sentences classified into 7 economic/financial topic categories, with per-speaker attribution on transcript sentences. The CDFSG index measures the gap in financial stability emphasis between transcripts and minutes.
- **Method C (FASTopic Topic Modeling)**: Unsupervised topic modeling across 7 FOMC document corpora for cross-method convergence validation.

See METHODOLOGY.md for full details.

## Validation Summary

| Procedure | Result |
|-----------|--------|
| Independence audit (staff V4) | PASS — 0 contamination phrases; lag-1 autocorrelation reduced from 0.818 to 0.690 |
| Staff score quality | ~73% VALID, ~22% QUESTIONABLE, ~5% INCORRECT at dimension level; all INCORRECT corrected |
| Staff concordance (minutes vs. transcript, core dims) | r = 0.925–0.977 |
| Discussion reproducibility (MAD across 16 re-scores) | 1.9 points |
| Direction errors in 628 dimension-checks | 0 |
| Model-model kappa (not human-validated) | 8/8 dimensions ≥ 0.60 |
| Cross-method convergence (B vs. C, financial) | ρ = 0.587 |

See VALIDATION_REPORT.md for full details.

## Computational Requirements

| Item | Detail |
|------|--------|
| Language | Python 3.10+ |
| Dependencies | See code/requirements.txt |
| LLM API | Claude API (Anthropic); models: claude-sonnet-4-6, claude-opus-4-6 |
| Scoring cost | Sentence classification: ~$26; staff/discussion scoring: ~$180 total |
| Reproducibility note | LLM scoring is stochastic; scored .md evidence files + rubrics serve as reproducibility mitigation |

## Loading the Data (Python)

```python
import pandas as pd

staff = pd.read_csv("data/primary/staff_scores_v4.csv")
discussion = pd.read_csv("data/primary/discussion_scores_v3.csv")
registry = pd.read_csv("data/primary/meeting_registry.csv")

# Compute staff minutes-transcript gap for a dimension
mins = staff[staff["SOURCE_TYPE"] == "minutes"].set_index("MEETING_DATE")
trans = staff[staff["SOURCE_TYPE"] == "transcript"].set_index("MEETING_DATE")
fc_gap = trans["FINANCIAL_CONDITIONS"] - mins["FINANCIAL_CONDITIONS"]

# Compute discussion dissent gap
disc_mins = discussion[discussion["SOURCE_TYPE"] == "minutes"].set_index("MEETING_DATE")
disc_trans = discussion[discussion["SOURCE_TYPE"] == "transcript"].set_index("MEETING_DATE")
dissent_gap = disc_trans["DISSENT_INTENSITY"] - disc_mins["DISSENT_INTENSITY"]
```

## Source Data Availability

Raw FOMC documents (minutes, transcripts) are not included. They are publicly available:
- Historical transcripts and minutes: https://www.federalreserve.gov/monetarypolicy/fomc_historical.htm
- Current calendars and minutes: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm

## Citation

If you use this dataset, please cite:
```
Chen, Robin. (2026). FOMC Minutes-Transcript Scoring Dataset, 1993-2020 [Data set].
openICPSR. https://doi.org/[DOI to be assigned upon deposit]
```

## Funding

This dataset was developed with support from a Research Sponsorship Program (RSP) Capacity Building Grant at the University of Northern Iowa for the project "Revealed Federal Reserve Priorities: Developing AI Methods to Measure Policy Responses to Financial Conditions." The dataset extends the scope of the original grant to include additional scoring dimensions, multiple independent analytical methods, and minutes coverage through 2026. The research is motivated by the question of whether the Federal Reserve treats financial stability as an implicit third mandate alongside its statutory dual mandate of maximum employment and stable prices (Cieslak and Vissing-Jorgensen 2021; Powell 2023).

## Note on Column Naming

The primary CSVs use different column name conventions:
- `staff_scores_v4.csv` and `discussion_scores_v3.csv` use **UPPERCASE** (e.g., `MEETING_DATE`, `SOURCE_TYPE`)
- `meeting_registry.csv` uses **lowercase** (e.g., `meeting_date`, `chair`)
- `master_mechanisms.csv` uses **UPPERCASE** with `DATE` (not `MEETING_DATE`)

When joining across files, use case-insensitive matching or rename columns accordingly.

## License

CC-BY-4.0. See LICENSE.md.
