import unittest
from src.enki_regex import Regexes
from src.enki_checks import *
from src.enki_msg import Report
import os


# class for every function
class TestTooManyCommentsCheck(unittest.TestCase):
    def setUp(self):
        self.current_path = os.path.dirname(__file__)
        self.fixtures_path = os.path.join(self.current_path, "fixtures")

    def test_too_many_comments(self):
        file_name = os.path.join(self.fixtures_path, "comments.adoc")
        report = Report()

        with open(file_name, 'r') as file:
            original = file.read()
            stripped = Regexes.MULTI_LINE_COMMENT.sub('', original)
            stripped = Regexes.SINGLE_LINE_COMMENT.sub('', stripped)


            result = too_many_comments_check(original, stripped, report, file_name)
            self.assertIn('More than 1/3 of the lines are comments. Too many comments', report.report)

    def test_few_comments(self):
        file_name = os.path.join(self.fixtures_path, "few-comments.adoc")
        report = Report()

        with open(file_name, 'r') as file:
            original = file.read()
            stripped = Regexes.MULTI_LINE_COMMENT.sub('', original)
            stripped = Regexes.SINGLE_LINE_COMMENT.sub('', stripped)


            result = too_many_comments_check(original, stripped, report, file_name)
            self.assertNotIn('Over 1/3 of the file is comments. Too many comments', report.report)


class TestFootnoteRefCheck(unittest.TestCase):
    def test_deprecated_footnote(self):
        file_contents = """
footnoteref:[Some text]
"""
        result = footnote_ref_check(file_contents)
        self.assertTrue(result, "Should return True when file has a deprecated footnoteref.")

    def test_no_footnote(self):
        file_contents = """
No footnote.
"""
        result = footnote_ref_check(file_contents)
        self.assertFalse(result, "Should return False when file has no deprecated footnoteref.")


class TestUnterminatedConditionalCheck(unittest.TestCase):
    def test_closed_conditionals(self):
        file_contents = """
ifeval::[{ProductNumber} == 8]
ifndef::context[]
[id="assembly_affinity-in-rhel-for-real-time"]
endif::[]
ifdef::context[]
[id="assembly_affinity-in-rhel-for-real-time_{context}"]
= Affinity in
endif::[]
endif::[]
"""
        result = unterminated_conditional_check(file_contents)
        self.assertFalse(result, "Should return False when all conditionals are closed.")


    def test_unclosed_conditionals(self):
        file_contents = """
ifeval::[{ProductNumber} == 8]
ifndef::context[]
[id="assembly_affinity-in-rhel-for-real-time"]
endif::[]
ifdef::context[]
[id="assembly_affinity-in-rhel-for-real-time_{context}"]
= Affinity in

endif::[]
"""
        result = unterminated_conditional_check(file_contents)
        self.assertTrue(result, "Should return True when all conditionals are not closed.")


class TestEmptyLineAfterIncludeCheck(unittest.TestCase):
    def test_empty_line_present(self):
        file_contents = """= Heading

include::some.adoc[leveloffset=+1]

include::other.adoc[leveloffset=+1]
"""

        result = empty_line_after_include_check(file_contents)
        self.assertIsNone(result, "Should return None when the empty line is present.")

    def test_empty_line_not_present(self):
        file_contents = """= Heading

include::some.adoc[leveloffset=+1]
include::other.adoc[leveloffset=+1]
"""

        result = empty_line_after_include_check(file_contents)
        self.assertTrue(result, "Should return True when the empty line is present.")

class TestVanillaXrefCheck(unittest.TestCase):
    def test_tag_present(self):
        file_contents = """= Heading

<<This-is-a-vanilla-xref>>
<<this is not a vanilla xref>>
<not xref>
"""

        result = vanilla_xref_check(file_contents)
        self.assertTrue(result, "Should return True when file has a vanilla xref.")

    def test_tag_not_present(self):
        file_contents = """= Heading

<<this is not a vanilla xref>>
<not xref>
"""
        result = vanilla_xref_check(file_contents)
        self.assertFalse(result, "Should return False when file has no vanilla xref.")


class TestHumanReadableLabelCheck(unittest.TestCase):
    def test_label_present_xref(self):
        file_contents = """= Heading

[role="_abstract"]
This is examle abstract and xref:human-readable_label[present]."""

        result = human_readable_label_check(file_contents)
        self.assertIsNone(result, "Should return None when xref has a human readable label.")

    def test_label_not_present_xref(self):
        file_contents = """= Heading

[role="_abstract"]
This is examle abstract and xref:human-readable_label[present].
xref:human-readable-label_not-present[]."""

        result = human_readable_label_check(file_contents)
        self.assertTrue(result, "Should return True when xref has no human readable label.")

    def test_label_present_link(self):
        file_contents = """= Heading

[role="_abstract"]
This is examle abstract and http://www.sample-link.com[present]."""

        result = human_readable_label_check(file_contents)
        self.assertIsNone(result, "Should return None when link has a human readable label.")

    def test_label_not_present_link(self):
        file_contents = """= Heading

[role="_abstract"]
This is examle abstract and http://www.sample-link.com[]."""

        result = human_readable_label_check(file_contents)
        self.assertTrue(result, "Should return True when link has no human readable label.")


class TestHtmlMarkupCheck(unittest.TestCase):
    def test_html_markup_present(self):
        file_contents = """= Heading

<html>markup</html>"""

        result = html_markup_check(file_contents)
        self.assertTrue(result, "Should return True when file has HTML markup.")

    def test_html_markup_not_present(self):
        file_contents = """= Heading

<nothtml>markup<nothtml>"""

        result = html_markup_check(file_contents)
        self.assertIsNone(result, "Should return None when file has no HTML markup.")


class TestNestingInModules(unittest.TestCase):
    def setUp(self):
        self.file_path = "some/path"

    def test_nested_assembly_in_module(self):
        report = Report()

        file_contents = """= Heading

Some sample text.
include::assembly_some-assembly.adoc[]"""

        result = nesting_in_modules_check(report, file_contents, self.file_path)
        self.assertIn('Nesting in modules', report.report)

    def test_nested_module_in_module(self):
        report = Report()

        file_contents = """= Heading

Some sample text.
include::proc_some-module.adoc[]"""

        result = nesting_in_modules_check(report, file_contents, self.file_path)
        self.assertIn('Nesting in modules', report.report)

    def test_no_nested_in(self):
        report = Report()

        file_contents = ""

        result = nesting_in_modules_check(report, file_contents, self.file_path)
        self.assertNotIn('Nesting in modules', report.report)


class TestRelatedInfoCheck(unittest.TestCase):
    def test_module_section_present(self):
        file_contents = """= Heading

.Related information
Sample text."""
        result = related_info_check(file_contents)
        self.assertTrue(result, "Should return True when file has `.Related information` section.")

    def test_assembly_section_present(self):
        file_contents = """= Heading

= Related information
Sample text."""
        result = related_info_check(file_contents)
        self.assertTrue(result, "Should return True when file has `= Related information` section.")

    def test_no_section_present(self):
        file_contents = """= Heading

Sample text."""
        result = related_info_check(file_contents)
        self.assertFalse(result, "Should return False when file has no related information` section.")


# run all the tests in this file
if __name__ == '__main__':
    unittest.main()
