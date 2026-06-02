from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_database
from app.repositories.chunks_documentos_repository import ChunksDocumentosRepository
from app.repositories.historial_consultas_repository import HistorialConsultasRepository
from app.schemas.chat import (
    HistorialConsultaRespuesta,
    PreguntaChatRequest,
    RespuestaChatResponse,
)
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat ia"])


def obtener_servicio_chat(
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> ChatService:
    return ChatService(
        ChunksDocumentosRepository(database),
        HistorialConsultasRepository(database),
    )


@router.post("/preguntar", response_model=RespuestaChatResponse)
async def preguntar(
    request: PreguntaChatRequest,
    service: ChatService = Depends(obtener_servicio_chat),
) -> RespuestaChatResponse:
    return await service.preguntar(request)


@router.get("/historial", response_model=list[HistorialConsultaRespuesta])
async def listar_historial(
    limite: int = Query(default=20, ge=1, le=100),
    service: ChatService = Depends(obtener_servicio_chat),
) -> list[HistorialConsultaRespuesta]:
    return await service.listar_historial(limite)


@router.delete("/historial")
async def limpiar_historial(
    service: ChatService = Depends(obtener_servicio_chat),
) -> dict[str, int]:
    return await service.limpiar_historial()
