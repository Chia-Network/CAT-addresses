import logging
import sqlite3

from src.data.coin_record import CoinRecord


class CoinStore:
    """
    Stores coin records related to all CATs in a coin table.
    """

    connection: sqlite3.Connection
    log = logging.getLogger("CoinStore")

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def init(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS coin(
                coin_name TEXT NOT NULL,
                inner_puzzle_hash TEXT NOT NULL,
                outer_puzzle_hash TEXT NOT NULL,
                amount INTEGER NOT NULL,
                tail_hash TEXT NOT NULL,
                spent_height INTEGER DEFAULT 0,
                PRIMARY KEY (coin_name)
            );
            """
        )
        self.connection.commit()
        cursor.close()

    """
    Persist to DB or throw error on failure. Do not proceed without retry if there is any error persisting data.
    """
    def persist(self, coin_record: CoinRecord):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO coin(
                coin_name,
                inner_puzzle_hash,
                outer_puzzle_hash,
                amount,
                tail_hash,
                spent_height
            )
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            (
                coin_record.coin_name,
                coin_record.inner_puzzle_hash,
                coin_record.outer_puzzle_hash,
                coin_record.amount,
                coin_record.tail_hash,
                coin_record.spent_height
            )
        )
        self.connection.commit()
        cursor.close()
