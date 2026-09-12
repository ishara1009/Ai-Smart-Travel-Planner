from pymongo import ASCENDING, DESCENDING, IndexModel
from pymongo.asynchronous.database import AsyncDatabase

from app.db.collections import CONVERSATIONS, FEEDBACK, ITINERARIES, TRIPS, USERS


async def create_indexes(database: AsyncDatabase) -> None:
    await database[USERS].create_indexes([IndexModel([("email", ASCENDING)], unique=True)])
    await database[TRIPS].create_indexes(
        [
            IndexModel([("user_id", ASCENDING), ("created_at", DESCENDING)]),
            IndexModel([("status", ASCENDING)]),
        ]
    )
    await database[ITINERARIES].create_indexes([IndexModel([("trip_id", ASCENDING)], unique=True)])
    await database[CONVERSATIONS].create_indexes([IndexModel([("trip_id", ASCENDING), ("created_at", ASCENDING)])])
    await database[FEEDBACK].create_indexes([IndexModel([("trip_id", ASCENDING), ("user_id", ASCENDING)], unique=True)])
