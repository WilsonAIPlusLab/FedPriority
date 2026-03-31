# FOMC Staff Assessment Scoring — 2020-07-29
**Rubric version**: FOMC_Staff_Review_Prompt_v4
**Source**: transcript (staff_economic_briefing.txt)
**Scored**: 2026-03-22

---

## Part 1: Thinking Process

### 1. Document type identification

This is a **transcript** from the July 28–29, 2020 FOMC meeting. The document is post-2005 and segmented; the decomposition pipeline identifies a `staff_economic_briefing` component. The briefing is delivered by **MS. MEADE** (Ellen Meade, Senior Special Adviser to the Board, Division of Board Members).

There is no `staff_financial_briefing.txt` or `staff_outlook_briefing.txt` in the source directory. The only other staff content available is `questions_for_staff.txt`, which confirms the procedural context.

### 2. Era context

July 2020: COVID-19 recession. The economy had experienced a catastrophic contraction in Q2 2020 (unemployment peaked above 14% in April, recovering partially by July). The Fed had cut rates to the ELB and launched massive asset-purchase programs. This would normally be a period with deep recession-level scores across economic dimensions.

However, this context is **noted but not used to override the text**, per rubric rules.

### 3. Content assessment — special-topic meeting

The `staff_economic_briefing.txt` is not a standard economic and financial conditions briefing. MS. MEADE's remarks are entirely devoted to presenting and explaining the **Draft Statement on Longer-Run Goals and Monetary Policy Strategy** — the FOMC's framework review document. Her briefing covers:

- The structure and history of the review process
- Paragraph-by-paragraph explanation of the draft consensus statement
- Changes from the 2012 statement (treatment of maximum employment, inflation averaging, ELB language, etc.)

No macroeconomic data, forecasts, or assessments of current economic conditions are presented. There is no Tealbook/Greenbook economic briefing content in this file. The `questions_for_staff.txt` confirms the entire first session of the meeting was the go-round on the strategy statement, not an economic review.

**Ruling**: This meeting qualifies as a **special-topic meeting** under the rubric's edge-case rules. The rubric states explicitly: "Special-topic meetings (balance sheet, framework, operations): These contain no standard economic assessment. Score ALL dimensions as N/A. Flag as anomaly with description of actual topic."

### 4. Polarity verification, bright-line checks, coherence checks

Not applicable — all dimensions are N/A due to the special-topic ruling. No economic or financial content exists to score.

### 5. Staff speakers

- **MS. MEADE** (Ellen Meade): Sole staff presenter; briefing on Draft Statement on Longer-Run Goals and Monetary Policy Strategy
- **CHAIR POWELL**: Provides opening context about the review process (not a staff speaker for scoring purposes)

---

## Part 2: Evidence and Scores

All dimensions are scored N/A because no standard economic assessment is present in this briefing. The content is exclusively a presentation of the draft FOMC consensus statement on longer-run goals and monetary policy strategy.

**Supporting evidence for N/A ruling:**

- MS. MEADE: "I'll be referring to the first pages of the handout 'Material for Briefing on Draft Statement on Longer-Run Goals and Monetary Policy Strategy.'"
- MS. MEADE: Paragraph-by-paragraph walkthrough of the draft statement, covering its treatment of the dual mandate, the ELB challenge, average inflation targeting language, and employment shortfalls — all as framework/strategy content, not real-time assessments.
- CHAIR POWELL (questions_for_staff.txt): "First up today is our discussion of the Statement on Longer-Run Goals and Monetary Policy Strategy... This go-round is the opportunity for you to share your comments on the document and the issues that it addresses."
- No Tealbook, no Greenbook, no economic data, no output gap estimates, no labor market statistics, no financial market conditions discussed anywhere in the briefing.

---

## Part 3: Structured Output

```
MEETING_DATE: 2020-07-29
SOURCE_TYPE: transcript
--- ECONOMIC CONDITIONS ---
INFLATION_PRESSURE: N/A
INFLATION_PRESSURE_UNC: N/A
INFLATION_PRESSURE_CONF: N/A
OUTPUT_GAP: N/A
OUTPUT_GAP_UNC: N/A
OUTPUT_GAP_CONF: N/A
LABOR_TIGHTNESS: N/A
LABOR_TIGHTNESS_UNC: N/A
LABOR_TIGHTNESS_CONF: N/A
CONSUMPTION_INVESTMENT: N/A
CONSUMPTION_INVESTMENT_UNC: N/A
CONSUMPTION_INVESTMENT_CONF: N/A
PRODUCTIVITY: N/A
PRODUCTIVITY_UNC: N/A
PRODUCTIVITY_CONF: N/A
--- FINANCIAL CONDITIONS ---
FINANCIAL_CONDITIONS: N/A
FINANCIAL_CONDITIONS_UNC: N/A
FINANCIAL_CONDITIONS_CONF: N/A
TREASURY_STRESS: N/A
TREASURY_STRESS_UNC: N/A
TREASURY_STRESS_CONF: N/A
CREDIT_SPREADS: N/A
CREDIT_SPREADS_UNC: N/A
CREDIT_SPREADS_CONF: N/A
EQUITY_VALUATION: N/A
EQUITY_VALUATION_UNC: N/A
EQUITY_VALUATION_CONF: N/A
BANKING_STRESS: N/A
BANKING_STRESS_UNC: N/A
BANKING_STRESS_CONF: N/A
DOLLAR_STRENGTH: N/A
DOLLAR_STRENGTH_UNC: N/A
DOLLAR_STRENGTH_CONF: N/A
--- INFLATION SUB-COMPONENTS (N/A if not discussed) ---
INFLATION_GOODS: N/A
INFLATION_SERVICES: N/A
INFLATION_HOUSING: N/A
INFLATION_EXPECTATIONS: N/A
--- FLAGS ---
ANOMALY_FLAG: Yes
ANOMALY_NOTE: Special-topic meeting. The entire first session (July 28) was devoted to discussion of the Draft Statement on Longer-Run Goals and Monetary Policy Strategy (the FOMC framework review). Staff briefer MS. MEADE (Ellen Meade) presented a paragraph-by-paragraph walkthrough of the draft consensus statement covering average inflation targeting, employment shortfalls language, and ELB risk framing. No standard Tealbook economic or financial conditions briefing is present in the transcript. All dimensions scored N/A per rubric special-topic edge-case rule.
```
