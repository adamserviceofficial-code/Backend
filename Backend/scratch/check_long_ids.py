import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def check_all_movies():
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
    
    print("Checking for long IDs in ALL movies...")
    async for movie in db.movie.find():
        for q in movie.get("telegram", []):
            if len(q.get("id", "")) > 60:
                print(f"Found long ID in movie: {movie.get('title')}")
                print(f"  ID: {q.get('id')}")

if __name__ == "__main__":
    asyncio.run(check_all_movies())
