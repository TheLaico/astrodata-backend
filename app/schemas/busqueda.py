from pydantic import BaseModel


class ResultadoBusqueda(BaseModel):
    coleccion: str
    id: str
    titulo: str
    descripcion: str
    score: float | None = None


class BusquedaResponse(BaseModel):
    consulta: str
    resultados: list[ResultadoBusqueda]
