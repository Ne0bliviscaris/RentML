import re

import pandas as pd


def read_datetime(uploaded_image) -> tuple[str, str]:
    """Extract date and time from image metadata."""
    date, time = time_from_filename(uploaded_image)

    if date is None or time is None:
        timestamp = pd.Timestamp.now()
        today = timestamp.strftime("%Y-%m-%d")
        now = timestamp.strftime("%H:%M:%S")

        date, time = today, now

    return date, time


def time_from_filename(filename: str):
    """Extracts date from file name."""
    DATE = r"\d{8}"  # 8 digits
    TIME = r"\d{6}"  # 6 digits

    match = re.search(rf"{DATE}_{TIME}", filename)
    if match:
        date_str = match.group()
        timestamp = pd.to_datetime(date_str, format="%Y%m%d_%H%M%S")
        date = timestamp.strftime("%Y-%m-%d")
        time = timestamp.strftime("%H:%M:%S")
        return date, time
    else:
        return None, None
