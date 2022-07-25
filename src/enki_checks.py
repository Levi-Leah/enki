#!/usr/bin/python3

import re


class Tags:

    """Define tags."""
    ABSTRACT = '[role="_abstract"]'
    ADD_RES = '[role="_additional-resources"]'
    EXPERIMENTAL = ':experimental:'
    LVLOFFSET = ':leveloffset:'


class Regex:
    """Define regular expresiions for the checks."""

    OPENING_CONDITIONAL = re.compile(r'(ifdef|ifndef|ifeval)::(.*)?\]')
    CLOSING_CONDITIONAL = re.compile(r'endif::(.*)?\]')
    SINGLE_LINE_CONDITIONAL = re.compile(r'(ifdef|ifndef)::[\S]*\[(?!\])(.*)\]')
    INCLUDE = re.compile(r'include::.*\]\n')
    EMPTY_LINE_AFTER_INCLUDE = re.compile(r'include::.*\]\n\n')
    MODULE_TYPE = re.compile(r':_content-type: (PROCEDURE|CONCEPT|REFERENCE)')
    ASSEMBLY_TYPE = re.compile(r':_content-type: ASSEMBLY')
    SNIPPET_TYPE = re.compile(r':_content-type: SNIPPET')
    PREFIX_ASSEMBLIES = re.compile(r'.*\/assembly.*\.adoc')
    PREFIX_MODULES = re.compile(r'.*\/con.*\.adoc|.*\/proc.*\.adoc|.*\/ref.*\.adoc')
    # should exclude pseudo vanilla like <<some content>>
    VANILLA_XREF = re.compile(r'<<[^\s]*>>')
    MULTI_LINE_COMMENT = re.compile(r'(/{4,})(.*\n)*?(/{4,})')
    SINGLE_LINE_COMMENT = re.compile(r'(?<!\/\/)(?<!\/)^\/\/(?!\/\/).*\n', re.M)
    EMPTY_LINE_AFTER_ABSTRACT = re.compile(r'\[role="_abstract"]\n(?=\n)')
    FIRST_PARA = re.compile(r'(?<!\n\n)\[role="_abstract"]\n(?!\n)')
    NO_EMPTY_LINE_BEFORE_ABSTRACT = re.compile(r'(?<!\n\n)\[role="_abstract"]')
    COMMENT_AFTER_ABSTRACT = re.compile(r'\[role="_abstract"]\n(?=\//|(/{4,})(.*\n)*?(/{4,}))')
    VAR_IN_TITLE = re.compile(r'(?<!\=)=\s.*{.*}.*')
    INLINE_ANCHOR = re.compile(r'=.*\[\[.*\]\]')
    UI_MACROS = re.compile(r'btn:\[.*\]|menu:.*\[.*\]|kbd:.*\[.*\]')
    HTML_MARKUP = re.compile(r'(?<!\`|_)<.*>.*<\/.*>|<.*>\n.*\n</.*>(?!\`|_)')
    INTERNAL_IFDEF = re.compile(r'(ifdef::internal\[\])(.*\n)*?(endif::\[\])')
    CODE_BLOCK_DASHES = re.compile(r'(-{4,})(.*\n)*?(-{4,})')
    CODE_BLOCK_DOTS = re.compile(r'(\.{4,})(.*\n)*?(\.{4,})')
    CODE_BLOCK_TWO_DASHES = re.compile(r'(-{2,})(.*\n)*?(-{2,})')
    HUMAN_READABLE_LABEL_XREF = re.compile(r'xref:.*\[]')
    HUMAN_READABLE_LABEL_LINK = re.compile(r'\b(?:https?|file|ftp|irc):\/\/[^\s\[\]<]*\[\]')
    NESTED_ASSEMBLY = re.compile(r'include.*assembly([a-z|0-9|A-Z|\-|_]+)\.adoc(\[.*\])')
    NESTED_MODULES = re.compile(r'include.*(proc|con|ref)([a-z|0-9|A-Z|\-|_]+)\.adoc(\[.*\])')
    RELATED_INFO = re.compile(r'= Related information|\.Related information', re.IGNORECASE)
    ADDITIONAL_RES = re.compile(r'= Additional resources|\.Additional resources', re.IGNORECASE)
    ADD_RES_TAG = re.compile(r'\[role="_additional-resources"]')
    ADD_RES_ASSEMBLY = re.compile(r'== Additional resources', re.IGNORECASE)
    ADD_RES_MODULE = re.compile(r'\.Additional resources', re.IGNORECASE)
    EMPTY_LINE_AFTER_ADD_RES_TAG = re.compile(r'\[role="_additional-resources"]\n(?=\n)')
    COMMENT_AFTER_ADD_RES_TAG = re.compile(r'\[role="_additional-resources"]\n(?=\//|(/{4,})(.*\n)*?(/{4,}))')
    EMPTY_LINE_AFTER_ADD_RES_HEADER = re.compile(r'== Additional resources\s\n|\.Additional resources\n\n', re.IGNORECASE)
    FOOTNOTE_REF = re.compile(r'footnoteref:\[.*?\]')


def undetermined_conditional_check(stripped_file):
    open = re.findall(Regex.OPENING_CONDITIONAL, stripped_file)
    closed = re.findall(Regex.CLOSING_CONDITIONAL, stripped_file)
    if len(open) != len(closed):
        return True


def footnote_ref_check(stripped_file):
    if re.findall(Regex.FOOTNOTE_REF, stripped_file):
        return True


def empty_line_after_include_check(original_file):
    if re.findall(Regex.INCLUDE, original_file) and not re.findall(Regex.EMPTY_LINE_AFTER_INCLUDE, original_file):
        return True


def vanilla_xref_check(stripped_file):
    """Check if the file contains vanilla xrefs."""
    if re.findall(Regex.VANILLA_XREF, stripped_file):
        return True


def inline_anchor_check(stripped_file):
    """Check if the in-line anchor directly follows the level 1 heading."""
    if re.findall(Regex.INLINE_ANCHOR, stripped_file):
        return True


def human_readable_label_check_xrefs(stripped_file):
    "Check if the human readable label is present in xrefs."""
    if re.findall(Regex.HUMAN_READABLE_LABEL_XREF, stripped_file):
        return True


def human_readable_label_check_links(stripped_file):
    "Check if the human readable label is present in links."""
    if re.findall(Regex.HUMAN_READABLE_LABEL_LINK, stripped_file):
        return True


def html_markup_check(stripped_file):
    """Check if HTML markup is present in the file."""
    if re.findall(Regex.HTML_MARKUP, stripped_file):
        return True


# Standalone check on modules_found
def nesting_in_modules_check(report, stripped_file, file_path):
    """Check if modules contains nested content."""
    if re.findall(Regex.NESTED_ASSEMBLY, stripped_file):
        report.create_report('nesting in modules. nesting', file_path)
    if re.findall(Regex.NESTED_MODULES, stripped_file):
        report.create_report('nesting in modules. nesting', file_path)


# Standalone check on modules_found
def add_res_section_module_check(report, stripped_file, file_path):
    if re.findall(Regex.ADDITIONAL_RES, stripped_file):
        if not re.findall(Regex.ADD_RES_MODULE, stripped_file):
            report.create_report("Additional resources section for modules should be `.Additional resources`. Wrong section name was", file_path)

# Standalone check on assemblies_found
def add_res_section_assembly_check(report, stripped_file, file_path):
    if re.findall(Regex.ADDITIONAL_RES, stripped_file):
        if not re.findall(Regex.ADD_RES_ASSEMBLY, stripped_file):
            return report.create_report("additional resources section for assemblies should be `== Additional resources`. Wrong section name was", file_path)


def lvloffset_check(stripped_file):
    """Check if file contains unsupported includes."""
    if re.findall(Tags.LVLOFFSET, stripped_file):
        return True


def abstarct_tag_multiple_check(stripped_file):
    """Checks if the abstract tag is not set or set more than once."""
    if stripped_file.count(Tags.ABSTRACT) > 1:
        return True


def related_info_check(stripped_file):
    """Checks if everything related to additional resources section is OK"""
    if re.findall(Regex.RELATED_INFO, stripped_file):
        return True


def add_res_tag_missing(stripped_file):
    if re.findall(Regex.ADDITIONAL_RES, stripped_file):
        if stripped_file.count(Tags.ADD_RES) == 0:
            return True


def add_res_tag_multiple(stripped_file):
    if stripped_file.count(Tags.ADD_RES) > 1:
        return True


def add_res_tag_without_header(stripped_file):
    if re.findall(Regex.ADD_RES_TAG, stripped_file):
        if not re.findall(Regex.ADDITIONAL_RES, stripped_file):
            return True


def empty_line_after_add_res_tag(stripped_file, original_file):
    if stripped_file.count(Tags.ADD_RES) == 1:
        if re.findall(Regex.EMPTY_LINE_AFTER_ADD_RES_TAG, original_file):
            return True


def comment_after_add_res_tag(stripped_file, original_file):
    if stripped_file.count(Tags.ADD_RES) == 1:
        if re.findall(Regex.COMMENT_AFTER_ADD_RES_TAG, original_file):
            return True


def empty_line_after_add_res_header(stripped_file, original_file):
    if stripped_file.count(Tags.ADD_RES) == 1:
        if re.findall(Regex.EMPTY_LINE_AFTER_ADD_RES_HEADER, original_file):
            return True


def checks(report, stripped_file, original_file, file_path):
    """Run the checks."""
    if undetermined_conditional_check(stripped_file):
        report.create_report('Unterminated conditional statement', file_path)

    if footnote_ref_check(stripped_file):
        report.create_report('Deprecated `footnoteref` markup was', file_path)

    if related_info_check(stripped_file):
        report.create_report('"Related information" section was', file_path)

    if add_res_tag_missing(stripped_file):
        report.create_report('additional resources tag not', file_path)

    if add_res_tag_multiple(stripped_file):
        report.create_report('multiple additional resources tags were', file_path)

    if add_res_tag_without_header(stripped_file):
        report.create_report('additional resources tag without the Additional resources header was', file_path)

    if empty_line_after_add_res_tag(stripped_file, original_file):
        report.create_report('an empty line after the additional resources tag was', file_path)

    if empty_line_after_add_res_header(stripped_file, original_file):
        report.create_report('an empty line after the additional resources header was', file_path)

    if comment_after_add_res_tag(stripped_file, original_file):
        report.create_report('a comment after the additional resources tag was', file_path)

    if vanilla_xref_check(stripped_file):
        report.create_report('vanilla xrefs', file_path)

    if inline_anchor_check(stripped_file):
        report.create_report('in-line anchors', file_path)

    if html_markup_check(stripped_file):
        report.create_report('HTML markup', file_path)

    if human_readable_label_check_xrefs(stripped_file):
        report.create_report('xrefs without a human readable label', file_path)

    if human_readable_label_check_links(stripped_file):
        report.create_report('links without a human readable label', file_path)

    if lvloffset_check(stripped_file):
        report.create_report('unsupported use of :leveloffset:. unsupported includes', file_path)

    if abstarct_tag_multiple_check(stripped_file):
        report.create_report('multiple abstract tags', file_path)

    if empty_line_after_include_check(original_file):
        report.create_report('no empty line after include statement', file_path)
