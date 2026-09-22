#!/usr/bin/env python3
"""Extract team 5's dataset slice and generate the blind labelling sheets.

Run from the repo root:

    python3 scripts/make_golden_sample.py

Produces:
    data/team5_rows.csv                      all 1000 of our rows (JMeter source)
    golden-set/labelling_sheet_A.csv         200 sampled tickets, no source_label
    golden-set/labelling_sheet_B.csv         the same 200, for the second labeller

The sample is drawn with a fixed seed so anyone can regenerate the identical
set and confirm we did not cherry-pick the tickets.

The labelling sheets deliberately omit source_label. Those labels were chosen
by consumers at submission time and are noisy -- seeing them while labelling
would anchor us to them, which is the corruption the brief warns about.
"""

import csv
import random
import sys
from pathlib import Path

csv.field_size_limit(sys.maxsize)

TEAM_NUMBER = 5
ROW_START = TEAM_NUMBER * 1000
ROW_END = ROW_START + 999
SAMPLE_SIZE = 200          # brief allows 150-200
SEED = 20260922            # fixed for reproducibility; do not change after freeze

SOURCE = Path("ict3113_tickets.csv")
ROW_KEY = "\\row"


def main():
    if not SOURCE.exists():
        sys.exit(f"{SOURCE} not found. Run this from the repo root.")

    with SOURCE.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if ROW_START <= int(r[ROW_KEY]) <= ROW_END]

    if len(rows) != 1000:
        sys.exit(f"Expected 1000 rows for team {TEAM_NUMBER}, got {len(rows)}")

    Path("data").mkdir(exist_ok=True)
    Path("golden-set").mkdir(exist_ok=True)

    # Full slice, source_label kept. This feeds JMeter's CSV Data Set Config.
    with Path("data/team5_rows.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["row", "source_label", "narrative"])
        for r in rows:
            w.writerow([r[ROW_KEY], r["source_label"], r["narrative"]])

    # Blind sample for hand labelling.
    sample = random.Random(SEED).sample(rows, SAMPLE_SIZE)
    sample.sort(key=lambda r: int(r[ROW_KEY]))

    for sheet in ("A", "B"):
        path = Path(f"golden-set/labelling_sheet_{sheet}.csv")
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["row", "narrative", "label"])
            for r in sample:
                w.writerow([r[ROW_KEY], r["narrative"], ""])
        print(f"wrote {path} ({SAMPLE_SIZE} tickets, label column blank)")

    print(f"wrote data/team5_rows.csv ({len(rows)} rows)")
    print(f"sample seed {SEED} -- rerunning reproduces the identical 200 tickets")


if __name__ == "__main__":
    main()
