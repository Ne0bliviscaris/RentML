import json

import modules.detection_model as detect
import modules.ocr as ocr
from modules.date import read_datetime


def extract_data(image) -> list[int, str]:
    if image is not None:
        mileage = read_mileage(image)
        car_type = detect.identify_car(image)
        date, time = read_datetime(image)
        return [mileage, car_type, date, time]


def read_mileage(img):
    """Perform OCR on image."""
    mileage = ocr.mileage_ocr(img)
    return mileage[0] if mileage is not None else None


def open_json():
    """Read JSON file or return empty list."""
    try:
        with open("modules\\data\\mileage.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_json(data):
    """Save data to JSON file."""
    try:
        with open("modules\\data\\mileage.json", "w") as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False


def is_duplicate(data, new_record):
    """Check if record already exists in database."""
    for duplicate_index, record in enumerate(data):
        if (
            record["Date"] == new_record["Date"]
            and record["Mileage"] == new_record["Mileage"]
            and record["Car type"] == new_record["Car type"]
        ):
            return duplicate_index
    return False


def append_to_json(file_path=None, date=None, time=None, mileage=None, car_type=None, note=None):
    """Extract data from file and append it to JSON file."""
    # Check if JSON file is empty
    record = {
        "Filename": file_path,
        "Date": str(date),
        "Time": str(time),
        "Mileage": mileage,
        "Car type": car_type,
        "Notes": note or "",
    }

    data = open_json()
    if not data:
        data = [record]

    duplicate = is_duplicate(data, record)
    if duplicate is not False:
        existing_note = data[duplicate]["Notes"]
        new_note = record["Notes"]

        if existing_note and new_note:
            data[duplicate]["Notes"] = f"{existing_note}\n{new_note}"
        elif new_note:
            data[duplicate]["Notes"] = new_note
    else:
        data.append(record)

    return save_json(data)
