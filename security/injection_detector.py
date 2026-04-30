from __future__ import annotations

from dataclasses import dataclass


ATTACK_PATTERNS = (
    "ignore previous instructions",
    "reveal system prompt",
    "developer message",
    "exfiltrate",
    "show hidden",
)


@dataclass(frozen=True)
class InjectionDetection:
    is_attack: bool
    reason: str


def detect_prompt_injection(text: str) -> InjectionDetection:
    lowered = text.lower()
    for pattern in ATTACK_PATTERNS:
        if pattern in lowered:
            return InjectionDetection(True, f"matched pattern: {pattern}")
    return InjectionDetection(False, "no attack pattern matched")
