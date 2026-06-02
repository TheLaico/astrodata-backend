import asyncio

from app.core.config import settings
from app.db.mongodb import close_mongo_connection, connect_to_mongo, get_database
from app.rag.embeddings import GeneradorEmbeddings
from app.repositories.chunks_documentos_repository import ChunksDocumentosRepository


async def ejecutar_generacion_embeddings() -> None:
    if not settings.mongodb_configured:
        raise RuntimeError("Define MONGODB_URI en .env antes de generar embeddings.")

    await connect_to_mongo()
    database = get_database()
    repository = ChunksDocumentosRepository(database)
    generador = GeneradorEmbeddings(settings.embedding_model)

    total_actualizados = 0

    while True:
        chunks = await repository.listar_sin_embedding(settings.embedding_batch_size)
        if not chunks:
            break

        textos = [chunk["texto"] for chunk in chunks]
        embeddings = generador.generar(textos)

        for chunk, embedding in zip(chunks, embeddings, strict=True):
            await repository.guardar_embedding(chunk["_id"], embedding)
            total_actualizados += 1

        print(f"Embeddings actualizados hasta ahora: {total_actualizados}")

    await close_mongo_connection()
    print(f"Generacion completada. Chunks actualizados: {total_actualizados}.")


if __name__ == "__main__":
    asyncio.run(ejecutar_generacion_embeddings())
