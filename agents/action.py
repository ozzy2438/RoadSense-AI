from __future__ import annotations

from agents.state import TriageState
from agents.tools.dispatch import dispatch_tow
from agents.tools.eta import estimate_eta
from agents.tools.weather import get_weather_risk


def run_actions(state: TriageState) -> TriageState:
    location = state.request.location or "Victoria, AU"
    state.tool_results["weather"] = get_weather_risk(location)
    state.tool_results["eta"] = estimate_eta(location)

    if state.intent in {"claim", "roadside"} and state.confidence >= 0.72:
        state.tool_results["dispatch"] = dispatch_tow(member_id=state.request.member_id, location=location)

    return state
