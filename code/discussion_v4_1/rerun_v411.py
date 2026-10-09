"""Queue runner for the 2026-10-07 follow-up: transcript re-scores (T) and blind second-pass minutes cells (S).

  python rerun_v411.py build     write rerun_manifest.csv
  python rerun_v411.py status    valid / invalid / missing per queue
  python rerun_v411.py next N    ledger up to N undone items (cap 10 in flight over both queues) and print dispatch details

T items: full V4.1 + V4.1.1 re-score of a transcript from member_discussion_v2b -> independent_transcripts_v2b/<date>.md
S items: blind second pass of listed dimensions of one minutes document -> second_pass/<date>.md
State is read from files; an item is done when its output passes the check.
"""
import csv, json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_v41 as R

ROOT = HERE.parents[2]
V2B_T = ROOT / "03_decomposition" / "output_rebuild" / "member_discussion_v2b" / "transcripts"
V2_M = ROOT / "03_decomposition" / "output_rebuild" / "member_discussion_v2" / "minutes"
OUT_T = HERE / "independent_transcripts_v2b"
OUT_S = HERE / "second_pass"
MAN = HERE / "rerun_manifest.csv"
LED = HERE / "rerun_dispatched.txt"
CAP = 10
OPUS = {"1994-03-24", "2010-11-03", "2015-04-29", "2015-09-17"}  # parked after two failed Sonnet runs; retried on another model


def build():
    OUT_T.mkdir(exist_ok=True); OUT_S.mkdir(exist_ok=True)
    changed = set((HERE / "v2b_changed_transcripts.txt").read_text().split())
    allna = {r["MEETING_DATE"] for r in csv.DictReader(open(HERE / "all_scores_discussion_v41.csv", encoding="utf-8"))
             if r["HAWKISH_DOVISH_LEAN"] == "N/A"}
    tset = sorted(changed | allna | OPUS)
    rows = []
    for d in tset:
        why = [w for w, s in (("fvp_fix", changed), ("special_topic_rule", allna), ("parked", OPUS)) if d in s]
        rows.append(dict(kind="T", meeting_date=d, input=str(V2B_T / f"{d}.txt"), output=str(OUT_T / f"{d}.md"),
                         dims="ALL", model="opus" if d in OPUS else "sonnet", why="+".join(why)))
    tg = json.load(open(HERE / "minutes_patch" / "second_pass_targets.json"))
    for d, dims in tg.items():
        rows.append(dict(kind="S", meeting_date=d, input=str(V2_M / f"{d}.txt"), output=str(OUT_S / f"{d}.md"),
                         dims=",".join(dims), model="sonnet", why="second_pass"))
    with open(MAN, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(len(rows), "items:", {k: sum(r["kind"] == k for r in rows) for k in "TS"})


def load():
    return list(csv.DictReader(open(MAN, encoding="utf-8")))


def check(r):
    p = Path(r["output"])
    if not p.exists():
        return ["missing"]
    if r["kind"] == "T":
        d, pr = R.check(dict(meeting_date=r["meeting_date"], output_path=r["output"], source_type="discussion"))
        return pr if d is not None else (pr or ["no Part 3"])
    t = p.read_text(encoding="utf-8")
    m = re.findall(r"```(?:\w*)\s*\n(MEETING_DATE:.*?)```", t, re.DOTALL)
    if not m:
        return ["no code block"]
    d = {}
    for ln in m[-1].splitlines():
        if ":" in ln:
            k, _, v = ln.partition(":"); d[k.strip()] = v.strip()
    pr = []
    if d.get("MEETING_DATE") != r["meeting_date"]:
        pr.append("date")
    for k in r["dims"].split(","):
        v = d.get(k)
        if v is None:
            pr.append(f"{k} missing"); continue
        if v == "N/A":
            continue
        if not (v.isdigit() and 1 <= int(v) <= 100):
            pr.append(f"{k} value {v}")
        if k not in R.SUBS:
            if not re.fullmatch(r"\+-\d+", d.get(k + "_UNC", "")): pr.append(f"{k}_UNC")
            if d.get(k + "_CONF") not in ("High", "Moderate", "Low"): pr.append(f"{k}_CONF")
    return pr


def status():
    rows = load(); out = {}
    for k in "TS":
        rs = [r for r in rows if r["kind"] == k]
        ok = sum(check(r) == [] for r in rs)
        bad = {r["meeting_date"]: check(r) for r in rs if check(r) not in ([], ["missing"])}
        print(f"{k}: valid {ok}/{len(rs)}; invalid-existing {len(bad)}; missing {len(rs) - ok - len(bad)}", list(bad.items())[:6])


STALE = 8 * 60  # a dispatched item with no valid output after this many seconds is treated as failed and re-queued


def read_ledger():
    import time
    d = {}
    if LED.exists():
        for ln in LED.read_text().splitlines():
            parts = ln.split()
            if parts:
                d[parts[0]] = float(parts[1]) if len(parts) > 1 else time.time() - 120  # legacy line: assume recent
    return d


def nxt(n):
    import time
    rows = load(); now = time.time(); led = read_ledger()
    key = lambda r: f"{r['kind']}:{r['meeting_date']}"
    inflight = [r for r in rows if key(r) in led and check(r) != [] and now - led[key(r)] < STALE]
    retry = [r for r in rows if key(r) in led and check(r) != [] and now - led[key(r)] >= STALE]
    fresh = [r for r in rows if key(r) not in led and check(r) != []]
    fresh.sort(key=lambda r: (r["kind"] != "T", r["meeting_date"]))  # transcripts first
    n = max(0, min(n, CAP - len(inflight)))
    pick = (retry + fresh)[:n]
    with open(LED, "a") as f:
        for r in pick:
            f.write(f"{key(r)} {now}" + chr(10))
    attempts = {}
    for ln in (LED.read_text().splitlines() if LED.exists() else []):
        p = ln.split()
        if p:
            attempts[p[0]] = attempts.get(p[0], 0) + 1
    print(f"in flight {len(inflight)}; stale/failed awaiting retry {len(retry)}; launching {len(pick)}")
    for r in pick:
        tag = "RETRY" if r in retry else "NEW"
        model = r["model"]
        if tag == "RETRY" and attempts.get(key(r), 0) >= 2 and model != "opus":
            model = "opus"  # two failed Sonnet attempts: switch model and log the exception
            with open(HERE / "MODEL_EXCEPTIONS.txt", "a") as mf:
                mf.write(f"{r['meeting_date']}   (kind {r['kind']}; >=2 failed Sonnet attempts; retried on opus)" + chr(10))
        print(tag, r["kind"], r["meeting_date"], "MODEL=" + model, r["dims"], r["why"], "(partial file exists: overwrite)" if Path(r["output"]).exists() else "")
    print("remaining fresh after this batch:", len(fresh) - max(0, len(pick) - len(retry)))


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "build": build()
    elif c == "status": status()
    elif c == "next": nxt(int(sys.argv[2]) if len(sys.argv) > 2 else 6)
    else: print(__doc__)
