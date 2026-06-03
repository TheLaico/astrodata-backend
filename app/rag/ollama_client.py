import httpx


class OllamaClient:
    def __init__(self, base_url: str, modelo: str, timeout_seconds: float = 180) -> None:
        self.base_url = base_url.rstrip("/")
        self.modelo = modelo
        self.timeout_seconds = timeout_seconds

    async def generar_respuesta(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.modelo,
                    "prompt": prompt,
                    "stream": False,
                },
            )
            response.raise_for_status()
            data = response.json()

        return str(data.get("response", "")).strip()
