# Instructions: blind check of EQUITY_VALUATION and CREDIT_SPREADS on ONE transcript

You score two dimensions, EQUITY_VALUATION and CREDIT_SPREADS, for one FOMC transcript document, from the participants' words alone. You are **not** shown any earlier score for this meeting and must not look for one. This check exists because the first scorers applied the rules for these two dimensions inconsistently; the clarifications now fix the reading.

## Files you may read (only these)
1. The rubric: `<project>\04_scoring\discussion\v4_1\FOMC_Discussion_Review_Prompt_v4_1.md`. Read the sections for EQUITY_VALUATION and CREDIT_SPREADS, the RULES, the BRIGHT-LINE RULES and the EDGE CASES.
2. The clarifications: `<project>\04_scoring\discussion\v4_1_scores\V4_1_1_CLARIFICATIONS.md` (they win where they differ from a looser reading of the rubric; read sections 2 and 3 with care).
3. The INPUT file named in the dispatch message.

Do not open any other file or folder: not the existing analyses, not any score file, not other meetings.

## Reading the input
The input holds every member and participant turn (staff turns removed) and ends with a vote read-out. It can be long (up to about 78,000 words). Read it in chunks **to the last line**. Only participants' words are evidence: staff and Desk text is not in the file and must not be inferred from what you remember about the period. If a passage is garbled, lower confidence and say so.

## What to do
For each of the two dimensions, decide under the clarifications:
- EQUITY_VALUATION: a stated valuation or concern view is scored on the table; a bare price move with no valuation view is 45 to 55 with Low confidence; a wealth-effect or spending-channel mention only, or no mention, is N/A.
- CREDIT_SPREADS: a stated level governs the side of 50; a spread, yield or premium direction only is 45 to 55 on the side of the move with Low confidence; lending standards, terms, availability or issuance language without spread wording may support a score with Low confidence and uncertainty of at least +-10, said in the evidence; neither is N/A.
Quote the participant words (with speaker) that your score rests on. Count how many different participants support the reading, if you can.

## What to write
ONE file at the OUTPUT path:
1. For each dimension, a short paragraph: the quoted words with speaker names, the clarification rule you applied, and the score (or why N/A).
2. A final code block exactly in this shape, `UNC` written as `+-N`, and `N/A` for the value, `_UNC` and `_CONF` when the text does not support a score:

```
MEETING_DATE: <date>
SOURCE_TYPE: discussion
CREDIT_SPREADS: <1-100 or N/A>
CREDIT_SPREADS_UNC: <+-N or N/A>
CREDIT_SPREADS_CONF: <High/Moderate/Low or N/A>
EQUITY_VALUATION: <1-100 or N/A>
EQUITY_VALUATION_UNC: <+-N or N/A>
EQUITY_VALUATION_CONF: <High/Moderate/Low or N/A>
```

## Rules
Valid range 1 to 100, never 0. Do not use outside knowledge of the economy at the time, and do not let the meeting date or what you recall about the meeting override what the text says. Write no scratch files.

## Final reply
At most two sentences: the output path and the two scores.
