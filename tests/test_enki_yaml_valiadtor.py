import unittest
import os
import yaml

from src.enki_yaml_valiadtor import *


# needs empty.yml, valid.yml
class TestGetYamlSize(unittest.TestCase):
    def setUp(self):
        self.current_path = os.path.dirname(__file__)
        self.fixtures_path = os.path.join(self.current_path, "fixtures")

    def test_empty_yml_file(self):
        file_name = os.path.join(self.fixtures_path, "empty.yml")
        manipulating_build_yaml = ManipulatingBuildYaml(file_name)

        with self.assertRaises(SystemExit) as cm:
            manipulating_build_yaml.get_yaml_size()

        self.assertEqual(cm.exception.code, 2)

    def test_valid_yml_file(self):
        file_name = os.path.join(self.fixtures_path, "valid.yml")
        manipulating_build_yaml = ManipulatingBuildYaml(file_name)

        try:
            manipulating_build_yaml.get_yaml_size()
        except ZeroDivisionError as exc:
            assert False, f"'valid.yml' raised an exception {exc}"


# needs syntax-error.yml, valid.yml
class TestGetLoadedYaml(unittest.TestCase):
    def setUp(self):
        self.current_path = os.path.dirname(__file__)
        self.fixtures_path = os.path.join(self.current_path, "fixtures")

    def test_corrupt_yml_syntax(self):
        file_name = os.path.join(self.fixtures_path, "syntax-error.yml")
        manipulating_build_yaml = ManipulatingBuildYaml(file_name)

        with self.assertRaises(SystemExit) as cm:
            manipulating_build_yaml.get_loaded_yaml()

        self.assertEqual(cm.exception.code, 2)

    def test_valid_yml_syntax(self):
        file_name = os.path.join(self.fixtures_path, "valid.yml")
        manipulating_build_yaml = ManipulatingBuildYaml(file_name)

        try:
            manipulating_build_yaml.get_loaded_yaml()
        except ZeroDivisionError as exc:
            assert False, f"'valid.yml' raised an exception {exc}"


class TestGetYamlErrors(unittest.TestCase):
    def setUp(self):
        self.current_path = os.path.dirname(__file__)
        self.fixtures_path = os.path.join(self.current_path, "fixtures")

    def test_missing_key_yml(self):
        file = yaml.safe_load("""
variants:
  - name: rhel8
    attributes:
      - rhel-8/common-content/_attributes.adoc

    build: true
    files:
      included:
        - rhel-8/assemblies/*.adoc
""")
        with self.assertRaises(SystemExit) as cm:
            get_yaml_errors(file)

        self.assertEqual(cm.exception.code, 2)

    def test_missing_value_yml(self):
        file = yaml.safe_load("""
repository:
variants:
  - name: rhel8
    attributes:
      - rhel-8/common-content/_attributes.adoc

    build: true
    files:
      included:
        - rhel-8/assemblies/*.adoc
""")
        with self.assertRaises(SystemExit) as cm:
            get_yaml_errors(file)

        self.assertEqual(cm.exception.code, 2)

    def test_valid_yml(self):
        path_to_script = os.path.dirname(os.path.realpath(__file__))
        file_name = (path_to_script + "/fixtures/valid.yml")
        manipulating_build_yaml = ManipulatingBuildYaml(file_name)
        file = manipulating_build_yaml.get_loaded_yaml()

        try:
            get_yaml_errors(file)
        except ZeroDivisionError as exc:
            assert False, f"'valid.yml' raised an exception {exc}"


# run all the tests in this file
if __name__ == '__main__':
    unittest.main()
