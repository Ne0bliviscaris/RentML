# v1.01 - Append data to a JSON file
import json
from typing import Dict, List, Optional


def append_to_json(
    filename: str, data: List[Dict], notes: Optional[str] = None
) -> None:
    """
    Append data to a JSON file with an option to add notes.

    If the file does not exist or cannot be decoded, it is treated as empty.
    Lists in the 'Mileage' column are converted to strings.
    If notes are provided, they are added to each data item.

    Args:
        filename (str): The name of the JSON file.
        data (List[Dict]): The data to append.
        notes (Optional[str]): The notes to add. Defaults to None.
    """
    try:
        with open(filename, "r") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    for item in data:
        if isinstance(item.get("Mileage"), list):
            item["Mileage"] = ", ".join(map(str, item["Mileage"]))
        if notes:
            item["Notes"] = notes

    existing_data.extend(data)

    with open(filename, "w") as f:
        json.dump(existing_data, f)
