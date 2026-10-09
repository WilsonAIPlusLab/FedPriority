"""Discussion scoring v4.1 runner (agents score; no API). Two tracks: transcripts (SOURCE_TYPE discussion) and minutes (discussion_m).

  python run_v41.py manifest [--pilot]   enumerate inputs from 03_decomposition/output_rebuild/member_discussion
  python run_v41.py status
  python run_v41.py validate             check every output file's Part 3 (20 scored dims, ranges, N/A rules)
  python run_v41.py next [N]             print up to N undispatched/invalid items, record them in dispatched.txt
  python run_v41.py parse                write all_scores_discussion_v41.csv and all_scores_disc_m_v41.csv (valid files only)
"""
import csv, re, sys, json
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent
SRC = {"transcript": ROOT / "03_decomposition" / "output_rebuild" / "member_discussion_v2" / "transcripts",
       "minutes": ROOT / "03_decomposition" / "output_rebuild" / "member_discussion_v2" / "minutes"}
OUTDIR = {"transcript": HERE / "independent_transcripts", "minutes": HERE / "independent_minutes"}
STYPE = {"transcript": "discussion", "minutes": "discussion_m"}
CSVNAME = {"transcript": "all_scores_discussion_v41.csv", "minutes": "all_scores_disc_m_v41.csv"}
MANIFEST = HERE / "manifest.csv"
LEDGER = HERE / "dispatched.txt"
CAP = 10
PARKED = HERE / "parked_failures.txt"
PILOT_FILE = HERE / "pilot_dates.json"
RUBRIC = ROOT / "04_scoring" / "discussion" / "v4_1" / "FOMC_Discussion_Review_Prompt_v4_1.md"

FULL = ["INFLATION_PRESSURE", "OUTPUT_GAP", "LABOR_TIGHTNESS", "CONSUMPTION_INVESTMENT", "PRODUCTIVITY",
        "FINANCIAL_CONDITIONS", "TREASURY_STRESS", "CREDIT_SPREADS", "EQUITY_VALUATION", "BANKING_STRESS", "DOLLAR_STRENGTH",
        "HAWKISH_DOVISH_LEAN", "DISSENT_INTENSITY", "FINANCIAL_STABILITY_EMPHASIS", "FORWARD_GUIDANCE_TONE", "UNCERTAINTY_EXPRESSED"]
SUBS = ["INFLATION_GOODS", "INFLATION_SERVICES", "INFLATION_HOUSING", "INFLATION_EXPECTATIONS"]
TIER3 = FULL[11:]
COLS = ["MEETING_DATE", "SOURCE_TYPE"] + [c for d in FULL for c in (d, d + "_UNC", d + "_CONF")] + SUBS + ["ANOMALY_FLAG", "ANOMALY_NOTE"]


def manifest(pilot=False):
    rows = []
    for tr, d in SRC.items():
        for p in sorted(d.glob("*.txt")):
            rows.append(dict(track=tr, meeting_date=p.stem, src_path=str(p), output_path=str(OUTDIR[tr] / f"{p.stem}.md"), source_type=STYPE[tr]))
    for d in OUTDIR.values(): d.mkdir(exist_ok=True)
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(len(rows), "items:", {t: sum(r["track"] == t for r in rows) for t in SRC})


def part3(path):
    t = path.read_text(encoding="utf-8")
    m = re.findall(r"```(?:\w*)\s*\n(MEETING_DATE:.*?)```", t, re.DOTALL)
    if not m: return None
    d = {}
    for ln in m[-1].splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("---") and ":" in ln:
            k, _, v = ln.partition(":"); d[k.strip()] = v.strip()
    return d


def check(row):
    """return (data, problems)"""
    p = Path(row["output_path"])
    if not p.exists(): return None, ["missing"]
    d = part3(p)
    if d is None: return None, ["no Part 3 block"]
    pr = []
    if d.get("MEETING_DATE") != row["meeting_date"]: pr.append(f"MEETING_DATE {d.get('MEETING_DATE')}")
    if d.get("SOURCE_TYPE") != row["source_type"]: pr.append(f"SOURCE_TYPE {d.get('SOURCE_TYPE')}")
    anom = d.get("ANOMALY_FLAG") in ("Yes", "No")
    if not anom: pr.append("ANOMALY_FLAG")
    for k in FULL:
        v = d.get(k)
        if v is None: pr.append(f"{k} missing"); continue
        if v == "N/A":
            if d.get(k + "_UNC") != "N/A" or d.get(k + "_CONF") != "N/A": pr.append(f"{k} N/A unc/conf")
            if k in TIER3 and d.get("ANOMALY_FLAG") != "Yes": pr.append(f"{k} N/A without anomaly flag")
            continue
        if not (v.isdigit() and 1 <= int(v) <= 100): pr.append(f"{k} value {v}")
        if not re.fullmatch(r"\+-\d+", d.get(k + "_UNC", "")): pr.append(f"{k}_UNC {d.get(k+'_UNC')}")
        if d.get(k + "_CONF") not in ("High", "Moderate", "Low"): pr.append(f"{k}_CONF {d.get(k+'_CONF')}")
    for k in SUBS:
        v = d.get(k)
        if v is None or not (v == "N/A" or (v.isdigit() and 1 <= int(v) <= 100)): pr.append(f"{k} {v}")
    return d, pr


def load():
    return list(csv.DictReader(open(MANIFEST, encoding="utf-8")))


def status():
    rows = load(); bad = {}; ok = 0
    for r in rows:
        d, pr = check(r)
        if d is not None and not pr: ok += 1
        elif pr != ["missing"]: bad[(r["track"], r["meeting_date"])] = pr
    print(f"valid {ok} / {len(rows)}; invalid-existing {len(bad)}; missing {len(rows)-ok-len(bad)}")
    for k, v in list(bad.items())[:20]: print(" ", k, v[:4])


def nxt(n):
    rows = load()
    if PILOT_FILE.exists():
        pil = set(json.load(open(PILOT_FILE))); rows = [r for r in rows if f"{r['track']}:{r['meeting_date']}" in pil]
    led = set(LEDGER.read_text().split()) if LEDGER.exists() else set()
    parked = {ln.split()[0] for ln in PARKED.read_text().splitlines() if ln.strip()} if PARKED.exists() else set()
    todo = []
    for r in rows:
        key = f"{r['track']}:{r['meeting_date']}"
        d, pr = check(r)
        if d is not None and not pr: continue
        if key in led or key in parked: continue  # in flight, finished-invalid (inspect by hand) or parked
        todo.append((key, r))
    inflight = sum(1 for k, r in ((f"{r['track']}:{r['meeting_date']}", r) for r in rows) if k in led and k not in parked and check(r)[0] is None)
    n = max(0, min(n, CAP - inflight))
    print(f"in flight (ledgered, no output): {inflight}; launching {n}")
    pick = todo[:n]
    with open(LEDGER, "a") as f:
        for k, _ in pick: f.write(k + "\n")
    for k, r in pick: print(k)
    print("remaining after this batch:", len(todo) - len(pick))


def parse():
    rows = load(); out = {t: [] for t in SRC}
    for r in rows:
        d, pr = check(r)
        if d is None or pr: continue
        out[r["track"]].append({c: d.get(c, "") for c in COLS})
    for t, rs in out.items():
        rs.sort(key=lambda x: x["MEETING_DATE"])
        with open(HERE / CSVNAME[t], "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rs)
        print(t, len(rs), "rows ->", CSVNAME[t])


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "manifest": manifest()
    elif c == "status": status()
    elif c == "validate": status()
    elif c == "next": nxt(int(sys.argv[2]) if len(sys.argv) > 2 else 8)
    elif c == "parse": parse()
    elif c == "reset-stale":
        rows = load(); led = LEDGER.read_text().split() if LEDGER.exists() else []
        keep = [k for k in led if check(next(r for r in rows if f"{r['track']}:{r['meeting_date']}" == k))[1] != ["missing"]]
        LEDGER.write_text(chr(10).join(keep) + chr(10)); print("ledger", len(led), "->", len(keep))
    else: print(__doc__)
