from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field


class Channel(StrEnum):
    chat = "chat"
    email = "email"
    call = "call"


class TriageRequest(BaseModel):
    member_id: str = Field(min_length=1)
    channel: Channel = Channel.chat
    message: str = Field(min_length=1)
    location: str | None = None


class EvidenceChunk(BaseModel):
    chunk_id: str
    source: str
    text: str
    score: float = 0.0


class AgentStep(BaseModel):
    name: str
    status: Literal["started", "completed", "blocked"] = "completed"
    summary: str
    payload: dict[str, Any] = Field(default_factory=dict)


class TriageState(BaseModel):
    request: TriageRequest
    intent: str | None = None
    risk_flags: list[str] = Field(default_factory=list)
    evidence: list[EvidenceChunk] = Field(default_factory=list)
    tool_results: dict[str, Any] = Field(default_factory=dict)
    recommendation: str | None = None
    confidence: float = 0.0
    handoff_required: bool = False
    prompt_version: str = "triage-v0.1.0"
