from __future__ import annotations

import argparse
import json
from pathlib import Path


def judge(record: dict) -> dict:
    evidence_required = record.get("expected_action") != "human_handoff"
    grounded = bool(record.get("evidence_ids")) or not evidence_required
    return {"id": record["id"], "policy_grounded": grounded, "verdict": "pass" if grounded else "fail"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Policy-grounded judge harness.")
    parser.add_argument("--input", default="eval/golden_set.jsonl")
    args = parser.parse_args()

    results = [judge(json.loads(line)) for line in Path(args.input).read_text().splitlines() if line]
    print(json.dumps({"results": results}, indent=2))


if __name__ == "__main__":
    main()
