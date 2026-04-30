from __future__ import annotations

from agents.state import TriageState


def reason_over_policy(state: TriageState) -> TriageState:
    evidence_text = " ".join(chunk.text.lower() for chunk in state.evidence)
    request_text = state.request.message.lower()

    if "ignore previous instructions" in request_text:
        state.recommendation = "Do not answer the request. Escalate to a human operator for security review."
        state.confidence = 0.99
        state.handoff_required = True
        return state

    covered_tow = "towing is covered" in evidence_text and any(
        word in request_text for word in ("accident", "collision", "damage", "debris", "hit")
    )
    if covered_tow:
        state.recommendation = (
            "Treat as a likely covered roadside claim. Dispatch towing, capture incident details, "
            "and ask the member to upload photos when safe."
        )
        state.confidence = 0.88
    else:
        state.recommendation = (
            "Collect more details before making a coverage statement. Keep the member in a human-assisted path."
        )
        state.confidence = 0.61
        state.handoff_required = True
    return state
