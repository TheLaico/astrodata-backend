from pydantic import BaseModel


class ApiStatusResponse(BaseModel):
    app_name: str
    environment: str
    database: str
    ollama_model: str
    embedding_model: str
    mongodb_configured: bool
