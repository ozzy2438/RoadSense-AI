from __future__ import annotations

import argparse
import json
from pathlib import Path


SAMPLE_RECORDS = [
    {
        "source": "synthetic-roadside",
        "member_id": "M-10042",
        "text": "Member reports collision damage outside Geelong and requests towing.",
        "label": "roadside_claim",
    },
    {
        "source": "synthetic-policy",
        "member_id": "M-10073",
        "text": "Policy includes towing after an insured accident when vehicle is unsafe.",
        "label": "policy_evidence",
    },
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create normalized seed data for local demos.")
    parser.add_argument("--output", default="data/processed/normalized.jsonl")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in SAMPLE_RECORDS:
            handle.write(json.dumps(record) + "\n")
    print(f"wrote {len(SAMPLE_RECORDS)} records to {output}")


if __name__ == "__main__":
    main()
