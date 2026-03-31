---
title: "FOMC Staff Assessment Scores — staff_scores_v4.csv"
version: 1.0
created: 2026-03-30
source_file: data/primary/staff_scores_v4.csv
rubric_file: rubrics/staff_scoring_rubric_v4.md
---

## Overview

This file contains meeting-level scores of the Federal Reserve staff's economic and financial assessment as presented in FOMC meeting documents (minutes or transcripts). Each row represents a single meeting-document pair scored by a large language model (LLM) using the v4 scoring rubric. The LLM reads only the staff-attributable content — Tealbook/Greenbook projections, staff presentations by named economists (Stockton, Kohn, Dudley, etc.), and staff-sourced language in minutes ("the staff reported," "the staff forecast") — and ignores participant or Committee member views. Scores reflect what the staff communicated at the time, not ex-post macroeconomic reality. Coverage spans FOMC meetings from 1993 onward, for both minutes and (where available and declassified) transcripts.

## Unit of Observation

One row = one FOMC meeting document (identified by MEETING_DATE and SOURCE_TYPE). When both minutes and transcript exist for a meeting, they appear as two separate rows.

## Variable Definitions

### Identifier Variables

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| MEETING_DATE | Date (ISO 8601) | YYYY-MM-DD | Date on which the FOMC meeting started. For multi-day meetings, this is the first day. Used as the primary key together with SOURCE_TYPE. |
| SOURCE_TYPE | Categorical | `minutes`, `transcript` | Document type scored. `minutes` = the published meeting minutes (synthesized summary, uses staff-attributable language). `transcript` = the verbatim transcript, available after a five-year declassification lag; staff speakers are identified by name. |

---

### Scoring Conventions (apply to all dimension scores)

- **Scale**: 1–100 continuous integer. The scale is anchored at 50 (neutral midpoint). Scores are never exactly 0; the minimum is 1, reserved for the most extreme possible case.
- **Polarity**: Uniform across all dimensions — **higher = more of the named construct** without exception. See each dimension entry for the specific polarity statement.
- **N/A**: Assigned when the topic is not discussed at all in the source document. Represented as the string `N/A` in the CSV. Distinct from 50 (which means "discussed but neutral/balanced").
- **UNC columns** (`{DIM}_UNC`): The uncertainty band around the point score, expressed in score points (e.g., a value of 5 means ±5). Reflects the LLM's confidence given text clarity: narrow band (3–5) = staff language is specific and unambiguous; wide band (10–15) = language is vague, mixed, or open to interpretation. `N/A` when the dimension score is `N/A`.
- **CONF columns** (`{DIM}_CONF`): Confidence tier. Reflects the quantity and specificity of textual evidence. Three tiers: `High` = multiple sentences with specific data points; `Moderate` = topic discussed but briefly; `Low` = inferred from limited or indirect language. `N/A` when the dimension score is `N/A`.

---

### Tier 1: Core Economic Dimensions

These dimensions are scored for every meeting. `N/A` is used only in the rare case of a truly atypical meeting (emergency call, framework-only session) where no economic assessment was presented.

---

**INFLATION_PRESSURE**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| INFLATION_PRESSURE | Integer | 1–100 or N/A | Staff's overall assessment of inflation pressure relative to the Federal Reserve's 2% PCE target. Higher = staff perceives MORE inflation pressure. Scores below 50 indicate below-target or disinflationary conditions; 50 = at the 2% target; scores above 50 indicate above-target or accelerating inflation. Era anchors: ~15–20 (2009 deflation scare), ~38–42 (2013–2019 persistent below-target period), ~50 (early 2018 "at target"), ~65–72 (2021 Q3–Q4 elevated), ~82–88 (2022 Q2–Q3 peak). Note: "transitory" forward-looking language does not reduce the score — the score reflects the staff's current-period assessment, not the forecast. |
| INFLATION_PRESSURE_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the INFLATION_PRESSURE score. |
| INFLATION_PRESSURE_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for INFLATION_PRESSURE based on volume and specificity of textual evidence. |

---

**OUTPUT_GAP**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| OUTPUT_GAP | Integer | 1–100 or N/A | Staff's assessment of where the economy is operating relative to its potential output. Higher = economy operating MORE ABOVE potential (more overheating). Scores below 50 indicate slack or recession; 50 = at potential; above 50 = above trend. Bright-line rule: any "above potential" or "above trend" language must produce a score > 50; any "below potential" or "slack remains" language must produce a score < 50. Era anchors: ~15–22 (GFC trough 2008–2009; COVID Q2 2020), ~35–42 (2010–2014 recovery), ~50–55 (2016–2019 near potential), ~57–63 (late 1990s boom; 2022). |
| OUTPUT_GAP_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the OUTPUT_GAP score. |
| OUTPUT_GAP_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for OUTPUT_GAP. |

---

**LABOR_TIGHTNESS**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| LABOR_TIGHTNESS | Integer | 1–100 or N/A | Staff's assessment of labor market tightness. Higher = TIGHTER labor market (more worker shortages, lower unemployment, stronger wage pressure). Scores below 50 indicate slack or elevated unemployment; 50 = near NAIRU / full employment; above 50 = tighter than neutral. Era anchors: ~15–22 (2009–2010, 2020 Q2), ~35–40 (2011–2014), ~50 (2016–2017), ~55–62 (2018–2019), ~65–75 (1999–2000, 2022–2023). Calibration note: unemployment below 4% should almost always produce a score above 55. The score reflects the level of tightness, not the rate of improvement. |
| LABOR_TIGHTNESS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the LABOR_TIGHTNESS score. |
| LABOR_TIGHTNESS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for LABOR_TIGHTNESS. |

---

**CONSUMPTION_INVESTMENT**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| CONSUMPTION_INVESTMENT | Integer | 1–100 or N/A | Staff's assessment of the combined strength of consumer spending and business investment relative to trend. Higher = STRONGER demand. Scores below 50 indicate below-trend or contracting demand; 50 = at-trend pace; above 50 = above-trend or robust. The score reflects the net position across both consumer spending and business investment, weighted by the document's discussion emphasis. Era anchors: ~15–20 (2008 Q4–2009 Q1; 2020 Q2), ~35–42 (2011–2013 "moderate"), ~50–55 (2014–2019 "solid pace"), ~62–68 (2021 Q3–2022 Q1 surge). |
| CONSUMPTION_INVESTMENT_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the CONSUMPTION_INVESTMENT score. |
| CONSUMPTION_INVESTMENT_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for CONSUMPTION_INVESTMENT. |

---

**PRODUCTIVITY**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| PRODUCTIVITY | Integer | 1–100 or N/A | Staff's assessment of productivity growth. Higher = MORE productivity growth perceived. Scores below 50 indicate below-historical-trend growth; 50 = at historical trend (~2% annually); above 50 = above-trend gains. This dimension is frequently N/A because productivity is not discussed in many meetings. |
| PRODUCTIVITY_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the PRODUCTIVITY score. |
| PRODUCTIVITY_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for PRODUCTIVITY. |

---

### Tier 1: Core Financial Dimensions

---

**FINANCIAL_CONDITIONS**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| FINANCIAL_CONDITIONS | Integer | 1–100 or N/A | Staff's assessment of overall financial conditions. Higher = conditions are TIGHTER / more restrictive. Scores below 50 indicate loose or accommodative conditions; 50 = neutral (the 2017–2019 period is the calibration anchor for neutral); above 50 = tighter than normal. Bright-line rule: "accommodative" / "supportive" / "easy" language must produce a score < 50; "tight" / "restrictive" / "strained" language must produce a score > 50. Note: this dimension scores conditions (credit availability, spreads, market functioning), not the policy rate itself. Era anchors: ~10–20 (2005–2006 pre-crisis ease), ~46–54 (2017–2019 neutral), ~55–65 (2022 rate hike effects), ~85–95 (September 2008 credit freeze; March 2020 dash for cash). |
| FINANCIAL_CONDITIONS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the FINANCIAL_CONDITIONS score. |
| FINANCIAL_CONDITIONS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for FINANCIAL_CONDITIONS. |

---

**TREASURY_STRESS**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| TREASURY_STRESS | Integer | 1–100 or N/A | Staff's assessment of Treasury market functioning. Higher = MORE market dysfunction. Scores below 50 indicate smooth or normal functioning; 50 = normal market operation; above 55 indicates actual dysfunction (not merely yield movements). Critical note: yield movements from policy expectations or inflation expectations are normal market functioning and should NOT push this score above 55. Scores above 55 require evidence of actual market dysfunction: liquidity problems, bid-ask spread widening, settlement failures, auction demand shortfalls, or basis-trade stress. N/A if Treasury market functioning is not specifically discussed. Era anchors: ~25–35 (2010–2015 calm), ~40–50 (normal), ~65–80 (March 2020 "dash for cash"), ~85–95 (September–October 2008). |
| TREASURY_STRESS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the TREASURY_STRESS score. |
| TREASURY_STRESS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for TREASURY_STRESS. |

---

**CREDIT_SPREADS**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| CREDIT_SPREADS | Integer | 1–100 or N/A | Staff's assessment of credit spread conditions. Higher = MORE credit stress (wider spreads, reduced availability). Scores below 50 indicate compressed or below-normal spreads; 50 = normal credit conditions; above 50 = spreads widening or elevated. Bright-line rule: "compressed" / "narrow" / "historically tight" language must produce a score < 50; "widened" / "elevated" language must produce a score > 50. Note: the score reflects the level of spreads, not the direction of change (spreads widening from very compressed levels can still score below 50). Era anchors: ~10–20 (2005–2006 extremely compressed), ~30–40 (2013–2019 generally favorable), ~55–65 (2022 mild widening), ~80–95 (2008 Q4 credit freeze). |
| CREDIT_SPREADS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the CREDIT_SPREADS score. |
| CREDIT_SPREADS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for CREDIT_SPREADS. |

---

**EQUITY_VALUATION**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| EQUITY_VALUATION | Integer | 1–100 or N/A | Staff's assessment of equity market valuation and concern. Higher = MORE concern (overvaluation or crash/stress concern). Scores below 50 indicate overvaluation concern (elevated/bubble territory); 50 = roughly fair valued; above 50 = undervaluation or crash concern. Important: this dimension scores the staff's stated valuation concern, not price direction. "Equities declined" alone maps to approximately 50–55. "Equities remain elevated despite decline" maps to 25–35. "Equities at distressed levels" maps to 70–80. N/A if equity markets are not specifically discussed. Era anchors: ~15–25 (2000 dot-com bubble, 2005–2006 stretched valuations), ~40–50 (2013–2019 typical), ~65–80 (2008 Q4 crash, March 2020). |
| EQUITY_VALUATION_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the EQUITY_VALUATION score. |
| EQUITY_VALUATION_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for EQUITY_VALUATION. |

---

**BANKING_STRESS**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| BANKING_STRESS | Integer | 1–100 or N/A | Staff's assessment of banking system health, expressed as stress. Higher = MORE banking system stress or impairment. Scores below 50 indicate a healthy, well-capitalized system; 50 = neutral/mixed; above 50 = emerging or significant stress. Bright-line rule: "well-capitalized" / "sound" / "healthy" language must produce a score < 50 (low stress). Note: this dimension was named BANKING_HEALTH in v3, causing widespread polarity inversion — v4 renames it to BANKING_STRESS to enforce the correct direction. N/A if banking system conditions are not specifically discussed. Era anchors: ~25–35 (2014–2019 well-capitalized), ~40–50 (2006–2007 growing concerns), ~55–65 (March 2023 SVB episode), ~70–85 (2008–2009 systemic crisis). |
| BANKING_STRESS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the BANKING_STRESS score. |
| BANKING_STRESS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for BANKING_STRESS. |

---

**DOLLAR_STRENGTH**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| DOLLAR_STRENGTH | Integer | 1–100 or N/A | Staff's assessment of the U.S. dollar's exchange rate level and direction. Higher = STRONGER dollar (appreciation). Scores below 50 indicate dollar weakness or depreciation; 50 = stable, no directional concern; above 50 = dollar strengthening or strong. Bright-line rule: dollar appreciation / strengthening language must produce a score > 50; dollar depreciation / weakening language must produce a score < 50. Note: this dimension was named DOLLAR_FX in v3 and suffered approximately 40% polarity inversion. N/A if dollar/foreign exchange is not specifically discussed. Era anchors: ~20–30 (2003–2004 dollar decline; 2017 depreciation), ~45–55 (2012–2013 stable), ~60–70 (2015 H1 sharp appreciation), ~75–85 (2022 Q3 DXY at 20-year highs). |
| DOLLAR_STRENGTH_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the DOLLAR_STRENGTH score. |
| DOLLAR_STRENGTH_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for DOLLAR_STRENGTH. |

---

### Tier 2: Inflation Sub-Component Dimensions

These four dimensions are scored only when the staff specifically discusses that sub-component of inflation. They do not carry separate UNC or CONF columns in v4 (unlike Tier 1 dimensions). All four share the same polarity: higher = more price pressure in that category. N/A is the common value when the sub-component is not discussed.

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| INFLATION_GOODS | Integer | 1–100 or N/A | Staff's assessment of goods price inflation. Higher = MORE goods price pressure. Score of 1 = falling goods prices (deflation); 50 = stable goods prices; 100 = surging goods inflation. Commonly elevated during supply-chain disruptions (2021–2022) and near N/A or below 50 in normal periods. |
| INFLATION_SERVICES | Integer | 1–100 or N/A | Staff's assessment of services price inflation. Higher = MORE services price pressure. Score of 1 = falling services prices; 50 = stable services prices; 100 = surging services inflation. Structurally stickier than goods inflation; typically slower to respond to rate changes. |
| INFLATION_HOUSING | Integer | 1–100 or N/A | Staff's assessment of housing/shelter inflation. Higher = MORE housing price or rent pressure. Score of 1 = declining rents and shelter costs; 50 = stable shelter costs; 100 = surging housing inflation. Important component of core PCE; lagged response to real-time rent data is a known issue. |
| INFLATION_EXPECTATIONS | Integer | 1–100 or N/A | Staff's assessment of inflation expectations anchoring. Higher = MORE concern about expectations becoming unanchored or drifting upward. Score of 1 = expectations anchored well below target (deflation anchoring concern); 50 = expectations anchored at the 2% target; 100 = expectations unanchored or rising materially above target. Era anchors: ~25–35 (2009 "risk of unanchoring to downside"), ~45–55 (2014–2019 "well-anchored"), ~60–70 (2022 "showing signs of moving up"). |

---

### Quality and Anomaly Variables

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| ANOMALY_FLAG | Categorical | `No`, `Yes` | Indicates whether the scoring LLM identified any anomaly or unusual characteristic requiring human review. `No` = standard scoring proceeded without issues. `Yes` = see ANOMALY_NOTE for explanation. Common triggers: emergency meeting with abbreviated briefing, special-topic meeting (balance sheet, framework review) scored entirely N/A, unsegmented pre-2005 minutes requiring manual staff/participant separation, or apparent bright-line rule violations. |
| ANOMALY_NOTE | String | Free text or empty | Human-readable explanation of the anomaly flagged in ANOMALY_FLAG. Empty string when ANOMALY_FLAG = `No`. Examples: "Emergency meeting; briefing covered only financial market conditions; all economic dimensions N/A," or "Pre-2005 minutes; staff and participant content mixed; scorer relied on 'the staff reported' language cues." |

---

## Notes

1. **N/A vs. 50**: These are distinct values with different interpretations. `N/A` means the topic was not discussed in the source document. `50` means the topic was discussed and the staff's assessment was neutral or balanced. Do not treat N/A as missing-at-random; it is informative (certain topics, especially Tier 2 sub-components and PRODUCTIVITY, are only discussed when there is something to say about them).

2. **Tier 2 sub-components lack UNC/CONF**: The four Tier 2 inflation sub-component columns (INFLATION_GOODS, INFLATION_SERVICES, INFLATION_HOUSING, INFLATION_EXPECTATIONS) are single point-estimate columns without associated uncertainty or confidence columns. Researchers using these variables should treat them with lower precision than Tier 1 dimensions.

3. **CORRECTION_NOTES**: An earlier version of the documentation referenced a CORRECTION_NOTES column, but this column is not present in staff_scores_v4.csv. Corrections to individual scores are tracked in the ANOMALY_FLAG and ANOMALY_NOTE columns; the full correction log is at `data/derived/correction_log.csv`.

4. **Source type differences**: Minutes are available for all meetings; transcripts become available with a five-year lag. For overlapping meeting-date rows, the minutes and transcript scores are independent assessments of the same meeting. Systematic differences between them reflect both document differences (synthesis vs. verbatim) and construct differences (staff presentations are more structured in transcripts).

5. **Pre-2005 unsegmented minutes**: Before approximately 2005, FOMC minutes did not cleanly separate staff review sections from participant discussion. The scoring rubric instructs the LLM to score only staff-attributable language ("the staff reported," "the Greenbook projection"). Users should treat pre-2005 scores as somewhat noisier.

6. **Early transcript coverage (1993–1997)**: Transcripts from this period are structured differently — staff presentations may be less segmented, and some staff economists gave combined economic-and-financial briefings. Confidence tiers for this period tend to be lower.

7. **EQUITY_VALUATION polarity**: This dimension has an unusual polarity. Below 50 indicates overvaluation concern (the staff sees equities as too high, a "bubble" concern). Above 50 indicates undervaluation or crash concern. The neutral midpoint (50) reflects fair valuation with no particular concern. This is the one dimension where a lower score can indicate a type of financial instability (asset price excess). See the rubric Bright-Line Rules for further guidance.
