import json
from pathlib import Path

with open(Path(__file__).parent.parent / "secrets" / "credentials.json", "r") as f:
    credentials = json.load(f)
