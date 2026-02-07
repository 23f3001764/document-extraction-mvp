import os
import json

from extract_pdf import extract_text_from_pdf
from document_classifier import detect_document_type
from extractors import electricity, constitution, math_book

RAW_PDF_DIR = "../data/raw_pdfs"
OUTPUT_DIR = "../data/extracted_text"

for pdf_file in os.listdir(RAW_PDF_DIR):
    if not pdf_file.lower().endswith(".pdf"):
        continue

    pdf_name = os.path.splitext(pdf_file)[0]
    pdf_path = os.path.join(RAW_PDF_DIR, pdf_file)
    pdf_output_dir = os.path.join(OUTPUT_DIR, pdf_name)

    print(f"\n📄 Processing: {pdf_file}")

    # Step 1: OCR
    text_path = extract_text_from_pdf(pdf_path, pdf_output_dir)

    with open(text_path, "r", encoding="utf-8") as f:
        ocr_text = f.read()

    # Step 2: Detect document type
    doc_type = detect_document_type(ocr_text)
    print(f"➡️ Detected document type: {doc_type}")

    # Step 3: Extract structured data
    if doc_type == "electricity":
        structured_data = electricity.extract(ocr_text)

    elif doc_type == "constitution":
        structured_data = constitution.extract(ocr_text)

    elif doc_type == "math":
        structured_data = math_book.extract(ocr_text)

    else:
        structured_data = {"error": "Unknown document type"}

    # Step 4: Save JSON
    output_json_path = os.path.join(pdf_output_dir, "output.json")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=4)

    print(f"✅ JSON saved: {output_json_path}")

print("\n🎉 All PDFs processed successfully")