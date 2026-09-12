from fastapi import APIRouter, Query, Response, status

from app.api.dependencies import CurrentUserId, DatabaseDep
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import TripPublic
from app.services.trip_service import TripService

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.get("", response_model=list[TripPublic])
async def list_trips(
    user_id: CurrentUserId,
    database: DatabaseDep,
    search: str | None = Query(default=None, max_length=100),
    trip_status: str | None = Query(default=None, alias="status", max_length=30),
) -> list[TripPublic]:
    return await TripService(TripRepository(database)).list(user_id, search, trip_status)


@router.get("/{trip_id}", response_model=TripPublic)
async def get_trip(trip_id: str, user_id: CurrentUserId, database: DatabaseDep) -> TripPublic:
    return await TripService(TripRepository(database)).get(trip_id, user_id)


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(trip_id: str, user_id: CurrentUserId, database: DatabaseDep) -> Response:
    await TripService(TripRepository(database)).delete(trip_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
