from lib.api.exceptions import *


def sanitize(query, parameters_groups, *args):
    for group in parameters_groups:
        verify_group_completeness(query, group)

    return sanitize_parameters(query, *args)


def verify_group_completeness(query, group):
    present_elements = []
    for element in group:
        present_elements.append(query.get(element))
    if len(present_elements) != present_elements.count(None) and present_elements.count(None):
        raise MissingParameter(group)


def sanitize_parameters(query, *args):
    values = {}
    for arg in args:
        sanitizer = getattr(sys.modules[__name__], arg)
        values[arg] = sanitizer(query.get(arg))
    return values


def start_map_id(start_map_id_raw):
    return sanitize_map_id(start_map_id_raw)


def end_map_id(end_map_id_raw):
    return sanitize_map_id(end_map_id_raw)


def sanitize_map_id(map_id_raw):
    if map_id_raw is None:
        raise StartOrEndUnspecified

    try:
        map_id_int = int(map_id_raw)
    except ValueError:
        raise MapIdNotAnInteger(map_id_raw)

    return map_id_int


def start_cell(start_cell_raw):
    return sanitize_cell(start_cell_raw)


def end_cell(end_cell_raw):
    return sanitize_cell(end_cell_raw)


def sanitize_cell(cell_raw):
    if cell_raw is None:
        return None

    try:
        cell_int = int(cell_raw)
    except ValueError:
        raise CellNotAnInteger(cell_raw)

    if not (0 <= cell_int < 560):
        raise BadCellRange(cell_int)

    return cell_int
