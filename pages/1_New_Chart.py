import streamlit as st

from modules.charts import show_chart
from modules.data_processing import open_json_as_df
from modules.settings import JSON_FILE

st.set_page_config(layout="wide")


def main():
    st.title("New Chart")
    json = open_json_as_df(JSON_FILE)
    if json.empty:
        st.warning("No data to display")
        return
    chart = show_chart(json, legend_column="Car")
    st.altair_chart(chart, use_container_width=True)


main()
