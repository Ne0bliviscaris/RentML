# v1.01 - Mileage extraction using EasyOCR
import re

import easyocr

import modules.streamlit_functions as sf


def mileage_ocr(img):
    """
    Performs Optical Character Recognition (OCR) on an image to extract 6-digit numbers, typically representing mileage.
    EasyOCR uses np.array as input.
    """
    img = sf.load_image(img)

    # Create a reader to perform OCR
    reader = easyocr.Reader(["en"], gpu=True)

    # Read all text from image
    result = reader.readtext(img, allowlist="0123456789")

    # Find all 6-digit numbers
    six_digit_numbers = re.findall(r"\b\d{6}\b", str(result))

    # If no 6-digit number found, return empty variable
    if not six_digit_numbers:

        return None

    # Return the list of 6-digit numbers as integers
    return list(map(int, six_digit_numbers))
