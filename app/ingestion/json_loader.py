import json
from pathlib import Path

def load_json(file_path: str) -> list | dict:
    """
    Load JSON data from a file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
