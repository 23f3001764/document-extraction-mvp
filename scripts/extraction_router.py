from scripts.extractors import electricity, math_book
from scripts.extractors.slm_extractor import extract_with_slm

def extract_data(text, doc_type, mode):
    """
    mode: 'Variant C' or 'Variant B'
    """

    if mode == "Variant C":
        if doc_type == "Electricity Bill":
            return electricity.extract(text)
        elif doc_type == "Math Book":
            return math_book.extract(text)

    elif mode == "Variant B":
        return extract_with_slm(text, doc_type)

    raise ValueError("Unsupported extraction mode or document type")