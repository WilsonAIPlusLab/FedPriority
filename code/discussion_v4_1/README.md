# Discussion V4.1 pipeline scripts (provenance)

These scripts document how the V4.1 tables were built. They are **not** a stand-alone runnable pipeline: the scoring itself was done by fresh LLM agents dispatched one document at a time from a Claude Code session, and the scripts assume the working folders (`03_decomposition/output_rebuild/member_discussion_v2*`, `04_scoring/discussion/v4_1_scores/`) from the original project. They read agent output files, validate them against the rubric's Part 3 format, keep the dispatch ledgers, and merge the results.

- `build_member_discussion_v2.py`: builds the member-discussion inputs (transcripts: all member turns, staff removed, roll call appended; minutes: participants' views + vote record).
- `run_v41.py`: manifest, validator (`check`), ledger and CSV parse for the first V4.1 run.
- `patch_status.py`, `merge_minutes_patch.py`: the minutes patch runner and merge.
- `rerun_v411.py`: queue runner for the follow-up (transcript re-scores and blind second pass).
- `followup_merge.py`, `apply_na_decision.py`: merge, comparison and the N/A decision applied to 36 minutes cells.
- `minutes_fresh_runner.py`: draws the 60-meeting fresh minutes sample (seed 20261011), keeps the dispatch ledger, validates outputs and writes the comparison with the published minutes values.
- `apply_credit_update.py`: applies the blind CREDIT_SPREADS re-check to the 16 first-run N/A transcript cells that now carry a Low-confidence score (reads the check outputs from the original project folders, which are not shipped except as `scoring_evidence/discussion_v4_1/credit_update/`).
