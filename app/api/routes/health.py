import httpx
from fastapi import APIRouter

from app.core.config import settings
from app.db.mongodb import ping_mongo
from app.schemas.health import HealthFullResponse, HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/health/full", response_model=HealthFullResponse)
async def health_full() -> HealthFullResponse:
    mongodb_conectado = await ping_mongo() if settings.mongodb_configured else False
    ollama_configurado = await _ollama_disponible()

    return HealthFullResponse(
        status="ok" if mongodb_conectado or not settings.mongodb_configured else "degraded",
        mongodb_configurado=settings.mongodb_configured,
        mongodb_conectado=mongodb_conectado,
        ollama_configurado=ollama_configurado,
        embedding_model=settings.embedding_model,
        embedding_dimensions=settings.embedding_dimensions,
    )


async def _ollama_disponible() -> bool:
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            response = await client.get(f"{settings.ollama_base_url.rstrip('/')}/api/tags")
            return response.status_code == 200
    except httpx.HTTPError:
        return False
