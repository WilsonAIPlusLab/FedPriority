# Instructions: score ONE FOMC minutes discussion document fresh, with the v4.1 rubric plus the V4.1.1 clarifications

Same task as `SCORING_INSTRUCTIONS.md` (minutes track) plus the three rules clarified in `V4_1_1_CLARIFICATIONS.md`. The dispatch message gives the meeting date, INPUT path and OUTPUT path. SOURCE_TYPE is `discussion_m`. This is a fresh score of the minutes text, not a patch of any earlier analysis; you are not shown any earlier score.

## Files you may read (only these)
1. The rubric: `<project>\04_scoring\discussion\v4_1\FOMC_Discussion_Review_Prompt_v4_1.md` (follow it exactly, including the three-part output format and the 20 scored dimensions).
2. The clarifications: `<project>\04_scoring\discussion\v4_1_scores\V4_1_1_CLARIFICATIONS.md` (they win where they differ from a looser reading of the rubric).
3. The INPUT file named in the dispatch message.

## What the input contains
The participants'-views text of the minutes, followed by a block headed `=== Committee Policy Action (vote record) ===` holding the directive, the vote ("Votes for / against this action") and any dissent explanation. Use the vote record for DISSENT_INTENSITY and policy lean; staff-reported content is not in the input and must not be inferred. Quantifier language ("all", "most", "many", "several", "some", "a few") carries the weight of agreement. Read the whole file, to the last line. Page markers and the odd garbled PDF character can be ignored; if a passage is garbled so that you cannot tell what was said, lower confidence and say so in ANOMALY_NOTE.

## Output
Write ONE file at the OUTPUT path: Part 1, Part 2 (evidence and scores), Part 3 (the code block). **Part 1 is omitted in this run:** write the single line `Part 1: omitted in this run` and do not write step-by-step reasoning anywhere. Part 2 is a compact evidence list (for each scored dimension: the quoted phrase or phrases with quantifier language, then the score; for each N/A, one short reason). Part 3 is the complete code block. Use exactly the rubric keys, `SOURCE_TYPE: discussion_m`, `UNC` written as `+-N`, N/A lines as `N/A` for value, `_UNC` and `_CONF` (the four inflation sub-components have value only). Valid range 1-100, never 0. State in ANOMALY_NOTE whether you treated the document as special-topic and why.

## Independence rules (strict)
Score this document as if it were the only FOMC document you have ever seen. Do not open any other meeting's scores, analyses or inputs, any CSV of scores, or any other folder. Write no scratch files. Do not use the meeting date or what you recall about the meeting to override what the text says.

## Final reply
At most two sentences: the output path and HAWKISH_DOVISH_LEAN / DISSENT_INTENSITY / UNCERTAINTY_EXPRESSED values, plus any text problem you noticed.
