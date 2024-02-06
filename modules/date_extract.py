# v1.01 - Date and time extraction from picture
import re
from datetime import datetime


def extract_time_from_filename(filename: str):
    """
    Returns a datetime object based on the filename.

    The filename should contain a date and time in the 'YYYYMMDD_HHMMSS' format.
    The date and time should be separated by an underscore.
    If the filename does not contain a date and time in the required format, the function returns "Unreadable date".

    Args:
        filename (str): The filename to process.

    Returns:
        datetime.datetime or str: A datetime object representing the date and time from the filename, or "Unreadable date" if the date and time cannot be extracted.
    """
    match = re.search(r"\d{8}_\d{6}", filename)
    if match:
        date_str = match.group()
        date = datetime.strptime(date_str, "%Y%m%d_%H%M%S").date().strftime("%Y-%m-%d")
        time = datetime.strptime(date_str, "%Y%m%d_%H%M%S").time().strftime("%H:%M:%S")
        return date, time
    else:
        print(f"Cannot extract date from filename: {filename}")
        return None, None


# Future improvement: a function to extract date and time from image metadata - for real time data extraction from phone camera images
