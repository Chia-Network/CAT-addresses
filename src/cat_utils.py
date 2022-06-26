from typing import Dict, List, Tuple, Union
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.blockchain_format.program import Program
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.condition_with_args import ConditionWithArgs
from chia.util.condition_tools import conditions_dict_for_solution
from chia.util.ints import uint64
from chia.wallet.cat_wallet.cat_utils import match_cat_puzzle
from clvm.casts import int_from_bytes


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


def extract_cat(coin_spend: CoinSpend) -> Union[
    None,
    Tuple[
        Program,
        Program,
        Program,
        Program,
        Program
    ]
]:
    outer_puzzle = coin_spend.puzzle_reveal.to_program()
    outer_solution = coin_spend.solution.to_program()
    matched, curried_args = match_cat_puzzle(outer_puzzle)

    if not matched:
        return None

    _, tail_hash, inner_puzzle = curried_args
    inner_solution = outer_solution.first()

    # _, inner_puzzle_conditions, _ = conditions_dict_for_solution(inner_puzzle, inner_solution, 0)

    # inner_puzzle_create_coin_conditions = []
    # if inner_puzzle_conditions is not None:
    #     inner_puzzle_create_coin_conditions = created_outputs_for_conditions_dict(inner_puzzle_conditions, coin_spend.coin.name())

    return tail_hash, outer_puzzle, outer_solution, inner_puzzle, inner_solution
