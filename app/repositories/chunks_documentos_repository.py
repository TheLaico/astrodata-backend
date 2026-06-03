import math
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from pymongo import ReturnDocument

from app.core.config import settings
from app.schemas.documentos import ActualizarChunkDocumento, CrearChunkDocumento, fecha_actual_utc


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

    async def crear(self, datos: CrearChunkDocumento) -> dict[str, Any]:
        ahora = fecha_actual_utc()
        documento = datos.model_dump(mode="json")
        documento["creado_en"] = ahora
        documento["actualizado_en"] = ahora

        resultado = await self.collection.insert_one(documento)
        documento["_id"] = resultado.inserted_id

        return self._serializar(documento)

    async def listar_por_documento(
        self,
        documento_id: str,
        *,
        limite: int,
        salto: int,
    ) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find({"documento_id": documento_id})
            .sort("indice", 1)
            .skip(salto)
            .limit(limite)
        )
        documentos = await cursor.to_list(length=limite)
        return [self._serializar(documento) for documento in documentos]

    async def obtener_por_id(self, chunk_id: str) -> dict[str, Any] | None:
        if not ObjectId.is_valid(chunk_id):
            return None

        documento = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if documento is None:
            return None

        return self._serializar(documento)

    async def actualizar(
        self,
        chunk_id: str,
        datos: ActualizarChunkDocumento,
    ) -> dict[str, Any] | None:
        if not ObjectId.is_valid(chunk_id):
            return None

        cambios = datos.model_dump(mode="json", exclude_unset=True)
        if not cambios:
            return await self.obtener_por_id(chunk_id)

        cambios["actualizado_en"] = fecha_actual_utc()
        documento = await self.collection.find_one_and_update(
            {"_id": ObjectId(chunk_id)},
            {"$set": cambios},
            return_document=ReturnDocument.AFTER,
        )
        if documento is None:
            return None

        return self._serializar(documento)

    async def eliminar(self, chunk_id: str) -> bool:
        if not ObjectId.is_valid(chunk_id):
            return False

        resultado = await self.collection.delete_one({"_id": ObjectId(chunk_id)})
        return resultado.deleted_count == 1

    async def eliminar_por_documento(self, documento_id: str) -> int:
        resultado = await self.collection.delete_many({"documento_id": documento_id})
        return int(resultado.deleted_count)

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

    async def buscar_por_vector(
        self,
        embedding: list[float],
        *,
        limite: int,
    ) -> list[dict[str, Any]]:
        pipeline = [
            {
                "$vectorSearch": {
                    "index": settings.vector_search_index_name,
                    "path": "embedding",
                    "queryVector": embedding,
                    "numCandidates": max(limite * 20, 100),
                    "limit": limite,
                }
            },
            {
                "$project": {
                    "documento_id": 1,
                    "fuente": 1,
                    "indice": 1,
                    "texto": 1,
                    "metadatos": 1,
                    "score": {"$meta": "vectorSearchScore"},
                }
            },
        ]

        try:
            documentos = await self.collection.aggregate(pipeline).to_list(length=limite)
            return [self._serializar(documento) for documento in documentos]
        except PyMongoError:
            return await self._buscar_por_vector_local(embedding, limite=limite)

    async def _buscar_por_vector_local(
        self,
        embedding: list[float],
        *,
        limite: int,
    ) -> list[dict[str, Any]]:
        cursor = self.collection.find(
            {
                "embedding": {
                    "$exists": True,
                    "$ne": None,
                }
            },
            {
                "documento_id": 1,
                "fuente": 1,
                "indice": 1,
                "texto": 1,
                "metadatos": 1,
                "embedding": 1,
            },
        )
        documentos = await cursor.to_list(length=None)

        documentos_con_score = []
        for documento in documentos:
            score = self._coseno(embedding, documento.get("embedding", []))
            documento["score"] = score
            documento.pop("embedding", None)
            documentos_con_score.append(documento)

        documentos_ordenados = sorted(
            documentos_con_score,
            key=lambda item: item["score"],
            reverse=True,
        )[:limite]

        return [self._serializar(documento) for documento in documentos_ordenados]

    def _coseno(self, vector_a: list[float], vector_b: list[float]) -> float:
        if not vector_a or not vector_b or len(vector_a) != len(vector_b):
            return 0.0

        producto = sum(a * b for a, b in zip(vector_a, vector_b, strict=True))
        norma_a = math.sqrt(sum(a * a for a in vector_a))
        norma_b = math.sqrt(sum(b * b for b in vector_b))

        if norma_a == 0 or norma_b == 0:
            return 0.0

        return producto / (norma_a * norma_b)

    def _serializar(self, documento: dict[str, Any]) -> dict[str, Any]:
        documento["id"] = str(documento.pop("_id"))
        return documento
