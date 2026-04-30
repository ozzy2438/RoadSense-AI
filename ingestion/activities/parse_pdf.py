from __future__ import annotations


def main(document: dict) -> dict:
    return {
        "document_id": document.get("name", "unknown"),
        "text": "Towing is covered after an insured accident when the vehicle cannot be safely driven.",
        "metadata": {"parser": "azure-document-intelligence", "size": document.get("size", 0)},
    }
