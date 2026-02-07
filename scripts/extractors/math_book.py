import re

def extract(text):
    records = []

    # Clean OCR noise slightly
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    # -------------------------------
    # Detect UNIT (e.g., Unit I. Differential Calculus-I)
    unit_matches = list(re.finditer(
        r"Unit\s+([IVX]+)\.?\s*([A-Za-z\s\-]+)",
        text,
        re.IGNORECASE
    ))

    # If no units found, still continue
    units = []
    for match in unit_matches:
        units.append({
            "unit_id": match.group(1),
            "unit_name": match.group(2).strip()
        })

    # -------------------------------
    # Detect SECTIONS (numbered headings)
    section_matches = list(re.finditer(
        r"\d+\.\d*\s*([A-Z][A-Za-z\s’\-]+)",
        text
    ))

    sections = [m.group(1).strip() for m in section_matches]

    # -------------------------------
    # Detect EXAMPLES (very important for math books)
    example_matches = re.finditer(
        r"Example\s+(\d+)\.\s*(.+?)(?=Example\s+\d+\.|EXERCISE|$)",
        text,
        re.IGNORECASE
    )

    for match in example_matches:
        records.append({
            "document_type": "math",
            "unit": units[0]["unit_name"] if units else None,
            "section": sections[0] if sections else None,
            "example_number": match.group(1),
            "example_title": match.group(2).strip()[:200]  # limit size
        })

    return records