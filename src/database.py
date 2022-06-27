import sqlite3

from sqlite3 import Cursor
from src.coin_create_record import CoinCreateRecord
from src.coin_spend_record import CoinSpendRecord
from src.config import Config


connection: sqlite3.Connection = sqlite3.connect(Config.database_path)


def persist_coin_spend(cursor: Cursor, coin_spend_record: CoinSpendRecord) -> None:
    cursor.execute(
        """
        INSERT INTO coin_spend(
            coin_name,
            inner_puzzle,
            outer_puzzle,
            inner_solution,
            outer_solution,
            amount,
            tail_hash,
            spent_height
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            coin_spend_record.coin_name,
            coin_spend_record.inner_puzzle,
            coin_spend_record.outer_puzzle,
            coin_spend_record.inner_solution,
            coin_spend_record.outer_solution,
            coin_spend_record.amount,
            coin_spend_record.tail_hash,
            coin_spend_record.spent_height
        )
    )


def get_next_coin_spends(start_height: int, limit: int):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM coin_spend WHERE spent_height >= ? ORDER BY spent_height ASC LIMIT ?",
        (start_height, limit)
    )
    output = cursor.fetchall()
    if output is None:
        return None
    value = output
    connection.commit()
    cursor.close()
    return value


def persist_coin_create(cursor: Cursor, coin_create_record: CoinCreateRecord) -> None:
    cursor.execute(
        """
        INSERT INTO coin_create(
            coin_name,
            inner_puzzle_hash,
            outer_puzzle_hash,
            amount,
            tail_hash,
            created_height
        )
        VALUES(?, ?, ?, ?, ?, ?)
        """,
        (
            coin_create_record.coin_name,
            coin_create_record.inner_puzzle_hash,
            coin_create_record.outer_puzzle_hash,
            coin_create_record.amount,
            coin_create_record.tail_hash,
            coin_create_record.created_height
        )
    )
