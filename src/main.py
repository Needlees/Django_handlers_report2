import argparse
from typing import Type

import reports

REPORTS: dict[str, Type[reports.ReportTable]] = {
    'handlers': reports.HandlersReport
}


def parse_args() -> tuple[list[str], str]:
    parser = argparse.ArgumentParser(
        description='Вывод отчета на основании лог-файлов',
        epilog='Пример использования: python main.py app1.log app2.log app3.log --report handlers'
    )
    parser.add_argument('log_files', nargs='+', help='Лог-файлы для обработки')
    parser.add_argument('--report', required=True, choices=REPORTS, help='Наименование отчета')

    args = parser.parse_args()
    return args.log_files, args.report


def check_files(files: list[str]) -> None:
    for f in files:
        try:
            with open(f, encoding='utf-8'):
                pass
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{f}' не существует.")


class Report:
    def __init__(self, report_table: reports.ReportTable) -> None:
        self.title: str = report_table.title
        self.header: list[str] = report_table.header
        self.table: list[list[str | int]] = report_table.table

        self.total_column: list[int] = self.__get_total_column()
        self.total_row: list[int] = self.__get_total_row()
        self.total_all: int = sum(self.total_row)
        self.column_widths: list[int] = self.__get_column_widths()

    def __get_total_column(self):
        return [sum(i for i in row if isinstance(i, int)) for row in self.table]

    def __get_total_row(self):
        return [
            sum(self.table[j][i] if isinstance(self.table[j][i], int) else 0 for j in range(len(self.table)))
            for i in range(len(self.table[0]))
        ]

    def __get_column_widths(self):
        return [
            max(len(str(row[i])) for row in [self.header, *self.table, self.total_row])
            for i in range(len(self.table[0]))
        ]

    def output(self) -> None:
        # Total
        print(f'Total {self.title}:', self.total_all)
        print()

        # header
        print("—" * (sum(i for i in self.column_widths) + len(self.column_widths) * 4 + 6))
        for i, column in enumerate(self.header):
            print(str(column), ' ' * (self.column_widths[i] - len(str(column))), end='')
            print(' | ', end='')
        print("TOTAL")
        print("—" * (sum(i for i in self.column_widths) + len(self.column_widths) * 4 + 6))

        # table
        for i, row in enumerate(self.table):
            for j, value in enumerate(row):
                print(str(value), ' ' * (self.column_widths[j] - len(str(value))), end='')
                print(' | ', end='')
            print(self.total_column[i])

        # total row
        print("—" * (sum(i for i in self.column_widths) + len(self.column_widths) * 4 + 6))
        print(' ' * (self.column_widths[0] + 1), end='')
        print(' | ', end='')
        for i in range(1, len(self.total_row)):
            print(str(self.total_row[i]), ' ' * (self.column_widths[i] - len(str(self.total_row[i]))), end='')
            print(' | ', end='')


class App:
    def __init__(self) -> None:
        self.log_files, self.report_name = parse_args()
        check_files(self.log_files)
        Report(REPORTS[self.report_name](self.log_files)).output()


if __name__ == '__main__':
    App()
