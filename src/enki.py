#!/usr/bin/python3

import argparse
from pathlib import Path
import os
import sys
from subprocess import call
from enki_yaml_valiadtor import yaml_file_validation
from enki_files_valiadtor import validating_files_in_build_yml, validating_adoc_files

parser = argparse.ArgumentParser(prog='enki')
subparsers = parser.add_subparsers(dest='command')

parser_a = subparsers.add_parser("validate", help="Perform validation.")
parser_a.add_argument("path", nargs='*', type=Path, help='Path to files.')

parser_b = subparsers.add_parser("generate", help="Generate build.yml from a template.")
parser_b.add_argument("path", nargs='*', type=Path, help='Path to files.')

p = parser.parse_args()


for item in p.path:
    if not os.path.exists(item):
        print("ERROR: Provided path doesn't exist; exiting...")
        sys.exit(2)

user_input = p.path


if p.command == 'generate':

    if user_input.is_dir():
        path = str(user_input)
        path_to_script = os.path.dirname(os.path.realpath(__file__))
        call("bash " + path_to_script + "/buildyml-generator.sh " + path, shell=True)
        sys.exit(0)
    else:
        print("ERROR: Provided path is not a directory.")
elif p.command == 'validate':

    item_count = len(user_input)

    for item in user_input:
        file_extension = Path(item).suffix
        if file_extension == '.yml':
            print(f"\nINFO: Validating {item}")
            yaml_file_validation(item)
            validating_files_in_build_yml(item)

        else:
            validating_adoc_files(user_input, file_extension)
