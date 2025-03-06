# v1.01 - Mileage extraction using EasyOCR
import re

import easyocr
import numpy as np
from PIL import Image, ImageOps


def mileage_ocr(img):
    """
    Performs Optical Character Recognition (OCR) on an image to extract 6-digit numbers, typically representing mileage.
    EasyOCR uses np.array as input.
    """
    img_array = load_image_as_array(img)

    # Create a reader to perform OCR
    reader = easyocr.Reader(["en"], gpu=True)

    # Read all text from image
    result = reader.readtext(img_array, allowlist="0123456789")

    # Find all 6-digit numbers
    six_digit_numbers = re.findall(r"\b\d{6}\b", str(result))

    # If no 6-digit number found, return empty variable
    if not six_digit_numbers:

        return None

    # Return the list of 6-digit numbers as integers
    return list(map(int, six_digit_numbers))


def load_image_as_array(uploaded_file):
    """Load an image from a file, and return it as a NumPy array."""
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)
    return np.array(img)
