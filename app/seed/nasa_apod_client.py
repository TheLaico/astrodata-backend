from datetime import date, timedelta
from typing import Any

import httpx


class NasaApodClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://api.nasa.gov/planetary/apod"

    async def obtener_rango(self, cantidad: int) -> list[dict[str, Any]]:
        fecha_fin = date.today()
        fecha_inicio = fecha_fin - timedelta(days=cantidad - 1)

        params = {
            "api_key": self.api_key,
            "start_date": fecha_inicio.isoformat(),
            "end_date": fecha_fin.isoformat(),
            "thumbs": "true",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

        if isinstance(data, dict):
            return [data]

        return data
