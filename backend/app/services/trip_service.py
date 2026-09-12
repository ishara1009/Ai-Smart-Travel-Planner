from app.core.exceptions import NotFoundError
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import TripPublic
from app.utils.response_utils import serialize_document


def to_public_trip(document: dict) -> TripPublic:
    return TripPublic.model_validate(serialize_document(document))


class TripService:
    def __init__(self, trips: TripRepository):
        self.trips = trips

    async def list(self, user_id: str, search: str | None, status: str | None) -> list[TripPublic]:
        return [to_public_trip(item) for item in await self.trips.list_owned(user_id, search, status)]

    async def get(self, trip_id: str, user_id: str) -> TripPublic:
        document = await self.trips.get_owned(trip_id, user_id)
        if not document:
            raise NotFoundError("Trip not found", "TRIP_NOT_FOUND")
        return to_public_trip(document)

    async def delete(self, trip_id: str, user_id: str) -> None:
        if not await self.trips.delete_owned(trip_id, user_id):
            raise NotFoundError("Trip not found", "TRIP_NOT_FOUND")
