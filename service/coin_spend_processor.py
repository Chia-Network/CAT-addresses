import logging
import time

from chia.types.condition_opcodes import ConditionOpcode
from chia.util.condition_tools import conditions_by_opcode
from chia.wallet.cat_wallet.cat_utils import match_cat_puzzle
from clvm.casts import int_from_bytes

from service.utils import parse_sexp_to_conditions


class CoinSpendProcessor:
    last_heartbeat_time = time.time()
    log = logging.getLogger("CoinSpendProcessor")

    def process_coin_spends(self, height, header_hash: str, coin_spends, height_persistance):
        self.log.debug("Processing %i coin spends for block %s at height %i", len(coin_spends), header_hash, height)

        for coin_spend in coin_spends:
            outer_puzzle = coin_spend.puzzle_reveal.to_program()
            matched, curried_args = match_cat_puzzle(outer_puzzle)

            if matched:
                _, tail_hash, _ = curried_args

                outer_solution = coin_spend.solution.to_program()
                coin_name = coin_spend.coin.name()

                r = outer_puzzle.run(outer_solution)
                _, conditions = parse_sexp_to_conditions(r)

                if conditions is not None:
                    cbo = conditions_by_opcode(conditions)
                    create_coin_conditions = cbo.get(ConditionOpcode.CREATE_COIN)
                    if create_coin_conditions is not None:
                        for condition in create_coin_conditions:
                            puzzle_hash = condition.vars[0]
                            amount = int_from_bytes(condition.vars[1])

                            if len(condition.vars) < 2:
                                self.log.warn("Found CAT create coin condition without a hint")
                            else:
                                hint = condition.vars[2]
                                self.record_cat_coin(
                                    height, coin_name, tail_hash, puzzle_hash, amount, hint
                                )
            else:
                self.log.debug("Found non-CAT coin spend")

    def record_cat_coin(self, height, coin_name, tail_hash, puzzle_hash, amount, hint):
        self.log.info(
            "Recording CAT coin created with coin name %s, TAIL %s, puzzle_hash %s, amount %i, and hint %s, at block height %i",
            coin_name,
            tail_hash,
            puzzle_hash,
            amount,
            hint,
            height
        )

        # todo: record created CAT coin details
