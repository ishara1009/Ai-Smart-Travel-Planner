from fastapi import APIRouter, status

from app.api.dependencies import CurrentUserId, DatabaseDep
from app.repositories.itinerary_repository import ItineraryRepository
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import ModifyTripRequest, TravelRequest, TripPublic
from app.schemas.agent import TravelQuery, TravelQueryResult
from app.services.planner_service import PlannerService

router = APIRouter(prefix="/planner", tags=["Planner"])


def service(database: DatabaseDep) -> PlannerService:
    return PlannerService(TripRepository(database), ItineraryRepository(database))


@router.post("/generate", response_model=TripPublic, status_code=status.HTTP_201_CREATED)
async def generate(payload: TravelRequest, user_id: CurrentUserId, database: DatabaseDep) -> TripPublic:
    return await service(database).generate(user_id, payload)


@router.post("/query", response_model=TravelQueryResult)
async def query(payload: TravelQuery, user_id: CurrentUserId, database: DatabaseDep) -> TravelQueryResult:
    return await service(database).query(user_id, payload)


@router.post("/{trip_id}/modify", response_model=TripPublic)
async def modify(trip_id: str, payload: ModifyTripRequest, user_id: CurrentUserId, database: DatabaseDep) -> TripPublic:
    return await service(database).modify(trip_id, user_id, payload)


@router.post("/{trip_id}/regenerate", response_model=TripPublic)
async def regenerate(trip_id: str, user_id: CurrentUserId, database: DatabaseDep) -> TripPublic:
    return await service(database).regenerate(trip_id, user_id)


@router.post("/{trip_id}/approve", response_model=TripPublic)
async def approve(trip_id: str, user_id: CurrentUserId, database: DatabaseDep) -> TripPublic:
    return await service(database).approve(trip_id, user_id)
