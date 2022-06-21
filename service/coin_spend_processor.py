import logging
import time

from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.condition_opcodes import ConditionOpcode
from chia.util.condition_tools import  conditions_by_opcode
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
                                self.log.info("condition.hint=%s", hint)

                # self.process_cat(
                #     height, coin_name, tail_hash, outer_solution, coin_spend.coin.amount
                # )
            else:
                self.log.debug("Found non-CAT coin spend")

    # def process_cat(self, height, coin_name, tail_hash, outer_solution, amount):
    #     self.log.info("Processing CAT spend with TAIL %s and amount %i", tail_hash, amount)

    #     this_coin_info = outer_solution.rest().rest().rest().first()

    #     this_coin_info_parent_coin_info = this_coin_info.first()
    #     this_coin_info_puzzle_hash = this_coin_info.rest().first()
    #     # this_coin_info_amount = this_coin_info.rest().rest().first()

    #     if len(this_coin_info_parent_coin_info.atom) != 32 or len(this_coin_info_puzzle_hash.atom) != 32:
    #         alert_message = "⚠️ FOUND MALICIOUS COIN SPEND! Coin name 0x{} @channel".format(coin_name)
    #         keybase_alert(alert_message)
    #         self.log.warn(alert_message)
    #         return False
    #     else:
    #         self.log.info("Processed CAT spend and everything is fine - coin_name=%s height=%i", coin_name, height)
    #         return True
