# Changelog

All notable changes to this dataset will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [2.0.0] DRAFT — 2026-10-23, updated 2026-10-24 (local commits only; not pushed, not published)

Re-focus on the priorities (price stability, maximum employment, financial stability) and removal of components that are not validated or are superseded. The 1.3.0 draft changes below are all included. Removed files were moved to `publish_staging/v2.0.0_removed/` in the project repository (same relative paths); they remain in the public GitHub history of v1.0.0.

### Added
- `data/primary/staff_scores_v6.csv` (495 rows: 270 minutes + 225 transcripts; transcripts re-scored on repaired text; `SCORE_VERSION` column). Replaces `staff_scores_v4.csv`, which differed in 84–139 of 486 shared rows per main dimension.
- `data/derived/staff_v6_minutes_vs_transcripts.csv`: 215 same-date pairs, 2,231 numeric pairs, minutes minus transcript (2,166 after the 2026-10-24 re-score of the pre-2009 minutes, see below).
- `data/derived/priority_variable_map.csv`: variable → price stability / employment / financial stability / context (author's judgement).
- `label_source` column in `classified_sentences.csv`: 7,979 `keyword_script` rows (transcript 5,118; speech 2,448; minutes 413), rest `llm_presumed`. Source list: project `docs/keyword_labelled_rows_2026-10-17.csv`. `meeting_variables.csv` was not recomputed.
- `validation/README.md` stating which reports describe earlier tables.

### Removed (reason)
- `data/derived/master_mechanisms.csv`, `CODEBOOK_mechanisms.md`, `analysis/` (narratives and 41 batch files), `scoring_evidence/meeting_comparisons/`: hand-typed gap columns correlate 0.26 / 0.09 / 0.25 with the V4.1 gaps; REGIME rule and generating inputs unverifiable; some case-study quotes shown wrong; not a priority measure.
- `data/primary/discussion_scores_v3.csv`, `CODEBOOK_discussion_scores.md`, `scoring_evidence/discussion_v3/`, `data/legacy/`, `data/derived/correction_log.csv`, `concordance_*.csv`, `removed_rows_log_2026-10-17.csv`, `validation/{concordance_report,deep_analysis_results,v3_validation_summary}.md`: superseded V3 scoring (the correction log and concordance files use V3 dimension names such as BANKING_HEALTH, DOLLAR_FX, FINANCIAL_TIGHTNESS that do not exist in the current tables).
- `data/supplementary/` (2026 statement, press-conference, Beige Book, speech FSAI scores): later vintage, 4–61 rows each, three Beige values steered by a stated rule, no review.
- `econclasshub/` (website application, not data), all `*.bak*` backup files.

### Changed
- Documents rewritten or patched for the new scope: README, CHANGELOG, METHODOLOGY, DATA_PROVENANCE, VALIDATION_REPORT, codebooks.
- The discussion minutes patch `v2d` (2000-12-19 HAWKISH_DOVISH_LEAN 42, not 38) was already in the shipped V4.1 table and gap file; the README no longer calls it pending.

### Added after the first 2.0.0 commit (2026-10-23)
- `STAFF_TEXT_SCOPE` column in `staff_scores_v6.csv` (now 43 columns): `minutes_full_body_incl_participant_discussion` (128 rows, minutes 1993-2008; these rows were replaced on 2026-10-24, see "Re-scored pre-2009 minutes" below), `minutes_staff_sections_only` (142 rows, 2009-2026), `transcript_staff_turns_not_fully_audited` (225 rows). `minutes_text_scope` column in `data/derived/staff_v6_minutes_vs_transcripts.csv`.
- Audit of the parsed text: for 1993-2008 minutes the staff and participant components are empty in the parse (no split), and the discussion-track input is fully contained in the staff-track input (median overlap 100%; 2009+ median 0%).
- [Superseded by [2.0.0] item "Re-scored pre-2009 minutes" below: these figures describe the pre-2009 minutes scored on the whole body.] Staff minutes-versus-transcript R-squared / mean gap (minutes minus transcript), pre-2009 vs 2009+ pairs: labour tightness 0.90 / 0.96; output gap 0.86 / 0.94; inflation pressure 0.76 (-2.8) / 0.83 (-1.4); financial conditions 0.79 (-2.5) / 0.56 (+1.1); equity valuation 0.27 (+3.0) / 0.70 (+2.4); treasury stress 0.42 / 0.34; credit spreads 0.79 / 0.74. Pre-2009 pairs are contaminated, so their agreement is not a clean staff-content measure; the 2009+ column is the clean one. Not tested: the effect of the contamination on scores.

### Re-scored pre-2009 minutes (2026-10-24)
- Rebuilt the staff / discussion separation of the 128 minutes of 1993-2008 (118 from raw HTML, 10 from PDF; rule-based labelling by text anchors, every boundary read) and re-scored both components blind, one fresh agent per document and component (256 agents; a 12-agent pilot was part of them).
- `data/primary/staff_scores_v6.csv`: the 128 pre-2009 minutes rows replaced (`STAFF_TEXT_SCOPE` = `minutes_staff_sections_split_2026-10`, `SCORE_VERSION` = `v4.1_split_2026-10`). Previously `minutes_full_body_incl_participant_discussion`.
- `data/primary/discussion_scores_v4_1.csv`: the 128 pre-2009 minutes rows replaced (`METHOD` = `fresh_blind_split_2026-10`, `INPUT_VERSION` = `member_discussion_split_2026-10-23`, `RUBRIC_VERSION` v4.1 with the V4.1.1 clarifications). Previously patched scores (`patch_of_v4_analysis`, 265 to 137 rows). The 36 N/A decisions and the credit update in those rows no longer apply to them.
- Derived gap tables rebuilt for the pre-2009 pairs by the same procedure (checked: the builder reproduced the previous tables exactly before the replacement); 2009+ rows unchanged. `staff_v6_minutes_vs_transcripts.csv`: 2,166 numeric pairs (was 2,231; fewer where a scorer returned N/A), `minutes_text_scope` = `staff_sections_split_2026-10` for the pre-2009 rows. `discussion_v4_1_minutes_vs_transcripts.csv`: 3,125 rows (was 3,129).
- Headline changes (all minutes minus transcripts): staff FINANCIAL_CONDITIONS +1.6 (was -0.9; sign changed), OUTPUT_GAP -0.3 (was -0.8), INFLATION_PRESSURE -2.2 (unchanged); discussion FSE -15.1 (was -13.3), dissent -10.8 (-8.3), uncertainty -7.2 (-5.0). The discussion widening is the same direction and size as scoring-vintage drift and is probably not a finding. Pre-2009 staff R2 fell for inflation pressure (0.76 to 0.56) and credit spreads (0.79 to 0.49).
- Contamination test of the staff input (20 random meetings, repeat vs strict input, blind agents): differences between inputs about as large as scorer noise (about 2 points per score); 127 of 128 staff scorers still flagged a Committee-recap paragraph; the bright-line check run on the finished tables: 0 hard failures, 11 soft flags (staff), 27 (discussion). See DATA_PROVENANCE 5.5.

### Not done
- No human validation. Staff v6 CREDIT_SPREADS remains mixed-vintage. The transcript topic-model agreement stays at r ≈ 0.48.

## [1.3.0] DRAFT — 2026-10-16, updated 2026-10-17 (local working copy; not committed, not pushed, not published)

Counts below are those of the files in this folder on 2026-10-17 (checked by recomputation). Items marked "project repository only" changed outside `dataset/` and are not in these files.

- Rubric: staff CREDIT_SPREADS bright line clarified to the level reading (`04_scoring/staff/rubric/FOMC_Staff_Review_Prompt_v4_1.md`) and 93 staff documents re-checked on that dimension; 79 CREDIT_SPREADS cells (74 minutes rows, 5 transcript rows) updated in `staff_scores_v4.csv` (log in `data/derived/credit_spreads_v4_1_applied_2026-10-17.csv`); most transcript rows still carry the old rule. See codebook note. (`FOMC_Staff_Review_Prompt_v4_1.md` is in the project repository only; a further `v4_2_addendum` changes no score definition; decisions are in `04_scoring/RUBRIC_DECISIONS_2026-10-17.md`.)

- Staff table status: `staff_scores_v4.csv` (486 rows: 270 minutes + 216 transcripts) is the original V4 run plus the changes listed here. The project's canonical staff table is `04_scoring/staff/v4_scores_patched_v6/all_scores_v4_patched_v6.csv` (495 rows: 270 minutes + 225 transcripts, re-scored on repaired transcripts). It was NOT promoted to this folder; the two differ in 84-139 of 486 shared rows for each of the seven main dimensions compared, so choose deliberately which one to release.

- New `data/supplementary/` (draft): 2026 statement, press-conference, Beige Book and speech (FSAI) scores from a later scoring vintage (5, 10, 4 and 61 rows); see its README and `CODEBOOK_supplementary.md`. Beige Books 2026-07-15, 09-02 and 10-14 were re-scored (BANKING_STRESS 57; the agents were told the rule, so the value is steered by it), and press-conference opening FINANCIAL_CONDITIONS for 2026-04-29 and 2026-06-17 is set to N/A under the "not discussed" rule. Not validated by a human.

- Docs: four codebooks (sentence classification, discussion v4.1, staff scores, meeting registry) and `analysis/DEEP_INSIGHTS_FINAL_v2.md` corrected against current data; the staff +8.3 transcript-minus-minutes convergence in `concordance_deep_dive.md` is retracted (project repository). README, DATA_PROVENANCE and VALIDATION_REPORT were synced to the 2026-10-17 state in a later pass; see their own notes.

- Staff V4: four minutes scored from gutted text (audit C4: 2002-03-19, 2001-11-06, 1997-11-12, 1994-03-22) re-scored on recovered text and replaced in `staff_scores_v4.csv`; field-level log in `04_scoring/staff/v4_scores_patched_v4/gutted_minutes_changes.csv`.

### Fixed
- **Footer-glued speaker labels (1993-96 transcripts).** A page-footer stamp (for example `9/24/96 -19`) was glued onto the next speaker's label, so line-anchored parsers merged that turn into the previous speaker's: 439 labels in 42 meetings. `data/sentence_classification/classified_sentences.csv`: 2,001 rows now carry the correct `speaker` / `speaker_role`; no topic or confidence label changed.
- **Page-break artifacts in sentence text.** Printed page footers (`--- PAGE n ---` plus the date/page line) were removed from 26,732 sentences; 3,479 rows that fell below the corpus's 5-word minimum were dropped. After this step the corpus had 500,049 rows (was 526,516); the later steps below change that count. Dropped rows: `06_cdfsg_pipeline/data/dropped_page_artifact_rows_2026-10-16.csv`.
- **Crisis-era minutes (2007-10 to 2009-06)** rebuilt (13 meetings, earlier garbled by a naive PDF reader); about 3,500 rows differ from 1.2.0.
- **`discussion_scores_v3.csv`: duplicate row removed (audit finding H2).** The 2008-01-21/22 emergency conference call was scored twice, once under each date key, with different scores. The 2008-01-22 row is removed (the registry key is the start date, 2008-01-21); the file now has 537 rows (265 minutes + 272 transcripts). This is the V3 file. Logged in `data/derived/removed_rows_log_2026-10-17.csv`; previous file `discussion_scores_v3.csv.bak_2026-10-17_pre_dedupe`.
- **Topic-modeling files replaced (audit finding H3).** `data/topic_modeling/cross_method_matrix.csv` and `cross_corpus_matrix.csv` now hold the cleaned 2026-10-07 re-run (minutes r = 0.865, N = 265; transcripts 0.48; rebuilt staff text 0.78); the February files (minutes 0.916 on a corpus with a duplicate meeting) moved to `_superseded_2026-02-09/`; the duplicate 2012-10-24 row was removed from `minutes_econ_ratio_timeseries.csv`. See `data/topic_modeling/README_2026-10-17.md`.
- **Double-ingested sentences removed (audit finding H1, 2026-10-17).** 22,815 rows dropped: 4,809 minutes sentences that had been ingested a second time in a later build batch (same meeting, section, speaker and text, sentence ids more than 5,000 apart; the two copies' labels disagreed in about half the cases, the earlier carried label is kept) and 18,006 transcript sentences that appeared in two components of the same meeting (decomposer overlap between `go_around_combined` and `policy_discussion`). Repeats inside one component are kept. After this step the corpus was 500,049 rows, with no document above 15% internal duplicates (was 73). Effect on `meeting_variables.csv`: FSS_transcript changes in 60 meetings (mean +0.003, max 0.084), FSS_minutes in 24 (mean +0.005, max 0.097); mean CDFSG against minutes goes from -0.1500 to -0.1554 (re-confirmed on 2026-10-17: 215 meetings, -0.1554). Dropped rows: `06_cdfsg_pipeline/data/dropped_double_ingested_rows_2026-10-17.csv`; script `06_cdfsg_pipeline/dedupe_double_ingestion.py`.
- `meeting_variables.csv` recomputed (FSS_transcript changes by at most 0.015 in any meeting; mean CDFSG against minutes -0.1512 -> -0.1500; see the double-ingestion entry for the current value).

### Changed (2026-10-17)
- **Meeting registry rebuilt through a key map.** `data/primary/meeting_registry.csv` now has 320 rows (1993-01-06 to 2026-09-16; 269 scheduled, 45 conference calls, 6 emergency; an earlier line of this draft said 321, which does not match the file). Columns: `meeting_date,start_date,end_date,meeting_type,chair,documents_found,documents_expected,rate_decision,target_rate,special_notes`. `meeting_date` is the document-name date: the last day for 162 of the 176 rows whose start_date differs from end_date (and for 1993-95), the first day for the other 14 (1996-99 and 2003-09-15 scheduled meetings, 2012-10-23, three 2008 conference calls, the 2020-03-02 emergency meeting); `start_date` and `end_date` give the span. Every score-table date key maps to a registry meeting through `02_registry/meeting_key_map.csv` in the project repository (check with `tools/check_keys.py`). `rate_decision` and `target_rate` are still empty (no source); `documents_expected` is unfilled for 2011-2018.
- **Two statements ingested into the sentence corpus** (2007-06-28, 9 sentences; 2008-12-16, 17 sentences), classified by one agent with prompt v2 (several rate-decision and balance-sheet sentences are borderline FINANCIAL/OTHER; the label for one 2007 sentence differs from a legacy copy of it). `classified_sentences.csv` now has 500,075 rows (transcript 428,487, minutes 52,831, speech 18,544, statement 213; 440 dates). `meeting_variables.csv` (440 rows) was recomputed: only those two meetings' statement columns changed; CDFSG (transcript minus statement) is now populated for 17 meetings (was 15), CDFSG_minutes for 215 (mean -0.1554).
- `data/sentence_classification/all_sentences_scored.csv` has a new `join_key` column (meeting_date, doc_type and the first 12 characters of the md5 of the lower-cased text, pipe-joined). Its `sentence_id` does not match the ids in `classified_sentences.csv`; join on `join_key`.
- `data/derived/master_mechanisms.csv`: new columns `DISSENT_GAP_V41`, `FSE_GAP_V41`, `UNCERTAINTY_GAP_V41` (transcript minus minutes, from `discussion_v4_1_minutes_vs_transcripts.csv`) and `V41_GAP_SOURCE`. The legacy hand-typed gap columns are kept; they correlate only 0.26 / 0.09 / 0.25 with the V4.1 gaps, so use the V4.1 columns. The frequency tables depend on the text mechanism columns, not the gaps, and were not regenerated.

### Added
- **Five 2026 meetings** (2026-03-18, 04-29, 06-17, 07-29, 09-16): rows in `meeting_registry.csv` (chair Warsh from 2026-06-17), `staff_scores_v4.csv` (5 minutes rows, fresh V4 scores; the table now has 486 rows) and `discussion_scores_v4_1.csv` (5 minutes rows; the table now has 542 rows = 272 transcripts + 270 minutes; fresh V4.1.1 scores, `METHOD` = `fresh_score`, `INPUT_VERSION` = `member_discussion_v2c`). Evidence: `scoring_evidence/discussion_v4_1/minutes_new_2026/`, `scoring_evidence/staff_v4/new_2026_minutes/`.

### Caution — scoring vintages
The five new discussion rows were scored on 2026-10-16/17. Re-scoring 44 transcripts with unchanged inputs on those days gave, on average, FINANCIAL_STABILITY_EMPHASIS 6.0 points lower (se 1.0), DISSENT_INTENSITY 2.4 lower and UNCERTAINTY_EXPRESSED 2.9 lower than the original scores; the economic and market dimensions moved by less than 1 point. Minutes and transcripts drift by similar amounts, so the minutes-minus-transcript gaps are unchanged (28 same-day pairs: FSE -14.1 -> -13.0, dissent -8.4 -> -9.7, uncertainty -3.8 -> -4.0). Levels of those three dimensions are therefore not comparable between the 2026 rows and the older rows. Details: `04_scoring/discussion/v4_1_scores/footer_fix_rescore/README.md` in the project repository. The same applies to the supplementary 2026 tables and the speech re-score below: compare within a vintage only.

### Project repository only (not in the files of this folder)
These changed in the working project on 2026-10-17 and have not been promoted to `dataset/`. Listed so the draft notes are complete; promote deliberately or leave out.
- Canonical staff table `04_scoring/staff/v4_scores_patched_v6/` (495 rows; v5 plus the five 2026 minutes rows, whose CREDIT_SPREADS rechecks were all unchanged). Patched v1-v5 are superseded.
- Discussion minutes patch `04_scoring/discussion/v4_1_scores/minutes_patch/all_scores_disc_m_v411_patched_v2d.csv` (265 rows): 2000-12-19 re-scored on the v2d input, HAWKISH_DOVISH_LEAN 38 -> 42, 19 other dimensions unchanged. `data/primary/discussion_scores_v4_1.csv` and `data/derived/discussion_v4_1_minutes_vs_transcripts.csv` now carry the re-scored 2000-12-19 minutes row (INPUT_VERSION `member_discussion_v2d`; derived diff 7 to 11).
- Speeches: 1,979 in the manifest; 61 new 2026 speeches scored; 62 re-scored after re-parsing (correlation with old FSAI 0.90, mean change -11.1; vintage drift and text dilution cannot be separated). `data/fsai_scores_all_2026-10-17.csv` carries a `SCORE_VINTAGE` column (original 1,856; rescored 62; new_2026_batch 61). About 99 pre-2007 speeches may have dropped paragraphs from the old parser and were not re-scored.
- Decomposition: canonical tree is `03_decomposition/output_rebuild/` (the old `output/` tree has defective two-column text); 42 transcript folders regenerated after the footer-glued-label fix; manifest 2,053 rows. Extraction gate: 4 transcripts (1998-11-17, 2004-06-30, 2005-06-30, 2011-11-02) have staff special sessions missing from component files (full text complete).
- Transmission: panel v2 (264 rows x 325 columns, built through the key map), discussion node now V4.1, pipeline re-run once (`09_transmission/run_all.py`); old results kept as `*_v1_2026-10-17`. Link means moved L1 0.184 -> 0.187, L2 0.377 -> 0.404, L3 0.474 -> 0.471, L4 0.219 -> 0.203; mediated share for financial conditions 93% -> 66%. Some `TRANSMISSION_REPORT.md` tables still describe v1.
- Tools and figure: `tools/bright_line_check.py` (mechanical score checks), `tools/check_keys.py`, and `06_cdfsg_pipeline/figures/fig1_cdfsg_timeseries.png`.

### Not done / limits
- Nothing is committed, pushed or published; the `dataset/` repository is 4 commits ahead of origin and this draft is uncommitted on top.
- Topic-model transcripts r = 0.48 is unexplained and fails the r > 0.7 success rule. A re-run of decomposed transcripts on the rebuilt corpus is in progress; no decomposed-transcript topic results are claimed.
- Downloads pending approval: statements 2007-08-17 and 2020-08-27, Warsh testimony 2026-07-14, Beige Book 2008-01-16. Transcripts exist only through 2020.
- No human validation of any score; all scorers are LLM agents.

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
- Scorer noise measured on 15 transcripts: mean absolute difference 1.8 points between a score and a blind re-score (financial-stability emphasis noisiest at 3.1); the sample is mostly 1994 to 2008. EQUITY_VALUATION in the 201 transcripts scored before the V4.1.1 clarifications may run about 2 points high relative to the clarified rule. See the codebook.
- Minutes rows are patches, not fresh scores. A fresh blind re-score of 60 random minutes documents differs from the published values by a mean absolute 3.3 points (4% of cells differ on scored versus `N/A`); the headline gaps are not weakened by it. Cell-level comparison in `data/derived/discussion_v4_1_minutes_fresh_sample.csv` and `..._by_dimension.csv`; agent outputs in `scoring_evidence/discussion_v4_1/minutes_fresh/`.
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
- `data/derived/master_mechanisms.csv`: 216 meetings with compression mechanism coding across dissent, financial stability, and uncertainty dimensions [Corrected 2026-10-17 after verification: the gap columns of this table are hand-typed (gen_csv.py), match the analyst batch gaps exactly in only ~20% of meetings and correlate only 0.26/0.09/0.25 with the V4.1 dissent/FSE/uncertainty gaps; use `data/derived/discussion_v4_1_minutes_vs_transcripts.csv` for gap analysis. See codebooks/CODEBOOK_mechanisms.md.]
- `data/derived/correction_log.csv`: 564 score corrections with audit trail (dimension, original, corrected, delta, rule applied)
- `data/derived/minutes_vs_transcripts.csv`: Staff score gap analysis for 171 matched meeting pairs
- `data/derived/concordance_summary.csv` and `concordance_by_era.csv`: Cross-document concordance by era

### Added — Sentence Classification
- `data/sentence_classification/classified_sentences.csv`: ~394,000 classified sentences, 394 meetings
- `data/sentence_classification/meeting_variables.csv`: 394-row meeting-level CDFSG index
- `data/sentence_classification/all_sentences_scored.csv`: 70,610 sentences from 17 crisis-period meetings with additional dictionary scores

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
