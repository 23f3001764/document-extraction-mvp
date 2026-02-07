import re

def extract(text):
    records = []

    # Light cleanup
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    # ---------------------------------
    # Extract PARTS (PART I, PART II, etc.)
    part_pattern = list(re.finditer(
        r"(PART\s+[IVXLC]+)\s+([A-Z\s\-]+)",
        text
    ))

    parts = []
    for i, part in enumerate(part_pattern):
        part_start = part.start()
        part_end = part_pattern[i + 1].start() if i + 1 < len(part_pattern) else len(text)

        parts.append({
            "part_id": part.group(1),
            "part_title": part.group(2).strip(),
            "content": text[part_start:part_end]
        })

    # ---------------------------------
    # Extract ARTICLES within each PART
    article_regex = re.compile(
        r"(\d+[A-Z]?)\.\s+([A-Z][^—\.\n]+)[—\-\.]\s*(.*?)(?=\d+[A-Z]?\.\s+[A-Z]|$)",
        re.IGNORECASE
    )

    for part in parts:
        for match in article_regex.finditer(part["content"]):
            records.append({
                "document_type": "constitution",
                "part": part["part_id"],
                "part_title": part["part_title"],
                "article_number": match.group(1),
                "article_title": match.group(2).strip(),
                "article_text": match.group(3).strip()[:1500]  # limit size
            })

    return records
