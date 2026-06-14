import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient

sys.path.append(os.getcwd())
from Backend.config import Telegram

async def create_indices():
    uri = Telegram.DATABASE
    if isinstance(uri, list):
        uri = uri[0]
    
    print(f"Connecting to database to create indexes...")
    client = AsyncIOMotorClient(uri)
    db = client["projectS"]
    
    for coll_name in ["movie", "tv"]:
        collection = db[coll_name]
        print(f"Creating indices for {coll_name}...")
        
        # Sort indices
        await collection.create_index([("updated_on", -1)])
        await collection.create_index([("views", -1)])
        await collection.create_index([("rating", -1)])
        
        # Search index
        await collection.create_index([("title", "text")])
        
        print(f"Created indices for {coll_name}")

    client.close()

if __name__ == "__main__":
    asyncio.run(create_indices())
