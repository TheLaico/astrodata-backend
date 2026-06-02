from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.documentos import fecha_actual_utc


class HistorialConsultasRepository:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.collection = database["query_history"]

    async def guardar(
        self,
        *,
        pregunta: str,
        respuesta: str,
        fuentes: list[dict[str, Any]],
    ) -> dict[str, Any]:
        documento = {
            "pregunta": pregunta,
            "respuesta": respuesta,
            "fuentes": fuentes,
            "creado_en": fecha_actual_utc(),
        }

        resultado = await self.collection.insert_one(documento)
        documento["_id"] = resultado.inserted_id

        return self._serializar(documento)

    async def listar(self, limite: int) -> list[dict[str, Any]]:
        cursor = self.collection.find({}).sort("creado_en", -1).limit(limite)
        documentos = await cursor.to_list(length=limite)
        return [self._serializar(documento) for documento in documentos]

    async def limpiar(self) -> int:
        resultado = await self.collection.delete_many({})
        return int(resultado.deleted_count)

    def _serializar(self, documento: dict[str, Any]) -> dict[str, Any]:
        documento["id"] = str(documento.pop("_id"))
        return documento
