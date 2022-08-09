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
    # Opening conditionals
    #
    # Matches any opening conditional; single-line and multi-line (e.g. ifdef, ifndef, ifeval)
    #
    # Examples
    #
    #   ifdef::condition[]
    #   ifndef::condition[]
    #   ifeval::["{attribute}" >= "v.1"]
    #   ifdef::condition[description!]
    #
    OPENING_CONDITIONAL = re.compile(r'(ifdef|ifndef|ifeval)::(.*)?\]')

    # Closing conditionals
    #
    # Matches any closing conditional (e.g. endif)
    #
    # Examples
    #
    #   endif::condition[]
    #   endif::[]
    #
    CLOSING_CONDITIONAL = re.compile(r'endif::(.*)?\]')

    # Single-line conditionals
    #
    # Matches only single-line conditionals (e.g. ifdef, ifndef)
    #
    # Examples
    #
    # ifdef::condition[description!]
    # ifndef::condition[description!]
    #
    SINGLE_LINE_CONDITIONAL = re.compile(r'(ifdef|ifndef)::[\S]*\[(?!\])(.*)\]')

    # Empty line after
    #
    # Matches an include followed by an empty line
    #
    # Examples
    #
    #   include::file.adoc[]
    #
    #
    EMPTY_LINE_AFTER_INCLUDE = re.compile(r'include::.*\]\n\n')

    # Module content type tags
    #
    # Matches procedure, concept, reference content type tags
    #
    # Examples
    #
    #   :_content-type: PROCEDURE
    #   :_content-type: CONCEPT
    #   :_content-type: REFERENCE
    #
    MODULE_TYPE = re.compile(r':_content-type: (PROCEDURE|CONCEPT|REFERENCE)')

    # Assembly content type tag
    #
    # Matches assembly content type tag
    #
    # Examples
    #
    #   :_content-type: ASSEMBLY
    #
    ASSEMBLY_TYPE = re.compile(r':_content-type: ASSEMBLY')

    # Snippet content type tag (NOT USED)
    #
    # Matches snippet content type tag
    #
    # Examples
    #
    #   :_content-type: SNIPPET
    #
    SNIPPET_TYPE = re.compile(r':_content-type: SNIPPET')

    # Assembly prefix (NOT USED)
    #
    # Matches assembly prefix
    #
    # Examples
    #
    #   <PATH>/assembly_file-name.adoc
    #   <PATH>/assembly-file-name.adoc
    #
    PREFIX_ASSEMBLIES = re.compile(r'.*\/assembly.*\.adoc')

    # Modules prefix (NOT USED)
    #
    # Matches modules prefix (e.g. con, proc, ref)
    #
    # Examples
    #
    #   <PATH>/con_file-name.adoc
    #   <PATH>/con-file-name.adoc
    #   <PATH>/proc_file-name.adoc
    #   <PATH>/proc-file-name.adoc
    #   <PATH>/ref_file-name.adoc
    #   <PATH>/ref-file-name.adoc
    #
    PREFIX_MODULES = re.compile(r'.*\/con.*\.adoc|.*\/proc.*\.adoc|.*\/ref.*\.adoc')

    # Vanilla xrefs
    #
    # Matches any vanilla xref
    #
    # Excludes pseudo vanilla like <<some content>>
    #
    # Examples
    #
    #   <<id_parent-id>>
    #   <<some-id>>
    #   <<id,text>>
    #
    VANILLA_XREF = re.compile(r'<<[^\s]*>>')

    # Multi-line comment
    #
    # Matches multi-line comments
    #
    # Examples
    #
    #   ////
    #   This is a
    #   multi-line comment
    #   ////
    #
    MULTI_LINE_COMMENT = re.compile(r'(/{4,})(.*\n)*?(/{4,})')

    # Single-line comment TODO: remove lookaround
    #
    # Matches any single-line comment
    #
    # Example
    #   // This is a single-line comment
    #
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

    # Human readable label
    # Matches human readable label for xrefs and links
    #
    # Examples
    #
    #   xref:some-id[Human readable label]
    #   https://link.com[Human readable label]
    #   link:https://link.com[Human readable label]
    #
    HUMAN_READABLE_LABEL = re.compile(r'xref:[\S]*\[\]|\b(?:https?|file|ftp|irc):\/\/[^\s\[\]<]*\[\]')

    # Include statement
    # Matches all includes
    #
    # Examples
    #
    #   include::file.adoc[]
    #   include::file.adoc[leveloffset=+1]
    #
    INCLUDE_STATEMENT = re.compile(r'include::[\S]*\]')

    # Included snippets
    #
    # Matches any snippet include
    #
    # Example
    #   include::sni-file.adoc[leveloffset=+1]
    #   include::snip_file.adoc[leveloffset=+1]
    #
    SNIPPET_INCLUDE = re.compile(r'include::[\S]*(snip-|snip_)[\S]*\[')

    # Related information section
    #
    #
    # Matches related info section (case is ignored)
    #
    # Examples
    #   = Related information
    #   .Related information
    #
    RELATED_INFO = re.compile(r'= Related information|\.Related information', re.IGNORECASE)

    # Additional information information section
    #
    #
    # Matches additional info section (case is ignored)
    #
    # Examples
    #   == Additional information
    #   .Additional information
    #
    ADDITIONAL_RES = re.compile(r'== Additional resources\n|\.Additional resources\n', re.IGNORECASE)

    ADD_RES_ASSEMBLY = re.compile(r'== Additional resources', re.IGNORECASE)
    ADD_RES_MODULE = re.compile(r'\.Additional resources', re.IGNORECASE)
    CORRECT_ADDITIONAL_RES_SECTION = re.compile(r'\[role="_additional-resources"\]\n(== Additional resources|\.Additional resources)\n(\*|(ifdef|ifndef|ifeval)::(.*)?\]\n\*)', re.IGNORECASE)
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


def add_res_section_module_check(report, stripped_file, file_path):
    if re.findall(Regex.ADDITIONAL_RES, stripped_file):
        if not re.findall(Regex.ADD_RES_MODULE, stripped_file):
            report.create_report("Additional resources section for modules should be `.Additional resources`. Wrong section name was", file_path)


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
    if re.findall(Tags.ADD_RES, stripped_file):
        if not re.findall(Regex.ADDITIONAL_RES, stripped_file):
            return True


def add_res_wrong_format(stripped_file):
    if not re.findall(Regex.ADDITIONAL_RES, stripped_file):
        return
    if not stripped_file.count(Tags.ADD_RES) == 1:
        return
    if not re.findall(Regex.CORRECT_ADDITIONAL_RES_SECTION, stripped_file):
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

    if add_res_wrong_format(stripped_file):
        report.create_report('incorrectly formatted Additional recourses section', file_path)

    if vanilla_xref_check(stripped_file):
        report.create_report('vanilla xrefs', file_path)

    if inline_anchor_check(stripped_file):
        report.create_report('in-line anchors', file_path)

    if html_markup_check(stripped_file):
        report.create_report('HTML markup', file_path)

    if human_readable_label_check(stripped_file):
        report.create_report('xrefs or link without a human readable label', file_path)

    if lvloffset_check(stripped_file):
        report.create_report('unsupported use of :leveloffset:. unsupported includes', file_path)

    if abstarct_tag_multiple_check(stripped_file):
        report.create_report('multiple abstract tags', file_path)

    if empty_line_after_include_check(original_file):
        report.create_report('no empty line after include statement', file_path)
