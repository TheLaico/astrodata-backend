import re
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from app.schemas.objetos_celestes import (
    ActualizarObjetoCeleste,
    CrearObjetoCeleste,
    fecha_actual_utc,
)


class ObjetosCelestesRepository:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.collection = database["celestial_objects"]

    async def crear(self, datos: CrearObjetoCeleste) -> dict[str, Any]:
        ahora = fecha_actual_utc()
        documento = datos.model_dump()
        documento["creado_en"] = ahora
        documento["actualizado_en"] = ahora

        resultado = await self.collection.insert_one(documento)
        documento["_id"] = resultado.inserted_id

        return self._serializar(documento)

    async def listar(
        self,
        *,
        limite: int,
        salto: int,
        tipo_objeto: str | None = None,
    ) -> list[dict[str, Any]]:
        filtro: dict[str, Any] = {}
        if tipo_objeto:
            filtro["tipo_objeto"] = tipo_objeto

        cursor = self.collection.find(filtro).skip(salto).limit(limite)
        documentos = await cursor.to_list(length=limite)

        return [self._serializar(documento) for documento in documentos]

    async def buscar_por_texto(self, terminos: list[str], *, limite: int) -> list[dict[str, Any]]:
        patrones = [
            {"$regex": re.escape(termino), "$options": "i"}
            for termino in terminos
            if termino.strip()
        ]
        if not patrones:
            return []

        condiciones: list[dict[str, Any]] = []
        for patron in patrones:
            condiciones.extend(
                [
                    {"nombre": patron},
                    {"descripcion": patron},
                    {"etiquetas": patron},
                    {"tipo_objeto": patron},
                ]
            )

        cursor = self.collection.find({"$or": condiciones}).limit(limite)
        documentos = await cursor.to_list(length=limite)

        return [self._serializar(documento) for documento in documentos]

    async def obtener_por_id(self, objeto_id: str) -> dict[str, Any] | None:
        if not ObjectId.is_valid(objeto_id):
            return None

        documento = await self.collection.find_one({"_id": ObjectId(objeto_id)})
        if documento is None:
            return None

        return self._serializar(documento)

    async def actualizar(
        self,
        objeto_id: str,
        datos: ActualizarObjetoCeleste,
    ) -> dict[str, Any] | None:
        if not ObjectId.is_valid(objeto_id):
            return None

        cambios = datos.model_dump(exclude_unset=True)
        if not cambios:
            return await self.obtener_por_id(objeto_id)

        cambios["actualizado_en"] = fecha_actual_utc()

        documento = await self.collection.find_one_and_update(
            {"_id": ObjectId(objeto_id)},
            {"$set": cambios},
            return_document=ReturnDocument.AFTER,
        )
        if documento is None:
            return None

        return self._serializar(documento)

    async def eliminar(self, objeto_id: str) -> bool:
        if not ObjectId.is_valid(objeto_id):
            return False

        resultado = await self.collection.delete_one({"_id": ObjectId(objeto_id)})

        return resultado.deleted_count == 1

    def _serializar(self, documento: dict[str, Any]) -> dict[str, Any]:
        documento["id"] = str(documento.pop("_id"))
        return documento
