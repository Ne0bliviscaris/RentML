import re
from datetime import datetime

import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS


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
    match = re.search(r"\d{8}_\d{6}", filename)
    if match:
        date_str = match.group()
        timestamp = pd.to_datetime(date_str, format="%Y%m%d_%H%M%S")
        date = timestamp.strftime("%Y-%m-%d")
        time = timestamp.strftime("%H:%M:%S")
        return date, time
    else:
        return None, None
