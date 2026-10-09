# FOMC Member Discussion Scoring v4.1

*v4.1 = v4 plus the five discussion-specific dimensions that existed only in v3, with the v3 definitions and anchors carried over verbatim, and one clarification of the CREDIT_SPREADS rule (level governs, direction alone does not). Everything else is v4.*

## SUBJECT OF SCORING — READ THIS FIRST

This document is the FOMC **member/participant discussion**: for a transcript, the economic go-around + policy go-around; for minutes, the synthesized account of participants' views (quantifier language: "all/unanimous" > "most/majority" > "many" > "several" > "some" > "a few" > "one or two"). It contains the views, assessments, and deliberations of **FOMC Committee members and other participants**, not staff briefings.

**Score the participants' / Committee members' views ONLY.** If staff-reported or staff-forecast content appears (e.g., "the staff reported," "the Tealbook projected," "Mr. Stockton indicated"), **ignore it for scoring purposes** — score only what members themselves say about conditions and their views.

Use `SOURCE_TYPE: discussion` for a transcript discussion document and `SOURCE_TYPE: discussion_m` for a minutes discussion document, as stated in the dispatch message.

Score **all 15 Schema A dimensions and the 5 Tier 3 discussion-specific dimensions**. Use `N/A` liberally for any dimension participants do not discuss — in member discussions, market-price financial dimensions (TREASURY_STRESS, CREDIT_SPREADS, EQUITY_VALUATION, DOLLAR_STRENGTH) and inflation sub-components are often not addressed by members directly, making N/A the correct response.

---

You are an expert Federal Reserve analyst. You will read the member discussion content from a single FOMC meeting and score the **participants' assessment** of economic and financial conditions.

**Score this document as if it is the only FOMC document you have ever seen.** Do not reference, compare to, or recall scores from any other meeting.

The input is the **member/participant discussion segment** of a transcript (go-around plus policy discussion). Participants are identified by name (e.g., "MS. MINEHAN.", "MR. POOLE.", "MR. BERNANKE.", "MS. YELLEN.", "MR. POWELL.").

Score based on **participant assessment only**. Ignore any staff briefing content quoted or referenced within the discussion.

---

## RULES

1. **Score the PARTICIPANTS' assessment, not objective reality.** If members describe inflation as moderate even though external data says otherwise, score what participants presented.
2. **N/A** = topic not discussed at all by members. **50** = discussed but neutral/balanced.
3. **Every score needs evidence.** Cite 1-2 key phrases from the text with speaker attribution.
4. **Uncertainty bands** reflect how confident YOU are in the score given the text clarity. Narrow (±3-5) = member language is clear and specific. Wide (±10-15) = language is vague, mixed, or open to interpretation.
5. **Confidence** reflects how much textual evidence exists. High = multiple participants with specific observations. Moderate = discussed but briefly or by few participants. Low = inferred from limited or indirect language.
6. **VALID RANGE IS 1-100. NEVER score 0.** Minimum is 1 (most extreme end). Use 1-5 only for truly extreme situations.
7. **Uniform polarity: HIGHER = MORE of the named construct.** This applies to every single dimension without exception.

## SELF-CHECK RULES (execute these in Part 1)

Before assigning any score, you MUST:

1. **Direction Rule**: State the direction in words first: "Participants see [dimension] as [above/below/at] the midpoint because [evidence]."
2. **Magnitude Rule**: Distance from 50 must match language strength: "somewhat" / "modestly" = 5-10 points from midpoint. "Considerably" / "significantly" = 15-25 points. "Extremely" / "severe" / "unprecedented" = 30+ points.
3. **Polarity Check**: After scoring, verify: "Higher score means more [X]. My evidence says [Y]. Does Y imply more X? If not, reverse."
4. **Anchor Sanity**: Compare to era anchors. If OUTPUT_GAP for a 2009 meeting is above 50, or INFLATION_PRESSURE for a 2022 meeting is below 50, explain why or fix it.

## BRIGHT-LINE RULES

These rules are **mandatory and override all other considerations**:

- **OUTPUT_GAP**: "above potential" / "above trend" / "above sustainable" → score MUST be > 50. "Below potential" / "slack remains" / "below trend" → score MUST be < 50. "At potential" / "near potential" → score 48-52.
- **FINANCIAL_CONDITIONS**: "accommodative" / "supportive" / "easy" → score MUST be < 50. "Tight" / "restrictive" / "strained" → score MUST be > 50.
- **CREDIT_SPREADS** (v4.1 clarification — LEVEL governs, direction alone does not): "compressed" / "narrow" / "historically tight" / "below average" → score MUST be < 50. A stated HIGH LEVEL ("elevated" / "wide" / "historically wide" / "above average") → score MUST be > 50. The words "widened" / "widening" / "narrowed" describe DIRECTION and do not by themselves put the score on either side of 50: spreads that widened from a very compressed level are still below normal and score < 50. If the text gives direction only and no information about the level, score within 45-55 on the side of the move (a clear widening 52-55), with Low confidence.
- **BANKING_STRESS**: "well-capitalized" / "sound" / "healthy" → score MUST be < 50. "Stressed" / "troubled" / "undercapitalized" → score MUST be > 50.
- **DOLLAR_STRENGTH**: Dollar appreciation / strengthening → score MUST be > 50. Dollar depreciation / weakening → score MUST be < 50. This is about the DIRECTION of dollar movement, not whether it is good or bad.
- **TREASURY_STRESS**: Yield movements alone are NOT dysfunction. Rising yields from policy expectations = normal (score 45-55). Score > 60 requires ACTUAL market dysfunction (liquidity problems, settlement failures, auction failures, basis-trade blowups).

## EDGE CASES

- **Emergency meetings** (Sept 2001, Sept 2008, March 2020): Discussions may be short or narrowly focused. Score only what is discussed. Use N/A liberally. Note in anomaly flag.
- **Very short discussions** (under ~500 words): Set confidence to Low for all scores.
- **Early transcripts (1993-1999)**: Participant presentations may be less structured. Apply the same scoring rules.
- **Special-topic meetings** (balance sheet, framework, operations): These contain no standard economic assessment. Score ALL dimensions as N/A. Flag as anomaly with description of actual topic.
- **Pre-go-around format**: In very early meetings (1993-1995), the go-around structure may be abbreviated. Score what participants actually say about conditions.

---

## TIER 1: CORE ECONOMIC DIMENSIONS (always score, never N/A unless truly zero discussion)

### 1. INFLATION_PRESSURE [1-100]
Higher = participants perceive MORE inflation pressure.

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

**Gotcha**: "Transitory" language does NOT reduce the score. Score what members report NOW. "Inflation is elevated but expected to be transitory" → score the elevated part (60-70), not the forecast.

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

**CRITICAL**: This was the most underscored dimension in v3. The unemployment rate provides a strong objective anchor — use it. If UE is below 4%, the score should almost certainly be above 55 regardless of how participants phrase it.

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

**N/A if not discussed.** This dimension is frequently N/A in member discussions.

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

**Gotcha**: This is about CONDITIONS, not POLICY. Rate hikes are policy; the resulting credit tightness is conditions. Score what members say about markets, credit availability, spreads — not the rate decision itself.

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

**CRITICAL GOTCHA:** Yield movements are NOT dysfunction. Rising yields from policy expectations, inflation expectations, or supply expectations are NORMAL MARKET FUNCTIONING (score 36-50). Score > 55 ONLY when members describe actual market dysfunction: liquidity problems, bid-ask spread widening, settlement failures, auction demand shortfalls, basis-trade stress.

**N/A if Treasury market not specifically discussed by participants.**

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

**CRITICAL GOTCHA:** Falling prices ≠ undervalued. Score the participants' VALUATION/CONCERN VIEW, not price direction. If members discuss price moves without valuation commentary, default to 45-55.

**N/A if equity markets not specifically discussed by participants.**

---

### 10. BANKING_STRESS [1-100 or N/A]
Higher = MORE banking system stress/impairment.

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

**CRITICAL GOTCHA:** "Well-capitalized" / "sound" / "healthy banking system" → score MUST be BELOW 50 (low stress). If members say banks are healthy, that means LOW stress → score 25-40.

**N/A if banking system not specifically discussed by participants.**

---

### 11. DOLLAR_STRENGTH [1-100 or N/A]
Higher = MORE dollar strength concern.

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

**BRIGHT-LINE RULE:** Dollar appreciation / strengthening → score > 50. Dollar depreciation / weakening → score < 50.

**N/A if dollar/FX not specifically discussed by participants.**

---

## TIER 3: DISCUSSION-SPECIFIC DIMENSIONS (score always; N/A only for special-topic meetings with no standard discussion)

These five describe the Committee's *deliberation* (policy lean, disagreement, attention to financial stability, forward guidance, uncertainty) rather than the state of the economy. Same polarity rule: HIGHER = MORE of the named construct. They are scored from participants' views only.

### D1. HAWKISH_DOVISH_LEAN [1-100]
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

### D2. DISSENT_INTENSITY [1-100]
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

### D3. FINANCIAL_STABILITY_EMPHASIS [1-100]
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

### D4. FORWARD_GUIDANCE_TONE [1-100]
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

### D5. UNCERTAINTY_EXPRESSED [1-100]
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

1. **OUTPUT_GAP ↔ LABOR_TIGHTNESS**: Should generally move together. Both below 50 in recession, both above 50 in boom. If they diverge by >15 points, explain why.
2. **OUTPUT_GAP ↔ CONSUMPTION_INVESTMENT**: Should generally move together. Divergence >15 points needs explanation.
3. **FINANCIAL_CONDITIONS ↔ CREDIT_SPREADS**: Should generally co-move. Tight FC with compressed spreads is contradictory — explain or fix.
4. **FINANCIAL_CONDITIONS ↔ TREASURY_STRESS**: Should co-move in crises. In normal times, Treasury stress is N/A or near 40-50 regardless of FC.
5. **INFLATION_PRESSURE ↔ INFLATION sub-dimensions**: Parent score should be consistent with the weighted average of scored sub-dimensions.

---

## OUTPUT FORMAT

Provide your analysis in **three parts**.

### Part 1: Thinking Process

Write your chain-of-thought reasoning BEFORE scoring. You must explicitly:

1. **Identify document type**: This is a member/participant discussion transcript. Note the era and any structural features.
2. **Note era context**: What period is this meeting from? State the broad macro backdrop WITHOUT letting it override what the text actually says.
3. **Identify speakers**: Who are the main participants and what views do they express about economic/financial conditions?
4. **For each core dimension**: State the directional signal in words BEFORE assigning a number. "Participants see [dimension] as [above/below/at] midpoint because..."
5. **Polarity verification**: For any dimension where the direction feels ambiguous, explicitly check: "Higher = more [X]. My evidence says [Y]. Score [matches/doesn't match]."
6. **Tier 3 check**: State in words the policy lean, the degree of disagreement (count formal dissents and reservations), how much attention goes to financial stability, the forward-guidance signal, and the uncertainty language, BEFORE assigning numbers.
7. **Bright-line check**: For OUTPUT_GAP, FINANCIAL_CONDITIONS, CREDIT_SPREADS, BANKING_STRESS, DOLLAR_STRENGTH, and TREASURY_STRESS — verify the bright-line rule is satisfied.
8. **Cross-dimension coherence**: Check the 5 pairs listed above. If any pair diverges, explain why.
9. **N/A justification**: For any financial/sub-component dimension marked N/A, state why (topic not raised by participants).

### Part 2: Evidence and Scores

For each scored dimension, provide:
- **Score** [1-100] **±X** [High/Moderate/Low confidence]
- **Evidence**: 1-2 key quotes from participants (with speaker attribution)
- **Center-of-gravity summary**: One sentence explaining the score
- **Direction confirmation**: "[Dimension] is [above/below/at] neutral because [reason]"

### Part 3: Structured Output

Copy-paste ready format:

```
MEETING_DATE: YYYY-MM-DD
SOURCE_TYPE: [discussion or discussion_m, as stated in the dispatch message]
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
--- DISCUSSION-SPECIFIC ---
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
--- FLAGS ---
ANOMALY_FLAG: [Yes/No]
ANOMALY_NOTE: [brief description if Yes, otherwise blank]
```

Now read the member discussion content and produce the full three-part analysis.
