import logging
import sqlite3
from chia.types.blockchain_format.sized_bytes import bytes32


class PuzzlehashRecord:
    inner_puzzle_hash: bytes32
    tail_hash: bytes32

    def __init__(
        self,
        inner_puzzle_hash: bytes32,
        tail_hash: bytes32,
    ):
        self.inner_puzzle_hash = inner_puzzle_hash
        self.tail_hash = tail_hash


class PuzzlehashStore:
    """
    Stores puzzle hash records related to all CATs in a puzzlehash table.
    """

    connection: sqlite3.Connection
    log = logging.getLogger("PuzzlehashStore")

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def init(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS puzzle_hash(
                inner_puzzle_hash TEXT NOT NULL,
                tail_hash TEXT NOT NULL,
                PRIMARY KEY (inner_puzzle_hash, tail_hash)
            );
            """
        )
        self.connection.commit()
        cursor.close()

    """
    Persist to DB or throw error on failure. Do not proceed without retry if there is any error persisting data.
    """
    def persist(self, puzzle_hash_record: PuzzlehashRecord):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO puzzle_hash(inner_puzzle_hash, tail_hash) VALUES(?, ?)",
            (
                str(puzzle_hash_record.inner_puzzle_hash),
                str(puzzle_hash_record.tail_hash)
            )
        )
        self.connection.commit()
        cursor.close()
