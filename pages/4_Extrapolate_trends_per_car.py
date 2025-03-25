from datetime import datetime

import streamlit as st

import modules.charts as charts
from modules.trends import predict_car

st.set_page_config(layout="wide")


def calculate_trend_lines(df, extrapolation_date):
    """Calculate trend lines for each car type and model"""
    scudo = charts.filter_by_car(df, car_type="Osobowy")
    l3h2 = charts.filter_by_car(df, car_name="L3H2")
    l4h2 = charts.filter_by_car(df, car_name="L4H2")

    scudo, scudo_trend = charts.calculate_trend(scudo, extrapolation_date, "pink")
    l3h2, l3h2_trend = charts.calculate_trend(l3h2, extrapolation_date, "cyan")
    l4h2, l4h2_trend = charts.calculate_trend(l4h2, extrapolation_date, "blue")

    trend_lines = [
        scudo_trend,
        l3h2_trend,
        l4h2_trend,
    ]

    return trend_lines


def show_extrapolated_chart(df, extrapolation_date):
    """Create interactive visualization with points and trend lines"""
    trend_lines = calculate_trend_lines(df, extrapolation_date)
    chart = charts.show_chart(df, legend_column="Car", trend_lines=trend_lines)
    st.altair_chart(chart, use_container_width=True)


def set_extrapolation_date():
    """Get extrapolation parameters from user input"""
    target_year = st.slider("Extrapolate to year", min_value=2024, max_value=2027, value=2025)
    target_date = datetime(target_year, 1, 1)
    return target_date


def show_car_prediction(df):
    """Show interface for car prediction based on mileage and date"""
    st.subheader("Predict car based on mileage and date")

    col1, col2 = st.columns(2)
    with col1:
        mileage = st.number_input("Mileage", min_value=0, value=50000)
        prediction_date = st.date_input("Date")

    with col2:
        car_type = st.selectbox("Car type (optional)", options=["All"] + list(df["Car type"].unique()))
        car_type = None if car_type == "All" else car_type

    if st.button("Predict car"):
        predicted_car = predict_car(mileage, prediction_date, df, car_type)
        st.success(f"Predicted car: {predicted_car}")


def main():
    """Main application flow for trend calculation and visualization"""
    df = charts.read_and_format_json()
    target_date = set_extrapolation_date()

    show_extrapolated_chart(df, target_date)
    show_car_prediction(df)


if __name__ == "__main__":
    main()
