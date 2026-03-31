# Independent Rescoring Evidence Package

**Date produced**: 2026-03-21
**Purpose**: Self-contained evidence folder for the independent rescoring of all FOMC scoring — both staff assessments (V4) and participant discussion (V3 independent).

---

## What This Contains

### 1. Staff V4 Rescoring (`staff_v4/`)

- **`all_scores_v4.csv`** — Master CSV with 482 scored staff assessment documents (minutes + transcripts, 1993–2026). 15 dimensions per document.
- **`manifest.csv`** — Full scoring manifest with source paths and status.
- **`rubric/`** — The V4 staff scoring prompt and anchor meetings used for calibration.
- **`scored_files/`** — 351 scored .md files from batched agent scoring (agent1 minutes + agent2 transcripts).
- **`scored_files_independent/`** — 266 independently scored staff minutes (one fresh agent per document, no batching).
- **`analysis/`** — Quality report, gap analysis (old V3 vs new V4), comparison report, independence audit.

### 2. Discussion V3 Independent Rescoring (`discussion_v3_independent/`)

- **`all_scores_v3_independent.csv`** — Master CSV with 539 scored discussion documents (266 minutes + 273 transcripts, 1993–2026). 10 core + 10 optional dimensions per document.
- **`manifest.csv`** — Full scoring manifest.
- **`rubric/`** — The V3 independent scoring prompt (no calibration chain — rubric anchor tables only).
- **`scored_minutes/`** — 266 independently scored minutes .md files.
- **`scored_transcripts/`** — 273 independently scored transcript .md files.

### 3. Comparison (`comparison/`)

- **`all_scores_v3_batched.csv`** — The OLD batched V3 discussion scores (for comparison).
- **`concordance_*.csv`** — Minutes-transcript concordance analysis from the old batched scoring.
- **`v3_validation_summary.md`** — Validation summary from the old batched scoring.
- **`run_v3_scoring.py`** — The scoring/extraction/comparison script (includes `compare` command).
- **`run_v4_scoring.py`** — The staff scoring/extraction script.

---

## Scoring Methodology

### Staff V4
- Each meeting's staff assessment (Greenbook/Tealbook) scored by a single agent using the V4 rubric.
- 15 dimensions: INFLATION_PRESSURE, OUTPUT_GAP, LABOR_TIGHTNESS, CONSUMPTION_INVESTMENT, PRODUCTIVITY, FINANCIAL_CONDITIONS, TREASURY_STRESS, CREDIT_SPREADS, EQUITY_VALUATION, BANKING_STRESS, DOLLAR_STRENGTH, INFLATION_GOODS, INFLATION_SERVICES, INFLATION_HOUSING, INFLATION_EXPECTATIONS.

### Discussion V3 Independent
- **One fresh agent per document** — no batching, no shared context, no calibration chain.
- Agent receives ONLY the rubric (with anchor tables) and the source document.
- Minutes and transcripts scored completely independently — no forced concordance.
- 10 core dimensions: INFLATION_PRESSURE, OUTPUT_GAP, LABOR_TIGHTNESS, CONSUMPTION_INVESTMENT, FINANCIAL_TIGHTNESS, HAWKISH_DOVISH_LEAN, DISSENT_INTENSITY, FINANCIAL_STABILITY_EMPHASIS, FORWARD_GUIDANCE_TONE, UNCERTAINTY_EXPRESSED.
- 10 optional dimensions scored when prominently discussed by 2+ participants.

---

## Key Findings

### Old Batched vs New Independent Discussion Scores

| Dimension | r (old vs new) | MAD | Interpretation |
|---|---|---|---|
| INFLATION_PRESSURE | 0.937 | 3.7 | Highly stable |
| OUTPUT_GAP | 0.962 | 2.6 | Highly stable |
| LABOR_TIGHTNESS | 0.969 | 3.1 | Highly stable |
| CONSUMPTION_INVESTMENT | 0.967 | 2.3 | Highly stable |
| FINANCIAL_TIGHTNESS | 0.927 | 5.2 | Stable |
| HAWKISH_DOVISH_LEAN | 0.964 | 3.6 | Highly stable |
| DISSENT_INTENSITY | 0.802 | 5.7 | Moderate change |
| FINANCIAL_STABILITY_EMPHASIS | 0.870 | 7.2 | Moderate change |
| FORWARD_GUIDANCE_TONE | 0.966 | 4.2 | Highly stable |
| UNCERTAINTY_EXPRESSED | 0.854 | 5.4 | Moderate change |

### Minutes-Transcript Gaps (New Independent, Paired t-tests)

| Dimension | Mean Gap | t-stat | Significant? |
|---|---|---|---|
| DISSENT_INTENSITY | -9.7 | -18.8 | Yes — minutes underreport dissent |
| FINANCIAL_STABILITY_EMPHASIS | -11.3 | -15.5 | Yes — minutes compress FSE |
| UNCERTAINTY_EXPRESSED | -5.2 | -11.2 | Yes — minutes understate uncertainty |
| LABOR_TIGHTNESS | -2.6 | -10.5 | Modest — minutes slightly lower |
| Economic dimensions (INFL, OUTG, CONS) | ~0 | |t| < 3 | No systematic gap |

### Minutes-Transcript Concordance (New Independent)

| Tier | Dimensions | r |
|---|---|---|
| Very high | OUTPUT_GAP, LABOR, CONSUMPTION, HAWKISH, FORWARD_GUIDANCE, INFLATION | 0.95–0.97 |
| High | FINANCIAL_TIGHTNESS | 0.91 |
| Moderate | UNCERTAINTY (0.85), FSE (0.83), DISSENT (0.76) | 0.76–0.85 |

### Discussion vs Staff (V4) Concordance — Improved by Independent Rescoring

| Dimension | Old batched r | New independent r | Improvement |
|---|---|---|---|
| INFLATION_PRESSURE | 0.937 | 0.947 | +0.010 |
| OUTPUT_GAP | 0.939 | 0.958 | +0.019 |
| LABOR_TIGHTNESS | 0.955 | 0.963 | +0.008 |
| CONSUMPTION_INVESTMENT | 0.908 | 0.926 | +0.018 |

### Autocorrelation (lag-1, minutes track)

Independent scoring shows slightly lower autocorrelation than old batched scoring across most dimensions, confirming the old method had modest cross-meeting contamination. Changes are small (median delta = -0.007), indicating the economic signal was largely genuine.

### Conclusion

1. **Economic dimensions are robust** — near-identical between old/new methods, with improved staff concordance.
2. **Minutes-transcript gaps in DISSENT, FSE, and UNCERTAINTY are real editorial effects** — they persist and strengthen under independent scoring.
3. **The FSE gap is structural and era-persistent** — minutes compress financial stability discussion by ~11 points on average.
4. **Cross-meeting contamination in old batched scoring was modest** — it affected subjective dimensions (DISSENT, FSE, UNCERTAINTY) more than economic dimensions.

---

## File Counts

| Category | Count |
|---|---|
| Staff V4 scored files (batched) | 351 |
| Staff V4 scored files (independent minutes) | 266 |
| Discussion V3 independent scored minutes | 266 |
| Discussion V3 independent scored transcripts | 273 |
| Total scored .md files | 1,156 |
| Master CSVs | 3 (staff V4, discussion independent, discussion batched) |
| Anomaly-flagged meetings | 167/539 (31%) |
