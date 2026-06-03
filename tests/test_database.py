from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_database_ping_responde_sin_mongodb_configurado() -> None:
    response = client.get("/api/db/ping")

    assert response.status_code == 200
    body = response.json()
    assert "configurado" in body
    assert "conectado" in body
    assert body["base_datos"] == "astrodata_lab"
