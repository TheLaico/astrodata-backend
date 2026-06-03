import httpx
from fastapi import HTTPException, status

from app.core.config import settings
from app.rag.embeddings import GeneradorEmbeddings
from app.rag.ollama_client import OllamaClient
from app.rag.prompt_builder import PromptBuilder
from app.repositories.chunks_documentos_repository import ChunksDocumentosRepository
from app.repositories.documentos_repository import DocumentosRepository
from app.repositories.historial_consultas_repository import HistorialConsultasRepository
from app.repositories.objetos_celestes_repository import ObjetosCelestesRepository
from app.schemas.chat import (
    FuenteRag,
    HistorialConsultaRespuesta,
    PreguntaChatRequest,
    RespuestaChatResponse,
)


class ChatService:
    def __init__(
        self,
        chunks_repository: ChunksDocumentosRepository,
        historial_repository: HistorialConsultasRepository,
        objetos_repository: ObjetosCelestesRepository | None = None,
        documentos_repository: DocumentosRepository | None = None,
        generador_embeddings: GeneradorEmbeddings | None = None,
        ollama_client: OllamaClient | None = None,
        prompt_builder: PromptBuilder | None = None,
    ) -> None:
        self.chunks_repository = chunks_repository
        self.historial_repository = historial_repository
        self.objetos_repository = objetos_repository
        self.documentos_repository = documentos_repository
        self.generador_embeddings = generador_embeddings or GeneradorEmbeddings(settings.embedding_model)
        self.ollama_client = ollama_client or OllamaClient(
            settings.ollama_base_url,
            settings.ollama_model,
            settings.ollama_timeout_seconds,
        )
        self.prompt_builder = prompt_builder or PromptBuilder()

    async def preguntar(self, request: PreguntaChatRequest) -> RespuestaChatResponse:
        embedding = self.generador_embeddings.generar([request.pregunta])[0]
        chunks = await self.chunks_repository.buscar_por_vector(
            embedding,
            limite=settings.rag_top_k,
        )

        fuentes = [
            FuenteRag(
                chunk_id=chunk["id"],
                documento_id=chunk["documento_id"],
                texto=chunk["texto"],
                score=chunk.get("score"),
                metadatos=chunk.get("metadatos", {}),
            )
            for chunk in chunks
        ]

        fuentes.extend(await self._buscar_fuentes_objetos(request.pregunta))
        fuentes.extend(await self._buscar_fuentes_documentos_recientes(request.pregunta))

        prompt = self.prompt_builder.construir(request.pregunta, fuentes)

        try:
            respuesta = await self.ollama_client.generar_respuesta(prompt)
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Ollama no respondio. Verifica que el modelo local este corriendo.",
            ) from exc

        await self.historial_repository.guardar(
            pregunta=request.pregunta,
            respuesta=respuesta,
            fuentes=[fuente.model_dump() for fuente in fuentes],
        )

        return RespuestaChatResponse(
            pregunta=request.pregunta,
            respuesta=respuesta,
            fuentes=fuentes,
        )

    async def listar_historial(self, limite: int) -> list[HistorialConsultaRespuesta]:
        documentos = await self.historial_repository.listar(limite)
        return [
            HistorialConsultaRespuesta.model_validate(documento)
            for documento in documentos
        ]

    async def limpiar_historial(self) -> dict[str, int]:
        eliminados = await self.historial_repository.limpiar()
        return {"eliminados": eliminados}

    async def _buscar_fuentes_objetos(self, pregunta: str) -> list[FuenteRag]:
        if self.objetos_repository is None:
            return []

        objetos = await self.objetos_repository.buscar_por_texto(
            self._extraer_terminos_busqueda(pregunta),
            limite=3,
        )

        return [
            FuenteRag(
                chunk_id=f"objeto:{objeto['id']}",
                documento_id=objeto["id"],
                texto=self._formatear_objeto(objeto),
                score=None,
                metadatos={
                    "coleccion": "celestial_objects",
                    "tipo_fuente": "objeto_celeste",
                    "nombre": objeto.get("nombre"),
                },
            )
            for objeto in objetos
        ]

    async def _buscar_fuentes_documentos_recientes(self, pregunta: str) -> list[FuenteRag]:
        if self.documentos_repository is None:
            return []

        pregunta_normalizada = self._normalizar_texto(pregunta)
        pide_apod = "apod" in pregunta_normalizada or "documento" in pregunta_normalizada
        pide_recientes = "reciente" in pregunta_normalizada or "ultim" in pregunta_normalizada
        pide_resumen = "resume" in pregunta_normalizada or "resumen" in pregunta_normalizada

        if not pide_apod or not (pide_recientes or pide_resumen):
            return []

        documentos = await self.documentos_repository.listar_por_fuente_recientes(
            "apod",
            limite=5,
        )

        return [
            FuenteRag(
                chunk_id=f"documento:{documento['id']}",
                documento_id=documento["id"],
                texto=self._formatear_documento(documento),
                score=None,
                metadatos={
                    "coleccion": "documents",
                    "tipo_fuente": "documento_reciente",
                    "fuente": documento.get("fuente"),
                    "titulo": documento.get("titulo"),
                    "fecha_publicacion": documento.get("fecha_publicacion"),
                },
            )
            for documento in documentos
        ]

    def _extraer_terminos_busqueda(self, pregunta: str) -> list[str]:
        stopwords = {
            "sobre",
            "para",
            "como",
            "cual",
            "cuales",
            "donde",
            "esta",
            "este",
            "esta",
            "esto",
            "tiene",
            "informacion",
            "base",
            "datos",
            "que",
            "hay",
            "del",
            "las",
            "los",
            "una",
            "uno",
            "con",
            "por",
        }
        terminos = []
        for palabra in pregunta.lower().replace("¿", " ").replace("?", " ").split():
            normalizada = palabra.strip(".,:;()[]{}¡!\"'")
            if len(normalizada) < 4 or normalizada in stopwords:
                continue
            terminos.append(normalizada)

        return list(dict.fromkeys(terminos))[:8]

    def _normalizar_texto(self, texto: str) -> str:
        reemplazos = str.maketrans("áéíóúÁÉÍÓÚñÑ", "aeiouAEIOUnN")
        return texto.translate(reemplazos).lower()

    def _formatear_objeto(self, objeto: dict) -> str:
        propiedades = objeto.get("propiedades_fisicas") or {}
        propiedades_texto = ", ".join(
            f"{clave}: {valor}" for clave, valor in propiedades.items()
        )
        etiquetas = ", ".join(objeto.get("etiquetas") or [])

        partes = [
            f"Objeto celeste: {objeto.get('nombre', 'Sin nombre')}",
            f"Tipo: {objeto.get('tipo_objeto', 'desconocido')}",
            f"Descripcion: {objeto.get('descripcion', '')}",
        ]
        if propiedades_texto:
            partes.append(f"Propiedades fisicas: {propiedades_texto}")
        if etiquetas:
            partes.append(f"Etiquetas: {etiquetas}")

        return "\n".join(partes)

    def _formatear_documento(self, documento: dict) -> str:
        return "\n".join(
            [
                f"Documento APOD: {documento.get('titulo', 'Sin titulo')}",
                f"Fecha: {documento.get('fecha_publicacion', 'sin fecha')}",
                f"Descripcion: {documento.get('descripcion', '')}",
                f"URL: {documento.get('url', '')}",
            ]
        )
