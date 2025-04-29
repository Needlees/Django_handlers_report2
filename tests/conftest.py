import pytest

from src.main import check_files
from src.reports import ReportTable


@pytest.fixture(params=[
    [['NAME', 'COL1', 'COL2'], ['Name1', 5, 7], ['Name2', 0, 3]],
    [['NAME', 'COL1', 'COL2', 'COL3'], ['Name1', 5, 'type1', 7], ['Name2', 0, 'type2', 3]],
    [['HANDLER', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], ['/admin/dashboard/', 0, 10, 0, 3, 0],
     ['/admin/login/', 0, 8, 0, 2, 0], ['/api/v1/auth/login/', 0, 7, 0, 1, 0],
     ['/api/v1/cart/', 0, 4, 0, 0, 0], ['/api/v1/checkout/', 0, 11, 0, 2, 0],
     ['/api/v1/orders/', 0, 6, 0, 3, 0], ['/api/v1/payments/', 0, 10, 0, 2, 0],
     ['/api/v1/products/', 0, 8, 0, 3, 0], ['/api/v1/reviews/', 0, 13, 0, 1, 0],
     ['/api/v1/shipping/', 0, 5, 0, 2, 0], ['/api/v1/support/', 0, 9, 0, 3, 0],
     ['/api/v1/users/', 0, 7, 0, 2, 0]]
])
def report_test(request):
    class ReportTableTest(ReportTable):
        def __init__(self):
            super().__init__()
            self.__header = request.param[0]
            self.__table = request.param[1:]

        @property
        def title(self):
            return 'tests'

        @property
        def header(self):
            return self.__header

        @property
        def table(self):
            return self.__table

    return ReportTableTest()


@pytest.fixture(params=[
    [".\\Logs\\app1.log", ".\\Logs\\app2.log", ".\\Logs\\app3.log"],
    [".\\Logs\\app2.log", ".\\Logs\\app3.log"],
    [".\\Logs\\app3.log"]
])
def file_logs(request):
    check_files(request.param)
    return request.param
