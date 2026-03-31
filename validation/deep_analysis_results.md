# Deep Analysis: Independent vs Batched Discussion Scoring

**Date**: 2026-03-21
**Method**: All 538 FOMC discussion documents re-scored independently (one fresh agent per document, rubric-only calibration, no cross-meeting context).

---

## 1. Distribution Statistics — New Independent Scores

| Dimension | Mean | Median | SD | Min | Max | N |
|---|---|---|---|---|---|---|
| INFLATION_PRESSURE | 43.4 | 42 | 14.4 | 15 | 85 | 523 |
| OUTPUT_GAP | 44.4 | 47 | 11.8 | 10 | 65 | 523 |
| LABOR_TIGHTNESS | 47.1 | 49 | 15.6 | 8 | 75 | 522 |
| CONSUMPTION_INVESTMENT | 46.6 | 48 | 12.0 | 10 | 70 | 522 |
| FINANCIAL_TIGHTNESS | 42.9 | 38 | 17.6 | 15 | 92 | 529 |
| HAWKISH_DOVISH_LEAN | 44.8 | 47 | 19.3 | 3 | 83 | 527 |
| DISSENT_INTENSITY | 31.6 | 32 | 11.8 | 5 | 70 | 531 |
| FINANCIAL_STABILITY_EMPHASIS | 42.2 | 38 | 20.7 | 3 | 97 | 534 |
| FORWARD_GUIDANCE_TONE | 43.3 | 48 | 22.8 | 5 | 87 | 526 |
| UNCERTAINTY_EXPRESSED | 52.7 | 52 | 12.6 | 25 | 93 | 528 |

---

## 2. Minutes-Transcript Gap (Paired, New Independent)

| Dimension | N | Mean Gap | SE | t-stat | Median | IQR |
|---|---|---|---|---|---|---|
| INFLATION_PRESSURE | 214 | -0.84 | 0.28 | -2.96 | 0 | [-3,+2] |
| OUTPUT_GAP | 214 | -0.45 | 0.19 | -2.36 | 0 | [-2,+1] |
| LABOR_TIGHTNESS | 214 | -2.56 | 0.24 | -10.48 | -2 | [-5,0] |
| CONSUMPTION_INVESTMENT | 214 | -0.25 | 0.20 | -1.24 | 0 | [-2,+1] |
| FINANCIAL_TIGHTNESS | 215 | +0.05 | 0.47 | +0.11 | 0 | [-3,+4] |
| HAWKISH_DOVISH_LEAN | 215 | -0.30 | 0.31 | -0.96 | 0 | [-3,+2] |
| DISSENT_INTENSITY | 215 | -9.74 | 0.52 | -18.84 | -8 | [-15,-5] |
| FINANCIAL_STABILITY_EMPHASIS | 215 | -11.26 | 0.73 | -15.45 | -12 | [-17,-5] |
| FORWARD_GUIDANCE_TONE | 214 | -0.87 | 0.37 | -2.36 | 0 | [-4,+2] |
| UNCERTAINTY_EXPRESSED | 214 | -5.21 | 0.46 | -11.24 | -6 | [-10,0] |

---

## 3. Minutes-Transcript Gap by Era

| Dimension | 1993-2003 | 2004-2007 | 2008-2012 | 2013-2019 | Overall |
|---|---|---|---|---|---|
| INFLATION_PRESSURE | -1.1 | -0.8 | -2.0 | +0.4 | -0.8 |
| OUTPUT_GAP | -0.8 | +1.2 | -0.1 | -1.1 | -0.4 |
| LABOR_TIGHTNESS | -1.3 | -3.4 | -1.9 | -4.6 | -2.6 |
| CONSUMPTION_INVESTMENT | +0.2 | +1.3 | -1.6 | -0.7 | -0.3 |
| FINANCIAL_TIGHTNESS | -1.4 | -1.0 | +3.7 | +0.1 | +0.1 |
| HAWKISH_DOVISH_LEAN | +0.1 | -0.8 | +0.6 | -1.5 | -0.3 |
| DISSENT_INTENSITY | -9.5 | -9.2 | -13.5 | -8.2 | -9.7 |
| FINANCIAL_STABILITY_EMPHASIS | -12.6 | -8.2 | -7.7 | -12.7 | -11.3 |
| FORWARD_GUIDANCE_TONE | -1.1 | +0.6 | -1.4 | -1.4 | -0.9 |
| UNCERTAINTY_EXPRESSED | -2.7 | -2.1 | -6.8 | -9.4 | -5.2 |

---

## 4. Largest FINANCIAL_STABILITY_EMPHASIS Gaps

**Most negative (minutes << transcript):**

| Date | Minutes | Transcript | Gap |
|---|---|---|---|
| 2020-07-29 | 10 | 78 | -68 |
| 2016-04-27 | 32 | 78 | -46 |
| 2019-05-01 | 32 | 68 | -36 |
| 2002-06-26 | 32 | 65 | -33 |
| 1995-02-01 | 28 | 60 | -32 |
| 2018-11-08 | 37 | 68 | -31 |
| 2013-09-18 | 35 | 65 | -30 |

---

## 5. Cross-Dimension Correlation Matrix (New Independent)

N = 522 meetings with all 10 core dimensions scored.

|  | INFL | OUTG | LABR | CONS | FINT | HAWK | DISS | FISE | FWGD | UNCE |
|---|---|---|---|---|---|---|---|---|---|---|
| INFL | 1.00 | 0.59 | 0.62 | 0.46 | -0.01 | 0.63 | -0.03 | -0.10 | 0.61 | -0.14 |
| OUTG | 0.59 | 1.00 | 0.93 | 0.88 | -0.37 | 0.82 | -0.13 | -0.33 | 0.80 | -0.52 |
| LABR | 0.62 | 0.93 | 1.00 | 0.75 | -0.20 | 0.74 | -0.13 | -0.17 | 0.76 | -0.35 |
| CONS | 0.46 | 0.88 | 0.75 | 1.00 | -0.53 | 0.77 | -0.15 | -0.41 | 0.71 | -0.60 |
| FINT | -0.01 | -0.37 | -0.20 | -0.53 | 1.00 | -0.39 | 0.10 | 0.61 | -0.30 | 0.64 |
| HAWK | 0.63 | 0.82 | 0.74 | 0.77 | -0.39 | 1.00 | -0.20 | -0.38 | 0.95 | -0.54 |
| DISS | -0.03 | -0.13 | -0.13 | -0.15 | 0.10 | -0.20 | 1.00 | 0.33 | -0.21 | 0.15 |
| FISE | -0.10 | -0.33 | -0.17 | -0.41 | 0.61 | -0.38 | 0.33 | 1.00 | -0.32 | 0.60 |
| FWGD | 0.61 | 0.80 | 0.76 | 0.71 | -0.30 | 0.95 | -0.21 | -0.32 | 1.00 | -0.43 |
| UNCE | -0.14 | -0.52 | -0.35 | -0.60 | 0.64 | -0.54 | 0.15 | 0.60 | -0.43 | 1.00 |

**Key structure:**
- Real-economy cluster: OUTG-LABR (0.93), OUTG-CONS (0.88)
- Policy cluster: HAWK-FWGD (0.95)
- Stress cluster: FINT-UNCE (0.64), FINT-FISE (0.61)
- DISSENT is weakly correlated with everything — an independent process dimension

---

## 6. Old-vs-New Bias by Era (new minus old)

| Dimension | 1993-2003 | 2004-2007 | 2008-2012 | 2013-2019 | 2020+ |
|---|---|---|---|---|---|
| INFLATION_PRESSURE | -1.9 | -0.5 | -0.3 | -0.0 | -0.1 |
| OUTPUT_GAP | -0.8 | +0.1 | +0.0 | -0.8 | -1.2 |
| LABOR_TIGHTNESS | -1.1 | -1.6 | +1.0 | -2.3 | +0.3 |
| CONSUMPTION_INVESTMENT | +0.2 | -0.4 | -0.1 | -1.3 | -0.8 |
| FINANCIAL_TIGHTNESS | -2.1 | -2.7 | -0.6 | -1.1 | -1.7 |
| HAWKISH_DOVISH_LEAN | -0.5 | +0.6 | -0.5 | -0.6 | +0.2 |
| DISSENT_INTENSITY | -3.3 | -3.2 | +2.9 | +0.2 | -1.6 |
| FSE | -3.2 | -1.2 | -0.6 | +1.3 | -1.0 |
| FORWARD_GUIDANCE_TONE | +0.1 | +0.9 | -2.0 | -1.2 | -0.2 |
| UNCERTAINTY_EXPRESSED | -2.3 | -1.0 | -0.6 | -2.9 | +0.0 |

---

## 7. Discussion vs Staff (V4) Concordance

### New Independent Discussion (minutes) vs Staff

| Discussion dim | Staff dim | r | MAD | Bias | N |
|---|---|---|---|---|---|
| INFLATION_PRESSURE | INFLATION_PRESSURE | 0.947 | 3.5 | +0.6 | 224 |
| OUTPUT_GAP | OUTPUT_GAP | 0.958 | 2.4 | +0.6 | 225 |
| LABOR_TIGHTNESS | LABOR_TIGHTNESS | 0.963 | 3.3 | +1.5 | 225 |
| CONSUMPTION_INVESTMENT | CONSUMPTION_INVESTMENT | 0.926 | 3.3 | +1.1 | 224 |
| FINANCIAL_TIGHTNESS | FINANCIAL_CONDITIONS | 0.839 | 7.3 | -2.6 | 226 |

### New Independent Discussion (transcript) vs Staff

| Discussion dim | Staff dim | r | MAD | Bias | N |
|---|---|---|---|---|---|
| INFLATION_PRESSURE | INFLATION_PRESSURE | 0.887 | 4.6 | +1.7 | 180 |
| OUTPUT_GAP | OUTPUT_GAP | 0.963 | 2.4 | +1.1 | 181 |
| LABOR_TIGHTNESS | LABOR_TIGHTNESS | 0.961 | 4.6 | +4.1 | 181 |
| CONSUMPTION_INVESTMENT | CONSUMPTION_INVESTMENT | 0.927 | 3.4 | +0.8 | 180 |
| FINANCIAL_TIGHTNESS | FINANCIAL_CONDITIONS | 0.859 | 7.2 | -3.8 | 183 |

### Improvement Over Old Batched (minutes vs staff)

| Dimension | Old r | New r | Change |
|---|---|---|---|
| INFLATION_PRESSURE | 0.937 | 0.947 | +0.010 |
| OUTPUT_GAP | 0.939 | 0.958 | +0.019 |
| LABOR_TIGHTNESS | 0.955 | 0.963 | +0.008 |
| CONSUMPTION_INVESTMENT | 0.908 | 0.926 | +0.018 |

---

## 8. Autocorrelation Comparison (lag-1, minutes track)

| Dimension | Old AC1 | New AC1 | Delta |
|---|---|---|---|
| INFLATION_PRESSURE | 0.951 | 0.930 | -0.021 |
| OUTPUT_GAP | 0.943 | 0.939 | -0.004 |
| LABOR_TIGHTNESS | 0.967 | 0.963 | -0.004 |
| CONSUMPTION_INVESTMENT | 0.903 | 0.886 | -0.017 |
| FINANCIAL_TIGHTNESS | 0.864 | 0.796 | -0.068 |
| HAWKISH_DOVISH_LEAN | 0.904 | 0.913 | +0.009 |
| DISSENT_INTENSITY | 0.445 | 0.475 | +0.030 |
| FINANCIAL_STABILITY_EMPHASIS | 0.736 | 0.734 | -0.002 |
| FORWARD_GUIDANCE_TONE | 0.933 | 0.926 | -0.007 |
| UNCERTAINTY_EXPRESSED | 0.778 | 0.737 | -0.042 |

---

## 9. FSE Distribution: Minutes vs Transcript

**Minutes** (N=266): Mean=35.3, SD=16.7, Median=35
- Concentrated in 11-50 range (83% of scores)
- Very few scores above 70 (5%)

**Transcripts** (N=268): Mean=49.0, SD=22.1, Median=45
- Much wider distribution
- 21% of scores above 70 (vs 5% for minutes)
- 6% of scores above 90 (dedicated financial stability sessions)

The distribution shift confirms that **minutes systematically compress the upper tail** of financial stability emphasis — meetings where transcripts show intensive FSE discussion (60-97 range) get reported as moderate (30-50) in minutes.

---

## 10. Confidence Level Distribution

| Level | Count | Percentage |
|---|---|---|
| High | 4,021 | 74.6% |
| Moderate | 1,048 | 19.4% |
| Low | 203 | 3.8% |
| Other | 117 | 2.2% |

167 of 539 documents (31%) flagged as anomalous — these are emergency calls, special sessions, truncated documents, and non-standard meetings.
