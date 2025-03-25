# from docx import Document
from docxtpl import DocxTemplate

from modules.settings import HANDOVER_TEMPLATE_PATH, OUTPUT_PATH


def generate_handover_protocol(mileage=None, car=None, date=None, time=None, note=None):
    """Generate a handover protocol from template with provided car details."""
    OUTPUT_FILE = f"{date} {car.model}.docx"

    formatted_date = date.strftime("%d.%m.%Y") if date else ""
    formatted_time = time.strftime("%H:%M") if time else ""

    doc = DocxTemplate(HANDOVER_TEMPLATE_PATH)

    protocol_content = {
        "car": car.model,
        "registration": car.registration,
        "mileage": f"               {str(mileage)}               "
        or "....................................................",
        "date": f"          {formatted_date}          "
        or "...........................................................................",
        "time": f"          {formatted_time}          " or "...............................",
        "note": (
            note
            or """…………………………………………………………………………………………....................................................................................................
…………………………………………………………………………………………...................................................................................................."""
        ),
    }

    doc.render(protocol_content)
    doc.save(OUTPUT_PATH + OUTPUT_FILE)
    return OUTPUT_PATH + OUTPUT_FILE
