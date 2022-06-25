import os
from pathlib import Path
import socket

from chia.util.config import load_config
from chia.util.ints import uint16

database_path = "/root/.chia/mainnet/db/cat.db"
start_height: int = int(os.getenv("START_HEIGHT", "0"))
target_height: int = int(os.getenv("TARGET_HEIGHT", "-1"))

if start_height < 0:
    raise Exception("START_HEIGHT environment variable must be set to a number greater than 0")

if target_height < 0:
    raise Exception("TARGET_HEIGHT environment variable must be set")

if target_height < start_height:
    raise Exception(
        "TARGET_HEIGHT environment variable must be set to a value less than or equal to START_HEIGHT"
    )


class RpcOptions:
    hostname: str = socket.gethostname()
    port: uint16 = uint16(8555)
    chia_root: Path = Path(os.path.expanduser(os.getenv("CHIA_ROOT", "~/.chia/mainnet"))).resolve()
    config = load_config(chia_root, "config.yaml")
    retry_count: int = 10


class Config:
    database_path: str = database_path
    start_height: int = start_height
    target_height: int = target_height
