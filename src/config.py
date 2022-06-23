import os


class Config:
    start_height: int
    target_height: int

    def __init__(self):
        self.start_height = int(os.getenv("START_HEIGHT", "0"))
        self.target_height = int(os.getenv("TARGET_HEIGHT", "-1"))

        if self.start_height < 0:
            raise Exception("START_HEIGHT environment variable must be set to a number greater than 0")

        if self.target_height < 0:
            raise Exception("TARGET_HEIGHT environment variable must be set")

        if self.target_height < self.start_height:
            raise Exception(
                "TARGET_HEIGHT environment variable must be set to a value less than or equal to START_HEIGHT"
            )
