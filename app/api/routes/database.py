from fastapi import APIRouter

from app.core.config import settings
from app.db.mongodb import ping_mongo
from app.schemas.database import DatabasePingResponse

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
