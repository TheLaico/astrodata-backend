from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.documentos import fecha_actual_utc


class ChunksDocumentosRepository:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.collection = database["document_chunks"]

    async def listar_sin_embedding(self, limite: int) -> list[dict[str, Any]]:
        cursor = self.collection.find(
            {
                "$or": [
                    {"embedding": None},
                    {"embedding": {"$exists": False}},
                ]
            }
        ).limit(limite)

        return await cursor.to_list(length=limite)

    async def guardar_embedding(self, chunk_id: ObjectId, embedding: list[float]) -> None:
        await self.collection.update_one(
            {"_id": chunk_id},
            {
                "$set": {
                    "embedding": embedding,
                    "actualizado_en": fecha_actual_utc(),
                }
            },
        )
