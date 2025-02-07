# v1.01 - main streamlit application
import os
import subprocess

import streamlit as st

import modules.detect_car as detect
import modules.streamlit_functions as sf
import modules.view_plot as alt_plot

# st.set_page_config(page_title="Car Mileage Analysis", page_icon="🚗", layout="wide")


def uploader():
    # if st.button("Camera"):
    #     return st.camera_input("Take a photo")
    # if st.button("Upload image"):
    return st.file_uploader("Select image", type=["jpg", "png", "jpeg", "gif"])


def show_chart():
    chart = alt_plot.prepare_plot()
    if chart:
        st.altair_chart(chart)


def extract_data(image):
    if image is not None:
        mileage = sf.extract_mileage(image)
        car_type = detect.identify_car(image)
        return [mileage, car_type]


def upload_form():
    col1, col2 = st.columns(2)

    with col1:
        st.write("Upload image")
        uploaded_img = uploader()
        data = extract_data(uploaded_img)

    with col2:
        if data is not None:
            st.write(data)
            confirmation_form(data)
            if st.button("Confirm"):
                # sf.extract_and_append_data(uploaded_img.name, data[0], data[1])
                st.write(data[0], data[1])


def confirmation_form(data):
    pass


# # Deprecated
def process_file(image):
    path = f"data\\main-dataset\\{image.name}"
    numpy_img = sf.load_image(image)
    mileage = sf.extract_mileage(numpy_img)
    car_type = detect.identify_car(image)
    sf.extract_and_append_data(path, mileage, car_type)
    sf.load_and_display_data(path)


def main():
    # upload_form()

    uploaded_img = uploader()

    if uploaded_img is not None:
        process_file(uploaded_img)

    show_chart()


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
