# cvapp/utils/pdf_parser.py

import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_bytes

def extract_text_from_pdf(file):
    try:
        # Primero intentamos extraer texto directamente con PyMuPDF
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        if text.strip():
            return text
    except Exception:
        pass

    # Si no se pudo extraer texto, volvemos al principio del archivo y usamos OCR
    file.seek(0)
    images = convert_from_bytes(file.read())
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text
