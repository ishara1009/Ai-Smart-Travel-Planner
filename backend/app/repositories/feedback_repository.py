from pymongo.asynchronous.database import AsyncDatabase

from app.db.collections import FEEDBACK
from app.models.feedback import feedback_document


class FeedbackRepository:
    def __init__(self, database: AsyncDatabase):
        self.collection = database[FEEDBACK]

    async def create(self, trip_id: str, user_id: str, rating: int, comment: str | None) -> dict:
        document = feedback_document(trip_id, user_id, rating, comment)
        result = await self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return document
