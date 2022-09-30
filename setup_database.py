import logging
import sys
from src.config import Config
from src.database import connection

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

log = logging.getLogger('setup_database')

log.info("Setting up database")

cursor = connection.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS coin_spend(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin_name TEXT NOT NULL,
        inner_puzzle TEXT NOT NULL,
        outer_puzzle TEXT NOT NULL,
        inner_solution TEXT NOT NULL,
        outer_solution TEXT NOT NULL,
        amount INTEGER NOT NULL,
        tail_hash TEXT NOT NULL,
        spent_height INTEGER DEFAULT 0
    );
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS coin_create(
        coin_name TEXT NOT NULL,
        inner_puzzle_hash TEXT NOT NULL,
        outer_puzzle_hash TEXT NOT NULL,
        amount INTEGER NOT NULL,
        tail_hash TEXT NOT NULL,
        created_height INTEGER DEFAULT 0,
        PRIMARY KEY (coin_name)
    );
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS tail(
        hash TEXT NOT NULL,
        type TEXT NOT NULL,
        PRIMARY KEY (hash)
    );
    """
)

connection.commit()
cursor.close()

log.info("Database setup complete")
