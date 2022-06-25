class CoinRecord:
    coin_name: str
    inner_puzzle_hash: str
    outer_puzzle_hash: str
    amount: int
    tail_hash: str
    spent_height: int

    def __init__(
        self,
        coin_name: str,
        inner_puzzle_hash: str,
        outer_puzzle_hash: str,
        amount: int,
        tail_hash: str,
        spent_height: int = 0
    ):
        self.coin_name = coin_name
        self.inner_puzzle_hash = inner_puzzle_hash
        self.outer_puzzle_hash = outer_puzzle_hash
        self.amount = amount
        self.tail_hash = tail_hash
        self.spent_height = spent_height
