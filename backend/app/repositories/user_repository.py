from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from app.db.collections import USERS
from app.models.user import new_user_document


class UserRepository:
    def __init__(self, database: AsyncDatabase):
        self.collection = database[USERS]

    async def find_by_email(self, email: str) -> dict[str, Any] | None:
        return await self.collection.find_one({"email": email.lower()})

    async def find_by_id(self, user_id: str) -> dict[str, Any] | None:
        if not ObjectId.is_valid(user_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(user_id)})

    async def create(self, name: str, email: str, password_hash: str) -> dict[str, Any]:
        document = new_user_document(name, email.lower(), password_hash)
        result = await self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return document

    async def update(self, user_id: str, changes: dict[str, Any]) -> dict[str, Any] | None:
        changes["updated_at"] = datetime.now(timezone.utc)
        return await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)}, {"$set": changes}, return_document=True
        )
