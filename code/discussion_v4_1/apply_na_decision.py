"""User decision 2026-10-07: set the 36 patched minutes cells that the blind second pass scored N/A to N/A.
Writes a NEW table; the patched table from the first run is left untouched."""
import csv, hashlib
from pathlib import Path
H = Path(__file__).parent
SRC = H / "minutes_patch" / "all_scores_disc_m_v41_patched.csv"
OUT = H / "minutes_patch" / "all_scores_disc_m_v411_patched.csv"
LOGP = H / "minutes_patch" / "na_decision_log.csv"
before = hashlib.sha256(SRC.read_bytes()).hexdigest()
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
cols = list(rows[0].keys())
byd = {r["MEETING_DATE"]: r for r in rows}
targets = [r for r in csv.DictReader(open(H / "second_pass_vs_patched.csv", encoding="utf-8"))
           if r["category"] == "patched_value__second_NA"]
assert len(targets) == 36, len(targets)
log = []
for t in targets:
    r = byd[t["meeting_date"]]; d = t["dimension"]
    assert r[d].isdigit() and r[d] == t["patched"], (t["meeting_date"], d, r[d])
    old = (r[d], r.get(d + "_UNC", ""), r.get(d + "_CONF", ""))
    r[d] = "N/A"
    if d + "_UNC" in r: r[d + "_UNC"] = "N/A"
    if d + "_CONF" in r: r[d + "_CONF"] = "N/A"
    log.append(dict(meeting_date=t["meeting_date"], dimension=d, old_value=old[0], old_unc=old[1], old_conf=old[2],
                    patch_status=t["patch_status"], reason="user decision: blind second pass scored N/A"))
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
with open(LOGP, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(log[0])); w.writeheader(); w.writerows(log)
assert hashlib.sha256(SRC.read_bytes()).hexdigest() == before
# verify: exactly 36 cells differ
a = {(r["MEETING_DATE"], c): r[c] for r in csv.DictReader(open(SRC, encoding="utf-8")) for c in cols}
b = {(r["MEETING_DATE"], c): r[c] for r in csv.DictReader(open(OUT, encoding="utf-8")) for c in cols}
dv = [k for k in a if a[k] != b[k]]
print(len(log), "cells set to N/A;", len(dv), "field changes (value+UNC+CONF);", len(rows), "rows")
import collections
print(collections.Counter(l["dimension"] for l in log), collections.Counter(l["patch_status"] for l in log))
