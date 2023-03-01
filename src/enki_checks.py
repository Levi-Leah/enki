import re
import itertools
import inspect
import sys

from enki_msg import Report
from enki_regex import Regexes, Tags

# standalone test to run on code blocks
def sudo_check(
    stripped_file: str,
    report: Report,
    file_path: str) -> None:
    """Checks if sudo access is mentioned in documentation."""
    if re.findall(Regexes.SUDO, stripped_file):
        report.create_report(
                      'Mentions of sudo access', file_path)

# standalone test to run on filenames;
# exclusive to CLI
def con_lang_filename_check(
    report: Report,
    file_path: str) -> None:
    """Checks if stop words are present in filaname."""
    if re.findall(Regexes.CON_LANG, file_path):
        report.create_report(
            'Filename contains word such as master, slave, whitelist, blacklist. Stopwords', file_path)


# standalone test to run on partially stripepd files;
# exclusive to CLI
def con_lang_check(
    stripped_file: str,
    report: Report,
    file_path: str) -> None:
    """Checks if stop words are present in file source."""
    if re.findall(Regexes.CON_LANG, stripped_file):
        report.create_report(
            'Words such as master, slave, whitelist, blacklist', file_path)


def path_xref_check(stripped_file: str) -> bool:
    """Checks if path-based xref is present."""
    if re.findall(Regexes.PATH_XREF, stripped_file):
        return True
    else:
        return False


def pantheon_env_check(stripped_file: str) -> bool:
    """Checks if pantheonenv var is present."""
    if re.findall(Regexes.PV_ENV, stripped_file):
        return True
    else:
        return False


def too_many_comments_check(
        original_file: str,
        stripped_file: str,
        report: Report,
        file_path: str) -> None:
    """Checks if more than 1/3 (34%) of the lines in a file are comments."""
    if len(stripped_file.splitlines()) < len(original_file.splitlines()) * 0.66:
        report.create_report(
            'More than 1/3 of the lines are comments. Too many comments', file_path)


def unterminated_conditional_check(stripped_file: str) -> bool:
    """Checks if the number of opening and closing conditionals match."""
    opening_conditional = re.findall(
        Regexes.OPENING_CONDITIONAL, stripped_file)
    closing_conditional = re.findall(
        Regexes.CLOSING_CONDITIONAL, stripped_file)
    if len(opening_conditional) != len(closing_conditional):
        return True
    else:
        return False


# NOTE: DISABLED
# def footnote_ref_check(stripped_file: str) -> bool:
#     """Checks if deprecated foornoteref is present."""
#     if re.findall(Regexes.FOOTNOTE_REF, stripped_file):
#         return True
#     else:
#         return False

# FIXME: might not catch all cases cause of comment being removed


def empty_line_after_include_check(stripped_file: str) -> bool:
    """Checks if there's an empty line after every include statement."""
    if re.findall(Regexes.EMPTY_LINE_AFTER_INCLUDE, stripped_file):
        return True
    else:
        return False


def vanilla_xref_check(stripped_file: str) -> bool:
    """Checks if the file contains vanilla xrefs."""
    if re.findall(Regexes.VANILLA_XREF, stripped_file):
        return True
    else:
        return False


# NOTE: DISABLED
# def human_readable_label_check_links(stripped_file: str) -> bool:
#     "Checks if the human readable label is present in links."""
#     if re.findall(Regexes.HUMAN_READABLE_LABEL_LINKS, stripped_file):
#         return True
#     else:
#         return False


# NOTE: DISABLED
# def human_readable_label_check_xrefs(stripped_file: str) -> bool:
#     "Checks if the human readable label is present in xrefs."""
#     if re.findall(Regexes.HUMAN_READABLE_LABEL_XREFS, stripped_file):
#         return True
#     else:
#         return False


# NOTE: DISABLED
def html_markup_check(stripped_file: str) -> bool:
    """Checks if HTML markup is present in the file."""
    if re.findall(Regexes.HTML_MARKUP, stripped_file):
        return True
    else:
        return False


def nesting_in_modules_check(
        report: Report,
        stripped_file: str,
        file_path: str) -> None:
    """Checks if modules contains nested content."""
    includes = re.findall(Regexes.INCLUDE_STATEMENT, stripped_file)

    error = 0
    for i in includes:
        if not Regexes.SNIPPET_INCLUDE.match(i):
            error += 1
    if error != 0:
        report.create_report('Nesting in modules', file_path)


def related_info_check(stripped_file: str) -> bool:
    """Checks if related information section is present."""
    if re.findall(Regexes.RELATED_INFO, stripped_file):
        return True
    else:
        return False


# NOTE: DISABLED
"""
def add_res_wrong_format_check(stripped_file: str) -> bool:
    if not re.findall(Regex.ADDITIONAL_RES, stripped_file):
        return False
    if not stripped_file.count(Tags.ADD_RES) == 1:
        return False
    if not re.findall(Regex.CORRECT_ADDITIONAL_RES_SECTION, stripped_file):
        return True
    # TODO: A provisional fallback value. Check if this it the right one.
    else:
        return False
"""


def checks(
        report: Report,
        stripped_file: str,
        original_file: str,
        file_path: str) -> None:
    """Run the checks."""

    if unterminated_conditional_check(stripped_file):
        report.create_report('Unterminated conditional statement', file_path)

    # NOTE: DISABLED
    # if footnote_ref_check(stripped_file):
    #     report.create_report('Deprecated `footnoteref` markup', file_path)

    if related_info_check(stripped_file):
        report.create_report('"Related information" section', file_path)

    # NOTE: DISABLED
    # if add_res_wrong_format_check(stripped_file):
    #    report.create_report('incorrectly formatted Additional recourses section', file_path)

    if vanilla_xref_check(stripped_file):
        report.create_report('Vanilla xrefs', file_path)

    # NOTE: DISABLED
    # if html_markup_check(stripped_file):
    #    report.create_report('HTML markup', file_path)

    # NOTE: DISABLED
    #if human_readable_label_check_links(stripped_file):
    #    report.create_report(
    #        'Links without the human readable label', file_path)

    # NOTE: DISABLED
    #if human_readable_label_check_xrefs(stripped_file):
    #    report.create_report(
    #        'Xrefs without the human readable label', file_path)

    if empty_line_after_include_check(stripped_file):
        report.create_report(
            'No empty line after the include statement', file_path)


    if pantheon_env_check(stripped_file):
        report.create_report('`pantheonenv` variable', file_path)


    if path_xref_check(stripped_file):
        report.create_report('Path-based xref', file_path)
