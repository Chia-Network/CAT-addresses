import asyncio
import logging
import sqlite3
import sys
from src.full_node_client import FullNodeClient
from src.height_persistance import HeightPersistance

from src.coin_spend_processor import CoinSpendProcessor

connection = sqlite3.connect('cat.db')

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


async def start():
    coin_spend_processor = CoinSpendProcessor(connection)
    height_persistance = HeightPersistance(connection)
    full_node_client = FullNodeClient(coin_spend_processor, height_persistance)

    await full_node_client.bootstrap()
    await full_node_client.start()

if __name__ == "__main__":
    asyncio.run(start())
