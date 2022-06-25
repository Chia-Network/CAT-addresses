from logging import getLogger, Logger
from typing import Union
from src.database import Database

log: Logger = getLogger("HeightPersistance")


class HeightPersistance:
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
