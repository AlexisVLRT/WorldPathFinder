import json
import time

from bottle import route, run, request, HTTPResponse

from lib.api.entrypoint import Entrypoint
from lib.api.exceptions import ApiBaseException
from lib.api.logger import log_request


@route('/blackfalcon/get_path')
def main():
    start = time.time()
    try:
        status, result = entry_point.process_request(request)
    except ApiBaseException as exc:
        status, result = exc.status, exc.response

    response = HTTPResponse(status=status, body=json.dumps(result))
    log_request(request, status, time.time() - start)
    return response


allowed_parameters = ["start_map_id", "end_map_id", "start_cell", "end_cell"]
parameters_groups = [
    ("start_map_id", "end_map_id")
]
entry_point = Entrypoint(allowed_parameters, parameters_groups)

run(host="0.0.0.0", port=8080, server='gunicorn', workers=1)
