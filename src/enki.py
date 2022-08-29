#!/usr/bin/python3

import argparse
from pathlib import Path
import os
import sys
import time
from enki_files_validator import validating_files

start = time.time()

parser = argparse.ArgumentParser(prog='enki')
subparsers = parser.add_subparsers(dest='command')

parser_a = subparsers.add_parser("validate", help="perform validation")
group_a = parser_a.add_mutually_exclusive_group()
group_a.add_argument("--oneline", action="store_true", help="print one validation error per line")
group_a.add_argument("--gitlab", action="store_true", help="print validation errors in xml format")
group_a.add_argument("--links", action="store_true", help="perform links validation")
parser_a.add_argument("path", nargs='+', type=Path, help='path to files')

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()


for item in args.path:
    if not os.path.exists(item):
        print(f"\nERROR: '{item}' doesn't exist in your repository.")
        args.path.remove(item)
        sys.exit(2)

user_input = args.path


def expand_file_paths(item: Path) -> list[str]:
    """Expand filepaths."""
    expanded_files = []

    for dirpath, dirnames, filenames in os.walk(str(item) + '/'):
        for name in filenames:
            if not name.startswith('_') and name.endswith('.adoc') and name != 'README.adoc':
                file = os.path.realpath(os.path.join(dirpath, name))
                if file not in expanded_files:
                    expanded_files.append(file)

    return expanded_files


if args.command == 'validate':
    files = []
    unsupported_files = []

    for item in user_input:

        item = str(item)

        if os.path.isdir(item):
            expanded_files = expand_file_paths(item)
            for file in expanded_files:
                if file not in files:
                    files.append(file)
        elif item.endswith('.adoc'):
            file = os.path.realpath(item)
            if file not in files:
                files.append(file)
        else:
            unsupported_files.append(item)

    if unsupported_files:
        separator = "\n\t"
        print('\nERROR: Unsupported file format. The following files cannot be validated:')
        print('\t' + separator.join(unsupported_files))
        sys.exit(2)

    if files:
        if args.oneline:
            validating_files(files, output='oneline')
        elif args.gitlab:
            validating_files(files, output='gitlab', start_time=start)
        elif args.links:
            lcheck_path = os.path.dirname(os.path.abspath(__file__)) + '/lcheck.rb'

            master_adocs = []
            for file in files:
                if os.path.basename(file) == 'master.adoc':
                    master_adocs.append(file)
            os.system(f'ruby {lcheck_path} {master_adocs}')

        else:
            validating_files(files)
