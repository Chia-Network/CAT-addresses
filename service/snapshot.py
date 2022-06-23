import logging
from pathlib import Path
from chia.types.blockchain_format.sized_bytes import bytes32


class SnapshotRecord:
    tail_hash: str
    inner_puzzle_hash: bytes32
    parent_coin_info: bytes32

    def __init__(
        self,
        tail_hash: str,
        inner_puzzle_hash: bytes32,
        parent_coin_info: bytes32,
    ):
        self.tail_hash = tail_hash
        self.inner_puzzle_hash = inner_puzzle_hash
        self.parent_coin_info = parent_coin_info

    def __str__(self):
        return "{}, {}, {}".format(
            str(self.tail_hash),
            str(self.inner_puzzle_hash),
            str(self.parent_coin_info),
        )


class Snapshot:
    file: Path
    log = logging.getLogger("Snapshot")

    def __init__(self, path: str):
        self.file = Path(path)
        self.file.touch(exist_ok=True)

    def add(self, snapshot_record: SnapshotRecord):
        with open(self.file, "r+") as f:
            f.write(snapshot_record.__str__())

        self.log.info("Added record to Snapshot: %s", snapshot_record)
