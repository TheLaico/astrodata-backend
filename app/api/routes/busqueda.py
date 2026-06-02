from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_database
from app.repositories.busqueda_repository import BusquedaRepository
from app.schemas.busqueda import BusquedaResponse
from app.services.busqueda_service import BusquedaService

router = APIRouter(prefix="/busqueda", tags=["busqueda"])


def obtener_servicio_busqueda(
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> BusquedaService:
    return BusquedaService(BusquedaRepository(database))


@router.get("", response_model=BusquedaResponse)
async def buscar(
    q: str = Query(min_length=2, max_length=120),
    limite: int = Query(default=10, ge=1, le=50),
    service: BusquedaService = Depends(obtener_servicio_busqueda),
) -> BusquedaResponse:
    return await service.buscar(q, limite)
