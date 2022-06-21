from chia.types.blockchain_format.program import Program
from service.utils import parse_sexp_to_conditions

from chia.types.condition_opcodes import ConditionOpcode
from chia.types.condition_with_args import ConditionWithArgs


def test_parse_sexp_to_conditions():
    conditions = parse_sexp_to_conditions(
        Program.fromhex(
            "ffff33ffa0b8fa601f85c9a1b638aeee3480d6a8eb5e486db64bdf33b7a0475752" +
            "28c2e002ff830f4240ffffa0628d91d5f1b73957cc726a557da60e7986c35f87e5" +
            "c1c959e10cc358b14847098080ffff33ffa073a10e669f727fefedd03e6bb9294b" +
            "7145cc1015cc2919c0569e4af90a2ac118ff8402fb46708080"
        )
    )

    assert conditions == (
        None,
        [
            ConditionWithArgs(ConditionOpcode.CREATE_COIN, [
                bytes.fromhex("b8fa601f85c9a1b638aeee3480d6a8eb5e486db64bdf33b7a047575228c2e002"),
                bytes.fromhex("0f4240"),
                # hint is extracted
                bytes.fromhex("628d91d5f1b73957cc726a557da60e7986c35f87e5c1c959e10cc358b1484709")
            ]),
            ConditionWithArgs(ConditionOpcode.CREATE_COIN, [
                bytes.fromhex("73a10e669f727fefedd03e6bb9294b7145cc1015cc2919c0569e4af90a2ac118"),
                bytes.fromhex("02fb4670")
            ])
        ]
    )
