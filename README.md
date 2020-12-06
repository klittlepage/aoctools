# Automating your Advent of Code (AOC) Workflow: aoctools

## Introduction

`aoctools` is a command line interface (cli) that helps you automate
[Advent of Code (AOC)](https://adventofcode.com/) boilerplate, e.g., downloading
the day's problem input and writing python boilerplate.

## Workflow

### Step 0: Install

`pip3 install aoctools`

### Step 1: Initialize a project

```text
usage: aoctools init [-h] root_path year

positional arguments:
  root_path   the root project directory
  year
```

The `init` command will create an `aoctools` project at the path that you
specify.

### Step 2: Bootstrap the boilerplate for a new day

Make sure that you set an environment variable named `AOC_SESSION_COOKIE` to the
`session` cookie of your AOC login; in Chrome, you can obtain this cookie by
opening Developer Tools (`View > Developer > Developer Tools`), opening the
`Application` tab, and looking for the value that appears next to `session`.

As an alternative to setting this variable every time that you run the tool, `aoctools` supports `.env` files. You can create a `.env` file under your
project directory and run `aoctools` from said directory for an even more
ergonomic workflow. NB: `.env` files are loaded relative to the working
directory (where you run `aoctools` from) - *not* the project directory.

```text
usage: aoctools init_day [-h] [--root-path [ROOT_PATH]] [--year YEAR]
                         [--skip-bootstrap] [--skip-download]
                         [--session-cookie SESSION_COOKIE]
                         day

positional arguments:
  day                   aoc challenge day

optional arguments:
  -h, --help            show this help message and exit
  --root-path [ROOT_PATH]
                        the root project directory; defaults to the current
                        working directory
  --year YEAR           aoc challenge year; defaults to the project year
  --skip-bootstrap      don't generate python boilerplate
  --skip-download       don't download the challenge input data
  --session-cookie SESSION_COOKIE
                        an AOC login session cookie; defaults to the
                        environment variable AOC_SESSION_COOKIE
```

If you want to generate boilerplate for the challenge day without downloading
the day's input file, pass `--skip-download` to the `aoctools init_day`
command; you can download the day's input file later by passing
`--skip-bootstrap`; NB: the `init_day` command will not clobber existing
python files, so running it twice without passing `--skip-bootstrap` will fail.

### Step 3: Hack

Bootstrapping will generate a new module under the root `aoc` module named after
the freshly bootstrapped day. For example, running `aoctools init_day 1` will
create a file named `aoc/d01/main.py` containing:

```python
from typing import IO

def p_1(input_file: IO,
        debug=False): # pylint: disable=unused-argument
    pass


def p_2(input_file: IO,
        debug=False): # pylint: disable=unused-argument
    pass

```

Filling in `p_1` and `p_2` is where you come in; `aoctools` requires that
you return a (stringifiable) value if you want to use the built-in solution
printer and regression test framework, but there are no restrictions beyond
that.

Running your solution with `aoctools` will result in `p_1` or `p_2` being
called with a reference to the input file; semantically, it's the same as if
you had written:

```python
import aoc.d01

if __name__ == '__main__':
    with open('data/d01/input.txt', 'r', encoding='utf8') as input_file:
        aoc.d01.p_1(input_file, False) # or True
```

and run the file from the root of your project directory. The `debug` variable
is set via the `cli` and makes it easy to control print output:

```python
def p_1(input_file: IO, debug=False):
    v_1 = 1
    v_2 = 2

    if debug:
        print(f"v_1 + v_2 = {v_1} + {v_2} = {v_1 + v_2}")

    return v_1 + v_2
```

### Step 4: Test the example inputs

Create a new example by running the `init_example` command:

```text
usage: aoctools init_example [-h] [--root-path [ROOT_PATH]]
                             day {1,2} expected [example_number]

positional arguments:
  day                   aoc challenge day
  {1,2}                 the challenge part for the example
  expected              the expected example value
  example_number        aoc challenge day; optional (autoincrement)

optional arguments:
  -h, --help            show this help message and exit
  --root-path [ROOT_PATH]
                        the root project directory; defaults to the current
                        working directory
```

Examples are created in `data/day/example_n.txt`. By default, your examples will
be numbered sequentially; you can specify a number explicitly by passing an
additional `[example_number]` argument.

Example files take the form:

```text
part: 1
expected: 2

1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
```

The first line must be `part: (1|2)` corresponding to the part of the AOC
problem that the example pertains to. The second line must be an expected
value: `expected: (.+)`. The third line must be blank line. The rest of the file
should contain the example text.

Run examples via the `run_examples` command:

```text
usage: aoctools run_examples [-h] [--root-path [ROOT_PATH]] [--debug]
                             day [example_number]

positional arguments:
  day                   aoc challenge day
  example_number        the example to run; defaults to all examples

optional arguments:
  -h, --help            show this help message and exit
  --root-path [ROOT_PATH]
                        the root project directory
  --debug               print debug info
```

You must specify a day. You can optionally specify a specific example to run;
by default, all examples for the given day will run.

### Step 5: Run your solution

```text
usage: aoctools run [-h] [--root-path [ROOT_PATH]] [--debug] day {1,2}

positional arguments:
  day                   aoc challenge day
  {1,2}                 the challenge part to run

optional arguments:
  -h, --help            show this help message and exit
  --root-path [ROOT_PATH]
                        the root project directory
  --debug               print debug info
```

As an example, you can run Day 1, Pt 1 from your root project directory by
invoking:

```text
aoctools run 1 1

solution to day 1, part 1: xxxx
```

### Step 6 (Optional): Regression tests & Code Quality

Once you identify a solution you can populate the automatically generated
regression tests under `tests/aoc/test_d*`:

```python
import aoc.d01

from tests.aoc.test_base import BaseTestCase


class TestAll(BaseTestCase):
    def test_part_one(self):
        self.run_aoc_part(1, CHANGEME, aoc.d01.p_1)

    def test_part_two(self):
        self.run_aoc_part(1, CHANGEME, aoc.d01.p_2)
```

Running `make test` from the root project directory will run all regression
tests.

Similarly, running `make lint` will type lint and type check your code and
tests with both `pylint` and `mypy`.
