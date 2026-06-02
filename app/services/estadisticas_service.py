from app.core.config import settings
from app.db.mongodb import get_database_or_none, ping_mongo
from app.repositories.estadisticas_repository import EstadisticasRepository
from app.schemas.estadisticas import EstadisticasColeccionesResponse


class EstadisticasService:
    async def obtener_estadisticas(self) -> EstadisticasColeccionesResponse:
        if not settings.mongodb_configured:
            return self._respuesta_sin_conexion(
                conectado=False,
                mensaje="MongoDB no esta configurado. Define MONGODB_URI en .env.",
            )

        database = get_database_or_none()
        conectado = await ping_mongo()

        if database is None or not conectado:
            return self._respuesta_sin_conexion(
                conectado=False,
                mensaje="MongoDB esta configurado, pero no respondio correctamente.",
            )

        repository = EstadisticasRepository(database)

        return EstadisticasColeccionesResponse(
            configurado=True,
            conectado=True,
            base_datos=settings.mongodb_database,
            total_objetos_celestes=await repository.contar_objetos_celestes(),
            total_documentos=await repository.contar_documentos(),
            total_chunks=await repository.contar_chunks(),
            total_chunks_con_embedding=await repository.contar_chunks_con_embedding(),
            total_consultas_historial=await repository.contar_consultas_historial(),
            mensaje="Estadisticas calculadas correctamente.",
        )

    def _respuesta_sin_conexion(
        self,
        *,
        conectado: bool,
        mensaje: str,
    ) -> EstadisticasColeccionesResponse:
        return EstadisticasColeccionesResponse(
            configurado=settings.mongodb_configured,
            conectado=conectado,
            base_datos=settings.mongodb_database,
            total_objetos_celestes=0,
            total_documentos=0,
            total_chunks=0,
            total_chunks_con_embedding=0,
            total_consultas_historial=0,
            mensaje=mensaje,
        )
