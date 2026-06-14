# ─────────────────────────────────────────────────────────────────────────────
# Author  : ThiruXD
# GitHub  : https://github.com/ThiruXD
# Portfolio: https://thiruxd.is-a.dev
# ─────────────────────────────────────────────────────────────────────────────
import asyncio
import os
import json
import zlib
import base64
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

async def compact_encode(chat_id, msg_id, file_hash):
    raw = f"{chat_id}:{msg_id}:{file_hash}"
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")

def base62_decode(data):
    BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    num = 0
    try:
        for char in data:
            num = num * 62 + BASE62_ALPHABET.index(char)
        return num.to_bytes((num.bit_length() + 7) // 8, 'big') or b'\0'
    except Exception:
        return None

async def decode_string(encoded_data):
    try:
        compressed_data = base62_decode(encoded_data)
        if not compressed_data: return None
        json_data = zlib.decompress(compressed_data).decode()
        return json.loads(json_data)
    except Exception:
        return None

async def migrate():
    # Force load from config.env in parent dir
    env_vars = {}
    config_path = "../config.env"
    if not os.path.exists(config_path):
        config_path = "config.env" # try local too
        
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    env_vars[key.strip()] = val.strip().strip('"').strip("'")
    
    db_uri = env_vars.get("DATABASE")
    if not db_uri:
        print("Error: DATABASE URI not found in config.env")
        return
        
    print(f"Connecting to: {db_uri[:20]}...")
    client = AsyncIOMotorClient(db_uri)
    db = client.get_database("projectS")
    
    try:
        # Test connection
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    print("Starting Migration...")
    
    # Migrate Movies
    movie_count = 0
    print("Fetching movies...")
    cursor = db.movie.find({})
    async for movie in cursor:
        updated_telegram = []
        changed = False
        if "telegram" not in movie: continue
        
        for q in movie.get("telegram", []):
            if "id" in q and len(q["id"]) > 60:
                data = await decode_string(q["id"])
                if data:
                    new_id = await compact_encode(data["chat_id"], data["msg_id"], data["hash"])
                    q["id"] = new_id
                    changed = True
            updated_telegram.append(q)
        
        if changed:
            await db.movie.update_one({"_id": movie["_id"]}, {"$set": {"telegram": updated_telegram}})
            movie_count += 1
            print(f"Migrated movie: {movie.get('title')}")

    # Migrate TV Shows
    tv_count = 0
    print("Fetching TV shows...")
    cursor = db.tv.find({})
    async for tv in cursor:
        changed_tv = False
        if "seasons" not in tv: continue
        
        for season in tv.get("seasons", []):
            for episode in season.get("episodes", []):
                if "telegram" not in episode: continue
                updated_telegram = []
                for q in episode.get("telegram", []):
                    if "id" in q and len(q["id"]) > 60:
                        data = await decode_string(q["id"])
                        if data:
                            new_id = await compact_encode(data["chat_id"], data["msg_id"], data["hash"])
                            q["id"] = new_id
                            changed_tv = True
                    updated_telegram.append(q)
                episode["telegram"] = updated_telegram
        
        if changed_tv:
            await db.tv.update_one({"_id": tv["_id"]}, {"$set": {"seasons": tv["seasons"]}})
            tv_count += 1
            print(f"Migrated TV show: {tv.get('title')}")

    print(f"\nMigration finished!")
    print(f"Movies migrated: {movie_count}")
    print(f"TV Shows migrated: {tv_count}")

if __name__ == "__main__":
    asyncio.run(migrate())
