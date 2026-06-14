import asyncio
from themoviedb import aioTMDb

tmdb = aioTMDb(key="44cf8f2bba6890333d4ffcb6fa1dd7f6", language="en-US", region="US")

async def main():
    movies_details = await tmdb.movie(24428).details() # The Avengers
    print(movies_details.belongs_to_collection)
    if movies_details.belongs_to_collection:
        print(movies_details.belongs_to_collection.id)
        print(movies_details.belongs_to_collection.name)

asyncio.run(main())
