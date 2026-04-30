from __future__ import annotations


def main(chunks: list[dict]) -> dict:
    return {
        "indexed": len(chunks),
        "index": "roadsense-policy-chunks",
        "chunk_ids": [chunk["chunk_id"] for chunk in chunks],
    }
