import os
from pathlib import Path

from src.height_persistance import HeightPersistance

test_path = "test.dat"


def test_creates_empty_file_on_init():
    file = Path(test_path)

    assert file.is_file() is False

    HeightPersistance(test_path)

    assert file.is_file() is True

    with open(file, "r") as f:
        assert f.readline() == ""

    os.remove(test_path)

    assert file.is_file() is False


def test_overwrites_file_content_with_passed_height():
    file = Path(test_path)

    height_persistance = HeightPersistance(test_path)

    height_persistance.set(29000000)

    result = height_persistance.get()

    assert result == 29000000

    with open(file, "r") as f:
        assert f.readline() == "29000000"

    os.remove(test_path)

    assert file.is_file() is False
