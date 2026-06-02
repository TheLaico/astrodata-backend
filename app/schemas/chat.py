from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PreguntaChatRequest(BaseModel):
    pregunta: str = Field(min_length=3, max_length=1000)


class FuenteRag(BaseModel):
    chunk_id: str
    documento_id: str
    texto: str
    score: float | None = None
    metadatos: dict[str, Any] = Field(default_factory=dict)


class RespuestaChatResponse(BaseModel):
    pregunta: str
    respuesta: str
    fuentes: list[FuenteRag]


class HistorialConsultaRespuesta(RespuestaChatResponse):
    id: str
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)
