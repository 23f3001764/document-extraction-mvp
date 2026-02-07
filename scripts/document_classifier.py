def detect_document_type(text):
    text_lower = text.lower()

    if "article" in text_lower and "constitution" in text_lower:
        return "constitution"

    if (
        "engineering mathematics" in text_lower
        or "unit i" in text_lower
        or "differential calculus" in text_lower
        or "example 1." in text_lower
        or "exercise 1.1" in text_lower
        or "mathematics" in text_lower
    ):
        return "math"

    if "bill" in text_lower and "kwh" in text_lower:
        return "electricity"

    return "unknown"