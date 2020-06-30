import json

from bottle import route, run, request

from lib.assets_management.assets_manager import Assets
from lib.path import get_path
from lib.api.input import *

assets = Assets.instance()


@route('/get_path')
def path():

    try:
        values = sanitize(
            request.query,
            "start_map_id",
            "end_map_id",
            "start_cell",
            "end_cell"
        )
    except get_possible_exceptions() as exc:
        return json.dumps(exc.response)

    path = get_path(
        map_info=assets.assets["map_info"],
        graph=assets.assets["pathfinder_graph"],
        start_map_id=values["start_map_id"],
        end_map_id=values["end_map_id"],
        start_cell=values["start_cell"],
        end_cell=values["end_cell"]
    )

    return json.dumps(path)


run(host='localhost', port=8080, debug=True)
