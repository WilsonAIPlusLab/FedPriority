# validation/ (historical reports, read with care)

These reports were written in March 2026 about the **original V4 staff run (482 documents)** and the earlier independent re-score. They were not regenerated for v2.0.0. Their numbers describe the files named in each report, not `data/primary/staff_scores_v6.csv` (495 rows) or the V4.1 discussion table.

- `independence_audit_report.md`, `COMPARISON_SYNTHESIS.md`, `EVIDENCE_SUMMARY.md`: the independent-scoring comparison and audit (model-vs-model).
- `quality_report.md`, `staff_comparison_report.md`: automated flags and minutes-vs-transcript statistics on the original V4 staff table.
- `pilot_kappa/`: pilot sentence-classification labels. The reported kappa of 0.751 could not be reproduced (a closest recomputation gave 0.686); see the README validation table.

No file here is a human validation. Reports about the V3 discussion scoring, the V3 concordance and the mechanism analysis were removed in v2.0.0 (see CHANGELOG).
