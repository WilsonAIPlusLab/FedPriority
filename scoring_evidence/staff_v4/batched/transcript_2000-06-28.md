# FOMC Staff Assessment Scoring — 2000-06-28
**Source**: Transcript (staff_economic_briefing.txt + staff_outlook_briefing.txt)
**Scored by**: FOMC_Staff_Review_Prompt_v4

---

## Part 1: Thinking Process

### 1. Document Type Identification

This is a **transcript** from the June 28, 2000 FOMC meeting. Individual staff speakers are identified:
- **MR. STOCKTON** (David Stockton) — domestic economic outlook, GDP, labor, inflation, financial conditions model analysis, recession probability
- **MS. JOHNSON** (Karen Johnson) — international financial markets, dollar/FX, trade, foreign growth
- **MR. SLIFMAN** (Larry Slifman) — mentioned as co-presenter in the appendix note; inflation cost accounting (appears at pages 20-22)
- **MR. KOHN** (Don Kohn) — questions/discussion of NAIRU, dollar depreciation as inflationary force (Q&A section, not primary briefing)

The transcript is a pre-2005 era meeting. The staff briefing content is in the dedicated "staff economic briefing" and "staff outlook briefing" files. The "questions_for_staff.txt" is primarily participant discussion/Q&A — I will draw on staff responses there (Stockton, Kohn) but be careful not to score participant views.

The transcript is **partially damaged/garbled** — many lines appear in two-column OCR format with text split oddly (left and right columns interleaved). Despite this, the core content is recoverable.

### 2. Era Context

June 2000 is the **peak of the late 1990s expansion / dot-com boom**. The Fed had been tightening since June 1999. The federal funds rate was at 6.5% (having been raised 175 bps). The stock market had peaked in March 2000 and Nasdaq was already down ~25-30%. The economy was running very hot — unemployment near 4%, GDP above trend — but with early signs of slowing. This is exactly the period the rubric anchors call out: "late 90s boom; 2022" → OUTPUT_GAP 57-63, LABOR_TIGHTNESS 65-75.

### 3. Directional Signals per Dimension

**INFLATION_PRESSURE**: Staff describes core PCE "about to pick up," unit labor costs accelerating, GDP 3% above potential driving inflation, oil prices boosting total PCE. Total PCE prices stepping up this year, core inflation above 1999 levels. The regression framework suggests a 0.6 pp acceleration in core inflation from the ~3% output gap. Nonfinancial corporate deflator accelerating. Staff sees inflation as **modestly to clearly above target** — above midpoint. The text says total PCE rises in 2000 then "drops back to a 2 percent" in 2001, suggesting *current* reading above 2%. Core PCE expected at "2.1 and 2.2 percent this year and next" per President Parry's Fed staff estimate. Direction: **above 50**, but not extremely elevated — moderately above target.

**OUTPUT_GAP**: Stockton explicitly states "we estimate that the level of actual GDP is about 3 percent above the level of potential." The economy has been "rising at more than a 5-1/2 percent pace over the past two years." This is a clear **above-potential** signal. Bright-line rule: MUST be > 50. With a 3% positive output gap stated explicitly, this is well above neutral — in the 63-70 range.

**LABOR_TIGHTNESS**: "Pressures in labor markets are relatively intense." Staff estimates NAIRU at ~5.25%, current unemployment clearly below that (the text references UE near 4% based on era context and staff NAIRU discussion — Stockton says NAIRU is "5-1/4 percent" and current rate is "a tiny bit below even the low NAIRU"). District reporters confirm "labor markets remain very tight." Direction: **well above 50**. Unemployment below NAIRU, very tight by any measure.

**CONSUMPTION_INVESTMENT**: Mixed picture: Consumer spending "decidedly slower growth" anticipated as a deceleration from very high levels. Domestic spending has been rising at "more than 5-1/2 percent pace over the past two years" but projected to slow to "3-1/2 percent in 2001." Housing showing clear signs of slowing. Business equipment spending (E&S) "remained very strong" — capital spending orders robust. Net: still above trend but decelerating. Direction: **above 50** but near the "strong/slowing to moderate" range.

**PRODUCTIVITY**: Stockton and Slifman discuss productivity extensively. Structural productivity growth is a key theme — "upward productivity growth" is mentioned as affecting equilibrium rates. Staff discusses "sustained, above-trend productivity growth" as the reason the expansion has continued. Slifman refers to "the component of our productivity projection" and "underlying structural productivity growth." Staff sees productivity as **above historical trend** — above 50, notably elevated.

**FINANCIAL_CONDITIONS**: Stockton discusses "further tightening of financial conditions" assumed in the forecast. Real rates on corporate bonds expected to "resume the upward trajectory." However, he notes that "the stock market...has risen more than 12 percent over the past year" — equities still buoyant. The financial conditions model analysis shows the stock market offset has "dampened considerably the restraining effects that would be expected to accompany a substantial run-up in the funds rate." Net: financial conditions are **tightening but not yet fully restrictive**. The funds rate assumption is "a bit above the upper end of the range over the past decade." Direction: **above 50** (tighter than neutral), but not dramatically so given stock market resilience.

**TREASURY_STRESS**: The text mentions real rates on corporate bonds and the federal funds rate trajectory, and discusses Treasury-related items in the opening (Treasury auction discussion in the pre-meeting segment), but there is no description of Treasury market dysfunction — no liquidity problems, auction failures, etc. The brief pre-meeting Treasury discussion appears to be about the mechanics of debt management, not market stress. Direction: **near neutral/normal**. Yield movements are from policy expectations, not dysfunction. Score in the 36-50 range.

**CREDIT_SPREADS**: Staff discusses "real rates on corporate bonds" and the model's expected corporate bond rate trajectory. The Southeast district banker notes "their best days in terms of credit quality may be behind them" and "more reports of...less accommodative lending." However, the dominant financial story is equities, not credit spreads. Johnson notes "foreign private purchases of U.S. securities remain at extraordinary levels." No explicit mention of spread widening or tightening. Some slight tightening of lending standards is noted anecdotally. Direction: **slightly above 50** (mild tightening of credit conditions), but evidence is limited.

**EQUITY_VALUATION**: Stockton notes "stock prices have risen more than 12 percent over the past year and are projected to remain flat going forward." The model expected a "drop of 13 percent over the past year" but instead equities rose — the resilience surprised the model. Staff mentions "enthusiasm in equity markets." The banker in the District go-around says "the days of irrational exuberance are over and now we just have exuberance." The staff's model projects equities flat going forward (implicitly still elevated). Staff view is that equities remain **elevated** — stock market has provided stimulus that offset rate hikes. Direction: **below 50** (elevated valuations = low stress on the equity_valuation scale where higher = more stress). Score 25-35 range.

**BANKING_STRESS**: The go-around mentions some districts noting banks tightening credit standards ("more cautious and less accommodative lending"), but the overall system is described as still healthy. District bankers note credit quality concerns are "behind them" with tightening going forward. No systemic stress. Direction: **below 50** (low stress), possibly with some minor emerging concerns. Score 35-45.

**DOLLAR_STRENGTH**: Johnson (MS. JOHNSON) provides an extensive international briefing. She states: "the average foreign exchange value of the dollar in terms of the currencies of the other major industrial countries — the black line — has risen on balance so far this year." The dollar has been appreciating against the euro (described as continuing its "upward trend"). Against the yen, the dollar is "little changed from where it started the year." The staff projects "the real exchange value of the dollar...will depreciate on balance over the forecast period" — but the *current* description is dollar has **risen/appreciated** year-to-date. Bright-line: dollar appreciation → score MUST be > 50. Score: modestly to notably above 50.

**INFLATION_GOODS (S1)**: Johnson describes non-oil import prices "providing a favorable backdrop" to inflation (implying goods import prices have been declining), but projects core import prices to "accelerate to an annual rate of increase of about 3 percent, after experiencing significantly lower increases and even decreases since 1997." Non-oil commodity prices "expected to recover." Dollar appreciation had been offsetting goods inflation from abroad. Going forward, goods inflation expected to **pick up**. Direction: currently near neutral/below, but turning up. Score around 45-55.

**INFLATION_SERVICES (S2)**: Not explicitly broken out. The general inflation framework mentions unit labor costs, compensation, and productivity. Services inflation is implicitly embedded in the core PCE discussion. N/A for explicit services discussion.

**INFLATION_HOUSING (S3)**: Housing clearly discussed. Rising interest rates and higher home prices have "lifted monthly payments relative to personal income." Housing starts declining from 1.67 million to ~1.5 million units. Some price appreciation moderation anticipated. Housing is explicitly a channel of restraint. Current housing prices still rising. Direction: housing inflation elevated but starting to ease. Score around 55-60 (currently elevated, easing).

**INFLATION_EXPECTATIONS (S4)**: Not explicitly discussed in the staff briefing. The NAIRU discussion is about the structural inflation dynamics model, not survey-based expectations. No specific mention of survey expectations or breakeven inflation rates. Score N/A.

### 4. Polarity Verification

- **FINANCIAL_CONDITIONS**: Higher = tighter. Staff says further tightening assumed, rate hikes working through lags. Score > 50. ✓
- **CREDIT_SPREADS**: Higher = wider/more stress. Evidence shows some tightening of standards but no explicit spread data. Mild. ✓
- **EQUITY_VALUATION**: Higher = more stress. Staff shows equities elevated (still buoyant, surprising model). That means LOW stress → score < 50. ✓
- **BANKING_STRESS**: Higher = more stressed. Banks healthy but tightening. Score < 50. ✓
- **DOLLAR_STRENGTH**: Higher = stronger dollar. Dollar has risen YTD. Score > 50. ✓
- **OUTPUT_GAP**: Higher = more above potential. GDP 3% above potential stated explicitly. Score > 50, well above. ✓

### 5. Bright-Line Checks

- **OUTPUT_GAP**: "we estimate that the level of actual GDP is about 3 percent above the level of potential." → Score MUST be > 50. Confirmed: scoring ~67.
- **FINANCIAL_CONDITIONS**: "further tightening of financial conditions" projected; funds rate above historical range. → Score > 50 (tight direction). Confirmed: scoring ~57.
- **CREDIT_SPREADS**: No "compressed/narrow" language. Some tightening noted. → Score slightly > 50. Confirmed.
- **BANKING_STRESS**: No systemic stress, mild caution. → Score < 50. Confirmed: scoring ~38.
- **DOLLAR_STRENGTH**: Dollar "has risen on balance so far this year." → Score MUST be > 50. Confirmed: scoring ~62.
- **TREASURY_STRESS**: No actual market dysfunction described. → Score 36-50. Confirmed: N/A given no Treasury-specific market discussion in briefing.

### 6. Cross-Dimension Coherence Checks

1. **OUTPUT_GAP (67) ↔ LABOR_TIGHTNESS (70)**: Both well above 50. Consistent with late-expansion, hot economy. Gap is small (~3 pts). ✓
2. **OUTPUT_GAP (67) ↔ CONSUMPTION_INVESTMENT (62)**: Both above 50. Domestic spending deceleration from very high levels. Slight divergence explainable by deceleration in progress. ✓
3. **FINANCIAL_CONDITIONS (57) ↔ CREDIT_SPREADS (52)**: FC slightly tighter, credit spreads mildly elevated. Roughly consistent — credit spreads hadn't widened dramatically yet. ✓
4. **FINANCIAL_CONDITIONS (57) ↔ TREASURY_STRESS (N/A)**: Treasury stress N/A — normal market functioning. Consistent with mildly tight FC. ✓
5. **INFLATION_PRESSURE (62) ↔ sub-dimensions**: Goods inflation S1 (~48), housing S3 (~57), expectations N/A. Weighted average roughly consistent with core parent score of 62. ✓

### 7. Speaker-Topic Mapping

- **MR. STOCKTON**: Domestic GDP, consumption, investment, housing, productivity, financial conditions model, recession probabilities, inflation (unit labor costs, output gap → inflation regression)
- **MS. JOHNSON**: International — dollar/FX, foreign growth, trade flows, oil prices, import prices, current account, foreign financial markets
- **MR. SLIFMAN** (mentioned in note): Part of the "Chart Show" — inflation cost accounting (nonfinancial corporate deflator, unit labor costs)
- **MR. KOHN** (Q&A): Discussion of NAIRU upside/downside risks, dollar depreciation as inflationary force

---

## Part 2: Evidence and Scores

### 1. INFLATION_PRESSURE

**Score: 62 ±7 | High confidence**

**Evidence**:
- MR. STOCKTON (p.20): "we estimate that the level of actual GDP is about 3 percent above the level of potential...a 3 percent imbalance between aggregate demand and aggregate supply at the end of last year is likely to be associated with a 0.6 percentage point step-up in inflation this year."
- MR. STOCKTON (p.21): "demand has been rising more quickly than supply and with...over the forecast period, we expect [unit labor costs] to pick up. At the same time, we think [productivity] is likely to slow...The result is an acceleration [in costs] in the nonfinancial corporate sector over the forecast period."
- MR. STOCKTON (p.9): "The increase in total PCE prices steps up this year and drops back to a 2 percent [rate in 2001]." Core inflation running above target in 2000.

**Center of gravity**: Staff sees inflation clearly above target in 2000, driven by a positive output gap and accelerating unit labor costs, with a projected deceleration only in 2001 as the gap closes. Clearly above 50 but not in a spiral.

**Direction confirmation**: INFLATION_PRESSURE is above neutral because staff quantifies a 3% output gap translating to ~0.6 pp core acceleration, with total PCE above 2% target and expected to stay elevated through 2000.

---

### 2. OUTPUT_GAP

**Score: 67 ±5 | High confidence**

**Evidence**:
- MR. STOCKTON (p.20): "currently we estimate that the level of actual GDP is about 3 percent above the level of potential."
- MR. STOCKTON (p.9): "Domestic spending, which has been rising at more than a 5-1/2 percent pace over the past two years, is expected to increase just 3-1/2 percent in 2001." — substantial above-trend growth leading to deceleration.

**Center of gravity**: A 3% positive output gap is explicitly stated. This is a clear, large positive gap — well above potential, consistent with the late-1990s boom but already expected to narrow. Anchors for this era: 57-63 for late 90s boom; a stated 3% gap pushes to the higher end.

**Direction confirmation**: OUTPUT_GAP is above neutral. "3 percent above the level of potential" is unambiguous. Score of 67 satisfies the BRIGHT-LINE RULE (must be > 50 for above-potential language).

---

### 3. LABOR_TIGHTNESS

**Score: 70 ±5 | High confidence**

**Evidence**:
- MR. STOCKTON (p.9): "Pressures in labor markets are relatively intense over the next year and a half, given our projection of below trend growth [only gradually brings rate down]...but the unemployment rate next year [falls only modestly]."
- MR. STOCKTON (Q&A, p.37): "Our current point estimate [of NAIRU] is...down from the 5-3/4 percent to 6 percent range." Staff puts NAIRU at ~5.25% and current UE "a tiny bit below even the low NAIRU."
- District evidence (MR. STONE, p.51): "labor markets remain very tight. Unemployment rates in the District are now slightly below the national average."
- Era anchor: June 2000, unemployment ~3.9-4.0% nationally. LABOR_TIGHTNESS anchor for 1999-2000 is 65-75.

**Center of gravity**: Unemployment well below NAIRU (estimated ~5.25%), with pervasive labor shortages reported across districts. Very tight labor market at the peak of the boom.

**Direction confirmation**: LABOR_TIGHTNESS is above neutral. Staff explicitly says labor pressures are "relatively intense" and UE is below the NAIRU estimate. Score 70 is consistent with the era anchor (65-75 for 1999-2000).

---

### 4. CONSUMPTION_INVESTMENT

**Score: 62 ±6 | High confidence**

**Evidence**:
- MR. STOCKTON (p.9): "Domestic spending, which has been rising at more than a 5-1/2 percent pace over the past two years..." — extremely strong recent history.
- MR. STOCKTON (p.11): "In contrast to the reasonably clear signs of slowing in residential investment, the recent indicators of capital spending by businesses have remained very strong...new orders for nondefense capital goods moved up in recent months."
- MR. STOCKTON (p.11): Housing starts expected to slide from 1.67 million to ~1.5 million; consumer spending "steady deceleration...this year and next."

**Center of gravity**: Consumer spending decelerating from very high levels, housing clearly weakening, but business equipment/E&S still very strong. The net is still above trend — the deceleration is from an extraordinarily elevated base and the projected level remains robust. Domestic spending projected to slow to 3.5% (still above trend potential growth of ~2.5-3%).

**Direction confirmation**: CONSUMPTION_INVESTMENT is above neutral because the economy has been running at 5.5%+ domestic spending growth. Even the deceleration scenario still projects above-trend spending through 2001.

---

### 5. PRODUCTIVITY

**Score: 65 ±8 | Moderate confidence**

**Evidence**:
- MR. STOCKTON (p.9): "upward productivity growth on 'equilibrium' [interest rate]" — raised the equilibrium rate, reducing the restrictiveness implied by the funds rate.
- MR. STOCKTON (p.21): Productivity discussed in the inflation context — compensation rising faster than productivity in the near term ("demand rising more quickly than supply and with...productivity likely to slow"). However, the *structural* productivity backdrop is elevated.
- MR. STOCKTON (Q&A): "underlying structural productivity growth" described as elevated; NAIRU has been pushed down partly because productivity is higher.
- District evidence (MR. MOSKOW, pp.43-44): Directors report "definite acceleration in productivity in their industries over the past three years as a result of investment in information processing equipment and utilization of the Internet."

**Center of gravity**: Staff has embedded elevated structural productivity growth as the explanation for why the expansion has lasted so long without more inflation. The *level* of productivity growth is seen as above historical trend (the "new economy" thesis). However, in the near-term forecast, staff notes some deceleration of productivity gains (cyclical) as demand is outpacing supply.

**Direction confirmation**: PRODUCTIVITY is above neutral at the structural level — the whole forecast framework is built on above-trend productivity. The near-term cyclical dip is embedded in the cost acceleration story, but the structural view remains elevated.

---

### 6. FINANCIAL_CONDITIONS

**Score: 57 ±6 | High confidence**

**Evidence**:
- MR. STOCKTON (p.9): "We have assumed further tightening of financial conditions to begin to relieve some of the inflationary pressures...The additional tightening...would bring the funds rate a bit above the upper end of the range over the past decade."
- MR. STOCKTON (p.10): "stock prices have risen more than 12 percent over the past year" (offset to tightening) vs. "the model expected a drop of 13 percent over the past year and projects a further decline in coming quarters." — Net: equities still buoyant, partially offsetting rate-driven tightening.
- MR. STOCKTON (p.10): "there is little reason to have expected much restraining effect yet from the change in financial conditions over the past year. But moving forward...the restraining influence of financial conditions should begin to show through more noticeably."

**Center of gravity**: Financial conditions are in the process of tightening — policy has been tightened substantially (rate now "a bit above" historic range), but the stock market resilience has muted the overall tightening of conditions. The net effect is moderately tighter than neutral — not yet restrictive but clearly above the neutral zone.

**Direction confirmation**: FINANCIAL_CONDITIONS is above neutral (tighter than baseline). The funds rate is above the decade's upper range, though offset by equity strength. Score of 57 reflects tighter-than-neutral conditions without full restrictiveness.

---

### 7. TREASURY_STRESS

**Score: N/A**

The staff briefing does not address Treasury market functioning, liquidity, or auction dynamics in any substantive way. The brief pre-meeting discussion about Treasury appears to be about debt management mechanics, not market stress. No language about Treasury market dysfunction, bid-ask spreads, or auction failures.

---

### 8. CREDIT_SPREADS

**Score: 52 ±8 | Low confidence**

**Evidence**:
- MR. STOCKTON (p.9): "expect real rates on corporate bonds to resume the upward trajectory" — suggesting some widening of risk-adjusted rates.
- Go-around (MR. GUYNN, p.48): "more reports of tightening credit standards and more cautious and less accommodative lending."
- MS. JOHNSON (p.17): "foreign private purchases of U.S. securities remain at extraordinary levels" — strong capital inflows suggest credit broadly available internationally.

**Center of gravity**: No explicit credit spread data is discussed. Some tightening of bank lending standards at the margin, but no evidence of significant spread widening. The U.S. was still a highly attractive investment destination. Score near neutral with slight upward bias from the early tightening of bank standards.

**Direction confirmation**: CREDIT_SPREADS is marginally above neutral due to early-stage bank lending tightening, but evidence is thin and indirect.

---

### 9. EQUITY_VALUATION

**Score: 28 ±8 | Moderate confidence**

**Evidence**:
- MR. STOCKTON (p.10): "stock prices have risen more than 12 percent over the past year and are projected to remain flat going forward." — Staff acknowledges equities remain elevated vs. model expectations.
- District go-around (p.51): "A banker noted that he believes the economy is near a turning point...the days of irrational exuberance are over and now we just have exuberance." — Still elevated, merely somewhat less frothy.
- MR. STOCKTON (p.10): The stock market's "resilience...damps considerably the restraining effects that would be expected to accompany a substantial run-up in the funds rate." — Equities providing stimulus, implying elevated valuations.

**Center of gravity**: Staff views equity markets as still elevated (buoyant despite rate increases) — the model's expected correction of 13% had not materialized and prices were above model predictions. This is the dot-com peak period; stocks are described as stretched relative to what rate hikes should have produced.

**Direction confirmation**: EQUITY_VALUATION is below neutral (low stress, high valuation concern). Higher score = more stress/undervaluation. Staff sees equities as elevated/overvalued relative to what fundamentals/rates imply → low score (~28). Era anchor: 15-25 for 2000 dot-com bubble; scores slightly above this range given the Nasdaq had already corrected from March peak.

---

### 10. BANKING_STRESS

**Score: 37 ±8 | Moderate confidence**

**Evidence**:
- Go-around (MR. GUYNN, p.48): "Our financial institutions are telling our lead Bank examiners that their best days in terms of credit quality may be behind them and, consequently, there are more reports of tightening credit standards and more cautious and less accommodative lending."
- Go-around (p.48): "fortunately there seem to be few signs of...stupid competition" and "noticeable pullback in lending to marginal companies."
- No staff briefing content explicitly discusses the banking system's capital adequacy or stress levels.

**Center of gravity**: Banks are healthy — credit quality still good, capital intact — but early-stage caution emerging. The tightening of standards is a normal prudential response, not a sign of stress. Score below 50 consistent with a well-functioning system.

**Direction confirmation**: BANKING_STRESS is below neutral. Language like "best days in credit quality may be behind them" and "tightening standards" suggests very low stress with mild caution. Score of 37 reflects a basically healthy system.

---

### 11. DOLLAR_STRENGTH

**Score: 62 ±7 | High confidence**

**Evidence**:
- MS. JOHNSON (p.13): "the average foreign exchange value of the dollar in terms of the currencies of the other major industrial countries — the black line — has risen on balance so far this year, although it has most recently given back some of that appreciation."
- MS. JOHNSON (p.14): "Through May, the dollar continued its upward trend in terms of the euro." Against yen: "the dollar today is little changed from where it started the year."
- MS. JOHNSON (p.14): Staff expects "the real exchange value of the dollar...will depreciate on balance over the forecast period" — but current description is appreciation.

**Center of gravity**: The dollar has risen on net YTD against the euro (upward trend) and is flat against the yen — net appreciation. The projected future depreciation does not change the current reading. The dollar is **stronger** than at the start of the year.

**Direction confirmation**: DOLLAR_STRENGTH is above neutral. Dollar has "risen on balance so far this year" against major currencies (BRIGHT-LINE RULE met). The score of 62 reflects notable but not extreme appreciation — in the 60-70 zone consistent with a modestly-strong dollar period.

---

### Inflation Sub-Components

**S1. INFLATION_GOODS**

**Score: 47 ±8 | Moderate confidence**

- MS. JOHNSON (p.13): "non-oil import prices provide a favorable backdrop to inflation" (suppressing goods inflation). Core import prices expected to "accelerate to an annual rate of increase of about 3 percent, after experiencing significantly lower increases and even decreases since 1997."
- Dollar appreciation has been holding down import goods prices, but that support is fading as dollar expected to depreciate going forward.
- Currently: goods prices fairly subdued (dollar appreciation offset); forward-looking: turning up. Score just below neutral.

---

**S2. INFLATION_SERVICES**

**Score: N/A**

Services inflation not separately discussed in the staff briefing.

---

**S3. INFLATION_HOUSING**

**Score: 58 ±8 | Moderate confidence**

- MR. STOCKTON (p.11): "rising interest rates and higher home prices have lifted monthly payments relative to personal income over the past year." Housing affordability worsening.
- MR. STOCKTON (p.11): "deterioration in consumer perceptions of home buying conditions...Builders' ratings of new home sales have become less favorable."
- While housing is slowing, prices are still elevated and affordability is impaired. Score modestly above neutral.

---

**S4. INFLATION_EXPECTATIONS**

**Score: N/A**

No specific discussion of survey-based or market-based inflation expectations in the staff briefing.

---

## Part 3: Structured Output

```
MEETING_DATE: 2000-06-28
SOURCE_TYPE: transcript
--- ECONOMIC CONDITIONS ---
INFLATION_PRESSURE: 62
INFLATION_PRESSURE_UNC: +-7
INFLATION_PRESSURE_CONF: High
OUTPUT_GAP: 67
OUTPUT_GAP_UNC: +-5
OUTPUT_GAP_CONF: High
LABOR_TIGHTNESS: 70
LABOR_TIGHTNESS_UNC: +-5
LABOR_TIGHTNESS_CONF: High
CONSUMPTION_INVESTMENT: 62
CONSUMPTION_INVESTMENT_UNC: +-6
CONSUMPTION_INVESTMENT_CONF: High
PRODUCTIVITY: 65
PRODUCTIVITY_UNC: +-8
PRODUCTIVITY_CONF: Moderate
--- FINANCIAL CONDITIONS ---
FINANCIAL_CONDITIONS: 57
FINANCIAL_CONDITIONS_UNC: +-6
FINANCIAL_CONDITIONS_CONF: High
TREASURY_STRESS: N/A
TREASURY_STRESS_UNC: N/A
TREASURY_STRESS_CONF: N/A
CREDIT_SPREADS: 52
CREDIT_SPREADS_UNC: +-8
CREDIT_SPREADS_CONF: Low
EQUITY_VALUATION: 28
EQUITY_VALUATION_UNC: +-8
EQUITY_VALUATION_CONF: Moderate
BANKING_STRESS: 37
BANKING_STRESS_UNC: +-8
BANKING_STRESS_CONF: Moderate
DOLLAR_STRENGTH: 62
DOLLAR_STRENGTH_UNC: +-7
DOLLAR_STRENGTH_CONF: High
--- INFLATION SUB-COMPONENTS (N/A if not discussed) ---
INFLATION_GOODS: 47
INFLATION_SERVICES: N/A
INFLATION_HOUSING: 58
INFLATION_EXPECTATIONS: N/A
--- FLAGS ---
ANOMALY_FLAG: No
ANOMALY_NOTE:
```
