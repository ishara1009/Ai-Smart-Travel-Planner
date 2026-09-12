from uuid import uuid4

from app.core.exceptions import AppError, NotFoundError
from app.graph.builder import travel_graph
from app.repositories.itinerary_repository import ItineraryRepository
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import ModifyTripRequest, TravelRequest, TripPublic, TripStatus
from app.schemas.agent import TravelQuery, TravelQueryResult
from app.services.trip_service import to_public_trip


class PlannerService:
    def __init__(self, trips: TripRepository, itineraries: ItineraryRepository):
        self.trips = trips
        self.itineraries = itineraries

    async def generate(self, user_id: str, payload: TravelRequest) -> TripPublic:
        document = await self.trips.create(user_id, payload)
        return await self._run(str(document["_id"]), user_id, payload, document)

    async def query(self, user_id: str, payload: TravelQuery) -> TravelQueryResult:
        request_id = str(uuid4())
        state = {
            "request_id": request_id,
            "user_id": user_id,
            "user_query": payload.query,
            "structured_request": False,
            "retry_count": 0,
            "errors": [],
            "warnings": [],
            "progress": [],
            "status": "draft",
        }
        result = await travel_graph.ainvoke(
            state,
            config={"configurable": {"thread_id": request_id}, "recursion_limit": 20},
        )
        decision = result.get("supervisor_decision", {})
        return TravelQueryResult(
            request_id=request_id,
            intent=decision.get("intent", "unknown"),
            clarification_question=decision.get("clarification_question"),
            search_results=result.get("search_results", []),
            weather=result.get("weather_data"),
            budget_analysis=result.get("budget_analysis"),
            recommendations=result.get("recommendations", []),
            itinerary=result.get("itinerary"),
            validation=result.get("validation_result"),
            warnings=list(dict.fromkeys(result.get("warnings", []) + result.get("errors", []))),
        )

    async def modify(self, trip_id: str, user_id: str, payload: ModifyTripRequest) -> TripPublic:
        document = await self._owned(trip_id, user_id)
        request = self._request_from_document(document)
        await self.trips.update_owned(trip_id, user_id, {"status": TripStatus.MODIFYING.value})
        return await self._run(trip_id, user_id, request, document, payload.instructions)

    async def regenerate(self, trip_id: str, user_id: str) -> TripPublic:
        document = await self._owned(trip_id, user_id)
        return await self._run(trip_id, user_id, self._request_from_document(document), document)

    async def approve(self, trip_id: str, user_id: str) -> TripPublic:
        document = await self._owned(trip_id, user_id)
        if not document.get("itinerary"):
            raise AppError("Generate an itinerary before approval", "ITINERARY_REQUIRED", 409)
        updated = await self.trips.update_owned(trip_id, user_id, {"status": TripStatus.APPROVED.value})
        return to_public_trip(updated)

    async def _run(
        self,
        trip_id: str,
        user_id: str,
        request: TravelRequest,
        existing: dict,
        instructions: str | None = None,
    ) -> TripPublic:
        request_id = str(uuid4())
        state = {
            "request_id": request_id,
            "user_id": user_id,
            "structured_request": True,
            **request.model_dump(mode="json"),
            "modification_instructions": instructions,
            "previous_itinerary": existing.get("itinerary") if instructions else None,
            "search_queries": existing.get("search_queries", []) if instructions else [],
            "search_results": existing.get("search_results", []) if instructions else [],
            "weather_data": existing.get("weather") if instructions else None,
            "budget_analysis": existing.get("budget_analysis") if instructions else None,
            "recommendations": existing.get("recommendations", []) if instructions else [],
            "retry_count": 0,
            "errors": [],
            "warnings": [],
            "progress": [],
            "status": TripStatus.DRAFT.value,
        }
        try:
            result = await travel_graph.ainvoke(
                state,
                config={"configurable": {"thread_id": trip_id}, "recursion_limit": 20},
            )
        except Exception:
            await self.trips.update_owned(trip_id, user_id, {"status": TripStatus.FAILED.value})
            raise
        changes = {
            "status": result.get("status", TripStatus.AWAITING_APPROVAL.value),
            "weather": result.get("weather_data"),
            "budget_analysis": result.get("budget_analysis"),
            "recommendations": result.get("recommendations", []),
            "search_queries": result.get("search_queries", []),
            "search_results": result.get("search_results", []),
            "itinerary": result.get("itinerary"),
            "warnings": list(dict.fromkeys(result.get("warnings", []))),
            "last_request_id": request_id,
            "agent_progress": result.get("progress", []),
            "validation_result": result.get("validation_result"),
        }
        updated = await self.trips.update_owned(trip_id, user_id, changes)
        if changes["itinerary"]:
            await self.itineraries.upsert(trip_id, changes["itinerary"])
        return to_public_trip(updated)

    async def _owned(self, trip_id: str, user_id: str) -> dict:
        document = await self.trips.get_owned(trip_id, user_id)
        if not document:
            raise NotFoundError("Trip not found", "TRIP_NOT_FOUND")
        return document

    @staticmethod
    def _request_from_document(document: dict) -> TravelRequest:
        keys = set(TravelRequest.model_fields)
        return TravelRequest.model_validate({key: value for key, value in document.items() if key in keys})
