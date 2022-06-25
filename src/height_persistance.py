from logging import getLogger, Logger
from typing import Union

from src.config import Config
from src.database import Database

log: Logger = getLogger("HeightPersistance")


class HeightPersistance:
    @staticmethod
    def init():
        cursor = Database.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata(
                name TEXT NOT NULL,
                value INTEGER NOT NULL,
                PRIMARY KEY (name)
            );
            """
        )
        value = HeightPersistance.get()
        if value is None:
            cursor.execute("INSERT INTO metadata(name, value) VALUES(?, ?)", ("height", Config.start_height))
        Database.connection.commit()
        cursor.close()

    @staticmethod
    def get() -> Union[int, None]:
        cursor = Database.connection.cursor()
        cursor.execute("SELECT value FROM metadata WHERE name = 'height'")
        output = cursor.fetchone()
        if output is None:
            return None
        value = output[0]
        Database.connection.commit()
        cursor.close()
        return value

    @staticmethod
    def set(height: int) -> None:
        cursor = Database.connection.cursor()
        cursor.execute("UPDATE metadata SET value = ? WHERE name = ?", (height, "height"))
        Database.connection.commit()
        cursor.close()
