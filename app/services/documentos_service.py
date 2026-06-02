from fastapi import HTTPException, status

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


class DocumentosService:
    def __init__(
        self,
        documentos_repository: DocumentosRepository,
        chunks_repository: ChunksDocumentosRepository,
    ) -> None:
        self.documentos_repository = documentos_repository
        self.chunks_repository = chunks_repository

    async def crear_documento(self, datos: CrearDocumentoFuente) -> DocumentoFuenteRespuesta:
        documento = await self.documentos_repository.crear(datos)
        return DocumentoFuenteRespuesta.model_validate(documento)

    async def listar_documentos(self, *, limite: int, salto: int) -> list[DocumentoFuenteRespuesta]:
        documentos = await self.documentos_repository.listar(limite=limite, salto=salto)
        return [DocumentoFuenteRespuesta.model_validate(documento) for documento in documentos]

    async def obtener_documento(self, documento_id: str) -> DocumentoFuenteRespuesta:
        documento = await self.documentos_repository.obtener_por_id(documento_id)
        if documento is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Documento no encontrado.")

        return DocumentoFuenteRespuesta.model_validate(documento)

    async def actualizar_documento(
        self,
        documento_id: str,
        datos: ActualizarDocumentoFuente,
    ) -> DocumentoFuenteRespuesta:
        documento = await self.documentos_repository.actualizar(documento_id, datos)
        if documento is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Documento no encontrado.")

        return DocumentoFuenteRespuesta.model_validate(documento)

    async def eliminar_documento(self, documento_id: str) -> None:
        eliminado = await self.documentos_repository.eliminar(documento_id)
        if not eliminado:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Documento no encontrado.")
        await self.chunks_repository.eliminar_por_documento(documento_id)

    async def crear_chunk(self, datos: CrearChunkDocumento) -> ChunkDocumentoRespuesta:
        documento = await self.chunks_repository.crear(datos)
        return ChunkDocumentoRespuesta.model_validate(documento)

    async def listar_chunks_documento(
        self,
        documento_id: str,
        *,
        limite: int,
        salto: int,
    ) -> list[ChunkDocumentoRespuesta]:
        chunks = await self.chunks_repository.listar_por_documento(
            documento_id,
            limite=limite,
            salto=salto,
        )
        return [ChunkDocumentoRespuesta.model_validate(chunk) for chunk in chunks]

    async def obtener_chunk(self, chunk_id: str) -> ChunkDocumentoRespuesta:
        chunk = await self.chunks_repository.obtener_por_id(chunk_id)
        if chunk is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Chunk no encontrado.")

        return ChunkDocumentoRespuesta.model_validate(chunk)

    async def actualizar_chunk(
        self,
        chunk_id: str,
        datos: ActualizarChunkDocumento,
    ) -> ChunkDocumentoRespuesta:
        chunk = await self.chunks_repository.actualizar(chunk_id, datos)
        if chunk is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Chunk no encontrado.")

        return ChunkDocumentoRespuesta.model_validate(chunk)

    async def eliminar_chunk(self, chunk_id: str) -> None:
        eliminado = await self.chunks_repository.eliminar(chunk_id)
        if not eliminado:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Chunk no encontrado.")
