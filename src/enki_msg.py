#!/usr/bin/env/ python3

from cerberus import errors
from cerberus.errors import BasicErrorHandler


class CustomErrorHandler(BasicErrorHandler):
    """Custom error messages."""

    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.REQUIRED_FIELD.code] = "key is missing"
    messages[errors.UNKNOWN_FIELD.code] = "unsupported key"
    messages[errors.NOT_NULLABLE.code] = "value can't be empty"


def printing_build_yml_error(msg, *files):
    """Print error message."""
    print('\nERROR: Your build.yml contains the following {}:\n'.format(msg))
    for file in files:
        if file:
            print('\t', file)


class Report():
    """Create and print report. thank u J."""

    def __init__(self):
        """Create placeholder for problem description."""
        self.report = {}
        self.count = 0

    def create_report(self, category, file_path):
        """Generate report."""
        self.count += 1
        if not category in self.report:
            self.report[category] = []
        self.report[category].append(file_path)

    def print_report(self):

        """Print report."""
        separator = "\n\t"

        for category, files in self.report.items():
            print("\nERROR: {} found in the following files:".format(category))
            print('\t' + separator.join(files))
