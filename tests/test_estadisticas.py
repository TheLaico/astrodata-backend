from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_stats_responde_sin_mongodb_configurado() -> None:
    response = client.get("/api/stats")

    assert response.status_code == 200
    body = response.json()
    assert body["configurado"] is False
    assert body["conectado"] is False
    assert body["total_objetos_celestes"] == 0
    assert body["total_documentos"] == 0
    assert body["total_chunks"] == 0
