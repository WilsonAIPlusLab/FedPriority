# V4.1.1 clarifications (addendum to the V4.1 rubric; the rubric file itself is unchanged)

These three rules were applied inconsistently by the V4.1 scoring agents. This addendum fixes the reading. It changes no scale, anchor or bright-line rule. Documents scored under it are labelled `v411` in the outputs.

## 1. What counts as a special-topic meeting (Tier 3 and everything else)

A document is **special-topic** only if it contains **neither** (a) a vote or roll call on a monetary policy action (target rate, directive, policy statement, balance-sheet operation) **nor** (b) a go-around or sustained discussion of the policy stance. Typical: a framework, governance, repo-facility or operational session, or a briefing-only conference call.

- Special-topic document: every dimension N/A that the text does not actually support; HAWKISH_DOVISH_LEAN and DISSENT_INTENSITY N/A; ANOMALY_FLAG Yes with a note saying what the meeting was. FINANCIAL_STABILITY_EMPHASIS, FORWARD_GUIDANCE_TONE and UNCERTAINTY_EXPRESSED may be scored if participants say something explicit about them; otherwise N/A.
- A vote on a foreign-exchange swap line or other foreign-currency/lending facility (for example the 1993-95 Mexico swap lines) is **not** a monetary policy action. Such a document is special-topic unless it also has a policy-stance discussion or a policy vote. Record any dissent on the facility vote in ANOMALY_NOTE. (The first agents to score these meetings applied this reading on their own; it is written down here so later runs match.)
- If the document has a policy vote or a stance discussion, it is **not** special-topic, even if it is a short conference call or an emergency meeting: score the Tier 3 dimensions from what was said and the vote record, and give N/A to condition dimensions that no participant discusses.
- A long framework session at the start of an otherwise normal meeting does not make the meeting special-topic; score the normal part and ignore the framework part for the condition dimensions.

## 2. EQUITY_VALUATION

- Participants state a valuation or concern view ("stretched", "rich", "elevated valuations", "froth", "bubble", or "undervalued", "depressed"): score it on the table.
- Participants only report a price move ("equity prices rose / fell") with no valuation view: score 45-55 on the side of the move, CONF Low (this is the rubric's own default).
- Participants mention equities only as a wealth-effect or spending channel, or do not mention them: N/A.

## 3. CREDIT_SPREADS

- A stated level ("elevated", "wide", "historically narrow", "above/below pre-crisis norms") governs the side of 50.
- A spread, yield or risk-premium **direction** only ("spreads narrowed", "widened noticeably"): 45-55 on the side of the move, CONF Low.
- Lending standards, loan terms, credit availability or issuance language **without** any spread, yield or premium wording may support a score, because the dimension is defined as "wider spreads, less availability". Use CONF Low and UNC at least +-10, and say in the evidence that it rests on availability.
- Neither spreads/yields/premiums nor availability/lending/issuance discussed by participants: N/A. Staff or Desk text is never evidence.

## 4. Reading the whole file

The vote record or roll call is at the **end** of the file (a `=== Vote read-out ... ===` block for transcripts, `=== Committee Policy Action (vote record) ===` for minutes). Read to the last line before scoring DISSENT_INTENSITY and the policy lean. One earlier agent reported a missing roll call that was present at the end of a long file.
