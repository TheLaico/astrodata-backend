import asyncio

from app.services.chat_service import ChatService


class ObjetosRepositoryFalso:
    def __init__(self) -> None:
        self.terminos = []

    async def buscar_por_texto(self, terminos, *, limite):
        self.terminos = terminos
        return [
            {
                "id": "europa-1",
                "nombre": "Europa",
                "tipo_objeto": "luna",
                "descripcion": "Luna de Jupiter con superficie helada y posible oceano subsuperficial.",
                "propiedades_fisicas": {"temperatura_kelvin": 102},
                "etiquetas": ["sistema_solar", "luna", "oceano_subsuperficial"],
            }
        ][:limite]


class DocumentosRepositoryFalso:
    async def listar_por_fuente_recientes(self, fuente, *, limite):
        return [
            {
                "id": "doc-1",
                "fuente": fuente,
                "titulo": "The Vela Supernova Remnant",
                "fecha_publicacion": "2026-06-02",
                "descripcion": "Imagen APOD reciente sobre un remanente de supernova.",
                "url": "https://example.test/apod",
            }
        ][:limite]


def test_chat_service_convierte_objetos_celestes_en_fuentes_rag() -> None:
    objetos_repository = ObjetosRepositoryFalso()
    service = ChatService(
        chunks_repository=None,
        historial_repository=None,
        objetos_repository=objetos_repository,
        generador_embeddings=object(),
        ollama_client=object(),
    )

    fuentes = asyncio.run(
        service._buscar_fuentes_objetos("Que informacion hay sobre la luna Europa?")
    )

    assert "europa" in objetos_repository.terminos
    assert "luna" in objetos_repository.terminos
    assert fuentes[0].chunk_id == "objeto:europa-1"
    assert "Luna de Jupiter" in fuentes[0].texto
    assert fuentes[0].metadatos["coleccion"] == "celestial_objects"


def test_chat_service_agrega_documentos_apod_recientes_al_contexto() -> None:
    service = ChatService(
        chunks_repository=None,
        historial_repository=None,
        documentos_repository=DocumentosRepositoryFalso(),
        generador_embeddings=object(),
        ollama_client=object(),
    )

    fuentes = asyncio.run(
        service._buscar_fuentes_documentos_recientes("resume los documentos APOD recientes")
    )

    assert fuentes[0].chunk_id == "documento:doc-1"
    assert "The Vela Supernova Remnant" in fuentes[0].texto
    assert fuentes[0].metadatos["coleccion"] == "documents"
