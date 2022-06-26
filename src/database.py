import sqlite3
from typing import Union
from src.coin_record import CoinRecord
from src.config import Config


connection: sqlite3.Connection = sqlite3.connect(Config.database_path)


def get_height() -> Union[int, None]:
    cursor = connection.cursor()
    cursor.execute("SELECT value FROM metadata WHERE name = 'height'")
    output = cursor.fetchone()
    if output is None:
        return None
    value = output[0]
    connection.commit()
    cursor.close()
    return value


def set_height(height: int) -> None:
    cursor = connection.cursor()
    cursor.execute("UPDATE metadata SET value = ? WHERE name = ?", (height, "height"))
    connection.commit()
    cursor.close()


def persist_coin(coin_record: CoinRecord) -> None:
    cursor = connection.cursor()
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
            coin_record.coin_name,
            coin_record.inner_puzzle,
            coin_record.outer_puzzle,
            coin_record.inner_solution,
            coin_record.outer_solution,
            coin_record.amount,
            coin_record.tail_hash,
            coin_record.spent_height
        )
    )
    connection.commit()
    cursor.close()
