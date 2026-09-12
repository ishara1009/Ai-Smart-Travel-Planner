from fastapi import APIRouter, status

from app.api.dependencies import CurrentUserId, DatabaseDep
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import FeedbackCreate
from app.services.feedback_service import FeedbackService

router = APIRouter(prefix="/trips", tags=["Feedback"])


@router.post("/{trip_id}/feedback", status_code=status.HTTP_201_CREATED)
async def create_feedback(trip_id: str, payload: FeedbackCreate, user_id: CurrentUserId, database: DatabaseDep) -> dict:
    return await FeedbackService(FeedbackRepository(database), TripRepository(database)).create(trip_id, user_id, payload)
