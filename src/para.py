#!/usr/bin/python3
import re
from enki_checks import *


def checks(line, line_number, report, file_path):

    if vanilla_xref_check(line):
        report.create_report('vanilla xrefs', file_path, line_number)

    if inline_anchor_check(line):
        report.create_report('in-line anchors', file_path, line_number)

    if experimental_tag_check(line):
        report.create_report('files contain UI macros but the :experimental: tag not', file_path, line_number)



class Report():
    """Create and print report. thank u J."""

    def __init__(self):
        """Create placeholder for problem description."""
        self.report = {}
        self.count = 0

    def create_report(self, category, file_path, line_numbers):
        """Generate report."""
        self.count += 1
        if not category in self.report:
            self.report[category] = {}
        if file_path not in self.report[category]:
            self.report[category][file_path] = []
        self.report[category][file_path].append(str(line_numbers))

    def print_report(self):
        """Print report."""

        for category, files in self.report.items():
            print("\nVALIDATION ERROR: {} found in the following files:".format(category))

            for file_path, line_numbers in files.items():
                print("\t" + file_path + ' [' +', '.join(line_numbers) + ']')


paths = ['/home/levi/rhel-8-docs/rhel-9/modules/upgrades-and-differences/ref_changes-to-desktop.adoc', '/home/levi/rhel-8-docs/rhel-8/modules/anaconda-customization/ref_addon-gui-advanced-features.adoc', '/home/levi/rhel-8-docs/rhel-8/assemblies/assembly_backing-up-an-xfs-file-system.adoc', '/home/levi/rhel-8-docs/rhel-8/assemblies/assembly_kickstart-commands-for-addons-supplied-with-the-rhel-installation-program.adoc']


def main(files):
    report = Report()

    for path in files:

        line_count = 0
        expects_empty = False
        comment = False

        with open(path, 'r') as file:

            for line in file:
                line_count += 1

                if re.match(Regex.SINGLE_LINE_COMMENT, line):
                    continue

                if line.startswith(("////", "----", "....", "--\n")):
                    comment = True if not comment else False
                    continue

                if comment:
                    continue


                checks(line, line_count, report, path)

                # Ignore conditions:
                if line.startswith(('ifeval', 'ifdef', 'ifndef', '//', 'endif')):
                    continue

                # Check if an empty line is expected:
                if expects_empty and line not in ('\n', '\r\n'):
                    # Report the problematic line:
                    report.create_report('no empty line after include statement', path, expects_empty)
                    #print(expects_empty, end='')

                # Mark that empty line is no longer expected:
                expects_empty = False

                # Check if the line is an include:
                if re.findall(Regex.INCLUDE, line):
                    # Mark that empty line is expected:
                    expects_empty = f"{line_count}"


    return report

v = main(paths)

if v.count != 0:
    v.print_report()
