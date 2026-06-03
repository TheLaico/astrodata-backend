from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from app.schemas.documentos import (
    ActualizarDocumentoFuente,
    CrearDocumentoFuente,
    fecha_actual_utc,
)


class DocumentosRepository:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.collection = database["documents"]

    async def crear(self, datos: CrearDocumentoFuente) -> dict[str, Any]:
        ahora = fecha_actual_utc()
        documento = datos.model_dump(mode="json")
        documento["creado_en"] = ahora
        documento["actualizado_en"] = ahora

        resultado = await self.collection.insert_one(documento)
        documento["_id"] = resultado.inserted_id

        return self._serializar(documento)

    async def listar(self, *, limite: int, salto: int) -> list[dict[str, Any]]:
        cursor = self.collection.find({}).sort("fecha_publicacion", -1).skip(salto).limit(limite)
        documentos = await cursor.to_list(length=limite)
        return [self._serializar(documento) for documento in documentos]

    async def listar_por_fuente_recientes(self, fuente: str, *, limite: int) -> list[dict[str, Any]]:
        cursor = (
            self.collection.find({"fuente": fuente})
            .sort("fecha_publicacion", -1)
            .limit(limite)
        )
        documentos = await cursor.to_list(length=limite)
        return [self._serializar(documento) for documento in documentos]

    async def obtener_por_id(self, documento_id: str) -> dict[str, Any] | None:
        if not ObjectId.is_valid(documento_id):
            return None

        documento = await self.collection.find_one({"_id": ObjectId(documento_id)})
        if documento is None:
            return None

        return self._serializar(documento)

    async def actualizar(
        self,
        documento_id: str,
        datos: ActualizarDocumentoFuente,
    ) -> dict[str, Any] | None:
        if not ObjectId.is_valid(documento_id):
            return None

        cambios = datos.model_dump(mode="json", exclude_unset=True)
        if not cambios:
            return await self.obtener_por_id(documento_id)

        cambios["actualizado_en"] = fecha_actual_utc()
        documento = await self.collection.find_one_and_update(
            {"_id": ObjectId(documento_id)},
            {"$set": cambios},
            return_document=ReturnDocument.AFTER,
        )
        if documento is None:
            return None

        return self._serializar(documento)

    async def eliminar(self, documento_id: str) -> bool:
        if not ObjectId.is_valid(documento_id):
            return False

        resultado = await self.collection.delete_one({"_id": ObjectId(documento_id)})
        return resultado.deleted_count == 1

    def _serializar(self, documento: dict[str, Any]) -> dict[str, Any]:
        documento["id"] = str(documento.pop("_id"))
        return documento
