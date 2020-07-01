import inspect
import sys


def get_possible_exceptions():
    exc_list = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            exc_list.append(obj)
    return tuple(exc_list)


class ApiBaseException(BaseException):
    def __init__(self):
        self.status = 500
        self.response = "Uncaught error occurred"


class StartOrEndUnspecified(ApiBaseException):
    def __init__(self):
        self.status = 400
        self.response = f"A start map and an end map must be specified"


class MapIdNotAnInteger(ApiBaseException):
    def __init__(self, value):
        self.status = 400
        self.response = f"start_map_id and end_map_id must be integers. Got {value}"


class CellNotAnInteger(ApiBaseException):
    def __init__(self, value):
        self.status = 400
        self.response = f"start_cell and end_cell must be integers. Got {value}"


class BadCellRange(ApiBaseException):
    def __init__(self, value):
        self.status = 400
        self.response = f"start_cell and end_cell values must be between 0 and 559. Got {value}"


class MissingParameter(ApiBaseException):
    def __init__(self, group):
        self.status = 400
        self.response = f"Missing at least one parameter of group {group}"


class TooManyRequests(ApiBaseException):
    def __init__(self):
        self.status = 429
        self.response = "Too many requests"


