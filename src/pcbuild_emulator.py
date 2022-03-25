#!/usr/bin/python3

import os
import shutil
from enki_files_valiadtor import SourcingFilesFromBuildYaml
from enki_yaml_valiadtor import ManipulatingBuildYaml
from enki_msg import ReportModified
import re
import subprocess
import sys
from queue import Queue
from threading import Thread


home_dir = os.path.expanduser('~')
pcmd_build_dir = home_dir + '/pcmd-build'
pcmd_images_dir = pcmd_build_dir + '/images'
pcmd_previews_dir = pcmd_build_dir + '/previews'

current_count = 0


class BuildWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            item, lang, attributes, output_format, current_count, content_count = self.queue.get()
            try:
                print('Building {0:d}/{1:d}: {2:s}'.format(current_count, content_count, item))
                asciidoctor_build(lang, attributes, item, output_format)
            finally:
                self.queue.task_done()


def build_files(files_to_build, lang, attributes, output_format):
    content_count = len(files_to_build)

    queue = Queue()

    for x in range(8):
        worker = BuildWorker(queue)
        worker.daemon = True
        worker.start()

    global current_count

    for item in files_to_build:
        current_count += 1
        queue.put((item, lang, attributes, output_format, current_count, content_count))

    queue.join()


def prepare_build_directory():
    paths = (pcmd_build_dir, pcmd_images_dir, pcmd_previews_dir)

    for item in paths:
        if not os.path.exists(item):
            os.makedirs(item, exist_ok=True)


def copy_resources(files):
    """Copy resources such as images and files to the build directory."""
    # Copy resources
    for file in files:
        if file.endswith(('jpg', 'jpeg', 'png', 'svg')):
            shutil.copy(file, pcmd_images_dir)


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


def get_adoc_files(all_file):
    adoc_files = []

    for item in all_file:
        if item.endswith('.adoc'):
            adoc_files.append(item)

    return adoc_files


def get_changed_files(all_adoc_files):
    changed_files = []

    for item in all_adoc_files:
        item_html = pcmd_previews_dir + '/' + os.path.splitext(os.path.basename(item))[0] + '.html'
        try:
            mod_time_adoc = os.path.getmtime(item)
            mod_time_html = os.path.getmtime(item_html)

            if mod_time_adoc > mod_time_html:
                changed_files.append(item)
        except OSError as e:
            continue

    return changed_files


def get_affected_files(changed_files, all_adoc_files):
    patterns = []
    affected_files = []

    for item in changed_files:
        basename = os.path.basename(item)
        pattern = r'include::.*{}\['.format(basename)
        patterns.append(pattern)

    for item in all_adoc_files:
        with open(item, 'r') as file:
            f = file.read()
            for p in patterns:
                if re.findall(p, f):
                    if item in affected_files:
                        continue
                    affected_files.append(item)

    return affected_files


def get_files_to_build(all_adoc_files):
    if len(os.listdir(pcmd_previews_dir)) == 0:
        files_to_build = all_adoc_files
    else:
        changed_files = get_changed_files(all_adoc_files)
        affected_files = get_affected_files(changed_files, all_adoc_files)
        files_to_build = [*changed_files, *affected_files]

    return files_to_build


def asciidoctor_build(lang, attributes, files_to_build, output_format):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    templates = script_dir + "/../templates/ "
    haml = script_dir + "/../haml/ "
    fonts = script_dir + "/../fonts/ "
    theme = script_dir + "/../templates/red-hat.yml "

    if output_format == 'pdf':
        command = ("asciidoctor-pdf -a pdf-themesdir=" + templates + "-a pdf-theme=" + theme + "-a pdf-fontsdir=" + fonts + lang + attributes + " -a imagesdir=images " + files_to_build + " -D pcmd-build/")
    else:
        command = ("asciidoctor -a toc! -a icons! " + lang + attributes + " -a imagesdir=images -E haml -T " + haml + files_to_build + " -D " + pcmd_previews_dir)

    process = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout

    print("\nAccess your previe files in `{}` directory.".format(pcmd_previews_dir))


def main(path_to_yaml, language, output_format):
    report_modified = ReportModified()

    manipulating_build_yaml = ManipulatingBuildYaml(path_to_yaml)
    loaded_yaml = manipulating_build_yaml.get_loaded_yaml()
    sourcing_files_from_build_yaml = SourcingFilesFromBuildYaml(loaded_yaml, path_to_yaml)

    files = sourcing_files_from_build_yaml.source_existing_content()
    adoc_files = get_adoc_files(files)

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

    files_to_build = get_files_to_build(adoc_files)
    if not files_to_build:
        print("\nNo changes detected since the last build.\nAccess your previe files in `{}` directory.".format(pcmd_previews_dir))
        sys.exit(0)

    resolved_attributes = get_resolved_attributes_dict(unique_attributes)
    attribute_string = combine_attributes_into_string(resolved_attributes)

    prepare_build_directory()
    copy_resources(adoc_files)

    build_files(files_to_build, language, attribute_string, output_format)
