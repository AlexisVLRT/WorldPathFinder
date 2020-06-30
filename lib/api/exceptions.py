import inspect
import sys


def get_possible_exceptions():
    exc_list = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            exc_list.append(obj)
    return tuple(exc_list)


class StartOrEndUnspecified(BaseException):
    def __init__(self):
        self.response = f"A start map and an end map must be specified"


class MapIdNotAnInteger(BaseException):
    def __init__(self, value):
        self.response = f"start_map_id and end_map_id must be integers. Got {value}"


class CellNotAnInteger(BaseException):
    def __init__(self, value):
        self.response = f"start_cell and end_cell must be integers. Got {value}"


class BadCellRange(BaseException):
    def __init__(self, value):
        self.response = f"start_cell and end_cell values must be between 0 and 559. Got {value}"
