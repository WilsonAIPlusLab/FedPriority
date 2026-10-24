# FedPriority: Model-Scored Measures of Federal Reserve Priorities in FOMC Minutes and Transcripts, 1993–2026

**Version 2.0.0 (draft, 2026-10-23; local, not committed, not pushed, not published).**

## Focus: financial stability and the dual mandate

This dataset measures what the FOMC prioritises, read from its own documents. It is organised around three priorities:

1. **Price stability** (inflation pressure, components and expectations),
2. **Maximum employment** (output gap and labour tightness), together the statutory *dual mandate*, and
3. **Financial stability**, the possible implicit third objective (Cieslak and Vissing-Jorgensen 2021; Powell 2023): financial conditions, credit spreads, Treasury, banking and equity stress, explicit financial-stability emphasis, and the sentence-level share of financial-stability language (CDFSG).

`data/derived/priority_variable_map.csv` assigns every score column to one of these groups or to *context* (policy stance, committee process, spending, productivity, the dollar). The assignment is the author's judgement, not an estimated result; a few columns could reasonably sit elsewhere (OUTPUT_GAP is filed under employment).

Version 2.0.0 keeps only components that have a reported model-versus-model or internal-consistency check, no open defect, and are not superseded. Removed material is listed in CHANGELOG [2.0.0].

## Read this first: what the data are not

- **No human validation.** No human has labelled any part of this dataset. Every score is produced by Claude models; every reliability figure here is model-versus-model or an internal-consistency check, none measured against human coding.
- **Scoring vintages are not comparable in level.** Re-scoring 44 unchanged transcripts on 2026-10-16/17 moved FINANCIAL_STABILITY_EMPHASIS by −6.0 points on average, dissent −2.4 and uncertainty −2.9. Minutes-minus-transcript *gaps* inside one vintage are more stable than levels. Each row carries its vintage in `SCORE_VERSION` (staff) or `METHOD` / `INPUT_VERSION` (discussion).
- **The scores measure what a model reads in a document**, not what participants thought, and not whether differences between minutes and transcripts are caused by editorial choices.
- **Financial-stability convergence across methods is weak:** LLM scores versus the sentence index (A vs B) ρ = 0.317, below the 0.50 threshold set in advance.

## Dataset at a glance

| Item | Value |
|---|---|
| Staff assessment scores (`staff_scores_v6.csv`) | 495 documents (270 minutes + 225 transcripts), 15 dimensions |
| Discussion scores (`discussion_scores_v4_1.csv`) | 542 documents (270 minutes + 272 transcripts), 20 dimensions |
| Meeting registry | 320 events, 1993-01-06 to 2026-09-16 (269 scheduled, 45 conference calls, 6 emergency) |
| Classified sentences | 500,075 (transcript 428,487; minutes 52,831; speech 18,544; statement 213), 440 dates |
| Matched minutes–transcript pairs | 215 same-date staff pairs; 224 discussion pairs |
| Coverage | minutes 1993–2026; transcripts 1993–2020 (none released after 2020) |
| Chairs | Greenspan, Bernanke, Yellen, Powell, Warsh (from 2026-06-17) |

## Folder structure

```
data/primary/                  staff_scores_v6.csv, discussion_scores_v4_1.csv, meeting_registry.csv
data/derived/                  gap tables, patch/decision logs, priority_variable_map.csv
data/sentence_classification/  Method B: classified sentences, meeting-level CDFSG variables, crisis-period dictionary scores
data/topic_modeling/           Method C: topic-model comparison and economic-ratio series
scoring_evidence/              agent outputs behind the discussion scores and the staff minutes
rubrics/  codebooks/  code/  dictionaries/  validation/
```

## Primary files

| File | Rows | Notes |
|---|---|---|
| `data/primary/staff_scores_v6.csv` | 495 | Staff-assessment (Tealbook-type) content as scored from minutes and from transcripts. Transcripts were re-scored on repaired text. **Mixed vintage:** see `SCORE_VERSION`; compare only within a vintage. Staff transcript rows have no shipped evidence files. |
| `data/primary/discussion_scores_v4_1.csv` | 542 | Participant discussion, 20 dimensions. Transcripts scored fresh (V4.1; 71 re-scored as V4.1.1). Minutes: the 128 minutes of 1993–2008 are fresh blind scores on a rebuilt discussion-only input (`METHOD` = `fresh_blind_split_2026-10`, one agent per document, 2026-10-24); the other minutes are *patched* from an earlier scoring (137 rows) or fresh (5 rows from 2026); see `METHOD`. 36 minutes cells (patched rows) were set to N/A after a blind second pass. |
| `data/primary/meeting_registry.csv` | 320 | `meeting_date` is the date in the document name (last day for most two-day meetings); `start_date` / `end_date` give the span. `rate_decision` and `target_rate` are empty for 318 of 320 rows (no source). |

CREDIT_SPREADS in the staff table follows a level reading (a wide-but-stable spread scores by level, not direction); 79 cells were updated under it, most transcript rows still carry the older rule, so the column is mixed-vintage. Do not difference staff and discussion CREDIT_SPREADS.

## Derived files

| File | Description |
|---|---|
| `data/derived/staff_v6_minutes_vs_transcripts.csv` | Long-format minutes, transcript and difference (minutes minus transcript) per meeting and dimension, 215 same-date pairs, 2,166 numeric pairs |
| `data/derived/discussion_v4_1_minutes_vs_transcripts.csv` | Same for the discussion table, 224 pairs × 20 dimensions |
| `data/derived/discussion_v4_1_*` (patch log, second-pass check, rescore diff, N/A log, fresh-sample files, credit update log) | Audit trail for the V4.1 minutes patch and re-scores |
| `data/derived/credit_spreads_v4_1_applied_2026-10-17.csv` | The 79 staff CREDIT_SPREADS cells updated |
| `data/derived/priority_variable_map.csv` | Variable → priority group |
| `data/sentence_classification/classified_sentences.csv` | Sentence-level topic label (FINANCIAL, INFLATION, EMPLOYMENT_OUTPUT, REGULATION_SUPERVISION, OTHER), 1–5 stability intensity for financial sentences, speaker. New column `label_source`: **7,979 rows (transcript 5,118, speech 2,448, minutes 413) are `keyword_script`** (their labels match a keyword script, not an LLM judgement); the other 492,096 are `llm_presumed`, meaning no keyword-script evidence was found, which is not a verification. |
| `data/sentence_classification/meeting_variables.csv` | 440 meetings: financial-stability share per document and CDFSG. Computed with the keyword-labelled rows included; the effect on CDFSG was not re-estimated. |
| `data/sentence_classification/all_sentences_scored.csv` | 70,610 crisis-period sentences with dictionary counts; join to the classified file on `join_key` |
| `data/topic_modeling/` | FASTopic vs BERTopic agreement: minutes r = 0.865 (N = 265), staff text 0.78, transcripts 0.48 (the transcript result is not robust to model choice; reason unexplained). Superseded February figures in `_superseded_2026-02-09/` |

## Headline gaps (minutes minus transcripts; model-scored; not human-validated)

- Financial-stability emphasis **−15.1**, dissent **−10.8**, uncertainty **−7.2** (V4.1, 224 pairs; recomputed 2026-10-24 after the 1993–2008 minutes were re-scored fresh; before that: −13.3, −8.3, −5.0). Most of the change is in the 128 pre-2009 pairs (financial-stability emphasis −13.5 to −16.6, dissent −8.3 to −12.6, uncertainty −1.9 to −5.7); the 96 pairs from 2009 on are unchanged. **Read the widening as a scoring-vintage effect, not as new evidence:** the re-scored minutes were scored on 2026-10-24, the transcripts earlier, and re-scoring unchanged text in a later session moved these three dimensions by −6.0, −2.4 and −2.9 (Validation summary, drift control), the same direction and size as the change. An earlier V3 scoring (no longer shipped) gave the same signs and similar sizes, but its figures were recorded inconsistently across documents and are not quoted here; V3 and V4.1 come from one model family and are not independent confirmations.
- Staff financial conditions, from the v6 table: transcript minus minutes **−1.55** (213 pairs; recomputed 2026-10-24 after the pre-2009 staff minutes were re-scored on staff-only text; it was +0.92 before, so the sign is not stable, and scorer-to-scorer noise is about 2 points per score). An earlier +8.3 was retracted in the project (largely a scoring-contamination artifact). Staff price-stability and employment gaps are small (INFLATION_PRESSURE −2.2, LABOR_TIGHTNESS −0.7, OUTPUT_GAP −0.3, minutes minus transcripts).

- **The financial-stability emphasis gap is largely a length effect.** In a within-meeting test on 40 meetings (160 model scorings, 2026-10-23; project folder `14_length_test/`, not shipped), a neutral, topic-proportional summary of the transcript cut to the length of the published minutes lowered the score by 8.2 points (95% CI −10.0 to −6.4), against 11.2 points for the published minutes in the same batch (CI −14.3 to −8.2): summarising at minutes length reproduces about 72% of the gap (CI 0.54 to 0.99). About 3 points remain (−3.1, CI −6.2 to −0.1; −2.8 without the four pilot meetings, CI −6.1 to +0.3), mostly in the 1990s–2000s, and that residual is not robust. Read the −13 to −15 financial-stability emphasis gap as mainly the consequence of document length and summarising, not as evidence that the minutes selectively understate financial stability; some selective weighting is not ruled out. Limits: the comparison summaries were written by a model of the same family as the scorer and were not checked by a human for topic proportion (financial-term density was checked on four summaries only); scorers can recognise excerpts and, less so, summaries; one sample, one rubric, one scorer family; the dimension has no human validation. The other economic dimensions did not move (within about ±1.5) under the same procedure. The dissent gap behaves differently: published minutes sit 5.5 points below the neutral summary (CI −7.3 to −3.8).

Dissent and uncertainty are kept as context for the priorities, not as priority measures.

## Validation summary (model-vs-model only)

| Procedure | Result |
|---|---|
| Independence audit (original staff V4 run) | 0 contamination phrases; lag-1 autocorrelation 0.818 → 0.690 (reduced, not removed) |
| Staff second-model review (64 files, original V4) | ~73% VALID, ~22% QUESTIONABLE, ~5% INCORRECT at dimension level |
| V4.1 minutes (patched) | Fresh blind re-score of 60 minutes: mean absolute difference 3.3; blind second pass 3.8; 4% of cells differ between scored and N/A |
| Drift control | 44 unchanged transcripts re-scored: FSE −6.0, dissent −2.4, uncertainty −2.9 |
| Cross-method (financial) | A vs B ρ = 0.317 (fails threshold); A vs C 0.540; B vs C 0.587 |
| Pilot sentence kappa | Reported 0.751 could not be reproduced (closest recomputation 0.686) |
| Human validation | **None.** A protocol exists in the project repository; nothing has been filled. |

Details and caveats: `VALIDATION_REPORT.md`, `validation/README.md`.

## Known limits

- **Staff minutes before 2009 (re-scored 2026-10-24, with a residual).** The earlier staff scores for the 128 minutes of 1993–2008 were given the whole minutes body, including the participants' discussion. They were replaced by blind scores on a rebuilt staff-only input (`STAFF_TEXT_SCOPE` = `minutes_staff_sections_split_2026-10`; one agent per document; the split is described in CHANGELOG [2.0.0]). The separation is by text anchors and was checked rule by rule and by reading each boundary, not by a sentence-by-sentence human audit, and it leaves a residual: the opening paragraph of the staff's financial review begins with a sentence recalling the previous meeting's directive, and 127 of the 128 staff scorers flagged it (`ANOMALY_NOTE`). Most said they ignored it; about 22 said they used market facts from the same paragraph. A test on 20 random meetings (the original input scored again, and a stricter input without the Committee-attributing sentences, blind agents) found differences between the two inputs about as large as between two scorings of the same input (about 2 points per score), so no contamination effect was detectable in that sample; it is small and cannot rule out an effect of a few points on single dimensions. The pre-2009 staff scores changed in level against the earlier ones (financial conditions +4.8 on average; correlation with the earlier scores 0.89 to 0.95 on the headline dimensions). The scorers did not run the mechanical bright-line check; run afterwards on the new tables it found 0 hard failures and 11 soft flags (a coarse keyword screen). From 2009 onward (142 minutes) the staff sections were always separate. Staff minutes-versus-transcript R² is now, pre-2009 / 2009+: labour tightness 0.83 / 0.96, output gap 0.81 / 0.94, inflation pressure 0.56 / 0.83, financial conditions 0.69 / 0.56; see CHANGELOG [2.0.0].
- Staff transcript rows (`transcript_staff_turns_not_fully_audited`) were built from staff presentation turns; member questions inside the staff briefing and staff answers inside the member text were seen in the parsed text but not audited row by row.

- 4 transcripts (1998-11-17, 2004-06-30, 2005-06-30, 2011-11-02) fall below the extraction-quality gate in their component split.
- The staff v6 table is not the table the staff evidence files were written for (evidence covers the 266 original minutes scores plus 5 new 2026 minutes).
- Sentence corpus: see `label_source` above.
- `INFLATION_HOUSING` and `INFLATION_SERVICES` are scored in few documents (13 and 12 same-date pairs).

## Source documents and licence

Raw FOMC documents are not included; see federalreserve.gov (historical materials and calendars). Code: Python 3.10+, `code/requirements.txt`, Claude models for scoring; LLM scoring is stochastic, so the evidence files and rubrics are the reproducibility mitigation. Licence CC-BY-4.0 (`LICENSE.md`).

## Citation

```
Chen, Robin. (2026). FedPriority: Model-Scored Measures of Federal Reserve Priorities, 1993-2026 [Data set]. Version 2.0.0 (draft).
```

## Funding

University of Northern Iowa Research Sponsorship Program (RSP) Capacity Building Grant, "Revealed Federal Reserve Priorities: Developing AI Methods to Measure Policy Responses to Financial Conditions."

## Column naming

`staff_scores_v6.csv` and `discussion_scores_v4_1.csv` use UPPERCASE (`MEETING_DATE`, `SOURCE_TYPE`); `meeting_registry.csv` uses lowercase; gap tables use lowercase `meeting_date`. Join case-insensitively. Ten score-table dates (for example 1996-01-31, 2003-09-16, 2012-10-24) are not registry `meeting_date` values; `data/derived/meeting_key_map.csv` maps the keys of the staff v6 and discussion V4.1 tables to their registry meeting (0 unmatched). In `meeting_variables.csv`, 115 of the 440 dates match no meeting (dates of speeches without a meeting); they are marked `unmatched` there.
