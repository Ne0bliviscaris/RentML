from datetime import datetime, timedelta

import altair as alt
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

import modules.charts as charts

st.set_page_config(layout="wide")


def show_chart(df, extrapolation_date):
    """Create interactive visualization with points and trend lines"""
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
    # Create and display visualization
    chart = charts.show_chart(df, legend_column="Car", trend_lines=trend_lines)
    st.altair_chart(chart, use_container_width=True)


def set_extrapolation_date():
    """Get extrapolation parameters from user input"""
    target_year = st.slider("Extrapolate to year", min_value=2024, max_value=2027, value=2025)
    target_date = datetime(target_year, 1, 1)
    return target_date


def main():
    """Main application flow for trend calculation and visualization"""
    df = charts.read_and_format_json()
    target_date = set_extrapolation_date()
    show_chart(df, target_date)


if __name__ == "__main__":
    main()
