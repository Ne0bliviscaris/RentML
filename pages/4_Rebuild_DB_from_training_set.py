import json
import os

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

import modules.charts as charts
from modules.settings import JSON_FILE, TRAINING_JSON

st.set_page_config(layout="wide")
st.title("Rebuilding Database from Training Set")


def cluster_by_distance_from_trend(df):
    """Divide dataframe into clusters based on distance from trend."""
    distance_from_trend = np.abs(df["Mileage"] - df["trend"]).values.reshape(-1, 1)
    kmeans = KMeans(n_clusters=2, random_state=0)
    cluster_labels = kmeans.fit_predict(distance_from_trend)
    df["group"] = cluster_labels
    return df


def identify_car(df, clustered_df):
    """Identify car subtypes based on clustering results."""
    df["Car"] = "Scudo"

    cluster = clustered_df["group"]
    l4h2 = clustered_df[cluster == 0].index
    l3h2 = clustered_df[cluster == 1].index

    df.loc[l4h2, "Car"] = "L4H2"
    df.loc[l3h2, "Car"] = "L3H2"

    return df


def calculate_trend(df, color="red"):
    """Calculate polynomial trend and return trend line chart."""
    x = df["Date"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    y = df["Mileage"].values

    model = make_pipeline(PolynomialFeatures(degree=3), LinearRegression())
    model.fit(x, y)
    trend_values = model.predict(x)

    df["trend"] = trend_values
    trend_line = alt.Chart(df).mark_line(color=color).encode(x="Date:T", y="trend:Q")

    return df, trend_line


def save_data_to_json(df, target_file=JSON_FILE):
    """Save processed data to JSON file."""
    try:
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
        df["Time"] = pd.to_datetime(df["Time"]).dt.strftime("%H:%M")
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        df.to_json(target_file, orient="records", indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False


def step_1_load_data():
    """Load and visualize data with car type colors."""
    st.header("1. Load training data")
    df = charts.read_and_format_json(TRAINING_JSON)
    if df.empty:
        st.warning("No training data to load.")
        return pd.DataFrame()

    st.write(f"Loaded {len(df)} records.")
    st.dataframe(df.head())

    chart = charts.show_chart(df)
    st.altair_chart(chart, use_container_width=True)

    return df


def step_2_calculate_trend(df):
    """Calculate trend line for truck vehicles only."""
    st.header("2. Calculate trend line (truck vehicles only)")

    truck_df = charts.filter_by_car(df, car_type="Dostawczy")
    if truck_df.empty:
        st.warning("No vehicles found to calculate trend.")
        return pd.DataFrame()

    truck_df_with_trend, trend_line = calculate_trend(truck_df)

    chart = charts.show_chart(truck_df, legend_column="Car type", trend_lines=trend_line)
    st.altair_chart(chart, use_container_width=True)

    return truck_df_with_trend


def step_3_cluster_data(truck_df):
    """Cluster truck vehicles by distance from trend line."""
    st.header("3. Cluster truck vehicles by distance from trend")

    if truck_df.empty:
        st.warning("No truck vehicles found for clustering.")
        return truck_df

    df_clustered = cluster_by_distance_from_trend(truck_df)
    chart = charts.show_chart(df_clustered, legend_column="group")

    st.altair_chart(chart, use_container_width=True)
    return df_clustered


def step_4_identify_vehicle_types(df, df_clustered):
    """Identify vehicle subtypes based on clustering results."""
    st.header("4. Vehicle type identification")

    df_classified = identify_car(df, df_clustered)

    scudo = df_classified[df_classified["Car type"] == "Osobowy"]
    car_name = df_classified["Car"]
    l3h2 = df_classified[car_name == "L3H2"]
    l4h2 = df_classified[car_name == "L4H2"]

    st.write(f"Osobowy Scudo: {len(scudo)} records")
    st.write(f"Dostawczy L3H2: {len(l3h2)} records")
    st.write(f"Dostawczy L4H2: {len(l4h2)} records")

    chart = charts.show_chart(df_classified, legend_column="Car")
    st.altair_chart(chart, use_container_width=True)

    return df_classified


def step_5_save_data(df_classified):
    """Save processed data to file."""
    st.header("5. Save processed data")

    if st.button("Save data to JSON file"):
        if save_data_to_json(df_classified):
            st.success(f"Data saved to {JSON_FILE}")
            st.balloons()


def main():
    """Process training data step by step with visualizations."""
    df = step_1_load_data()
    if not df.empty:
        truck_df_with_trend = step_2_calculate_trend(df)
        if not truck_df_with_trend.empty:
            df_clustered = step_3_cluster_data(truck_df_with_trend)
            df_classified = step_4_identify_vehicle_types(df, df_clustered)
            step_5_save_data(df_classified)


if __name__ == "__main__":
    main()
