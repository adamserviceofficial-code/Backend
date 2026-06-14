import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def debug_movies():
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
    
    print("Listing some movies and their IDs...")
    async for movie in db.movie.find().limit(10):
        print(f"Movie: {movie.get('title')}")
        for q in movie.get("telegram", []):
            print(f"  ID Length: {len(q.get('id', ''))} | ID: {q.get('id')[:20]}...")

if __name__ == "__main__":
    asyncio.run(debug_movies())
