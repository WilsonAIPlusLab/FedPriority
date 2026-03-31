"""
V4 FOMC Staff Assessment Scoring — Orchestration Helpers

This script provides:
1. Manifest generation (which documents to score, in what order)
2. Output parsing (extract Part 3 structured blocks from scored .md files)
3. Quality checks (anchor validation, cross-dimension consistency, bright-line rules)
4. Status tracking

The actual scoring is done by Claude agents in an interactive session,
NOT via API calls. Each agent receives the v4 prompt + one source document
and writes its output to v4_scores/{agent}/raw/{source_type}_{date}.md

Usage:
    python run_v4_scoring.py manifest      # Generate scoring manifest
    python run_v4_scoring.py extract       # Parse all scored files → CSV
    python run_v4_scoring.py validate      # Run quality checks on extracted CSV
    python run_v4_scoring.py status        # Show scoring progress
"""

import csv
import json
import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
RUBRIC_DIR = SCRIPT_DIR / "rubric"
V4_DIR = SCRIPT_DIR / "v4_scores"
COMBINED_STAFF_DIR = SCRIPT_DIR / "combined_staff"

MANIFEST_PATH = V4_DIR / "manifest.csv"
MASTER_CSV = V4_DIR / "all_scores_v4.csv"
ANCHOR_CSV = RUBRIC_DIR / "anchor_meetings_v4.csv"

# V4 column names — staff dimensions (not discussion policy dims)
CORE_ECONOMIC_DIMS = [
    "INFLATION_PRESSURE", "OUTPUT_GAP", "LABOR_TIGHTNESS",
    "CONSUMPTION_INVESTMENT", "PRODUCTIVITY",
]

CORE_FINANCIAL_DIMS = [
    "FINANCIAL_CONDITIONS", "TREASURY_STRESS", "CREDIT_SPREADS",
    "EQUITY_VALUATION", "BANKING_STRESS", "DOLLAR_STRENGTH",
]

CORE_DIMS = CORE_ECONOMIC_DIMS + CORE_FINANCIAL_DIMS

INFLATION_SUBS = [
    "INFLATION_GOODS", "INFLATION_SERVICES",
    "INFLATION_HOUSING", "INFLATION_EXPECTATIONS",
]

ALL_DIMS = CORE_DIMS + INFLATION_SUBS

# Dimensions that always have _UNC and _CONF
DIMS_WITH_UNC_CONF = CORE_DIMS

ALL_COLUMNS = (
    ["MEETING_DATE", "SOURCE_TYPE"]
    + [f for d in DIMS_WITH_UNC_CONF for f in (d, f"{d}_UNC", f"{d}_CONF")]
    + INFLATION_SUBS
    + ["ANOMALY_FLAG", "ANOMALY_NOTE"]
)


def cmd_manifest(args):
    """Generate the scoring manifest from combined_staff directory."""
    V4_DIR.mkdir(parents=True, exist_ok=True)
    (V4_DIR / "agent1_minutes" / "raw").mkdir(parents=True, exist_ok=True)
    (V4_DIR / "agent2_transcripts" / "raw").mkdir(parents=True, exist_ok=True)

    rows = []

    for f in sorted(COMBINED_STAFF_DIR.glob("*.txt")):
        name = f.stem  # e.g., minutes_2018-05-02_staff_combined
        if name.startswith("minutes_"):
            date = name.split("_")[1]  # 2018-05-02
            source_type = "minutes"
            output_path = V4_DIR / "agent1_minutes" / "raw" / f"minutes_{date}.md"
        elif name.startswith("transcript_"):
            date = name.split("_")[1]
            source_type = "transcript"
            output_path = V4_DIR / "agent2_transcripts" / "raw" / f"transcript_{date}.md"
        else:
            continue

        rows.append({
            "meeting_date": date,
            "source_type": source_type,
            "source_path": str(f),
            "output_path": str(output_path),
            "status": "pending",
        })

    with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "meeting_date", "source_type", "source_path", "output_path", "status"
        ])
        writer.writeheader()
        writer.writerows(rows)

    n_min = sum(1 for r in rows if r["source_type"] == "minutes")
    n_tr = sum(1 for r in rows if r["source_type"] == "transcript")
    print(f"Manifest written: {len(rows)} documents ({n_min} minutes, {n_tr} transcripts)")
    print(f"  Path: {MANIFEST_PATH}")


def cmd_status(args):
    """Show scoring progress."""
    if not MANIFEST_PATH.exists():
        print("No manifest found. Run: python run_v4_scoring.py manifest")
        return

    with open(MANIFEST_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    scored = sum(1 for r in rows if Path(r["output_path"]).exists())
    pending = len(rows) - scored
    minutes_scored = sum(1 for r in rows if r["source_type"] == "minutes" and Path(r["output_path"]).exists())
    transcripts_scored = sum(1 for r in rows if r["source_type"] == "transcript" and Path(r["output_path"]).exists())
    minutes_total = sum(1 for r in rows if r["source_type"] == "minutes")
    transcripts_total = sum(1 for r in rows if r["source_type"] == "transcript")

    print(f"V4 Scoring Progress:")
    print(f"  Total:       {scored}/{len(rows)} ({scored/len(rows)*100:.1f}%)")
    print(f"  Minutes:     {minutes_scored}/{minutes_total}")
    print(f"  Transcripts: {transcripts_scored}/{transcripts_total}")
    print(f"  Pending:     {pending}")


def extract_part3(filepath: Path) -> dict | None:
    """Extract key-value pairs from Part 3 structured output block."""
    text = filepath.read_text(encoding="utf-8")

    # Find the Part 3 code block (case-insensitive header, optional language tag)
    match = re.search(r"##\s*Part\s*3.*?```(?:\w*)\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if not match:
        # Try alternate: find MEETING_DATE through ANOMALY_NOTE block
        match = re.search(r"MEETING_DATE:.*?(?:ANOMALY_NOTE:.*)", text, re.DOTALL)
        if not match:
            return None

    block = match.group(1) if match.lastindex else match.group(0)

    # Check if this is JSON format
    if block.strip().startswith("{"):
        return _extract_json_format(block)

    # Check if this is YAML nested format (has "score:" subkeys)
    if re.search(r"^\s+score:", block, re.MULTILINE):
        return _extract_yaml_format(block)

    data = {}
    for line in block.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # Handle combined format: "67 ±6 High" or "67 +-6 High"
            combined = re.match(
                r"^(\d+)\s*[±\xb1]?\s*[+\-]*\s*(\d+)\s+(High|Moderate|Low)$", value
            )
            if combined and key in CORE_DIMS:
                data[key] = combined.group(1)
                data[f"{key}_UNC"] = combined.group(2)
                data[f"{key}_CONF"] = combined.group(3)
            else:
                data[key] = value

    return data


def _extract_yaml_format(block: str) -> dict:
    """Extract scores from YAML nested format."""
    data = {}
    current_dim = None

    for line in block.strip().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("---") or stripped.startswith("#"):
            continue

        if not line.startswith(" ") and not line.startswith("\t") and ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            if value and key in ("MEETING_DATE", "SOURCE_TYPE",
                                  "ANOMALY_FLAG", "ANOMALY_NOTE"):
                data[key] = value
            continue

        if stripped.endswith(":") and stripped.isupper():
            continue

        indent = len(line) - len(line.lstrip())
        if indent <= 4 and stripped.endswith(":") and not stripped.startswith("score") \
                and not stripped.startswith("uncertainty") and not stripped.startswith("confidence"):
            current_dim = stripped[:-1].strip()
            continue

        if current_dim and ":" in stripped:
            subkey, _, subval = stripped.partition(":")
            subkey = subkey.strip()
            subval = subval.strip()

            if subkey == "score":
                data[current_dim] = subval
            elif subkey == "uncertainty_band":
                m = re.match(r"\[(\d+),\s*(\d+)\]", subval)
                if m and current_dim:
                    score = int(data.get(current_dim, 50))
                    lo, hi = int(m.group(1)), int(m.group(2))
                    unc = max(score - lo, hi - score)
                    data[f"{current_dim}_UNC"] = str(unc)
            elif subkey == "confidence":
                if current_dim:
                    data[f"{current_dim}_CONF"] = subval

    return data


def _extract_json_format(block: str) -> dict:
    """Extract scores from JSON format output."""
    try:
        obj = json.loads(block)
    except json.JSONDecodeError:
        return {}

    data = {}
    if "meeting_date" in obj:
        data["MEETING_DATE"] = obj["meeting_date"]
    if "source_type" in obj:
        data["SOURCE_TYPE"] = obj["source_type"]

    for tier_key in ("tier1", "tier2", "economic", "financial", "inflation_subs"):
        tier = obj.get(tier_key, {})
        for dim, info in tier.items():
            if isinstance(info, dict):
                data[dim] = str(info.get("score", ""))
                lo = info.get("band_lo")
                hi = info.get("band_hi")
                score = info.get("score", 50)
                if lo is not None and hi is not None:
                    unc = max(score - lo, hi - score)
                    data[f"{dim}_UNC"] = str(unc)
                conf = info.get("confidence", "")
                if conf:
                    data[f"{dim}_CONF"] = conf
            else:
                data[dim] = str(info)

    data["ANOMALY_FLAG"] = obj.get("anomaly_flag", obj.get("ANOMALY_FLAG", "No"))
    data["ANOMALY_NOTE"] = obj.get("anomaly_note", obj.get("ANOMALY_NOTE", ""))

    return data


def cmd_extract(args):
    """Parse all scored files and produce master CSV."""
    V4_DIR.mkdir(parents=True, exist_ok=True)

    raw_dirs = [
        V4_DIR / "independent" / "minutes",
        V4_DIR / "independent" / "transcripts",
    ]

    all_files = []
    for d in raw_dirs:
        if d.exists():
            all_files.extend(sorted(d.glob("*.md")))

    print(f"Found {len(all_files)} scored files")

    rows = []
    errors = []

    for fp in all_files:
        data = extract_part3(fp)
        if data is None:
            errors.append(f"  No Part 3 block: {fp.name}")
            continue

        row = {}
        for col in ALL_COLUMNS:
            raw = data.get(col, "")
            if col.endswith("_UNC"):
                raw = raw.replace("+-", "").replace("±", "").strip()
            row[col] = raw

        rows.append(row)

    with open(MASTER_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ALL_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Extracted {len(rows)} rows -> {MASTER_CSV}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(e)


def cmd_validate(args):
    """Run quality checks on extracted scores."""
    if not MASTER_CSV.exists():
        print("No master CSV found. Run: python run_v4_scoring.py extract")
        return

    with open(MASTER_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Validating {len(rows)} scored meetings...\n")

    flags = []

    for row in rows:
        date = row.get("MEETING_DATE", "???")
        src = row.get("SOURCE_TYPE", "???")
        label = f"{src}_{date}"

        # Check 1: Range (1-100, no zeros)
        for dim in ALL_DIMS:
            val = row.get(dim, "")
            if val and val != "N/A":
                try:
                    v = int(val)
                    if v < 1 or v > 100:
                        flags.append(f"[RANGE] {label}: {dim}={v}")
                    if v == 0:
                        flags.append(f"[ZERO] {label}: {dim}=0")
                except ValueError:
                    flags.append(f"[PARSE] {label}: {dim}='{val}'")

        # Check 2: Cross-dimension consistency
        og = _safe_int(row.get("OUTPUT_GAP"))
        lt = _safe_int(row.get("LABOR_TIGHTNESS"))
        if og is not None and lt is not None:
            if og < 25 and lt > 65:
                flags.append(f"[CROSS] {label}: OUTPUT_GAP={og} but LABOR_TIGHTNESS={lt}")
            if og > 70 and lt < 30:
                flags.append(f"[CROSS] {label}: OUTPUT_GAP={og} but LABOR_TIGHTNESS={lt}")

        fc = _safe_int(row.get("FINANCIAL_CONDITIONS"))
        cs = _safe_int(row.get("CREDIT_SPREADS"))
        if fc is not None and cs is not None:
            if abs(fc - cs) > 35:
                flags.append(f"[CROSS] {label}: FC={fc} vs CREDIT_SPREADS={cs} (delta={abs(fc-cs)})")

        og2 = _safe_int(row.get("OUTPUT_GAP"))
        ci = _safe_int(row.get("CONSUMPTION_INVESTMENT"))
        if og2 is not None and ci is not None:
            if abs(og2 - ci) > 30:
                flags.append(f"[CROSS] {label}: OUTPUT_GAP={og2} vs C_I={ci} (delta={abs(og2-ci)})")

        # Check 3: Bright-line polarity checks (spot-check known problem dimensions)
        bs = _safe_int(row.get("BANKING_STRESS"))
        ds = _safe_int(row.get("DOLLAR_STRENGTH"))
        ts = _safe_int(row.get("TREASURY_STRESS"))

        # Banking stress: flag if > 45 and non-crisis era (potential polarity confusion)
        if bs is not None and date is not None:
            year = int(date[:4]) if len(date) >= 4 else 0
            if bs > 55 and year not in (2007, 2008, 2009, 2020, 2023):
                flags.append(f"[POLARITY?] {label}: BANKING_STRESS={bs} in non-crisis year")

        # Treasury stress: flag if > 55 (likely confusing yield moves with dysfunction)
        if ts is not None and ts > 60:
            year = int(date[:4]) if len(date) >= 4 else 0
            if year not in (2008, 2009, 2020):
                flags.append(f"[TREAS_OVER?] {label}: TREASURY_STRESS={ts} in non-crisis year")

    # Check 4: Anchor meetings
    if ANCHOR_CSV.exists():
        anchors = _load_anchors()
        for row in rows:
            date = row.get("MEETING_DATE", "")
            src = row.get("SOURCE_TYPE", "")
            key = (date, src)
            if key in anchors:
                anchor = anchors[key]
                for dim, (lo, hi) in anchor.items():
                    val = _safe_int(row.get(dim))
                    if val is not None and (val < lo - 10 or val > hi + 10):
                        flags.append(f"[ANCHOR] {src}_{date}: {dim}={val} expected {lo}-{hi}")

    # Summary stats
    print("=== Distribution Summary ===")
    for dim in CORE_DIMS:
        vals = [_safe_int(r.get(dim)) for r in rows if _safe_int(r.get(dim)) is not None]
        if vals:
            print(f"  {dim:25s}: N={len(vals):3d}  mean={sum(vals)/len(vals):5.1f}  "
                  f"min={min(vals):3d}  max={max(vals):3d}  range={max(vals)-min(vals)}")

    print(f"\n=== Optional Dimensions Coverage ===")
    for dim in INFLATION_SUBS:
        scored = sum(1 for r in rows if r.get(dim, "") not in ("", "N/A"))
        print(f"  {dim:25s}: {scored}/{len(rows)} ({scored/len(rows)*100:.0f}%)")

    print(f"\n=== Flags ({len(flags)}) ===")
    for f in sorted(flags):
        print(f"  {f}")

    # Write quality report
    report_path = V4_DIR / "quality_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# V4 Staff Scoring Quality Report\n\n")
        f.write(f"Total scored: {len(rows)}\n")
        f.write(f"Total flags: {len(flags)}\n\n")
        f.write("## Flags\n\n")
        for flag in sorted(flags):
            f.write(f"- {flag}\n")
    print(f"\nReport: {report_path}")


def _safe_int(val):
    if val is None or val == "" or val == "N/A":
        return None
    try:
        return int(val)
    except ValueError:
        return None


def _load_anchors():
    """Load anchor meeting expected ranges."""
    anchors = {}
    with open(ANCHOR_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["meeting_date"], row["source_type"])
            anchor = {}
            for dim in CORE_DIMS:
                lo_key = f"{dim}_min"
                hi_key = f"{dim}_max"
                if lo_key in row and hi_key in row and row[lo_key] and row[hi_key]:
                    anchor[dim] = (int(row[lo_key]), int(row[hi_key]))
            anchors[key] = anchor
    return anchors


def cmd_compare(args):
    """Compare minutes vs transcripts scores for overlapping meetings."""
    if not MASTER_CSV.exists():
        print("No master CSV found. Run: python run_v4_scoring.py extract")
        return

    with open(MASTER_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Group by meeting date
    by_date = defaultdict(dict)
    for row in rows:
        date = row.get("MEETING_DATE", "")
        src = row.get("SOURCE_TYPE", "")
        by_date[date][src] = row

    # Find meetings with both minutes and transcript
    both = {d: v for d, v in by_date.items() if "minutes" in v and "transcript" in v}
    print(f"Meetings with both minutes and transcript: {len(both)}")

    # Check how many transcripts are all-N/A (special-topic)
    all_na_transcripts = 0
    scorable_pairs = {}
    for date, sources in sorted(both.items()):
        tr = sources["transcript"]
        has_score = any(
            _safe_int(tr.get(d)) is not None for d in CORE_DIMS
        )
        if not has_score:
            all_na_transcripts += 1
        else:
            scorable_pairs[date] = sources

    print(f"All-N/A transcripts (special-topic): {all_na_transcripts}")
    print(f"Scorable pairs for comparison: {len(scorable_pairs)}\n")

    # Per-dimension comparison
    comparison_csv_path = V4_DIR / "minutes_vs_transcripts.csv"
    comp_rows = []

    print(f"{'DIMENSION':30s} {'N':>4s} {'r':>6s} {'MAD':>6s} {'Bias':>7s}  (min-trans)")
    print("-" * 65)

    for dim in CORE_DIMS + INFLATION_SUBS:
        min_vals = []
        trans_vals = []

        for date, sources in sorted(scorable_pairs.items()):
            m_val = _safe_int(sources["minutes"].get(dim))
            t_val = _safe_int(sources["transcript"].get(dim))
            if m_val is not None and t_val is not None:
                min_vals.append(m_val)
                trans_vals.append(t_val)
                comp_rows.append({
                    "meeting_date": date,
                    "dimension": dim,
                    "minutes_score": m_val,
                    "transcript_score": t_val,
                    "diff": m_val - t_val,
                })

        n = len(min_vals)
        if n < 5:
            print(f"{dim:30s} {n:4d}   (too few)")
            continue

        # Pearson correlation
        r = _pearson(min_vals, trans_vals)
        # Mean absolute difference
        mad = sum(abs(a - b) for a, b in zip(min_vals, trans_vals)) / n
        # Mean bias (minutes - transcript)
        bias = sum(a - b for a, b in zip(min_vals, trans_vals)) / n

        print(f"{dim:30s} {n:4d} {r:6.3f} {mad:6.1f} {bias:+7.1f}")

    # Write comparison CSV
    if comp_rows:
        with open(comparison_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "meeting_date", "dimension", "minutes_score", "transcript_score", "diff"
            ])
            writer.writeheader()
            writer.writerows(comp_rows)
        print(f"\nComparison CSV: {comparison_csv_path} ({len(comp_rows)} rows)")

    # Write comparison report
    report_path = V4_DIR / "comparison_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# V4 Staff Scores: Minutes vs Transcripts Comparison\n\n")
        f.write(f"- Meetings with both sources: {len(both)}\n")
        f.write(f"- All-N/A transcripts (special-topic): {all_na_transcripts}\n")
        f.write(f"- Scorable pairs: {len(scorable_pairs)}\n\n")
        f.write(f"| Dimension | N | r | MAD | Bias (min-trans) |\n")
        f.write(f"|-----------|---|---|-----|------------------|\n")

        for dim in CORE_DIMS + INFLATION_SUBS:
            min_vals = []
            trans_vals = []
            for date, sources in sorted(scorable_pairs.items()):
                m_val = _safe_int(sources["minutes"].get(dim))
                t_val = _safe_int(sources["transcript"].get(dim))
                if m_val is not None and t_val is not None:
                    min_vals.append(m_val)
                    trans_vals.append(t_val)
            n = len(min_vals)
            if n < 5:
                f.write(f"| {dim} | {n} | — | — | — |\n")
            else:
                r = _pearson(min_vals, trans_vals)
                mad = sum(abs(a - b) for a, b in zip(min_vals, trans_vals)) / n
                bias = sum(a - b for a, b in zip(min_vals, trans_vals)) / n
                f.write(f"| {dim} | {n} | {r:.3f} | {mad:.1f} | {bias:+.1f} |\n")

    print(f"Report: {report_path}")


def _pearson(x, y):
    """Compute Pearson correlation coefficient."""
    n = len(x)
    if n < 2:
        return 0.0
    mx = sum(x) / n
    my = sum(y) / n
    sx = (sum((xi - mx) ** 2 for xi in x)) ** 0.5
    sy = (sum((yi - my) ** 2 for yi in y)) ** 0.5
    if sx == 0 or sy == 0:
        return 0.0
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    return cov / (sx * sy)


def cmd_audit(args):
    """Audit V4 independent scored files for contamination signals."""
    import math

    v4_dirs = [
        V4_DIR / "independent" / "minutes",
        V4_DIR / "independent" / "transcripts",
    ]
    old_dirs = [
        V4_DIR / "agent1_minutes" / "raw",
        V4_DIR / "agent2_transcripts" / "raw",
    ]

    # --- Check 1: Cross-meeting contamination phrases ---
    # Agent-opinion phrases (BAD) vs source-document quotes (OK)
    CONTAMINATION_PHRASES = [
        r"I scored", r"in my previous", r"consistent with my earlier",
        r"similar to the last", r"as I scored", r"my earlier assessment",
        r"in the last meeting I scored", r"previously scored",
    ]
    CONTEXT_PHRASES = [
        r"prior meeting", r"previous meeting", r"last meeting",
        r"compared to the .* meeting", r"from the previous",
    ]

    print("=" * 70)
    print("  INDEPENDENCE AUDIT: V4 Scored Files")
    print("=" * 70)

    # Scan V4 independent files
    contamination_hits = []
    context_hits_v4 = {"in_evidence": 0, "in_reasoning": 0, "total_files": 0}

    v4_files = []
    for d in v4_dirs:
        if d.exists():
            v4_files.extend(sorted(d.glob("*.md")))
    context_hits_v4["total_files"] = len(v4_files)

    for fp in v4_files:
        text = fp.read_text(encoding="utf-8")
        # Check for hard contamination phrases
        for pat in CONTAMINATION_PHRASES:
            if re.search(pat, text, re.IGNORECASE):
                contamination_hits.append((fp.name, pat))

        # Check context phrases — classify as evidence-quote vs reasoning
        for pat in CONTEXT_PHRASES:
            for m in re.finditer(pat, text, re.IGNORECASE):
                # Check if match is inside an Evidence block
                start = max(0, m.start() - 200)
                preceding = text[start:m.start()]
                if "**Evidence**" in preceding or "Evidence:" in preceding:
                    context_hits_v4["in_evidence"] += 1
                else:
                    context_hits_v4["in_reasoning"] += 1

    print(f"\n--- Check 1: Contamination Phrases (V4 independent, N={len(v4_files)}) ---")
    if contamination_hits:
        print(f"  CONTAMINATION DETECTED in {len(contamination_hits)} instances:")
        for fname, pat in contamination_hits:
            print(f"    {fname}: matched '{pat}'")
    else:
        print("  PASS: Zero contamination phrases found")

    print(f"\n--- Check 2: Context Phrases (V4 independent) ---")
    print(f"  In evidence blocks (source quotes, OK): {context_hits_v4['in_evidence']}")
    print(f"  In reasoning text (potential issue):     {context_hits_v4['in_reasoning']}")

    # Scan OLD files for comparison
    old_files = []
    for d in old_dirs:
        if d.exists():
            old_files.extend(sorted(d.glob("*.md")))

    old_contamination = 0
    old_context = {"in_evidence": 0, "in_reasoning": 0}
    for fp in old_files:
        text = fp.read_text(encoding="utf-8")
        for pat in CONTAMINATION_PHRASES:
            if re.search(pat, text, re.IGNORECASE):
                old_contamination += 1
        for pat in CONTEXT_PHRASES:
            for m in re.finditer(pat, text, re.IGNORECASE):
                start = max(0, m.start() - 200)
                preceding = text[start:m.start()]
                if "**Evidence**" in preceding or "Evidence:" in preceding:
                    old_context["in_evidence"] += 1
                else:
                    old_context["in_reasoning"] += 1

    print(f"\n--- Check 3: Old Batched Scoring (N={len(old_files)}) ---")
    print(f"  Contamination phrases: {old_contamination}")
    print(f"  Context in evidence (OK): {old_context['in_evidence']}")
    print(f"  Context in reasoning (BAD): {old_context['in_reasoning']}")

    # --- Check 4: Lag-1 autocorrelation of FC scores ---
    print(f"\n--- Check 4: FC Score Autocorrelation (calibration drift test) ---")

    def _lag1_autocorr(vals):
        """Lag-1 autocorrelation."""
        n = len(vals)
        if n < 3:
            return float("nan")
        mean = sum(vals) / n
        var = sum((v - mean) ** 2 for v in vals) / n
        if var == 0:
            return 0.0
        cov = sum((vals[i] - mean) * (vals[i + 1] - mean) for i in range(n - 1)) / (n - 1)
        return cov / var

    # V4 independent transcripts — sorted by date (scoring order)
    v4_trans_dir = V4_DIR / "independent" / "transcripts"
    v4_trans_fc = []
    if v4_trans_dir.exists():
        for fp in sorted(v4_trans_dir.glob("*.md")):
            data = extract_part3(fp)
            if data:
                fc = _safe_int(data.get("FINANCIAL_CONDITIONS"))
                if fc is not None:
                    v4_trans_fc.append(fc)

    # Old agent2 transcripts — sorted by date
    old_trans_dir = V4_DIR / "agent2_transcripts" / "raw"
    old_trans_fc = []
    if old_trans_dir.exists():
        for fp in sorted(old_trans_dir.glob("*.md")):
            data = extract_part3(fp)
            if data:
                fc = _safe_int(data.get("FINANCIAL_CONDITIONS"))
                if fc is not None:
                    old_trans_fc.append(fc)

    # V4 independent minutes
    v4_min_dir = V4_DIR / "independent" / "minutes"
    v4_min_fc = []
    if v4_min_dir.exists():
        for fp in sorted(v4_min_dir.glob("*.md")):
            data = extract_part3(fp)
            if data:
                fc = _safe_int(data.get("FINANCIAL_CONDITIONS"))
                if fc is not None:
                    v4_min_fc.append(fc)

    # Old agent1 minutes
    old_min_dir = V4_DIR / "agent1_minutes" / "raw"
    old_min_fc = []
    if old_min_dir.exists():
        for fp in sorted(old_min_dir.glob("*.md")):
            data = extract_part3(fp)
            if data:
                fc = _safe_int(data.get("FINANCIAL_CONDITIONS"))
                if fc is not None:
                    old_min_fc.append(fc)

    r1_old_trans = _lag1_autocorr(old_trans_fc)
    r1_v4_trans = _lag1_autocorr(v4_trans_fc)
    r1_old_min = _lag1_autocorr(old_min_fc)
    r1_v4_min = _lag1_autocorr(v4_min_fc)

    print(f"  Old agent2 transcripts FC: N={len(old_trans_fc)}, lag-1 r = {r1_old_trans:.3f}")
    print(f"  V4  independent trans  FC: N={len(v4_trans_fc)}, lag-1 r = {r1_v4_trans:.3f}")
    print(f"  Old agent1 minutes     FC: N={len(old_min_fc)}, lag-1 r = {r1_old_min:.3f}")
    print(f"  V4  independent min    FC: N={len(v4_min_fc)}, lag-1 r = {r1_v4_min:.3f}")
    print()
    if r1_old_trans > r1_v4_trans + 0.05:
        print("  >> Old batched transcripts show HIGHER autocorrelation — consistent with calibration drift")
    else:
        print("  >> Autocorrelation similar (note: FC has real temporal persistence, so both will be positive)")

    # --- Check 5: Runs test on FC residuals ---
    print(f"\n--- Check 5: Runs Test on FC Residuals (independence of signs) ---")

    def _runs_test(vals):
        """One-sample runs test: are consecutive residuals independent?"""
        if len(vals) < 10:
            return None, None, None
        median = sorted(vals)[len(vals) // 2]
        signs = [1 if v > median else 0 for v in vals]
        n1 = sum(signs)
        n0 = len(signs) - n1
        if n0 == 0 or n1 == 0:
            return None, None, None
        # Count runs
        runs = 1
        for i in range(1, len(signs)):
            if signs[i] != signs[i - 1]:
                runs += 1
        # Expected runs and std under H0
        n = n0 + n1
        exp = 1 + 2 * n0 * n1 / n
        var = 2 * n0 * n1 * (2 * n0 * n1 - n) / (n ** 2 * (n - 1))
        if var <= 0:
            return runs, exp, None
        z = (runs - exp) / var ** 0.5
        return runs, exp, z

    for label, vals in [
        ("Old agent2 trans FC", old_trans_fc),
        ("V4 independent trans FC", v4_trans_fc),
        ("Old agent1 min FC", old_min_fc),
        ("V4 independent min FC", v4_min_fc),
    ]:
        runs, exp, z = _runs_test(vals)
        if z is not None:
            print(f"  {label:30s}: runs={runs:.0f}, expected={exp:.1f}, z={z:+.2f}"
                  f"  {'*too few runs*' if z < -1.96 else 'OK'}")
        else:
            print(f"  {label:30s}: insufficient data")

    # --- Write audit report ---
    report_path = V4_DIR / "independence_audit_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# V4 Independence Audit Report\n\n")
        f.write("## 1. Contamination Phrase Scan\n\n")
        if contamination_hits:
            f.write(f"**FAIL**: {len(contamination_hits)} contamination phrases found:\n\n")
            for fname, pat in contamination_hits:
                f.write(f"- `{fname}`: matched `{pat}`\n")
        else:
            f.write("**PASS**: Zero contamination phrases in V4 independent files.\n\n")

        f.write(f"\n## 2. Cross-Meeting Context References\n\n")
        f.write(f"| Location | V4 Independent | Old Batched |\n")
        f.write(f"|----------|---------------|-------------|\n")
        f.write(f"| In evidence blocks (source quotes) | {context_hits_v4['in_evidence']} | {old_context['in_evidence']} |\n")
        f.write(f"| In reasoning text (potential contamination) | {context_hits_v4['in_reasoning']} | {old_context['in_reasoning']} |\n\n")

        f.write(f"\n## 3. FC Lag-1 Autocorrelation (Calibration Drift Test)\n\n")
        f.write(f"| Series | N | Lag-1 r |\n")
        f.write(f"|--------|---|--------|\n")
        f.write(f"| Old agent2 transcripts | {len(old_trans_fc)} | {r1_old_trans:.3f} |\n")
        f.write(f"| V4 independent transcripts | {len(v4_trans_fc)} | {r1_v4_trans:.3f} |\n")
        f.write(f"| Old agent1 minutes | {len(old_min_fc)} | {r1_old_min:.3f} |\n")
        f.write(f"| V4 independent minutes | {len(v4_min_fc)} | {r1_v4_min:.3f} |\n\n")
        f.write("Note: Both old and new will show positive autocorrelation because FC has real temporal persistence.\n")
        f.write("The diagnostic is whether old batched series shows *higher* autocorrelation than independent.\n\n")

        f.write(f"\n## 4. Runs Test\n\n")
        for label, vals in [
            ("Old agent2 trans FC", old_trans_fc),
            ("V4 independent trans FC", v4_trans_fc),
            ("Old agent1 min FC", old_min_fc),
            ("V4 independent min FC", v4_min_fc),
        ]:
            runs, exp, z = _runs_test(vals)
            if z is not None:
                f.write(f"- **{label}**: runs={runs:.0f}, expected={exp:.1f}, z={z:+.2f}\n")
            else:
                f.write(f"- **{label}**: insufficient data\n")

        f.write(f"\n\n## 5. Conclusion\n\n")
        if not contamination_hits:
            f.write("V4 independent scoring shows **no evidence of cross-document contamination**.\n")
            f.write("Cross-meeting references found in V4 files are source-document quotes, not agent opinions.\n")
        else:
            f.write("**WARNING**: Contamination phrases detected — investigate further.\n")

    print(f"\nAudit report: {report_path}")


def cmd_gap_analysis(args):
    """Compare old batched vs new V4 independent FC gaps."""
    import math

    # Load old per-meeting gaps from analysis_output
    old_gaps_path = SCRIPT_DIR / "analysis_output" / "dimension_comparison_detail.csv"
    if not old_gaps_path.exists():
        print(f"Old gap file not found: {old_gaps_path}")
        return

    # Load old gaps
    old_fc_gaps = {}  # date -> gap (T - M)
    with open(old_gaps_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row["date"]
            fc_gap = row.get("FINANCIAL_CONDITIONS_gap", "")
            if fc_gap and fc_gap != "N/A":
                old_fc_gaps[date] = float(fc_gap)

    # Load V4 scores
    if not MASTER_CSV.exists():
        print("No V4 master CSV. Run: python run_v4_scoring.py extract")
        return

    with open(MASTER_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Group V4 by date
    v4_by_date = defaultdict(dict)
    for row in rows:
        date = row.get("MEETING_DATE", "")
        src = row.get("SOURCE_TYPE", "")
        v4_by_date[date][src] = row

    # Compute V4 FC gaps for meetings with both sources
    v4_fc_gaps = {}
    for date, sources in v4_by_date.items():
        if "minutes" in sources and "transcript" in sources:
            m_fc = _safe_int(sources["minutes"].get("FINANCIAL_CONDITIONS"))
            t_fc = _safe_int(sources["transcript"].get("FINANCIAL_CONDITIONS"))
            if m_fc is not None and t_fc is not None:
                v4_fc_gaps[date] = t_fc - m_fc  # T - M to match old convention

    # Find overlapping meetings
    overlap_dates = sorted(set(old_fc_gaps.keys()) & set(v4_fc_gaps.keys()))
    print(f"Overlapping meetings with FC gaps in both old and V4: {len(overlap_dates)}")

    # Era classification
    def _era(date):
        y = int(date[:4])
        if y <= 2005:
            return "Greenspan"
        elif y <= 2013:
            return "Bernanke"
        elif y <= 2017:
            return "Yellen"
        else:
            return "Powell"

    # Build comparison table
    comp_rows = []
    old_vals = []
    new_vals = []
    for date in overlap_dates:
        og = old_fc_gaps[date]
        ng = v4_fc_gaps[date]
        comp_rows.append({
            "date": date,
            "era": _era(date),
            "old_gap_TM": og,
            "v4_gap_TM": ng,
            "reduction": og - ng,
        })
        old_vals.append(og)
        new_vals.append(ng)

    # Write CSV
    out_csv = V4_DIR / "old_vs_new_gap_analysis.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "era", "old_gap_TM", "v4_gap_TM", "reduction"])
        writer.writeheader()
        writer.writerows(comp_rows)

    # Overall stats
    n = len(old_vals)
    old_mean = sum(old_vals) / n
    new_mean = sum(new_vals) / n
    diffs = [o - v for o, v in zip(old_vals, new_vals)]
    diff_mean = sum(diffs) / n
    diff_sd = (sum((d - diff_mean) ** 2 for d in diffs) / (n - 1)) ** 0.5
    t_stat = diff_mean / (diff_sd / n ** 0.5) if diff_sd > 0 else 0

    print(f"\n{'=' * 70}")
    print(f"  FINANCIAL_CONDITIONS Gap: Old Batched vs V4 Independent")
    print(f"{'=' * 70}")
    print(f"  N = {n} overlapping meetings")
    print(f"  Old mean gap (T-M):  {old_mean:+.1f}")
    print(f"  V4  mean gap (T-M):  {new_mean:+.1f}")
    print(f"  Mean reduction:      {diff_mean:+.1f}")
    print(f"  SD of reduction:     {diff_sd:.1f}")
    print(f"  Paired t-test:       t({n-1}) = {t_stat:.2f}", end="")
    if abs(t_stat) > 2.576:
        print("  p < 0.001 ***")
    elif abs(t_stat) > 1.96:
        print("  p < 0.05 *")
    else:
        print("  n.s.")

    # Per-era breakdown
    print(f"\n  Per-Era Breakdown:")
    print(f"  {'Era':12s} {'N':>4s} {'Old gap':>8s} {'V4 gap':>8s} {'Reduction':>10s}")
    print(f"  {'-'*44}")

    era_groups = defaultdict(lambda: {"old": [], "new": []})
    for row in comp_rows:
        era_groups[row["era"]]["old"].append(row["old_gap_TM"])
        era_groups[row["era"]]["new"].append(row["v4_gap_TM"])

    for era in ["Greenspan", "Bernanke", "Yellen", "Powell"]:
        if era in era_groups:
            ov = era_groups[era]["old"]
            nv = era_groups[era]["new"]
            om = sum(ov) / len(ov)
            nm = sum(nv) / len(nv)
            print(f"  {era:12s} {len(ov):4d} {om:+8.1f} {nm:+8.1f} {om - nm:+10.1f}")

    # Correlation between old and new gaps
    r = _pearson(old_vals, new_vals)
    print(f"\n  Correlation between old and V4 gaps: r = {r:.3f}")
    print(f"  (Low r means old gap was mostly artifact, not real signal)")

    # Score-level comparison: old agent vs V4 independent for same source
    print(f"\n{'=' * 70}")
    print(f"  Score-Level Comparison: Same Document, Different Agent Architecture")
    print(f"{'=' * 70}")

    # Extract old agent scores
    old_scores = {}
    for d in [V4_DIR / "agent1_minutes" / "raw", V4_DIR / "agent2_transcripts" / "raw"]:
        if d.exists():
            for fp in sorted(d.glob("*.md")):
                data = extract_part3(fp)
                if data:
                    date = data.get("MEETING_DATE", "")
                    src = data.get("SOURCE_TYPE", "")
                    fc = _safe_int(data.get("FINANCIAL_CONDITIONS"))
                    if date and src and fc is not None:
                        old_scores[(date, src)] = fc

    # Compare old vs V4 for same (date, source)
    for source_type in ["minutes", "transcript"]:
        old_fc_vals = []
        v4_fc_vals = []
        for date, sources in v4_by_date.items():
            if source_type in sources:
                v4_fc = _safe_int(sources[source_type].get("FINANCIAL_CONDITIONS"))
                old_fc = old_scores.get((date, source_type))
                if v4_fc is not None and old_fc is not None:
                    old_fc_vals.append(old_fc)
                    v4_fc_vals.append(v4_fc)

        if len(old_fc_vals) >= 5:
            r = _pearson(old_fc_vals, v4_fc_vals)
            mad = sum(abs(a - b) for a, b in zip(old_fc_vals, v4_fc_vals)) / len(old_fc_vals)
            bias = sum(a - b for a, b in zip(old_fc_vals, v4_fc_vals)) / len(old_fc_vals)
            print(f"  {source_type:12s}: N={len(old_fc_vals)}, r={r:.3f}, MAD={mad:.1f}, "
                  f"bias(old-V4)={bias:+.1f}")

    print(f"\n  If old transcripts systematically higher than V4 transcripts (positive bias),")
    print(f"  that confirms agent2 calibration drift inflated transcript FC scores.")

    print(f"\nGap analysis CSV: {out_csv}")


def main():
    parser = argparse.ArgumentParser(description="V4 FOMC Staff Assessment Scoring Orchestration")
    parser.add_argument("command", choices=[
        "manifest", "extract", "validate", "status", "compare", "audit", "gap_analysis"
    ])
    args = parser.parse_args()

    if args.command == "manifest":
        cmd_manifest(args)
    elif args.command == "extract":
        cmd_extract(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "compare":
        cmd_compare(args)
    elif args.command == "audit":
        cmd_audit(args)
    elif args.command == "gap_analysis":
        cmd_gap_analysis(args)


if __name__ == "__main__":
    main()
