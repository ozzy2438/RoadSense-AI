from __future__ import annotations

import hashlib


def _embedding_stub(text: str) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return [round(byte / 255, 4) for byte in digest[:12]]


def main(parsed_document: dict) -> list[dict]:
    text = parsed_document.get("text", "")
    document_id = parsed_document.get("document_id", "unknown")
    return [
        {
            "chunk_id": f"{document_id}#0001",
            "document_id": document_id,
            "text": text,
            "embedding": _embedding_stub(text),
            "metadata": parsed_document.get("metadata", {}),
        }
    ]
