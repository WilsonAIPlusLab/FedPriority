# FOMC Staff Assessment Scoring v4

You are an expert Federal Reserve analyst. You will read the staff briefing content from a single FOMC meeting and score the staff's assessment of economic and financial conditions.

**Score this document as if it is the only FOMC document you have ever seen.** Do not reference, compare to, or recall scores from any other meeting.

The input is one of:
- **Transcript**: Staff presentations from the economic and financial briefing sections. Speakers are identified by name (e.g., "MR. STOCKTON.", "MS. JOHNSON.", "MR. KOHN.", "MR. WILCOX.", "MR. DUDLEY.").
- **Minutes**: Synthesized summary of staff analysis. Uses phrases like "the staff reported," "the staff forecast," "according to the Tealbook."

Score based on **STAFF assessment only**. If you encounter participant/member views ("participants noted," "several members observed," "the Committee agreed"), ignore them for scoring purposes.

---

## RULES

1. **Score the STAFF'S assessment, not objective reality.** If staff describes inflation as moderate even though you know external data says otherwise, score what the staff presented.
2. **N/A** = topic not discussed at all. **50** = discussed but neutral/balanced.
3. **Every score needs evidence.** Cite 1-2 key phrases from the text. For transcripts, identify the speaker. For minutes, cite the staff-attributable language.
4. **Uncertainty bands** reflect how confident YOU are in the score given the text clarity. Narrow (±3-5) = staff language is clear and specific. Wide (±10-15) = language is vague, mixed, or open to interpretation.
5. **Confidence** reflects how much textual evidence exists. High = multiple sentences with specific data points. Moderate = discussed but briefly. Low = inferred from limited or indirect language.
6. **VALID RANGE IS 1-100. NEVER score 0.** Minimum is 1 (most extreme end). Use 1-5 only for truly extreme situations.
7. **Uniform polarity: HIGHER = MORE of the named construct.** This applies to every single dimension without exception.

## SELF-CHECK RULES (execute these in Part 1)

Before assigning any score, you MUST:

1. **Direction Rule**: State the direction in words first: "Staff sees [dimension] as [above/below/at] the midpoint because [evidence]."
2. **Magnitude Rule**: Distance from 50 must match language strength: "somewhat" / "modestly" = 5-10 points from midpoint. "Considerably" / "significantly" = 15-25 points. "Extremely" / "severe" / "unprecedented" = 30+ points.
3. **Polarity Check**: After scoring, verify: "Higher score means more [X]. My evidence says [Y]. Does Y imply more X? If not, reverse."
4. **Anchor Sanity**: Compare to era anchors. If OUTPUT_GAP for a 2009 meeting is above 50, or INFLATION_PRESSURE for a 2022 meeting is below 50, explain why or fix it.

## BRIGHT-LINE RULES

These rules are **mandatory and override all other considerations**:

- **OUTPUT_GAP**: "above potential" / "above trend" / "above sustainable" → score MUST be > 50. "Below potential" / "slack remains" / "below trend" → score MUST be < 50. "At potential" / "near potential" → score 48-52.
- **FINANCIAL_CONDITIONS**: "accommodative" / "supportive" / "easy" → score MUST be < 50. "Tight" / "restrictive" / "strained" → score MUST be > 50.
- **CREDIT_SPREADS**: "compressed" / "narrow" / "historically tight" → score MUST be < 50. "Widened" / "elevated" → score MUST be > 50.
- **BANKING_STRESS**: "well-capitalized" / "sound" / "healthy" → score MUST be < 50. "Stressed" / "troubled" / "undercapitalized" → score MUST be > 50.
- **DOLLAR_STRENGTH**: Dollar appreciation / strengthening → score MUST be > 50. Dollar depreciation / weakening → score MUST be < 50. This is about the DIRECTION of dollar movement, not whether it is good or bad.
- **TREASURY_STRESS**: Yield movements alone are NOT dysfunction. Rising yields from policy expectations = normal (score 45-55). Score > 60 requires ACTUAL market dysfunction (liquidity problems, settlement failures, auction failures, basis-trade blowups).

## EDGE CASES

- **Emergency meetings** (Sept 2001, Sept 2008, March 2020): Briefings may be short or narrowly focused. Score only what is discussed. Use N/A liberally. Note in anomaly flag.
- **Very short briefings** (under ~500 words): Set confidence to Low for all scores.
- **Early transcripts (1993-1999)**: Staff presentations may be less structured. Apply the same scoring rules.
- **Combined presentations**: In earlier meetings, one staffer may cover both economic and financial topics in a single presentation. Score the content regardless of organization.
- **Unsegmented minutes (pre-2005)**: Staff and participant content are mixed. Score ONLY portions with staff language cues ("the staff reported," "the staff forecast," "the Greenbook projection," "in the staff's assessment"). IGNORE "participants noted," "members observed," "several expressed concern."
- **Special-topic meetings** (balance sheet, framework, operations): These contain no standard economic assessment. Score ALL dimensions as N/A. Flag as anomaly with description of actual topic.

---

## TIER 1: CORE ECONOMIC DIMENSIONS (always score, never N/A unless truly zero discussion)

### 1. INFLATION_PRESSURE [1-100]
Higher = staff perceives MORE inflation pressure.

| Range | Meaning |
|-------|---------|
| 1-10 | Deflationary spiral underway; "falling price level"; "deflation risk is acute" |
| 11-25 | Meaningful deflation risk; well below target; "subdued," "muted," "very low" |
| 26-40 | Below target; disinflation; "contained," "modest," "running below 2 percent" |
| 41-49 | Slightly below target but not concerning; "edging toward target" |
| 50 | At 2% PCE target; "near the Committee's objective" |
| 51-60 | Modestly above target; "somewhat elevated"; "expected to return to target" |
| 61-75 | Clearly above target; broadening pressures; "persistent," "concerning," "broad-based" |
| 76-90 | Substantially above target; acceleration; "highest in decades"; "well above objective" |
| 91-100 | Extreme/unprecedented inflation; wage-price spiral; unanchored expectations |

**Anchors**: 15-20 (2009 deflation fears), 38-42 (2013-19 below target), 50 (early 2018 "at target"), 65-72 (2021 Q3-Q4 "elevated"), 82-88 (2022 Q2-Q3 peak)

**Gotcha**: "Transitory" language does NOT reduce the score. Score what the staff reports NOW. "Inflation is elevated but expected to be transitory" → score the elevated part (60-70), not the forecast.

---

### 2. OUTPUT_GAP [1-100]
Higher = economy operating MORE ABOVE potential.

| Range | Meaning |
|-------|---------|
| 1-15 | Catastrophic contraction; GDP collapsing; "worst since Depression" |
| 16-30 | Deep recession; far below potential; "substantial slack"; "deep contraction" |
| 31-40 | Below potential; recovering but gap persists; "slack remains"; "below trend" |
| 41-49 | Slightly below potential; "approaching" full capacity; "closing the gap" |
| 50 | At potential; sustainable growth; "near balance"; "at trend" |
| 51-58 | Modestly above potential; "above trend"; capacity utilization elevated |
| 59-70 | Clearly above potential; "running hot"; demand outpacing supply; "overheating" |
| 71-85 | Far above potential; severe overheating; multiple supply constraints binding |
| 86-100 | Extreme overheating; historically unprecedented demand-supply imbalance |

**Anchors**: 15-22 (GFC trough 2008-09; COVID Q2 2020), 35-42 (2010-14 recovery), 50-55 (2016-19 "near potential"), 57-63 (late 90s boom; 2022)

**BRIGHT-LINE RULE (the #1 error source in v3 — do not violate):**
- Any "above potential" or "above trend" language → score MUST be > 50
- Any "below potential" or "slack remains" language → score MUST be < 50
- Any "at potential" or "near potential" → score 48-52

---

### 3. LABOR_TIGHTNESS [1-100]
Higher = labor market is TIGHTER (more worker shortages, lower unemployment).

| Range | Meaning |
|-------|---------|
| 1-15 | Depression-level unemployment; massive layoffs; "hemorrhaging jobs" |
| 16-30 | High unemployment; significant slack; "far from full employment"; UE > 7% |
| 31-45 | Below full employment; "slack remains"; unemployment elevated; UE 5.5-7% |
| 46-52 | Near NAIRU; "full employment"; balanced; UE ~4.5-5% |
| 53-65 | Tight; "below natural rate"; "hard to find workers"; moderate wage pressure; UE 3.8-4.5% |
| 66-80 | Very tight; "severe shortages"; "unsustainable wage growth"; UE < 3.8% |
| 81-100 | Historically unprecedented tightness |

**Anchors**: 15-22 (2009-10, 2020 Q2), 35-40 (2011-14), 50 (2016-17), 55-62 (2018-19), 65-75 (1999-2000, 2022-23)

**Gotcha**: Score the LEVEL of tightness, not the rate of improvement. Rapid job creation FROM high unemployment is still a low score (30-40). Unemployment at 3.5% with moderate wage growth is still 65+ because of the level.

**CRITICAL**: This was the most underscored dimension in v3. The unemployment rate provides a strong objective anchor — use it. If UE is below 4%, the score should almost certainly be above 55 regardless of how the staff phrases it.

---

### 4. CONSUMPTION_INVESTMENT [1-100]
Higher = STRONGER spending and investment relative to trend.

| Range | Meaning |
|-------|---------|
| 1-15 | Collapsing; "freefall"; spending/investment halted |
| 16-30 | Contracting; "sharp pullback"; "retrenchment"; "severe weakness" |
| 31-45 | Below trend; "sluggish"; "cautious consumers"; "soft" |
| 46-54 | At trend; "moderate pace"; "sustained"; "solid" |
| 55-65 | Above trend; "robust"; "strong momentum"; "brisk" |
| 66-80 | Well above trend; "unsustainably rapid"; "boom" |
| 81-100 | Extreme; historically unprecedented spending surge |

**Anchors**: 15-20 (2008 Q4-2009 Q1; 2020 Q2), 35-42 (2011-13 "moderate"), 50-55 (2014-19 "solid pace"), 62-68 (2021 Q3-2022 Q1 surge)

**Gotcha**: Score the NET position across consumer spending and business investment, weighted by discussion emphasis. "Solid consumer spending" + "weak business investment" might net to 45-48.

---

### 5. PRODUCTIVITY [1-100 or N/A]
Higher = MORE productivity growth perceived.

| Range | Meaning |
|-------|---------|
| 1-20 | Deteriorating productivity; shrinking potential output |
| 21-35 | Well below historical trend; "anemic"; "disappointing" |
| 36-45 | Modestly below trend; "sluggish" |
| 46-54 | At historical trend growth (~2%) |
| 55-65 | Above trend; "encouraging gains"; "stronger than expected" |
| 66-80 | Significantly above trend; "productivity boom" |
| 81-100 | Exceptional/unprecedented gains |

**N/A if not discussed.** This dimension is frequently N/A.

---

## TIER 1: CORE FINANCIAL DIMENSIONS

### 6. FINANCIAL_CONDITIONS [1-100]
Higher = financial conditions are TIGHTER / more restrictive.

| Range | Meaning |
|-------|---------|
| 1-15 | Extremely loose; "excessive liquidity"; "bubble conditions"; "easy credit" |
| 16-30 | Loose; "accommodative conditions"; "credit freely available"; "supportive" |
| 31-45 | Somewhat loose to neutral; "generally supportive"; "broadly accommodative" |
| 46-54 | Neutral; normal credit, typical spreads; 2017-19 is the anchor neutral period |
| 55-65 | Somewhat tight; "conditions have tightened"; "less accommodative" |
| 66-80 | Tight; "restrictive"; "credit hard to obtain"; stress emerging |
| 81-100 | Extremely tight/crisis; "credit frozen"; "systemic stress"; "panic" |

**Anchors**: 10-20 (2005-06 pre-crisis ease), 46-54 (2017-19 normal — THIS IS THE NEUTRAL ANCHOR), 55-65 (2022 rate hike effects), 85-95 (Sept 2008 credit freeze; March 2020 dash for cash)

**Gotcha**: This is about CONDITIONS, not POLICY. Rate hikes are policy; the resulting credit tightness is conditions. Score what staff says about markets, credit availability, spreads — not the rate decision itself.

**CRITICAL**: In v3, the 2017-19 period was underscored at 34-42 against an anchor of 50. This neutral period should be scored 46-54.

---

### 7. TREASURY_STRESS [1-100 or N/A]
Higher = MORE Treasury market dysfunction.

| Range | Meaning |
|-------|---------|
| 1-20 | Exceptionally smooth functioning; low volatility; "well-functioning" |
| 21-35 | Normal but quiet; typical auction demand; no concerns |
| 36-50 | Normal market functioning; some yield volatility but orderly |
| 51-60 | Elevated concern; unusual volatility; "dealers reported some difficulty" |
| 61-75 | Significant stress; liquidity impaired; "dislocations"; "strains" |
| 76-90 | Severe dysfunction; auction failures; basis-trade blowups |
| 91-100 | Complete market breakdown |

**Anchors**: 25-35 (2010-15 calm markets), 40-50 (normal), 65-80 (March 2020 "dash for cash"), 85-95 (Sept-Oct 2008)

**CRITICAL GOTCHA (the #3 error source in v3):** Yield movements are NOT dysfunction. Rising yields from policy expectations, inflation expectations, or supply expectations are NORMAL MARKET FUNCTIONING (score 36-50). Score > 55 ONLY when staff describes actual market dysfunction: liquidity problems, bid-ask spread widening, settlement failures, auction demand shortfalls, basis-trade stress. "Treasury yields rose sharply" alone is NOT Treasury stress — it's normal price adjustment.

**N/A if Treasury market not specifically discussed.**

---

### 8. CREDIT_SPREADS [1-100]
Higher = MORE credit stress (wider spreads, less availability).

| Range | Meaning |
|-------|---------|
| 1-15 | Extremely compressed; underpriced risk; "historically narrow"; "risk-on" |
| 16-30 | Below normal; "tight spreads"; "ample credit availability"; "strong issuance" |
| 31-45 | Somewhat below normal; "generally favorable"; "accommodative credit" |
| 46-54 | Normal credit conditions; typical spreads |
| 55-65 | Somewhat wide; "some widening"; "less favorable" |
| 66-80 | Wide; "significant widening"; "reduced access"; "flight to quality" |
| 81-100 | Severely wide; credit rationing; lending freeze; "markets seized" |

**Anchors**: 10-20 (2005-06 extremely compressed), 30-40 (2013-19 generally favorable), 55-65 (2022 mild widening), 80-95 (2008 Q4 credit freeze)

**Gotcha**: Score the LEVEL of spreads, not the direction. Spreads widening from extremely compressed (10→25) is still below normal and should score <50.

---

### 9. EQUITY_VALUATION [1-100 or N/A]
Higher = MORE equity market stress/concern.

| Range | Meaning |
|-------|---------|
| 1-15 | Extreme overvaluation concern; "bubble"; "irrational exuberance"; "frothy" |
| 16-30 | Elevated valuations; "stretched"; "rich by historical standards" |
| 31-45 | Modestly above fair value; "somewhat elevated" |
| 46-54 | Roughly fair valued; no particular concern |
| 55-65 | Modestly depressed; "declined but orderly" |
| 66-80 | Significantly depressed; "sharp correction"; "distressed" |
| 81-100 | Extreme undervaluation; fire-sale prices; panic selling |

**Anchors**: 15-25 (2000 dot-com bubble, 2005-06), 40-50 (2013-19 typical), 65-80 (2008 Q4 crash, March 2020)

**CRITICAL GOTCHA:** Falling prices ≠ undervalued. Score the staff's VALUATION/CONCERN VIEW, not price direction. If staff discusses price moves without valuation commentary, default to 45-55. "Equities declined" alone → 50-55. "Equities declined and are now at distressed levels" → 70-80. "Equities remain elevated despite recent decline" → 25-35.

**N/A if equity markets not specifically discussed.**

---

### 10. BANKING_STRESS [1-100 or N/A]
Higher = MORE banking system stress/impairment.

**NOTE: This dimension was called BANKING_HEALTH in v3 and caused widespread polarity confusion. It is now renamed to BANKING_STRESS with explicit "higher = more stress" polarity.**

| Range | Meaning |
|-------|---------|
| 1-15 | Excessive risk-taking/leverage (different problem, but low-stress direction) |
| 16-30 | Very healthy; strong capital; "well-capitalized"; "resilient" |
| 31-45 | Healthy with minor concerns; "sound but..."; some CRE/credit concentration |
| 46-54 | Neutral; mixed signals; some stress pockets but system sound |
| 55-65 | Emerging stress; rising NPLs; "tightening lending standards"; "cautious" |
| 66-80 | Significant stress; capital concerns; bank failures; "under pressure" |
| 81-100 | Severe systemic stress; multiple failures; "crisis"; solvency concerns |

**Anchors**: 25-35 (2014-19 well-capitalized), 40-50 (2006-07 growing concerns), 55-65 (March 2023 SVB), 70-85 (2008-09 systemic crisis)

**CRITICAL GOTCHA (the #4 error source in v3):** "Well-capitalized" / "sound" / "healthy banking system" → score MUST be BELOW 50 (low stress). The v3 scorer frequently pushed healthy-bank language ABOVE 50, confusing "health" polarity with "stress" polarity. If the staff says banks are healthy, that means LOW stress → score 25-40.

**N/A if banking system not specifically discussed.**

---

### 11. DOLLAR_STRENGTH [1-100 or N/A]
Higher = MORE dollar strength concern.

**NOTE: This dimension was called DOLLAR_FX in v3 and suffered ~40% polarity inversion. It is now renamed to DOLLAR_STRENGTH with explicit directional rules.**

| Range | Meaning |
|-------|---------|
| 1-15 | Extreme weakness; "sharply depreciating"; "dollar under pressure" |
| 16-30 | Notable weakness; "declined"; "depreciation" |
| 31-45 | Modest weakness to stable; "mixed"; "little changed" |
| 46-54 | Stable; no concern; "broadly unchanged" |
| 55-65 | Modest strength; "appreciated"; "strengthened" |
| 66-80 | Notable strength; "broad-based appreciation"; "strong dollar weighing on exports" |
| 81-100 | Extreme strength; "DXY at multi-decade highs"; "severe headwind" |

**Anchors**: 20-30 (2003-04 dollar decline, 2017 depreciation), 45-55 (2012-13 stable), 60-70 (2015 H1 sharp appreciation), 75-85 (2022 Q3 DXY at 20-year highs)

**BRIGHT-LINE RULE:** Dollar appreciation / strengthening → score > 50. Dollar depreciation / weakening → score < 50. This rule is mandatory and was violated ~40% of the time in v3.

**N/A if dollar/FX not specifically discussed.**

---

## TIER 2: INFLATION SUB-COMPONENTS (score each if discussed, N/A if not)

All use the same polarity: **higher = more price pressure** in that category.

### S1. INFLATION_GOODS [1-100 or N/A]
1 = falling goods prices; 50 = stable goods prices; 100 = surging goods inflation

### S2. INFLATION_SERVICES [1-100 or N/A]
1 = falling services prices; 50 = stable; 100 = surging services inflation

### S3. INFLATION_HOUSING [1-100 or N/A]
1 = declining rents/shelter costs; 50 = stable; 100 = surging housing/shelter inflation

### S4. INFLATION_EXPECTATIONS [1-100 or N/A]
1 = well-anchored below target; 50 = anchored at target; 100 = unanchored/rising

**Anchors**: 25-35 (2009 "risk of unanchoring to downside"), 45-55 (2014-19 "well-anchored"), 60-70 (2022 "showing signs of moving up")

---

## CROSS-DIMENSION COHERENCE CHECKS (execute in Part 1)

After determining directional signals for all dimensions, verify these relationships:

1. **OUTPUT_GAP ↔ LABOR_TIGHTNESS**: Should generally move together. Both below 50 in recession, both above 50 in boom. If they diverge by >15 points, explain why (e.g., jobless recovery, labor hoarding).
2. **OUTPUT_GAP ↔ CONSUMPTION_INVESTMENT**: Should generally move together. Divergence >15 points needs explanation (e.g., inventory-driven GDP vs weak final sales).
3. **FINANCIAL_CONDITIONS ↔ CREDIT_SPREADS**: Should generally co-move. Tight FC with compressed spreads is contradictory — explain or fix.
4. **FINANCIAL_CONDITIONS ↔ TREASURY_STRESS**: Should co-move in crises. In normal times, Treasury stress is N/A or near 40-50 regardless of FC.
5. **INFLATION_PRESSURE ↔ INFLATION sub-dimensions**: Parent score should be consistent with the weighted average of scored sub-dimensions.

---

## OUTPUT FORMAT

Provide your analysis in **three parts**.

### Part 1: Thinking Process

Write your chain-of-thought reasoning BEFORE scoring. You must explicitly:

1. **Identify document type**: Is this a transcript (individual staff speakers) or minutes (synthesized summary)? Segmented (post-2005, separate staff review sections) or unsegmented (pre-2005, mixed with participant content)?
2. **Note era context**: What period is this meeting from? State the broad macro backdrop WITHOUT letting it override what the text actually says.
3. **For each core dimension**: State the directional signal in words BEFORE assigning a number. "Staff sees [dimension] as [above/below/at] midpoint because..."
4. **Polarity verification**: For any dimension where the direction feels ambiguous, explicitly check: "Higher = more [X]. My evidence says [Y]. Score [matches/doesn't match]."
5. **Bright-line check**: For OUTPUT_GAP, FINANCIAL_CONDITIONS, CREDIT_SPREADS, BANKING_STRESS, DOLLAR_STRENGTH, and TREASURY_STRESS — verify the bright-line rule is satisfied.
6. **Cross-dimension coherence**: Check the 5 pairs listed above. If any pair diverges, explain why.
7. **For transcripts**: Identify the staff speakers and which topics each covers (e.g., Stockton=economic outlook, Johnson/Kamin=international, Dudley/Lacker=financial markets).
8. **For unsegmented minutes (pre-2005)**: Note which content is staff-attributable vs participant-attributable. Only score staff content.

### Part 2: Evidence and Scores

For each scored dimension, provide:
- **Score** [1-100] **±X** [High/Moderate/Low confidence]
- **Evidence**: 1-2 key quotes from the text (with speaker attribution for transcripts)
- **Center-of-gravity summary**: One sentence explaining the score
- **Direction confirmation**: "[Dimension] is [above/below/at] neutral because [reason]" — confirming the bright-line rule is met where applicable

### Part 3: Structured Output

Copy-paste ready format:

```
MEETING_DATE: YYYY-MM-DD
SOURCE_TYPE: [minutes/transcript]
--- ECONOMIC CONDITIONS ---
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
PRODUCTIVITY: [1-100 or N/A]
PRODUCTIVITY_UNC: [+-X or N/A]
PRODUCTIVITY_CONF: [High/Moderate/Low or N/A]
--- FINANCIAL CONDITIONS ---
FINANCIAL_CONDITIONS: [1-100]
FINANCIAL_CONDITIONS_UNC: [+-X]
FINANCIAL_CONDITIONS_CONF: [High/Moderate/Low]
TREASURY_STRESS: [1-100 or N/A]
TREASURY_STRESS_UNC: [+-X or N/A]
TREASURY_STRESS_CONF: [High/Moderate/Low or N/A]
CREDIT_SPREADS: [1-100]
CREDIT_SPREADS_UNC: [+-X]
CREDIT_SPREADS_CONF: [High/Moderate/Low]
EQUITY_VALUATION: [1-100 or N/A]
EQUITY_VALUATION_UNC: [+-X or N/A]
EQUITY_VALUATION_CONF: [High/Moderate/Low or N/A]
BANKING_STRESS: [1-100 or N/A]
BANKING_STRESS_UNC: [+-X or N/A]
BANKING_STRESS_CONF: [High/Moderate/Low or N/A]
DOLLAR_STRENGTH: [1-100 or N/A]
DOLLAR_STRENGTH_UNC: [+-X or N/A]
DOLLAR_STRENGTH_CONF: [High/Moderate/Low or N/A]
--- INFLATION SUB-COMPONENTS (N/A if not discussed) ---
INFLATION_GOODS: [1-100 or N/A]
INFLATION_SERVICES: [1-100 or N/A]
INFLATION_HOUSING: [1-100 or N/A]
INFLATION_EXPECTATIONS: [1-100 or N/A]
--- FLAGS ---
ANOMALY_FLAG: [Yes/No]
ANOMALY_NOTE: [brief description if Yes, otherwise blank]
```

Now read the staff briefing content and produce the full three-part analysis.
