import logging
import sqlite3


class PuzzlehashRecord:
    inner_puzzle_hash: str
    tail_hash: str

    def __init__(
        self,
        inner_puzzle_hash: str,
        tail_hash: str,
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
                processed INTEGER DEFAULT 0,
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
                puzzle_hash_record.inner_puzzle_hash,
                puzzle_hash_record.tail_hash
            )
        )
        self.connection.commit()
        cursor.close()

    def get(self, processed: int, count: int):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT inner_puzzle_hash, tail_hash FROM puzzle_hash WHERE processed = ? LIMIT ?",
            (processed, count)
        )
        output = cursor.fetchall()
        if output is None:
            return None
        self.connection.commit()
        cursor.close()
        return output

    def mark_processed(self, inner_puzzle_hash: str, tail_hash: str, processed: int):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE puzzle_hash SET processed = ? WHERE inner_puzzle_hash = ? AND tail_hash = ?",
            (
                processed,
                inner_puzzle_hash,
                tail_hash
            )
        )
        self.connection.commit()
        cursor.close()
