import pytest
from contextlib import nullcontext as does_not_raise

from src.main import Report, App, parse_args


@pytest.mark.parametrize(
    "argv, res, expectation",
    [
        (
                ["main.py", r"Logs\app1.log", r"Logs\app2.log", r"Logs\app3.log", "--report", "handlers"],
                ([r"Logs\app1.log", r"Logs\app2.log", r"Logs\app3.log"], "handlers"), does_not_raise()
        ),
        (
                ["main.py", "--report", "handlers", r"Logs\app1.log"],
                ([r"Logs\app1.log"], "handlers"), does_not_raise()
        ),
        (
                ["main.py", "--report", "unknown_report", r"Logs\app1.log"],
                ([r"Logs\app1.log"], "unknown_report"), pytest.raises(SystemExit)
        ),
    ]
)
def test_parse_args(argv, res, expectation, monkeypatch):
    monkeypatch.setattr("sys.argv", argv)
    with expectation:
        assert parse_args() == res


def test_check_files(file_logs):
    assert file_logs


def test_report__get_column_widths(report_test):
    report = Report(report_test)
    for row in [*report.table]:
        for j, val in enumerate(row):
            assert len(str(val)) <= report.column_widths[j]


def test_app(monkeypatch):
    monkeypatch.setattr("sys.argv",
                        ["main.py", r"Logs\app1.log", r"Logs\app2.log", r"Logs\app3.log", "--report", "handlers"])
    App()
