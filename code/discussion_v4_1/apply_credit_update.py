"""User decision 2026-10-08: apply the V4.1.1 CREDIT_SPREADS re-check to the first-run transcript cells that were N/A.

Source of new values: the blind check outputs in transcript_check/, transcript_check_b/, transcript_check_c/ (27 cells where the first run
gave CREDIT_SPREADS = N/A; 16 now score, all Low confidence; 11 stay N/A and are left unchanged).
Writes a NEW table (all_scores_discussion_v411_creditupd.csv) and a change log; the input table is not modified.
Only the three CREDIT_SPREADS fields change; the extra column CREDIT_UPDATE marks the rows touched. Nothing else in a row is changed
(including SCORE_VERSION, which describes the run that produced the other 19 dimensions).
"""
import csv, hashlib, importlib.util
from pathlib import Path

H = Path(__file__).parent
SRC = H / "all_scores_discussion_v411.csv"
OUT = H / "all_scores_discussion_v411_creditupd.csv"
LOGP = H / "credit_update_log.csv"
before = hashlib.sha256(SRC.read_bytes()).hexdigest()

rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
cols = list(rows[0].keys()) + ["CREDIT_UPDATE"]
byd = {r["MEETING_DATE"]: r for r in rows}

new = {}
for f in ("transcript_check", "transcript_check_b", "transcript_check_c"):
    spec = importlib.util.spec_from_file_location("cr_" + f, H / f / "check_runner.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    orig = {r["meeting_date"]: r for r in csv.DictReader(open(H / f / "original_values_PRIVATE.csv", encoding="utf-8"))}
    for r in m.rows():
        d = r["meeting_date"]
        if orig[d]["CREDIT_SPREADS"] == "N/A":
            p = m.parse(r)
            new[d] = dict(batch=f, words=r["words"], value=p["CREDIT_SPREADS"], unc=p["CREDIT_SPREADS_UNC"], conf=p["CREDIT_SPREADS_CONF"])
assert len(new) == 27, len(new)

for r in rows:
    r["CREDIT_UPDATE"] = ""
log = []
for d, n in sorted(new.items()):
    r = byd[d]
    assert r["CREDIT_SPREADS"] == "N/A" and r["SCORE_VERSION"] == "v41_v2", (d, r["CREDIT_SPREADS"], r["SCORE_VERSION"])
    if not n["value"].isdigit():
        log.append(dict(meeting_date=d, input_words=n["words"], batch=n["batch"], action="kept N/A", old="N/A", new="N/A", unc="N/A", conf="N/A"))
        continue
    assert n["conf"] == "Low" and n["unc"].startswith("+-"), (d, n)
    r["CREDIT_SPREADS"], r["CREDIT_SPREADS_UNC"], r["CREDIT_SPREADS_CONF"] = n["value"], n["unc"], n["conf"]
    r["CREDIT_UPDATE"] = "v411_blind_check_2026-10-08"
    log.append(dict(meeting_date=d, input_words=n["words"], batch=n["batch"], action="N/A -> scored", old="N/A", new=n["value"], unc=n["unc"], conf=n["conf"]))

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
with open(LOGP, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(log[0])); w.writeheader(); w.writerows(log)
assert hashlib.sha256(SRC.read_bytes()).hexdigest() == before

# verification: exactly 16 cells x 3 fields + the marker differ from the source, nothing else
a = {(r["MEETING_DATE"], c): r[c] for r in csv.DictReader(open(SRC, encoding="utf-8")) for c in cols[:-1]}
b = {(r["MEETING_DATE"], c): r[c] for r in csv.DictReader(open(OUT, encoding="utf-8")) for c in cols[:-1]}
diff = [k for k in a if a[k] != b[k]]
changed = sum(l["action"] == "N/A -> scored" for l in log)
assert len(diff) == 3 * changed and all(k[1].startswith("CREDIT_SPREADS") for k in diff), len(diff)
na_left = sum(r["CREDIT_SPREADS"] == "N/A" for r in rows)
print(f"{changed} cells updated, {len(log) - changed} kept N/A; {len(diff)} field changes; {len(rows)} rows; CREDIT_SPREADS N/A now {na_left} of {len(rows)}")
