from logging import getLogger, Logger
from pathlib import Path


class HeightPersistance:
    file: Path
    log: Logger = getLogger("HeightPersistance")

    def __init__(self, path: str):
        self.file = Path(path)
        self.file.touch(exist_ok=True)

    def get(self) -> int:
        with open(self.file, "r") as f:
            line = f.readline()

            if line == "":
                return -1
            else:
                return int(line)

    def set(self, height) -> None:
        with open(self.file, "r+") as f:
            f.write(str(height))
            self.log.debug("Updated height to %i", height)
