from typing import Any

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.database import ConsultaMongoRequest, ConsultaMongoResponse
from app.utils.mongo_serialization import serializar_mongo


COLECCIONES_PERMITIDAS = {
    "celestial_objects",
    "documents",
    "document_chunks",
    "query_history",
}

OPERADORES_BLOQUEADOS = {
    "$where",
    "$function",
    "$accumulator",
    "$out",
    "$merge",
}


class TerminalDbService:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.database = database

    async def ejecutar(self, request: ConsultaMongoRequest) -> ConsultaMongoResponse:
        self._validar_request(request)
        collection = self.database[request.coleccion]
        limite = min(request.limite, 100)

        if request.operacion == "find":
            cursor = collection.find(request.filtro, request.proyeccion).limit(limite)
            resultados = await cursor.to_list(length=limite)
            salida: list[Any] | int = serializar_mongo(resultados)
        elif request.operacion == "aggregate":
            pipeline = (request.pipeline or []) + [{"$limit": limite}]
            resultados = await collection.aggregate(pipeline).to_list(length=limite)
            salida = serializar_mongo(resultados)
        else:
            salida = await collection.count_documents(request.filtro)

        return ConsultaMongoResponse(
            coleccion=request.coleccion,
            operacion=request.operacion,
            resultados=salida,
        )

    def _validar_request(self, request: ConsultaMongoRequest) -> None:
        if request.coleccion not in COLECCIONES_PERMITIDAS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coleccion no permitida para la terminal de BD.",
            )

        payload: Any = {
            "filtro": request.filtro,
            "proyeccion": request.proyeccion,
            "pipeline": request.pipeline,
        }
        self._validar_operadores(payload)

        if request.operacion == "aggregate" and not request.pipeline:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La operacion aggregate requiere pipeline.",
            )

    def _validar_operadores(self, valor: Any) -> None:
        if isinstance(valor, dict):
            for clave, item in valor.items():
                if clave in OPERADORES_BLOQUEADOS:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Operador no permitido en terminal de BD: {clave}",
                    )
                self._validar_operadores(item)
        elif isinstance(valor, list):
            for item in valor:
                self._validar_operadores(item)
