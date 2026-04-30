from __future__ import annotations


def estimate_eta(location: str) -> dict[str, object]:
    return {
        "location": location,
        "provider": "mock-dispatch-network",
        "eta_minutes": 42,
        "confidence": 0.81,
    }
