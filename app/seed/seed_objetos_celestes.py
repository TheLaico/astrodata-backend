import asyncio

from app.core.config import settings
from app.db.mongodb import close_mongo_connection, connect_to_mongo, get_database
from app.seed.datos_objetos_celestes import OBJETOS_CELESTES_INICIALES
from app.schemas.objetos_celestes import CrearObjetoCeleste, fecha_actual_utc


async def ejecutar_seed() -> None:
    if not settings.mongodb_configured:
        raise RuntimeError("Define MONGODB_URI en .env antes de ejecutar el seed.")

    await connect_to_mongo()
    database = get_database()
    collection = database["celestial_objects"]

    insertados = 0
    actualizados = 0

    for item in OBJETOS_CELESTES_INICIALES:
        objeto = CrearObjetoCeleste.model_validate(item)
        ahora = fecha_actual_utc()
        documento = objeto.model_dump()
        documento["actualizado_en"] = ahora

        resultado = await collection.update_one(
            {"nombre": objeto.nombre},
            {
                "$set": documento,
                "$setOnInsert": {"creado_en": ahora},
            },
            upsert=True,
        )

        if resultado.upserted_id is not None:
            insertados += 1
        elif resultado.modified_count > 0:
            actualizados += 1

    await close_mongo_connection()
    print(
        f"Seed completado. Insertados: {insertados}. Actualizados: {actualizados}."
    )


if __name__ == "__main__":
    asyncio.run(ejecutar_seed())
