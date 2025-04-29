import pytest

from src.main import Report
from src.reports import HandlersReport


@pytest.fixture
def report_handler(file_logs):
    return HandlersReport(file_logs)


def test_report_output(report_test):
    print()
    Report(report_test).output()


def test_report_handler(report_handler):
    print()
    report = Report(report_handler)
    report.output()
