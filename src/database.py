import sqlite3

from src.config import Config


class Database:
    connection: sqlite3.Connection = sqlite3.connect(Config.database_path)
