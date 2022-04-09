import unittest
from src.enki_checks import *
from src.enki_msg import Report


# class for every function
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


class TestInlineAnchorCheck(unittest.TestCase):
    def test_tag_present(self):
        file_contents = """= Heading[[inline-anchor]]

[role="_abstract"]
This is examle abstract."""

        result = inline_anchor_check(file_contents)
        self.assertTrue(result, "Should return True when file has an inline anchor.")

    def test_tag_not_present(self):
        file_contents = """= Heading

[role="_abstract"]
This is examle abstract."""

        result = inline_anchor_check(file_contents)
        self.assertFalse(result, "Should return False when file has no inline anchor.")


class TestExperimentalTagCheck(unittest.TestCase):
    def test_tag_present(self):
        file_contents = """:experimental:
= Heading

Some btn:[button]."""
        result = experimental_tag_check(file_contents)
        self.assertFalse(result, "Should return False when file has no inline anchor.")


class TestHumanReadableLabelCheckXref(unittest.TestCase):
    def test_label_present(self):
        file_contents = """= Heading

[role="_abstract"]
This is examle abstract and xref:human-readable_label[present]."""

        result = human_readable_label_check_xrefs(file_contents)
        self.assertIsNone(result, "Should return None when xref has a human readable label.")

    def test_label_not_present(self):
        file_contents = """= Heading

[role="_abstract"]
This is examle abstract and xref:human-readable_label[present].
xref:human-readable-label_not-present[]."""

        result = human_readable_label_check_xrefs(file_contents)
        self.assertTrue(result, "Should return True when xref has no human readable label.")


class TestHumanReadableLabelCheckLinks(unittest.TestCase):
    def test_label_present(self):
        file_contents = """= Heading

[role="_abstract"]
This is examle abstract and http://www.sample-link.com[present]."""

        result = human_readable_label_check_links(file_contents)
        self.assertIsNone(result, "Should return None when link has a human readable label.")

    def test_label_not_present(self):
        file_contents = """= Heading

[role="_abstract"]
This is examle abstract and http://www.sample-link.com[]."""

        result = human_readable_label_check_links(file_contents)
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
        self.assertIn('nesting in modules. nesting', report.report)

    def test_nested_module_in_module(self):
        report = Report()

        file_contents = """= Heading

Some sample text.
include::proc_some-module.adoc[]"""

        result = nesting_in_modules_check(report, file_contents, self.file_path)
        self.assertIn('nesting in modules. nesting', report.report)

    def test_no_nested_in(self):
        report = Report()

        file_contents = ""

        result = nesting_in_modules_check(report, file_contents, self.file_path)
        self.assertNotIn('nesting in modules. nesting', report.report)


class TestAddResSectionModuleCheck(unittest.TestCase):
    def setUp(self):
        self.file_path = "some/path"

    def test_add_res_section_none(self):
        report = Report()
        file_contents = ""

        result = add_res_section_module_check(report, file_contents, self.file_path)
        self.assertNotIn('Additional resources section for modules should be `.Additional resources`. Wrong section name was', report.report)

    def test_add_res_section_wrong(self):
        report = Report()
        file_contents = "== Additional resources"

        result = add_res_section_module_check(report, file_contents, self.file_path)
        self.assertIn('Additional resources section for modules should be `.Additional resources`. Wrong section name was', report.report)

    def test_add_res_section_correct(self):
        report = Report()
        file_contents = ".Additional resources"

        result = add_res_section_module_check(report, file_contents, self.file_path)
        self.assertNotIn('Additional resources section for modules should be `.Additional resources`. Wrong section name was', report.report)


class TestLvloffsetCheck(unittest.TestCase):
    def test_lvloffset_tag_not_present(self):
        file_contents = """= Heading

include::some-include.adoc[]"""

        result = lvloffset_check(file_contents)
        self.assertIsNone(result, "Should return None when file has no :leveloffset: tag.")

    def test_lvloffset_tag_present(self):
        file_contents = """= Heading

:leveloffset:
include::some-include.adoc[]"""

        result = lvloffset_check(file_contents)
        self.assertTrue(result, "Should return True when file has no :leveloffset: tag.")


class TestAbstractTagMultipleCheck(unittest.TestCase):
    def test_multiple_tags_present(self):
        file_contents = """= Heading
[role="_abstract"]
[role="_abstract"]
This is examle abstract."""
        result = abstarct_tag_multiple_check(file_contents)
        self.assertTrue(result, "Should return True when file has multiple abstract tags.")

    def test_no_multiple_tags_present(self):
        file_contents = """= Heading
[role="_abstract"]
This is examle abstract."""
        result = abstarct_tag_multiple_check(file_contents)
        self.assertFalse(result, "Should return False when file doesn't have multiple abstract tag.")


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
