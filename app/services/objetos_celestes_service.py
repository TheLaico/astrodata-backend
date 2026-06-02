from fastapi import HTTPException, status

from app.repositories.objetos_celestes_repository import ObjetosCelestesRepository
from app.schemas.objetos_celestes import (
    ActualizarObjetoCeleste,
    CrearObjetoCeleste,
    ObjetoCelesteRespuesta,
)


class ObjetosCelestesService:
    def __init__(self, repository: ObjetosCelestesRepository) -> None:
        self.repository = repository

    async def crear_objeto(
        self,
        datos: CrearObjetoCeleste,
    ) -> ObjetoCelesteRespuesta:
        documento = await self.repository.crear(datos)
        return ObjetoCelesteRespuesta.model_validate(documento)

    async def listar_objetos(
        self,
        *,
        limite: int,
        salto: int,
        tipo_objeto: str | None,
    ) -> list[ObjetoCelesteRespuesta]:
        documentos = await self.repository.listar(
            limite=limite,
            salto=salto,
            tipo_objeto=tipo_objeto,
        )
        return [ObjetoCelesteRespuesta.model_validate(documento) for documento in documentos]

    async def obtener_objeto(self, objeto_id: str) -> ObjetoCelesteRespuesta:
        documento = await self.repository.obtener_por_id(objeto_id)
        if documento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Objeto celeste no encontrado.",
            )

        return ObjetoCelesteRespuesta.model_validate(documento)

    async def actualizar_objeto(
        self,
        objeto_id: str,
        datos: ActualizarObjetoCeleste,
    ) -> ObjetoCelesteRespuesta:
        documento = await self.repository.actualizar(objeto_id, datos)
        if documento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Objeto celeste no encontrado.",
            )

        return ObjetoCelesteRespuesta.model_validate(documento)

    async def eliminar_objeto(self, objeto_id: str) -> None:
        eliminado = await self.repository.eliminar(objeto_id)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Objeto celeste no encontrado.",
            )
