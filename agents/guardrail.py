from __future__ import annotations

import re

from agents.state import TriageState
from security.injection_detector import detect_prompt_injection


EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"\b(?:\+?61|0)[2-478](?:[ -]?\d){8}\b")


def apply_guardrails(state: TriageState) -> TriageState:
    message = state.request.message
    if detect_prompt_injection(message).is_attack:
        state.risk_flags.append("prompt_injection")
        state.handoff_required = True
        state.intent = "security_review"

    if EMAIL_RE.search(message) or PHONE_RE.search(message):
        state.risk_flags.append("pii_detected")

    if state.confidence < 0.72:
        state.handoff_required = True

    return state
