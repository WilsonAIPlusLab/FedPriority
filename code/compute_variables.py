"""
Compute meeting-level variables from classified sentences.

Aggregates sentence-level topic classifications into FSS, DMS, CDFSG,
and within-transcript gap variables.

Usage:
    python compute_variables.py
    python compute_variables.py --input data/classified_sentences.csv
"""

import csv
import sys
import argparse
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    CLASSIFIED_SENTENCES_CSV, MEETING_VARIABLES_CSV, DATA_DIR,
    CRISIS_MEETINGS, TOPIC_CATEGORIES,
)


def load_classified_sentences(csv_path):
    """Load classified sentences from CSV."""
    with open(str(csv_path), "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_topic_shares(sentences):
    """Compute topic share (fraction) for a group of sentences.

    Returns dict: topic → share (0.0 to 1.0)
    """
    total = len(sentences)
    if total == 0:
        return {t: 0.0 for t in TOPIC_CATEGORIES}

    counts = defaultdict(int)
    for s in sentences:
        topic = s.get("topic", "OTHER")
        counts[topic] += 1

    return {t: counts.get(t, 0) / total for t in TOPIC_CATEGORIES}


def compute_meeting_variables(sentences):
    """Compute all meeting-level variables.

    Returns list of dicts, one per meeting, with FSS, FCS, DMS, CDFSG, etc.
    """
    # Group by meeting_date × doc_type × section
    groups = defaultdict(list)
    for s in sentences:
        meeting = s.get("meeting_date", "")
        doc_type = s.get("doc_type", "")
        section = s.get("section", "")
        if not meeting or not doc_type:
            continue
        groups[(meeting, doc_type)].append(s)
        groups[(meeting, doc_type, section)].append(s)

    # Get unique meetings
    meetings = sorted(set(s.get("meeting_date", "") for s in sentences if s.get("meeting_date")))

    results = []
    for meeting in meetings:
        row = {"meeting_date": meeting}

        # For each document type, compute topic shares
        for doc_type in ["transcript", "minutes", "statement", "speech"]:
            key = (meeting, doc_type)
            sents = groups.get(key, [])
            n = len(sents)
            row[f"n_{doc_type}"] = n

            if n > 0:
                shares = compute_topic_shares(sents)
                # V2 taxonomy: FINANCIAL_STABILITY + FINANCIAL_CONDITIONS merged into FINANCIAL.
                # FSS = share of FINANCIAL sentences (for CDFSG computation).
                # For V1 data (FINANCIAL_STABILITY / FINANCIAL_CONDITIONS split), fall back.
                fin_share = shares.get("FINANCIAL", 0)
                fss_v1    = shares.get("FINANCIAL_STABILITY", 0)
                fcs_v1    = shares.get("FINANCIAL_CONDITIONS", 0)
                row[f"FSS_{doc_type}"] = round(fin_share if fin_share > 0 else fss_v1, 4)
                row[f"FCS_{doc_type}"] = round(fcs_v1, 4)   # always 0 under V2
                row[f"INF_{doc_type}"] = round(shares.get("INFLATION", 0), 4)
                row[f"EMP_{doc_type}"] = round(shares.get("EMPLOYMENT_OUTPUT", 0), 4)
                row[f"REG_{doc_type}"] = round(shares.get("REGULATION_SUPERVISION", 0), 4)
                row[f"OTH_{doc_type}"] = round(shares.get("OTHER", 0), 4)
                row[f"DMS_{doc_type}"] = round(
                    shares.get("INFLATION", 0) + shares.get("EMPLOYMENT_OUTPUT", 0), 4
                )
            else:
                for prefix in ["FSS", "FCS", "INF", "EMP", "REG", "OTH", "DMS"]:
                    row[f"{prefix}_{doc_type}"] = ""

        # Cross-document gaps (CDFSG)
        fss_transcript = row.get("FSS_transcript", "")
        fss_statement = row.get("FSS_statement", "")
        fss_minutes = row.get("FSS_minutes", "")
        fss_speech = row.get("FSS_speech", "")

        # CDFSG = FSS_transcript - FSS_statement
        if fss_transcript != "" and fss_statement != "":
            row["CDFSG"] = round(float(fss_transcript) - float(fss_statement), 4)
        else:
            row["CDFSG"] = ""

        # CDFSG_minutes = FSS_transcript - FSS_minutes
        if fss_transcript != "" and fss_minutes != "":
            row["CDFSG_minutes"] = round(float(fss_transcript) - float(fss_minutes), 4)
        else:
            row["CDFSG_minutes"] = ""

        # CDFSG_speech = FSS_transcript - FSS_speech
        if fss_transcript != "" and fss_speech != "":
            row["CDFSG_speech"] = round(float(fss_transcript) - float(fss_speech), 4)
        else:
            row["CDFSG_speech"] = ""

        # Within-transcript gap (FOMC1 vs FOMC2)
        fomc1_sents = groups.get((meeting, "transcript", "FOMC1"), [])
        fomc2_sents = groups.get((meeting, "transcript", "FOMC2"), [])

        row["n_FOMC1"] = len(fomc1_sents)
        row["n_FOMC2"] = len(fomc2_sents)

        if fomc1_sents:
            fomc1_shares = compute_topic_shares(fomc1_sents)
            fs1 = fomc1_shares.get("FINANCIAL", fomc1_shares.get("FINANCIAL_STABILITY", 0))
            row["FSS_FOMC1"] = round(fs1, 4)
        else:
            row["FSS_FOMC1"] = ""

        if fomc2_sents:
            fomc2_shares = compute_topic_shares(fomc2_sents)
            fs2 = fomc2_shares.get("FINANCIAL", fomc2_shares.get("FINANCIAL_STABILITY", 0))
            row["FSS_FOMC2"] = round(fs2, 4)
        else:
            row["FSS_FOMC2"] = ""

        if row["FSS_FOMC1"] != "" and row["FSS_FOMC2"] != "":
            row["within_gap"] = round(float(row["FSS_FOMC1"]) - float(row["FSS_FOMC2"]), 4)
        else:
            row["within_gap"] = ""

        results.append(row)

    return results


def write_variables(results, output_path):
    """Write meeting-level variables to CSV."""
    if not results:
        print("No results to write.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Define column order
    fieldnames = ["meeting_date"]

    # Sentence counts
    for dt in ["transcript", "minutes", "statement", "speech"]:
        fieldnames.append(f"n_{dt}")
    fieldnames.extend(["n_FOMC1", "n_FOMC2"])

    # Topic shares per doc type
    for dt in ["transcript", "minutes", "statement", "speech"]:
        for prefix in ["FSS", "FCS", "INF", "EMP", "REG", "OTH", "DMS"]:
            fieldnames.append(f"{prefix}_{dt}")

    # FOMC1/FOMC2
    fieldnames.extend(["FSS_FOMC1", "FSS_FOMC2", "within_gap"])

    # Cross-document gaps
    fieldnames.extend(["CDFSG", "CDFSG_minutes", "CDFSG_speech"])

    with open(str(output_path), "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    print(f"Wrote {len(results)} meeting rows to {output_path}")

    # Print summary
    print("\n" + "=" * 80)
    print("MEETING-LEVEL VARIABLES SUMMARY")
    print("=" * 80)
    print(f"{'Meeting':12s} | {'n_trans':>7s} | {'n_min':>6s} | {'n_stmt':>6s} | "
          f"{'FSS_tr':>7s} | {'FSS_st':>7s} | {'CDFSG':>7s} | {'Within':>7s}")
    print("-" * 80)

    for r in results:
        print(f"{r['meeting_date']:12s} | "
              f"{str(r.get('n_transcript', '')):>7s} | "
              f"{str(r.get('n_minutes', '')):>6s} | "
              f"{str(r.get('n_statement', '')):>6s} | "
              f"{str(r.get('FSS_transcript', '')):>7s} | "
              f"{str(r.get('FSS_statement', '')):>7s} | "
              f"{str(r.get('CDFSG', '')):>7s} | "
              f"{str(r.get('within_gap', '')):>7s}")


def main():
    parser = argparse.ArgumentParser(description="Compute meeting-level variables")
    parser.add_argument("--input", type=str, default=None,
                        help="Input classified sentences CSV")
    parser.add_argument("--output", type=str, default=None,
                        help="Output meeting variables CSV")
    args = parser.parse_args()

    input_path = Path(args.input) if args.input else CLASSIFIED_SENTENCES_CSV
    output_path = Path(args.output) if args.output else MEETING_VARIABLES_CSV

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        print("Run classify_sentences.py first to generate classified sentences.")
        sys.exit(1)

    sentences = load_classified_sentences(input_path)
    print(f"Loaded {len(sentences)} classified sentences")

    # Filter to sentences with valid topics
    valid = [s for s in sentences if s.get("topic", "") in TOPIC_CATEGORIES]
    print(f"Valid classifications: {len(valid)} ({100*len(valid)/len(sentences):.1f}%)")

    results = compute_meeting_variables(valid)
    write_variables(results, output_path)


if __name__ == "__main__":
    main()
