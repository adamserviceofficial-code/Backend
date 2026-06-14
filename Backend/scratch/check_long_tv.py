import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def check_all_tv():
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
    
    print("Checking for long IDs in ALL TV shows...")
    async for tv in db.tv.find():
        for season in tv.get("seasons", []):
            for episode in season.get("episodes", []):
                for q in episode.get("telegram", []):
                    if len(q.get("id", "")) > 60:
                        print(f"Found long ID in TV: {tv.get('title')}")
                        print(f"  ID: {q.get('id')}")

if __name__ == "__main__":
    asyncio.run(check_all_tv())
