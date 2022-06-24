import asyncio
import logging
import sqlite3
import sys
from src.coin_store import CoinStore
from src.config import Config
from src.full_node_client import FullNodeClient
from src.height_persistance import HeightPersistance

from src.coin_spend_processor import CoinSpendProcessor
from src.puzzlehash_store import PuzzlehashStore

connection = sqlite3.connect('/root/.chia/mainnet/db/cat.db')

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


async def start():
    config = Config()
    puzzle_hash_store = PuzzlehashStore(connection)
    coin_store = CoinStore(connection)
    puzzle_hash_store.init()
    coin_store.init()
    coin_spend_processor = CoinSpendProcessor(puzzle_hash_store)
    height_persistance = HeightPersistance(config, connection)
    full_node_client = FullNodeClient(config, coin_spend_processor, height_persistance, puzzle_hash_store, coin_store)

    await full_node_client.bootstrap()
    await full_node_client.collect_puzzle_hashes()
    await full_node_client.collect_unspent_coins()

    # todo: generate summary and export snapshot data

if __name__ == "__main__":
    asyncio.run(start())
