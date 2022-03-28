#!/usr/bin/python3

import argparse
from pathlib import Path
import os
import sys
from subprocess import call
from enki_yaml_valiadtor import yaml_file_validation
from enki_files_valiadtor import validating_files_in_build_yml, validating_adoc_files, expand_file_paths
from pcbuild_emulator import main

parser = argparse.ArgumentParser(prog='enki')
subparsers = parser.add_subparsers(dest='command')

parser_a = subparsers.add_parser("validate", help="Perform validation.")
parser_a.add_argument("path", nargs='+', type=Path, help='Path to files.')

parser_b = subparsers.add_parser("generate", help="Generate build.yml from a template.")
parser_b.add_argument("path", nargs='+', type=Path, help='Path to files.')

# Andrew's code
parser_c = subparsers.add_parser('preview', help='Build a preview of content.')
# changed to path
parser_c.add_argument("path", nargs='+', type=Path, help='Path to files.')
parser_c.add_argument('--format', choices=['html','pdf'], help='The format of the files to output.')
parser_c.add_argument('--yml', type=Path, help='Path to the build.yml file.')
parser_c.add_argument('--lang', help='The language to build. For example, ja-JP.')
parser_d = subparsers.add_parser('clean', help='Clean the build directory.')


if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()


for item in args.path:
    if not os.path.exists(item):
        print(f"\nENKI ERROR: '{item}' doesn't exist in your repository.")
        #args.path.remove(item)
        #continue
        sys.exit(2)

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

elif args.command == "preview":
    # get output format
    output_format = args.format
    if not output_format:
        output_format = 'html'

    # get build.yml
    build_yml = args.yml
    # get language
    language = args.lang
    if not language:
        language = ''

    files = []
    unsupported_files = []

    # if user input is a build.yml:
    # validate the yml file
    # build preview of the content within the yml file
    for item in user_input:
        if os.path.basename(str(item)) == 'build.yml':
            yaml_file_validation(item)
            main(str(item), language, output_format)
        else:
            print('Can only validate build.yml. Support for other files coming soon.')

    if unsupported_files:
        separator = "\n\t"
        print('\nENKI ERROR: unsupported file format:')
        print('\t' + separator.join(unsupported_files))

    if files:
        print('files')
