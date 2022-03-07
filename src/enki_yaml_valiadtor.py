#!/usr/bin/env/ python3

import sys
import os
import yaml
from cerberus import Validator, errors
from enki_msg import CustomErrorHandler


class ManipulatingBuildYaml():
    def __init__(self, path_to_yaml):
        self.path_to_yaml = path_to_yaml

    def get_file_name(self):
        if os.path.basename(self.path_to_yaml) != 'build.yml':
            print("\nERROR: Provided file is not a build.yml; exiting...")
            sys.exit(2)

    def get_yaml_existence(self):
        if not os.path.isfile(self.path_to_yaml):
            print("\nERROR: Provided file doesn't exist; exiting...")
            sys.exit(2)

    def get_yaml_size(self):
        """Test if build.yml is empty."""
        if os.path.getsize(self.path_to_yaml) == 0:
            print("\nERROR: Your build.yml file is empty; exiting...")
            sys.exit(2)

    def get_loaded_yaml(self):
        with open(self.path_to_yaml, 'r') as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError:
                print("There's a syntax error in your build.yml file. Please fix it and try again.\nTo detect an error try running yaml lint on your build.yml file.")
                sys.exit(2)


def get_yaml_errors(loaded_yaml):
    """Validate build.yml against a schema abd report errors."""
    path_to_script = os.path.dirname(os.path.realpath(__file__))
    # load schema
    schema = eval(open(path_to_script + '/schema.py', 'r').read())
    # load validator with custom error handler
    v = Validator(schema, error_handler=CustomErrorHandler())
    # validate the build.yml with schema
    v.validate(loaded_yaml, schema)

    if v.errors:
        print("ERROR: there is an error in your yaml file:")
        for key in v.errors.keys():
            print("\n\t'{}' {}".format(key, ', '.join(str(item) for item in v.errors[key])))
        sys.exit(2)


def yaml_file_validation(path_to_yaml):
    my_class = ManipulatingBuildYaml(path_to_yaml)

    my_class.get_file_name()
    my_class.get_yaml_existence()
    my_class.get_yaml_size()
    get_yaml_errors(my_class.get_loaded_yaml())
