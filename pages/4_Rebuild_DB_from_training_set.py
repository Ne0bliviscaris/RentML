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

from modules.settings import JSON_FILE, TRAINING_JSON

st.set_page_config(layout="wide")
st.title("Rebuilding Database from Training Set")


def load_training_data():
    """Load data from training dataset JSON file."""
    try:
        with open(TRAINING_JSON, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])
        df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.time
        df = df.sort_values("Date")
        return df
    except (FileNotFoundError, json.JSONDecodeError):
        st.error("Error loading training data. File does not exist or is empty.")
        return pd.DataFrame()


def calculate_trend(df, car_type="Dostawczy", degree=3):
    """Calculate polynomial trend line for specified car type."""
    filtered_df = df[df["Car type"] == car_type]
    x = filtered_df["Date"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    y = filtered_df["Mileage"].values

    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(x, y)
    trend = model.predict(x)

    return filtered_df, trend, model


def cluster_by_distance_from_trend(df, trend):
    """Divide dataframe into clusters based on distance from trend."""
    mileage = df["Mileage"].values
    distance_from_trend = np.abs(mileage - trend).reshape(-1, 1)
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


def visualize(df, legend_column="Car type", trend_column=None):
    """Create interactive visualization with flexible configuration."""

    mileage = "Mileage"
    y_min = df[mileage].min() * 0.95
    y_max = df[mileage].max() * 1.05
    y_scale = alt.Scale(domain=[y_min, y_max])

    date = alt.Tooltip("Date:T")
    formatted_mileage = alt.Tooltip(mileage, format=" ,")
    car_type = alt.Tooltip(f"{legend_column}:N")
    tooltip_fields = [date, formatted_mileage, car_type]

    if "Notes" in df.columns:
        notes = alt.Tooltip("Notes:N")
        tooltip_fields.append(notes)

    base_chart = alt.Chart(df).encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y(f"{mileage}:Q", title=mileage, scale=y_scale),
        tooltip=tooltip_fields,
    )

    point_colors = alt.Color(f"{legend_column}:N")
    legend = alt.selection_point(fields=[legend_column], bind="legend")
    visible = alt.value(1)
    hidden = alt.value(0.2)
    points_opacity = alt.condition(predicate=legend, if_true=visible, if_false=hidden)

    points = base_chart.mark_circle(size=200).encode(color=point_colors, opacity=points_opacity)
    chart = points.properties(width=800, height=400).add_params(legend)

    if trend_column:
        trend_values = alt.Y(f"{trend_column}:Q")
        trend_line = base_chart.mark_line(color="red").encode(y=trend_values)
        chart = chart + trend_line

    return chart


def save_processed_data(df):
    """Save processed data to JSON file."""
    result = []
    for _, row in df.iterrows():
        record = {
            "Filename": row.get("Filename", ""),
            "Date": row["Date"].strftime("%Y-%m-%d"),
            "Time": row["Time"].strftime("%H:%M:%S"),
            "Mileage": int(row["Mileage"]),
            "Type": row["Car type"],
            "Car": row["Car"],
            "Notes": row.get("Notes", ""),
        }
        result.append(record)

    try:
        os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)
        with open(JSON_FILE, "w") as f:
            json.dump(result, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False


def step_1_load_data():
    """Load and visualize data with car type colors."""
    st.header("1. Load training data")
    df = load_training_data()
    if df.empty:
        st.warning("No training data to process.")
        return pd.DataFrame()

    st.write(f"Loaded {len(df)} records.")
    st.dataframe(df.head())

    chart = visualize(df)
    st.altair_chart(chart, use_container_width=True)

    return df


def step_2_calculate_trend(df):
    """Calculate trend line for truck vehicles only."""
    st.header("2. Calculate trend line (truck vehicles only)")

    truck_df, trend, model = calculate_trend(df, "Dostawczy")

    if truck_df.empty:
        st.warning("No truck vehicles found to calculate trend.")
        return None, None, None

    df_with_trend = truck_df.copy()
    df_with_trend["trend"] = trend
    chart = visualize(df_with_trend, legend_column="Car type", trend_column="trend")

    st.altair_chart(chart, use_container_width=True)
    return truck_df, trend


def step_3_cluster_data(truck_df, trend):
    """Cluster truck vehicles by distance from trend line."""
    st.header("3. Cluster truck vehicles by distance from trend")

    if truck_df.empty:
        st.warning("No truck vehicles found for clustering.")
        return truck_df

    df_clustered = cluster_by_distance_from_trend(truck_df.copy(), trend)
    chart = visualize(df_clustered, legend_column="group")

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

    chart = visualize(df_classified, legend_column="Car")
    st.altair_chart(chart, use_container_width=True)

    return df_classified


def step_5_save_data(df_classified):
    """Save processed data to file."""
    st.header("5. Save processed data")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save data to JSON file"):
            if save_processed_data(df_classified):
                st.success(f"Data saved to {JSON_FILE}")
                st.balloons()

    with col2:
        st.download_button(
            label="Download as JSON",
            data=json.dumps(
                [
                    {
                        "Filename": row.get("Filename", ""),
                        "Date": str(row["Date"].date()),
                        "Time": str(row.get("Time", "")),
                        "Mileage": int(row["Mileage"]),
                        "Type": row["Car type"],
                        "Car": row["Car"],
                        "Notes": row.get("Notes", ""),
                    }
                    for _, row in df_classified.iterrows()
                ],
                indent=2,
            ),
            file_name="classified_vehicles.json",
            mime="application/json",
        )


def main():
    """Process training data step by step with visualizations."""
    df = step_1_load_data()
    if not df.empty:
        truck_df, trend = step_2_calculate_trend(df)
        if truck_df is not None:
            df_clustered = step_3_cluster_data(truck_df, trend)
            df_classified = step_4_identify_vehicle_types(df, df_clustered)
            step_5_save_data(df_classified)


if __name__ == "__main__":
    main()
