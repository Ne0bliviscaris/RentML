# v1.01 - main streamlit application
import os
import subprocess

import streamlit as st

from modules.data_processing import extract_data
from modules.streamlit_functions import confirmation_form, uploader
from modules.view_plot import show_altair_chart

st.set_page_config(page_title="Car Mileage Analysis", page_icon="🚗")


def left_column():
    """Left column handles image upload and preview."""
    img = uploader()
    if img:
        st.image(img, use_column_width=True)
        # preprocessed_img = preprocess(img)  #Potential image preprocessing here
        data = extract_data(img)
        return data


def main():
    left_col, right_col = st.columns(2)

    with left_col:
        data = left_column()

    with right_col:
        if data is not None:
            confirmation_form(data)

    # show_altair_chart()


if __name__ == "__main__":
    if not os.environ.get("RUNNING"):
        # Mark streamlit as running
        os.environ["RUNNING"] = "1"
        # Get file path
        file_path = os.path.abspath(__file__)
        # Run streamlit in a new process
        subprocess.run(f"streamlit run {file_path}")
    else:
        main()
