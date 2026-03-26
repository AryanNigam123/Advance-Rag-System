import fitz  # PyMuPDF
from pathlib import Path

def load_pdf(pdf_path: str):
    """
    Loads a PDF file and returns a PyMuPDF document object.
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    return doc
