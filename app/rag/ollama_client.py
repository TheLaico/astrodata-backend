import httpx


class OllamaClient:
    def __init__(self, base_url: str, modelo: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.modelo = modelo

    async def generar_respuesta(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=60) as client:
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
