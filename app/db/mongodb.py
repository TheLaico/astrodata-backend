from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


class MongoConnection:
    client: AsyncIOMotorClient | None = None
    database: AsyncIOMotorDatabase | None = None


mongo_connection = MongoConnection()


async def connect_to_mongo() -> None:
    if not settings.mongodb_configured:
        return

    mongo_connection.client = AsyncIOMotorClient(settings.mongodb_uri)
    mongo_connection.database = mongo_connection.client[settings.mongodb_database]


async def close_mongo_connection() -> None:
    if mongo_connection.client is not None:
        mongo_connection.client.close()
        mongo_connection.client = None
        mongo_connection.database = None


def get_database() -> AsyncIOMotorDatabase:
    if mongo_connection.database is None:
        raise RuntimeError("MongoDB is not configured or connection is not initialized.")

    return mongo_connection.database
