class CoinCreateRecord:
    coin_name: str
    inner_puzzle_hash: str
    outer_puzzle_hash: str
    amount: int
    tail_hash: str
    created_height: int

    def __init__(
        self,
        coin_name: str,
        inner_puzzle_hash: str,
        outer_puzzle_hash: str,
        amount: int,
        tail_hash: str,
        created_height: int
    ):
        self.coin_name = coin_name
        self.inner_puzzle_hash = inner_puzzle_hash
        self.outer_puzzle_hash = outer_puzzle_hash
        self.amount = amount
        self.tail_hash = tail_hash
        self.created_height = created_height
