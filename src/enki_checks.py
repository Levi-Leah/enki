#!/usr/bin/python3

import re
from enki_regex import Regex, Tags


def too_many_comments_check(original_file, stripped_file, report, file_path):
    """Checks if more than 1/3 of the file is comments."""
    if stripped_file.count('\n') < original_file.count('\n')*0.75:
        report.create_report('Over 1/3 of the file is comments. Too many comments', file_path)


def unterminated_conditional_check(stripped_file):
    """Check if the number of opening conditionals matches
    the number of closing conditionals."""
    opening_conditional = re.findall(Regex.OPENING_CONDITIONAL, stripped_file)
    closing_conditional = re.findall(Regex.CLOSING_CONDITIONAL, stripped_file)
    if len(opening_conditional) != len(closing_conditional):
        return True


def footnote_ref_check(stripped_file):
    """Checks if deprecated foornoteref is present."""
    if re.findall(Regex.FOOTNOTE_REF, stripped_file):
        return True


def empty_line_after_include_check(original_file):
    """Checks if there's an empty line after every include statement."""
    if re.findall(Regex.INCLUDE_STATEMENT, original_file) and not re.findall(Regex.EMPTY_LINE_AFTER_INCLUDE, original_file):
        return True


def vanilla_xref_check(stripped_file):
    """Check if the file contains vanilla xrefs."""
    if re.findall(Regex.VANILLA_XREF, stripped_file):
        return True


def inline_anchor_check(stripped_file):
    """Check if the in-line anchor directly follows the level 1 heading."""
    if re.findall(Regex.INLINE_ANCHOR, stripped_file):
        return True


def human_readable_label_check(stripped_file):
    "Check if the human readable label is present in xrefs."""
    if re.findall(Regex.HUMAN_READABLE_LABEL, stripped_file):
        return True


#NOTE: DISABLED
def html_markup_check(stripped_file):
    """Check if HTML markup is present in the file."""
    if re.findall(Regex.HTML_MARKUP, stripped_file):
        return True


def nesting_in_modules_check(report, stripped_file, file_path):
    """Check if modules contains nested content."""
    includes = re.findall(Regex.INCLUDE_STATEMENT, stripped_file)

    for i in includes:
        if not Regex.SNIPPET_INCLUDE.match(i):
            report.create_report('nesting in modules. nesting', file_path)


def abstarct_tag_multiple_check(stripped_file):
    """Checks if the abstract tag is set more than once."""
    if stripped_file.count(Tags.ABSTRACT) > 1:
        return True


def related_info_check(stripped_file):
    """Checks if releted info section is present."""
    if re.findall(Regex.RELATED_INFO, stripped_file):
        return True


def add_res_tag_missing_check(stripped_file):
    """Checks if the add res tag is missing."""
    if re.findall(Regex.ADDITIONAL_RES, stripped_file):
        if stripped_file.count(Tags.ADD_RES) == 0:
            return True


def add_res_tag_multiple_check(stripped_file):
    """Checks if there are multiple add res tags."""
    if stripped_file.count(Tags.ADD_RES) > 1:
        return True


def add_res_tag_without_header_check(stripped_file):
    """Checks id add res header is missing."""
    if re.findall(Regex.ADD_RES, stripped_file):
        if not re.findall(Regex.ADDITIONAL_RES, stripped_file):
            return True


'''def add_res_wrong_format_check(stripped_file):
    if not re.findall(Regex.ADDITIONAL_RES, stripped_file):
        return
    if not stripped_file.count(Tags.ADD_RES) == 1:
        return
    if not re.findall(Regex.CORRECT_ADDITIONAL_RES_SECTION, stripped_file):
        return True'''


def checks(report, stripped_file, original_file, file_path):
    """Run the checks."""

    if unterminated_conditional_check(stripped_file):
        report.create_report('Unterminated conditional statement', file_path)

    if footnote_ref_check(stripped_file):
        report.create_report('Deprecated `footnoteref` markup was', file_path)

    if related_info_check(stripped_file):
        report.create_report('"Related information" section was', file_path)

    if add_res_tag_missing_check(stripped_file):
        report.create_report('additional resources tag not', file_path)

    if add_res_tag_multiple_check(stripped_file):
        report.create_report('multiple additional resources tags were', file_path)

    if add_res_tag_without_header_check(stripped_file):
        report.create_report('additional resources tag without the Additional resources header was', file_path)

    #NOTE: DISABLED
    #if add_res_wrong_format_check(stripped_file):
    #    report.create_report('incorrectly formatted Additional recourses section', file_path)

    if vanilla_xref_check(stripped_file):
        report.create_report('vanilla xrefs', file_path)

    if inline_anchor_check(stripped_file):
        report.create_report('in-line anchors', file_path)

    #NOTE: DISABLED
    #if html_markup_check(stripped_file):
    #    report.create_report('HTML markup', file_path)

    if human_readable_label_check(stripped_file):
        report.create_report('xrefs or link without a human readable label', file_path)

    if abstarct_tag_multiple_check(stripped_file):
        report.create_report('multiple abstract tags', file_path)

    if empty_line_after_include_check(original_file):
        report.create_report('no empty line after include statement', file_path)
