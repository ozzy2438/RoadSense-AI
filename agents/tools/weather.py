from __future__ import annotations


def get_weather_risk(location: str) -> dict[str, object]:
    return {
        "location": location,
        "risk": "moderate",
        "signals": ["wet_roads_possible", "reduced_visibility_possible"],
    }
