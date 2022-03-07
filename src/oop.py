#!/usr/bin/env/ python3

import subprocess
import os
from enki_yaml_valiadtor import ManipulatingBuildYaml
from enki_msg import Report
import sys
from pathlib import Path
from enki_checks import Regex, icons_check, toc_check, nbsp_check, checks, nesting_in_modules_check, add_res_section_module_check, add_res_section_assembly_check
import re


class ReportModified(Report):
    def print_report(self):
        """Print report."""
        separator = "\n\t"

        for category, files in self.report.items():
            print("\nERROR: {}:".format(category))
            print('\t' + separator.join(files))


class SourcingFilesFromBuildYaml():
    def __init__(self, loaded_yaml, path_to_yaml):
        self.loaded_yaml = loaded_yaml
        self.path_to_yaml = os.path.dirname(path_to_yaml)

    def source_attribute_files(self):
        """Get attribute files specifiyed in build.yml."""
        attribute_files = []

        for variant in self.loaded_yaml['variants']:
            for item in variant['attributes']:
                attribute_files.append(item)

        existing_attributes, nonexistent_attributes = sort_files_into_existing_nonexistent(attribute_files, self.path_to_yaml)

        unique_attributes = get_realpath(existing_attributes)

        return unique_attributes, nonexistent_attributes

    def source_other_file(self, var):
        sourced_files = []

        for yaml_dict in self.loaded_yaml['variants']:
            for subkey in yaml_dict['files']:
                if subkey != var:
                    continue

                for item in yaml_dict['files'][var]:
                    if item not in sourced_files:
                        sourced_files.append(item)

        return sourced_files

    def source_includes(self):
        included_values = self.source_other_file('included')
        existent_includes, nonexistent_includes = sort_files_into_existing_nonexistent(included_values, self.path_to_yaml)

        unique_includes = get_realpath(existent_includes)

        return unique_includes, nonexistent_includes

    def source_excludes(self):
        excluded_values = self.source_other_file('excluded')
        existing_excludes, nonexistent_excludes = sort_files_into_existing_nonexistent(excluded_values, self.path_to_yaml)

        unique_excludes = get_realpath(existing_excludes)

        return unique_excludes, nonexistent_excludes

    def source_nonexistent_values(self):
        unique_includes, nonexistent_includes = self.source_includes()
        existing_excludes, nonexistent_excludes = self.source_excludes()
        existing_attributes, nonexistent_attributes = self.source_attribute_files()

        nonexistent_files = nonexistent_includes + nonexistent_excludes + nonexistent_attributes

        return nonexistent_files

    def attribute_naming_errors(self):
        wrong_name_atrributes = []

        unique_attributes, nonexistent_attributes = self.source_attribute_files()

        for item in unique_attributes:
            file_name = os.path.basename(item)
            file_path = os.path.basename(item)

            if file_path.startswith("_"):
                continue
            elif "/_" in file_path:
                continue
            elif file_name.startswith("_"):
                continue
            else:
                wrong_name_atrributes.append(item)

        return wrong_name_atrributes

    def removing_excludes_from_includes(self):
        unique_includes, nonexistent_includes = self.source_includes()
        unique_excludes, nonexistent_excludes = self.source_excludes()

        content_list = [x for x in unique_includes if x not in unique_excludes]

        return content_list

    def sort_content(self):
        content_list = self.removing_excludes_from_includes()
        attribute_files, prefix_assemblies, prefix_modules, undefined_content = sort_prefix_files(content_list)

        return attribute_files, prefix_assemblies, prefix_modules, undefined_content

    def file_validation(self):
        """Validate all files."""
        report = Report()

        attribute_files, prefix_assemblies, prefix_modules, undefined_content = self.sort_content()
        unique_attributes, nonexistent_attributes = self.source_attribute_files()

        all_attributes = [*attribute_files, *unique_attributes]
        all_files = [*attribute_files, *prefix_assemblies, *prefix_modules, *undefined_content]

        undetermined_file_type = []
        confused_files = []

        for path in all_files:
            relative_path = path.replace(self.path_to_yaml + '/', '')
            with open(path, 'r') as file:
                original = file.read()
                stripped = Regex.MULTI_LINE_COMMENT.sub('', original)
                stripped = Regex.SINGLE_LINE_COMMENT.sub('', stripped)
                stripped = Regex.CODE_BLOCK_DASHES.sub('', stripped)
                stripped = Regex.CODE_BLOCK_TWO_DASHES.sub('', stripped)
                stripped = Regex.CODE_BLOCK_DOTS.sub('', stripped)
                stripped = Regex.INTERNAL_IFDEF.sub('', stripped)

                checks(report, stripped, original, relative_path)
                icons_check(report, stripped, relative_path)
                toc_check(report, stripped, relative_path)

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

        reporting_relative_path(undetermined_file_type, self.path_to_yaml, report, 'files can not be checked. no filename prefix or content type')

        reporting_relative_path(confused_files, self.path_to_yaml, report, 'mismatched filename prefix and content type tag')

        return report

    def generating_report(self, report):
        wrong_name_atrributes = self.attribute_naming_errors()
        nonexistent_files = self.source_nonexistent_values()

        reporting_relative_path(nonexistent_files, self.path_to_yaml, report, 'The following values do not exist in your repository')

        reporting_relative_path(wrong_name_atrributes, self.path_to_yaml, report, 'The following attribute files do not adhere to naming conventions')

        return report


def reporting_relative_path(files, path, report, msg):
    if files:
        for file in files:
            relative_path = file.replace(path + '/', '')
            report.create_report(f'{msg}', relative_path)


def expand_file_paths(value):
    """Expand filepaths."""
    command = ("find  " + value + " -type f 2>/dev/null")
    process = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout
    expanded_files = process.strip().decode('utf-8').split('\n')

    return expanded_files


def sort_files_into_existing_nonexistent(sourced_files, path):
    content_list = []
    nonexistent_value = []

    for value in sourced_files:
        item = path + '/' + value
        expanded_value = expand_file_paths(item)
        if not expanded_value:
            continue
        if '' in expanded_value:
            nonexistent_value.append(item)
            continue
        for file_path in expanded_value:
            if file_path not in content_list:
                content_list.append(file_path)

    return content_list, nonexistent_value


def get_realpath(files):
    """Get unique file list of content excluding attributes"""
    # get unique file list through realpath
    unique_files = []

    for file in files:
        real_path = os.path.realpath(file)
        if real_path not in unique_files:
            unique_files.append(real_path)

    return unique_files


def sort_prefix_files(files):
    """Get a list of assemblies, modulesa, and unidentifiyed files."""
    attribute_files = []
    prefix_assemblies = []
    prefix_modules = []
    undefined_content = []

    for file in files:
        file_extension = Path(file).suffix
        if file_extension != '.adoc':
            continue

        file_name = os.path.basename(file)
        file_path = os.path.basename(file)

        if file_path.startswith("_"):
            attribute_files.append(file)
        elif "/_" in file_path:
            attribute_files.append(file)
        elif file_name.startswith("_"):
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


def validating_files_in_build_yml(path_to_yaml):
    report = ReportModified()

    manipulating_yaml = ManipulatingBuildYaml(path_to_yaml)
    loaded_yaml = manipulating_yaml.get_loaded_yaml()
    sourcing_files = SourcingFilesFromBuildYaml(loaded_yaml, path_to_yaml)

    generating_report = sourcing_files.generating_report(report)
    file_validation = sourcing_files.file_validation()

    if generating_report.count != 0:
        generating_report.print_report()

    if file_validation.count != 0:
        file_validation.print_report()
