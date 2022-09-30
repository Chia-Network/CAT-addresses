import asyncio
import logging
import sys
from src.cat_snapshot import CatSnapshot

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


async def main():
    cat2 = "--cat2" in sys.argv
    cat_snapshot = await CatSnapshot.create(cat2)
    await cat_snapshot.generate()

if __name__ == "__main__":
    asyncio.run(main())
