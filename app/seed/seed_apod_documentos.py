import asyncio
from datetime import date
from typing import Any

from app.core.config import settings
from app.db.mongodb import close_mongo_connection, connect_to_mongo, get_database
from app.schemas.documentos import CrearChunkDocumento, CrearDocumentoFuente, fecha_actual_utc
from app.seed.nasa_apod_client import NasaApodClient
from app.utils.chunking import dividir_texto_por_oraciones


def _parsear_fecha(valor: str | None) -> date | None:
    if not valor:
        return None
    return date.fromisoformat(valor)


def _construir_documento(apod: dict[str, Any]) -> CrearDocumentoFuente:
    return CrearDocumentoFuente(
        fuente="apod",
        titulo=apod["title"],
        fecha_publicacion=_parsear_fecha(apod.get("date")),
        descripcion=apod["explanation"],
        url=apod.get("hdurl") or apod.get("url"),
        media_type=apod.get("media_type"),
        copyright=apod.get("copyright"),
        metadatos={
            "service_version": apod.get("service_version"),
            "thumbnail_url": apod.get("thumbnail_url"),
            "raw_date": apod.get("date"),
        },
    )


async def ejecutar_seed() -> None:
    if not settings.mongodb_configured:
        raise RuntimeError("Define MONGODB_URI en .env antes de ejecutar el seed APOD.")

    await connect_to_mongo()
    database = get_database()
    documents = database["documents"]
    chunks_collection = database["document_chunks"]

    client = NasaApodClient(settings.nasa_api_key)
    apods = await client.obtener_rango(settings.apod_seed_limit)

    documentos_insertados = 0
    documentos_actualizados = 0
    chunks_insertados = 0

    for apod in apods:
        documento = _construir_documento(apod)
        ahora = fecha_actual_utc()
        documento_mongo = documento.model_dump(mode="json")
        documento_mongo["actualizado_en"] = ahora

        filtro = {
            "fuente": "apod",
            "fecha_publicacion": documento_mongo["fecha_publicacion"],
            "titulo": documento.titulo,
        }

        resultado = await documents.update_one(
            filtro,
            {
                "$set": documento_mongo,
                "$setOnInsert": {"creado_en": ahora},
            },
            upsert=True,
        )

        if resultado.upserted_id is not None:
            documento_id = str(resultado.upserted_id)
            documentos_insertados += 1
        else:
            existente = await documents.find_one(filtro, {"_id": 1})
            documento_id = str(existente["_id"])
            if resultado.modified_count > 0:
                documentos_actualizados += 1

        await chunks_collection.delete_many({"documento_id": documento_id})

        textos = dividir_texto_por_oraciones(documento.descripcion)
        chunks = [
            CrearChunkDocumento(
                documento_id=documento_id,
                fuente="apod",
                indice=indice,
                texto=texto,
                embedding=None,
                metadatos={
                    "titulo_documento": documento.titulo,
                    "fecha_publicacion": documento_mongo["fecha_publicacion"],
                    "media_type": documento.media_type,
                },
            ).model_dump(mode="json")
            for indice, texto in enumerate(textos)
        ]

        if chunks:
            for chunk in chunks:
                chunk["creado_en"] = ahora
                chunk["actualizado_en"] = ahora

            await chunks_collection.insert_many(chunks)
            chunks_insertados += len(chunks)

    await close_mongo_connection()
    print(
        "Seed APOD completado. "
        f"Documentos insertados: {documentos_insertados}. "
        f"Documentos actualizados: {documentos_actualizados}. "
        f"Chunks insertados: {chunks_insertados}."
    )


if __name__ == "__main__":
    asyncio.run(ejecutar_seed())
