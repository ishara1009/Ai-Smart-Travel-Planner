from datetime import datetime, timezone
from typing import Any
import re

from bson import ObjectId
from pymongo import DESCENDING
from pymongo.asynchronous.database import AsyncDatabase

from app.db.collections import CONVERSATIONS, FEEDBACK, ITINERARIES, TRIPS
from app.models.trip import new_trip_document
from app.schemas.trip import TravelRequest


class TripRepository:
    def __init__(self, database: AsyncDatabase):
        self.database = database
        self.collection = database[TRIPS]

    async def create(self, user_id: str, request: TravelRequest) -> dict[str, Any]:
        document = new_trip_document(user_id, request)
        result = await self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return document

    async def get_owned(self, trip_id: str, user_id: str) -> dict[str, Any] | None:
        if not ObjectId.is_valid(trip_id) or not ObjectId.is_valid(user_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(trip_id), "user_id": ObjectId(user_id)})

    async def list_owned(self, user_id: str, search: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        query: dict[str, Any] = {"user_id": ObjectId(user_id)}
        if search:
            query["destination"] = {"$regex": re.escape(search[:100]), "$options": "i"}
        if status:
            query["status"] = status
        cursor = self.collection.find(query).sort("created_at", DESCENDING).limit(100)
        return await cursor.to_list(length=100)

    async def update_owned(self, trip_id: str, user_id: str, changes: dict[str, Any]) -> dict[str, Any] | None:
        changes["updated_at"] = datetime.now(timezone.utc)
        return await self.collection.find_one_and_update(
            {"_id": ObjectId(trip_id), "user_id": ObjectId(user_id)},
            {"$set": changes},
            return_document=True,
        )

    async def delete_owned(self, trip_id: str, user_id: str) -> bool:
        if not ObjectId.is_valid(trip_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(trip_id), "user_id": ObjectId(user_id)})
        if result.deleted_count == 1:
            trip_object_id = ObjectId(trip_id)
            await self.database[ITINERARIES].delete_many({"trip_id": trip_object_id})
            await self.database[CONVERSATIONS].delete_many({"trip_id": trip_object_id})
            await self.database[FEEDBACK].delete_many({"trip_id": trip_object_id})
        return result.deleted_count == 1
