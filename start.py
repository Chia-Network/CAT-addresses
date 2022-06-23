import asyncio
import logging
import sqlite3
import sys
from src.config import Config
from src.full_node_client import FullNodeClient
from src.height_persistance import HeightPersistance

from src.coin_spend_processor import CoinSpendProcessor

connection = sqlite3.connect('/root/.chia/mainnet/db/cat.db')

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


async def start():
    config = Config()
    coin_spend_processor = CoinSpendProcessor(connection)
    height_persistance = HeightPersistance(config, connection)
    full_node_client = FullNodeClient(config, coin_spend_processor, height_persistance)

    await full_node_client.bootstrap()
    await full_node_client.collect_puzzle_hashes()

if __name__ == "__main__":
    asyncio.run(start())
