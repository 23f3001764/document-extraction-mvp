import os
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    pages = convert_from_path(pdf_path, dpi=300)
    full_text = ""

    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page, config="--oem 3 --psm 6")
        full_text += f"\n\n--- PAGE {i+1} ---\n\n{text}"

    text_output_path = os.path.join(output_dir, "output.txt")
    with open(text_output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    return text_output_path