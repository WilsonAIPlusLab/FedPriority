# LEGACY (2026-10-17): this script reads the OLD decomposition tree 03_decomposition/output/, which is stale (defective two-column text, pre-rebuild).
# It is kept to reproduce the historical (V3-era / pre-rebuild) results. For new work use 03_decomposition/output_rebuild/ and build_member_discussion_v2.py.
"""
V3 FOMC Discussion Scoring — Orchestration Helpers

This script provides:
1. Manifest generation (which documents to score, in what order)
2. Output parsing (extract Part 3 structured blocks from scored .md files)
3. Quality checks (anchor validation, cross-dimension consistency)
4. Independent scoring support (one agent per document, calibration chain)

The actual scoring is done by Claude agents in an interactive session,
NOT via API calls. Each agent receives the v3 prompt + one source document
and writes its output to v3_scores/{agent}/raw/{source_type}_{date}.md

For independent scoring, each agent is fresh (no shared context) and receives
the previous meeting's Part 3 block as calibration context. Output goes to
v3_scores/independent/{minutes|transcripts}/{type}_{date}.md

Usage:
    python run_v3_scoring.py manifest              # Generate scoring manifest (batched)
    python run_v3_scoring.py manifest_independent   # Generate manifest for independent scoring
    python run_v3_scoring.py extract               # Parse batched scored files → CSV
    python run_v3_scoring.py extract_independent   # Parse independent scored files → CSV
    python run_v3_scoring.py validate              # Run quality checks on extracted CSV
    python run_v3_scoring.py status                # Show batched scoring progress
    python run_v3_scoring.py status_independent    # Show independent scoring progress
    python run_v3_scoring.py prepare_agent         # Print agent prompt for next unscored doc
    python run_v3_scoring.py compare               # Compare old batched vs independent scores
"""

import csv
import json
import re
import sys
import random
import argparse
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
RUBRIC_DIR = SCRIPT_DIR / "rubric_v3"
V3_DIR = SCRIPT_DIR / "v3_scores"
MINUTES_SRC = SCRIPT_DIR.parent.parent / "03_decomposition" / "output" / "member_discussion" / "minutes"
TRANSCRIPTS_SRC = SCRIPT_DIR.parent.parent / "03_decomposition" / "output" / "member_discussion" / "transcripts"

MANIFEST_PATH = V3_DIR / "manifest.csv"
MASTER_CSV = V3_DIR / "all_scores_v3.csv"
ANCHOR_CSV = RUBRIC_DIR / "anchor_meetings.csv"

# Independent scoring paths
INDEP_DIR = V3_DIR / "independent"
INDEP_MINUTES_DIR = INDEP_DIR / "minutes"
INDEP_TRANSCRIPTS_DIR = INDEP_DIR / "transcripts"
INDEP_MANIFEST_PATH = INDEP_DIR / "manifest.csv"
INDEP_MASTER_CSV = INDEP_DIR / "all_scores_v3_independent.csv"
INDEP_PROMPT_PATH = RUBRIC_DIR / "FOMC_Discussion_Scoring_Prompt_v3_independent.md"

# V3 column names
CORE_DIMS = [
    "INFLATION_PRESSURE", "OUTPUT_GAP", "LABOR_TIGHTNESS",
    "CONSUMPTION_INVESTMENT", "FINANCIAL_TIGHTNESS",
    "HAWKISH_DOVISH_LEAN", "DISSENT_INTENSITY",
    "FORWARD_GUIDANCE_TONE",
    "UNCERTAINTY_EXPRESSED",
]

OPTIONAL_DIMS = [
    "INFLATION_GOODS", "INFLATION_SERVICES", "INFLATION_HOUSING",
    "INFLATION_EXPECTATIONS", "CREDIT_STRESS", "EQUITY_STRESS",
    "BANKING_STRESS", "TREASURY_STRESS", "DOLLAR_CONCERN", "PRODUCTIVITY",
]

ALL_COLUMNS = (
    ["MEETING_DATE", "SOURCE_TYPE"]
    + [f for d in CORE_DIMS for f in (d, f"{d}_UNC", f"{d}_CONF")]
    + OPTIONAL_DIMS
    + ["ANOMALY_FLAG", "ANOMALY_NOTE"]
)


def cmd_manifest(args):
    """Generate the scoring manifest."""
    V3_DIR.mkdir(parents=True, exist_ok=True)

    rows = []

    # Minutes
    for f in sorted(MINUTES_SRC.glob("*.txt")):
        date = f.stem
        rows.append({
            "meeting_date": date,
            "source_type": "minutes",
            "source_path": str(f),
            "output_path": str(V3_DIR / "agent1_minutes" / "raw" / f"minutes_{date}.md"),
            "status": "pending",
        })

    # Transcripts
    for f in sorted(TRANSCRIPTS_SRC.glob("*.txt")):
        date = f.stem
        rows.append({
            "meeting_date": date,
            "source_type": "transcript",
            "source_path": str(f),
            "output_path": str(V3_DIR / "agent2_transcripts" / "raw" / f"transcript_{date}.md"),
            "status": "pending",
        })

    with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "meeting_date", "source_type", "source_path", "output_path", "status"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Manifest written: {len(rows)} documents ({sum(1 for r in rows if r['source_type']=='minutes')} minutes, "
          f"{sum(1 for r in rows if r['source_type']=='transcript')} transcripts)")
    print(f"  Path: {MANIFEST_PATH}")


def cmd_status(args):
    """Show scoring progress."""
    if not MANIFEST_PATH.exists():
        print("No manifest found. Run: python run_v3_scoring.py manifest")
        return

    with open(MANIFEST_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Check which output files exist
    scored = 0
    pending = 0
    for row in rows:
        if Path(row["output_path"]).exists():
            scored += 1
        else:
            pending += 1

    total = len(rows)
    minutes_scored = sum(1 for r in rows if r["source_type"] == "minutes" and Path(r["output_path"]).exists())
    transcripts_scored = sum(1 for r in rows if r["source_type"] == "transcript" and Path(r["output_path"]).exists())
    minutes_total = sum(1 for r in rows if r["source_type"] == "minutes")
    transcripts_total = sum(1 for r in rows if r["source_type"] == "transcript")

    print(f"Scoring Progress:")
    print(f"  Total:       {scored}/{total} ({scored/total*100:.1f}%)")
    print(f"  Minutes:     {minutes_scored}/{minutes_total}")
    print(f"  Transcripts: {transcripts_scored}/{transcripts_total}")
    print(f"  Pending:     {pending}")


def extract_part3(filepath: Path) -> dict | None:
    """Extract key-value pairs from Part 3 structured output block."""
    text = filepath.read_text(encoding="utf-8")

    # Find the Part 3 code block (case-insensitive header, optional language tag)
    match = re.search(r"##\s*Part\s*3.*?```(?:\w*)\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if not match:
        # Try alternate pattern without header
        match = re.search(r"MEETING_DATE:.*?(?:ANOMALY_NOTE:.*|PRODUCTIVITY:.*)", text, re.DOTALL)
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
            combined = re.match(r"^(\d+)\s*[±\xb1]?\s*[+\-]*\s*(\d+)\s+(High|Moderate|Low)$", value)
            if combined and key in CORE_DIMS:
                data[key] = combined.group(1)
                data[f"{key}_UNC"] = combined.group(2)
                data[f"{key}_CONF"] = combined.group(3)
            else:
                data[key] = value

    return data


def _extract_yaml_format(block: str) -> dict:
    """Extract scores from YAML nested format (score/uncertainty_band/confidence subkeys)."""
    data = {}
    current_dim = None

    for line in block.strip().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("---") or stripped.startswith("#"):
            continue

        # Top-level key: value (MEETING_DATE, SOURCE_TYPE, etc.)
        if not line.startswith(" ") and not line.startswith("\t") and ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            if value and key in ("MEETING_DATE", "SOURCE_TYPE", "AGENT",
                                  "ANOMALY_FLAG", "ANOMALY_NOTE"):
                data[key] = value
            continue

        # Section headers like CORE_DIMENSIONS: or OPTIONAL_DIMENSIONS:
        if stripped.endswith(":") and stripped.isupper():
            continue

        # Dimension name (indented, ends with colon, no value on same line)
        indent = len(line) - len(line.lstrip())
        if indent <= 4 and stripped.endswith(":") and not stripped.startswith("score") \
                and not stripped.startswith("uncertainty") and not stripped.startswith("confidence") \
                and not stripped.startswith("key_evidence"):
            current_dim = stripped[:-1].strip()
            continue

        # Subkeys under a dimension
        if current_dim and ":" in stripped:
            subkey, _, subval = stripped.partition(":")
            subkey = subkey.strip()
            subval = subval.strip()

            if subkey == "score":
                data[current_dim] = subval
            elif subkey == "uncertainty_band":
                # Parse [lo, hi] -> +-X format
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
    # Top-level fields
    if "meeting_date" in obj:
        data["MEETING_DATE"] = obj["meeting_date"]
    if "source_type" in obj:
        data["SOURCE_TYPE"] = obj["source_type"]

    # Tier 1 and tier 2 dimensions
    for tier_key in ("tier1", "tier2"):
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

    # Skipped tier 2 dims = N/A
    for dim in obj.get("tier2_skipped", []):
        data[dim] = "N/A"

    # Anomaly
    data["ANOMALY_FLAG"] = obj.get("anomaly_flag", obj.get("ANOMALY_FLAG", "No"))
    data["ANOMALY_NOTE"] = obj.get("anomaly_note", obj.get("ANOMALY_NOTE", obj.get("notes", "")))

    return data


def cmd_extract(args):
    """Parse all scored files and produce master CSV."""
    V3_DIR.mkdir(parents=True, exist_ok=True)

    raw_dirs = [
        V3_DIR / "agent1_minutes" / "raw",
        V3_DIR / "agent2_transcripts" / "raw",
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
            # Clean up uncertainty format
            if col.endswith("_UNC"):
                raw = raw.replace("+-", "").replace("±", "").strip()
            row[col] = raw

        rows.append(row)

    # Write master CSV
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
        print("No master CSV found. Run: python run_v3_scoring.py extract")
        return

    with open(MASTER_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Validating {len(rows)} scored meetings...\n")

    flags = []

    for row in rows:
        date = row.get("MEETING_DATE", "???")
        src = row.get("SOURCE_TYPE", "???")
        label = f"{src}_{date}"

        # Check 1: No zeros or out-of-range
        for dim in CORE_DIMS:
            val = row.get(dim, "")
            if val and val != "N/A":
                try:
                    v = int(val)
                    if v < 1 or v > 100:
                        flags.append(f"[RANGE] {label}: {dim}={v} (out of 1-100)")
                    if v == 0:
                        flags.append(f"[ZERO] {label}: {dim}=0 (illegal)")
                except ValueError:
                    flags.append(f"[PARSE] {label}: {dim}='{val}' (not integer)")

        # Check 2: Cross-dimension consistency
        og = _safe_int(row.get("OUTPUT_GAP"))
        lt = _safe_int(row.get("LABOR_TIGHTNESS"))
        if og is not None and lt is not None:
            if og < 25 and lt > 65:
                flags.append(f"[CROSS] {label}: OUTPUT_GAP={og} but LABOR_TIGHTNESS={lt} (recession + tight labor?)")
            if og > 70 and lt < 30:
                flags.append(f"[CROSS] {label}: OUTPUT_GAP={og} but LABOR_TIGHTNESS={lt} (overheating + slack?)")

        hdl = _safe_int(row.get("HAWKISH_DOVISH_LEAN"))
        fgt = _safe_int(row.get("FORWARD_GUIDANCE_TONE"))
        if hdl is not None and fgt is not None:
            if abs(hdl - fgt) > 40:
                flags.append(f"[CROSS] {label}: HAWKISH_DOVISH={hdl} vs FORWARD_GUIDANCE={fgt} (delta={abs(hdl-fgt)})")

    # Check 3: Anchor meetings
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
            print(f"  {dim:30s}: N={len(vals):3d}  mean={sum(vals)/len(vals):5.1f}  "
                  f"min={min(vals):3d}  max={max(vals):3d}  range={max(vals)-min(vals)}")

    print(f"\n=== Flags ({len(flags)}) ===")
    for f in flags:
        print(f"  {f}")

    # Write quality report
    report_path = V3_DIR / "quality_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# V3 Scoring Quality Report\n\n")
        f.write(f"Total scored: {len(rows)}\n")
        f.write(f"Total flags: {len(flags)}\n\n")
        for flag in flags:
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
            for dim in ["INFLATION_PRESSURE", "OUTPUT_GAP", "LABOR_TIGHTNESS",
                         "HAWKISH_DOVISH_LEAN", "FINANCIAL_TIGHTNESS"]:
                lo_key = f"{dim}_min"
                hi_key = f"{dim}_max"
                if lo_key in row and hi_key in row:
                    anchor[dim] = (int(row[lo_key]), int(row[hi_key]))
            anchors[key] = anchor
    return anchors


def cmd_manifest_independent(args):
    """Generate manifest for independent scoring with calibration chain."""
    INDEP_DIR.mkdir(parents=True, exist_ok=True)
    INDEP_MINUTES_DIR.mkdir(parents=True, exist_ok=True)
    INDEP_TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    rows = []

    # Minutes — chronological order (calibration chain)
    minutes_files = sorted(MINUTES_SRC.glob("*.txt"))
    prev_minutes = ""
    for f in minutes_files:
        date = f.stem
        output_path = INDEP_MINUTES_DIR / f"minutes_{date}.md"
        rows.append({
            "meeting_date": date,
            "source_type": "minutes",
            "source_path": str(f),
            "output_path": str(output_path),
            "prev_scored_path": prev_minutes,
            "status": "pending",
        })
        prev_minutes = str(output_path)

    # Transcripts — chronological order
    transcript_files = sorted(TRANSCRIPTS_SRC.glob("*.txt"))
    prev_transcript = ""
    for f in transcript_files:
        date = f.stem
        output_path = INDEP_TRANSCRIPTS_DIR / f"transcript_{date}.md"
        rows.append({
            "meeting_date": date,
            "source_type": "transcript",
            "source_path": str(f),
            "output_path": str(output_path),
            "prev_scored_path": prev_transcript,
            "status": "pending",
        })
        prev_transcript = str(output_path)

    with open(INDEP_MANIFEST_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "meeting_date", "source_type", "source_path", "output_path",
            "prev_scored_path", "status"
        ])
        writer.writeheader()
        writer.writerows(rows)

    n_min = sum(1 for r in rows if r["source_type"] == "minutes")
    n_trans = sum(1 for r in rows if r["source_type"] == "transcript")
    print(f"Independent manifest written: {len(rows)} documents ({n_min} minutes, {n_trans} transcripts)")
    print(f"  Path: {INDEP_MANIFEST_PATH}")
    print(f"  Output dirs: {INDEP_MINUTES_DIR}")
    print(f"               {INDEP_TRANSCRIPTS_DIR}")


def _extract_part3_block(filepath: Path) -> str:
    """Extract raw Part 3 text block from a scored .md file (for calibration context)."""
    text = filepath.read_text(encoding="utf-8")
    match = re.search(r"##\s*Part\s*3.*?```(?:\w*)\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Fallback: find key-value block starting with MEETING_DATE
    match = re.search(r"(MEETING_DATE:.*?)(?:\n\n|\Z)", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def cmd_status_independent(args):
    """Show independent scoring progress."""
    if not INDEP_MANIFEST_PATH.exists():
        print("No independent manifest. Run: python run_v3_scoring.py manifest_independent")
        return

    with open(INDEP_MANIFEST_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    minutes_rows = [r for r in rows if r["source_type"] == "minutes"]
    transcript_rows = [r for r in rows if r["source_type"] == "transcript"]

    def count_done(row_list):
        return sum(1 for r in row_list if Path(r["output_path"]).exists())

    m_done = count_done(minutes_rows)
    t_done = count_done(transcript_rows)
    total_done = m_done + t_done
    total = len(rows)

    print(f"Independent Scoring Progress:")
    print(f"  Total:       {total_done}/{total} ({total_done/total*100:.1f}%)")
    print(f"  Minutes:     {m_done}/{len(minutes_rows)}")
    print(f"  Transcripts: {t_done}/{len(transcript_rows)}")

    # Show next pending for each track
    for label, track in [("Minutes", minutes_rows), ("Transcripts", transcript_rows)]:
        for r in track:
            if not Path(r["output_path"]).exists():
                print(f"  Next {label}: {r['meeting_date']}")
                break


def cmd_prepare_agent(args):
    """Print the full agent prompt for the next unscored document in each track."""
    if not INDEP_MANIFEST_PATH.exists():
        print("No independent manifest. Run: python run_v3_scoring.py manifest_independent")
        return

    if not INDEP_PROMPT_PATH.exists():
        print(f"Missing prompt: {INDEP_PROMPT_PATH}")
        return

    prompt_template = INDEP_PROMPT_PATH.read_text(encoding="utf-8")

    with open(INDEP_MANIFEST_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Parse optional --track flag
    track_filter = getattr(args, "track", None)

    for source_type in ["minutes", "transcript"]:
        if track_filter and track_filter != source_type:
            continue

        track_rows = [r for r in rows if r["source_type"] == source_type]
        for r in track_rows:
            if Path(r["output_path"]).exists():
                continue

            # This is the next unscored document
            date = r["meeting_date"]
            src_path = Path(r["source_path"])
            prev_path = r.get("prev_scored_path", "")

            # Build calibration block
            if prev_path and Path(prev_path).exists():
                cal_block = _extract_part3_block(Path(prev_path))
                if not cal_block:
                    cal_block = "Previous meeting scored file exists but Part 3 block could not be extracted."
            else:
                cal_block = "No previous meeting (first in series). Use anchor tables for calibration."

            # Build full prompt
            full_prompt = prompt_template.replace("{{CALIBRATION_BLOCK}}", cal_block)

            # Read source document
            source_text = src_path.read_text(encoding="utf-8")

            print(f"=== NEXT: {source_type} {date} ===")
            print(f"Source: {src_path}")
            print(f"Output: {r['output_path']}")
            print(f"Prev:   {prev_path or '(none — first in series)'}")
            print(f"Calibration block length: {len(cal_block)} chars")
            print()

            # Write the assembled prompt to a temp file for agent consumption
            assembled_path = INDEP_DIR / f"_next_{source_type}_prompt.md"
            with open(assembled_path, "w", encoding="utf-8") as out:
                out.write(full_prompt)
                out.write("\n\n---\n\n# SOURCE DOCUMENT\n\n")
                out.write(f"**Meeting date**: {date}\n")
                out.write(f"**Source type**: {source_type}\n\n")
                out.write(source_text)

            print(f"Assembled prompt written to: {assembled_path}")
            break  # Only show next unscored per track
        else:
            print(f"=== {source_type}: ALL DONE ===")


def cmd_extract_independent(args):
    """Parse all independently scored files and produce master CSV."""
    raw_dirs = [INDEP_MINUTES_DIR, INDEP_TRANSCRIPTS_DIR]

    all_files = []
    for d in raw_dirs:
        if d.exists():
            all_files.extend(sorted(d.glob("*.md")))

    # Exclude temp/prompt files
    all_files = [f for f in all_files if not f.name.startswith("_")]

    print(f"Found {len(all_files)} independently scored files")

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

    with open(INDEP_MASTER_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ALL_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Extracted {len(rows)} rows -> {INDEP_MASTER_CSV}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(e)


def cmd_compare(args):
    """Compare old batched vs independent discussion scores."""
    if not MASTER_CSV.exists():
        print(f"Missing batched CSV: {MASTER_CSV}")
        return
    if not INDEP_MASTER_CSV.exists():
        print(f"Missing independent CSV: {INDEP_MASTER_CSV}")
        return

    with open(MASTER_CSV, encoding="utf-8") as f:
        old_rows = {(r["MEETING_DATE"], r["SOURCE_TYPE"]): r for r in csv.DictReader(f)}
    with open(INDEP_MASTER_CSV, encoding="utf-8") as f:
        new_rows = {(r["MEETING_DATE"], r["SOURCE_TYPE"]): r for r in csv.DictReader(f)}

    common_keys = sorted(set(old_rows) & set(new_rows))
    print(f"Common meetings: {len(common_keys)}")

    dims_to_compare = CORE_DIMS + OPTIONAL_DIMS

    print(f"\n{'Dimension':40s} {'N':>4s} {'r':>6s} {'MAD':>6s} {'Bias(new-old)':>14s}")
    print("-" * 74)

    for dim in dims_to_compare:
        old_vals, new_vals = [], []
        for key in common_keys:
            ov = _safe_int(old_rows[key].get(dim))
            nv = _safe_int(new_rows[key].get(dim))
            if ov is not None and nv is not None:
                old_vals.append(ov)
                new_vals.append(nv)

        if len(old_vals) < 5:
            continue

        n = len(old_vals)
        mad = sum(abs(o - n_) for o, n_ in zip(old_vals, new_vals)) / n
        bias = sum(n_ - o for o, n_ in zip(old_vals, new_vals)) / n
        r = _pearson(old_vals, new_vals)

        print(f"  {dim:38s} {n:4d} {r:6.3f} {mad:6.1f} {bias:+14.1f}")

    # Minutes vs transcript gap comparison (old batched vs new independent)
    print(f"\n=== Minutes-Transcript Gap: Old Batched vs New Independent ===")
    print(f"{'Dimension':40s} {'N':>4s} {'Old Gap':>9s} {'New Gap':>9s} {'Change':>9s}")
    print("-" * 74)

    # Build paired meetings for each version
    for dim in dims_to_compare:
        old_gaps, new_gaps = [], []

        # Get all dates that have both minutes and transcript in both versions
        old_min = {k[0]: _safe_int(old_rows[k].get(dim))
                   for k in old_rows if k[1] == "minutes"}
        old_trans = {k[0]: _safe_int(old_rows[k].get(dim))
                     for k in old_rows if k[1] == "transcript"}
        new_min = {k[0]: _safe_int(new_rows[k].get(dim))
                   for k in new_rows if k[1] == "minutes"}
        new_trans = {k[0]: _safe_int(new_rows[k].get(dim))
                     for k in new_rows if k[1] == "transcript"}

        common_dates = sorted(
            set(old_min) & set(old_trans) & set(new_min) & set(new_trans)
        )

        for d in common_dates:
            om, ot = old_min[d], old_trans[d]
            nm, nt = new_min[d], new_trans[d]
            if all(v is not None for v in [om, ot, nm, nt]):
                old_gaps.append(om - ot)
                new_gaps.append(nm - nt)

        if len(old_gaps) < 5:
            continue

        n = len(old_gaps)
        old_mean = sum(old_gaps) / n
        new_mean = sum(new_gaps) / n

        print(f"  {dim:38s} {n:4d} {old_mean:+9.1f} {new_mean:+9.1f} {new_mean - old_mean:+9.1f}")


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


def main():
    parser = argparse.ArgumentParser(description="V3 FOMC Discussion Scoring Orchestration")
    parser.add_argument("command", choices=[
        "manifest", "extract", "validate", "status",
        "manifest_independent", "extract_independent",
        "status_independent", "prepare_agent", "compare"
    ])
    parser.add_argument("--track", choices=["minutes", "transcript"],
                        help="Filter to one track (for prepare_agent)")
    args = parser.parse_args()

    cmds = {
        "manifest": cmd_manifest,
        "extract": cmd_extract,
        "validate": cmd_validate,
        "status": cmd_status,
        "manifest_independent": cmd_manifest_independent,
        "extract_independent": cmd_extract_independent,
        "status_independent": cmd_status_independent,
        "prepare_agent": cmd_prepare_agent,
        "compare": cmd_compare,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
