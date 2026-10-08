# Changelog

All notable changes to this dataset will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
