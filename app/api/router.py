from fastapi import APIRouter

from app.api.routes import (
    busqueda,
    chat,
    database,
    documentos,
    estadisticas,
    health,
    objetos_celestes,
    status,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(status.router, tags=["status"])
api_router.include_router(database.router)
api_router.include_router(estadisticas.router)
api_router.include_router(documentos.router)
api_router.include_router(busqueda.router)
api_router.include_router(chat.router)
api_router.include_router(objetos_celestes.router)
