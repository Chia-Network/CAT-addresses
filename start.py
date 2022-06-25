import asyncio
import logging
import sys
from src.full_node_client import FullNodeClient

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

log = logging.getLogger('start')


async def main():
    full_node_client = FullNodeClient()

    await full_node_client.bootstrap()
    await full_node_client.collect_coins()

    log.info("Coins collected")

    # todo: generate summary and export snapshot data

if __name__ == "__main__":
    asyncio.run(main())
