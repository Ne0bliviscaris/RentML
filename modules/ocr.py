# v1.0
import re

import easyocr


def mileage_ocr(img):
    """
    Performs Optical Character Recognition (OCR) on an image to extract 6-digit numbers, typically representing mileage.

    The function uses the EasyOCR library to read text from the image. It then uses regular expressions to find all 6-digit numbers in the text.
    If no 6-digit numbers are found, the function returns the string "unreadable".

    Args:
        img (str or PIL.Image.Image): The image to perform OCR on. This can be a string representing the path to the image, or a PIL Image object.

    Returns:
        list or str: A list of strings representing the 6-digit numbers found in the image. If no 6-digit numbers are found, returns the string "unreadable".
    """
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
