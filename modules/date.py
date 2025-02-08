import re
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS


def read_datetime(uploaded_image) -> tuple[str, str]:
    """Extract date and time from image metadata."""

    date, time = time_from_metadata(uploaded_image)

    if date is None or time is None:
        date, time = time_from_filename(uploaded_image.name)

    if date is None or time is None:
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")

    return str(date), str(time)


def time_from_filename(filename: str):
    """Extracts date from file name."""
    match = re.search(r"\d{8}_\d{6}", filename)
    if match:
        date_str = match.group()
        date = datetime.strptime(date_str, "%Y%m%d_%H%M%S").date().strftime("%Y-%m-%d")
        time = datetime.strptime(date_str, "%Y%m%d_%H%M%S").time().strftime("%H:%M:%S")
        return date, time
    else:
        return None, None


def time_from_metadata(uploaded_image):
    img = Image.open(uploaded_image)
    exif = img._getexif()
    if exif:
        for tag_id in exif:
            tag = TAGS.get(tag_id, tag_id)
            if tag in ["DateTimeOriginal", "DateTime"]:
                # Format: '2024:02:07 17:30:00'
                date_time = exif[tag_id]
                # Konwertuj na odpowiedni format
                date, time = date_time.split(" ")
                date = date.replace(":", "-")
                return date, time
    return None, None
