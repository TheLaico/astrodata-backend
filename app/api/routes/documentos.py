from fastapi import APIRouter, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_database
from app.repositories.chunks_documentos_repository import ChunksDocumentosRepository
from app.repositories.documentos_repository import DocumentosRepository
from app.schemas.documentos import (
    ActualizarChunkDocumento,
    ActualizarDocumentoFuente,
    ChunkDocumentoRespuesta,
    CrearChunkDocumento,
    CrearDocumentoFuente,
    DocumentoFuenteRespuesta,
)
from app.services.documentos_service import DocumentosService

router = APIRouter(tags=["documentos"])


def obtener_servicio_documentos(
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> DocumentosService:
    return DocumentosService(
        DocumentosRepository(database),
        ChunksDocumentosRepository(database),
    )


@router.post(
    "/documentos",
    response_model=DocumentoFuenteRespuesta,
    status_code=status.HTTP_201_CREATED,
)
async def crear_documento(
    datos: CrearDocumentoFuente,
    service: DocumentosService = Depends(obtener_servicio_documentos),
) -> DocumentoFuenteRespuesta:
    return await service.crear_documento(datos)


@router.get("/documentos", response_model=list[DocumentoFuenteRespuesta])
async def listar_documentos(
    limite: int = Query(default=20, ge=1, le=100),
    salto: int = Query(default=0, ge=0),
    service: DocumentosService = Depends(obtener_servicio_documentos),
) -> list[DocumentoFuenteRespuesta]:
    return await service.listar_documentos(limite=limite, salto=salto)


@router.get("/documentos/{documento_id}", response_model=DocumentoFuenteRespuesta)
async def obtener_documento(
    documento_id: str,
    service: DocumentosService = Depends(obtener_servicio_documentos),
) -> DocumentoFuenteRespuesta:
    return await service.obtener_documento(documento_id)


@router.put("/documentos/{documento_id}", response_model=DocumentoFuenteRespuesta)
async def actualizar_documento(
    documento_id: str,
    datos: ActualizarDocumentoFuente,
    service: DocumentosService = Depends(obtener_servicio_documentos),
) -> DocumentoFuenteRespuesta:
    return await service.actualizar_documento(documento_id, datos)


@router.delete("/documentos/{documento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_documento(
    documento_id: str,
    service: DocumentosService = Depends(obtener_servicio_documentos),
) -> None:
    await service.eliminar_documento(documento_id)


@router.post(
    "/chunks",
    response_model=ChunkDocumentoRespuesta,
    status_code=status.HTTP_201_CREATED,
)
async def crear_chunk(
    datos: CrearChunkDocumento,
    service: DocumentosService = Depends(obtener_servicio_documentos),
) -> ChunkDocumentoRespuesta:
    return await service.crear_chunk(datos)


@router.get(
    "/documentos/{documento_id}/chunks",
    response_model=list[ChunkDocumentoRespuesta],
)
async def listar_chunks_documento(
    documento_id: str,
    limite: int = Query(default=50, ge=1, le=200),
    salto: int = Query(default=0, ge=0),
    service: DocumentosService = Depends(obtener_servicio_documentos),
) -> list[ChunkDocumentoRespuesta]:
    return await service.listar_chunks_documento(
        documento_id,
        limite=limite,
        salto=salto,
    )


@router.get("/chunks/{chunk_id}", response_model=ChunkDocumentoRespuesta)
async def obtener_chunk(
    chunk_id: str,
    service: DocumentosService = Depends(obtener_servicio_documentos),
) -> ChunkDocumentoRespuesta:
    return await service.obtener_chunk(chunk_id)


@router.put("/chunks/{chunk_id}", response_model=ChunkDocumentoRespuesta)
async def actualizar_chunk(
    chunk_id: str,
    datos: ActualizarChunkDocumento,
    service: DocumentosService = Depends(obtener_servicio_documentos),
) -> ChunkDocumentoRespuesta:
    return await service.actualizar_chunk(chunk_id, datos)


@router.delete("/chunks/{chunk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_chunk(
    chunk_id: str,
    service: DocumentosService = Depends(obtener_servicio_documentos),
) -> None:
    await service.eliminar_chunk(chunk_id)
