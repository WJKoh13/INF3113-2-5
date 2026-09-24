#!/usr/bin/env python3
"""Build JMeter's input file from data/team5_rows.csv.

Run from the repo root:

    python3 scripts/make_jmeter_input.py

Produces data/team5_jmeter.tsv: a header line, then one line per ticket with
two tab-separated columns, `row` and `body`. `body` is the complete JSON
request body for POST /tickets, already escaped, so JMeter's CSV Data Set
Config can read it with quoted-data handling off and send ${body} as-is.

team5_rows.csv is not modified. The narratives are sent unchanged; only
their encoding differs.
"""

import csv
import json
import sys
from pathlib import Path

# sys.maxsize overflows C long on Windows.
csv.field_size_limit(2**31 - 1)

SOURCE = Path("data/team5_rows.csv")
OUTPUT = Path("data/team5_jmeter.tsv")


def main():
    if not SOURCE.exists():
        sys.exit(f"{SOURCE} not found. Run this from the repo root.")

    with SOURCE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    with OUTPUT.open("w", newline="\n", encoding="utf-8") as out:
        out.write("row\tbody\n")
        for r in rows:
            # json.dumps escapes quotes, tabs and newlines, so each ticket is one line.
            body = json.dumps({"narrative": r["narrative"]})
            out.write(f"{r['row']}\t{body}\n")

    print(f"Wrote {len(rows)} tickets to {OUTPUT}")


if __name__ == "__main__":
    main()
