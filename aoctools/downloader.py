"""Tools for downloading AOC problems"""

from pathlib import Path

import requests


def download(root_path: str, session_cookie: str, year: int, day: int):
    """
    Download an AOC problem file and save it in the appropriate directory

    Parameters
    ----------
    root_path
        The path of the root AOC problem directory
    session_cookie
        The AOC session cookie (obtained from the AOC website, when logged in)
        to use when requesting a problem input file
    year
        The AOC year, e.g., 2015, 2016, ...
    day:
        The AOC problem day, e.g., 1, 2, ... 25
    """

    resp = requests.get(f"https://adventofcode.com/{year}/day/{day}/"
                        "input", cookies={'session': session_cookie})

    if 200 <= resp.status_code < 300:
        output_dir = Path(root_path, 'data', f"d{day:02d}")
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_dir.joinpath('input.txt'), 'w',
                  encoding='utf8') as output_file:
            output_file.write(resp.text)

    return resp.status_code
