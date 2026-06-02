from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings
from app.db.mongodb import get_database, ping_mongo
from app.schemas.database import ConsultaMongoRequest, ConsultaMongoResponse, DatabasePingResponse
from app.services.terminal_db_service import TerminalDbService

router = APIRouter(prefix="/db", tags=["database"])


@router.get("/ping", response_model=DatabasePingResponse)
async def ping_database() -> DatabasePingResponse:
    if not settings.mongodb_configured:
        return DatabasePingResponse(
            configurado=False,
            conectado=False,
            base_datos=settings.mongodb_database,
            mensaje="MongoDB no esta configurado. Define MONGODB_URI en el archivo .env.",
        )

    conectado = await ping_mongo()

    return DatabasePingResponse(
        configurado=True,
        conectado=conectado,
        base_datos=settings.mongodb_database,
        mensaje="MongoDB conectado correctamente."
        if conectado
        else "MongoDB esta configurado, pero no respondio al ping.",
    )


def obtener_terminal_db_service(
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> TerminalDbService:
    return TerminalDbService(database)


@router.post("/query", response_model=ConsultaMongoResponse)
async def ejecutar_consulta(
    request: ConsultaMongoRequest,
    service: TerminalDbService = Depends(obtener_terminal_db_service),
) -> ConsultaMongoResponse:
    return await service.ejecutar(request)
