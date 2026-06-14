import asyncio
from Backend import db

async def list_collections():
    await db.connect()
    collections = await db.db.list_collection_names()
    print("All collections:", collections)
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(list_collections())
