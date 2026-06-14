import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def get_ids():
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
    
    async for movie in db.movie.find().limit(5):
        print(f"TMDB ID: {movie.get('tmdb_id')} | Title: {movie.get('title')}")

if __name__ == "__main__":
    asyncio.run(get_ids())
