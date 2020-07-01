from lib.api.exceptions import get_possible_exceptions
from lib.api.input_processing import sanitize
from lib.api.throttler import Throttler
from lib.assets_management.assets_manager import Assets
from lib.path import get_path


class Entrypoint:
    def __init__(self, allowed_parameters, parameters_groups):
        self.allowed_parameters = allowed_parameters
        self.parameters_groups = parameters_groups
        self.throttler = Throttler()
        self.assets = Assets.instance()

    def process_request(self, request):
        try:
            self.throttler.throttle(request)
            sanitized_values = self._sanitize_inputs(request)
        except get_possible_exceptions() as exc:
            return exc.status, exc.response

        return 200, self._make_path(sanitized_values)

    def _sanitize_inputs(self, request):
        return sanitize(
            request.query,
            self.parameters_groups,
            *self.allowed_parameters
        )

    def _make_path(self, sanitized_values):
        return get_path(
            map_info=self.assets.assets["map_info"],
            graph=self.assets.assets["pathfinder_graph"],
            **sanitized_values
        )