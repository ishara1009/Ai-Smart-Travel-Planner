from app.core.exceptions import ConflictError, NotFoundError
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import FeedbackCreate
from app.utils.response_utils import serialize_document
from pymongo.errors import DuplicateKeyError


class FeedbackService:
    def __init__(self, feedback: FeedbackRepository, trips: TripRepository):
        self.feedback = feedback
        self.trips = trips

    async def create(self, trip_id: str, user_id: str, payload: FeedbackCreate) -> dict:
        if not await self.trips.get_owned(trip_id, user_id):
            raise NotFoundError("Trip not found", "TRIP_NOT_FOUND")
        try:
            document = await self.feedback.create(trip_id, user_id, payload.rating, payload.comment)
        except DuplicateKeyError as exc:
            raise ConflictError("Feedback has already been submitted", "FEEDBACK_EXISTS") from exc
        return serialize_document(document)
