from __future__ import annotations


def dispatch_tow(member_id: str, location: str) -> dict[str, object]:
    return {
        "dispatch_id": f"TOW-{member_id[-4:]}",
        "member_id": member_id,
        "location": location,
        "status": "queued",
    }
