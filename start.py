import asyncio
import logging
import os
import sys
from service.full_node_client import FullNodeClient
from service.height_persistance import HeightPersistance

from service.coin_spend_processor import CoinSpendProcessor

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


async def start():
    coin_spend_processor = CoinSpendProcessor()
    height_persistance = HeightPersistance(os.getenv("HEIGHT_PERSISTANCE_FILE_PATH", "height.dat"))
    full_node_client = FullNodeClient(coin_spend_processor, height_persistance)

    await full_node_client.bootstrap()
    await full_node_client.start()

if __name__ == "__main__":
    asyncio.run(start())
