ALLOWED_PARAMETERS = ["start_map_id", "end_map_id", "start_cell", "end_cell"]
PARAMETERS_GROUPS = [
    ("start_map_id", "end_map_id")
]
MIN_TIME_BETWEEN_REQUESTS = 0  # Set to 0 to disable throttling
REQUIRED_ASSETS = ["map_info", "pathfinder_graph"]
