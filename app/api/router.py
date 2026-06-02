from fastapi import APIRouter

from app.api.routes import health, status

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(status.router, tags=["status"])
