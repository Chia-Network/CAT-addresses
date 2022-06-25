import asyncio
import logging
import sys
import time
from src.coin_spend_processor import CoinSpendProcessor

from src.config import Config
from src.full_node import FullNode
from src.height_persistance import HeightPersistance

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

log = logging.getLogger('start')


async def main():
    full_node = await FullNode.create()

    while True:
        blockchain_state = await full_node.get_blockchain_state()
        peak = blockchain_state["peak"]

        persisted_height = HeightPersistance.get()

        height = persisted_height + 1

        if height > Config.target_height:
            break

        if height < peak.height:
            block_record = await full_node.get_block_record_by_height(height)

            log.debug("Got block record %s at height: %i", block_record.header_hash, height)

            if block_record.timestamp is not None:
                log.debug("Processing transaction block %s", block_record.header_hash)

                coin_spends = await full_node.get_block_spends(block_record.header_hash)

                log.debug("%i spends found in block", len(coin_spends))

                CoinSpendProcessor.process_coin_spends(height, block_record.header_hash, coin_spends)
            else:
                log.debug("Skipping non-transaction block at height %i", height)

            HeightPersistance.set(height)
        else:
            time.sleep(5)

    log.info("Coins collected")

    # todo: generate summary and export snapshot data

if __name__ == "__main__":
    asyncio.run(main())
