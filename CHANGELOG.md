# Changelog

All notable changes to this dataset will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.2.0] — 2026-10-08

### Added — Discussion scoring V4.1

- **`data/primary/discussion_scores_v4_1.csv`** (537 rows): participant-discussion scores on the V4.1 rubric
  (15 shared dimensions plus five discussion dimensions, hawkish/dovish lean, dissent intensity, financial-stability emphasis,
  forward-guidance tone and uncertainty expressed). Transcript rows (272) are fresh scores, one fresh agent per
  meeting, on rebuilt inputs; 71 were re-scored under the V4.1.1 clarifications. Minutes rows (265) are a patch of the earlier V4
  analyses, not fresh scores. Row-level provenance columns: `METHOD`, `RUBRIC_VERSION`, `INPUT_VERSION`, `MODEL_EXCEPTION`, `NA_DECISION_CELLS`.
- Rebuilt member-discussion inputs: the first-pass inputs had staff text inside member input, cut-off vote records and wrong go-around
  starts. Transcripts now hold all member and participant turns (First Vice Presidents and acting presidents included); minutes hold the
  participants' views and the vote record.
- `rubrics/discussion_scoring_rubric_v4_1.md`, `rubrics/discussion_scoring_clarifications_v4_1_1.md`, `codebooks/CODEBOOK_discussion_scores_v4_1.md`.
- `data/derived/discussion_v4_1_*`: matched-pair gaps, minutes patch log, blind second-pass check, transcript re-score diff, N/A decision log.
- `scoring_evidence/discussion_v4_1/`: per-document agent outputs (272 transcripts, 265 minutes patches, 216 second-pass files).
- `code/discussion_v4_1/`: provenance scripts (not a stand-alone pipeline).

### Changed
- 36 minutes cells that a blind second pass scored N/A were set to N/A (24 EQUITY_VALUATION, 9 CREDIT_SPREADS, 3 others); each is logged with its old value.
- 16 first-run transcript CREDIT_SPREADS cells that were `N/A` now carry a Low-confidence score from a blind re-check under the V4.1.1 clarifications (27 first-run `N/A` cells were re-checked; 11 stay `N/A`). New column `CREDIT_UPDATE` marks them; log in `data/derived/discussion_v4_1_credit_update_log.csv`, check outputs in `scoring_evidence/discussion_v4_1/credit_update/`. Seven new CREDIT_SPREADS pairs were added to `discussion_v4_1_minutes_vs_transcripts.csv`.
- V3 discussion scores (`discussion_scores_v3.csv`) are kept unchanged for comparison.

### Known limits
- All scorers are LLM agents of one model family; no human coding.
- Minutes rows are patched, so cells the patch left UNCHANGED partly rest on the earlier analysis; the second pass found closely matching values (mean absolute difference 3.8) but 9% of checked cells would not be scored blind.
- 12 transcripts were scored on Opus; the models of minutes-patch agents were not tracked per document.
- The re-scored transcripts omit Part 1 reasoning in their evidence files.
- Minutes-minus-transcripts gaps on 224 matched pairs: dissent -8.3, financial stability -13.3, uncertainty -5.0.

## [1.1.0] — 2026-09-27

### Fixed — Sentence Classification

- **`data/sentence_classification/classified_sentences.csv`** rebuilt from scratch to fix
  three defects in the prior corpus:
  - A duplicate-paragraph bug in `parse_documents.py`'s speech parser (`BeautifulSoup`
    with `html.parser` silently nested `<p>` tags on older Fed speech HTML that omits
    closing tags, causing each sentence to be emitted once per enclosing paragraph).
    Fixed by switching to `lxml`. Verified against a documented worked example
    (2009-04-20 Kohn speech: 532 duplicated rows → 162 correct rows).
  - A carry-forward bug in `build_decomposed_sentences.py` that matched unchanged
    minutes/transcript sentences against a source file with no label columns, silently
    producing 47,173 blank-labeled rows. Labels are now correctly reattached from the
    prior classified corpus.
  - **Missing speaker attribution for non-crisis transcripts.** ~91% of transcript rows
    (all meetings outside the 2007–2009 crisis window) previously had blank `speaker` /
    `speaker_role`, because the decomposition pipeline tokenized each component file
    directly without first splitting it into speaker turns. Transcripts are now
    re-segmented by speaker turn (reusing the same speaker-detection convention as the
    crisis-era parser) before tokenization. 96.6% of resulting sentences carried forward
    their existing label via exact-text match; the remaining 3.4% (13,732 sentences,
    whose text changed at the new turn boundaries) were freshly classified. Every
    transcript row now has a non-blank `speaker`.
  - Net effect: 394,127 → 526,516 rows (562,194 after the parser/carry-forward fixes
    alone, then −35,678 as the corrected speaker-turn tokenization dropped noise rows
    the old naive tokenizer had counted as sentences — e.g. header/divider-only
    fragments).
  - Added `confidence_raw`: the classifier's original confidence value verbatim (some
    older rows carry a raw 0–1 score rather than a HIGH/MEDIUM/LOW category).
    `confidence` continues to hold the normalized HIGH/MEDIUM/LOW category as before
    (thresholds: ≥0.8 HIGH, 0.6–0.79 MEDIUM, <0.6 LOW for numeric sources).
- **`data/sentence_classification/meeting_variables.csv`** recomputed from the corrected
  corpus: 394 → 440 meeting rows. The increase reflects meetings/sessions that were
  previously absent or miscounted in the stale corpus, not new source documents.
- Previous published versions of both files are retained as
  `*.bak_2026-09-27_pre_speaker_fix` for comparison.
- See `06_cdfsg_pipeline/merge_final.py`, `build_transcript_speakers.py`, and
  `build_final_with_speakers.py` for the full rebuild logic.

### Fixed — Primary Data

- Removed the duplicate **2012-10-24 minutes** row from `data/primary/discussion_scores_v3.csv` and
  `data/primary/staff_scores_v4.csv`. It was a second copy of the 2012-10-23 minutes (the registry holds
  one meeting, 2012-10-23, ending 2012-10-24); its scores differed from the 2012-10-23 row only by sampling
  noise. Row counts are now 538 (discussion) and 481 (staff), 265 minutes in each; the 1.0.0 entries below
  give the original counts (539 and 482). The 2012-10-24 *transcript* rows are kept (transcripts are keyed by
  the end date). The evidence file `minutes_2012-10-24.md` remains in `scoring_evidence/discussion_v3/minutes/`
  and `scoring_evidence/staff_v4/independent/` (266 files each).

## [1.0.0] — 2026-03-30

### Added — Primary Data
- `data/primary/staff_scores_v4.csv`: 482 scored documents (minutes and transcripts), 15 staff assessment dimensions, V4 independent scoring methodology
- `data/primary/discussion_scores_v3.csv`: 539 scored documents, 10 core + 10 optional participant discussion dimensions, V3 independent scoring
- `data/primary/meeting_registry.csv`: 316 FOMC events, 1993–2026

### Added — Derived Data
- `data/derived/master_mechanisms.csv`: 216 meetings with compression mechanism coding across dissent, financial stability, and uncertainty dimensions
- `data/derived/correction_log.csv`: 564 score corrections with audit trail (dimension, original, corrected, delta, rule applied)
- `data/derived/minutes_vs_transcripts.csv`: Staff score gap analysis for 171 matched meeting pairs
- `data/derived/concordance_summary.csv` and `concordance_by_era.csv`: Cross-document concordance by era

### Added — Sentence Classification
- `data/sentence_classification/classified_sentences.csv`: ~394,000 classified sentences, 394 meetings
- `data/sentence_classification/meeting_variables.csv`: 394-row meeting-level CDFSG index
- `data/sentence_classification/all_sentences_scored.csv`: 70,635 sentences from 17 crisis-period meetings with additional dictionary scores

### Added — Topic Modeling
- Four FASTopic output files covering cross-corpus comparison and economic ratio timeseries

### Added — Scoring Evidence
- 412 staff V4 batched scored .md files (canonical audit trail for staff_scores_v4.csv)
- 266 staff V4 independent scored .md files (QA validation rescore, minutes only)
- 266 discussion V3 scored minutes .md files
- 273 discussion V3 scored transcript .md files
- 216 meeting comparison .md files

### Added — Documentation
- METHODOLOGY.md, DATA_PROVENANCE.md, VALIDATION_REPORT.md
- 5 codebooks (staff scores, discussion scores, meeting registry, sentence classification, mechanisms)
- LICENSE.md (CC-BY-4.0), CHANGELOG.md

### Added — Analysis
- DEEP_INSIGHTS_FINAL_v2.md: Full-sample capstone synthesis (216 meetings)
- full_coverage_synthesis.md, frequency_tables.md: Mechanism prevalence statistics
- synthesis_historical.md: Chair-era qualitative analysis
- 20 full-coverage batch files, 21 Q-analysis batch files

### Legacy Data (superseded)
- `data/legacy/staff_scores_corrected_v3.csv`: V3 batched staff scores with corrections applied
- `data/legacy/discussion_scores_v3_batched.csv`: V3 batched discussion scores
- These are retained for methodological comparison only. Use V4/V3-independent versions for analysis.
