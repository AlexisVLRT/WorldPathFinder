from datetime import datetime
from pathlib import Path


def log_request(request, status, processing_time):
    entry = format_entry(request, status, processing_time)
    log(entry)


def format_entry(request, status, processing_time):
    client_ip = request.environ.get('REMOTE_ADDR')
    parameters = {param: request.query.get(param) for param in list(request.query)}
    processing_time = round(processing_time, 3)
    return f"{datetime.now().isoformat()} | {client_ip} | {status} | {processing_time}s | Parameters: {parameters}\n"


def log(entry):
    with open(Path(__file__).parent.parent.parent / "logs" / "log", "a+") as log_file:
        log_file.write(entry)