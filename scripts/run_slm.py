import json
from document_classifier import detect_document_type
from extractors import electricity, constitution, math_book

INPUT_TEXT = "../data/extracted_text/tata_power_bill/output.txt"
OUTPUT_JSON = "../data/extracted_text/tata_power_bill/output.json"

with open(INPUT_TEXT, "r", encoding="utf-8") as f:
    text = f.read()

doc_type = detect_document_type(text)

if doc_type == "electricity":
    extracted = electricity.extract(text)

elif doc_type == "constitution":
    extracted = constitution.extract(text)

elif doc_type == "math":
    extracted = math_book.extract(text)

else:
    extracted = {"error": "Unknown document type"}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(extracted, f, indent=4)

print(f"✅ Document type detected: {doc_type}")
print("✅ Extraction complete")