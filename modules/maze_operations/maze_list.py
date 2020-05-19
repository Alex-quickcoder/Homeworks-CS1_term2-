""""""
import json


class MazesList:
    """"""

    def __init__(self, options_filename: str = "database/options.json",
                 list_filename: str = "database/mazes_list.json"):
        with open(options_filename, encoding="utf-8") as opt_f:
            options_dct = json.load(opt_f)
        for key in options_dct:
            self.__dict__[key] = options_dct[key]
        with open(list_filename, encoding="utf-8") as list_f:
            self.mazes_list = json.load(list_f)
        self.list_filename = list_filename

    def get_context(self):
        """"""
        return self.__dict__

    @staticmethod
    def _filter_condition(elem, filters: list):
        """"""
        for filt in filters:
            if filt not in elem:
                return False
        return True

    def sort_by_key(self, key: str, filters: list):
        """"""
        filtered = filter(lambda x: self._filter_condition(x["parameters"],
                                                           filters),
                          self.mazes_list)
        return sorted(filtered, key=lambda x: x["parameters"][key][0])

    def save(self):
        """"""
        with open(self.list_filename, encoding="utf-8") as list_f:
            self.mazes_list = json.load(list_f)

    def get_current_mazes(self):
        """"""
        return self.mazes_list
