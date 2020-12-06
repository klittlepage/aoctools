"""aoctools main"""

import argparse
import importlib
import os
import sys

from dotenv import load_dotenv, find_dotenv

import aoctools.bootstrapper as bootstrapper
import aoctools.downloader as downloader
import aoctools.runner as runner

sys.path.append(os.getcwd())
load_dotenv(find_dotenv(usecwd=True))


def _valid_year(arg):
    year = int(arg)

    if year >= 2015:
        return year

    raise ValueError


def _valid_day(arg):
    day = int(arg)
    if 1 <= day <= 31:
        return day

    raise ValueError


def _build_init(subparsers):
    def _exec_init(args):
        bootstrapper.init(args.root_path, args.year)

    init_cmd = subparsers.add_parser('init',
                                     help='initialize a new aoc root directory')
    init_cmd.add_argument('root_path', help='the root project directory')
    init_cmd.add_argument('year', type=_valid_year)
    init_cmd.set_defaults(func=_exec_init)


def _build_init_day(subparsers):
    def _exec_init_day(args):
        if not args.skip_bootstrap:
            bootstrapper.make_day(args.root_path, args.day)

        if not args.skip_download:
            if args.year:
                year = args.year
            else:
                try:
                    sys.path.append(args.root_path)
                    aoc_module = importlib.import_module('aoc')
                    year = getattr(aoc_module, 'AOC_YEAR')
                except:  # pylint: disable=bare-except
                    print('the root directory is not a valid AOC project')
                    sys.exit(1)

            result = downloader.download(args.root_path, args.session_cookie,
                                         year, args.day)

            if not 200 <= result <= 300:
                print(f"input file download failed with status {result}")
                sys.exit(1)

    init_cmd = subparsers.add_parser('init_day',
                                     help='initialize a new day')
    init_cmd.add_argument('--root-path', nargs='?', default=os.getcwd(),
                          help='the root project directory; defaults to the '
                               'current working directory')
    init_cmd.add_argument('--year', type=_valid_year,
                          help='aoc challenge year; defaults to the project '
                               'year')
    init_cmd.add_argument('--skip-bootstrap',
                          help="don't generate python boilerplate",
                          default=False,
                          action='store_true')
    init_cmd.add_argument('--skip-download',
                          help="don't download the challenge input data",
                          default=False,
                          action='store_true')
    init_cmd.add_argument('--session-cookie', type=str,
                          default=os.environ.get('AOC_SESSION_COOKIE'),
                          help='an AOC login session cookie; defaults to the '
                               'environment variable AOC_SESSION_COOKIE')

    init_cmd.add_argument('day', type=_valid_day,
                          help='aoc challenge day')
    init_cmd.set_defaults(func=_exec_init_day)


def _build_init_example(subparsers):
    def _exec_init_example(args):
        bootstrapper.make_example(args.root_path,
                                  args.day,
                                  args.part,
                                  args.expected,
                                  args.example_number)
    init_cmd = subparsers.add_parser('init_example',
                                     help='initialize a new example')
    init_cmd.add_argument('--root-path', nargs='?', default=os.getcwd(),
                          help='the root project directory; defaults to the '
                               'current working directory')
    init_cmd.add_argument('day', type=_valid_day,
                          help='aoc challenge day')
    init_cmd.add_argument('part', type=int, choices=[1, 2],
                          help='the challenge part for the example')
    init_cmd.add_argument('expected', type=str,
                          help='the expected example value')
    init_cmd.add_argument('example_number', type=int, nargs='?', default=None,
                          help='aoc challenge day; optional (autoincrement)')
    init_cmd.set_defaults(func=_exec_init_example)


def _build_runner(subparsers):
    def _run(args):
        sys.path.append(args.root_path)
        runner.run(args.root_path, args.day, args.part, args.debug)

    run_cmd = subparsers.add_parser('run',
                                    help='runs a challenge problem')
    run_cmd.add_argument('--root-path', nargs='?', default=os.getcwd(),
                         help='the root project directory')
    run_cmd.add_argument('--debug', help='print debug info', default=False,
                         action='store_true')

    run_cmd.add_argument('day', type=_valid_day, help='aoc challenge day')
    run_cmd.add_argument('part', type=int, choices=[1, 2],
                         help='the challenge part to run')
    run_cmd.set_defaults(func=_run)


def _build_example_runner(subparsers):
    def _run_example(args):
        sys.path.append(args.root_path)
        runner.run_example(args.root_path, args.day, args.debug,
                           args.example_number)

    run_cmd = subparsers.add_parser('run_examples',
                                    help='runs examples for a challenge '
                                         'problem')
    run_cmd.add_argument('--root-path', nargs='?', default=os.getcwd(),
                         help='the root project directory')
    run_cmd.add_argument('--debug', help='print debug info', default=False,
                         action='store_true')

    run_cmd.add_argument('day', type=_valid_day, help='aoc challenge day')
    run_cmd.add_argument('example_number', type=int, nargs='?', default=None,
                         help='the example to run; defaults to all examples')
    run_cmd.set_defaults(func=_run_example)


def main():
    """
    The main entrypoint of the CLI
    """

    parser = argparse.ArgumentParser(prog='aoctools')

    def _print_help(_args):
        parser.print_help()

    parser = argparse.ArgumentParser(prog='aoctools')
    parser.set_defaults(func=_print_help)
    subparsers = parser.add_subparsers(help='Advent of Code (AOC) cli command')

    _build_init(subparsers)
    _build_init_day(subparsers)
    _build_init_example(subparsers)
    _build_runner(subparsers)
    _build_example_runner(subparsers)

    args = parser.parse_args()
    args.func(args)
