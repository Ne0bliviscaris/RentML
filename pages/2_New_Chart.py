import altair as alt
import pandas as pd
import streamlit as st

from modules.settings import JSON_FILE

st.set_page_config(layout="wide")


def open_json(file):
    try:
        json_data = pd.read_json(file)
    except:
        json_data = pd.DataFrame()
    return json_data


def show_chart():
    """Display chart with car mileage data."""
    json = open_json(JSON_FILE)
    if json.empty:
        st.warning("No data to display")
        return
    json["Date"] = pd.to_datetime(json["Date"]).dt.strftime("%Y-%m-%d")
    json["Time"] = pd.to_datetime(json["Time"]).dt.strftime("%H:%M:%S")
    json = json.sort_values("Date")

    min_y = json["Mileage"].min()
    max_y = json["Mileage"].max()
    chart_scale = [min_y, max_y]

    points = (
        alt.Chart(json)
        .mark_point()
        .encode(x="Date:T", y=alt.Y("Mileage:Q", scale=alt.Scale(domain=chart_scale)), color="Car:N")
    )

    chart = (
        alt.Chart(json)
        .mark_line()
        .encode(x="Date:T", y=alt.Y("Mileage:Q", scale=alt.Scale(domain=chart_scale)), color="Car:N")
    )

    chart = chart + points
    st.altair_chart(chart.properties(width=800, height=400), use_container_width=True)


def main():
    st.title("New Chart")
    show_chart()


main()
