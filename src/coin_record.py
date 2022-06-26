class CoinRecord:
    coin_name: str
    inner_puzzle: str
    outer_puzzle: str
    inner_solution: str
    outer_solution: str
    amount: int
    tail_hash: str
    spent_height: int

    def __init__(
        self,
        coin_name: str,
        inner_puzzle: str,
        outer_puzzle: str,
        inner_solution: str,
        outer_solution: str,
        amount: int,
        tail_hash: str,
        spent_height: int = 0
    ):
        self.coin_name = coin_name
        self.inner_puzzle = inner_puzzle
        self.outer_puzzle = outer_puzzle
        self.inner_solution = inner_solution
        self.outer_solution = outer_solution
        self.amount = amount
        self.tail_hash = tail_hash
        self.spent_height = spent_height
