#!/usr/bin/python3

import argparse
from pathlib import Path
import os
import sys
from subprocess import call
from enki_yaml_valiadtor import yaml_file_validation
from enki_files_valiadtor import validating_files_in_build_yml, validating_adoc_files, expand_file_paths

parser = argparse.ArgumentParser(prog='enki')
subparsers = parser.add_subparsers(dest='command')

parser_a = subparsers.add_parser("validate", help="Perform validation.")
parser_a.add_argument("path", nargs='+', type=Path, help='Path to files.')

parser_b = subparsers.add_parser("generate", help="Generate build.yml from a template.")
parser_b.add_argument("path", nargs='+', type=Path, help='Path to files.')

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()


for item in args.path:
    if not os.path.exists(item):
        print(f"\nENKI ERROR: '{item}' doesn't exist in your repository.")
        args.path.remove(item)
        continue

user_input = args.path


if args.command == 'generate':

    if user_input.is_dir():
        path = str(user_input)
        path_to_script = os.path.dirname(os.path.realpath(__file__))
        call("bash " + path_to_script + "/buildyml-generator.sh " + path, shell=True)
        sys.exit(0)
    else:
        print("\nENKI ERROR: Provided path is not a directory.")

elif args.command == 'validate':
    files = []
    unsupported_files = []

    for item in user_input:
        if os.path.isdir(item):
            expand_files = expand_file_paths(str(item) + '/')
            for file in expand_files:
                files.append(file)
        elif str(item).endswith('.adoc'):
            files.append(str(item))
        elif os.path.basename(str(item)) == 'build.yml':
            yaml_file_validation(item)
            validating_files_in_build_yml(item)
        else:
            unsupported_files.append(str(item))

    if unsupported_files:
        separator = "\n\t"
        print('\nENKI ERROR: unsupported file format. The following files were not validated:')
        print('\t' + separator.join(unsupported_files))

    if files:
        validating_adoc_files(files)
