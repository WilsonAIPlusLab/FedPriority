---
title: "FOMC Meeting Registry — meeting_registry.csv"
version: 1.0
created: 2026-03-30
source_file: data/primary/meeting_registry.csv
---

## Overview

This file is the master list of all FOMC meetings in the dataset. It records the basic administrative and contextual attributes of each meeting: date, type, presiding chair, available source documents, the policy decision taken, and any notable contextual information. It serves as the authoritative joining key for all other dataset files — staff_scores_v4.csv and discussion_scores_v3.csv both key on MEETING_DATE. The registry covers meetings from 1993 onward, including regularly scheduled meetings, intermeeting conference calls, and unscheduled emergency actions. It distinguishes between meetings that produced scoreable documents (full transcripts or minutes) and those for which only limited records exist (e.g., conference call transcripts without a corresponding economic briefing).

## Unit of Observation

One row = one FOMC meeting or formal action, identified by meeting_date. Conference calls and intermeeting actions appear as separate rows from the surrounding scheduled meetings.

## Variable Definitions

| Variable | Type | Valid Values | Description |
|----------|------|--------------|-------------|
| meeting_date | Date (ISO 8601) | YYYY-MM-DD | The date on which the meeting or conference call began. For multi-day meetings, this is the first day. Primary key for the registry and the join key for all score files. |
| end_date | Date (ISO 8601) | YYYY-MM-DD or empty | The closing date for multi-day scheduled meetings (e.g., a two-day meeting that begins on a Tuesday and ends on a Wednesday carries the Wednesday date here). Empty for single-day meetings and conference calls, in which case meeting_date is both start and end. Researchers computing meeting duration should treat empty end_date as equivalent to meeting_date. |
| meeting_type | Categorical | `scheduled`, `unscheduled`, `conference_call` | The formal classification of the meeting. `scheduled` = one of the eight (historically fewer) regularly scheduled FOMC meetings in the annual calendar. `unscheduled` = an emergency or ad hoc in-person meeting called outside the regular schedule. `conference_call` = an intermeeting conference call, which may have produced only a brief record or a full transcript depending on the era and purpose. Conference calls rarely include a full economic briefing and are commonly N/A across most scoring dimensions. |
| chair | Categorical | `Greenspan`, `Bernanke`, `Yellen`, `Powell` | The Federal Reserve Chair presiding at the time of the meeting. In this dataset (1993–2026): Alan Greenspan (1993–2006), Ben Bernanke (2006–2014), Janet Yellen (2014–2018), Jerome Powell (2018–2026). Note that meetings at chair transitions may bear the outgoing or incoming chair depending on the exact date. |
| documents_found | String | Free text (comma-separated document types) | The source documents actually located and ingested for this meeting. Common values: `minutes,transcript` (both available); `minutes` (transcript not yet declassified or not ingested); `transcript` (minutes not separately ingested); `confcall_transcript` (conference call transcript only); empty (no scoreable document found). This field is a free-text string enumerating document types, not a count. |
| documents_expected | String | Free text (comma-separated document types) | The source documents that would be expected for a meeting of this type based on standard FOMC practice. For scheduled meetings, both minutes and transcript are expected (transcript after the five-year declassification lag). For conference calls, only a conference call transcript is expected. Differences between documents_found and documents_expected indicate gaps in coverage. |
| rate_decision | String | Free text or empty | A human-readable description of the federal funds rate action taken at or immediately following the meeting. Common formats include the basis-point change ("25bp hike," "50bp cut," "no change"), a word description ("held steady," "emergency 100bp cut"), or an indication that no rate decision was made (for informational conference calls). Empty when no action was taken or when the record is incomplete. |
| target_rate | Numeric | Percentage (%) or empty | The federal funds rate target (or target range midpoint) established as a result of this meeting, expressed as a percentage. For pre-corridor-system meetings, this is the single target rate. For meetings after the adoption of the target range (post-2008), this reflects the midpoint of the range or the upper bound depending on convention in the source data. Empty when no rate decision was made or when the historical record does not specify a numeric target. |
| special_notes | String | Free text or empty | Any anomalies, unusual context, or notable features of the meeting that are not captured by the other fields. Examples include: notation that a meeting was called in response to a specific crisis event (9/11 attacks, Lehman failure, COVID-19 onset), notation that the economic briefing was abbreviated or omitted, notation of a policy framework review, or notation of a simultaneous intermeeting action. Empty for routine meetings with no notable features. |

---

## Notes

1. **Primary key**: meeting_date is the primary key and is assumed unique within this file. When joining to staff_scores_v4.csv or discussion_scores_v3.csv, join on meeting_date; the score files add SOURCE_TYPE as a second key dimension.

2. **documents_found vs. documents_expected**: The difference between these two fields is the primary indicator of coverage gaps. Researchers analyzing the full 1993–present span should note that transcripts have a five-year declassification lag, so recent meetings will show `minutes` in documents_found but `minutes,transcript` in documents_expected. Meetings with empty documents_found had no scoreable content and will have no corresponding rows in the score files.

3. **Conference calls**: Most conference calls did not include a Tealbook economic briefing or a structured participant go-around. As a result, conference call rows in meeting_registry.csv typically have no corresponding rows in staff_scores_v4.csv, and any rows in discussion_scores_v3.csv will show N/A for most dimensions. The meeting_type = `conference_call` flag is the cleanest way to identify and exclude these from continuous time-series analyses.

4. **Chair field precision**: The chair variable reflects the presiding chair at the time of the meeting. It does not capture acting chairs, vice chairs presiding in the chair's absence, or cases where a new chair's first meeting was the final day of a two-day meeting that began under the previous chair. For precision analyses near transition dates, consult the special_notes field.

5. **target_rate empty cells**: The target_rate field is empty for conference calls that did not result in a rate action, for informational meetings, and for early meetings where the specific numeric target was not recorded in the source. An empty target_rate should not be interpreted as a rate of zero.

6. **rate_decision text format**: The rate_decision field is a free-text string and is not standardized to a fixed vocabulary. Researchers who need a numeric or categorical rate decision variable should parse this field or construct the variable from target_rate differences between consecutive rows.

7. **Multi-day meeting end_date**: The majority of scheduled meetings in the modern era (post-1994) are two-day meetings. The end_date field is populated for these. Pre-1994 scheduled meetings were typically one-day; end_date will be empty for those rows.
