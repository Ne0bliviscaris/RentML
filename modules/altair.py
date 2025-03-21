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
