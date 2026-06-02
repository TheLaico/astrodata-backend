from datetime import date, datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


TipoFuenteDocumento = Literal["apod", "manual", "articulo"]


class DocumentoFuenteBase(BaseModel):
    fuente: TipoFuenteDocumento = "apod"
    titulo: str = Field(min_length=2, max_length=250)
    fecha_publicacion: date | None = None
    descripcion: str = Field(min_length=10)
    url: HttpUrl | None = None
    media_type: str | None = None
    copyright: str | None = None
    metadatos: dict[str, Any] = Field(default_factory=dict)


class CrearDocumentoFuente(DocumentoFuenteBase):
    pass


class ActualizarDocumentoFuente(BaseModel):
    fuente: TipoFuenteDocumento | None = None
    titulo: str | None = Field(default=None, min_length=2, max_length=250)
    fecha_publicacion: date | None = None
    descripcion: str | None = Field(default=None, min_length=10)
    url: HttpUrl | None = None
    media_type: str | None = None
    copyright: str | None = None
    metadatos: dict[str, Any] | None = None


class DocumentoFuenteRespuesta(DocumentoFuenteBase):
    id: str
    creado_en: datetime
    actualizado_en: datetime

    model_config = ConfigDict(from_attributes=True)


class ChunkDocumentoBase(BaseModel):
    documento_id: str
    fuente: TipoFuenteDocumento = "apod"
    indice: int = Field(ge=0)
    texto: str = Field(min_length=10)
    embedding: list[float] | None = None
    metadatos: dict[str, Any] = Field(default_factory=dict)


class CrearChunkDocumento(ChunkDocumentoBase):
    pass


class ActualizarChunkDocumento(BaseModel):
    texto: str | None = Field(default=None, min_length=10)
    embedding: list[float] | None = None
    metadatos: dict[str, Any] | None = None


class ChunkDocumentoRespuesta(ChunkDocumentoBase):
    id: str
    creado_en: datetime
    actualizado_en: datetime

    model_config = ConfigDict(from_attributes=True)


def fecha_actual_utc() -> datetime:
    return datetime.now(timezone.utc)
