import re


class Tags:
    """Define tags."""
    ABSTRACT = '[role="_abstract"]'
    ADD_RES = '[role="_additional-resources"]'
    EXPERIMENTAL = ':experimental:'
    LVLOFFSET = ':leveloffset:'


class Regexes:
    """Define regular expressions for the checks."""

    # Additional resources tag
    #
    # Matches add res tag
    # Duplicates Tag.ADD_RES cause some tests need it as regex
    #
    # Examples
    #
    #   [role="_additional-resources"]
    #
    ADD_RES = re.compile(r'\[role="_additional-resources"\]')

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
    SINGLE_LINE_CONDITIONAL = re.compile(
        r'(ifdef|ifndef)::[\S]*\[(?!\])(.*)\]')

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

    # Snippet content type tag
    #
    # Matches snippet content type tag
    #
    # Examples
    #
    #   :_content-type: SNIPPET
    #
    SNIPPET_TYPE = re.compile(r':_content-type: SNIPPET')

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
    SINGLE_LINE_COMMENT = re.compile(
        r'(?<!\/\/)(?<!\/)^\/\/(?!\/\/).*\n', re.M)

    # In-line anchor
    #
    # Matches in-line anchors
    #
    # Example
    #   [[this-is-an-inline-anchor]]
    #
    INLINE_ANCHOR = re.compile(r'=.*\[\[.*\]\]')

    # HTML markup (NOTE:DISABLED)
    #
    # Matches multi-line and single-line html markup
    #
    # Example
    #
    #   <title>Title</title>
    #
    #   <title>
    #       Page Title
    #   </title>
    #
    HTML_MARKUP = re.compile(r'(?<!\`|_)<.*>.*<\/.*>|<.*>\n.*\n</.*>(?!\`|_)')

    # Internal conditionals TODO: expand regex to include oneliners
    #
    # Matches internal conditionals
    #
    # Example
    #   ifdef::internal[]
    #   This text
    #   Is only visible
    #   Internally
    #   endif::[]
    #
    INTERNAL_IFDEF = re.compile(r'(ifdef::internal\[\])(.*\n)*?(endif::\[\])')

    # Code blocks
    #
    # Matches code blocks
    #
    # Example
    #
    #    ----
    #    this is a code block
    #    ----
    #
    #    ....
    #    this is also a code block
    #    ....
    #
    #    --
    #    I guess this is a thing too
    #    --
    CODE_BLOCK = re.compile(r'((-|\.){2,}|--\n+)(.*\n)*?((-|\.){2,})')

    # Links without uman readable label
    # Matches links without human readable label
    #
    # Examples
    #
    #   https://link.com[]
    #   link:https://link.com[]
    #
    HUMAN_READABLE_LABEL_LINKS = re.compile(
        r'\b(?:https?|file|ftp|irc):\/\/[^\s\[\]<]*\[\]')

    # Xrefs without human readable label
    # Matches xrefs without human readable label for xrefs and links
    #
    # Examples
    #
    #   xref:some-id[]
    #
    HUMAN_READABLE_LABEL_XREFS = re.compile(
        r'xref:[\S]*\[\]')

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
    RELATED_INFO = re.compile(
        r'= Related information|\.Related information', re.IGNORECASE)

    # Additional information resources section
    #
    #
    # Matches additional res section (case is ignored)
    #
    # Examples
    #   == Additional information
    #   .Additional information
    #
    ADDITIONAL_RES = re.compile(
        r'== Additional resources|\.Additional resources', re.IGNORECASE)

    # CORRECT_ADDITIONAL_RES_SECTION = re.compile(
    #     r'\[role="_additional-resources"\]\n+((ifdef|ifndef|ifeval|endif)::.*\]\n+)*?(== Additional resources|\.Additional resources)\n+((ifdef|ifndef|ifeval|endif)::.*\]\n+)*?((\* .*\n+((ifdef|ifndef|ifeval|endif)::.*\]\n+)*?(^//.*\n+)*?((\/{4,})(.*\n)*?(\/{4,})\n+)*?)*\z)', re.IGNORECASE)

    # Deprecated footnoteref macro
    #
    # Matched deprecated footnoteref macro
    #
    # Examples
    #   footnoteref:[text]
    #
    FOOTNOTE_REF = re.compile(r'footnoteref:\[.*?\]')
