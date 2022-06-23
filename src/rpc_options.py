import os
from pathlib import Path
import socket

from chia.util.config import load_config
from chia.util.ints import uint16


class RpcOptions:
    hostname: str = socket.gethostname()
    port: uint16 = uint16(8555)
    chia_root: Path = Path(os.path.expanduser(os.getenv("CHIA_ROOT", "~/.chia/mainnet"))).resolve()
    config = load_config(chia_root, "config.yaml")
