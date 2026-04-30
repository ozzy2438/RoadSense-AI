from __future__ import annotations

from security.presidio_pipeline import mask_pii


def main(parsed_document: dict) -> dict:
    parsed_document["text"] = mask_pii(parsed_document.get("text", ""))
    parsed_document.setdefault("metadata", {})["pii_masked"] = True
    return parsed_document
