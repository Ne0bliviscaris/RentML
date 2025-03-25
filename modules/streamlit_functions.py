import os

import pandas as pd
import streamlit as st

from modules.cars import Car
from modules.data_processing import append_to_json, open_json_as_df
from modules.docs_generator import generate_handover_protocol
from modules.trends import predict_car


def uploader():
    # if st.button("Camera"):
    #     return st.camera_input("Take a photo")
    # if st.button("Upload image"):
    return st.file_uploader("Dodaj zdjęcie", type=["jpg", "png", "jpeg", "gif"])


def car_form_prediction(mileage, date, car_type=None):
    """Pre-fill car form with predicted car type."""
    if mileage is None or date is None:
        return None
    cars_data = open_json_as_df()
    return predict_car(mileage, date, cars_data, car_type)


def confirmation_form(data=None):
    """Display editable form with pre-filled mileage and car type."""
    mileage, car_type, date, time = data if data else (None, None, None, None)

    with st.form("Potwierdzenie danych", clear_on_submit=True, border=0):
        mileage = mileage_field(mileage)
        predicted_car = car_form_prediction(mileage, date, car_type)
        car_type = car_selector(car_type, predicted_car)
        date = date_field(date)
        time = time_field(time)
        notes = notes_field()
        st.write(predicted_car)

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Zapisz")
            if submitted:
                success = append_to_json(
                    file_path=None, mileage=mileage, car=car_type, date=date, time=time, note=notes
                )
                if success:
                    st.success("Zapisano dane")
                    st.session_state.form_submitted = True
                else:
                    st.warning("Dane istnieją już w bazie. Zaktualizowano notatkę.")

        with col2:
            handover = st.form_submit_button("Print Handover Protocol")
            if handover:
                protocol = generate_handover_protocol(mileage=mileage, car=car_type, date=date, time=time, note=notes)
                open_file(protocol)
                st.success("Protokół zwrotu wygenerowany")


def open_file(file_path):
    os.startfile(file_path)


def mileage_field(mileage):
    return st.number_input("Przebieg", min_value=0, max_value=999999, value=int(mileage) if mileage else 0, step=1)


def date_field(date_str):
    try:
        date = pd.to_datetime(date_str).date()
    except:
        date = pd.Timestamp.now().date()
    return st.date_input("Data", value=date)


def time_field(time_str):
    """Display editable time input field."""
    try:
        time = pd.to_datetime(time_str, format="%H:%M:%S").time()
    except:
        now = pd.Timestamp.now()
        time = pd.to_datetime(f"{now.hour}:{now.minute}:{now.second}", format="%H:%M:%S").time()
    return st.time_input("Godzina", value=time)


def notes_field():
    return st.text_area("Notatki", value="")


def first_car_of_type(car_type, all_cars):
    """Return first car of given type."""
    if car_type == "Osobowy":
        return next((i for i, car in enumerate(all_cars) if "Osobowy" in car.car_type), 0)
    elif car_type == "Dostawczy":
        return next((i for i, car in enumerate(all_cars) if "Dostawczy" in car.car_type), 0)
    else:
        return 0


def car_selector(predicted_car_type, predicted_car=None):
    """Display car type selector with default selection based on input value."""
    all_cars = Car.get_all_cars()
    cars_list = [car.name for car in all_cars]

    if predicted_car:
        default_index = next((i for i, car in enumerate(all_cars) if predicted_car in car.name), 0)
    else:
        default_index = first_car_of_type(predicted_car_type, all_cars)

    selected_name = st.selectbox("Samochód", options=cars_list, index=default_index)

    selected_car = next((car for car in all_cars if car.name == selected_name), all_cars[0])
    return selected_car
