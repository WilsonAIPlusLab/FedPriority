---
title: "FOMC Staff Assessment Scores — staff_scores_v6.csv"
version: 2.0.0-draft
created: 2026-03-30
updated: 2026-10-23
source_file: data/primary/staff_scores_v6.csv
rubric_file: rubrics/staff_scoring_rubric_v4.md
---

## Overview

This file contains meeting-level scores of the Federal Reserve staff's economic and financial assessment as presented in FOMC meeting documents (minutes or transcripts). Each row represents a single meeting-document pair scored by a large language model (LLM) using the v4 scoring rubric (the v4 rubric is applied to every row; the table mixes scoring vintages, see `SCORE_VERSION`). The LLM reads only the staff-attributable content — Tealbook/Greenbook projections, staff presentations by named economists (Stockton, Kohn, Dudley, etc.), and staff-sourced language in minutes ("the staff reported," "the staff forecast") — and ignores participant or Committee member views. Scores reflect what the staff communicated at the time, not ex-post macroeconomic reality. Coverage spans FOMC meetings from 1993 onward, for both minutes and (where available and declassified) transcripts. The file has 495 rows x 43 columns (the 41 columns of the earlier v4 table plus `SCORE_VERSION`; counts recomputed 2026-10-23): 270 minutes rows (1993-02-03 to 2026-09-16) and 225 transcript rows (1993-02-03 to 2020-12-16). 215 meetings have both a minutes and a transcript row (`data/derived/staff_v6_minutes_vs_transcripts.csv`).

**Scoring vintage and validation (rewritten 2026-10-23 for dataset 2.0.0).** This file, `staff_scores_v6.csv`, is the project's canonical staff table (copied from `04_scoring/staff/v4_scores_patched_v6/all_scores_v4_patched_v6.csv` in the project repository; v6 = v5 plus the five 2026 minutes rows; patched v1-v5 are superseded). It replaces `staff_scores_v4.csv` (486 rows), which is removed from the dataset; the two differed in 84-139 of their 486 shared (MEETING_DATE, SOURCE_TYPE) rows for each of the seven dimensions compared (INFLATION_PRESSURE 95, OUTPUT_GAP 92, LABOR_TIGHTNESS 90, CONSUMPTION_INVESTMENT 84, FINANCIAL_CONDITIONS 135, CREDIT_SPREADS 139, EQUITY_VALUATION 120; other dimensions not compared), because the transcripts were re-scored on repaired text. Figures quoted below as "v4" describe that earlier table; they are history, not a description of this file. All scores are produced by LLM agents; there is no human coding or human validation of the scores, including their polarity.

The table is **mixed vintage**. The `SCORE_VERSION` column records each row's vintage (counts recomputed from the file on 2026-10-23):

| SCORE_VERSION | Rows | Minutes | Transcripts |
|---|---|---|---|
| `v4_prior` | 197 | 191 | 6 |
| `v4_patched_2026-10` | 186 | 0 | 186 |
| `v4_prior+credit_v4_1` | 75 | 74 | 1 |
| `v4_patched_2026-10+credit_recheck` | 28 | 0 | 28 |
| `v4_new2026_minutes` | 5 | 5 | 0 |
| `v4_patched_2026-10+credit_v4_1` | 4 | 0 | 4 |
| **Total** | **495** | **270** | **225** |

What each label means is defined by the project's build scripts, which are not shipped in this folder; the descriptions in the `SCORE_VERSION` entry below are inferred from the label text and from the CHANGELOG, not documented by the builder. Compare levels within one vintage only. The five `v4_new2026_minutes` rows (2026-03-18, 04-29, 06-17, 07-29, 09-16) were fresh-scored on 2026-10-16/17, one agent per document, so they belong to a later vintage than the older minutes; their CREDIT_SPREADS were rechecked for v6 and all five were unchanged. The one other 2026 minutes row (2026-01-28) is `v4_prior`. Four older minutes rows (2002-03-19, 2001-11-06, 1997-11-12, 1994-03-22) were re-scored on recovered text after being scored from gutted text (carried in the v6 table; field-level log in the project repository only). Staff transcript rows have no shipped evidence files, and the evidence for minutes (`scoring_evidence/`) covers the original minutes scores, not the v6 table as a whole.

## Unit of Observation

One row = one FOMC meeting document (identified by MEETING_DATE and SOURCE_TYPE). When both minutes and transcript exist for a meeting, they appear as two separate rows.

## Variable Definitions

### Identifier Variables

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| MEETING_DATE | Date (ISO 8601) | YYYY-MM-DD | The document-name date of the meeting: for the 1993-95 meetings and for most two-day meetings after that it is the LAST day (the day on the minutes/transcript file name), not the first. Used as the primary key together with SOURCE_TYPE. Map it to a registry meeting through `data/derived/meeting_key_map.csv` (see Note 8). |
| SOURCE_TYPE | Categorical | `minutes`, `transcript` | Document type scored. `minutes` = the published meeting minutes (synthesized summary, uses staff-attributable language). `transcript` = the verbatim transcript, available after a five-year declassification lag; staff speakers are identified by name. |
| STAFF_TEXT_SCOPE | Categorical | `minutes_staff_sections_split_2026-10` (128), `minutes_staff_sections_only` (142), `transcript_staff_turns_not_fully_audited` (225) | What text the staff scorer was given (last column). 1993-2008 minutes (128 rows): since 2026-10-24 scored blind on a rebuilt staff-only input (staff review of the economy and of financial developments plus the staff forecast; participants' discussion, votes and directive removed; one agent per document; `SCORE_VERSION` `v4.1_split_2026-10`). The input still contains the opening sentence of the financial review that recalls the previous meeting's directive and a few sentences naming the Committee's views (about 5% of staff words); 127 of 128 scorers flagged this in `ANOMALY_NOTE`, most ignored it, about 22 used market facts from that paragraph. A 20-meeting test found no effect detectable beyond scorer noise (about 2 points per score); see DATA_PROVENANCE 5.5. 2009 onward (142 rows): only the staff sections were scored. Before 2026-10-24 the 128 rows were scored on the whole minutes body (`minutes_full_body_incl_participant_discussion`); those scores are replaced. |
| SCORE_VERSION | Categorical | `v4_prior`, `v4_patched_2026-10`, `v4_prior+credit_v4_1`, `v4_patched_2026-10+credit_recheck`, `v4_new2026_minutes`, `v4_patched_2026-10+credit_v4_1` | Scoring vintage of the row (last column of the file; absent from the earlier v4 table). Counts: 197 / 186 / 75 / 28 / 5 / 4 (see the table in the Overview). Reading from the labels (not documented by the builder): `v4_prior` = original V4 score carried unchanged (191 minutes, 6 transcripts); `v4_patched_2026-10` = transcript re-scored on repaired text; labels containing `credit` = additionally touched by the CREDIT_SPREADS level-reading recheck (107 rows in total); `v4_new2026_minutes` = fresh 2026 minutes score. The 79-cell log `data/derived/credit_spreads_v4_1_applied_2026-10-17.csv` describes the earlier v4 table and was not reconciled against these 107 v6 rows. |

---

### Priority groups (added 2026-10-23)

Dataset 2.0.0 is organised around three priorities. `data/derived/priority_variable_map.csv` assigns every score variable to a priority group (the author's judgement, not an estimated result). For the 15 staff dimensions:

| Priority group (`priority_group`) | Staff dimensions |
|---|---|
| `price_stability` (dual mandate) | INFLATION_PRESSURE, INFLATION_GOODS, INFLATION_SERVICES, INFLATION_HOUSING, INFLATION_EXPECTATIONS |
| `max_employment` (dual mandate) | OUTPUT_GAP, LABOR_TIGHTNESS (OUTPUT_GAP is filed under employment; it could reasonably sit elsewhere) |
| `financial_stability` | FINANCIAL_CONDITIONS, TREASURY_STRESS, CREDIT_SPREADS, EQUITY_VALUATION, BANKING_STRESS |
| `context` | CONSUMPTION_INVESTMENT and PRODUCTIVITY (context for the dual mandate), DOLLAR_STRENGTH (context for financial stability) |

Each dimension entry below repeats its group. The `_UNC` and `_CONF` columns are not listed in the map; by construction they follow the group of their dimension.

---

### Scoring Conventions (apply to all dimension scores)

- **Scale**: 1–100 continuous integer. The scale is anchored at 50 (neutral midpoint). Scores are never exactly 0; the minimum is 1, reserved for the most extreme possible case.
- **Polarity**: For every dimension except EQUITY_VALUATION, **higher = more of the named construct** (for the financial dimensions, more stress/tightness). EQUITY_VALUATION is the exception: scores below 50 indicate overvaluation concern and scores above 50 indicate undervaluation or crash/stress concern (see its entry and Note 7). See each dimension entry for the specific polarity statement.
- **N/A**: Assigned when the topic is not discussed at all in the source document. Represented as the string `N/A` in the CSV. Distinct from 50 (which means "discussed but neutral/balanced").
- **UNC columns** (`{DIM}_UNC`): The uncertainty band around the point score, expressed in score points (e.g., a value of 5 means ±5). Reflects the LLM's confidence given text clarity: narrow band (3–5) = staff language is specific and unambiguous; wide band (10–15) = language is vague, mixed, or open to interpretation. `N/A` when the dimension score is `N/A`. **Storage format**: despite the Integer type shown below, UNC cells are stored as text; in the current file (v6; counted 2026-10-23) 2,467 non-N/A cells are plain integers (e.g. `7`) and 2,314 cells, in 307 rows (83 minutes, 224 transcripts), are written with a `+-` prefix (e.g. `+-8`). Strip the prefix before numeric use.
- **CONF columns** (`{DIM}_CONF`): Confidence tier. Reflects the quantity and specificity of textual evidence. Three tiers: `High` = multiple sentences with specific data points; `Moderate` = topic discussed but briefly; `Low` = inferred from limited or indirect language. `N/A` when the dimension score is `N/A`.

---

### Tier 1: Core Economic Dimensions

These dimensions are intended to be scored for every meeting. In the v6 table N/A is rare (counted 2026-10-23): INFLATION_PRESSURE is N/A in 2 rows, OUTPUT_GAP in 1, LABOR_TIGHTNESS in 2 and CONSUMPTION_INVESTMENT in 2, all transcripts; no minutes row is N/A on any of the four. Four transcript rows (of 225) have N/A in at least one of them: 1993-08-17 (LABOR_TIGHTNESS), 1995-02-01 (CONSUMPTION_INVESTMENT), 1996-09-24 (INFLATION_PRESSURE) and 2003-09-15 (all four). 2003-09-15 is a genuine special session (the file is the evening session on communication strategy; the standard briefing is on day 2, 2003-09-16), so its N/A values are legitimate and its ANOMALY_NOTE is correct. The other three were not inspected against the full transcripts for this codebook. Treat N/A as missing, not as neutral. In the earlier v4 table 44 of 216 transcript rows were N/A on at least one core economic dimension, mostly scoring/segmentation failures (no staff-attributable text found); re-scoring the transcripts on fuller text removed most of them.

---

**INFLATION_PRESSURE** — priority group: `price_stability (dual mandate)`

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| INFLATION_PRESSURE | Integer | 1–100 or N/A | Staff's overall assessment of inflation pressure relative to the Federal Reserve's 2% PCE target. Higher = staff perceives MORE inflation pressure. Scores below 50 indicate below-target or disinflationary conditions; 50 = at the 2% target; scores above 50 indicate above-target or accelerating inflation. Era anchors: ~15–20 (2009 deflation scare), ~38–42 (2013–2019 persistent below-target period), ~50 (early 2018 "at target"), ~65–72 (2021 Q3–Q4 elevated), ~82–88 (2022 Q2–Q3 peak). Note: "transitory" forward-looking language does not reduce the score — the score reflects the staff's current-period assessment, not the forecast. |
| INFLATION_PRESSURE_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the INFLATION_PRESSURE score. |
| INFLATION_PRESSURE_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for INFLATION_PRESSURE based on volume and specificity of textual evidence. |

---

**OUTPUT_GAP** — priority group: `max_employment (dual mandate)`

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| OUTPUT_GAP | Integer | 1–100 or N/A | Staff's assessment of where the economy is operating relative to its potential output. Higher = economy operating MORE ABOVE potential (more overheating). Scores below 50 indicate slack or recession; 50 = at potential; above 50 = above trend. Bright-line rule: any "above potential" or "above trend" language must produce a score > 50; any "below potential" or "slack remains" language must produce a score < 50. Era anchors: ~15–22 (GFC trough 2008–2009; COVID Q2 2020), ~35–42 (2010–2014 recovery), ~50–55 (2016–2019 near potential), ~57–63 (late 1990s boom; 2022). |
| OUTPUT_GAP_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the OUTPUT_GAP score. |
| OUTPUT_GAP_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for OUTPUT_GAP. |

---

**LABOR_TIGHTNESS** — priority group: `max_employment (dual mandate)`

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| LABOR_TIGHTNESS | Integer | 1–100 or N/A | Staff's assessment of labor market tightness. Higher = TIGHTER labor market (more worker shortages, lower unemployment, stronger wage pressure). Scores below 50 indicate slack or elevated unemployment; 50 = near NAIRU / full employment; above 50 = tighter than neutral. Era anchors: ~15–22 (2009–2010, 2020 Q2), ~35–40 (2011–2014), ~50 (2016–2017), ~55–62 (2018–2019), ~65–75 (1999–2000, 2022–2023). Calibration note: unemployment below 4% should almost always produce a score above 55. The score reflects the level of tightness, not the rate of improvement. |
| LABOR_TIGHTNESS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the LABOR_TIGHTNESS score. |
| LABOR_TIGHTNESS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for LABOR_TIGHTNESS. |

---

**CONSUMPTION_INVESTMENT** — priority group: `context (context for the dual mandate)`

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| CONSUMPTION_INVESTMENT | Integer | 1–100 or N/A | Staff's assessment of the combined strength of consumer spending and business investment relative to trend. Higher = STRONGER demand. Scores below 50 indicate below-trend or contracting demand; 50 = at-trend pace; above 50 = above-trend or robust. The score reflects the net position across both consumer spending and business investment, weighted by the document's discussion emphasis. Era anchors: ~15–20 (2008 Q4–2009 Q1; 2020 Q2), ~35–42 (2011–2013 "moderate"), ~50–55 (2014–2019 "solid pace"), ~62–68 (2021 Q3–2022 Q1 surge). |
| CONSUMPTION_INVESTMENT_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the CONSUMPTION_INVESTMENT score. |
| CONSUMPTION_INVESTMENT_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for CONSUMPTION_INVESTMENT. |

---

**PRODUCTIVITY** — priority group: `context (context for the dual mandate)`

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| PRODUCTIVITY | Integer | 1–100 or N/A | Staff's assessment of productivity growth. Higher = MORE productivity growth perceived. Scores below 50 indicate below-historical-trend growth; 50 = at historical trend (~2% annually); above 50 = above-trend gains. This dimension is frequently N/A because productivity is not discussed in many meetings. |
| PRODUCTIVITY_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the PRODUCTIVITY score. |
| PRODUCTIVITY_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for PRODUCTIVITY. |

---

### Tier 1: Core Financial Dimensions

---

**FINANCIAL_CONDITIONS** — priority group: `financial_stability`

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| FINANCIAL_CONDITIONS | Integer | 1–100 or N/A | Staff's assessment of overall financial conditions. Higher = conditions are TIGHTER / more restrictive. Scores below 50 indicate loose or accommodative conditions; 50 = neutral (the 2017–2019 period is the calibration anchor for neutral); above 50 = tighter than normal. Bright-line rule: "accommodative" / "supportive" / "easy" language must produce a score < 50; "tight" / "restrictive" / "strained" language must produce a score > 50. Note: this dimension scores conditions (credit availability, spreads, market functioning), not the policy rate itself. Era anchors (rubric targets; observed scores deviate, see the bracket): ~10–20 (2005–2006 pre-crisis ease), ~46–54 (2017–2019 neutral), ~55–65 (2022 rate hike effects), ~85–95 (September 2008 credit freeze; March 2020 dash for cash). [Observed in this v6 file, recomputed 2026-10-23: 2005–2006 scores range 20–43 (mean 28.4, n=32); 2017–2019 range 12–62 (mean 39.8, n=48). The earlier v4 table had 22–38 (mean 27) and 18–53 (mean 39.4, n=36).] FINANCIAL_CONDITIONS is N/A in 3 transcript rows. |
| FINANCIAL_CONDITIONS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the FINANCIAL_CONDITIONS score. |
| FINANCIAL_CONDITIONS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for FINANCIAL_CONDITIONS. |

---

**TREASURY_STRESS** — priority group: `financial_stability`

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| TREASURY_STRESS | Integer | 1–100 or N/A | Staff's assessment of Treasury market functioning. Higher = MORE market dysfunction. Scores below 50 indicate smooth or normal functioning; 50 = normal market operation; above 55 indicates actual dysfunction (not merely yield movements). Critical note: yield movements from policy expectations or inflation expectations are normal market functioning and should NOT push this score above 55. Scores above 55 require evidence of actual market dysfunction: liquidity problems, bid-ask spread widening, settlement failures, auction demand shortfalls, or basis-trade stress. N/A if Treasury market functioning is not specifically discussed. Era anchors (rubric targets; the 2008 maximum observed in the file is 85, mean 60.5): ~25–35 (2010–2015 calm), ~40–50 (normal), ~65–80 (March 2020 "dash for cash"), ~85–95 (September–October 2008). [Recomputed 2026-10-23 on this v6 file: 2008 maximum 85, minimum 45, n=14, mean 60.5. The earlier v4 table had the same maximum (n=13, mean 62.5).] |
| TREASURY_STRESS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the TREASURY_STRESS score. |
| TREASURY_STRESS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for TREASURY_STRESS. |

---

**CREDIT_SPREADS** — priority group: `financial_stability`

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| CREDIT_SPREADS | Integer | 1–100 or N/A | Staff's assessment of credit spread conditions. Higher = MORE credit stress (wider spreads, reduced availability). Scores below 50 indicate compressed or below-normal spreads; 50 = normal credit conditions; above 50 = spreads widening or elevated. Bright-line rule: "compressed" / "narrow" / "historically tight" language must produce a score < 50; "widened" / "elevated" language must produce a score > 50. Note: the score reflects the level of spreads, not the direction of change (spreads widening from very compressed levels can still score below 50). Era anchors: ~10–20 (2005–2006 extremely compressed), ~30–40 (2013–2019 generally favorable), ~55–65 (2022 mild widening), ~80–95 (2008 Q4 credit freeze). |
| CREDIT_SPREADS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the CREDIT_SPREADS score. |
| CREDIT_SPREADS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for CREDIT_SPREADS. |

---

**EQUITY_VALUATION** — priority group: `financial_stability`

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| EQUITY_VALUATION | Integer | 1–100 or N/A | Staff's assessment of equity market valuation and concern. Non-uniform polarity: scores below 50 indicate overvaluation concern (elevated/bubble territory); 50 = roughly fair valued; above 50 = undervaluation or crash/stress concern (so a high score means more crash concern, a low score more bubble concern). Important: this dimension scores the staff's stated valuation concern, not price direction. "Equities declined" alone maps to approximately 50–55. "Equities remain elevated despite decline" maps to 25–35. "Equities at distressed levels" maps to 70–80. N/A if equity markets are not specifically discussed. Era anchors: ~15–25 (2000 dot-com bubble, 2005–2006 stretched valuations), ~40–50 (2013–2019 typical), ~65–80 (2008 Q4 crash, March 2020). |
| EQUITY_VALUATION_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the EQUITY_VALUATION score. |
| EQUITY_VALUATION_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for EQUITY_VALUATION. |

---

**BANKING_STRESS** — priority group: `financial_stability`

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| BANKING_STRESS | Integer | 1–100 or N/A | Staff's assessment of banking system health, expressed as stress. Higher = MORE banking system stress or impairment. Scores below 50 indicate a healthy, well-capitalized system; 50 = neutral/mixed; above 50 = emerging or significant stress. Bright-line rule: "well-capitalized" / "sound" / "healthy" language must produce a score < 50 (low stress). Note: this dimension was named BANKING_HEALTH in v3, causing widespread polarity inversion — v4 renames it to BANKING_STRESS to enforce the correct direction. N/A if banking system conditions are not specifically discussed. Era anchors: ~25–35 (2014–2019 well-capitalized), ~40–50 (2006–2007 growing concerns), ~55–65 (March 2023 SVB episode), ~70–85 (2008–2009 systemic crisis). |
| BANKING_STRESS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the BANKING_STRESS score. |
| BANKING_STRESS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for BANKING_STRESS. |

---

**DOLLAR_STRENGTH** — priority group: `context (context for financial stability)`

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| DOLLAR_STRENGTH | Integer | 1–100 or N/A | Staff's assessment of the U.S. dollar's exchange rate level and direction. Higher = STRONGER dollar (appreciation). Scores below 50 indicate dollar weakness or depreciation; 50 = stable, no directional concern; above 50 = dollar strengthening or strong. Bright-line rule: dollar appreciation / strengthening language must produce a score > 50; dollar depreciation / weakening language must produce a score < 50. Note: this dimension was named DOLLAR_FX in v3 and suffered approximately 40% polarity inversion. N/A if dollar/foreign exchange is not specifically discussed. Era anchors: ~20–30 (2003–2004 dollar decline; 2017 depreciation), ~45–55 (2012–2013 stable), ~60–70 (2015 H1 sharp appreciation), ~75–85 (2022 Q3 DXY at 20-year highs). |
| DOLLAR_STRENGTH_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the DOLLAR_STRENGTH score. |
| DOLLAR_STRENGTH_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for DOLLAR_STRENGTH. |

---

### Tier 2: Inflation Sub-Component Dimensions

These four dimensions are scored only when the staff specifically discusses that sub-component of inflation. They do not carry separate UNC or CONF columns (unlike Tier 1 dimensions). All four share the same polarity: higher = more price pressure in that category. N/A is the common value when the sub-component is not discussed (v6 N/A counts, minutes / transcripts: INFLATION_GOODS 59 / 85, INFLATION_SERVICES 216 / 174, INFLATION_HOUSING 220 / 184, INFLATION_EXPECTATIONS 65 / 34). Priority group: all four are `price_stability` (dual mandate).

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
| ANOMALY_FLAG | Categorical | `No`, `Yes` | Indicates whether the scoring LLM identified any anomaly or unusual characteristic requiring human review. `No` = standard scoring proceeded without issues. `Yes` = see ANOMALY_NOTE for explanation. Flag counts (v6): 339 `No`, 156 `Yes` (minutes 258 / 12, transcripts 81 / 144). ANOMALY_NOTE is non-empty in all 156 `Yes` rows but also in 22 `No` rows (resolved-issue notes, for example "Prior truncation/missing-briefing flag is resolved by the full text"), so it is empty for 317 of the 339 `No` rows, not all of them; the flag is not a reliable indicator of a problem. Common triggers: emergency meeting with abbreviated briefing, special-topic meeting (balance sheet, framework review) scored entirely N/A, unsegmented pre-2005 minutes requiring manual staff/participant separation, or apparent bright-line rule violations. |
| ANOMALY_NOTE | String | Free text or empty | Human-readable explanation of the anomaly flagged in ANOMALY_FLAG. Normally empty when ANOMALY_FLAG = `No`, with 22 exceptions (see above). Examples: "Emergency meeting; briefing covered only financial market conditions; all economic dimensions N/A," or "Pre-2005 minutes; staff and participant content mixed; scorer relied on 'the staff reported' language cues." |

---

## Notes

1. **N/A vs. 50**: These are distinct values with different interpretations. `N/A` means the topic was not discussed in the source document. `50` means the topic was discussed and the staff's assessment was neutral or balanced. Do not treat N/A as missing-at-random; it is informative (certain topics, especially Tier 2 sub-components and PRODUCTIVITY, are only discussed when there is something to say about them).

2. **Tier 2 sub-components lack UNC/CONF**: The four Tier 2 inflation sub-component columns (INFLATION_GOODS, INFLATION_SERVICES, INFLATION_HOUSING, INFLATION_EXPECTATIONS) are single point-estimate columns without associated uncertainty or confidence columns. Researchers using these variables should treat them with lower precision than Tier 1 dimensions.

3. **CORRECTION_NOTES**: An earlier version of the documentation referenced a CORRECTION_NOTES column, but this column is not present in staff_scores_v6.csv. Corrections to individual scores are tracked in the ANOMALY_FLAG and ANOMALY_NOTE columns and, for the vintage of each row, in SCORE_VERSION. The former `data/derived/correction_log.csv` was removed in dataset 2.0.0 (it used V3 dimension names that do not exist in the current table).

4. **Source type differences**: Minutes are available for the meetings that have a minutes document (270 minutes rows); not every registry meeting has one; transcripts (225 rows) become available with a five-year lag; 215 meetings have both. For overlapping meeting-date rows, the minutes and transcript scores are independent assessments of the same meeting. Systematic differences between them reflect both document differences (synthesis vs. verbatim) and construct differences (staff presentations are more structured in transcripts). [Recomputed 2026-10-24 on this v6 file after the 1993-2008 minutes were re-scored on staff-only text: the FINANCIAL_CONDITIONS transcript-minus-minutes gap on identical-date pairs is -1.55 (t=-2.47, n=213 of the 215 pairs; 2 pairs have N/A), the value the README reports. On 2026-10-23, before that re-score, it was +0.92 (t=1.53), so the sign depends on the scoring vintage and scorer noise is about 2 points per score. In the earlier v4 table the gap was +1.55 (t=2.70, n=166; +1.73 in the original `v4_scores/all_scores_v4.csv` before four gutted-text minutes re-scores), so the size of the gap depends on the scoring vintage. Chair splits (Greenspan +2.1, Bernanke -0.6, Yellen +4.2, Powell +4.5, n=6) were computed on the earlier v4 table and were not recomputed on v6. The per-dimension gap table is `data/derived/staff_v6_minutes_vs_transcripts.csv` (2,166 numeric pairs; its diff column is minutes minus transcript, the opposite sign to the gap quoted here).]

5. **Pre-2009 minutes (split rebuilt 2026-10-24)**: The 1993-2008 minutes do not separate staff review sections from participant discussion in the source; the dataset's parse now does, by text anchors, and the 128 rows were re-scored on the staff-only part (see `STAFF_TEXT_SCOPE`). Residual Committee-recap sentences remain. Earlier text: before approximately 2005, FOMC minutes did not cleanly separate them. The scoring rubric instructs the LLM to score only staff-attributable language ("the staff reported," "the Greenbook projection"). Users should treat pre-2005 scores as somewhat noisier.

6. **Early transcript coverage (1993–1997)**: Transcripts from this period are structured differently — staff presentations may be less segmented, and some staff economists gave combined economic-and-financial briefings. Confidence tiers for this period tend to be lower.

7. **EQUITY_VALUATION polarity**: This dimension has an unusual polarity. Below 50 indicates overvaluation concern (the staff sees equities as too high, a "bubble" concern). Above 50 indicates undervaluation or crash concern. The neutral midpoint (50) reflects fair valuation with no particular concern. This is the one dimension where a lower score can indicate a type of financial instability (asset price excess). See the rubric Bright-Line Rules for further guidance. [Recomputed 2026-10-23 on this v6 file: the 2008 transcript mean is 64.9 (n=8, range 50–80) and the 2000 transcript mean is 34.2 (n=8, range 12–62). The commonly quoted 72.0 for 2008 rested on only 5 transcripts in the earlier v4 table (range 65–80; 2000 mean 34.9 there). The direction (2008 above 50, 2000 below 50) holds in every vintage; the level does not, so do not cite 72.0 as a stable figure.]

8. **Join caveat and revision history (updated 2026-10-23)**: 11 score rows (10 transcript, 1 minutes) carry MEETING_DATE values that are not `meeting_date` keys in `data/primary/meeting_registry.csv` (1996-01-31, 1996-07-03, 1997-02-05, 1997-07-02, 1998-02-04, 1998-07-01, 1999-02-03, 1999-06-30, 2003-09-16 (minutes and transcript), 2012-10-24; ten distinct dates, recomputed on v6); each is the second day of a two-day meeting whose registry `meeting_date` is the first day, so a naive join to the registry drops them. Do not join on `start_date` instead: it matches only 204 of the 495 rows, because for most two-day meetings the score key is the last day. Use `data/derived/meeting_key_map.csv`, which maps the keys of the staff v6 and discussion V4.1 tables to a registry meeting (the README reports 0 unmatched; not re-run here). Earlier text named `02_registry/meeting_key_map.csv` and `tools/check_keys.py`; those are in the project repository, which is not shipped. Four minutes rows (1994-03-22, 1997-11-12, 2001-11-06, 2002-03-19) were originally scored from gutted source text and were re-scored on recovered text on 2026-10-17 (CHANGELOG 1.3.0); the backup of the pre-fix v4 file is not part of dataset 2.0.0.


**CREDIT_SPREADS rule note (2026-10-17; references updated 2026-10-23).** The V4 rubric used for the original scoring contradicted itself on CREDIT_SPREADS (bright line: "widened"/"elevated" must score above 50; gotcha: score the level, not the direction). The project decision is that the level governs (rubric v4.1, `04_scoring/staff/rubric/FOMC_Staff_Review_Prompt_v4_1.md` in the project repository; not shipped in this folder, where only `rubrics/staff_scoring_rubric_v4.md` is present and still carries the contradictory wording). On 2026-10-17 every minutes row and every transcript row still above 50 in the patched table of the time (v4; 93 documents: 74 minutes, 19 transcripts not already rechecked) was re-checked, one fresh agent per document, on the CREDIT_SPREADS dimension only (outputs in `04_scoring/staff/credit_recheck_v4_1/`, project repository only; 23 scores moved, mean -4.6 points, 46 confidences lowered, 7 of 93 now at or below 50). The 74 minutes rows and 5 transcript rows whose values matched the patched basis were updated in the then v4 table (log: `data/derived/credit_spreads_v4_1_applied_2026-10-17.csv`, 79 cells incl. UNC/CONF). 14 transcript rows in that original table differed from the patched basis and were left unchanged because the patched tables were re-scored on repaired transcripts. The five 2026 minutes rows were also rechecked for v6 and all five were unchanged. 53 transcripts had been rechecked earlier under the same rule in the patched tables. In this v6 file the rows touched by the recheck carry `credit` in SCORE_VERSION (107 rows: 75 `v4_prior+credit_v4_1`, 28 `v4_patched_2026-10+credit_recheck`, 4 `v4_patched_2026-10+credit_v4_1`); the 79-cell log was not re-reconciled against v6, and whether every other transcript row follows the old or the new rule cannot be determined from the file. The CREDIT_SPREADS column is therefore mixed-vintage (it is N/A in 30 transcript and 8 minutes rows). Do not difference this series against discussion CREDIT_SPREADS, and compare within one SCORE_VERSION. [The figures 93 documents (74 + 19), 23 scores moved (mean -4.6), 7 of 93 at or below 50 and 79 cells were re-derived on 2026-10-17 and are not re-derived here. The 2008-01-30 minutes recheck input was an attendee list only (4,776 bytes); its decision (70 unchanged) is supported by the full minutes text but was not made on the supplied input.]
