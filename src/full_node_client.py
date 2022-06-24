import aiohttp
import backoff
import logging
import time
from typing import List, Optional

from chia.consensus.block_record import BlockRecord
from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_record import CoinRecord
from chia.wallet.cat_wallet.cat_utils import CAT_MOD, construct_cat_puzzle
from src.coin_store import CoinStore, CoinRecord as CR
from src.config import Config

from src.height_persistance import HeightPersistance
from src.puzzlehash_store import PuzzlehashStore
from src.rpc_options import RpcOptions
from src.coin_spend_processor import CoinSpendProcessor

backoff_logger = logging.getLogger('backoff')

backoff_logger.addHandler(logging.StreamHandler())
backoff_logger.setLevel(logging.ERROR)


class FullNodeClient:
    client: FullNodeRpcClient
    height_persistance: HeightPersistance
    puzzle_hash_store: PuzzlehashStore
    coin_store: CoinStore
    log = logging.getLogger("FullNodeClient")
    rpc_options = RpcOptions()
    coin_spend_processor: CoinSpendProcessor

    def __init__(
        self,
        config: Config,
        coin_spend_processor: CoinSpendProcessor,
        height_persistance: HeightPersistance,
        puzzle_hash_store: PuzzlehashStore,
        coin_store: CoinStore
    ):
        self.config = config
        self.height_persistance = height_persistance
        self.puzzle_hash_store = puzzle_hash_store
        self.coin_store = coin_store
        self.coin_spend_processor = coin_spend_processor
        self.height_persistance.init()

    @backoff.on_exception(
        backoff.expo, (ConnectionRefusedError, aiohttp.client_exceptions.ClientConnectorError, Exception), max_tries=10
    )
    async def bootstrap(self):
        self.client = await FullNodeRpcClient.create(
            self.rpc_options.hostname, self.rpc_options.port, self.rpc_options.chia_root, self.rpc_options.config
        )

        self.log.debug("Checking node status")

        blockchain_state = await self.client.get_blockchain_state()

        curr: Optional[BlockRecord] = blockchain_state["peak"]

        if curr is None:
            raise Exception("Not ready to accept connections. Waiting for peak.")

        self.log.debug("Node online")

    """
    Initially processes blocks quickly then polls every 5 seconds once we reach the peak
    """

    @backoff.on_predicate(backoff.constant, jitter=None, interval=0)
    async def collect_puzzle_hashes(self):
        peak = await self.__get_peak()
        persisted_height = self.height_persistance.get()

        height = persisted_height + 1

        if height > self.config.target_height:
            self.log.info("Reached target height")
            return True

        if height < peak.height:
            block_record = await self.__get_block_record(height)

            self.log.debug("Got block record %s at height: %i", block_record.header_hash, height)

            if block_record.timestamp is not None:
                await self.__process_transaction_block(height, block_record.header_hash)
            else:
                self.log.debug("Skipping non-transaction block at height %i", height)

            self.height_persistance.set(height)
        else:
            time.sleep(5)

        return False

    @backoff.on_predicate(backoff.constant, jitter=None, interval=0)
    async def collect_unspent_coins(self):
        puzzle_hash_records = self.puzzle_hash_store.get(processed=0, count=3)

        # All puzzle hash records have been processed
        if len(puzzle_hash_records) == 0:
            return True

        for (inner_puzzle_hash, tail_hash) in puzzle_hash_records:
            outer_puzzle_hash = construct_cat_puzzle(
                CAT_MOD, bytes32.fromhex(tail_hash), bytes32.fromhex(inner_puzzle_hash)
            ).get_tree_hash(bytes32.fromhex(inner_puzzle_hash))

            coins = await self.__get_coin_records_by_puzzle_hash(outer_puzzle_hash, True)

            for coin in coins:
                # Only process coins that were not spent up to the target height
                if coin.spent_block_index == 0 or coin.spent_block_index > self.config.target_height:
                    coin_record = CR(
                        coin.coin.name().hex(),
                        inner_puzzle_hash,
                        outer_puzzle_hash.hex(),
                        coin.coin.amount,
                        tail_hash
                    )
                    self.coin_store.persist(coin_record)

                    self.log.info("Persisted coin record for coin: %s", coin_record.coin_name)

            self.puzzle_hash_store.mark_processed(
                inner_puzzle_hash,
                tail_hash,
                1
            )

            self.log.info("Marked processed. inner_puzzle_hash=%s tail_hash=%s", inner_puzzle_hash, tail_hash)

        return False

    async def __process_transaction_block(self, height, header_hash):
        self.log.debug("Processing transaction block %s", header_hash)

        coin_spends = await self.__get_block_spends(header_hash)

        self.log.debug("%i spends found in block", len(coin_spends))

        self.coin_spend_processor.process_coin_spends(height, header_hash, coin_spends, self.height_persistance)

    @backoff.on_exception(backoff.expo, ValueError, max_tries=10)
    async def __get_peak(self):
        blockchain_state = await self.client.get_blockchain_state()
        return blockchain_state["peak"]

    @backoff.on_exception(backoff.expo, ValueError, max_tries=10)
    async def __get_block_record(self, height):
        return await self.client.get_block_record_by_height(height)

    @backoff.on_exception(backoff.expo, ValueError, max_tries=10)
    async def __get_block_spends(self, header_hash: str):
        return await self.client.get_block_spends(header_hash)

    @backoff.on_exception(backoff.expo, ValueError, max_tries=10)
    async def __get_coin_records_by_puzzle_hash(
        self,
        puzzle_hash: bytes32,
        include_spent_coins: bool = False
    ) -> List[CoinRecord]:
        return await self.client.get_coin_records_by_puzzle_hash(
            puzzle_hash,
            include_spent_coins,
            start_height=self.config.start_height,
            end_height=self.config.target_height
        )
