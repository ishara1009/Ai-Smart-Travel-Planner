from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from app.db.collections import ITINERARIES
from app.models.itinerary import itinerary_document


class ItineraryRepository:
    def __init__(self, database: AsyncDatabase):
        self.collection = database[ITINERARIES]

    async def upsert(self, trip_id: str, payload: dict) -> None:
        document = itinerary_document(trip_id, payload)
        await self.collection.update_one({"trip_id": ObjectId(trip_id)}, {"$set": document}, upsert=True)
