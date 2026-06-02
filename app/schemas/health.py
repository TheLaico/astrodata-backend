from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class HealthFullResponse(BaseModel):
    status: str
    mongodb_configurado: bool
    mongodb_conectado: bool
    ollama_configurado: bool
    embedding_model: str
    embedding_dimensions: int
