from datetime import date, datetime
from typing import Any

from bson import ObjectId


def serializar_mongo(valor: Any) -> Any:
    if isinstance(valor, ObjectId):
        return str(valor)

    if isinstance(valor, (datetime, date)):
        return valor.isoformat()

    if isinstance(valor, list):
        return [serializar_mongo(item) for item in valor]

    if isinstance(valor, dict):
        return {clave: serializar_mongo(item) for clave, item in valor.items()}

    return valor
