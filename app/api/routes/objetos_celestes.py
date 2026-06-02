from fastapi import APIRouter, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_database
from app.repositories.objetos_celestes_repository import ObjetosCelestesRepository
from app.schemas.objetos_celestes import (
    ActualizarObjetoCeleste,
    CrearObjetoCeleste,
    ObjetoCelesteRespuesta,
    TipoObjetoCeleste,
)
from app.services.objetos_celestes_service import ObjetosCelestesService

router = APIRouter(prefix="/objetos-celestes", tags=["objetos celestes"])


def obtener_servicio_objetos_celestes(
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> ObjetosCelestesService:
    repository = ObjetosCelestesRepository(database)
    return ObjetosCelestesService(repository)


@router.post(
    "",
    response_model=ObjetoCelesteRespuesta,
    status_code=status.HTTP_201_CREATED,
)
async def crear_objeto_celeste(
    datos: CrearObjetoCeleste,
    service: ObjetosCelestesService = Depends(obtener_servicio_objetos_celestes),
) -> ObjetoCelesteRespuesta:
    return await service.crear_objeto(datos)


@router.get("", response_model=list[ObjetoCelesteRespuesta])
async def listar_objetos_celestes(
    limite: int = Query(default=20, ge=1, le=100),
    salto: int = Query(default=0, ge=0),
    tipo_objeto: TipoObjetoCeleste | None = None,
    service: ObjetosCelestesService = Depends(obtener_servicio_objetos_celestes),
) -> list[ObjetoCelesteRespuesta]:
    return await service.listar_objetos(
        limite=limite,
        salto=salto,
        tipo_objeto=tipo_objeto,
    )


@router.get("/{objeto_id}", response_model=ObjetoCelesteRespuesta)
async def obtener_objeto_celeste(
    objeto_id: str,
    service: ObjetosCelestesService = Depends(obtener_servicio_objetos_celestes),
) -> ObjetoCelesteRespuesta:
    return await service.obtener_objeto(objeto_id)


@router.put("/{objeto_id}", response_model=ObjetoCelesteRespuesta)
async def actualizar_objeto_celeste(
    objeto_id: str,
    datos: ActualizarObjetoCeleste,
    service: ObjetosCelestesService = Depends(obtener_servicio_objetos_celestes),
) -> ObjetoCelesteRespuesta:
    return await service.actualizar_objeto(objeto_id, datos)


@router.delete("/{objeto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_objeto_celeste(
    objeto_id: str,
    service: ObjetosCelestesService = Depends(obtener_servicio_objetos_celestes),
) -> None:
    await service.eliminar_objeto(objeto_id)
