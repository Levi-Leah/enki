from junit_xml import TestSuite, TestCase
from datetime import datetime
import time


class Report():
    """Create and print report. thank u J."""

    def __init__(self):
        """Create placeholder for problem description."""
        self.report: dict[str, list[str]] = {}
        self.count = 0

    def create_report(self, category: str, file_path: str) -> None:
        """Generate report."""
        self.count += 1
        if not category in self.report:
            self.report[category] = []
        self.report[category].append(file_path)

    def print_report(self, start_time: float, output: str = None) -> None:
        """Print report."""

        if output == 'oneline':
            for category, files in self.report.items():
                for file in files:
                    print("{}: ERROR: {} found.".format(file, category))
            return

        if output == 'gitlab':

            test_cases = []
            end_time = time.time()

            for category, files in self.report.items():
                for file in files:
                    # time num, sys out, sys err, assertions num,
                    test_case = TestCase(f'{category} found in {file}', 'ValidationTests', (end_time - start_time),
                                         '', '', '', datetime.timestamp(datetime.now()), 'status', 'class', file, 'line', 'log', 'url')
                    test_case.add_failure_info(
                        f'{category} found.', '', 'ERROR')
                    test_cases.append(test_case)

            ts = [TestSuite("ValidationErrors", test_cases)]
            print(TestSuite.to_xml_string(ts, prettyprint=True))

            return

        separator = "\n\t"

        for category, files in self.report.items():
            print("\nERROR: {} found in the following files:".format(category))
            print('\t' + separator.join(files))
