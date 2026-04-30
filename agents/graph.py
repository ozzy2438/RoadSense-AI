from __future__ import annotations

from collections.abc import AsyncIterator

from agents.action import run_actions
from agents.guardrail import apply_guardrails
from agents.policy_reasoning import reason_over_policy
from agents.retrieval import retrieve_evidence
from agents.router import route_intent
from agents.state import AgentStep, TriageRequest, TriageState


def _step(
    name: str, summary: str, status: str = "completed", **payload: object
) -> AgentStep:
    return AgentStep(name=name, status=status, summary=summary, payload=payload)


async def run_triage(request: TriageRequest) -> AsyncIterator[AgentStep]:
    state = TriageState(request=request)

    yield _step("router", "Classifying request intent", status="started")
    state = route_intent(state)
    yield _step("router", f"Intent classified as {state.intent}", intent=state.intent)

    yield _step("retrieval", "Retrieving policy and operations evidence", status="started")
    state = retrieve_evidence(state)
    yield _step(
        "retrieval",
        f"Retrieved {len(state.evidence)} evidence chunks",
        evidence=[chunk.model_dump() for chunk in state.evidence],
    )

    yield _step("policy_reasoning", "Checking policy-grounded recommendation", status="started")
    state = reason_over_policy(state)
    yield _step(
        "policy_reasoning",
        "Generated recommendation",
        recommendation=state.recommendation,
        confidence=state.confidence,
    )

    yield _step("action", "Running operational tools", status="started")
    state = run_actions(state)
    yield _step("action", "Tool calls completed", tool_results=state.tool_results)

    yield _step("guardrail", "Applying safety and handoff controls", status="started")
    state = apply_guardrails(state)
    yield _step(
        "guardrail",
        "Safety review completed",
        risk_flags=state.risk_flags,
        handoff_required=state.handoff_required,
    )

    yield _step(
        "final",
        state.recommendation or "No recommendation generated.",
        intent=state.intent,
        confidence=state.confidence,
        handoff_required=state.handoff_required,
        evidence_ids=[chunk.chunk_id for chunk in state.evidence],
        prompt_version=state.prompt_version,
    )
