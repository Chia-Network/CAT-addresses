import sqlite3


class Database:
    connection: sqlite3.Connection = sqlite3.connect('/root/.chia/mainnet/db/cat.db')
