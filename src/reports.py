import re

from abc import abstractmethod, ABC
from collections import defaultdict
from multiprocessing import Pool, cpu_count


class ReportTable(ABC):
    def __init__(self, log_files=None):
        self.log_files = log_files

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
    def __init__(self, log_files):
        super().__init__(log_files)
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

    def get_request_stats(self, log: str) -> dict[str, dict[str, int]]:
        result = defaultdict(lambda: dict.fromkeys(self.LVL, 0))

        try:
            with (open(log, encoding='utf-8') as file):
                for line in file:
                    if 'django.request' not in line:
                        continue

                    match = re.search(r"\s(\w+)\s+django\.request:\s+.*?(/\S+)", line)
                    if match:
                        level, handler = match.groups()
                        if level in self.LVL:
                            result[handler][level] += 1

        except Exception as e:
            print(f"Ошибка при обработке файла {log}: {str(e)}")
            return {}

        return dict(result)

    def merge_dicts(self, main_dict: dict[str, dict[str, int]],
                    new_dict: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
        merged = {**main_dict, **new_dict}
        for key in main_dict.keys() & new_dict.keys():
            merged[key] = {level: main_dict[key][level] + new_dict[key][level] for level in self.LVL}
        return merged

    def get_data_from_logs(self) -> None:
        result_dict: dict[str, dict[str, int]] = {}

        with Pool(processes=min(cpu_count(), len(self.log_files))) as pool:
            dict_list = pool.map(self.get_request_stats, self.log_files)

        for current_dict in dict_list:
            result_dict = self.merge_dicts(result_dict, current_dict)

        sorted_items = sorted(result_dict.items())
        self.__table = [[handler, *counts.values()] for handler, counts in sorted_items]
