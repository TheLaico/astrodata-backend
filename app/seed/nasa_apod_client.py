import asyncio
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
        lote_dias = 20

        resultados: list[dict[str, Any]] = []
        inicio_lote = fecha_inicio

        async with httpx.AsyncClient(timeout=httpx.Timeout(60, connect=15)) as client:
            while inicio_lote <= fecha_fin:
                fin_lote = min(inicio_lote + timedelta(days=lote_dias - 1), fecha_fin)
                resultados.extend(await self._obtener_lote(client, inicio_lote, fin_lote))
                inicio_lote = fin_lote + timedelta(days=1)

        return resultados

    async def _obtener_lote(
        self,
        client: httpx.AsyncClient,
        fecha_inicio: date,
        fecha_fin: date,
    ) -> list[dict[str, Any]]:
        params = {
            "api_key": self.api_key,
            "start_date": fecha_inicio.isoformat(),
            "end_date": fecha_fin.isoformat(),
            "thumbs": "true",
        }

        ultimo_error: Exception | None = None
        for intento in range(3):
            try:
                response = await client.get(self.base_url, params=params)
                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit() and intento < 2:
                        await asyncio.sleep(min(int(retry_after), 60))
                        continue
                    raise RuntimeError(
                        "NASA APOD rechazo la solicitud por limite de peticiones "
                        "(HTTP 429). Configura una NASA_API_KEY propia en .env "
                        "o espera a que se reinicie el limite de DEMO_KEY."
                    )
                response.raise_for_status()
                data = response.json()
                return [data] if isinstance(data, dict) else data
            except (httpx.TimeoutException, httpx.HTTPStatusError) as exc:
                ultimo_error = exc
                if intento == 2:
                    break

        raise RuntimeError(
            "No se pudo descargar APOD "
            f"entre {fecha_inicio.isoformat()} y {fecha_fin.isoformat()}."
        ) from ultimo_error
