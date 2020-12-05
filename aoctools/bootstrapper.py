"""Tools for generating the AOC problem directory"""

from pathlib import Path

_MAKEFILE = """
.PHONY: lint
lint:
	pylint aoc tests
	mypy aoc tests

.PHONY: test
test:
	python3 -m unittest discover

""".lstrip()

_REQUIREMENTS_DEV = """
mypy
pylint
autopep8
""".lstrip()

_PROBLEM_INIT = """
from aoc.{0}.main import p_1, p_2
""".lstrip()

_PROBLEM_MAIN = """
from typing import IO

def p_1(input_file: IO,
        debug=False): # pylint: disable=unused-argument
    pass


def p_2(input_file: IO,
        debug=False): # pylint: disable=unused-argument
    pass
""".lstrip()

_PROBLEM_TEST = """
import aoc.d{0:02d}

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part({0}, False, aoc.d{0:02d}.p_1)

    def test_part_two(self):
        self.run_aoc_part({0}, False, aoc.d{0:02d}.p_2)
""".lstrip()

_TEST_RUNNER = """
import unittest
import os


class BaseTestCase(unittest.TestCase):
    @staticmethod
    def get_path(day):
        cur_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(cur_path, '../../', 'data', f"d{day:02d}",
                            'input.txt')

    def run_aoc_part(self, day, expected, method):
        with open(BaseTestCase.get_path(day), 'r',
                  encoding='utf8') as input_file:
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

    with open(root_dir.joinpath('requirements-dev.txt'),
              'w', encoding='utf8') as requirements_dev:
        requirements_dev.write(_REQUIREMENTS_DEV)

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
