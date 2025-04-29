import re

from abc import abstractmethod, ABC


class ReportTable(ABC):
    def __init__(self, file_logs=None):
        self.file_logs = file_logs

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def header(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def table(self) -> list[list[str | int]]:
        pass


class HandlersReport(ReportTable):
    def __init__(self, file_logs):
        super().__init__(file_logs)
        self.LVL = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        self.__table = []
        self.get_data_from_logs()

    @property
    def title(self):
        return 'requests'

    @property
    def header(self):
        return ['HANDLER', *self.LVL]

    @property
    def table(self):
        return self.__table

    def get_data_from_logs(self) -> None:
        report_dict: dict[str, dict[str, int]] = {}
        for log in self.file_logs:
            current_dict = {}
            try:
                with (open(log, encoding='utf-8') as file):
                    for line in file:
                        if 'django.request' in line:
                            match_str = re.findall(r".+\s(\w+) django.request:?:.*?(/\S+)", line)
                            if match_str:
                                level, handler = match_str[0]
                                if handler not in current_dict:
                                    current_dict[handler] = dict.fromkeys(self.LVL, 0)
                                current_dict[handler][level] += 1
            except Exception:
                raise

            # Объединение словарей с суммированием значений
            union_dict = {**report_dict, **current_dict}
            for key in report_dict.keys() & current_dict.keys():
                union_dict[key] = {l: report_dict[key][l] + current_dict[key][l] for l in self.LVL}
            report_dict = {**union_dict}

        # Сортировка и преобразование в список
        report_dict = dict(sorted(report_dict.items()))
        report_list = [
            [handler, *counts.values()]
            for handler, counts in report_dict.items()
        ]

        self.__table = report_list
