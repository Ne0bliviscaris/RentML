# v1.0
import json
import os

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageOps

import date_extract
import detect_car as detect
import export as export
import ocr
import preprocessing as pp  # Currently not used - needed for preprocessing
import view_plot as alt_plot


# File upload and image display via Streamlit
def load_image(uploaded_file) -> np.ndarray:
    """
    Load an image from a file, transpose it according to its EXIF orientation tag,
    display it in Streamlit, and return it as a NumPy array.

    Args:
        uploaded_file : The file to load the image from. This can be obtained from a Streamlit file_uploader widget.

    Returns:
        np.ndarray: The loaded image as a NumPy array.
    """
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)
    st.image(img, caption="Wybrane zdjęcie", use_column_width=True)
    return np.array(img)


# OCR and preprocessing - currently preprocessing is skipped
def process_image(img_cv: np.ndarray):
    """
    Process an image by performing OCR on it. Currently, preprocessing is skipped.
    To enable preprocessing, uncomment lines 50-53

    Args:
        img_cv (np.ndarray): The image to process.

    Returns:
        Tuple[np.ndarray, Optional[int]]: A tuple containing the processed image and the mileage
                                          recognized from the image. If the mileage is not recognized,
                                          the second element of the tuple is None.
    """
    preprocessed_img = img_cv  # Skip preprocessing for now using the original image
    # preprocessed_img = pp.preprocess(img_cv) # Uncomment to enable preprocessing
    # st.image( # Uncomment to display the preprocessed image
    #     preprocessed_img, caption="Zdjęcie po preprocessingu", use_column_width=True
    # )
    st.write("Przebieg z ocr:")
    mileage = ocr.mileage_ocr(preprocessed_img)  # Perform OCR on the image
    if mileage is None:
        st.write("Przebieg nie został rozpoznany")
    else:
        st.write(mileage)
    return preprocessed_img, mileage


# Extract data from file and append to JSON file
def extract_and_append_data(path, mileage, car_type, note=None):
    """
    Extract data from file and append it to JSON file.

    Args:
        path (str): The path of the file to extract data from.
        mileage (int): The mileage to append to the JSON file.
        car_type (str): The type of the car to append to the JSON file.
        note (str, optional): The note to append to the JSON file. Empty by default.

    Returns:
        Optional[str]: A message indicating that the file already exists in the JSON file,
                       if it does. Otherwise, None.
    """
    # Check if JSON file is empty
    if os.path.getsize("mileage.json") == 0:
        rep_check = []
    else:
        # Read the JSON file
        with open("mileage.json", "r") as f:
            rep_check = json.load(f)

    # Check if the file is already in the JSON file
    for entry in rep_check:
        if entry["Filename"] == path:
            return f"File {path} already exists."

    # Extract date and time from filename
    date, time = date_extract.extract_time_from_filename(path)
    export.append_to_json(
        "mileage.json",
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

    Args:
        path (str): The path of the file to find the associated record for.
    """
    with open("mileage.json", "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    st.write("Rekord powiązany ze zdjęciem:")
    record = df[df["Filename"] == path]
    st.write(record)
    # st.write("Wszystkie rekordy w pliku:")
    # st.dataframe(df)


# Streamlit app
# File uploader widget
uploaded_file = st.file_uploader("Wybierz plik", type=["jpg", "png"])

# Continue only if file is uploaded
if uploaded_file is not None:
    path = f"dataset\\ML_test\\{uploaded_file.name}"
    img_cv = load_image(uploaded_file)
    preprocessed_img, mileage = process_image(img_cv)
    car_type = detect.identify(img_path=path)
    extract_and_append_data(path, mileage, car_type)
    load_and_display_data(path)

# Generate and display an Altair chart
chart = alt_plot.prepare_plot()
if chart:
    st.altair_chart(chart)
