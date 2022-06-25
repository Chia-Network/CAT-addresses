import asyncio
import logging
import sys
from src.coin_store import CoinStore
from src.full_node_client import FullNodeClient
from src.height_persistance import HeightPersistance

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

log = logging.getLogger('start')


async def start():
    CoinStore.init()
    HeightPersistance.init()
    full_node_client = FullNodeClient()

    await full_node_client.bootstrap()
    await full_node_client.collect_coins()

    log.info("Coins collected")

    # todo: generate summary and export snapshot data

if __name__ == "__main__":
    asyncio.run(start())
