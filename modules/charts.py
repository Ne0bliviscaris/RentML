import altair as alt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from modules.data_processing import open_json_as_df


def show_chart(df, legend_column="Car type", trend_lines=None):
    """Create interactive visualization with flexible configuration."""
    tooltip_fields = config_tooltip(df)
    y_scale = calculate_chart_scale(df)
    chart = create_base_chart(df, legend_column, tooltip_fields, y_scale)

    if trend_lines:
        chart = add_lines_to_chart(chart, trend_lines)

    return chart


def read_and_format_json(json):
    """Load data from training dataset JSON file."""
    try:
        df = open_json_as_df(json)
        df["Date"] = pd.to_datetime(df["Date"])
        df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.strftime("%H:%M")
        df = df.sort_values("Date")
        return df
    except:
        return pd.DataFrame()


def create_base_chart(df, legend_column, tooltip_fields, y_scale=None):
    """Create base chart with styled data points."""
    base_chart = alt.Chart(df).encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("Mileage:Q", title="Mileage", scale=y_scale),
        tooltip=tooltip_fields,
    )

    point_colors = alt.Color(f"{legend_column}:N")
    legend = alt.selection_point(fields=[legend_column], bind="legend")
    visible = alt.value(1)
    hidden = alt.value(0.2)
    points_opacity = alt.condition(predicate=legend, if_true=visible, if_false=hidden)

    points = base_chart.mark_circle(size=200).encode(color=point_colors, opacity=points_opacity)
    chart = points.properties(width=800, height=400).add_params(legend)

    return chart


def config_tooltip(df, date=True, time=True, mileage=True, car_type=True, notes=True):
    """Create tooltip configuration showing available fields from dataframe."""
    tooltip_fields = []

    if "Date" in df.columns and date:
        tooltip_fields.append(alt.Tooltip("Date:T"))

    if "Time" in df.columns and time:
        tooltip_fields.append(alt.Tooltip("Time:O"))

    if "Mileage" in df.columns and mileage:
        tooltip_fields.append(alt.Tooltip("Mileage", format=" ,"))

    if "Car type" in df.columns and car_type:
        tooltip_fields.append(alt.Tooltip("Car type:N"))

    if "Notes" in df.columns and notes:
        tooltip_fields.append(alt.Tooltip("Notes:N"))

    return tooltip_fields


def calculate_chart_scale(df, mileage="Mileage"):
    """Calculate appropriate y-axis scale for chart based on data and optional trend."""
    y_min = df[mileage].min() * 0.95
    y_max = df[mileage].max() * 1.05
    return alt.Scale(domain=[y_min, y_max])


def add_lines_to_chart(chart, lines):
    """Add trend lines to the chart."""
    if not isinstance(lines, list):
        lines = [lines]

    for line in lines:
        chart = chart + line
    return chart


def filter_by_car(df, car_type=None, car_name=None):
    """Filter dataframe by car type or name."""
    if car_type:
        return df[df["Car type"] == car_type]
    if car_name:
        return df[df["Car"] == car_name]
    if car_type and car_name:
        return df[(df["Car type"] == car_type) & (df["Car"] == car_name)]
    return df


def regression_model() -> Pipeline:
    """Configure prediction model."""
    polynomial_features = PolynomialFeatures(degree=3)
    linear_regression = LinearRegression()
    return make_pipeline(polynomial_features, linear_regression)


def calculate_trend(df, color="red"):
    """Calculate polynomial trend and return trend line chart."""
    if df.empty:
        return df, None

    x = df["Date"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    y = df["Mileage"].values

    model = regression_model()
    model.fit(x, y)
    trend_values = model.predict(x)

    df["trend"] = trend_values
    trend_line = alt.Chart(df).mark_line(color=color).encode(x="Date:T", y="trend:Q")

    return df, trend_line
