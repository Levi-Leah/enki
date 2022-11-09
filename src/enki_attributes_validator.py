from pathlib import Path
import os
import sys
import re
import tempfile
import subprocess
from enki_regex import Regexes
from bs4 import BeautifulSoup
from enki_files_validator import sort_files
from enki_msg import Report

path = '/home/levi/rhel-8-docs/'

def get_attribute_files(path):
    attribute_files = []

    patterns = ["_global-rt-attributes.adoc", "_attributes.adoc"]
    # collect attribute files
    posix_paths = [p for p in Path(path).rglob('*') if p.name in patterns]

    for i in posix_paths:
        if path not in attribute_files:
            attribute_files.append(str(i))

    return attribute_files


def parse_attributes(attributes):
    """Parse attributes file and return the list of attribute names."""
    attribute_names = []
    comment = False

    for i in attributes:
        with open(i, 'r') as file:
            f = file.readlines()
            for line in f:
                if re.match(Regexes.SINGLE_LINE_COMMENT, line):
                    continue
                if line.startswith("////"):
                    comment = True if not comment else False
                    continue

                if comment:
                    continue

                if re.match(r'^:\S+:.*', line):
                    name = line.split(":")[1].strip()
                    if name in attribute_names:
                        continue
                    attribute_names.append(name)

    return attribute_names


def resolve_attributes(attributes, attribute_names):
    """Build temp attributes file with asciidoctor and parse values into a key:value dictionary."""

    temp_adoc = tempfile.NamedTemporaryFile(suffix='.adoc', mode='w+')
    temp_html = tempfile.NamedTemporaryFile(suffix='.html', mode='w+')

    try:
        for i in attributes:
            temp_adoc.write('include::' + i + '[]\n')

        for i in attribute_names:
            temp_adoc.write('{' + i +'}\n')

        temp_adoc.seek(0)

        asciidoctor_build_attributes(temp_adoc.name, temp_html.name)

        with open(temp_html.name, 'r') as file:

            soup = BeautifulSoup(file, 'html.parser')
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                attribute_values = paragraph.prettify(formatter='html').splitlines()[1:-1]

        attributes_dict = dict(zip(attribute_names, attribute_values))
        return attributes_dict

    finally:
        temp_adoc.close()
        temp_html.close()


def asciidoctor_build_attributes(temp_adoc, temp_html):
    """Build atributes."""
    command = ("asciidoctor -o " + temp_html + ' ' + temp_adoc)
    process = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout


def get_resolved_attributes_dict(attributes):
    """Return dict of resolved attributes."""
    attribute_names = parse_attributes(attributes)
    resolved_attributes_dict = resolve_attributes(attributes, attribute_names)
    # remove keys if value == empty string
    resolved_attributes_dict = {key: value for key, value in resolved_attributes_dict.items() if value}
    # keys to remove
    remove_keys = ['toclevels', 'imagesdir']
    for key in remove_keys:
        del resolved_attributes_dict[key]

    return resolved_attributes_dict


def mock_sort(user_input):
    unique_files = []
    for file in user_input:
        if file not in unique_files:
            unique_files.append(file)

    return unique_files


def validation(user_input):
    report = Report()

    attribute_files = get_attribute_files(path)
    all_files = mock_sort(user_input)
    dict = get_resolved_attributes_dict(attribute_files)

    cwd = os.getcwd()


    for item in all_files:
        relative_path = os.path.relpath(item, cwd)
        with open(item, 'r') as file:
            original = file.read()
            stripped = Regexes.MULTI_LINE_COMMENT.sub('', original)
            stripped = Regexes.SINGLE_LINE_COMMENT.sub('', stripped)
            stripped = Regexes.NBSP.sub(' ', stripped)

            for key, value in dict.items():
                value = value.replace("&nbsp;", " " )
                # if re.findall(re.escape(value), stripped):
                #     print(f"{key} not used in {relative_path}")
                if re.findall(re.escape(value), stripped):
                    report.create_report(
                    f"'{value}' value can be replaced with '{key}' attribute. Value", relative_path)


    return report


def validate_attributes(user_input, start_time):
    report = Report()

    attribute_validation = validation(user_input)
    if attribute_validation.count == 0:
        sys.exit(0)

    attribute_validation.print_report(start_time)
    sys.exit(2)
