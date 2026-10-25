"""Fresh re-score of MINUTES for 60 matched meetings, to test whether the minutes-versus-transcript comparison is consistent across scoring processes.

The published minutes rows are patches of earlier analyses; the transcript rows are fresh scores. This run scores the same minutes inputs fresh (V4.1.1, blind),
so we can compare (a) fresh minutes versus patched minutes (patch/anchoring artifact), and (b) the fresh-minutes-versus-transcript gap against the published gap.

  python minutes_fresh_runner.py build     draw 60 matched meetings (20 per era, seed 20261011) -> minutes_fresh/manifest.csv
  python minutes_fresh_runner.py status | next N | compare

Dispatch prompt (one default-model agent per item):
  "Score one FOMC minutes discussion document fresh with the v4.1 rubric plus the V4.1.1 clarifications, blind to any earlier score. First read the procedure and
   follow it exactly: <...>\\SCORING_INSTRUCTIONS_minutes_v411.md / Meeting date: <d> / INPUT: <input> / OUTPUT: <output> /
   Treat this document in isolation; open no other meeting's files and no score files."
"""
import csv, datetime as dt, json, random, statistics as st, sys, time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_v41 as R  # noqa: E402

ROOT = HERE.parents[2]
D = HERE / "minutes_fresh"
MAN, LED = D / "manifest.csv", D / "dispatched.txt"
INP = ROOT / "03_decomposition/output_rebuild/member_discussion_v2/minutes"
T_TAB = HERE / "all_scores_discussion_v411_creditupd.csv"
M_TAB = HERE / "minutes_patch/all_scores_disc_m_v411_patched.csv"
CAP, STALE = 10, 12 * 60
DIMS = list(R.FULL) + list(R.SUBS)
HEAD = ["HAWKISH_DOVISH_LEAN", "DISSENT_INTENSITY", "FORWARD_GUIDANCE_TONE", "UNCERTAINTY_EXPRESSED"]
num = lambda v: int(v) if v and v.isdigit() else None
era = lambda d: "1993-2000" if d[:4] <= "2000" else "2001-2008" if d[:4] <= "2008" else "2009-2020"


def pairs():
    t = {r["MEETING_DATE"]: r for r in csv.DictReader(open(T_TAB, encoding="utf-8"))}
    out = {}
    for r in csv.DictReader(open(M_TAB, encoding="utf-8")):
        x = dt.date.fromisoformat(r["MEETING_DATE"])
        for k in (0, 1, -1):
            e = (x + dt.timedelta(k)).isoformat()
            if e in t:
                out[r["MEETING_DATE"]] = e; break
    return out


def build():
    D.mkdir(exist_ok=True); (D / "outputs").mkdir(exist_ok=True)
    pr = pairs(); rng = random.Random(20261011); pick = []
    for e in ("1993-2000", "2001-2008", "2009-2020"):
        pool = sorted(d for d in pr if era(d) == e); print(e, "matched", len(pool))
        pick += rng.sample(pool, 20)
    with open(MAN, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["meeting_date", "transcript_date", "input", "output", "era", "words"])
        for d in sorted(pick):
            p = INP / f"{d}.txt"
            w.writerow([d, pr[d], str(p), str(D / "outputs" / f"{d}.md"), era(d), len(p.read_text(encoding="utf-8").split())])
    print(len(pick), "picked")


def rows():
    return list(csv.DictReader(open(MAN, encoding="utf-8")))


def check(r):
    d, pr = R.check(dict(meeting_date=r["meeting_date"], output_path=r["output"], source_type="discussion_m"))
    return pr if d is not None else (pr or ["no Part 3"])


def status():
    rs = rows(); ok = sum(check(r) == [] for r in rs)
    bad = {r["meeting_date"]: check(r) for r in rs if check(r) not in ([], ["missing"])}
    print(f"valid {ok}/{len(rs)}; invalid-existing {len(bad)}; missing {len(rs) - ok - len(bad)}", list(bad.items())[:5])


def nxt(n):
    rs = rows(); now = time.time(); led = {}
    if LED.exists():
        for ln in LED.read_text().splitlines():
            p = ln.split()
            if len(p) == 2:
                led[p[0]] = float(p[1])
    inflight = [r for r in rs if r["meeting_date"] in led and check(r) != [] and now - led[r["meeting_date"]] < STALE]
    retry = [r for r in rs if r["meeting_date"] in led and check(r) != [] and now - led[r["meeting_date"]] >= STALE]
    fresh = [r for r in rs if r["meeting_date"] not in led and check(r) != []]
    pick = (retry + fresh)[:max(0, min(n, CAP - len(inflight)))]
    with open(LED, "a") as f:
        for r in pick:
            f.write(f"{r['meeting_date']} {now}" + chr(10))
    print(f"in flight {len(inflight)}; stale/failed awaiting retry {len(retry)}; launching {len(pick)}")
    for r in pick:
        print("RETRY" if r in retry else "NEW", r["meeting_date"], "|", r["input"].split("output_rebuild\\")[-1].replace("\\", "/"), "|", r["words"], "words")
    print("remaining undispatched after this batch:", len(fresh) - max(0, len(pick) - len(retry)))


def compare():
    rs = rows(); assert all(check(r) == [] for r in rs), "not all outputs valid"
    t = {r["MEETING_DATE"]: r for r in csv.DictReader(open(T_TAB, encoding="utf-8"))}
    m = {r["MEETING_DATE"]: r for r in csv.DictReader(open(M_TAB, encoding="utf-8"))}
    plog = {}
    pl = HERE / "minutes_patch/revision_log_long.csv"
    if pl.exists():
        for r in csv.DictReader(open(pl, encoding="utf-8")):
            plog[(r["meeting_date"], r.get("dimension", ""))] = r.get("patch_status", r.get("status", ""))
    cells = []
    for r in rs:
        d, td = r["meeting_date"], r["transcript_date"]
        fresh, _ = R.check(dict(meeting_date=d, output_path=r["output"], source_type="discussion_m"))
        for dm in DIMS:
            cells.append(dict(meeting_date=d, transcript_date=td, era=r["era"], dimension=dm, fresh_minutes=fresh[dm], patched_minutes=m[d][dm],
                              transcript=t[td][dm], fresh_conf=fresh.get(dm + "_CONF", ""), patch_status=plog.get((d, dm), "")))
    with open(D / "minutes_fresh_cells.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(cells[0])); w.writeheader(); w.writerows(cells)
    res = {}
    mean = lambda v: round(st.mean(v), 2) if v else None
    for dm in DIMS:
        cs = [c for c in cells if c["dimension"] == dm]
        fp = [(num(c["fresh_minutes"]), num(c["patched_minutes"])) for c in cs if num(c["fresh_minutes"]) is not None and num(c["patched_minutes"]) is not None]
        d_fp = [a - b for a, b in fp]
        tri = [(num(c["fresh_minutes"]), num(c["patched_minutes"]), num(c["transcript"])) for c in cs if None not in (num(c["fresh_minutes"]), num(c["patched_minutes"]), num(c["transcript"]))]
        res[dm] = dict(cells=len(cs), both_fresh_patched=len(fp), presence_flips=sum((num(c["fresh_minutes"]) is None) != (num(c["patched_minutes"]) is None) for c in cs),
                       mad_fresh_vs_patched=mean([abs(x) for x in d_fp]), bias_fresh_minus_patched=mean(d_fp),
                       within5=round(sum(abs(x) <= 5 for x in d_fp) / len(d_fp), 2) if d_fp else None,
                       corr_fresh_patched=round(st.correlation([a for a, b in fp], [b for a, b in fp]), 3) if len(fp) > 3 else None,
                       triples=len(tri), gap_patched_minus_transcript=mean([b - c for a, b, c in tri]), gap_fresh_minus_transcript=mean([a - c for a, b, c in tri]))
    allf = [(num(c["fresh_minutes"]), num(c["patched_minutes"])) for c in cells if num(c["fresh_minutes"]) is not None and num(c["patched_minutes"]) is not None and c["dimension"] in R.FULL]
    d_all = [a - b for a, b in allf]
    res["_ALL"] = dict(pairs=len(allf), mad=round(st.mean(abs(x) for x in d_all), 2), sd=round(st.stdev(d_all), 2), within5=round(sum(abs(x) <= 5 for x in d_all) / len(d_all), 3),
                       within10=round(sum(abs(x) <= 10 for x in d_all) / len(d_all), 3), over10=sum(abs(x) > 10 for x in d_all),
                       presence_flips=sum((num(c["fresh_minutes"]) is None) != (num(c["patched_minutes"]) is None) for c in cells if c["dimension"] in R.FULL),
                       n_cells=sum(1 for c in cells if c["dimension"] in R.FULL))
    json.dump(res, open(D / "minutes_fresh_results.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "build": build()
    elif c == "status": status()
    elif c == "next": nxt(int(sys.argv[2]) if len(sys.argv) > 2 else 10)
    elif c == "compare": compare()
    else: print(__doc__)
