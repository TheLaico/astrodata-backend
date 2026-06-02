from pydantic import BaseModel
from typing import Any, Literal


class DatabasePingResponse(BaseModel):
    configurado: bool
    conectado: bool
    base_datos: str
    mensaje: str


OperacionMongoPermitida = Literal["find", "aggregate", "count_documents"]


class ConsultaMongoRequest(BaseModel):
    coleccion: str
    operacion: OperacionMongoPermitida
    filtro: dict[str, Any] = {}
    proyeccion: dict[str, Any] | None = None
    pipeline: list[dict[str, Any]] | None = None
    limite: int = 20


class ConsultaMongoResponse(BaseModel):
    coleccion: str
    operacion: OperacionMongoPermitida
    resultados: list[Any] | int
