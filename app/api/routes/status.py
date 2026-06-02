from fastapi import APIRouter

from app.core.config import settings
from app.schemas.status import ApiStatusResponse

router = APIRouter()


@router.get("/status", response_model=ApiStatusResponse)
async def get_api_status() -> ApiStatusResponse:
    return ApiStatusResponse(
        app_name=settings.app_name,
        environment=settings.app_env,
        database=settings.mongodb_database,
        ollama_model=settings.ollama_model,
        embedding_model=settings.embedding_model,
        mongodb_configured=settings.mongodb_configured,
    )
