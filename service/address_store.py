import logging
from service.address_record import AddressRecord
from pathlib import Path


class AddressStore:
    file: Path
    log = logging.getLogger("AddressStore")

    def __init__(self, path: str):
        self.file = Path(path)
        self.file.touch(exist_ok=True)

    def add(self, address_record: AddressRecord):
        with open(self.file, "r+") as f:
            f.write("{}, {}, {}, {}, {}"
                    .format(
                        str(address_record.tail_hash),
                        str(address_record.inner_puzzle_hash),
                        str(address_record.outer_puzzle_hash),
                        str(address_record.inner_address),
                        str(address_record.outer_address)
                    )
                    )

        self.log.info("Added %s to AddressStore - %i records", address_record.inner_address)
