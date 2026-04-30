from __future__ import annotations

from pydantic import BaseModel, Field

try:
    from pydantic_ai import Agent
except Exception:  # pragma: no cover - optional in minimal local environments
    Agent = None


class PolicyDecision(BaseModel):
    covered: bool = Field(description="Whether the request is likely covered by retrieved policy text.")
    rationale: str
    confidence: float = Field(ge=0, le=1)
    evidence_ids: list[str] = Field(default_factory=list)


def build_policy_agent():
    if Agent is None:
        return None

    return Agent(
        "openai:gpt-4.1-mini",
        result_type=PolicyDecision,
        system_prompt=(
            "You are a policy-grounded insurance triage agent. Use only retrieved evidence, "
            "return structured output, and mark low-evidence decisions as not covered with low confidence."
        ),
    )
