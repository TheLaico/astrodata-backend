from motor.motor_asyncio import AsyncIOMotorDatabase


class EstadisticasRepository:
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self.database = database

    async def contar_objetos_celestes(self) -> int:
        return await self.database["celestial_objects"].count_documents({})

    async def contar_documentos(self) -> int:
        return await self.database["documents"].count_documents({})

    async def contar_chunks(self) -> int:
        return await self.database["document_chunks"].count_documents({})

    async def contar_chunks_con_embedding(self) -> int:
        return await self.database["document_chunks"].count_documents(
            {
                "embedding": {
                    "$exists": True,
                    "$ne": None,
                }
            }
        )

    async def contar_consultas_historial(self) -> int:
        return await self.database["query_history"].count_documents({})
