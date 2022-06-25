from logging import getLogger, Logger
import sqlite3
from typing import Union

from src.config import Config


class HeightPersistance:
    connection: sqlite3.Connection
    log: Logger = getLogger("HeightPersistance")

    def __init__(self, config: Config, connection: sqlite3.Connection):
        self.config = config
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
            cursor.execute("INSERT INTO metadata(name, value) VALUES(?, ?)", ("height", self.config.start_height))
        self.connection.commit()
        cursor.close()

    def get(self) -> Union[int, None]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT value FROM metadata WHERE name = 'height'")
        output = cursor.fetchone()
        if output is None:
            return None
        value = output[0]
        self.connection.commit()
        cursor.close()
        return value

    def set(self, height: int) -> None:
        cursor = self.connection.cursor()
        cursor.execute("UPDATE metadata SET value = ? WHERE name = ?", (height, "height"))
        self.connection.commit()
        cursor.close()
