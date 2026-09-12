import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import get_settings
from app.db.indexes import create_indexes

logger = logging.getLogger(__name__)


class MongoManager:
    client: AsyncMongoClient | None = None
    database: AsyncDatabase | None = None

    async def connect(self) -> None:
        settings = get_settings()
        self.client = AsyncMongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
        self.database = self.client[settings.mongodb_db_name]
        await self.client.admin.command("ping")
        await create_indexes(self.database)
        logger.info("MongoDB connection established")

    async def close(self) -> None:
        if self.client is not None:
            await self.client.close()
        self.client = None
        self.database = None

    def get_database(self) -> AsyncDatabase:
        if self.database is None:
            raise RuntimeError("MongoDB is not connected")
        return self.database


mongo = MongoManager()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        await mongo.connect()
        app.state.database_ready = True
    except Exception:
        app.state.database_ready = False
        logger.exception("MongoDB connection failed; dependent endpoints will return 503")
    yield
    await mongo.close()
