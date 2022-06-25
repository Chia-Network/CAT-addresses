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
    CREATE TABLE IF NOT EXISTS metadata(
        name TEXT NOT NULL,
        value INTEGER NOT NULL,
        PRIMARY KEY (name)
    );
    """
)
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

cursor.execute("INSERT INTO metadata(name, value) VALUES(?, ?)", ("height", Config.start_height))

connection.commit()
cursor.close()

log.info("Database setup complete")
