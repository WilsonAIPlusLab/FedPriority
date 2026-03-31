# Minutes vs Transcript Concordance Report

## Overview

**187 FOMC meetings** have both minutes and transcripts scored with the v3 rubric.
Minutes represent the public-facing summary -- what market participants and the public perceive 
about the Fed's assessment. Transcripts capture the actual deliberation -- the internal decision 
process with individual speaker views, tactical disagreements, and nuances that minutes compress.

**Signed delta convention**: `minutes_score - transcript_score`. Positive = minutes score higher.

## Core Dimension Concordance

| Dimension | N | Signed Delta | MAD | Pearson r | Spearman rho | % Within 10 |
|-----------|---|-------------|-----|-----------|-------------|-------------|
| INFLATION_PRESSURE | 184 | -2.61 | 4.57 | 0.909 | 0.932 | 87.5% |
| OUTPUT_GAP | 184 | +0.26 | 3.08 | 0.936 | 0.926 | 97.8% |
| LABOR_TIGHTNESS | 184 | -0.59 | 3.79 | 0.95 | 0.94 | 95.7% |
| CONSUMPTION_INVESTMENT | 184 | +0.71 | 2.79 | 0.947 | 0.947 | 99.5% |
| FINANCIAL_TIGHTNESS | 184 | -0.89 | 5.89 | 0.826 | 0.753 | 84.8% |
| HAWKISH_DOVISH_LEAN | 184 | -1.19 | 4.40 | 0.952 | 0.947 | 92.4% |
| DISSENT_INTENSITY | 184 | -9.37 | 11.14 | 0.586 | 0.573 | 52.2% |
| FINANCIAL_STABILITY_EMPHASIS | 185 | -8.61 | 11.57 | 0.725 | 0.634 | 58.4% |
| FORWARD_GUIDANCE_TONE | 184 | -0.60 | 4.78 | 0.946 | 0.941 | 90.2% |
| UNCERTAINTY_EXPRESSED | 185 | -3.41 | 7.06 | 0.667 | 0.597 | 78.9% |

## Key Findings

### 1. Systematic Biases (Minutes vs Transcripts)

Dimensions where minutes systematically differ from transcripts:

- **DISSENT_INTENSITY**: Minutes score lower by 9.4 points on average (MAD=11.1)
- **FINANCIAL_STABILITY_EMPHASIS**: Minutes score lower by 8.6 points on average (MAD=11.6)
- **UNCERTAINTY_EXPRESSED**: Minutes score lower by 3.4 points on average (MAD=7.1)
- **INFLATION_PRESSURE**: Minutes score lower by 2.6 points on average (MAD=4.6)
- **HAWKISH_DOVISH_LEAN**: Minutes score lower by 1.2 points on average (MAD=4.4)

### 2. Agreement Strength

Strongest agreement (highest correlation):
- **HAWKISH_DOVISH_LEAN**: r=0.952, 92% within 10 points
- **LABOR_TIGHTNESS**: r=0.95, 96% within 10 points
- **CONSUMPTION_INVESTMENT**: r=0.947, 100% within 10 points

Weakest agreement:
- **FINANCIAL_STABILITY_EMPHASIS**: r=0.725, 58% within 10 points
- **UNCERTAINTY_EXPRESSED**: r=0.667, 79% within 10 points
- **DISSENT_INTENSITY**: r=0.586, 52% within 10 points

### 3. Evolution Over Time

Mean signed delta (minutes - transcript) by era:

| Dimension | 1993-2004 | 2005-2011 | 2012-2026 |
|-----------|----------|----------|----------|
| INFLATION_PRESSURE | -5.0 | -0.2 | -0.9 |
| OUTPUT_GAP | +0.2 | +0.4 | +0.2 |
| LABOR_TIGHTNESS | -0.5 | +0.1 | -1.2 |
| CONSUMPTION_INVESTMENT | +1.5 | -0.1 | +0.2 |
| FINANCIAL_TIGHTNESS | -4.0 | +1.9 | +1.6 |
| HAWKISH_DOVISH_LEAN | +0.7 | -1.5 | -3.8 |
| DISSENT_INTENSITY | -8.4 | -13.8 | -7.7 |
| FINANCIAL_STABILITY_EMPHASIS | -11.0 | -9.1 | -4.9 |
| FORWARD_GUIDANCE_TONE | +0.4 | -2.2 | -0.9 |
| UNCERTAINTY_EXPRESSED | -2.1 | -4.0 | -4.8 |

### 4. Largest Divergences

**66 dimension-meeting pairs** have |delta| > 20:

| Date | Dimension | Minutes | Transcript | Delta |
|------|-----------|---------|------------|-------|
| 1994-05-17 | FINANCIAL_STABILITY_EMPHASIS | 18 | 60 | -42 |
| 2011-12-13 | FORWARD_GUIDANCE_TONE | 5 | 42 | -37 |
| 2001-08-21 | DISSENT_INTENSITY | 15 | 50 | -35 |
| 2010-11-03 | DISSENT_INTENSITY | 35 | 70 | -35 |
| 2011-11-02 | FORWARD_GUIDANCE_TONE | 5 | 40 | -35 |
| 1999-05-18 | DISSENT_INTENSITY | 18 | 52 | -34 |
| 2003-01-29 | FINANCIAL_STABILITY_EMPHASIS | 18 | 52 | -34 |
| 2003-06-25 | FINANCIAL_STABILITY_EMPHASIS | 28 | 62 | -34 |
| 1994-11-15 | FINANCIAL_STABILITY_EMPHASIS | 27 | 60 | -33 |
| 2005-08-09 | FINANCIAL_STABILITY_EMPHASIS | 32 | 65 | -33 |
| 2007-06-28 | FINANCIAL_STABILITY_EMPHASIS | 48 | 15 | +33 |
| 2019-06-19 | UNCERTAINTY_EXPRESSED | 65 | 32 | +33 |
| 2003-01-29 | FINANCIAL_TIGHTNESS | 25 | 57 | -32 |
| 2018-05-02 | FINANCIAL_STABILITY_EMPHASIS | 28 | 60 | -32 |
| 1996-11-13 | FINANCIAL_STABILITY_EMPHASIS | 18 | 48 | -30 |
| 1999-05-18 | FINANCIAL_STABILITY_EMPHASIS | 22 | 52 | -30 |
| 2002-06-26 | FINANCIAL_STABILITY_EMPHASIS | 38 | 68 | -30 |
| 2002-09-24 | FINANCIAL_STABILITY_EMPHASIS | 30 | 60 | -30 |
| 2012-03-13 | FINANCIAL_STABILITY_EMPHASIS | 38 | 8 | +30 |
| 2013-10-30 | UNCERTAINTY_EXPRESSED | 35 | 65 | -30 |

## Interpretation: Public Perception vs Internal Deliberation

### What Minutes Compress

Minutes are drafted by Fed staff and approved by the Committee. They serve a 
communication function -- signaling the Committee's consensus view to markets. 
This process systematically compresses certain aspects of the deliberation:

1. **Dissent and disagreement** are understated in minutes relative to transcripts. 
   Transcripts reveal the full range of individual views, tactical disagreements, 
   and reluctant support that minutes smooth into consensus language.

2. **Financial stability concerns** receive less emphasis in minutes than in transcripts. 
   Detailed individual assessments of market conditions, risk-taking behavior, and 
   systemic vulnerabilities are compressed into brief summary statements.

3. **Uncertainty** is moderated in minutes. Transcripts capture hedging, scenario 
   analysis, and explicit admissions of ignorance that minutes translate into 
   formulaic "risks are roughly balanced" or "uncertainty is elevated" language.

### What Minutes Preserve or Amplify

Some dimensions may show minutes scoring equal to or higher than transcripts, 
reflecting the Committee's desire to clearly communicate certain aspects 
of its assessment to the public.

## Optional Dimension Concordance

| Dimension | N | Signed Delta | MAD | Pearson r |
|-----------|---|-------------|-----|-----------|
| INFLATION_EXPECTATIONS | 147 | -1.39 | 4.92 | 0.78 |
| CREDIT_STRESS | 47 | -0.36 | 6.36 | 0.861 |
| EQUITY_STRESS | 18 | +1.39 | 5.72 | 0.93 |
| BANKING_STRESS | 16 | -6.19 | 8.31 | 0.913 |
| DOLLAR_CONCERN | 39 | +0.41 | 8.87 | 0.664 |
| PRODUCTIVITY | 63 | -0.14 | 5.76 | 0.782 |
