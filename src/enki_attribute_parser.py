#!/usr/bin/python3

import re
import tempfile
import subprocess
from enki_checks import Regex
from bs4 import BeautifulSoup


def parse_attributes(attributes):
    """Parse attributes file and return the list of attribute names."""
    attribute_names = []
    comment = False

    for i in attributes:
        with open(i, 'r') as file:
            f = file.readlines()
            for line in f:
                if re.match(Regex.SINGLE_LINE_COMMENT, line):
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
    """Read an attributes file and parse values into a key:value dictionary."""

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

    return resolved_attributes_dict


def get_attributes_string(attributes):
    """Creates a string of attributes in `-a ATTRIBUTE=VALUE@` format to pass to asciidoctor when building files."""
    resolved_attributes_dict = get_resolved_attributes_dict(attributes)

    attribute_string = ''

    for key, value in resolved_attributes_dict.items():
        attribute_substring = "-a " + key + "=" + "'" + value + "'@ "
        attribute_string += str(attribute_substring)

    return attribute_string
