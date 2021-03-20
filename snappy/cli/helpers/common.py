import os
from pathlib import Path
from typing import List

from snappy.cli.constants import APP_FILE


def get_app_dir() -> str:
    file = [str(path) for path in Path(".").rglob(APP_FILE)][0]
    return os.path.dirname(os.path.join(os.getcwd(), file))


def get_differences_in_letters(string1: str, string2: str) -> List[str]:
    return list(
        set(set(string1).difference(string2).union(set(string2).difference(string1)))
    )


def find_file(directory: str, file_name: str) -> List[str]:
    return [
        os.path.join(os.getcwd(), str(path))
        for path in Path(directory).rglob(file_name)
    ]
