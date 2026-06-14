import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

async def check_db():
    load_dotenv("config.env")
    db_uri = os.environ.get("DATABASE")
    client = AsyncIOMotorClient(db_uri)
    db = client.get_database("projectS")
    
    print("Checking Movies...")
    async for movie in db.movie.find().sort("updated_on", -1).limit(5):
        print(f"Movie: {movie.get('title')}")
        for q in movie.get("telegram", []):
            print(f"  ID: {q.get('id')}")
            
    print("\nChecking TV Shows...")
    async for tv in db.tv.find().sort("updated_on", -1).limit(5):
        print(f"TV: {tv.get('title')}")
        for season in tv.get("seasons", []):
            for episode in season.get("episodes", []):
                for q in episode.get("telegram", []):
                    print(f"  ID: {q.get('id')}")

if __name__ == "__main__":
    asyncio.run(check_db())
