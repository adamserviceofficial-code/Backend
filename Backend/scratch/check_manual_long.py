import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def check_manual_files():
    config_path = "../config.env"
    env_vars = {}
    with open(config_path, "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.split("=", 1)
                env_vars[key.strip()] = val.strip().strip('"').strip("'")
    
    db_uri = env_vars.get("DATABASE")
    client = AsyncIOMotorClient(db_uri)
    db = client.get_database("projectS")
    
    print("Checking for long IDs in ALL manual files...")
    async for f in db.manual_files.find():
        if "id" in f and len(f.get("id", "")) > 60:
            print(f"Found long ID in manual file: {f.get('name')}")
            print(f"  ID: {f.get('id')}")

if __name__ == "__main__":
    asyncio.run(check_manual_files())
