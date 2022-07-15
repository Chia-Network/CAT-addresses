import logging
from typing import Dict, List, Optional
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.condition_with_args import ConditionWithArgs
from chia.util.ints import uint64
from chia.util.hash import std_hash
from chia.wallet.cat_wallet.cat_utils import CAT_MOD, construct_cat_puzzle
from clvm.casts import int_from_bytes, int_to_bytes
from src.coin_spend_record import CoinSpendRecord
from src.coin_create_record import CoinCreateRecord
from src.cat_utils import create_coin_conditions_for_inner_puzzle, extract_cat
from src.config import Config
from src.database import connection, get_initial_id, get_next_coin_spends, persist_coin_create, persist_coin_spend
from src.full_node import FullNode


def created_outputs_for_conditions_dict(
    conditions_dict: Dict[ConditionOpcode, List[ConditionWithArgs]],
    input_coin_name: bytes32,
) -> List[Coin]:
    output_coins = []
    for cvp in conditions_dict.get(ConditionOpcode.CREATE_COIN, []):
        puzzle_hash, amount_bin = cvp.vars[0], cvp.vars[1]
        amount = int_from_bytes(amount_bin)
        # ignore magic conditions
        if amount > 0:
            coin = Coin(input_coin_name, bytes32(puzzle_hash), uint64(amount))
            output_coins.append(coin)
    return output_coins


class CatSnapshot:
    log = logging.getLogger('CatSnapshot')
    full_node: FullNode

    def __init__(self, full_node: FullNode):
        self.full_node = full_node

    @staticmethod
    async def create():
        full_node = await FullNode.create()

        return CatSnapshot(full_node)

    async def generate(self):
        # Collect CAT coin spends
        height = Config.start_height
        while True:
            if height > Config.target_height:
                break

            await self.__process_block(height)

            height = height + 1
        # Extract coin create conditions from coin spends
        id = get_initial_id(Config.start_height)
        if id is None:
            self.log.warn("No new coin spends were discovered by this scan")

            connection.close()
            self.full_node.close()

            return None
        while True:
            coin_spends = get_next_coin_spends(id, 100)

            if len(coin_spends) == 0:
                break

            for (
                id,
                coin_name,
                inner_puzzle,
                outer_puzzle,
                inner_solution,
                outer_solution,
                amount,
                tail_hash,
                spent_height
            ) in coin_spends:
                self.log.info(
                    "coin_name %s amount %i tail_hash %s spent_height %s",
                    coin_name,
                    amount,
                    tail_hash,
                    spent_height
                )
                inner_puzzle = Program.fromhex(inner_puzzle)
                outer_puzzle = Program.fromhex(outer_puzzle)
                inner_solution = Program.fromhex(inner_solution)
                outer_solution = Program.fromhex(outer_solution)

                inner_puzzle_create_coin_conditions = create_coin_conditions_for_inner_puzzle(
                    bytes32.fromhex(coin_name),
                    inner_puzzle,
                    inner_solution
                )

                cursor = connection.cursor()

                for coin in inner_puzzle_create_coin_conditions:
                    outer_puzzle_hash = construct_cat_puzzle(
                        CAT_MOD,
                        bytes32.fromhex(tail_hash),
                        coin.puzzle_hash
                    ).get_tree_hash(coin.puzzle_hash)

                    created_coin_name = std_hash(
                        bytes32.fromhex(coin_name) + outer_puzzle_hash + int_to_bytes(coin.amount)
                    ).hex()

                    coin_create_record = CoinCreateRecord(
                        coin_name=created_coin_name,
                        inner_puzzle_hash=coin.puzzle_hash.hex(),
                        outer_puzzle_hash=outer_puzzle_hash.hex(),
                        amount=coin.amount,
                        tail_hash=tail_hash,
                        created_height=spent_height
                    ) 

                    persist_coin_create(cursor, coin_create_record)

                    self.log.info(
                        "Persisted CAT coin created with name %s, TAIL %s, height %i",
                        created_coin_name,
                        tail_hash,
                        spent_height
                    )

                connection.commit()
                cursor.close()

            id = id + 1
        
        self.full_node.close()

    async def __process_block(self, height: int):
        block_record = await self.full_node.get_block_record_by_height(height)

        self.log.debug("Got block record %s at height: %i", block_record.header_hash, height)

        if block_record.timestamp is not None:
            self.log.debug("Processing transaction block %s", block_record.header_hash)

            coin_spends = await self.full_node.get_block_spends(block_record.header_hash)

            if coin_spends is not None:
                self.log.info("%i spends found in block", len(coin_spends))
                self.__process_coin_spends(height, block_record.header_hash, coin_spends)
            else:
                self.log.info("None at %i", height)
        else:
            self.log.info("Skipping non-transaction block at height %i", height)

    def __process_coin_spends(self, height, header_hash: str, coin_spends: Optional[List[CoinSpend]]):
        if coin_spends is None or len(coin_spends) == 0:
            return None

        self.log.info("Processing %i coin spends for block %s at height %i", len(coin_spends), header_hash, height)

        cursor = connection.cursor()

        for coin_spend in coin_spends:
            result = extract_cat(coin_spend)

            if result is None:
                self.log.debug("Found non-CAT coin spend")
            else:
                outer_puzzle = coin_spend.puzzle_reveal.to_program()
                outer_solution = coin_spend.solution.to_program()
                inner_solution = outer_solution.first()
                (
                    tail_hash,
                    outer_puzzle,
                    _,
                    inner_puzzle,
                    _
                ) = result

                spent_coin_record = CoinSpendRecord(
                    coin_name=coin_spend.coin.name().hex(),
                    inner_puzzle=inner_puzzle.__str__(),
                    outer_puzzle=outer_puzzle.__str__(),
                    inner_solution=inner_solution.__str__(),
                    outer_solution=outer_solution.__str__(),
                    amount=coin_spend.coin.amount,
                    tail_hash=tail_hash.as_python().hex(),
                    spent_height=height
                )

                persist_coin_spend(cursor, spent_coin_record)

        connection.commit()
        cursor.close()
