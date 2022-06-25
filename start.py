import asyncio
import logging
import sys
from src.cat_snapshot import CatSnapshot

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


async def main():
    cat_snapshot = await CatSnapshot.create()

    await cat_snapshot.generate()

    # todo: generate summary and export snapshot data

if __name__ == "__main__":
    asyncio.run(main())
