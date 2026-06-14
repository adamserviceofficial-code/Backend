import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def list_dbs():
    config_path = "../config.env"
    env_vars = {}
    with open(config_path, "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.split("=", 1)
                env_vars[key.strip()] = val.strip().strip('"').strip("'")
    
    db_uri = env_vars.get("DATABASE")
    client = AsyncIOMotorClient(db_uri)
    
    print("Listing all databases...")
    dbs = await client.list_database_names()
    for db_name in dbs:
        print(f"Database: {db_name}")
        db = client.get_database(db_name)
        collections = await db.list_collection_names()
        print(f"  Collections: {collections}")

if __name__ == "__main__":
    asyncio.run(list_dbs())
