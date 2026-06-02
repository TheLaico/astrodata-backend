from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase


class BusquedaRepository:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.database = database

    async def buscar(self, consulta: str, limite: int) -> list[dict[str, Any]]:
        patron = {"$regex": consulta, "$options": "i"}

        objetos_cursor = self.database["celestial_objects"].find(
            {
                "$or": [
                    {"nombre": patron},
                    {"descripcion": patron},
                    {"etiquetas": patron},
                ]
            }
        ).limit(limite)

        documentos_cursor = self.database["documents"].find(
            {
                "$or": [
                    {"titulo": patron},
                    {"descripcion": patron},
                ]
            }
        ).limit(limite)

        objetos = await objetos_cursor.to_list(length=limite)
        documentos = await documentos_cursor.to_list(length=limite)

        resultados: list[dict[str, Any]] = []
        for objeto in objetos:
            resultados.append(
                {
                    "coleccion": "celestial_objects",
                    "id": str(objeto["_id"]),
                    "titulo": objeto.get("nombre", "Objeto celeste"),
                    "descripcion": objeto.get("descripcion", ""),
                }
            )

        for documento in documentos:
            resultados.append(
                {
                    "coleccion": "documents",
                    "id": str(documento["_id"]),
                    "titulo": documento.get("titulo", "Documento"),
                    "descripcion": documento.get("descripcion", ""),
                }
            )

        return resultados[:limite]
