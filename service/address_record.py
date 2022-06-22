from chia.types.blockchain_format.sized_bytes import bytes32


class AddressRecord:
    tail_hash: str
    inner_puzzle_hash: bytes32
    outer_puzzle_hash: bytes32
    inner_address: str
    outer_address: str

    def __init__(
        self,
        tail_hash: str,
        inner_puzzle_hash: bytes32,
        outer_puzzle_hash: bytes32,
        inner_address: str,
        outer_address: str
    ):
        self.tail_hash = tail_hash
        self.inner_puzzle_hash = inner_puzzle_hash
        self.outer_puzzle_hash = outer_puzzle_hash
        self.inner_address = inner_address
        self.outer_address = outer_address
