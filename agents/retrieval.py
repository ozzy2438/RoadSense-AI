from __future__ import annotations

from agents.state import EvidenceChunk, TriageState


MOCK_INDEX = [
    EvidenceChunk(
        chunk_id="policy-comp-accident-tow-001",
        source="comprehensive-motor-policy.pdf",
        text="Towing is covered after an insured accident when the vehicle cannot be safely driven.",
        score=0.91,
    ),
    EvidenceChunk(
        chunk_id="policy-roadside-distance-002",
        source="roadside-assist-guide.pdf",
        text="Emergency roadside assistance can dispatch towing when the member is stranded.",
        score=0.86,
    ),
    EvidenceChunk(
        chunk_id="ops-weather-risk-003",
        source="operations-playbook.md",
        text="Severe weather, night conditions, and highway incidents increase dispatch priority.",
        score=0.73,
    ),
]


def retrieve_evidence(state: TriageState) -> TriageState:
    message = state.request.message.lower()
    ranked = sorted(
        MOCK_INDEX,
        key=lambda chunk: chunk.score + (0.05 if any(word in message for word in chunk.text.lower().split()) else 0),
        reverse=True,
    )
    state.evidence = ranked[:3]
    return state
