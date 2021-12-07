"""Tools for generating the AOC problem directory"""

from pathlib import Path
from typing import Optional

import aoctools.common as aoc_common

_MAKEFILE = """
.PHONY: format
format:
	poetry run autopep8 -i -r aoc tests

.PHONY: lint
lint:
	poetry run flake8 aoc tests
	poetry run mypy aoc tests

.PHONY: test
test:
	poetry run pytest
""".lstrip()

_PYPROJECT = """
[tool.poetry]
name = "{name}"
version = "0.1.0"
description = "AOC {name}"
authors = ["AOC Author <email@example.com"]

[tool.poetry.dependencies]
python = "^3.7"
aoctools = {{ git = "https://github.com/klittlepage/aoctools.git" }}

[tool.poetry.dev-dependencies]
pytest = "^6.2.5"
black = "*"
autopep8 = "*"
flake8 = "*"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
""".lstrip()

_MYPY = """
[mypy]
check_untyped_defs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
disallow_untyped_decorators = True
disallow_any_unimported = True
warn_return_any = True
warn_unused_ignores = True
no_implicit_optional = True
show_error_codes = True
"""

_FLAKE8 = """
[flake8]
max-line-length = 88
extend-ignore = E203
""".lstrip()

_PROBLEM_INIT = """
from aoc.{0}.main import p_1, p_2  # noqa: F401
""".lstrip()

_PROBLEM_MAIN = """
from typing import Any, IO


def p_1(input_file: IO, debug: bool = False) -> Any:
    pass


def p_2(input_file: IO, debug: bool = False) -> Any:
    pass
""".lstrip()

_PROBLEM_TEST = """
import aoc.d{0:02d}

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self) -> None:
        self.run_aoc_part({0}, False, aoc.d{0:02d}.p_1)

    def test_part_two(self) -> None:
        self.run_aoc_part({0}, False, aoc.d{0:02d}.p_2)
""".lstrip()

_TEST_RUNNER = """
import unittest
import os

from typing import Any, Callable, TextIO


class BaseTestCase(unittest.TestCase):
    @staticmethod
    def get_path(day: int) -> str:
        cur_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(cur_path, "../../", "data", f"d{day:02d}", "input.txt")

    def run_aoc_part(
        self, day: int, expected: Any, method: Callable[[TextIO], Any]
    ) -> None:
        with open(BaseTestCase.get_path(day), "r", encoding="utf8") as input_file:
            self.assertEqual(expected, method(input_file))
""".lstrip()


def _touch_empty(path: str):
    with open(path, 'w', encoding='utf8') as out_file:
        out_file.write('')


def init(root_path: str, year: int):
    """
    Initializes an AOC project for the given year

    Parameters
    ----------
    root_path
        The path of the root AOC problem directory
    year:
         The AOC year, e.g., 2015, 2016, ...
    """

    root_dir = Path(root_path)
    root_dir.mkdir(exist_ok=False)

    with open(root_dir.joinpath('Makefile'), 'w', encoding='utf8') as makefile:
        makefile.write(_MAKEFILE)

    with open(root_dir.joinpath('pyproject.toml'), 'w', encoding='utf8') as py_project:
        py_project.write(_PYPROJECT.format(name=year))

    with open(root_dir.joinpath('mypy.ini'),
              'w', encoding='utf8') as mypy:
        mypy.write(_MYPY)

    with open(root_dir.joinpath('.flake8'),
              'w', encoding='utf8') as flake8:
        flake8.write(_FLAKE8)

    module_dir = root_dir.joinpath('aoc')
    module_dir.mkdir(parents=True)
    with open(module_dir.joinpath('__init__.py'), 'w',
              encoding='utf8') as project_init:
        project_init.write(f"AOC_YEAR = {year:04d}\n")

    data_dir = root_dir.joinpath('data')
    data_dir.mkdir(parents=True)

    test_dir = root_dir.joinpath('tests')
    test_dir.mkdir(parents=True)

    test_dir.joinpath('__init__.py').touch()

    test_module = test_dir.joinpath('aoc')
    test_module.mkdir(parents=True)
    test_module.joinpath('__init__.py').touch()

    with open(test_module.joinpath('test_base.py'), 'w',
              encoding='utf8') as base_test_file:
        base_test_file.write(_TEST_RUNNER)


def make_day(root_path: str, day: int):
    """
    Adds a day to the AOC project

    Parameters
    ----------
    root_path
        The path of the root AOC problem directory
    day:
        The AOC problem day, e.g., 1, 2, ... 25
    """

    day_str = f"d{day:02d}"
    root_dir = Path(root_path)
    module_dir = root_dir.joinpath('aoc', day_str)
    module_dir.mkdir(parents=True)

    with open(module_dir.joinpath('__init__.py'),
              'w', encoding='utf8') as init_file:
        init_file.write(_PROBLEM_INIT.format(day_str))

    with open(module_dir.joinpath('main.py'),
              'w', encoding='utf8') as main_file:
        main_file.write(_PROBLEM_MAIN)

    test_file_path = root_dir.joinpath('tests', 'aoc', f"test_{day_str}.py")

    with open(test_file_path, 'w', encoding='utf8') as test_file:
        test_file.write(_PROBLEM_TEST.format(day))


def make_example(root_path: str, day: int, part: int, expected: str,
                 index: Optional[int]):
    """
    Adds an example to a given day

    Parameters
    ----------
    root_path
        The path of the root AOC problem directory
    day:
        The AOC problem day, e.g., 1, 2, ... 25
    part:
        The problem part, i.e., 1 or 2
    expected:
        The expected value
    index:
        The index of the example; one higher than the previous example, if not
        given explicitly
    """

    if index is None:
        examples = aoc_common.get_examples_sorted(root_path, day)
        index = examples[-1][0]+1 if examples else 1

    example_path = Path(root_path).joinpath('data', f"d{day:02d}",
                                            f"example_{index:02d}.txt")

    with open(example_path, 'w', encoding='utf8') as example_file:
        example_file.write(f"part: {part}\n")
        example_file.write(f"expected: {expected}\n")
        example_file.write('\n')
