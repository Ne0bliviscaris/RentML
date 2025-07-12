import re

import easyocr


def mileage_ocr(img):
    """Return first 6-digit number from OCR or None."""
    ocr = easyocr.Reader(["en"], gpu=True)
    img_bytes = img.read()
    ocr_result = ocr.readtext(img_bytes, allowlist="0123456789")

    SIX_DIGITS = r"\b\d{6}\b"
    six_digit_numbers = re.findall(SIX_DIGITS, str(ocr_result))

    return six_digit_numbers[0] if six_digit_numbers else None
