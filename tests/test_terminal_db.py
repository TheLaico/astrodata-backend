import pytest
from fastapi import HTTPException

from app.schemas.database import ConsultaMongoRequest
from app.services.terminal_db_service import TerminalDbService


def test_terminal_db_bloquea_colecciones_no_permitidas() -> None:
    service = TerminalDbService(database=None)
    request = ConsultaMongoRequest(
        coleccion="admin",
        operacion="find",
    )

    with pytest.raises(HTTPException):
        service._validar_request(request)


def test_terminal_db_bloquea_operadores_peligrosos() -> None:
    service = TerminalDbService(database=None)
    request = ConsultaMongoRequest(
        coleccion="documents",
        operacion="find",
        filtro={"$where": "this.x == 1"},
    )

    with pytest.raises(HTTPException):
        service._validar_request(request)
