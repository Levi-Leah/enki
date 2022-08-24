from junit_xml import TestSuite, TestCase
from datetime import datetime
import time


class Report():
    """Create and print report. thank u J."""

    def __init__(self):
        """Create placeholder for problem description."""
        self.report = {}
        self.count = 0

    def create_report(self, category, file_path):
        """Generate report."""
        self.count += 1
        if not category in self.report:
            self.report[category] = []
        self.report[category].append(file_path)

    def print_report(self, output=None, start_time=None):
        """Print report."""

        if output == 'oneline':
            for category, files in self.report.items():
                for file in files:
                    print("{}: ERROR: {} found.".format(file, category))
            return

        if output == 'gitlab':
            # TODO: figure out how to display the correct total number of tests

            test_cases = []

            end_time = time.time()
            duration = end_time - start_time

            for category, files in self.report.items():
                for file in files:
                    # has to be unique; GitLab only displays once
                    testcase_name = f'{category} found in {file}'
                    testsuite_name = 'ValidationErrors'
                    # args: sys out, sys err, assertions num
                    time_stamp = datetime.timestamp(datetime.now())
                    # args: status, class
                    test_case = TestCase(testcase_name, testsuite_name, duration, '', '', '', time_stamp, '', '', file) # args: line, log, url
                    test_case.add_failure_info(f'{category} found.', '', 'ERROR')
                    test_cases.append(test_case)

            # args: hostname, id, package, timestamp, ? num, file, log, url, sys out, sys err
            ts = [TestSuite("ValidationErrors", test_cases)]
            print(TestSuite.to_xml_string(ts, prettyprint=True))

            return

        separator = "\n\t"

        for category, files in self.report.items():
            print("\nERROR: {} found in the following files:".format(category))
            print('\t' + separator.join(files))
