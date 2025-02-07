# v1.01 - main streamlit application functions
import json
import os

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageOps

import modules.date_extract as date_extract
import modules.export as export
import modules.ocr as ocr
import modules.preprocessing as pp  # Currently not used - needed for preprocessing


# File upload and image display via Streamlit
def load_image(uploaded_file):
    """Load an image from a file, and return it as a NumPy array."""
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)
    st.image(img, caption="Wybrane zdjęcie", use_column_width=True)
    return np.array(img)


# OCR and preprocessing - currently preprocessing is skipped
def extract_mileage(img):
    """Perform OCR on image."""
    st.write("OCR Mileage:")
    mileage = ocr.mileage_ocr(img)
    if mileage is None:
        st.write("Mileage not recognized")
    else:
        st.write(mileage[0])
    return mileage[0] if mileage is not None else None


# Extract data from file and append to JSON file
def extract_and_append_data(path, mileage, car_type, note=None):
    """Extract data from file and append it to JSON file."""
    # Check if JSON file is empty
    if os.path.getsize("data/result/mileage.json") == 0:
        rep_check = []
    else:
        # Read the JSON file
        with open("data/result/mileage.json", "r") as f:
            rep_check = json.load(f)

    # Check if the file is already in the JSON file
    for entry in rep_check:
        if entry["Filename"] == path:
            return f"File {path} already exists."

    # Extract date and time from filename
    date, time = date_extract.extract_time_from_filename(path)
    export.append_to_json(
        "data/result/mileage.json",
        [
            {
                "Filename": path,
                "Date": date,
                "Time": time,
                "Mileage": str(mileage),
                "Type": car_type,
                "Notes": note,
            }
        ],
    )


# Load and display data from JSON file in Streamlit as a DataFrame
def load_and_display_data(path: str) -> None:
    """
    Load data from a JSON file, display the record associated with a specific path in Streamlit,
    Optionally display all records in the JSON file in Streamlit as a DataFrame. (currently commented out)
    """
    with open("data/result/mileage.json", "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    st.write("Rekord powiązany ze zdjęciem:")
    record = df[df["Filename"] == path]
    st.write(record)
    # st.write("Wszystkie rekordy w pliku:")
    # st.dataframe(df)
