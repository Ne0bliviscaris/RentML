# Module to prepare interactive Altair plot for Streamlit
import datetime as dt
import json
import os

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression


# Load and transform data in DataFrame
def load_and_transform_data(json_file="data/result/mileage.json") -> pd.DataFrame:
    """
    Load data from a JSON file and transform it into a DataFrame.

    The function performs the following transformations:
    - Converts the 'Date' column to datetime format
    - Removes square brackets and quotation marks from the 'Mileage' column
    - Converts the 'Mileage' column to numeric format

    Returns:
        DataFrame: The transformed data.
    """
    if not os.path.exists(json_file):
        return pd.DataFrame()

    with open(json_file, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Load data from JSON file
    df = pd.read_json(json_file)

    df["Date"] = pd.to_datetime(df["Date"])
    # Remove square brackets and quotation marks from 'Mileage' column
    df["Mileage"] = df["Mileage"].apply(lambda x: x.replace("[", "").replace("]", "").replace("'", ""))
    df["Mileage"] = df["Mileage"].astype(int)

    return df


# Extract 3 groups from DataFrame
def extract_groups(df) -> tuple:
    """
    Divide initial DataFrame 2 groups based on car type - truck or car.
    Truck group is further divided into 2 subgroups based on their mileage.
    """
    mileage = df["Mileage"].values

    trend = regression_line(df)

    distance_from_trend = np.abs(mileage - trend)

    # Divide distances into 2 groups using K-Means
    kmeans = KMeans(n_clusters=2, random_state=0).fit(distance_from_trend.reshape(-1, 1))
    df["group"] = kmeans.labels_

    group = df[df["group"] == 0]

    l4h2 = df[df["group"] == 1]
    car = group[group["Type"] == "car"]
    l3h2 = group[group["Type"] == "truck"]

    return car, l3h2, l4h2, df


def regression_line(df):
    """Draw a linear regression model from the DataFrame."""
    x = df["Date"].map(dt.datetime.toordinal).values.reshape(-1, 1)
    y = df["Mileage"].values
    model = LinearRegression().fit(x, y)
    trend = model.predict(x)
    return trend


# Assign records to one of 3 classes
def create_class_column(car, l3h2, l4h2, df):
    """
    Assign records to one of 3 classes and create a new 'class' column in the DataFrame.

    The function performs the following steps:
    - Removes the 'Type' column
    - Creates a new column 'class' and assigns 'unknown' to all records
    - Classifies records with known 'Type' as 'Car', 'L3H2' or 'L4H2'

    Args:
        car (DataFrame): DataFrame containing records of type 'Car'.
        l3h2 (DataFrame): DataFrame containing records of type 'L3H2'.
        l4h2 (DataFrame): DataFrame containing records of type 'L4H2'.
        df (DataFrame): The input DataFrame.

    Returns:
        DataFrame: The modified DataFrame with the new 'class' column.
    """
    # Remove 'Type' column
    df = df.drop(columns=["Type"])

    # Create new column 'class' and assign 'unknown' to all records
    df["class"] = "unknown"

    # Classify records with known 'Type' as 'Car', 'L3H2' or 'L4H2'
    df.loc[df.index.isin(car.index), "class"] = "Car"
    df.loc[df.index.isin(l4h2.index), "class"] = "L4H2"
    df.loc[df.index.isin(l3h2.index), "class"] = "L3H2"

    return df


def altair_chart(df) -> alt.Chart:
    """Create an Altair chart from the DataFrame with error handling."""
    try:
        base = alt.Chart(df).properties(width=720)

        chart = base.mark_circle(size=100).encode(
            x=alt.X("Date:T"),
            y=alt.Y("Mileage:Q", scale=alt.Scale(domain=[240000, df["Mileage"].max() + 5000])),
            color="class:N",
            tooltip=["Date", "Mileage", "class"],
        )

        return chart

    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None


# Create checkboxes for each class with pre-selected class
def display_checkboxes(df, pre_selected_class=None):
    """
    Display checkboxes for each car class in the DataFrame and filter the DataFrame based on the selected checkboxes.

    The function performs the following steps:
    - Retrieves the unique classes from the 'class' column
    - Displays a checkbox for each class. If a pre_selected_class is provided, only this checkbox is pre-selected
    - Filters the DataFrame to include only the records of the selected classes

    Args:
        df (DataFrame): The input DataFrame.
        pre_selected_class (str, optional): The class to be pre-selected. If None, all classes are pre-selected. Defaults to None.

    Returns:
        DataFrame: The filtered DataFrame.
    """
    classes = df["class"].unique()
    if pre_selected_class is None:
        selected_classes = [st.checkbox(c, True) for c in classes]
    else:
        selected_classes = [st.checkbox(c, c == pre_selected_class) for c in classes]
    filtered_df = df[df["class"].isin([c for c, selected in zip(classes, selected_classes) if selected])]
    return filtered_df


# Main function - prepare plot with Altair library for Streamlit
def prepare_plot():
    """Prepare an Altair chart from the data with error handling."""
    try:
        df = load_and_transform_data()
        if df.empty:
            return st.write("No data")

        df, car, l3h2, l4h2 = extract_groups(df)
        new_df = create_class_column(df, car, l3h2, l4h2)
        filtered_df = display_checkboxes(new_df)

        if filtered_df.empty:
            return st.write("No data selected")

        chart = altair_chart(filtered_df)
        if chart is not None:
            return chart
        return st.write("Error creating chart")

    except Exception as e:
        st.error(f"Error in prepare_plot: {str(e)}")
        return None


def show_altair_chart():
    chart = prepare_plot()
    if chart:
        st.altair_chart(chart)
