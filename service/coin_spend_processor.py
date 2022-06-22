import logging
import time

from chia.util.bech32m import encode_puzzle_hash
from chia.util.condition_tools import conditions_dict_for_solution, created_outputs_for_conditions_dict
from chia.wallet.cat_wallet.cat_utils import match_cat_puzzle

from service.address_record import AddressRecord
from service.address_store import AddressStore

prefix = "xch"


class CoinSpendProcessor:
    last_heartbeat_time = time.time()
    log = logging.getLogger("CoinSpendProcessor")
    address_store = AddressStore("addresses.dat")

    def process_coin_spends(self, height, header_hash: str, coin_spends, height_persistance):
        self.log.info("Processing %i coin spends for block %s at height %i", len(coin_spends), header_hash, height)

        for coin_spend in coin_spends:
            outer_puzzle = coin_spend.puzzle_reveal.to_program()
            outer_puzzle_hash = outer_puzzle.get_tree_hash()
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
                            address_record = AddressRecord(
                                tail_hash,
                                coin.puzzle_hash,
                                outer_puzzle_hash,
                                encode_puzzle_hash(coin.puzzle_hash, prefix),
                                encode_puzzle_hash(outer_puzzle_hash, prefix)
                            )

                            self.log.info("Recording CAT address record %s", address_record)

                            self.address_store.add(address_record)
            else:
                self.log.debug("Found non-CAT coin spend")
