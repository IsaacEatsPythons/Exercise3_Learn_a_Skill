from src.extractor import extract_fields
from src.pdf_reader import extract_text


def parse_datasheet(pdf_path):
    text = extract_text(pdf_path)
    extracted_fields = extract_fields(text)

    return extracted_fields
