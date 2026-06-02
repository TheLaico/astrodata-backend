import asyncio
import json
from pathlib import Path

from pymongo import ASCENDING, IndexModel

from app.core.config import settings
from app.db.mongodb import close_mongo_connection, connect_to_mongo, get_database


VECTOR_INDEX_FILE = Path(__file__).with_name("atlas_vector_search_index.json")


async def crear_indices() -> None:
    if not settings.mongodb_configured:
        raise RuntimeError("Define MONGODB_URI en .env antes de crear indices.")

    await connect_to_mongo()
    database = get_database()

    await database["celestial_objects"].create_indexes(
        [
            IndexModel([("nombre", ASCENDING)], name="idx_nombre_unico", unique=True),
            IndexModel([("tipo_objeto", ASCENDING)], name="idx_tipo_objeto"),
            IndexModel([("objeto_padre_id", ASCENDING)], name="idx_objeto_padre"),
            IndexModel([("etiquetas", ASCENDING)], name="idx_etiquetas"),
        ]
    )

    await database["documents"].create_indexes(
        [
            IndexModel(
                [("fuente", ASCENDING), ("fecha_publicacion", ASCENDING)],
                name="idx_fuente_fecha",
            ),
            IndexModel([("titulo", ASCENDING)], name="idx_titulo"),
        ]
    )

    await database["document_chunks"].create_indexes(
        [
            IndexModel([("documento_id", ASCENDING)], name="idx_documento_id"),
            IndexModel([("fuente", ASCENDING)], name="idx_fuente"),
            IndexModel([("embedding", ASCENDING)], name="idx_embedding_exists", sparse=True),
        ]
    )

    await database["query_history"].create_indexes(
        [
            IndexModel([("creado_en", ASCENDING)], name="idx_creado_en"),
        ]
    )

    await close_mongo_connection()

    vector_index = json.loads(VECTOR_INDEX_FILE.read_text(encoding="utf-8"))
    print("Indices normales creados correctamente.")
    print("Configura este indice vectorial en MongoDB Atlas Search:")
    print(json.dumps(vector_index, indent=2))


if __name__ == "__main__":
    asyncio.run(crear_indices())
