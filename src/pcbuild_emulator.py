#!/usr/bin/python3
import os
import shutil
from enki_files_valiadtor import SourcingFilesFromBuildYaml
from enki_yaml_valiadtor import ManipulatingBuildYaml
from enki_msg import ReportModified
import threading
import re
import subprocess
import sys

# Andrew's code
lock = threading.Lock()

def prepare_build_directory():
    """Removes any existing 'build' directory and creates the directory structure required."""

    # Remove build directory if it exists
    # renamed to pcmd-build bacause some repos have a build dir
    if os.path.exists('pcmd-build'):
        shutil.rmtree('pcmd-build')

    # Create a build directory
    os.makedirs('pcmd-build/images', exist_ok=True)
    os.makedirs('pcmd-build/files', exist_ok=True)


def copy_resources(files):
    """Copy resources such as images and files to the build directory."""
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Copy resources
    for file in files:
        if file.endswith(('jpg', 'jpeg', 'png', 'svg')):
            shutil.copy(file, 'pcmd-build/images/')
        else:
            shutil.copy(file, 'pcmd-build/files/')

    # Copy styling resources
    shutil.copytree(script_dir + '/resources', 'pcmd-build/resources')


def parse_attributes(attributes):
    """Read an attributes file and parse values into a key:value dictionary."""

    final_attributes = {}

    for line in attributes:
        line = re.sub('{nbsp}', '&#160;', line)
        if re.match(r'^:\S+:.*', line):
            attribute_name = line.split(":")[1].strip()
            attribute_value = line.split(":")[2].strip()
            final_attributes[attribute_name] = attribute_value

    return final_attributes


def resolve_attributes(text, dictionary):
    pattern = re.compile('\{([^}]+)\}')

    while True:
        attributes = pattern.findall(text)

        if not any(key in dictionary for key in attributes):
            return text

        for attribute in attributes:
            if attribute in dictionary:
                text = text.replace(f'{{{attribute}}}', dictionary[attribute])


def resolve_dictionary(dictionary):
    result = {}

    for key, value in dictionary.items():
        result[key] = resolve_attributes(value, dictionary)

    return result


def get_resolved_attributes_dict(attribute_files):
    for item in attribute_files:
        with open(item, 'r') as file:
            parsed_attributes = parse_attributes(file)
            resolved_attributes = resolve_dictionary(parsed_attributes)

    return resolved_attributes


def combine_attributes_into_string(resolved_attributes_dict):
    attribute_string = ''

    for key, value in resolved_attributes_dict.items():
        attribute_substring = "-a " + key + "=" + "'" + value + "'@ "
        attribute_string+=str(attribute_substring)

    return attribute_string


def asciidoctor_build_html(lang, attributes, all_files):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    templates = script_dir + "/../templates/ "
    haml =  script_dir + "/../haml/ "
    fonts = script_dir + "/../fonts/ "

    command = ("asciidoctor -a toc! -a icons! " + lang + attributes + " -a imagesdir=images -E haml -T " + haml + all_files + " -D pcmd-build/")
    process = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout


def asciidoctor_build_pdf(lang, attributes, all_files):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    templates = script_dir + "/../templates/ "
    haml =  script_dir + "/../haml/ "
    fonts = script_dir + "/../fonts/ "
    theme = script_dir + "/../templates/red-hat.yml "

    command = ("asciidoctor-pdf -a pdf-themesdir=" + templates + "-a pdf-theme=" + theme + "-a pdf-fontsdir=" + fonts + lang + attributes + " -a imagesdir=images " + all_files + " -D pcmd-build/")
    process = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout


def build_files(all_files, lang, attributes, output_format):
    for item in all_files:
        print('Building {}'.format(item))
        if item.endswith('.adoc'):
            if output_format == 'pdf':
                asciidoctor_build_pdf(lang, attributes, item)
            else:
                asciidoctor_build_html(lang, attributes, item)


def main(path_to_yaml, language, output_format):
    report_modified = ReportModified()

    manipulating_build_yaml = ManipulatingBuildYaml(path_to_yaml)
    loaded_yaml = manipulating_build_yaml.get_loaded_yaml()
    sourcing_files_from_build_yaml = SourcingFilesFromBuildYaml(loaded_yaml, path_to_yaml)

    files = sourcing_files_from_build_yaml.source_existing_content()

    # pull attribute files
    unique_attributes, nonexistent_attributes = sourcing_files_from_build_yaml.source_attributes()

    nonexistent_content = sourcing_files_from_build_yaml.source_nonexistent_content(report_modified)

    if not files:
        print(f"\nENKI ERROR: No files suppliyed. Check if files included in your build.yml exist in path.")
        sys.exit(2)

    if not unique_attributes:
        print(f"\nENKI ERROR: No attributes suppliyed. Check if files included in your build.yml exist in path.")
        sys.exit(2)

    if nonexistent_content.count != 0:
        nonexistent_content.print_report()

    resolved_attributes = get_resolved_attributes_dict(unique_attributes)
    attribute_string = combine_attributes_into_string(resolved_attributes)

    prepare_build_directory()
    copy_resources(files)

    build_files(files, language, attribute_string, output_format)
