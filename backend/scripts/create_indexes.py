import asyncio

from app.db.indexes import create_indexes
from app.db.mongodb import mongo


async def main() -> None:
    await mongo.connect()
    try:
        await create_indexes(mongo.get_database())
        print("MongoDB indexes are ready")
    finally:
        await mongo.close()


if __name__ == "__main__":
    asyncio.run(main())
