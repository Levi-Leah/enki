from junit_xml import TestSuite, TestCase
import junit_xml_output


class Report():
    """Create and print report. thank u J."""

    def __init__(self):
        """Create placeholder for problem description."""
        self.report = {}
        self.count = 0

    def create_report(self, category, file_path, function_name):
        """Generate report."""
        self.count += 1
        if not category in self.report:
            self.report[category] = {}
        if file_path not in self.report[category]:
            self.report[category][file_path] = []
        self.report[category][file_path].append(function_name)

    def print_report(self, output=None):
        """Print report."""

        if output == 'oneline':
            for category, files in self.report.items():
                for file in files:
                    print("{}: ERROR: {} found.".format(file, category))
            return

        if output == 'gitlab':

            test_cases = []

            for category, files in self.report.items():
                for file_path, function_name in files.items():
                    test_case = TestCase(str(function_name), 'ValidationChecks', '', '', '', '', 'timestamp', 'status', 'class', file_path, 'line', 'log', 'url')
                    test_case.add_failure_info('Failure message', '', 'FAIL')
                    test_case.add_error_info(f'{category} found', '', 'ERROR')
                    test_cases.append(test_case)

            ts = [TestSuite("ValidationErrors", test_cases)]
            print(TestSuite.to_xml_string(ts, prettyprint=True))

            return

        separator = "\n\t"

        for category, files in self.report.items():
            print("\nERROR: {} found in the following files:".format(category))
            print('\t' + separator.join(files))
