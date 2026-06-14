
import asyncio
import os
import sys
from bson import ObjectId
import motor.motor_asyncio

# Add the project root to sys.path
sys.path.append(os.getcwd())

from Backend.config import Telegram

async def inspect_languages():
    uri = Telegram.DATABASE
    if isinstance(uri, list):
        uri = uri[0]
    
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db = client["projectS"]
    
    print("Searching for all TV shows...")
    shows = await db.tv.find({}, {"title": 1, "languages": 1, "tmdb_id": 1}).to_list(None)
    for show in shows:
        print(f"Title: {show.get('title')}")
        print(f"  - TMDB ID: {show.get('tmdb_id')}")
        print(f"  - Languages: {show.get('languages')}")
        
    client.close()

if __name__ == "__main__":
    asyncio.run(inspect_languages())
