from app.repositories.busqueda_repository import BusquedaRepository
from app.schemas.busqueda import BusquedaResponse, ResultadoBusqueda


class BusquedaService:
    def __init__(self, repository: BusquedaRepository) -> None:
        self.repository = repository

    async def buscar(self, consulta: str, limite: int) -> BusquedaResponse:
        resultados = await self.repository.buscar(consulta, limite)
        return BusquedaResponse(
            consulta=consulta,
            resultados=[ResultadoBusqueda.model_validate(item) for item in resultados],
        )
