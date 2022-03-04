#!/usr/bin/python3

import argparse
from pathlib import Path
import os
import sys
from subprocess import call
from enki_yaml_valiadtor import yaml_validation
from enki_files_valiadtor import multi_file_validation, single_file_validation

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
        file_name = os.path.basename(user_input)
        file_path = os.path.dirname(user_input)
        if file_name == 'build.yml':
            file_name = os.path.basename(user_input)
            yaml_validation(user_input, file_path)
        else:

            file = str(user_input).split()
            single_file_validation(file)

    elif user_input.is_dir():
        multi_file_validation(user_input)
    else:
        print("ERROR: Provided path doesn't exist.")
