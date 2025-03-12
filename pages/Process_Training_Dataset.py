import json
import os
import shutil

import streamlit as st

from modules.data_processing import extract_data
from modules.settings import MULTI_READ, TRAINING_DATASET, UNREADABLE

TRAINING_JSON = "modules\\data\\training_dataset.json"


def process_training_dataset() -> None:
    """Process all training images with data extraction and error handling."""
    files = list_dataset_files()
    create_error_folders()

    progress_bar = st.progress(0)
    total_files = len(files)

    for index, rel_path in enumerate(files):
        process_single_image(rel_path, index, total_files, progress_bar)


def process_single_image(rel_path, index, total_files, progress_bar):
    """Process one image file and update progress."""
    file_path = os.path.join(TRAINING_DATASET, rel_path)

    mileage, car_type, date, time = extract_data(file_path)
    display_extraction_results(mileage, car_type, date, time)

    if not is_special_case(mileage, rel_path):
        process_valid_data(file_path, date, time, mileage, car_type)

    update_progress(rel_path, index, total_files, progress_bar)


def display_extraction_results(mileage, car_type, date, time):
    """Show extraction results to user."""
    st.toast(f"Extracted data: \n\nMileage: {mileage}\nCar type: {car_type}\nDate: {date}\nTime: {time}")


def is_special_case(mileage, rel_path):
    """Handle unreadable and multi-read cases."""
    if not mileage:
        copy_to_error_folder(rel_path, UNREADABLE)
        return True

    if isinstance(mileage, list) and len(mileage) > 1:
        copy_to_error_folder(rel_path, MULTI_READ)
        return True

    return False


def copy_to_error_folder(rel_path, target_folder):
    """Copy file to appropriate error folder."""
    source = os.path.join(TRAINING_DATASET, rel_path)
    target = os.path.join(target_folder, os.path.basename(rel_path))
    shutil.copy(source, target)


def process_valid_data(file_path, date, time, mileage, car_type):
    """Process data with valid mileage and car type."""
    mileage = mileage[0] if isinstance(mileage, list) else mileage
    record = {
        "Filename": file_path,
        "Date": str(date),
        "Time": str(time),
        "Mileage": mileage,
        "Car type": car_type,
        "Car": "",
        "Notes": "Training Dataset",
    }

    data = load_training_json()
    if not is_duplicate(data, record):
        data.append(record)
        save_training_json(data)


def is_duplicate(data, new_record):
    """Check if record already exists in dataset based on date and time."""
    return any(records["Date"] == new_record["Date"] and records["Time"] == new_record["Time"] for records in data)


def update_progress(rel_path, index, total_files, progress_bar):
    """Update progress indicators."""
    progress_bar.progress((index + 1) / total_files)
    st.write(f"Processed image: {rel_path}, {index+1}/{total_files}")


def list_dataset_files():
    """Get all image files recursively from the training dataset and its subdirectories."""
    filenames = []

    for root, _, files in os.walk(TRAINING_DATASET):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                rel_path = os.path.relpath(file_path, TRAINING_DATASET)
                filenames.append(rel_path)
    return filenames


def load_training_json():
    """Load training JSON file or return empty list."""
    try:
        with open(TRAINING_JSON, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_training_json(data):
    """Save data to training JSON file."""
    os.makedirs(os.path.dirname(TRAINING_JSON), exist_ok=True)
    with open(TRAINING_JSON, "w") as f:
        json.dump(data, f, indent=2)


def create_error_folders():
    """Create folders for problem files if they don't exist."""
    os.makedirs(UNREADABLE, exist_ok=True)
    os.makedirs(MULTI_READ, exist_ok=True)


st.title("Training Dataset Processing")
col1, col2 = st.columns(2)
with col1:
    if st.button("Process Training Dataset"):
        process_training_dataset()
with col2:
    if st.button("List Dataset Files"):
        st.write(list_dataset_files())

if os.path.exists(TRAINING_JSON):
    if st.button("View Training Data"):
        training_data = load_training_json()
        st.write(f"Records: {len(training_data)}")
        st.dataframe(training_data)
