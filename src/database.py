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


def get_initial_id(height: int):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id FROM coin_spend WHERE spent_height >= ? ORDER BY id ASC LIMIT 1",
        [height]
    )
    output = cursor.fetchone()
    if output is None:
        return 0
    value = output[0]
    connection.commit()
    cursor.close()
    return value


def get_next_coin_spends(id: int, limit: int):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM coin_spend WHERE id >= ? ORDER BY id ASC LIMIT ?",
        (id, limit)
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

def get_distinct_tail_hashes():
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT tail_hash FROM coin_create")
    output = cursor.fetchall()
    if output is None:
        return None
    value = output
    connection.commit()
    cursor.close()
    return value

def get_all_cat_balances(coins: bool):
    cursor = connection.cursor()
    if coins:
        cursor.execute(
            """
            SELECT coin_create.tail_hash, coin_create.coin_name, coin_create.inner_puzzle_hash, coin_create.amount FROM coin_create
            LEFT JOIN coin_spend ON coin_create.coin_name = coin_spend.coin_name
            WHERE coin_spend.coin_name IS null
            ORDER BY coin_create.created_height ASC
            """
        )
    else:
        # Must group by outer puzzle hash so amounts of inner puzzle hashes for different CATs don't get summed
        cursor.execute(
            """
            SELECT coin_create.tail_hash, coin_create.inner_puzzle_hash, SUM(coin_create.amount) FROM coin_create
            LEFT JOIN coin_spend ON coin_create.coin_name = coin_spend.coin_name
            WHERE coin_spend.coin_name IS null
            GROUP BY coin_create.outer_puzzle_hash
            ORDER BY MIN(coin_create.created_height) ASC
            """
        )
    output = cursor.fetchall()
    if output is None:
        return None
    value = output
    connection.commit()
    cursor.close()
    return value

def get_cat_balance(tail_hash: str, coins: bool):
    cursor = connection.cursor()
    if coins:
        cursor.execute(
            """
            SELECT coin_create.coin_name, coin_create.inner_puzzle_hash, coin_create.amount FROM coin_create
            LEFT JOIN coin_spend ON coin_create.coin_name = coin_spend.coin_name
            WHERE coin_create.tail_hash = ? AND coin_spend.coin_name IS null
            ORDER BY coin_create.created_height ASC
            """,
            [tail_hash]
        )
    else:
        cursor.execute(
            """
            SELECT coin_create.inner_puzzle_hash, sum(coin_create.amount) FROM coin_create
            LEFT JOIN coin_spend ON coin_create.coin_name = coin_spend.coin_name
            WHERE coin_create.tail_hash = ? AND coin_spend.coin_name IS null
            GROUP BY coin_create.inner_puzzle_hash
            ORDER BY MIN(coin_create.created_height) ASC
            """,
            [tail_hash]
        )
    output = cursor.fetchall()
    if output is None:
        return None
    value = output
    connection.commit()
    cursor.close()
    return value

def delete_coins_above(height: int):
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM coin_create WHERE created_height >= ?",
        [height]
    )
    cursor.execute(
        "DELETE FROM coin_spend WHERE spent_height >= ?",
        [height]
    )
    output = cursor.fetchall()
    if output is None:
        return None
    value = output
    connection.commit()
    cursor.close()
    return value
