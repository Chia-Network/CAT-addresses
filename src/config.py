import os

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


class Config:
    database_path: str = database_path
    start_height: int = start_height
    target_height: int = target_height
    rpc_retry_count: int = 10
