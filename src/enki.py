#!/usr/bin/python3

import argparse
from pathlib import Path
import os
import sys
import time
import logging

from enki_files_validator import validating_files, lcheck_validate
import enki_checks


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

    # if args.command == 'validate':
    #     validate(user_input, args)
    adoc_files, unsupported_files = get_files(user_input)

    if unsupported_files:
        separator = "\n\t"
        logging.error(f'Not adoc file. The following files cannot be validated:\n\t{separator.join(unsupported_files)}\n')
        sys.exit(2)

    if adoc_files:
        start = time.time()

        if args.validate:
            validating_files(adoc_files, start)
        elif args.oneline:
            validating_files(adoc_files, start, output='oneline')
        elif args.gitlab:
            validating_files(adoc_files, start, output='gitlab')
        elif args.links:
            lcheck_validate(adoc_files)
    else:
        #TODO: get rid of possix path
        separator = "\n\t"
        logging.error(f'No adoc files detected. The following paths cannot be validated:\n\t{user_input}\n')
        sys.exit(2)


def cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
                        prog = 'enki',
                        description = 'Enki runs validation tests on Asciidoc source files')

    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-t', '--testcase', action="store_true",
                         help="show test cases")
    parser.add_argument('path', nargs='+', type=Path, help='path to files')
    group.add_argument('-v', '--validate', action="store_true",
                         help="perform validation")
    group.add_argument('-o', '--oneline', action="store_true",
                         help="print one validation error per line")
    group.add_argument('-g', '--gitlab', action="store_true",
                         help="print validation errors in xml format")
    group.add_argument('-l', '--links', action="store_true",
                         help="find broken links")

    if any(x in sys.argv for x in ['-t', '--testcase']):
        help(enki_checks)
        sys.exit(0)
    
    args = parser.parse_args()

    return args


def get_files(user_input: list[Path]):
    files = []
    unsupported_files = []

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

    return files, unsupported_files

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
