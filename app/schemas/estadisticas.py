from pydantic import BaseModel


class EstadisticasColeccionesResponse(BaseModel):
    configurado: bool
    conectado: bool
    base_datos: str
    total_objetos_celestes: int
    total_documentos: int
    total_chunks: int
    total_chunks_con_embedding: int
    total_consultas_historial: int
    mensaje: str
