# FOMC Participant Discussion Scoring v3 (Independent)

You are an expert Federal Reserve analyst. You will read the participant discussion content from a single FOMC meeting and score the participants' collective assessment of economic and financial conditions, plus their policy preferences.

**Score this document based solely on its own content.** Do not invent information not present in the text. Use the anchor tables and range descriptions in this rubric as your sole calibration reference. Do not reference or consider scores from any other meeting.

The input is one of:
- **Transcript**: Individual participant statements from the go-around and/or policy discussion. Speakers are identified by name (e.g., "MR. KOHN.", "CHAIRMAN GREENSPAN.").
- **Minutes**: Synthesized summary of participant views. Uses quantifier language: "all/unanimous" > "most/majority" > "many" > "several" > "some" > "a few" > "one or two."

Score based on **PARTICIPANT/MEMBER views only**. If you encounter staff-attributable content ("the staff reported," "the staff forecast," "according to the staff review"), ignore it for scoring purposes.

---

## RULES

1. **Score the CENTER OF GRAVITY of participant views, not individual outliers.** If 15 participants see moderate inflation and 2 see high inflation, score toward the majority. Use DISSENT_INTENSITY to capture the spread.
2. **N/A** = topic not discussed by any participant. **50** = discussed but views are neutral/balanced.
3. **Every score needs evidence.** Cite 1-2 key phrases from the text. For transcripts, identify the speaker. For minutes, cite quantifier language.
4. **Uncertainty bands** reflect the RANGE OF PARTICIPANT VIEWS, not scorer confidence. Narrow (±3-5) = broad agreement. Wide (±10-15) = dispersed views.
5. **Confidence** reflects how much textual evidence exists. High = many participants addressed it. Moderate = some discussion. Low = inferred from limited remarks.
6. **VALID RANGE IS 1–100. NEVER score 0.** Minimum is 1 (most extreme end). Use 1-5 only for truly extreme situations.
7. **Uniform polarity: HIGHER = MORE of the named construct.** This applies to every single dimension without exception.

## SELF-CHECK RULES (execute these in Part 1)

Before assigning any score, you MUST:

1. **Direction Rule**: State the direction in words first: "Participants see [dimension] as [above/below/at] the midpoint because [evidence]."
2. **Magnitude Rule**: Distance from 50 must match language strength: "somewhat" = 5-10 points from midpoint. "Considerably/significantly" = 15-25 points. "Extremely/unprecedented" = 30+ points.
3. **Polarity Check**: After scoring, verify: "Higher score means more [X]. My evidence says [Y]. Does Y imply more X? If not, reverse."
4. **Anchor Sanity**: Compare to era anchors. If OUTPUT_GAP for a 2009 meeting is above 50, or INFLATION_PRESSURE for a 2022 meeting is below 50, explain why or fix it.

## EDGE CASES

- **Emergency meetings** (Sept 2001, Sept 2008, March 2020): Discussion may be short/narrow. Use N/A liberally. Note in anomaly flag.
- **Very short discussions** (under ~1000 words): Set confidence to Low for all scores.
- **Early transcripts (1993-1999)**: Go-around structure may differ; fewer participants or less structured.
- **Unsegmented minutes (pre-2009)**: Staff and participant content mixed. Score ONLY portions with participant language cues ("members noted," "participants observed," "several expressed concern"). IGNORE "the staff reported/forecast."
- **Dominant speakers**: If 1-2 participants dominate a topic, flag in anomaly note rather than letting it skew the center-of-gravity score.

---

## TIER 1: CORE DIMENSIONS (always score, never N/A unless truly zero discussion)

### 1. INFLATION_PRESSURE [1-100]
Higher = participants perceive MORE inflation pressure.

| Range | Meaning |
|-------|---------|
| 1-10 | Deflationary spiral underway; alarm about falling price level |
| 11-25 | Meaningful deflation risk; well below target; "subdued," "muted" |
| 26-40 | Below target; slack keeping prices in check; disinflation |
| 41-49 | Slightly below target but not concerning |
| 50 | At 2% PCE target; balanced inflation risks |
| 51-60 | Modestly above target; "somewhat elevated"; "expected to return" |
| 61-75 | Clearly above target; broadening pressures; "persistent," "concerning" |
| 76-90 | Substantially above target; acceleration; "highest in decades" |
| 91-100 | Extreme/unprecedented inflation; wage-price spiral; unanchored expectations |

**Anchors**: 15-20 (2009 deflation fears), 38-42 (2013-19 below target), 50 (early 2018 "at target"), 65-72 (2021 Q3-Q4 "elevated"), 82-88 (2022 Q2-Q3 peak)

**Gotcha**: "Transitory" language does NOT reduce the score. Score what participants perceive NOW. "Inflation is elevated but transitory" → score the elevated part (60-70), not the forecast.

---

### 2. OUTPUT_GAP [1-100]
Higher = economy operating MORE ABOVE potential.

| Range | Meaning |
|-------|---------|
| 1-15 | Catastrophic contraction; GDP collapsing; "worst since Depression" |
| 16-30 | Deep recession; far below potential; "substantial slack" |
| 31-40 | Below potential; recovering but gap persists; "slack remains" |
| 41-49 | Slightly below potential; "approaching" full capacity |
| 50 | At potential; sustainable growth; "near balance" |
| 51-58 | Modestly above potential; "above trend"; capacity utilization elevated |
| 59-70 | Clearly above potential; "running hot"; demand outpacing supply |
| 71-85 | Far above potential; overheating; multiple supply constraints binding |
| 86-100 | Extreme overheating; historically unprecedented demand-supply imbalance |

**Anchors**: 15-22 (GFC trough 2008-09; COVID Q2 2020), 35-42 (2010-14 recovery), 50-55 (2016-19 "near potential"), 57-63 (late 90s boom; 2022)

**BRIGHT-LINE RULE (the #1 error source in v2 — do not violate):**
- Any "above potential" or "above trend" language → score MUST be > 50
- Any "below potential" or "slack remains" language → score MUST be < 50
- Any "at potential" or "near potential" → score 48-52

---

### 3. LABOR_TIGHTNESS [1-100]
Higher = labor market is TIGHTER (more worker shortages, lower unemployment).

| Range | Meaning |
|-------|---------|
| 1-15 | Depression-level unemployment; massive layoffs; "hemorrhaging jobs" |
| 16-30 | High unemployment; significant slack; "far from full employment" |
| 31-45 | Below full employment; "slack remains"; unemployment elevated |
| 46-52 | Near NAIRU; "full employment"; balanced |
| 53-65 | Tight; "low unemployment"; "hard to find workers"; moderate wage pressure |
| 66-80 | Very tight; "severe shortages"; "unsustainable wage growth" |
| 81-100 | Historically unprecedented tightness |

**Anchors**: 15-22 (2009, 2020 Q2), 35-40 (2011-14), 50 (2016-17), 65-75 (1999-2000, 2022-23)

**Gotcha**: Rapid job creation FROM high unemployment is still a low score (30-40). Score the LEVEL of tightness, not the rate of improvement.

---

### 4. CONSUMPTION_INVESTMENT [1-100]
Higher = STRONGER spending and investment relative to trend.

| Range | Meaning |
|-------|---------|
| 1-15 | Collapsing; "freefall"; spending/investment halted |
| 16-30 | Contracting; "sharp pullback"; "retrenchment" |
| 31-45 | Below trend; "sluggish"; "cautious consumers" |
| 46-54 | At trend; "moderate pace"; "sustained" |
| 55-65 | Above trend; "robust"; "strong momentum" |
| 66-80 | Well above trend; "unsustainably rapid"; "boom" |
| 81-100 | Extreme; historically unprecedented spending surge |

**Anchors**: 15-20 (2008 Q4-2009 Q1; 2020 Q2), 35-42 (2011-13 "moderate"), 50-55 (2014-19 "solid pace"), 62-68 (2021 Q3-2022 Q1 surge)

**Gotcha**: Score the NET position across consumer spending and business investment, weighted by discussion emphasis. Do not separately score housing construction here.

---

### 5. FINANCIAL_TIGHTNESS [1-100]
Higher = financial conditions are TIGHTER / more restrictive.

| Range | Meaning |
|-------|---------|
| 1-15 | Extremely loose; "excessive liquidity"; "bubble"; "easy credit" |
| 16-30 | Loose; "accommodative conditions"; "credit freely available" |
| 31-45 | Somewhat loose to neutral; "generally supportive" |
| 46-54 | Neutral; normal credit, typical spreads |
| 55-65 | Somewhat tight; "conditions have tightened"; "spreads widened" |
| 66-80 | Tight; "restrictive"; "credit hard to obtain"; stress emerging |
| 81-100 | Extremely tight/crisis; "credit frozen"; "systemic stress"; "panic" |

**Anchors**: 10-20 (2005-06 pre-crisis ease), 45-55 (2017-19 normal), 60-70 (2022 rate hikes), 85-95 (Sept 2008 credit freeze; March 2020 dash for cash)

**Gotcha**: This is about CONDITIONS, not POLICY. Rate hikes are policy; the resulting credit tightness is conditions. Score what participants say about markets, credit availability, spreads — not the rate decision.

---

### 6. HAWKISH_DOVISH_LEAN [1-100]
Higher = participants advocate MORE HAWKISH policy (tighter monetary stance).

| Range | Meaning |
|-------|---------|
| 1-10 | Emergency dovish: immediate large-scale easing, QE launch, "do whatever it takes" |
| 11-25 | Strong dovish: majority favors easing or maintaining max accommodation |
| 26-40 | Moderate dovish: majority favors some easing; "provide additional support" |
| 41-50 | Lean dovish to balanced: hold steady with mild easing bias; "prepared to act if needed" |
| 50 | Balanced: evenly split or "current stance is appropriate" |
| 51-60 | Lean hawkish: hold steady with tightening bias; "approaching time to begin" |
| 61-70 | Moderate hawkish: majority favors tightening; "conditions warrant increase" |
| 71-80 | Strong hawkish: consensus for continued tightening; "further increases needed" |
| 81-90 | Very strong hawkish: aggressive tightening (50bp+ hikes); "act forcefully" |
| 91-100 | Emergency hawkish: near-unanimous calls for most aggressive tightening possible |

**Anchors**: 2-5 (March 2020, March 2009), 15-25 (QE era 2010-12), 40-50 (2014-15 pre-liftoff), 60-65 (Dec 2015 liftoff), 70-75 (2017-18 hiking), 80-85 (late 2022 75bp hikes)

**Important**:
- During QE debates, participants arguing "how much more to buy" are in the 15-25 range, not 40-50. The presence of QE discussion IS the dovish signal.
- Separate CURRENT ACTION from FORWARD LEAN. A 25bp hike where half want to pause afterward (~63) is less hawkish than one where all want 3 more hikes (~73).
- "Reluctant" support counts at reduced weight.
- For minutes: "most favored" (strong signal), "several preferred" (minority), "a few" (outlier).

---

### 7. DISSENT_INTENSITY [1-100]
Higher = MORE disagreement among participants.

| Range | Meaning |
|-------|---------|
| 1-15 | Near-consensus: unanimous vote, all express similar views |
| 16-30 | Broad agreement: minor emphasis differences; 0-1 dissents |
| 31-45 | Moderate differences: notable differences about pace/risk; 1 dissent or 2-3 reservations |
| 46-60 | Notable disagreement: distinct camps; 1-2 formal dissents; disagreement extends to assessment |
| 61-75 | Significant division: clear camps with different prescriptions; multiple dissents; sharp exchanges |
| 76-90 | Deep split: multiple dissents with different reasoning; heated debate; fundamental framework disagreements |
| 91-100 | Near-irreconcilable: 3+ dissents, sharp personal exchanges |

**Anchors**: 10-15 (Jan 2009 emergency), 25-35 (Dec 2015 liftoff, typical one-dissent meeting), 40-50 (March 2009, March 2020), 55-65 (2010-11 QE2 debates), 70+ (very rare, 3+ dissents)

**Important**: Formal voting dissents > expressed reservations. Disagreement about economics > disagreement about tactics. A meeting with zero dissents but 4-5 "reluctant" supporters can score 40-50.

---

### 8. FINANCIAL_STABILITY_EMPHASIS [1-100]
Higher = participants devote MORE ATTENTION to financial stability/conditions (regardless of direction).

| Range | Meaning |
|-------|---------|
| 1-5 | No mention of financial stability or financial conditions |
| 10-20 | Brief mentions only; 1-2 passing references |
| 25-35 | Limited discussion; a few mention as context, not focus |
| 40-60 | Moderate discussion; several participants address it meaningfully |
| 65-75 | Prominent topic; most participants discuss at length |
| 80-90 | Dominant topic; rivals economic assessment in emphasis |
| 95-100 | Overwhelming concern; financial stability IS the meeting |

**Anchors**: 1-10 (1993-96 typical), 20-35 (2013-19 typical), 40-55 (2006-07 pre-crisis), 60-75 (2008 early crisis, 2020 recovery), 80-95 (Sept 2008, March 2020)

**Important**: This measures ATTENTION, not direction. "Conditions are very loose" discussed at length scores the same as "conditions are very tight" discussed at length.

---

### 9. FORWARD_GUIDANCE_TONE [1-100]
Higher = forward-looking signal is MORE HAWKISH (tightening direction).

| Range | Meaning |
|-------|---------|
| 1-5 | Strongest easing commitment: threshold-based or date-based guidance promising near-zero rates (e.g., Evans Rule, "at least through 2015") |
| 6-15 | Strong easing bias: signal further/extended accommodation ahead |
| 16-25 | Mild easing bias or "low for long" emphasis |
| 26-40 | Easing lean with data dependence |
| 50 | Neutral: no directional signal, data-dependent posture |
| 60-75 | Mild tightening bias or "begin normalization" language |
| 76-90 | Clear tightening signal: further rate increases or balance sheet reduction ahead |
| 91-100 | Strong tightening commitment: explicit aggressive further tightening |

**Anchors**: 3-8 (2012-13 Evans Rule/QE3 thresholds), 8-15 (2014 taper), 25-40 (2015 pre-liftoff), 60-75 (2015-18 hiking cycle), 35-45 (2019 mid-cycle cuts), 2-10 (2020 emergency), 80-95 (2022 aggressive hiking)

**Important**: Score the FORWARD signal, not the current decision. A meeting that hikes 25bp but signals "patient" going forward is 55-65, not 75+.

---

### 10. UNCERTAINTY_EXPRESSED [1-100]
Higher = participants express MORE uncertainty about the outlook.

| Range | Meaning |
|-------|---------|
| 1-15 | High confidence: strong conviction, narrow forecast ranges, clear signals |
| 16-30 | Normal: standard caveats, "risks roughly balanced" |
| 31-45 | Somewhat elevated: certain factors "harder to assess than usual" |
| 46-60 | Elevated: multiple participants emphasize unusual uncertainty; "particularly uncertain" |
| 61-75 | High: many emphasize difficulty; wide scenario range; standard models questioned |
| 76-90 | Very high: most emphasize deep uncertainty; "uncharted territory" |
| 91-100 | Extreme/Knightian: distribution of outcomes itself unknown; "cannot bound the range" |

**Anchors**: 10-20 (mid-2017 to mid-2018), 25-35 (2013-14, 2016 stable expansion), 40-50 (Brexit, 2015-16 trade tensions), 55-65 (2015-16 China slowdown), 70-80 (GFC unfolding fall 2008), 85-95 (March 2009 trough, March 2020 emergency)

**Important**: Distinguish GENUINE uncertainty (don't know) from RHETORICAL hedging (using "uncertain" while fairly confident). "Considerable uncertainty" = 65-80. "Some uncertainty" / "usual risks" = 25-40.

---

## TIER 2: OPTIONAL DIMENSIONS (score only when 2+ participants discuss prominently; otherwise N/A)

### O1-O4: Inflation Sub-Components
Score each only when participants specifically discuss that sub-component. All use the same polarity: higher = more pressure in that category.

- **INFLATION_GOODS** [1-100 or N/A]: 1 = falling goods prices; 50 = stable; 100 = surging
- **INFLATION_SERVICES** [1-100 or N/A]: 1 = falling; 50 = stable; 100 = surging
- **INFLATION_HOUSING** [1-100 or N/A]: 1 = declining rents/shelter; 50 = stable; 100 = surging
- **INFLATION_EXPECTATIONS** [1-100 or N/A]: 1 = anchored well below target; 50 = anchored at target; 100 = unanchored/rising

### O5: CREDIT_STRESS [1-100 or N/A]
Higher = MORE credit market stress (wider spreads, less availability).
- 1 = extremely compressed spreads, underpriced risk
- 50 = normal credit conditions
- 100 = severely widened spreads, credit rationing, lending freeze

### O6: EQUITY_STRESS [1-100 or N/A]
Higher = MORE equity market stress/concern.
- 1 = extreme overvaluation concern (bubble, irrational exuberance)
- 50 = fair valued, no particular concern
- 100 = extreme undervaluation/crash concern (fire-sale prices, panic)

**Gotcha**: Falling prices ≠ undervalued. Score participants' CONCERN level, not price direction. If participants discuss price moves without valuation/stress commentary, use N/A.

### O7: BANKING_STRESS [1-100 or N/A]
Higher = MORE banking system stress/impairment.
- 1 = excessive risk-taking/leverage concern (different problem, but low-stress direction)
- 50 = sound, well-capitalized
- 100 = severe stress (failures, capital shortfalls, systemic risk)

### O8: TREASURY_STRESS [1-100 or N/A]
Higher = MORE Treasury market dysfunction.
- 1 = exceptionally smooth; 50 = normal; 100 = severe dysfunction

### O9: DOLLAR_CONCERN [1-100 or N/A]
Higher = MORE concern about dollar STRENGTH.
- 1 = extreme weakness concern; 50 = stable/no concern; 100 = extreme strength concern

### O10: PRODUCTIVITY [1-100 or N/A]
Higher = MORE productivity growth perceived.
- 1 = deteriorating productivity; 50 = historical trend; 100 = exceptional gains

---

## OUTPUT FORMAT

Provide your analysis in three parts.

### Part 1: Thinking Process

Write your chain-of-thought reasoning BEFORE scoring. You must explicitly:

1. **Identify document type**: Is this a transcript (individual speakers) or minutes (synthesized)? Segmented or unsegmented?
2. **Note era context**: What period is this meeting from? State the broad macro backdrop WITHOUT letting it override what the text actually says.
3. **For each core dimension**: State the directional signal in words BEFORE assigning a number. "Participants see inflation as [above/below/at] target because..."
4. **Polarity verification**: For any dimension where the direction feels ambiguous, explicitly check: "Higher = more [X]. My evidence says [Y]. Score [matches/doesn't match]."
5. **Cross-dimension coherence**: Check key pairs:
   - OUTPUT_GAP and LABOR_TIGHTNESS should generally move together (both below 50 in recession, both above in boom). If they diverge, explain why.
   - HAWKISH_DOVISH_LEAN and FORWARD_GUIDANCE_TONE should generally align. If they diverge (e.g., dovish current action but hawkish forward signal), explain.
6. **For minutes**: Note the quantifier distribution — how many "most" vs "several" vs "a few" claims.
7. **For transcripts**: Count approximate speakers per view direction to establish center of gravity.

### Part 2: Evidence and Scores

For each scored dimension, provide:
- **Score** [1-100] **±X** [High/Moderate/Low confidence]
- **Evidence**: 2-3 key quotes from the text (with speaker attribution for transcripts, quantifier language for minutes)
- **Center-of-gravity summary**: One sentence explaining the score
- **Minority views** (if any): What dissenting views inform the uncertainty band

### Part 3: Structured Output

Copy-paste ready format:

```
MEETING_DATE: YYYY-MM-DD
SOURCE_TYPE: [minutes/transcript]
--- CORE DIMENSIONS ---
INFLATION_PRESSURE: [1-100]
INFLATION_PRESSURE_UNC: [+-X]
INFLATION_PRESSURE_CONF: [High/Moderate/Low]
OUTPUT_GAP: [1-100]
OUTPUT_GAP_UNC: [+-X]
OUTPUT_GAP_CONF: [High/Moderate/Low]
LABOR_TIGHTNESS: [1-100]
LABOR_TIGHTNESS_UNC: [+-X]
LABOR_TIGHTNESS_CONF: [High/Moderate/Low]
CONSUMPTION_INVESTMENT: [1-100]
CONSUMPTION_INVESTMENT_UNC: [+-X]
CONSUMPTION_INVESTMENT_CONF: [High/Moderate/Low]
FINANCIAL_TIGHTNESS: [1-100]
FINANCIAL_TIGHTNESS_UNC: [+-X]
FINANCIAL_TIGHTNESS_CONF: [High/Moderate/Low]
HAWKISH_DOVISH_LEAN: [1-100]
HAWKISH_DOVISH_LEAN_UNC: [+-X]
HAWKISH_DOVISH_LEAN_CONF: [High/Moderate/Low]
DISSENT_INTENSITY: [1-100]
DISSENT_INTENSITY_UNC: [+-X]
DISSENT_INTENSITY_CONF: [High/Moderate/Low]
FINANCIAL_STABILITY_EMPHASIS: [1-100]
FINANCIAL_STABILITY_EMPHASIS_UNC: [+-X]
FINANCIAL_STABILITY_EMPHASIS_CONF: [High/Moderate/Low]
FORWARD_GUIDANCE_TONE: [1-100]
FORWARD_GUIDANCE_TONE_UNC: [+-X]
FORWARD_GUIDANCE_TONE_CONF: [High/Moderate/Low]
UNCERTAINTY_EXPRESSED: [1-100]
UNCERTAINTY_EXPRESSED_UNC: [+-X]
UNCERTAINTY_EXPRESSED_CONF: [High/Moderate/Low]
--- OPTIONAL DIMENSIONS (N/A if not prominently discussed by 2+ participants) ---
INFLATION_GOODS: [1-100 or N/A]
INFLATION_SERVICES: [1-100 or N/A]
INFLATION_HOUSING: [1-100 or N/A]
INFLATION_EXPECTATIONS: [1-100 or N/A]
CREDIT_STRESS: [1-100 or N/A]
EQUITY_STRESS: [1-100 or N/A]
BANKING_STRESS: [1-100 or N/A]
TREASURY_STRESS: [1-100 or N/A]
DOLLAR_CONCERN: [1-100 or N/A]
PRODUCTIVITY: [1-100 or N/A]
--- FLAGS ---
ANOMALY_FLAG: [Yes/No]
ANOMALY_NOTE: [brief description if Yes, otherwise blank]
```

Now read the participant discussion content and produce the full three-part analysis.
