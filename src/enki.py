#!/usr/bin/python3

import argparse
from pathlib import Path
import os
import sys
import time
import logging

from enki_files_validator import validating_files


def main() -> None:
    args = cli_args()

    # Configure the level of logging output
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    for item in args.path:
        if not os.path.exists(item):
            logging.error(f"'{item}' doesn't exist in your repository.")
            args.path.remove(item)
            sys.exit(2)

    user_input = args.path

    if args.command == 'validate':
        validate(user_input, args)


def cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='enki')
    subparsers = parser.add_subparsers(dest='command')

    parser_a = subparsers.add_parser("validate", help="perform validation")
    group_a = parser_a.add_mutually_exclusive_group()
    group_a.add_argument("--oneline", action="store_true",
                         help="print one validation error per line")
    group_a.add_argument("--gitlab", action="store_true",
                         help="print validation errors in xml format")
    group_a.add_argument("--links", action="store_true",
                         help="perform links validation")
    parser_a.add_argument("path", nargs='+', type=Path, help='path to files')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    return args


def validate(user_input: list[Path], args: argparse.Namespace) -> None:
    """
    Validate files specified on the command line as user_input.
    """
    files = []
    unsupported_files = []

    start = time.time()

    for path in user_input:

        str_path = str(path)

        if path.is_dir():
            expanded_files = expand_file_paths(path)
            for file in expanded_files:
                if file not in files:
                    files.append(file)
        elif path.suffix == '.adoc':
            file = os.path.realpath(path)
            if file not in files:
                files.append(file)
        else:
            unsupported_files.append(str_path)

    if unsupported_files:
        separator = "\n\t"
        logging.error(f'Unsupported file format. The following files cannot be validated:\n\t{separator.join(unsupported_files)}\n')
        sys.exit(2)

    if files:
        if args.oneline:
            validating_files(files, start, output='oneline')
        elif args.gitlab:
            validating_files(files, start, output='gitlab')
        elif args.links:
            lcheck_path = os.path.dirname(
                os.path.abspath(__file__)) + '/lcheck.rb'

            master_adocs = []
            for file in files:
                if os.path.basename(file) == 'master.adoc':
                    master_adocs.append(file)

            if master_adocs:
                os.system(f'ruby {lcheck_path} {master_adocs}')
            else:
                logging.error('No master.adoc detected.')

        else:
            validating_files(files, start)


def expand_file_paths(path: Path) -> list[str]:
    """Expand filepaths."""
    expanded_files = []

    for dirpath, _dirnames, filenames in os.walk(path):
        for name in filenames:
            if not name.startswith('_') and name.endswith('.adoc') and name != 'README.adoc':
                file = os.path.realpath(os.path.join(dirpath, name))
                if file not in expanded_files:
                    expanded_files.append(file)

    return expanded_files


# Run the program
if __name__ == '__main__':
    main()
