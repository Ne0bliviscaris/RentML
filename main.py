# v1.01 - main streamlit app
import streamlit as st
from PIL import Image

import modules.date_extract as date_extract
import modules.detect_car as detect
import modules.export as export
import modules.ocr as ocr
import modules.streamlit_functions as sf
import modules.view_plot as alt_plot

# Streamlit app
# File uploader widget
uploaded_file = st.file_uploader("Wybierz plik", type=["jpg", "png"])

# Continue only if file is uploaded
if uploaded_file is not None:
    path = f"data\\main-dataset\\{uploaded_file.name}"
    img_cv = sf.load_image(uploaded_file)
    preprocessed_img, mileage = sf.process_image(img_cv)
    car_type = detect.identify(img_path=path)
    sf.extract_and_append_data(path, mileage, car_type)
    sf.load_and_display_data(path)

# Generate and display an Altair chart
chart = alt_plot.prepare_plot()
if chart:
    st.altair_chart(chart)
