import time

from lib.api.exceptions import TooManyRequests


class Throttler:
    def __init__(self):
        self.request_log = {}
        self.secs_between_requests = 5

    def throttle(self, request):
        client_ip = request.environ.get("REMOTE_ADDR")
        if client_ip in self.request_log and self._request_is_too_soon(client_ip):
            raise TooManyRequests
        self._log_request(client_ip)

    def _request_is_too_soon(self, client_ip):
        return time.time() - self.request_log[client_ip] < self.secs_between_requests

    def _log_request(self, client_ip):
        self.request_log[client_ip] = time.time()