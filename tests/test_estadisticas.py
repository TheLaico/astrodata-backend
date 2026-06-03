from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_stats_responde_sin_mongodb_configurado() -> None:
    response = client.get("/api/stats")

    assert response.status_code == 200
    body = response.json()
    assert "configurado" in body
    assert "conectado" in body
    assert "total_objetos_celestes" in body
    assert "total_documentos" in body
    assert "total_chunks" in body
