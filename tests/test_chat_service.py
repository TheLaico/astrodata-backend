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
