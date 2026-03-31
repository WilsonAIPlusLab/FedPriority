# V3 Discussion Score Validation Summary

**Date**: 2026-03-18
**Method**: Opus 4.6 agents independently read scored files (Part 1 Thinking + Part 2 Evidence + Part 3 Scores) and source documents, then verified consistency across all three parts.
**Sample**: 64 files (12% of 538), stratified across 4 eras, mix of minutes and transcripts.

---

## Overall Results

| Metric | Era 1 (1993-2001) | Era 2 (2002-2010) | Era 3 (2011-2019) | Era 4 (2020-2026) | **Total** |
|--------|-------------------|-------------------|-------------------|-------------------|-----------|
| Files reviewed | 16 | 16 | 16 | 16 | **64** |
| Dimensions checked | 160 | 160 | 160 | 148 | **628** |
| PASS | 143 (89%) | 138 (86%) | 154 (96%) | 133 (90%) | **568 (90%)** |
| MAGNITUDE_OFF | 14 (9%) | 16 (10%) | 3 (2%) | 13 (9%) | **46 (7%)** |
| DIRECTION_WRONG | **0** | **0** | **0** | **0** | **0** |
| EVIDENCE_MISSING | 3 (2%) | 6 (4%) | 3 (2%) | 2 (1%) | **14 (2%)** |

### Reproducibility Spot-Check (16 files re-scored independently)

| Era | Files re-scored | Mean Absolute Deviation | Max single-dim delta |
|-----|-----------------|------------------------|---------------------|
| 1993-2001 | 4 | **1.8** | 6 |
| 2002-2010 | 4 | **2.0** | 5 |
| 2011-2019 | 4 | **2.1** | 5 |
| 2020-2026 | 4 | **1.8** | 3 |
| **Overall** | **16** | **1.9** | 6 |

---

## Key Findings

### Zero Direction Errors

Across all 628 dimension-checks, **not a single score was on the wrong side of 50**. Every "above potential" scored >50, every "below target inflation" scored <50, every "dovish" scored <50 on HAWKISH_DOVISH_LEAN. The v3 prompt's self-check rules (Direction Rule, Polarity Check) eliminated the polarity confusion that plagued v2.

### Zero Polarity Inversions

Higher always means more of the named construct. No cases where tight financial conditions were scored low, or where high inflation was scored low. The uniform polarity design works.

### Magnitude Deviations Are Small

All 46 MAGNITUDE_OFF flags are within 3-7 points of the validated correct value — well within the stated uncertainty bands (typically ±5-8). The most common pattern is DISSENT_INTENSITY being scored slightly high (the scorer weights internal debate and near-dissents more than formal vote counts alone).

### Evidence-Missing Flags Are Appropriate

All 14 EVIDENCE_MISSING cases come from anomaly-flagged meetings (inter-meeting calls, emergency sessions) where the source document has no economic go-around. The scorer correctly assigned Low confidence and set ANOMALY_FLAG=Yes. These are not errors.

### Reproducibility Is Excellent

Overall MAD of **1.9** across 16 re-scored files (160 dimensions) far exceeds the target of ≤8 and dramatically improves on v2's MAD of 13.72. The maximum single-dimension delta was 6 points (DISSENT_INTENSITY, a judgment-call dimension). This confirms the v3 prompt produces highly reproducible scores.

### Known Systematic Patterns (Not Errors)

1. **Transcripts score FINANCIAL_STABILITY_EMPHASIS and DISSENT_INTENSITY higher than minutes** for the same meeting (+14 and +9 on average). This is expected: transcripts preserve individual speaker emphasis that minutes compress. This is a feature of the source type, not a scoring error.

2. **DISSENT_INTENSITY has a slight upward bias** across all eras. The scorer weights internal debate, reluctant support, and near-dissents somewhat more than formal vote counts. Defensible but worth noting for downstream analysis.

3. **2016-12-14 minutes UNCERTAINTY_EXPRESSED** (52) may understate uncertainty by ~5-8 points compared to the transcript's 68. Minor, within uncertainty band.

---

## Actionable Findings

| Finding | Severity | Action |
|---------|----------|--------|
| 0 direction errors | N/A | None needed |
| 0 polarity inversions | N/A | None needed |
| 46 magnitude-off (all ≤7pts) | Minor | No correction needed — within uncertainty bands |
| 14 evidence-missing (all anomaly files) | Expected | No correction needed — correctly flagged |
| 2016-12-14 minutes UNCERTAINTY_EXPRESSED=52 | Minor | Optional: could adjust to 57-58 |

**Verdict: The v3 scoring dataset passes validation. No corrections required.**

---

## Validation Reports

- [Era 1 (1993-2001)](review_era1_1993_2001.md)
- [Era 2 (2002-2010)](review_era2_2002_2010.md)
- [Era 3 (2011-2019)](review_era3_2011_2019.md)
- [Era 4 (2020-2026)](review_era4_2020_2026.md)
