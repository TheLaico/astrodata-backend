from fastapi import APIRouter, Depends

from app.schemas.estadisticas import EstadisticasColeccionesResponse
from app.services.estadisticas_service import EstadisticasService

router = APIRouter(prefix="/stats", tags=["estadisticas"])


def obtener_servicio_estadisticas() -> EstadisticasService:
    return EstadisticasService()


@router.get("", response_model=EstadisticasColeccionesResponse)
async def obtener_estadisticas(
    service: EstadisticasService = Depends(obtener_servicio_estadisticas),
) -> EstadisticasColeccionesResponse:
    return await service.obtener_estadisticas()
