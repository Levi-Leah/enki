import re
from enki_regex import Regex, Tags


def too_many_comments_check(original_file, stripped_file, report, file_path):
    """Checks if more than 1/3 (34%) of the lines in a file are comments."""
    if stripped_file.count('\n') < original_file.count('\n')*0.66:
        report.create_report('More than 1/3 of the lines are comments. Too many comments', file_path, 'too_many_comments_check')


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


def human_readable_label_check(stripped_file):
    "Check if the human readable label is present in xrefs."""
    if re.findall(Regex.HUMAN_READABLE_LABEL, stripped_file):
        return True


# NOTE: DISABLED
def html_markup_check(stripped_file):
    """Check if HTML markup is present in the file."""
    if re.findall(Regex.HTML_MARKUP, stripped_file):
        return True


def nesting_in_modules_check(report, stripped_file, file_path):
    """Check if modules contains nested content."""
    includes = re.findall(Regex.INCLUDE_STATEMENT, stripped_file)

    error = 0
    for i in includes:
        if not Regex.SNIPPET_INCLUDE.match(i):
            error += 1
    if error != 0:
        report.create_report('Nesting in modules', file_path, 'nesting_in_modules_check')


def related_info_check(stripped_file):
    """Checks if related info section is present."""
    if re.findall(Regex.RELATED_INFO, stripped_file):
        return True


# NOTE: DISABLED
def add_res_wrong_format_check(stripped_file):
    if not re.findall(Regex.ADDITIONAL_RES, stripped_file):
        return
    if not stripped_file.count(Tags.ADD_RES) == 1:
        return
    if not re.findall(Regex.CORRECT_ADDITIONAL_RES_SECTION, stripped_file):
        return True


def checks(report, stripped_file, original_file, file_path):
    """Run the checks."""

    if unterminated_conditional_check(stripped_file):
        report.create_report('Unterminated conditional statement', file_path, 'unterminated_conditional_check')

    if footnote_ref_check(stripped_file):
        report.create_report('Deprecated `footnoteref` markup', file_path, 'footnote_ref_check')

    if related_info_check(stripped_file):
        report.create_report('"Related information" section', file_path, 'related_info_check')

    # NOTE: DISABLED
    #if add_res_wrong_format_check(stripped_file):
    #    report.create_report('incorrectly formatted Additional recourses section', file_path, 'add_res_wrong_format_check')

    if vanilla_xref_check(stripped_file):
        report.create_report('Vanilla xrefs', file_path, 'vanilla_xref_check')

    # NOTE: DISABLED
    #if html_markup_check(stripped_file):
    #    report.create_report('HTML markup', file_path, 'html_markup_check')

    if human_readable_label_check(stripped_file):
        report.create_report('Xrefs or links without the human readable label', file_path, 'human_readable_label_check')

    if empty_line_after_include_check(original_file):
        report.create_report('No empty line after the include statement', file_path, 'empty_line_after_include_check')
