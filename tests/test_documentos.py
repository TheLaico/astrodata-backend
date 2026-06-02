from datetime import date

from app.schemas.documentos import CrearChunkDocumento, CrearDocumentoFuente
from app.utils.chunking import dividir_texto_por_oraciones


def test_crear_documento_fuente_apod() -> None:
    documento = CrearDocumentoFuente(
        titulo="Astronomy Picture of the Day",
        fecha_publicacion=date(2026, 1, 1),
        descripcion="Una descripcion cientifica con suficiente contenido para ser valida.",
        url="https://example.com/image.jpg",
        media_type="image",
    )

    assert documento.fuente == "apod"
    assert documento.fecha_publicacion == date(2026, 1, 1)


def test_crear_chunk_documento_sin_embedding() -> None:
    chunk = CrearChunkDocumento(
        documento_id="abc123",
        indice=0,
        texto="Texto cientifico recuperable para el pipeline RAG.",
    )

    assert chunk.embedding is None
    assert chunk.indice == 0


def test_dividir_texto_por_oraciones_respeta_tamano_maximo() -> None:
    texto = (
        "Primera oracion sobre una galaxia lejana. "
        "Segunda oracion sobre formacion estelar. "
        "Tercera oracion sobre planetas habitables."
    )

    chunks = dividir_texto_por_oraciones(texto, max_caracteres=60)

    assert len(chunks) == 3
    assert all(len(chunk) <= 60 for chunk in chunks)
