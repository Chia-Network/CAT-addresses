import logging
import sqlite3
import time

from typing import Dict, List
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.condition_with_args import ConditionWithArgs
from chia.util.condition_tools import conditions_dict_for_solution
from chia.util.ints import uint64
from chia.wallet.cat_wallet.cat_utils import match_cat_puzzle
from clvm.casts import int_from_bytes

from src.puzzlehash_store import PuzzlehashRecord, PuzzlehashStore
from src.snapshot import Snapshot


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


class CoinSpendProcessor:
    last_heartbeat_time = time.time()
    log = logging.getLogger("CoinSpendProcessor")
    snapshot = Snapshot("snapshot.csv")

    def __init__(self, connection: sqlite3.Connection):
        self.puzzle_hash_store = PuzzlehashStore(connection)
        self.puzzle_hash_store.init()

    def process_coin_spends(self, height, header_hash: str, coin_spends, height_persistance):
        self.log.info("Processing %i coin spends for block %s at height %i", len(coin_spends), header_hash, height)

        for coin_spend in coin_spends:
            outer_puzzle = coin_spend.puzzle_reveal.to_program()
            matched, curried_args = match_cat_puzzle(outer_puzzle)

            if matched:
                _, tail_hash, inner_puzzle = curried_args

                coin_name = coin_spend.coin.name()
                outer_solution = coin_spend.solution.to_program()
                inner_solution = outer_solution.first()

                self.log.info("inner_puzzle=%s", inner_puzzle)
                self.log.info("inner_solution=%s", inner_solution)

                _, conditions, _ = conditions_dict_for_solution(inner_puzzle, inner_solution, 0)

                if conditions is not None:
                    create_coin_conditions = created_outputs_for_conditions_dict(conditions, coin_name)
                    if create_coin_conditions is not None:
                        for coin in create_coin_conditions:
                            puzzle_hash_record = PuzzlehashRecord(
                                coin.puzzle_hash,
                                tail_hash
                            )
                            self.puzzle_hash_store.persist(puzzle_hash_record)

                            self.log.info(
                                "Persisted puzzle hash record: %s %s",
                                puzzle_hash_record.inner_puzzle_hash,
                                puzzle_hash_record.tail_hash
                            )
            else:
                self.log.debug("Found non-CAT coin spend")
