"""Common utilities"""

import re

from pathlib import Path
from typing import List, Tuple


def get_examples_sorted(root_path: str, day: int) -> List[Tuple[int, Path]]:
    """
    Gets all example files for a given day, in numeric sort order

    Parameters
    ----------
    root_path
        The path of the root AOC problem directory
    day:
        The AOC problem day, e.g., 1, 2, ... 25
    """
    example_regex = re.compile(r"example_([0-9]+).txt")

    def map_example(example):
        res = example_regex.match(example.name)
        if not res:
            raise Exception(f"invalid example {example}")
        return (int(res.groups()[0]), example)

    examples = Path(root_path).joinpath('data', f"d{day:02}").glob('example_*')
    return sorted([map_example(x) for x in examples])
