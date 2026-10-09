"""Minutes patch runner: manifest | status | next [N] | verify-originals.
State comes from files. An output is valid when its Part 3 passes run_v41.check (20 dims, SOURCE_TYPE discussion_m), a Revision Log with
20 dimension rows exists, every dimension logged UNCHANGED has the same value/UNC/CONF in Part 3 as in the existing analysis, and
none of the five new dimensions is logged UNCHANGED."""
import csv, re, sys, hashlib, json
from pathlib import Path

HERE = Path(__file__).parent
V41 = HERE.parent
sys.path.insert(0, str(V41))
import run_v41 as R

ROOT = HERE.parents[3]
OLD = ROOT / "04_scoring" / "discussion" / "v4_scores_minutes" / "independent"
NEW = ROOT / "03_decomposition" / "output_rebuild" / "member_discussion_v2" / "minutes"
OUT = HERE / "patched"
DIFF = HERE / "textdiff"
MAN = HERE / "patch_manifest.csv"
LED = HERE / "patch_dispatched.txt"
HASH = HERE / "originals_sha256.json"
CAP = 10
OLD15 = R.FULL[:11] + R.SUBS
ALL20 = R.FULL + R.SUBS


def manifest():
    OUT.mkdir(exist_ok=True)
    rows = []
    for p in sorted(NEW.glob("*.txt")):
        d = p.stem
        rows.append(dict(meeting_date=d, old=str(OLD / f"{d}.md"), new=str(p), textdiff=str(DIFF / f"{d}.txt"), output=str(OUT / f"{d}.md")))
    with open(MAN, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    h = {r["meeting_date"]: hashlib.sha256(Path(r["old"]).read_bytes()).hexdigest() for r in rows if Path(r["old"]).exists()}
    if not HASH.exists():
        json.dump(h, open(HASH, "w"))
    print(len(rows), "meetings;", len(h), "originals hashed;", [r["meeting_date"] for r in rows if not Path(r["old"]).exists()], "have no original")


def load():
    return list(csv.DictReader(open(MAN, encoding="utf-8")))


def check(r):
    p = Path(r["output"])
    if not p.exists():
        return None, ["missing"]
    d = R.part3(p)
    if d is None:
        return None, ["no Part 3 block"]
    pr = []
    row = dict(track="minutes", meeting_date=r["meeting_date"], source_type="discussion_m", output_path=r["output"])
    _, p2 = R.check(row)
    pr += [x for x in p2 if x != "missing"]
    t = p.read_text(encoding="utf-8")
    m = re.search(r"##\s*Revision Log(.*?)(?=\n##\s|\Z)", t, re.S | re.I)
    log = {}
    if not m:
        pr.append("no Revision Log")
    else:
        for ln in m.group(1).splitlines():
            c = [x.strip().strip("`") for x in ln.strip().strip("|").split("|")]
            if len(c) >= 3 and c[0] in ALL20:
                log[c[0]] = c[1].upper()
        if len(log) != 20:
            pr.append(f"Revision Log has {len(log)}/20 dimension rows")
    ov = R.part3(Path(r["old"])) or {}
    for k in OLD15:
        if log.get(k) == "UNCHANGED" and ov:
            for suf in (("",) if k in R.SUBS else ("", "_UNC", "_CONF")):
                if d.get(k + suf) != ov.get(k + suf):
                    pr.append(f"{k}{suf} marked UNCHANGED but differs from original")
    for k in R.TIER3:
        if log.get(k) == "UNCHANGED":
            pr.append(f"{k} cannot be UNCHANGED (new dimension)")
    return (d, log), pr


def status():
    rows = load()
    ok = 0
    bad = {}
    counts = {"UNCHANGED": 0, "FILLED": 0, "CORRECTED": 0}
    for r in rows:
        res, pr = check(r)
        if res is not None and not pr:
            ok += 1
            for v in res[1].values():
                counts[v] = counts.get(v, 0) + 1
        elif pr != ["missing"]:
            bad[r["meeting_date"]] = pr
    print(f"valid {ok}/{len(rows)}; invalid-existing {len(bad)}; missing {len(rows) - ok - len(bad)}; status counts over valid files {counts}")
    for k, v in list(bad.items())[:15]:
        print(" ", k, v[:3])


def nxt(n):
    rows = load()
    led = set(LED.read_text().split()) if LED.exists() else set()
    infl = sum(1 for r in rows if r["meeting_date"] in led and check(r)[0] is None)
    n = max(0, min(n, CAP - infl))
    todo = [r for r in rows if r["meeting_date"] not in led and check(r)[0] is None]
    pick = todo[:n]
    with open(LED, "a") as f:
        for r in pick:
            f.write(r["meeting_date"] + "\n")
    print(f"in flight {infl}; launching {n}")
    for r in pick:
        print(r["meeting_date"])
    print("remaining after this batch:", len(todo) - len(pick))


def verify_originals():
    h = json.load(open(HASH))
    bad = [d for d, s in h.items() if hashlib.sha256((OLD / f"{d}.md").read_bytes()).hexdigest() != s]
    print("originals modified:", bad or "none")


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "manifest":
        manifest()
    elif c == "status":
        status()
    elif c == "next":
        nxt(int(sys.argv[2]) if len(sys.argv) > 2 else 8)
    elif c == "verify-originals":
        verify_originals()
    else:
        print(__doc__)
