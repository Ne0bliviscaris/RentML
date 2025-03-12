import pandas as pd
import streamlit as st

from modules.settings import JSON_FILE


def load_json():
    """Load JSON file and return it as a DataFrame."""
    try:
        return pd.read_json(JSON_FILE)
    except (FileNotFoundError, ValueError):
        return pd.DataFrame()


new_json = load_json()
st.altair_chart(new_json) if not new_json.empty else st.write("No data to display.")
