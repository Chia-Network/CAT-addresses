import logging
from service.address_record import AddressRecord
from typing import Dict


class AddressStore:
    addresses: Dict[str, AddressRecord] = {}
    log = logging.getLogger("AddressStore")

    def add(self, address_record: AddressRecord):
        self.addresses[address_record.inner_address] = address_record

        self.log.info("Added %s to AddressStore - %i records", address_record.inner_address, self.addresses.__len__())
