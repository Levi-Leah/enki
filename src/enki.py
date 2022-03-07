#!/usr/bin/python3

import argparse
from pathlib import Path
import os
import sys
from subprocess import call
from enki_yaml_valiadtor import yaml_file_validation
from enki_files_valiadtor import validating_files_in_build_yml, validating_single_file, validating_directory

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

parser_a = subparsers.add_parser("validate", help="Perform validation.")
parser_a.add_argument("path", type=Path, help='Path to files.')

parser_b = subparsers.add_parser("generate", help="Generate build.yml from a template.")
parser_b.add_argument("path", type=Path, help='Path to files.')

p = parser.parse_args()


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

    if user_input.is_file():
        file_extension = Path(user_input).suffix
        if file_extension == '.yml':
            yaml_file_validation(user_input)
            validating_files_in_build_yml(user_input)

        elif file_extension == '.adoc':
            string = str(user_input)
            list = string.split()
            validating_single_file(list)
        else:
            print("ERROR: Unsupported file type.")
    elif user_input.is_dir():
        validating_directory(str(user_input) + '/')
    else:
        print("ERROR: Provided path doesn't exist; exiting...")