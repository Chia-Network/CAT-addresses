import logging

from typing import Dict, List, Optional
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.condition_with_args import ConditionWithArgs
from chia.util.condition_tools import conditions_dict_for_solution
from chia.util.hash import std_hash
from chia.util.ints import uint64
from chia.wallet.cat_wallet.cat_utils import CAT_MOD, construct_cat_puzzle, match_cat_puzzle
from clvm.casts import int_from_bytes, int_to_bytes
from src.coin_store import CoinRecord, CoinStore

log = logging.getLogger("CoinSpendProcessor")


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
    @staticmethod
    def process_coin_spends(height, header_hash: str, coin_spends: Optional[List[CoinSpend]]):
        if coin_spends is None or len(coin_spends) == 0:
            return None

        log.info("Processing %i coin spends for block %s at height %i", len(coin_spends), header_hash, height)

        for coin_spend in coin_spends:
            outer_puzzle = coin_spend.puzzle_reveal.to_program()
            matched, curried_args = match_cat_puzzle(outer_puzzle)

            if matched:
                _, tail_hash, inner_puzzle = curried_args
                spent_coin_name = coin_spend.coin.name()

                spent_coin_record = CoinRecord(
                    coin_name=spent_coin_name.hex(),
                    inner_puzzle_hash=inner_puzzle.get_tree_hash().hex(),
                    outer_puzzle_hash=outer_puzzle.get_tree_hash().hex(),
                    amount=coin_spend.coin.amount,
                    tail_hash=tail_hash.as_python().hex(),
                    spent_height=height
                )
                CoinStore.persist(spent_coin_record)

                log.info(
                    "Persisted CAT coin spent with name %s, TAIL %s, height %i",
                    spent_coin_name.hex(),
                    tail_hash.as_python().hex(),
                    height
                )

                outer_solution = coin_spend.solution.to_program()
                inner_solution = outer_solution.first()

                _, conditions, _ = conditions_dict_for_solution(inner_puzzle, inner_solution, 0)

                if conditions is not None:
                    create_coin_conditions = created_outputs_for_conditions_dict(conditions, spent_coin_name)
                    if create_coin_conditions is not None:
                        for coin in create_coin_conditions:
                            inner_puzzle_hash = coin.puzzle_hash
                            outer_puzzle_hash = construct_cat_puzzle(
                                CAT_MOD,
                                bytes32.fromhex(tail_hash.as_python().hex()),
                                inner_puzzle_hash
                            ).get_tree_hash(inner_puzzle_hash)

                            amount = coin.amount
                            parent_coin_info = spent_coin_name
                            created_coin_name = std_hash(parent_coin_info + outer_puzzle_hash + int_to_bytes(amount))

                            created_coin_record = CoinRecord(
                                coin_name=created_coin_name.hex(),
                                inner_puzzle_hash=inner_puzzle_hash.hex(),
                                outer_puzzle_hash=outer_puzzle_hash.hex(),
                                amount=amount,
                                tail_hash=tail_hash.as_python().hex()
                            )
                            CoinStore.persist(created_coin_record)

                            log.info(
                                "Persisted CAT coin created with name %s, TAIL %s, height %i",
                                created_coin_name.hex(),
                                tail_hash.as_python().hex(),
                                height
                            )
            else:
                log.debug("Found non-CAT coin spend")
