from pathlib import Path
import fitz


def extract_text(pdf_path: Path) -> str:
    #Confirm that file exists and is a pdf file
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, received: {pdf_path.name}")


    try:
        with fitz.open(pdf_path) as document:
            page_texts: list[str] = []

            for page in document:
                page_text = page.get_text("text")
                page_texts.append(page_text)

    except fitz.FileDataError as error:
        message = f"Could not read PDF: {pdf_path}"
        raise ValueError(message)

    full_text = "\n\n".join(page_texts)
    return full_text
