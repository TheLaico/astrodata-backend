from fastapi import APIRouter

from app.api.routes import database, health, objetos_celestes, status

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(status.router, tags=["status"])
api_router.include_router(database.router)
api_router.include_router(objetos_celestes.router)
