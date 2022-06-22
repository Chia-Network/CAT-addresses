import logging
import time

from chia.types.condition_opcodes import ConditionOpcode
from chia.util.condition_tools import conditions_by_opcode, conditions_dict_for_solution, created_outputs_for_conditions_dict
from chia.wallet.cat_wallet.cat_utils import match_cat_puzzle
from clvm.casts import int_from_bytes


class CoinSpendProcessor:
    last_heartbeat_time = time.time()
    log = logging.getLogger("CoinSpendProcessor")

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

                self.log.info("outer_solution=%s", outer_solution)

                _, conditions, _ = conditions_dict_for_solution(inner_puzzle, inner_solution, 0)

                if conditions is not None:
                    create_coin_conditions = created_outputs_for_conditions_dict(conditions, coin_name)
                    if create_coin_conditions is not None:
                        for coin in create_coin_conditions:
                            # we extract the puzzle hash from the conditions before the CAT is executed

                            self.log.info("inner_puzzle_hash=%s amount=%i", coin.puzzle_hash, coin.amount)

                            self.record_cat_coin(
                                height, coin_name, tail_hash, coin.puzzle_hash, coin.amount
                            )
            else:
                self.log.debug("Found non-CAT coin spend")

    def record_cat_coin(self, height, coin_name, tail_hash, inner_puzzle_hash, amount):
        self.log.info(
            "Recording CAT coin created with coin name %s, TAIL %s, inner_puzzle_hash %s, amount %i, at block height %i",
            coin_name,
            tail_hash,
            inner_puzzle_hash,
            amount,
            height
        )

        # todo: record created CAT coin details
