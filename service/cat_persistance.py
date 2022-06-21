from logging import getLogger, Logger
import os

cat_persistance_directory = os.getenv("CAT_PERSISTANCE_DIRECTORY", "/app")


class CatPersistance:
    log: Logger = getLogger("CatPersistance")

    def append(self, tail_hash: str, outer_puzzle_hash: str, hint: str, height: int):
        with open("{}/{}.dat".format(cat_persistance_directory, tail_hash), "a") as file:
            file.write("{}, {}, {}\n".format(outer_puzzle_hash, hint, height))
