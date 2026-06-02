from pydantic import BaseModel


class DatabasePingResponse(BaseModel):
    configurado: bool
    conectado: bool
    base_datos: str
    mensaje: str
