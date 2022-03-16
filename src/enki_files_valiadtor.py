#!/usr/bin/env/ python3
import os
import re
import subprocess
from pathlib import Path
import sys
from enki_yaml_valiadtor import ManipulatingBuildYaml
from enki_msg import Report, ReportModified
from enki_checks import Regex, nbsp_check, checks, nesting_in_modules_check, add_res_section_module_check, add_res_section_assembly_check


class SourcingFilesFromBuildYaml():
    def __init__(self, loaded_yaml, path_to_yaml):
        self.loaded_yaml = loaded_yaml
        self.path_to_yaml = path_to_yaml
        self.yaml_dir = os.path.dirname(path_to_yaml)

    def source_attributes(self):
        """Get attribute files specifiyed in build.yml."""
        attribute_values = []

        for variant in self.loaded_yaml['variants']:
            for item in variant['attributes']:
                attribute_values.append(item)

        unique_attributes, nonexistent_attributes = get_unique_and_nonexistent_files(attribute_values, self.yaml_dir)

        return unique_attributes, nonexistent_attributes

    def source_includes(self):
        included_values = source_files(self.loaded_yaml, 'included')
        unique_includes, nonexistent_includes = get_unique_and_nonexistent_files(included_values, self.yaml_dir)

        return unique_includes, nonexistent_includes

    def source_excludes(self):
        excluded_values = source_files(self.loaded_yaml, 'excluded')
        unique_excludes, nonexistent_excludes = get_unique_and_nonexistent_files(excluded_values, self.yaml_dir)

        return unique_excludes, nonexistent_excludes

    def source_nonexistent_content(self, report_modified):
        unique_includes, nonexistent_includes = self.source_includes()
        unique_excludes, nonexistent_excludes = self.source_excludes()
        unique_attributes, nonexistent_attributes = self.source_attributes()

        nonexistent_values = nonexistent_includes + nonexistent_excludes + nonexistent_attributes

        if nonexistent_values:
            for value in nonexistent_values:
                report_modified.create_report(f'The following values do not exist in your repository', value)

        return report_modified

    def source_existing_content(self):
        unique_includes, nonexistent_includes = self.source_includes()
        unique_excludes, nonexistent_excludes = self.source_excludes()

        content_list = [x for x in unique_includes if x not in unique_excludes]

        return content_list

    def sort_content(self):
        content_list = self.source_existing_content()
        attribute_files, prefix_assemblies, prefix_modules, undefined_content = sort_files(content_list)

        return attribute_files, prefix_assemblies, prefix_modules, undefined_content

    def validate_content(self, report_modified, report_original):
        unique_attributes, nonexistent_attributes = self.source_attributes()
        attribute_files, prefix_assemblies, prefix_modules, undefined_content = self.sort_content()

        all_attributes = [*attribute_files, *unique_attributes]
        all_files = [*all_attributes, *prefix_assemblies, *prefix_modules, *undefined_content]

        validation = validate(all_files, report_original, undefined_content, prefix_assemblies, prefix_modules, all_attributes)

        nonexistent_files = self.source_nonexistent_content(report_modified)

        if (nonexistent_files.count) or (validation.count) != 0:
            nonexistent_files.print_report()
            validation.print_report()


def source_files(loaded_yaml, var):
    sourced_files = []

    for yaml_dict in loaded_yaml['variants']:
        for subkey in yaml_dict['files']:
            if subkey != var:
                continue

            for item in yaml_dict['files'][var]:
                if item not in sourced_files:
                    sourced_files.append(item)

    return sourced_files


def expand_file_paths(value):
    """Expand filepaths."""
    command = ("find  " + value + " -type f 2>/dev/null")
    process = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout
    expanded_files = process.strip().decode('utf-8').split('\n')

    return expanded_files


def get_existent_nonexistent_content(values, yaml_dir):
    content_files = []
    nonexistent_values = []

    for value in values:
        path_to_value = os.path.join(yaml_dir, value)
        # deal with global patterns
        wildcards = re.compile(r'[*?\[\]]')
        if wildcards.search(value):
            expanded_items = expand_file_paths(path_to_value)
            if expanded_items:
                for expanded_item in expanded_items:
                    if expanded_item != '':
                        content_files.append(expanded_item)
                    else:
                        nonexistent_values.append(value)
            else:
                continue
        elif os.path.isfile(path_to_value):
            content_files.append(path_to_value)
        else:
            nonexistent_values.append(value)

    return content_files, nonexistent_values


def get_unique_files(files):
    """Get unique file list of content excluding attributes"""
    # get unique file list through realpath
    unique_files = []

    for file in files:
        real_path = os.path.realpath(file)
        if real_path not in unique_files:
            unique_files.append(real_path)

    return unique_files


def get_unique_and_nonexistent_files(values, yaml_dir):
    existing_files, nonexistent_files = get_existent_nonexistent_content(values, yaml_dir)
    unique_files = get_unique_files(existing_files)

    return unique_files, nonexistent_files


def sort_files(files):
    """Get a list of assemblies, modules, and unidentifiyed files."""
    attribute_files = []
    prefix_assemblies = []
    prefix_modules = []
    undefined_content = []

    for file in files:
        file_extension = Path(file).suffix
        if file_extension != '.adoc':
            continue

        file_name = os.path.basename(file)

        if re.search("/_", file):
            attribute_files.append(file)
        elif file_name.startswith('assembly'):
            prefix_assemblies.append(file)
        elif file_name.startswith(("proc_", "con_", "ref_", "proc-", "con-", "ref-")):
            prefix_modules.append(file)
        elif file_name.startswith(("snip_", "snip-")):
            continue
        else:
            undefined_content.append(file)

    return attribute_files, prefix_assemblies, prefix_modules, undefined_content


def validate(all_files, report, undefined_content, prefix_assemblies, prefix_modules, all_attributes):

    undetermined_file_type = []
    confused_files = []

    cwd = os.getcwd()

    for path in all_files:
        relative_path = os.path.relpath(path, cwd)
        with open(path, 'r') as file:
            original = file.read()
            stripped = Regex.MULTI_LINE_COMMENT.sub('', original)
            stripped = Regex.SINGLE_LINE_COMMENT.sub('', stripped)
            stripped = Regex.CODE_BLOCK_DASHES.sub('', stripped)
            stripped = Regex.CODE_BLOCK_TWO_DASHES.sub('', stripped)
            stripped = Regex.CODE_BLOCK_DOTS.sub('', stripped)
            stripped = Regex.INTERNAL_IFDEF.sub('', stripped)

            checks(report, stripped, original, relative_path)

            if path in undefined_content:
                if re.findall(Regex.MODULE_TYPE, stripped):
                    nesting_in_modules_check(report, stripped, relative_path)
                    add_res_section_module_check(report, stripped, relative_path)

                elif re.findall(Regex.ASSEMBLY_TYPE, stripped):
                    add_res_section_assembly_check(report, stripped, relative_path)

                elif re.findall(Regex.SNIPPET_TYPE, stripped):
                    continue
                else:
                    undetermined_file_type.append(relative_path)

            if path in prefix_assemblies:
                if re.findall(Regex.MODULE_TYPE, stripped):
                    confused_files.append(relative_path)
                    nesting_in_modules_check(report, stripped, relative_path)
                    add_res_section_module_check(report, stripped, relative_path)
                else:
                    add_res_section_assembly_check(report, stripped, relative_path)

            if path in prefix_modules:
                if re.findall(Regex.ASSEMBLY_TYPE, stripped):
                    confused_files.append(path)
                    add_res_section_assembly_check(report, stripped, relative_path)
                else:
                    nesting_in_modules_check(report, stripped, relative_path)
                    add_res_section_module_check(report, stripped, relative_path)

            if path in all_attributes:
                nbsp_check(report, stripped, relative_path)

    return report


def validating_files_in_build_yml(path_to_yaml):
    report_original = Report()
    report_modified = ReportModified()

    manipulating_build_yaml = ManipulatingBuildYaml(path_to_yaml)
    loaded_yaml = manipulating_build_yaml.get_loaded_yaml()
    sourcing_files_from_build_yaml = SourcingFilesFromBuildYaml(loaded_yaml, path_to_yaml)

    sourcing_files_from_build_yaml.validate_content(report_modified, report_original)


def validating_adoc_files(user_input):
    report_original = Report()

    attribute_files, prefix_assemblies, prefix_modules, undefined_content = sort_files(user_input)

    all_files = [*attribute_files, *prefix_assemblies, *prefix_modules, *undefined_content]

    file_validation = validate(all_files, report_original, undefined_content, prefix_assemblies, prefix_modules, attribute_files)

    if file_validation.count != 0:
        file_validation.print_report()
        sys.exit(2)
