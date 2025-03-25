import altair as alt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from modules.data_processing import open_json_as_df
from modules.settings import JSON_FILE


def show_chart(df, legend_column="Car type", trend_lines=None):
    """Create interactive visualization with flexible configuration."""
    tooltip_fields = config_tooltip(df)
    y_scale = calculate_y_scale(df)
    chart = create_base_chart(df, legend_column, tooltip_fields, y_scale)

    if trend_lines:
        chart = add_lines_to_chart(chart, trend_lines)
    return chart


def read_and_format_json(json=JSON_FILE):
    """Load data from training dataset JSON file."""
    try:
        df = open_json_as_df(json)
        df["Date"] = pd.to_datetime(df["Date"])
        df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.strftime("%H:%M")
        df = df.sort_values("Date")
        return df
    except:
        return pd.DataFrame()


def configure_points(base_chart, legend_column):
    """Configure chart points with interactive legend selection"""
    legend = alt.selection_point(fields=[legend_column], bind="legend")
    point_colors = alt.Color(f"{legend_column}:N")
    visible = alt.value(1)
    hidden = alt.value(0.2)
    points_opacity = alt.condition(predicate=legend, if_true=visible, if_false=hidden)

    points = (
        base_chart.mark_circle(size=200)
        .encode(color=point_colors, opacity=points_opacity)
        .properties(width=800, height=400)
        .add_params(legend)
    )

    return points


def create_base_chart(df, legend_column, tooltip_fields, y_scale=None):
    """Create base chart with styled data points"""
    base_chart = alt.Chart(df).encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("Mileage:Q", title="Mileage", scale=y_scale),
        tooltip=tooltip_fields,
    )
    points = configure_points(base_chart, legend_column)
    return points


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


def calculate_y_scale(df, mileage="Mileage"):
    """Calculate appropriate y-axis scale for chart based on data and optional trend."""
    y_min = df[mileage].min() * 0.95
    y_max = df[mileage].max() * 1.05
    y_scale = alt.Scale(domain=[y_min, y_max])
    return y_scale


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


def prediction_model(x, y):
    """Create polynomial regression model."""
    polynomial_features = PolynomialFeatures(degree=3)
    linear_regression = LinearRegression()
    model = make_pipeline(polynomial_features, linear_regression)
    model.fit(x, y)
    return model


def predict_trend(df):
    """Predict trend for a specific car name."""
    trend_df = df.copy()
    x = df["Date"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    y = df["Mileage"].values

    model = prediction_model(x, y)
    trend_values = model.predict(x)

    trend_df["trend"] = trend_values
    return trend_df


def calculate_trend(df, target_date=None, color="red"):
    """Calculate polynomial trend and return trend line chart"""
    if df.empty:
        return df, None

    df_with_trend = predict_trend(df)

    extrapolation = target_date and target_date > df["Date"].max()
    if extrapolation:
        future_df = predict_future_trend(df, target_date)
        trend_line = create_trend_line(future_df, color)
    else:
        trend_line = create_trend_line(df_with_trend, color)

    return df_with_trend, trend_line


def predict_future_trend(df, target_date):
    """Generate predictions for dates up to target_date"""
    future_dates = pd.date_range(start=df["Date"].min(), end=target_date, freq="ME")
    future_df = pd.DataFrame({"Date": future_dates})

    future_x = future_df["Date"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    x = df["Date"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    y = df["Mileage"].values

    model = prediction_model(x, y)
    future_df["trend"] = model.predict(future_x)

    return future_df


def create_trend_line(df, color):
    """Create Altair line chart from dataframe with trend column"""
    return alt.Chart(df).mark_line(color=color).encode(x="Date:T", y="trend:Q")
