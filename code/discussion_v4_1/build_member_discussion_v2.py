"""Member-discussion inputs v2 (discussion track), built from the verified output_rebuild text.

Why v2: the first-pass extractors (extract_*_discussion.py) have defects found by the V4.1 pilot agents:
  * Transcripts: go-around start is chosen by heuristic (e.g. 2007-10-31 starts at turn 221 of 290, 3,245 words kept;
    2010-03-16 keeps 144 words) and the parser misses mixed-case labels such as 'MR. McANDREWS.'.
  * Minutes: paragraph_start() looks for a blank line, which in PDF-era text occurs only at page breaks, so starts include
    staff text from the previous page and ends drop up to a page of discussion (e.g. 2015-12-16 loses the forward-guidance
    paragraph, 2008-10-29 stops mid-word at 'facili-'). The vote record is also cut off, so dissents are invisible.

v2 definition (a construct change -- state it wherever results are quoted):
  * Transcripts: ALL turns by FOMC members/participants (Chair, Vice Chair, governors, presidents) in the meeting, in order,
    with speaker labels; staff, Secretary and counsel turns are removed. Member identity uses the roster logic of
    04_scoring/staff/build_staff_combined_v2.py (go-around headers, chair titles, go-around span rule). Includes members'
    questions during staff Q&A and the vote read-out; no go-around/policy segmentation heuristics.
  * Minutes: from the first participants'-discussion phrase (sentence start) to the policy-action marker, then a clearly
    labelled 'Committee Policy Action (vote record)' block (directive, 'Voting for/against', dissent explanations) up to the
    next section marker or 30,000 characters.
Writes output_rebuild/member_discussion_v2/{transcripts,minutes}/<date>.txt and member_discussion_v2/QA.csv. Never modifies other files.
"""
import csv, re, sys, collections
from pathlib import Path
from datetime import date as _D

HERE = Path(__file__).resolve().parent
RB = HERE.parent / "output_rebuild"
import os
OUT = RB / os.environ.get("FOMC_V2_OUT", "member_discussion_v2")
sys.path.insert(0, str(HERE))
from config import MINUTES_TRANSITION_PHRASES as MTP  # noqa: E402

HDR = re.compile(r"^(CHAIRMAN|VICE CHAIRMAN|CHAIR|VICE CHAIR|MR\.|MS\.|MRS\.|DR\.)\s+"
                 r"([A-Z][A-Za-z'\-]+(?:\s[A-Z][A-Za-z'\-]+)?)\d*\.\s*(.*)$")
GA_HDR = re.compile(r"SPEAKER:\s*([^|]+)\|")
PAGE_MARK = re.compile(r"^---\s*PAGE\s+\d+\s*---\s*$")
FOOTER = re.compile(r"^(?:(?:January|February|March|April|May|June|July|August|September|October|November|December)"
                    r"\s+\d{1,2}(?:\s*[–-]\s*\d{1,2})?,\s+\d{4}\s+)?\d+\s+of\s+\d+\s*$")
ROLL = re.compile(r"(?:Chairman|Vice Chairman|Chair|President|Governor|Mr\.|Ms\.|Mrs\.|Dr\.)\s+[A-Z][A-Za-z'\-]+\s+(?:Yes|No|Aye|Nay)\b")
FVP = re.compile(r"(?:First Vice President|Acting President)\s+(?:and [A-Za-z ]{2,40}?\s+)?([A-Z][A-Za-z'\-]+)")
TITLES = ("CHAIRMAN", "VICE CHAIRMAN", "CHAIR", "VICE CHAIR")
STAFF_BEFORE = {"KOHN": "2002-07-31", "DUDLEY": "2008-12-31", "FISHER": "2001-12-31", "WILLIAMS": "2005-12-31", "BOWMAN": "2018-10-31"}
STAFF_AFTER = {"MEYER": "2002-06-30"}  # Laurence Meyer was a governor until early 2002; a later Mr. Meyer is Board staff


def last(name):
    toks = re.sub(r"\d+$", "", name.strip()).split()
    toks = [t for t in toks if t.lower().strip(".") not in ("mr", "ms", "mrs", "dr", "chairman", "chair", "vice")]
    return re.sub(r"[^A-Za-z'\-]", "", toks[-1]).upper() if toks else ""


def parse_turns(text):
    turns, cur = [], None
    for line in text.splitlines():
        s = line.strip()
        if PAGE_MARK.match(s) or FOOTER.match(s):
            continue
        m = HDR.match(s)
        if m:
            cur = {"label": f"{m.group(1).upper()} {re.sub(chr(92)+'d+$', '', m.group(2).strip()).upper()}",
                   "title": m.group(1).upper(), "speaker": last(m.group(2)), "lines": [m.group(3)]}
            turns.append(cur)
        elif cur is not None:
            cur["lines"].append(s)
    for t in turns:
        t["text"] = re.sub(r"[ \t]+", " ", "\n".join(t["lines"])).strip()
    return turns


def build_transcripts():
    dates = sorted(p.name for p in (RB / "transcripts").iterdir() if p.is_dir())
    ga_sets = {}
    for d in dates:
        g = RB / "transcripts" / d / "go_around_combined.txt"
        ga_sets[d] = ({last(x) for x in GA_HDR.findall(g.read_text(encoding="utf-8", errors="replace"))} if g.exists() else set())
    spans = {}
    for d in dates:
        for nm in ga_sets[d]:
            lo, hi = spans.get(nm, (d, d)); spans[nm] = (min(lo, d), max(hi, d))
    gap = lambda a, b: abs((_D.fromisoformat(a) - _D.fromisoformat(b)).days)
    all_ga = set().union(*ga_sets.values())
    od = OUT / "transcripts"; od.mkdir(parents=True, exist_ok=True)
    qa = []
    for d in dates:
        base = RB / "transcripts" / d
        full = (base / "_full_text.txt").read_text(encoding="utf-8", errors="replace")
        turns = parse_turns(full)
        members = set(ga_sets[d]) | {t["speaker"] for t in turns if t["title"] in TITLES}
        members |= {nm for nm, (lo, hi) in spans.items() if (lo <= d and gap(d, hi) <= 120) or (lo <= d <= hi)}
        members |= {last(x) for x in FVP.findall(full)}  # first VPs / acting presidents sit as participants; the Chair introduces them by title
        members -= {sp for sp, cut in STAFF_BEFORE.items() if d <= cut} | {sp for sp, cut in STAFF_AFTER.items() if d > cut}  # staff-before-membership cutoffs also override go-around/span membership
        keep, mw, sw, roll = [], 0, 0, []
        for t in turns:
            is_member = t["speaker"] in members or (t["speaker"] in all_ga and not (t["speaker"] in STAFF_BEFORE and d <= STAFF_BEFORE[t["speaker"]]) and not (t["speaker"] in STAFF_AFTER and d > STAFF_AFTER[t["speaker"]]))
            if is_member and t["text"]:
                keep.append(f"{t['label']}.\n{t['text']}"); mw += len(t["text"].split())
            else:
                sw += len(t["text"].split())
                if len(ROLL.findall(t["text"])) >= 4:
                    roll.append(t["text"])
        if roll:
            keep.append("=== Vote read-out (roll call read by the Secretary; other staff speech removed) ===\n" + "\n\n".join(roll))
        (od / f"{d}.txt").write_text("\n\n".join(keep) + "\n", encoding="utf-8")
        total = len(full.split())
        qa.append(dict(track="transcript", meeting_date=d, words=mw, other_words=sw, full_words=total,
                       share=round(mw / total, 3) if total else 0, n_turns=len(keep), roll_call=int(bool(roll)), n_member_speakers=len({t['speaker'] for t in turns if t['speaker'] in members})))
    return qa


# ---- minutes ----
_APO = r"['’\x92]"
TIER1 = [r"In (?:their|the Committee" + r"['’]" + r"s) (?:review|discussion|assessment|evaluation)s? of (?:the )?(?:current|economic|prospective)",
         r"In their discussion of the economic situation", r"In their discussion of the economic and financial situation",
         r"In their discussion of the economic outlook", r"In the Committee" + _APO + r"s discussion of current and prospective economic developments",
         r"In the Committee" + _APO + r"s discussion of current and prospective", r"In the Committee" + _APO + r"s discussion of economic conditions"]
TIER2 = [r"In their discussion", r"In the Committee" + _APO + r"s discussion", r"Participants observed", r"Members noted", r"Participants noted",
         r"Members discussed", r"Participants discussed", r"In the discussion of economic conditions"]
POLICY_MARK = MTP["policy_action"] + [r"Votes? for this action", r"Voting for this action", r"The vote encompassed", r"By unanimous vote, the Committee (?:approved|voted)"]
BLOCK_END = [r"\n\s*Notation Votes?\b", r"It was agreed that the next meeting", r"\n\s*Summary of Economic Projections", r"The meeting adjourned",
             r"\n\s*Developments in Financial Markets and the Management of the System", r"\n\s*Conference Call"]


def earliest(text, pats, after=0):
    best = None
    for p in pats:
        try:
            m = re.search(p, text[after:], re.I)
        except re.error:
            continue
        if m and (best is None or after + m.start() < best):
            best = after + m.start()
    return best


def build_minutes():
    od = OUT / "minutes"; od.mkdir(parents=True, exist_ok=True)
    qa = []
    for p in sorted((RB / "minutes").iterdir()):
        if not p.is_dir(): continue
        d = p.name
        text = (p / "_full_text.txt").read_text(encoding="utf-8", errors="replace")
        pv, pa = p / "participants_views.txt", p / "policy_action.txt"
        if pv.exists() and pa.exists() and len(pv.read_text(encoding="utf-8", errors="replace").split()) >= 500:
            a = pv.read_text(encoding="utf-8", errors="replace").strip(); b = pa.read_text(encoding="utf-8", errors="replace").strip()
            (od / f"{d}.txt").write_text(a + "\n\n=== Committee Policy Action (vote record) ===\n\n" + b + "\n", encoding="utf-8")
            qa.append(dict(track="minutes", meeting_date=d, words=len(a.split()), block_words=len(b.split()), full_words=len(text.split()),
                           flag="segmented" + ("" if re.search(r"Voting against|Votes against", b, re.I) else ";no_voting_against")))
            continue
        s = earliest(text, TIER1)
        if s is None:
            stf = [m.start() for ph in MTP.get("staff_economic_review", []) + MTP.get("staff_financial_review", []) + MTP.get("staff_outlook", [])
                   for m in [re.search(ph, text, re.I)] if m]
            s = earliest(text, TIER2, after=min(stf) if stf else 0)
        if s is None:
            qa.append(dict(track="minutes", meeting_date=d, words=0, flag="no_start_phrase")); continue
        e = earliest(text, POLICY_MARK, after=s + 100)
        member = text[s:e] if e else text[s:]
        block = ""
        if e:
            b_end = earliest(text, BLOCK_END, after=e + 50)
            block = text[e:min(b_end if b_end else len(text), e + 30000)]
        out = member.strip() + (f"\n\n=== Committee Policy Action (vote record) ===\n\n{block.strip()}" if block.strip() else "")
        (od / f"{d}.txt").write_text(out + "\n", encoding="utf-8")
        flag = "" if e else "no_policy_marker"
        if re.search(r"Voting against|Votes against", block, re.I) is None and block: flag = (flag + ";no_voting_against").strip(";")
        qa.append(dict(track="minutes", meeting_date=d, words=len(member.split()), block_words=len(block.split()), full_words=len(text.split()), flag=flag))
    return qa


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    qa = build_transcripts() + build_minutes()
    keys = ["track", "meeting_date", "words", "other_words", "block_words", "full_words", "share", "n_turns", "roll_call", "n_member_speakers", "flag"]
    with open(OUT / "QA.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(qa)
    print(len(qa), "rows")
