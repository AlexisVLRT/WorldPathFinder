import json
import time

from bottle import route, run, request, HTTPResponse

from lib.api.entrypoint import Entrypoint
from lib.api.exceptions import ApiBaseException
from lib.api.logger import log_request
import config


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


entry_point = Entrypoint(config.ALLOWED_PARAMETERS, config.PARAMETERS_GROUPS)

run(host="0.0.0.0", port=80, server='gunicorn', workers=1)
