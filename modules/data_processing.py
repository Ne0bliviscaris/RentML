import json

import pandas as pd

import modules.detection_model as detection_model
import modules.ocr as ocr
from modules.date import read_datetime
from modules.settings import JSON_FILE


def open_json_as_df(file):
    try:
        json = pd.read_json(file)
    except:
        json = pd.DataFrame()
    return json


def extract_data(image) -> list[int, str]:
    """Extract data from image."""
    filename = image.name

    mileage = read_mileage(image)
    car_type = detection_model.identify_car(image)
    date, time = read_datetime(filename)
    return [mileage, car_type, date, time]


def read_mileage(img):
    """Perform OCR on image."""
    mileage = ocr.mileage_ocr(img)
    return mileage[0] if mileage is not None else None


def open_json():
    """Read JSON file or return empty list."""
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_json(data):
    """Save data to JSON file."""
    try:
        with open(JSON_FILE, "w") as file:
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
            and record["Car"] == new_record["Car"]
        ):
            return duplicate_index
    return False


def append_to_json(file_path=None, date=None, time=None, mileage=None, car=None, note=None):
    """Extract data from file and append it to JSON file."""
    record = {
        "Filename": file_path,
        "Date": str(date),
        "Time": str(time),
        "Mileage": mileage,
        "Type": car.car_type,
        "Car": car.name,
        "Notes": note or "",
    }

    data = open_json()
    if not data:
        data = [record]

    duplicate = is_duplicate(data, record)
    if duplicate:
        merge_notes(data, duplicate, record)
    else:
        data.append(record)

    return save_json(data)


def merge_notes(data, duplicate, record):
    """Merge notes from duplicate records."""
    existing_note = data[duplicate]["Notes"]
    new_note = record["Notes"]

    if existing_note and new_note:
        data[duplicate]["Notes"] = f"{existing_note}\n{new_note}"
    elif new_note:
        data[duplicate]["Notes"] = new_note
