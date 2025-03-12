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


def cluster_by_distance(df, trend):
    """Divide dataframe into clusters based on distance from trend."""
    mileage = df["Mileage"].values
    distance = np.abs(mileage - trend)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(distance.reshape(-1, 1))
    df["group"] = kmeans.labels_
    return df


def identify_car(df, clustered_df):
    """Identify car subtypes based on clustering results."""
    result_df = df.copy()
    result_df["Car"] = "Scudo"

    # Set L3H2 and L4H2 for trucks based on cluster groups
    group_0 = clustered_df[clustered_df["group"] == 0].index
    group_1 = clustered_df[clustered_df["group"] == 1].index

    result_df.loc[group_0, "Car"] = "L4H2"
    result_df.loc[group_1, "Car"] = "L3H2"

    return result_df


def visualize_by_type(df, type_column="Car type"):
    """Create visualization with car types."""
    selection = alt.selection_point(fields=[type_column], bind="legend")

    chart = (
        alt.Chart(df)
        .mark_circle(size=60)
        .encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y(
                "Mileage:Q",
                title="Mileage",
                scale=alt.Scale(domain=[df["Mileage"].min() * 0.95, df["Mileage"].max() * 1.05]),
            ),
            color=alt.Color(f"{type_column}:N", legend=alt.Legend(title="Car Type")),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
            tooltip=["Date", "Mileage", type_column],
        )
        .properties(width=800, height=400)
        .add_params(selection)
    )

    return chart


def save_processed_data(df):
    """Save processed data to JSON file."""
    result = []
    for _, row in df.iterrows():
        record = {
            "Filename": row.get("Filename", ""),
            "Date": str(row["Date"].date()),
            "Time": str(row.get("Time", "")),
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


def main():
    """Process training data step by step with visualizations."""

    def step_1_load_data():
        """Load and visualize data with car type colors."""
        st.header("1. Load training data")
        df = load_training_data()
        if df.empty:
            st.warning("No training data to process.")
            return pd.DataFrame()

        st.write(f"Loaded {len(df)} records.")
        st.dataframe(df.head())

        chart = visualize_by_type(df)
        st.altair_chart(chart, use_container_width=True)

        return df

    def step_2_calculate_trend():
        """Calculate trend line for truck vehicles only."""
        st.header("2. Calculate trend line (truck vehicles only)")

        truck_df, trend, model = calculate_trend(df, "Dostawczy")

        if truck_df.empty:
            st.warning("No truck vehicles found to calculate trend.")
            return None, None, None

        df_with_trend = truck_df.copy()
        df_with_trend["trend"] = trend

        y_domain = [df_with_trend["Mileage"].min() * 0.95, df_with_trend["Mileage"].max() * 1.05]

        trend_line = (
            alt.Chart(df_with_trend)
            .mark_line(color="red")
            .encode(
                x=alt.X("Date:T", title="Date"), y=alt.Y("trend:Q", title="Mileage", scale=alt.Scale(domain=y_domain))
            )
        )

        data_points = (
            alt.Chart(df_with_trend)
            .mark_circle()
            .encode(x="Date:T", y=alt.Y("Mileage:Q", scale=alt.Scale(domain=y_domain)), tooltip=["Date", "Mileage"])
        )

        trend_chart = trend_line + data_points

        st.altair_chart(trend_chart, use_container_width=True)
        return truck_df, trend, model

    def step_3_cluster_data(truck_df):
        """Cluster truck vehicles by distance from trend line."""
        st.header("3. Cluster truck vehicles by distance from trend")

        if truck_df.empty:
            st.warning("No truck vehicles found for clustering.")
            return df

        df_clustered = cluster_by_distance(truck_df.copy(), trend)

        cluster_chart = (
            alt.Chart(df_clustered)
            .mark_circle()
            .encode(
                x="Date:T",
                y=alt.Y(
                    "Mileage:Q",
                    title="Mileage",
                    scale=alt.Scale(
                        domain=[df_clustered["Mileage"].min() * 0.95, df_clustered["Mileage"].max() * 1.05]
                    ),
                ),
                color="group:N",
                tooltip=["Date", "Mileage", "group"],
            )
        )

        st.altair_chart(cluster_chart, use_container_width=True)
        return df_clustered

    def step_4_identify_vehicle_types():
        """Identify vehicle subtypes based on clustering results."""
        st.header("4. Vehicle type identification")

        df_classified = identify_car(df, df_clustered)

        personal = df_classified[df_classified["Car type"] == "Osobowy"]
        l3h2 = df_classified[df_classified["Car"] == "L3H2"]
        l4h2 = df_classified[df_classified["Car"] == "L4H2"]

        st.write(f"Osobowy (Scudo): {len(personal)} records")
        st.write(f"Dostawczy L3H2: {len(l3h2)} records")
        st.write(f"Dostawczy L4H2: {len(l4h2)} records")

        vehicle_chart = visualize_by_type(df_classified, "Car")
        st.altair_chart(vehicle_chart, use_container_width=True)

        return df_classified

    def step_5_save_data():
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

    df = step_1_load_data()
    if not df.empty:
        truck_df, trend, model = step_2_calculate_trend()
        if truck_df is not None:
            df_clustered = step_3_cluster_data(truck_df)
            df_classified = step_4_identify_vehicle_types()
            step_5_save_data()


if __name__ == "__main__":
    main()
