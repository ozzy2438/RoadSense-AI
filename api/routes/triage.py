from __future__ import annotations

import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from agents.graph import run_triage
from agents.state import TriageRequest


router = APIRouter()


@router.post("/stream")
async def triage_stream(request: TriageRequest) -> StreamingResponse:
    async def events():
        async for step in run_triage(request):
            yield f"event: {step.name}\n"
            yield f"data: {json.dumps(step.model_dump())}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream")


@router.post("")
async def triage_once(request: TriageRequest) -> dict:
    last_step = None
    async for step in run_triage(request):
        last_step = step
    return last_step.model_dump() if last_step else {"error": "no triage step produced"}
