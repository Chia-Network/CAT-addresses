import logging
from typing import List, Optional, Tuple

from chia.types.blockchain_format.program import Program
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.condition_with_args import ConditionWithArgs
from chia.util.errors import ConsensusError, Err

log = logging.getLogger("utils")


def as_atom_list(sexp: Program) -> List[bytes]:
    items = []
    obj = sexp
    while True:
        pair = obj.pair
        if pair is None:
            break
        atom = pair[0].atom
        obj = pair[1]
        if atom is None:
            # extract hint in coin create condition
            pair = pair[0].pair
            if pair is None:
                break
            if pair[1].atom == b"":
                items.append(pair[0].atom)
        else:
            items.append(atom)
    return items


def parse_sexp_to_condition(
    sexp: Program,
) -> Tuple[Optional[Err], Optional[ConditionWithArgs]]:
    """
    Takes a ChiaLisp sexp and returns a ConditionWithArgs.
    If it fails, returns an Error
    """
    as_atoms = as_atom_list(sexp)

    if len(as_atoms) < 1:
        return Err.INVALID_CONDITION, None
    opcode = as_atoms[0]
    opcode = ConditionOpcode(opcode)
    return None, ConditionWithArgs(opcode, as_atoms[1:])


def parse_sexp_to_conditions(
    sexp: Program,
) -> Tuple[Optional[Err], Optional[List[ConditionWithArgs]]]:
    """
    Takes a ChiaLisp sexp (list) and returns the list of ConditionWithArgss
    If it fails, returns as Error
    """
    results: List[ConditionWithArgs] = []
    try:
        for _ in sexp.as_iter():
            error, cvp = parse_sexp_to_condition(_)
            if error:
                return error, None
            results.append(cvp)  # type: ignore # noqa
    except ConsensusError:
        return Err.INVALID_CONDITION, None
    return None, results
