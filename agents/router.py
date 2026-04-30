from __future__ import annotations

from agents.state import TriageState


CLAIM_TERMS = {"accident", "claim", "collision", "damage", "covered", "comprehensive"}
ROADSIDE_TERMS = {"tow", "towing", "flat", "battery", "stranded", "breakdown"}
BILLING_TERMS = {"invoice", "payment", "renewal", "premium", "billing"}


def route_intent(state: TriageState) -> TriageState:
    text = state.request.message.lower()
    if any(term in text for term in CLAIM_TERMS):
        state.intent = "claim"
    elif any(term in text for term in ROADSIDE_TERMS):
        state.intent = "roadside"
    elif any(term in text for term in BILLING_TERMS):
        state.intent = "billing"
    else:
        state.intent = "general_inquiry"
    return state
