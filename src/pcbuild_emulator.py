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
from enki_attribute_parser import get_attributes_string
from enki_checks import Regex


script_dir = os.path.dirname(os.path.realpath(__file__))
# Define directory names for pcmd-build
home_dir = os.path.expanduser('~')
pcmd_build_dir = os.path.join(home_dir, 'pcmd-build')
pcmd_images_dir = os.path.join(pcmd_build_dir, 'images')
pcmd_previews_dir = os.path.join(pcmd_build_dir, 'previews')


current_count = 0


def prepare_build_directory(output_format):
    """Creates directory structure for previews."""
    previews_subdir = os.path.join(pcmd_previews_dir, output_format)
    paths = (pcmd_build_dir, pcmd_images_dir, previews_subdir)

    for item in paths:
        if not os.path.exists(item):
            os.makedirs(item, exist_ok=True)


def copy_resources(files):
    """Copies images."""
    # I think I can just point with asciidoctor to images dir
    # by determining the common parent?
    for file in files:
        if file.endswith(('jpg', 'jpeg', 'png', 'svg')):
            shutil.copy(file, pcmd_images_dir)


def get_adoc_files(all_file):
    """Returns only adoc files."""
    adoc_files = []

    for item in all_file:
        if item.endswith('.adoc'):
            adoc_files.append(item)

    return adoc_files


class BuildWorker(Thread):
    """Fetches files that need to be built and passes them to asciidoctor build function."""
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            item, lang, attributes_string, output_format, current_count, content_count = self.queue.get()
            try:
                print('Building {0:d}/{1:d}: {2:s}'.format(current_count, content_count, item))
                asciidoctor_build(lang, attributes_string, item, output_format)
            finally:
                self.queue.task_done()


def build_files(files_to_build, lang, attributes_string, output_format):
    """Threads the queue."""
    content_count = len(files_to_build)

    queue = Queue()

    for x in range(8):
        worker = BuildWorker(queue)
        worker.daemon = True
        worker.start()

    global current_count

    for item in files_to_build:
        current_count += 1
        queue.put((item, lang, attributes_string, output_format, current_count, content_count))

    queue.join()


def get_changed_files(all_adoc_files, output_format):
    """Returnes a list of files that were modified after the last preview build."""
    changed_files = []
    unbuilt_files = []

    for item in all_adoc_files:
        directory_path = os.path.dirname(os.path.relpath(item, home_dir))
        previews_subdir = os.path.join(pcmd_previews_dir, output_format)
        filename_no_extension = os.path.splitext(os.path.basename(item))[0]

        file_to_build = os.path.join(previews_subdir, directory_path, filename_no_extension + '.' + output_format)

        try:
            mod_time_adoc = os.path.getmtime(item)
            mod_time_built_files = os.path.getmtime(file_to_build)

            if mod_time_adoc > mod_time_built_files:
                changed_files.append(item)
        except OSError as e:
            unbuilt_files.append(item)

    return changed_files, unbuilt_files


def get_all_includes(all_adoc_files):
    """Get all include statements from adoc files."""
    all_includes = {}

    for item in all_adoc_files:
        with open(item, 'r') as file:
            original = file.read()
            stripped = Regex.MULTI_LINE_COMMENT.sub('', original)
            stripped = Regex.SINGLE_LINE_COMMENT.sub('', stripped)

            pattern = r'(?<=include::)[\S]*(?=\[)'
            match = re.findall(pattern, stripped)

        all_includes[item] = match

    return all_includes


def get_parrent_files(modified_files, included_files):
    """Return parent files."""
    patterns = []
    affected_files = []

    for item in modified_files:
        basename = os.path.basename(item)
        patterns.append(basename)


    for key, value in included_files.items():
        present = [i for i in value if any(j in i for j in patterns)]
        if not present:
            continue
        if key in affected_files:
            continue

        affected_files.append(key)

    return affected_files


def get_all_parrent_files(modified_files, included_files):
    """Loops and returns all parent files."""
    if len(modified_files) == 0:
        # returns empty list to avoid NoneType error
        return []
    else:
        last_mod = get_parrent_files(modified_files, included_files)
        if last_mod:
            # must be list
            last_mod = [last_mod.pop()]
        return last_mod + get_parrent_files(last_mod, included_files)


def get_affected_files(all_adoc_files, output_format, changed_files):
    changed_files, unbuilt_files = get_changed_files(all_adoc_files, output_format)
    all_includes = get_all_includes(all_adoc_files)

    return get_all_parrent_files(changed_files, all_includes)


def get_files_to_build(all_adoc_files, output_format):
    """Determines what files need to be build."""
    previews_subdir = os.path.join(pcmd_previews_dir, output_format)

    if len(os.listdir(previews_subdir)) == 0:
        files_to_build = all_adoc_files
    else:
        changed_files, unbuilt_files = get_changed_files(all_adoc_files, output_format)
        affected_files = get_affected_files(all_adoc_files, output_format, changed_files)

        files_to_build = set(changed_files) | set(affected_files) | set(unbuilt_files)

    return files_to_build


def asciidoctor_build(lang, attributes_string, file_to_build, output_format):
    """Runs asciidoctor."""
    templates = script_dir + "/../templates/ "
    haml = script_dir + "/../haml/ "
    fonts = script_dir + "/../fonts/ "
    theme = script_dir + "/../templates/red-hat.yml "

    directory_path = os.path.dirname(os.path.relpath(file_to_build, home_dir))
    output_dir = os.path.join(pcmd_previews_dir, output_format, directory_path)

    if not output_dir:
        os.makedirs(output_dir, exist_ok=True)

    if output_format == 'pdf':
        command = ("asciidoctor-pdf -q -a pdf-themesdir=" + templates + "-a pdf-theme=" + theme + "-a pdf-fontsdir=" + fonts + lang + attributes_string + " -a imagesdir=images " + file_to_build + " -D " + output_dir)
    else:
        command = ("asciidoctor -q -a toc! -a icons! " + lang + attributes_string + " -a imagesdir=images -E haml -T " + haml + file_to_build + " -D " + output_dir)

    process = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout


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
        print(f"\nENKI ERROR: No files supplied. Check if files included in your build.yml exist in path.")
        sys.exit(2)

    if not unique_attributes:
        print(f"\nENKI ERROR: No attributes supplied. Check if files included in your build.yml exist in path.")
        sys.exit(2)

    if nonexistent_content.count != 0:
        nonexistent_content.print_report()

    attribute_string = get_attributes_string(unique_attributes)

    prepare_build_directory(output_format)
    copy_resources(files)

    files_to_build = get_files_to_build(adoc_files, output_format)
    if not files_to_build:
        print("\nNo changes detected since the last build.\nAccess your previe files in `{}` directory.".format(pcmd_previews_dir))
        sys.exit(0)

    build_files(files_to_build, language, attribute_string, output_format)
    print("\nAccess your previe files in `{}` directory.".format(pcmd_previews_dir))
