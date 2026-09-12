import json

from app.prompts.supervisor import SUPERVISOR_PROMPT
from app.schemas.agent import AgentName, SupervisorDecision
from app.tools.llm_tool import structured_completion


class SupervisorAgent:
    name = "supervisor"

    async def run(self, state: dict) -> SupervisorDecision:
        if state.get("modification_instructions") and state.get("previous_itinerary"):
            return SupervisorDecision(
                intent="focused_itinerary_modification",
                required_agents=[AgentName.ITINERARY, AgentName.VALIDATOR],
            )
        if state.get("structured_request"):
            return SupervisorDecision(
                intent="full_trip_plan",
                required_agents=list(AgentName),
            )
        query = str(state.get("user_query", ""))
        return await structured_completion(
            SupervisorDecision,
            SUPERVISOR_PROMPT,
            json.dumps({"user_query": query}),
        )
