import aiohttp
import backoff
import logging
from typing import Dict, List, Optional
from chia.consensus.block_record import BlockRecord
from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_record import CoinRecord
from chia.types.coin_spend import CoinSpend
from chia.util.ints import uint32
from src.config import RpcOptions


class FullNode:
    log = logging.getLogger("FullNode")
    client: FullNodeRpcClient

    def __init__(self, client: FullNodeRpcClient):
        self.client = client

    @staticmethod
    async def create():
        client = await FullNodeRpcClient.create(
            RpcOptions.hostname, RpcOptions.port, RpcOptions.chia_root, RpcOptions.config
        )

        return await FullNode(client).__startup()
    
    def close(self):
        self.client.close()

    @backoff.on_exception(
        backoff.expo,
        (ConnectionRefusedError, aiohttp.client_exceptions.ClientConnectorError, Exception),
        max_tries=RpcOptions.retry_count
    )
    async def __startup(self):
        self.log.info("Checking node status")

        blockchain_state = await self.get_blockchain_state()

        curr: Optional[BlockRecord] = blockchain_state["peak"]

        if curr is None:
            raise Exception("Not ready to accept connections. Waiting for peak.")

        self.log.info("Node online")

        return self

    @backoff.on_exception(backoff.expo, ValueError, max_tries=RpcOptions.retry_count)
    async def get_blockchain_state(self) -> Dict:
        return await self.client.get_blockchain_state()

    @backoff.on_exception(backoff.expo, ValueError, max_tries=RpcOptions.retry_count)
    async def get_block_record_by_height(self, height):
        return await self.client.get_block_record_by_height(height)

    @backoff.on_exception(backoff.expo, ValueError, max_tries=RpcOptions.retry_count)
    async def get_block_spends(self, header_hash: str) -> Optional[List[CoinSpend]]:
        return await self.client.get_block_spends(header_hash)

    @backoff.on_exception(backoff.expo, ValueError, max_tries=RpcOptions.retry_count)
    async def get_coin_record_by_name(self, coin_id: bytes32) -> CoinRecord:
        return await self.client.get_coin_record_by_name(coin_id)

    @backoff.on_exception(backoff.expo, ValueError, max_tries=RpcOptions.retry_count)
    async def get_puzzle_and_solution(self, coin_id: bytes32, height: uint32) -> Optional[CoinSpend]:
        return await self.client.get_puzzle_and_solution(coin_id, height)

    @backoff.on_exception(backoff.expo, ValueError, max_tries=RpcOptions.retry_count)
    async def get_coin_records_by_parent_ids(self, parent_ids: List[bytes32], include_spent_coins: bool) -> List[CoinRecord]:
        return await self.client.get_coin_records_by_parent_ids(parent_ids, include_spent_coins)
