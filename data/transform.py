from __future__ import annotations

import argparse
import json
from pathlib import Path


def remap_record(record: dict) -> dict:
    return {
        "case_id": f"CASE-{record.get('member_id', 'UNKNOWN')}",
        "domain": "insurance-roadside",
        "intent": record.get("label", "general"),
        "utterance": record.get("text", ""),
        "metadata": {"source": record.get("source", "unknown")},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Remap normalized data into RoadSense schema.")
    parser.add_argument("--input", default="data/processed/normalized.jsonl")
    parser.add_argument("--output", default="data/processed/roadsense_cases.jsonl")
    args = parser.parse_args()

    src = Path(args.input)
    dst = Path(args.output)
    dst.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with src.open(encoding="utf-8") as in_handle, dst.open("w", encoding="utf-8") as out_handle:
        for line in in_handle:
            if not line.strip():
                continue
            out_handle.write(json.dumps(remap_record(json.loads(line))) + "\n")
            count += 1
    print(f"wrote {count} transformed records to {dst}")


if __name__ == "__main__":
    main()
