from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_database_ping_responde_sin_mongodb_configurado() -> None:
    response = client.get("/api/db/ping")

    assert response.status_code == 200
    assert response.json()["configurado"] is False
    assert response.json()["conectado"] is False
