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
def load_and_transform_data(json_file="mileage.json") -> pd.DataFrame:
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

    # Convert 'Date' column to datetime format
    df["Date"] = pd.to_datetime(df["Date"])

    # Remove square brackets and quotation marks from 'Mileage' column
    df["Mileage"] = df["Mileage"].apply(
        lambda x: x.replace("[", "").replace("]", "").replace("'", "")
    )

    # Convert 'Mileage' column to numeric format
    df["Mileage"] = df["Mileage"].astype(int)

    return df


# Extract 3 groups from DataFrame
def extract_groups(df) -> tuple:
    """
    Divide initial DataFrame 2 groups based on car type - truck or car.
    Truck group is further divided into 2 subgroups based on their mileage.

    The function performs the following steps:
    - Calculates the linear trend of the 'Mileage' over 'Date'
    - Calculates the distance of each point from the trend line
    - Divides distances into 2 groups using K-Means
    - Extracts groups based on the K-Means result
    - Extracts subgroups from truck group based on the 'Type' column

    Args:
        df (DataFrame): The input DataFrame.

    Returns:
        tuple: A tuple containing the extracted groups (car, l3h2, l4h2) and the modified DataFrame.
    """
    # Calculate linear trend
    x = df["Date"].map(dt.datetime.toordinal).values.reshape(-1, 1)
    y = df["Mileage"].values
    model = LinearRegression().fit(x, y)
    trend = model.predict(x)

    # Calculate the distance of each point from the trend line
    distances = np.abs(y - trend)

    # Divide distances into 2 groups using K-Means
    kmeans = KMeans(n_clusters=2, random_state=0).fit(distances.reshape(-1, 1))
    df["group"] = kmeans.labels_

    # Extract groups
    group1 = df[df["group"] == 0]
    l3h2 = df[df["group"] == 1]

    # Extract subgroups from group 1 based on the 'Type' column
    car = group1[group1["Type"] == "car"]
    l4h2 = group1[group1["Type"] == "truck"]

    return car, l3h2, l4h2, df


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


# Create Altair chart
def altair_chart(df) -> alt.Chart:
    """
    Create an Altair chart from the DataFrame.

    The function creates a scatter plot with circles as markers. The x-axis represents the 'Date' and the y-axis represents the 'Mileage'.
    The color of the circles is determined by the 'class' column. The tooltip shows the 'Date', 'Mileage' and 'class' of the data points.

    Args:
        df (DataFrame): The input DataFrame.

    Returns:
        alt.Chart: The created Altair chart.
    """
    chart = (
        alt.Chart(df)
        .mark_circle(size=100)
        .encode(
            x="Date:T",
            y=alt.Y(
                "Mileage:Q",
                scale=alt.Scale(domain=(240000, max(5000 + df["Mileage"]))),
            ),
            color="class:N",
            tooltip=["Date", "Mileage", "class"],
        )
        .properties(width=720)  # , height=400)  # Adjust chart size
    )

    return chart


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
    filtered_df = df[
        df["class"].isin(
            [c for c, selected in zip(classes, selected_classes) if selected]
        )
    ]
    return filtered_df


# Main function - prepare plot with Altair library for Streamlit
def prepare_plot() -> alt.Chart:
    """
    Prepare an Altair chart from the data.

    The function performs the following steps:
    - Loads and transforms data from a JSON file
    - Extracts 3 groups from the DataFrame
    - Creates a 'class' column in the DataFrame
    - Displays checkboxes for each unique class in the DataFrame and filters the DataFrame based on the selected checkboxes
    - If the filtered DataFrame is not empty, creates an Altair chart from the DataFrame

    Returns:
        alt.Chart: The created Altair chart. If the filtered DataFrame is empty, a message "No data selected" is displayed instead.
    """
    df = load_and_transform_data()
    if df.empty:
        return st.write("No data")

    df, car, l3h2, l4h2 = extract_groups(df)
    new_df = create_class_column(df, car, l3h2, l4h2)
    filtered_df = display_checkboxes(new_df)

    if filtered_df.empty:
        return st.write("No data")
    else:
        return altair_chart(filtered_df)
