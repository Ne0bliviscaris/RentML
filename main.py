# v1.01 - main streamlit application
import os
import subprocess

import streamlit as st

from modules.data_processing import extract_data
from modules.streamlit_functions import confirmation_form, uploader
from modules.view_plot import show_altair_chart

st.set_page_config(page_title="Car Mileage Analysis", page_icon="🚗")


def image_processing():
    """Left column handles image upload and preview."""
    st.session_state.image = uploader()

    if st.session_state.image:
        st.image(st.session_state.image, use_column_width=True)
        # preprocessed_img = preprocess(img)  #Potential image preprocessing here
        if not st.session_state.image_processed:
            st.session_state.extracted_data = extract_data(st.session_state.image)
            st.session_state.image_processed = True


def main():
    if "image" not in st.session_state:
        st.session_state.image = None
    if "image_processed" not in st.session_state:
        st.session_state.image_processed = False
    if "extracted_data" not in st.session_state:
        st.session_state.extracted_data = None

    left_col, right_col = st.columns(2)

    with left_col:
        image_processing()

    with right_col:
        confirmation_form(st.session_state.extracted_data)

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
