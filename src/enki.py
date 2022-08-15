#!/usr/bin/python3

import argparse
from pathlib import Path
import os
import sys
from enki_files_valiadtor import validating_files

parser = argparse.ArgumentParser(prog='enki')
subparsers = parser.add_subparsers(dest='command')

parser_a = subparsers.add_parser("validate", help="Perform validation.")
parser_a.add_argument("path", nargs='+', type=Path, help='Path to files.')

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()


for item in args.path:
    if not os.path.exists(item):
        print(f"\nENKI ERROR: '{item}' doesn't exist in your repository.")
        args.path.remove(item)
        sys.exit(2)

user_input = args.path


def expand_file_paths(item):
    """Expand filepaths."""
    expanded_files = []

    for dirpath, dirnames, filenames in os.walk(str(item) + '/'):
        for name in filenames:
            if not name.startswith('_') and name.endswith('.adoc') and name != 'master.adoc' and name != 'README.adoc':
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
        print('\nENKI ERROR: unsupported file format. The following files cannot be validated:')
        print('\t' + separator.join(unsupported_files))
        sys.exit(2)

    if files:
        validating_files(files)
