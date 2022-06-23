from logging import getLogger, Logger
import sqlite3
from typing import Union


class HeightPersistance:
    connection: sqlite3.Connection
    log: Logger = getLogger("HeightPersistance")

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def init(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata(
                name TEXT NOT NULL,
                value INTEGER NOT NULL,
                PRIMARY KEY (name)
            );
            """
        )
        value = self.get()
        if value is None:
            cursor.execute("INSERT INTO metadata(name, value) VALUES('height', 0)")
        self.connection.commit()
        cursor.close()

    def get(self) -> Union[int, None]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT value FROM metadata WHERE name = 'height'")
        output = cursor.fetchone()
        if output is None:
            return None
        value = output[0]
        self.log.info("value %i", value)
        self.connection.commit()
        cursor.close()
        return value

    def set(self, height: int) -> None:
        cursor = self.connection.cursor()
        cursor.execute("UPDATE metadata SET value = ? WHERE name = ?", (height, "height"))
        self.connection.commit()
        cursor.close()
