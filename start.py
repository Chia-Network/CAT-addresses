import asyncio
import logging
import sqlite3
import sys
from src.coin_store import CoinStore
from src.config import Config
from src.full_node_client import FullNodeClient
from src.height_persistance import HeightPersistance

from src.coin_spend_processor import CoinSpendProcessor

connection = sqlite3.connect('/root/.chia/mainnet/db/cat.db')

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

log = logging.getLogger('start')


async def start():
    config = Config()
    coin_store = CoinStore(connection)
    coin_store.init()
    coin_spend_processor = CoinSpendProcessor(coin_store)
    height_persistance = HeightPersistance(config, connection)
    full_node_client = FullNodeClient(config, coin_spend_processor, height_persistance, coin_store)

    await full_node_client.bootstrap()
    await full_node_client.collect_coins()

    log.info("Coins collected")

    # todo: generate summary and export snapshot data

if __name__ == "__main__":
    asyncio.run(start())
