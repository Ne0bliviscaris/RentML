import altair as alt
import pandas as pd

from modules.data_processing import open_json_as_df


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
