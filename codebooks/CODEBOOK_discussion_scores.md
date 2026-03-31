---
title: "FOMC Participant Discussion Scores — discussion_scores_v3.csv"
version: 1.0
created: 2026-03-30
source_file: data/primary/discussion_scores_v3.csv
rubric_file: rubrics/discussion_scoring_rubric_v3.md
---

## Overview

This file contains meeting-level scores of FOMC participant (member and president) discussion as captured in meeting documents (minutes or transcripts). Each row represents a single meeting-document pair scored by a large language model (LLM) using the v3 discussion rubric. Unlike the staff assessment scores, which reflect the views of Federal Reserve economists, these scores capture the collective center of gravity of participant opinions, preferences, and emphasis — the views of voting and non-voting members of the Federal Open Market Committee. The LLM is instructed to score only participant-attributable content ("participants noted," "members observed," "several expressed concern," individual named speakers in transcripts) and to ignore any staff-attributable language ("the staff reported," "the staff forecast"). This file is the primary source for minutes-transcript comparison analysis, as both document types are scored for the same set of meetings, enabling researchers to assess how well the published minutes represent the underlying transcript discussions.

## Unit of Observation

One row = one FOMC meeting document (identified by MEETING_DATE and SOURCE_TYPE). When both minutes and transcript exist for a meeting, they appear as two separate rows scored independently from each document's participant content.

## Variable Definitions

### Identifier Variables

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| MEETING_DATE | Date (ISO 8601) | YYYY-MM-DD | Date on which the FOMC meeting started. For multi-day meetings, this is the first day. Primary key together with SOURCE_TYPE. |
| SOURCE_TYPE | Categorical | `minutes`, `transcript` | Document type scored. `minutes` = published meeting minutes; uses quantifier language ("most," "several," "a few") to characterize participant views. `transcript` = verbatim transcript with individual speaker identification. The presence of both types for the same meeting enables minutes-transcript comparison analysis. |

---

### Scoring Conventions (apply to all dimension scores)

- **Scale**: 1–100 continuous integer. The scale is anchored at 50 (neutral midpoint). Scores are never exactly 0; the minimum is 1, reserved for the most extreme possible case.
- **Polarity**: Uniform across all dimensions — **higher = more of the named construct** without exception. See each dimension entry for the specific polarity statement.
- **Center-of-gravity principle**: Scores reflect the collective stance of participants, not individual outliers. If 15 participants hold moderate views and 2 hold extreme views, the score reflects the majority. DISSENT_INTENSITY captures the spread of views.
- **N/A**: Assigned when the topic is not discussed by any participant. Distinct from 50 (discussed but neutral/balanced).
- **UNC columns** (`{DIM}_UNC`): The uncertainty band (±points). In this file, the UNC value reflects the range of participant views (not solely scorer confidence): narrow band (3–5) = broad participant agreement; wide band (10–15) = dispersed or sharply divided participant views. `N/A` when the dimension score is `N/A`.
- **CONF columns** (`{DIM}_CONF`): Confidence tier based on quantity of textual evidence. `High` = many participants addressed the topic. `Moderate` = some discussion. `Low` = inferred from limited remarks. `N/A` when the dimension score is `N/A`.

---

### Tier 1: Core Economic Dimensions

Scored for every meeting. `N/A` used only when no participants discussed the topic at all.

---

**INFLATION_PRESSURE**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| INFLATION_PRESSURE | Integer | 1–100 or N/A | Participants' collective assessment of inflation pressure relative to the 2% PCE target. Higher = participants perceive MORE inflation pressure. Scores below 50 indicate perceived below-target or disinflationary conditions; 50 = at target; above 50 = above-target or accelerating. Note: "transitory" language does not reduce the score — the score reflects the current-period perception, not the forecast. Era anchors: ~15–20 (2009 deflation fears), ~38–42 (2013–2019 below-target period), ~50 (early 2018 "at target"), ~65–72 (2021 Q3–Q4 elevated), ~82–88 (2022 Q2–Q3 peak). |
| INFLATION_PRESSURE_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) reflecting dispersion of participant views on inflation pressure. |
| INFLATION_PRESSURE_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for INFLATION_PRESSURE based on volume of participant discussion. |

---

**OUTPUT_GAP**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| OUTPUT_GAP | Integer | 1–100 or N/A | Participants' collective assessment of the economy's position relative to potential output. Higher = economy operating MORE ABOVE potential (more overheating / less slack). Bright-line rule: "above potential" or "above trend" must produce score > 50; "below potential" or "slack remains" must produce score < 50. Era anchors: ~15–22 (GFC trough; COVID Q2 2020), ~35–42 (2010–2014 recovery), ~50–55 (2016–2019 near potential), ~57–63 (late 1990s boom; 2022). |
| OUTPUT_GAP_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) reflecting dispersion of participant views on the output gap. |
| OUTPUT_GAP_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for OUTPUT_GAP. |

---

**LABOR_TIGHTNESS**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| LABOR_TIGHTNESS | Integer | 1–100 or N/A | Participants' collective assessment of labor market tightness. Higher = TIGHTER labor market. Below 50 = slack or elevated unemployment; 50 = near NAIRU / full employment; above 50 = tight or overheated. The score reflects the level of tightness, not the rate of improvement. Era anchors: ~15–22 (2009, 2020 Q2), ~35–40 (2011–2014), ~50 (2016–2017), ~65–75 (1999–2000, 2022–2023). |
| LABOR_TIGHTNESS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) reflecting dispersion of participant views on labor market tightness. |
| LABOR_TIGHTNESS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for LABOR_TIGHTNESS. |

---

**CONSUMPTION_INVESTMENT**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| CONSUMPTION_INVESTMENT | Integer | 1–100 or N/A | Participants' collective assessment of consumer spending and business investment strength relative to trend. Higher = STRONGER demand. Below 50 = below trend or contracting; 50 = at trend; above 50 = above trend or robust. Era anchors: ~15–20 (2008 Q4–2009 Q1; 2020 Q2), ~35–42 (2011–2013 "moderate"), ~50–55 (2014–2019 "solid pace"), ~62–68 (2021 Q3–2022 Q1 surge). |
| CONSUMPTION_INVESTMENT_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) reflecting dispersion of participant views on spending and investment. |
| CONSUMPTION_INVESTMENT_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for CONSUMPTION_INVESTMENT. |

---

**FINANCIAL_TIGHTNESS**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| FINANCIAL_TIGHTNESS | Integer | 1–100 or N/A | Participants' collective assessment of overall financial conditions tightness. Higher = conditions are TIGHTER / more restrictive. Below 50 = loose or accommodative; 50 = neutral; above 50 = tighter than neutral. Scores conditions (credit availability, market spreads, liquidity), not the policy rate itself. Era anchors: ~10–20 (2005–2006 pre-crisis ease), ~45–55 (2017–2019 neutral), ~60–70 (2022 rate hike effects), ~85–95 (September 2008; March 2020 dash for cash). Note: this dimension is analogous to FINANCIAL_CONDITIONS in staff_scores_v4.csv but is scored from participant discussion rather than staff presentation. |
| FINANCIAL_TIGHTNESS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) reflecting dispersion of participant views on financial conditions. |
| FINANCIAL_TIGHTNESS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for FINANCIAL_TIGHTNESS. |

---

### Tier 1: Core Policy and Preference Dimensions

---

**HAWKISH_DOVISH_LEAN**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| HAWKISH_DOVISH_LEAN | Integer | 1–100 or N/A | The center of gravity of participant policy preferences at the time of the meeting. Higher = MORE HAWKISH (favoring tighter monetary policy). 50 = balanced or evenly split; below 50 = dovish lean (favoring accommodation, easing, or holding); above 50 = hawkish lean (favoring tightening, hiking, or signaling removal of accommodation). Scores reflect the current action combined with the implied forward lean; a meeting that hikes 25bp but signals patience going forward is scored lower than one where all participants want further hikes. Era anchors: ~2–5 (March 2020 emergency; March 2009), ~15–25 (QE era 2010–2012), ~40–50 (2014–2015 pre-liftoff), ~60–65 (December 2015 liftoff), ~70–75 (2017–2018 hiking cycle), ~80–85 (late 2022 75bp hikes). |
| HAWKISH_DOVISH_LEAN_UNC | Integer | 3–15 or N/A | Uncertainty band (±points). Wide values indicate divided participant views on the appropriate policy stance. |
| HAWKISH_DOVISH_LEAN_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for HAWKISH_DOVISH_LEAN. |

---

**DISSENT_INTENSITY**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| DISSENT_INTENSITY | Integer | 1–100 or N/A | The intensity and breadth of disagreement among participants. Higher = MORE or STRONGER dissent. Below 20 = near-consensus; 50 = notable disagreement; above 70 = significant division with multiple dissents or sharp disagreements. Captures both formal voting dissents and expressed reservations short of formal dissent. Formal voting dissents receive greater weight than reluctant support. Era anchors: ~10–15 (emergency unanimous meetings), ~25–35 (typical one-dissent meeting), ~40–50 (meetings with multiple reservations but consensus vote), ~55–65 (QE2 debates 2010–2011), ~70+ (three or more dissents, rare). |
| DISSENT_INTENSITY_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the DISSENT_INTENSITY score. |
| DISSENT_INTENSITY_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for DISSENT_INTENSITY. |

---

**FINANCIAL_STABILITY_EMPHASIS**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| FINANCIAL_STABILITY_EMPHASIS | Integer | 1–100 or N/A | The degree to which participants collectively devoted attention to financial stability and financial conditions. Higher = MORE emphasis on financial stability topics. Important: this dimension measures attention level, not the direction of concern. Whether conditions are described as very loose or very tight, extensive discussion of either produces a high score. Score of 1–10 = no mention; ~10–20 = brief passing references; ~40–60 = moderate discussion by several participants; ~80–95 = dominant topic that rivals economic assessment in time devoted. Era anchors: ~1–10 (1993–1996 typical), ~20–35 (2013–2019 typical), ~40–55 (2006–2007 pre-crisis), ~60–75 (2008 early crisis, 2020 recovery), ~80–95 (September 2008, March 2020). |
| FINANCIAL_STABILITY_EMPHASIS_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the FINANCIAL_STABILITY_EMPHASIS score. |
| FINANCIAL_STABILITY_EMPHASIS_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for FINANCIAL_STABILITY_EMPHASIS. |

---

**FORWARD_GUIDANCE_TONE**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| FORWARD_GUIDANCE_TONE | Integer | 1–100 or N/A | The directional tone of participants' forward-looking policy signals. Higher = MORE HAWKISH or tightening-oriented forward guidance. Score of 1–5 = strongest easing commitment (threshold-based or date-based guidance promising extended near-zero rates); 50 = neutral or purely data-dependent posture with no directional signal; ~76–90 = clear tightening signal with further hikes or balance sheet reduction communicated; ~91–100 = explicit commitment to aggressive further tightening. The score reflects the forward signal, not the current meeting's action. Era anchors: ~3–8 (2012–2013 Evans Rule / QE3 thresholds), ~8–15 (2014 taper), ~25–40 (2015 pre-liftoff), ~60–75 (2015–2018 hiking cycle), ~35–45 (2019 mid-cycle cuts), ~2–10 (2020 emergency), ~80–95 (2022 aggressive hiking). |
| FORWARD_GUIDANCE_TONE_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the FORWARD_GUIDANCE_TONE score. |
| FORWARD_GUIDANCE_TONE_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for FORWARD_GUIDANCE_TONE. |

---

**UNCERTAINTY_EXPRESSED**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| UNCERTAINTY_EXPRESSED | Integer | 1–100 or N/A | The degree to which participants collectively expressed uncertainty about the economic or policy outlook. Higher = MORE uncertainty voiced. Below 20 = high confidence / narrow forecast ranges; ~25–35 = standard caveats, "risks roughly balanced"; ~46–60 = elevated uncertainty with multiple participants emphasizing it; ~76–90 = deep or unusual uncertainty ("uncharted territory"); ~91–100 = Knightian uncertainty (distribution of outcomes itself unknown). Important: the scorer distinguishes genuine uncertainty from rhetorical hedging. "Considerable uncertainty" maps to 65–80; "some uncertainty" / "usual risks" maps to 25–40. Era anchors: ~10–20 (mid-2017 to mid-2018 stable expansion), ~25–35 (2013–2014, 2016), ~55–65 (2015–2016 China slowdown), ~70–80 (GFC unfolding fall 2008), ~85–95 (March 2009 trough; March 2020 emergency). |
| UNCERTAINTY_EXPRESSED_UNC | Integer | 3–15 or N/A | Uncertainty band (±points) around the UNCERTAINTY_EXPRESSED score. |
| UNCERTAINTY_EXPRESSED_CONF | Categorical | High / Moderate / Low / N/A | Confidence tier for UNCERTAINTY_EXPRESSED. |

---

### Tier 2: Optional / Supplementary Dimensions

These dimensions are scored only when two or more participants discuss the topic prominently. Single-column variables (no UNC or CONF columns). N/A is the common value. All share the polarity: higher = more of the named construct.

**Inflation Sub-Components**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| INFLATION_GOODS | Integer | 1–100 or N/A | Participants' assessment of goods price inflation. Higher = MORE goods price pressure. Score of 1 = falling goods prices; 50 = stable; 100 = surging goods inflation. |
| INFLATION_SERVICES | Integer | 1–100 or N/A | Participants' assessment of services price inflation. Higher = MORE services price pressure. Score of 1 = falling services prices; 50 = stable; 100 = surging services inflation. |
| INFLATION_HOUSING | Integer | 1–100 or N/A | Participants' assessment of housing/shelter inflation. Higher = MORE housing price or rent pressure. Score of 1 = declining rents/shelter costs; 50 = stable; 100 = surging housing inflation. |
| INFLATION_EXPECTATIONS | Integer | 1–100 or N/A | Participants' assessment of inflation expectations anchoring. Higher = MORE concern about expectations becoming unanchored or drifting upward. Score of 1 = well-anchored below target; 50 = anchored at target; 100 = unanchored or rising materially above target. |

**Financial Sub-Components**

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| CREDIT_STRESS | Integer | 1–100 or N/A | Participants' assessment of credit market stress. Higher = MORE credit stress (wider spreads, reduced availability). Score of 1 = extremely compressed spreads, underpriced risk; 50 = normal credit conditions; 100 = severely widened spreads, credit rationing, lending freeze. Analogous to CREDIT_SPREADS in staff_scores_v4.csv. |
| EQUITY_STRESS | Integer | 1–100 or N/A | Participants' assessment of equity market stress or concern. Higher = MORE equity stress or concern. Score of 1 = extreme overvaluation concern (bubble); 50 = roughly fair valued, no particular concern; 100 = extreme undervaluation or crash concern (fire-sale prices, panic). Note: the score reflects participants' stated concern level, not price direction alone. |
| BANKING_STRESS | Integer | 1–100 or N/A | Participants' assessment of banking system stress. Higher = MORE banking system stress or impairment. Score of 1 = excessive risk-taking concern; 50 = sound and well-capitalized; 100 = severe stress (failures, capital shortfalls, systemic risk). "Well-capitalized" / "sound" language maps below 50. |
| TREASURY_STRESS | Integer | 1–100 or N/A | Participants' assessment of Treasury market functioning. Higher = MORE market dysfunction. Score of 1 = exceptionally smooth functioning; 50 = normal; 100 = severe dysfunction (liquidity failure, auction problems). Yield movements from policy expectations alone are not dysfunction. |
| DOLLAR_CONCERN | Integer | 1–100 or N/A | Participants' concern about dollar strength. Higher = MORE concern about dollar STRENGTH or appreciation. Score of 1 = extreme weakness concern; 50 = stable dollar, no directional concern; 100 = extreme strength concern. Note the asymmetry: this dimension scores concern about strength, not concern about weakness. |
| PRODUCTIVITY | Integer | 1–100 or N/A | Participants' assessment of productivity growth. Higher = MORE productivity growth perceived. Score of 1 = deteriorating productivity; 50 = at historical trend; 100 = exceptional gains. Scored only when participants specifically discuss productivity in the meeting. |

---

### Quality and Anomaly Variables

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| ANOMALY_FLAG | Categorical | `No`, `Yes` | Indicates whether the scoring LLM identified any anomaly or unusual characteristic requiring human review. `No` = standard scoring proceeded without issues. `Yes` = see ANOMALY_NOTE for explanation. Common triggers: emergency meetings with abbreviated discussion, meetings dominated by one or two speakers (noted in ANOMALY_NOTE rather than distorting the center-of-gravity score), unsegmented pre-2009 minutes requiring manual content attribution. |
| ANOMALY_NOTE | String | Free text or empty | Human-readable explanation of the anomaly. Empty when ANOMALY_FLAG = `No`. |

---

## Notes

1. **Minutes vs. transcript scoring independence**: Each row is scored independently from its source document. The LLM does not see the paired document when scoring. This independence is by design — systematic differences between the two scores for the same meeting quantify information compression or editorial framing in the published minutes. Researchers should not average the two rows; they should treat them as distinct observations of distinct representations of the same meeting.

2. **Center of gravity, not outliers**: All scores except DISSENT_INTENSITY are calibrated to the central tendency of participant views, not to the most hawkish or most dovish participant. Outlier views are captured indirectly through DISSENT_INTENSITY and ANOMALY_NOTE.

3. **UNC interpretation differs from staff scores**: In staff_scores_v4.csv, the UNC columns reflect scorer confidence given text clarity. In this file, the UNC columns reflect the range of participant views. A narrow UNC means participants largely agreed; a wide UNC means participant views were dispersed.

4. **Tier 2 dimensions have no UNC/CONF columns**: The ten optional supplementary dimensions (INFLATION_GOODS through PRODUCTIVITY) are single-column point estimates without associated uncertainty or confidence indicators. Treat with lower precision.

5. **Pre-2009 minutes structure**: Minutes before approximately 2009 did not cleanly separate participant discussion from staff presentations. The rubric instructs the scorer to include only participant-attributable language ("members noted," "participants observed"). Pre-2009 scores may be noisier.

6. **FINANCIAL_STABILITY_EMPHASIS direction neutrality**: This dimension measures attention, not condition direction. A meeting where participants extensively discuss how loose conditions are and a meeting where participants extensively discuss how tight conditions are would produce similar FINANCIAL_STABILITY_EMPHASIS scores. The direction of concern is captured in FINANCIAL_TIGHTNESS.

7. **Relationship to staff_scores_v4.csv**: The two files are complementary but not directly comparable. Staff and participant views are scored independently and may diverge, particularly on the inflation, output gap, and financial conditions dimensions. The divergence itself is analytically meaningful. See feedback_cross_method_lessons.md for documented patterns of convergence and divergence.
