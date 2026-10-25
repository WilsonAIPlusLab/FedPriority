"""Merge and compare the 2026-10-07 follow-up runs (local only, nothing published).

  python followup_merge.py

Writes:
  all_scores_discussion_v411.csv   transcript table: v2b/V4.1.1 re-score where one exists, else the V4.1 row (+ SCORE_VERSION)
  transcript_rescore_diff.csv      old vs new value for every re-scored meeting and dimension
  second_pass_vs_patched.csv       blind second pass vs the patched minutes value, one row per target cell
  FOLLOWUP_STATS.json              the summary numbers used in V41_RESULTS_AND_LIMITS.md
"""
import csv, json, re, statistics as st
from pathlib import Path
import sys

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import run_v41 as R
import rerun_v411 as RR

MAIN = HERE / "all_scores_discussion_v41.csv"
PATCHED = HERE / "minutes_patch" / "all_scores_disc_m_v41_patched.csv"
LOG = HERE / "minutes_patch" / "revision_log_long.csv"


def read(p):
    return list(csv.DictReader(open(p, encoding="utf-8")))


def num(v):
    return int(v) if v and v.isdigit() else None


def main():
    main_rows = {r["MEETING_DATE"]: r for r in read(MAIN)}
    cols = list(next(iter(main_rows.values())).keys())
    man = RR.load()
    new_rows = {}
    for r in man:
        if r["kind"] != "T":
            continue
        d, pr = R.check(dict(meeting_date=r["meeting_date"], output_path=r["output"], source_type="discussion"))
        assert d is not None and not pr, (r["meeting_date"], pr)
        new_rows[r["meeting_date"]] = {c: d.get(c, "") for c in cols}
    merged, diffs = [], []
    for dt in sorted(set(main_rows) | set(new_rows)):
        if dt in new_rows:
            row = dict(new_rows[dt]); row["SCORE_VERSION"] = "v411_v2b"
        else:
            row = dict(main_rows[dt]); row["SCORE_VERSION"] = "v41_v2"
        merged.append(row)
        if dt in new_rows and dt in main_rows:
            for c in cols:
                if c in ("MEETING_DATE", "SOURCE_TYPE", "ANOMALY_FLAG", "ANOMALY_NOTE") or c.endswith(("_UNC", "_CONF")):
                    continue
                diffs.append(dict(meeting_date=dt, dimension=c, old=main_rows[dt][c], new=new_rows[dt][c]))
    with open(HERE / "all_scores_discussion_v411.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols + ["SCORE_VERSION"]); w.writeheader(); w.writerows(merged)
    with open(HERE / "transcript_rescore_diff.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["meeting_date", "dimension", "old", "new"]); w.writeheader(); w.writerows(diffs)

    why = {r["meeting_date"]: r["why"] for r in man if r["kind"] == "T"}
    stats = {"transcript_rows_total": len(merged), "transcripts_rescored": len(new_rows),
             "transcripts_new_rows (were missing)": sorted(set(new_rows) - set(main_rows))}
    # per-dimension change summary on re-scored meetings that had a V4.1 row
    per = {}
    for d in diffs:
        o, n = num(d["old"]), num(d["new"])
        s = per.setdefault(d["dimension"], dict(both=0, same=0, deltas=[], na_to_val=0, val_to_na=0))
        if o is not None and n is not None:
            s["both"] += 1; s["deltas"].append(n - o); s["same"] += (n == o)
        elif o is None and n is not None:
            s["na_to_val"] += 1
        elif o is not None and n is None:
            s["val_to_na"] += 1
    stats["transcript_dim_changes"] = {
        k: dict(n_both=v["both"], n_equal=v["same"],
                mean_delta=round(st.mean(v["deltas"]), 2) if v["deltas"] else None,
                mean_abs_delta=round(st.mean(abs(x) for x in v["deltas"]), 2) if v["deltas"] else None,
                na_to_value=v["na_to_val"], value_to_na=v["val_to_na"]) for k, v in per.items()}
    # the four new dimensions, by reason for re-score
    core = ["HAWKISH_DOVISH_LEAN", "DISSENT_INTENSITY", "FORWARD_GUIDANCE_TONE", "UNCERTAINTY_EXPRESSED"]
    bywhy = {}
    for d in diffs:
        if d["dimension"] not in core:
            continue
        for w_ in why[d["meeting_date"]].split("+"):
            s = bywhy.setdefault(w_, {}).setdefault(d["dimension"], [])
            o, n = num(d["old"]), num(d["new"])
            s.append((o, n))
    stats["core_by_reason"] = {w_: {dim: dict(n=len(v), old_na=sum(o is None for o, n in v), new_na=sum(n is None for o, n in v),
                                              mean_abs_delta=(round(st.mean(abs(n - o) for o, n in v if o is not None and n is not None), 2)
                                                              if any(o is not None and n is not None for o, n in v) else None))
                                  for dim, v in dd.items()} for w_, dd in bywhy.items()}
    # still all-N/A on core after rescoring
    stats["all_na_core_after"] = sorted(r["MEETING_DATE"] for r in merged if all(r[c] == "N/A" for c in ("HAWKISH_DOVISH_LEAN", "DISSENT_INTENSITY")))

    # ---- second pass vs patched minutes
    pat = {r["MEETING_DATE"]: r for r in read(PATCHED)}
    log = {}
    for r in read(LOG):
        log[(r["meeting_date"], r["dimension"])] = r
    tg = json.load(open(HERE / "minutes_patch" / "second_pass_targets.json"))
    rows = []
    for dt, dims in tg.items():
        r = [x for x in man if x["kind"] == "S" and x["meeting_date"] == dt][0]
        assert RR.check(r) == [], (dt, RR.check(r))
        t = Path(r["output"]).read_text(encoding="utf-8")
        m = re.findall(r"```(?:\w*)\s*\n(MEETING_DATE:.*?)```", t, re.DOTALL)[-1]
        sp = {}
        for ln in m.splitlines():
            if ":" in ln:
                k, _, v = ln.partition(":"); sp[k.strip()] = v.strip()
        for dim in dims:
            pv = pat[dt][dim]
            sv = sp.get(dim, "")
            lg = log.get((dt, dim), {})
            cat = ("both_NA" if not pv.isdigit() and not sv.isdigit() else "patched_value__second_NA" if pv.isdigit() and not sv.isdigit()
                   else "patched_NA__second_value" if sv.isdigit() and not pv.isdigit()
                   else "both_value_within_5" if abs(int(sv) - int(pv)) <= 5 else "both_value_within_10" if abs(int(sv) - int(pv)) <= 10 else "both_value_over_10")
            rows.append(dict(meeting_date=dt, dimension=dim, category=cat, patched=pv, second_pass=sv,
                             second_pass_conf=sp.get(dim + "_CONF", ""), patched_conf=pat[dt].get(dim + "_CONF", ""),
                             patch_status=lg.get("status", ""), patch_reason=lg.get("reason", "")[:200]))
    with open(HERE / "second_pass_vs_patched.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    both = [(num(r["patched"]), num(r["second_pass"]), r) for r in rows]
    nb = [(p, s, r) for p, s, r in both if p is not None and s is not None]
    d = [s - p for p, s, r in nb]
    ad = [abs(x) for x in d]
    stats["second_pass"] = dict(
        cells=len(rows), both_values=len(nb), patched_value_second_NA=sum(p is not None and s is None for p, s, r in both),
        patched_NA_second_value=sum(p is None and s is not None for p, s, r in both),
        both_NA=sum(p is None and s is None for p, s, r in both),
        mean_signed_diff_second_minus_patched=round(st.mean(d), 2), mean_abs_diff=round(st.mean(ad), 2),
        median_abs_diff=st.median(ad), share_within_5=round(sum(x <= 5 for x in ad) / len(ad), 3),
        share_within_10=round(sum(x <= 10 for x in ad) / len(ad), 3), share_over_15=round(sum(x > 15 for x in ad) / len(ad), 3),
        corr=round(st.correlation([p for p, s, r in nb], [s for p, s, r in nb]), 3))
    by = {}
    for p, s, r in both:
        k = r["dimension"]
        b = by.setdefault(k, dict(n=0, val_to_na=0, nb=[]))
        b["n"] += 1
        if p is not None and s is None:
            b["val_to_na"] += 1
        if p is not None and s is not None:
            b["nb"].append(s - p)
    stats["second_pass_by_dimension"] = {k: dict(n=v["n"], patched_value_second_NA=v["val_to_na"], n_both=len(v["nb"]),
                                                 mean_signed=round(st.mean(v["nb"]), 2) if v["nb"] else None,
                                                 mean_abs=round(st.mean(abs(x) for x in v["nb"]), 2) if v["nb"] else None)
                                         for k, v in sorted(by.items())}
    # sign of the second-pass shift for CREDIT_SPREADS: availability-based second pass tends to sit on which side of the patched value
    json.dump(stats, open(HERE / "FOLLOWUP_STATS.json", "w"), indent=1)
    print(json.dumps(stats, indent=1)[:6000])


if __name__ == "__main__":
    main()
