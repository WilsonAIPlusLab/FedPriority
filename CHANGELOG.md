# Changelog

All notable changes to this dataset will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
