import re

def extract(text):
    data = {
        "document_type": "electricity",
        "consumer_name": None,
        "meter_id": None,
        "bill_date": None,
        "billing_period": None,
        "kwh": None,
        "amount_payable": None,
        "zone": None,
        "tariff_category": None,
        "location": None
    }

    text = " ".join(text.split())

    meter_match = re.search(r"CA\s*NO\.?\s*[:\-]?\s*(\d{8,})", text, re.IGNORECASE)
    if meter_match:
        data["meter_id"] = meter_match.group(1)

    bill_date_match = re.search(r"Bill\s*Date\s*[\+\:]?\s*(\d{2}/\d{2}/\d{4})", text)
    if bill_date_match:
        data["bill_date"] = bill_date_match.group(1)

    period_match = re.search(
        r"Bill\s*Period\s*(\d{2}/\d{2}/\d{4}\s*to\s*\d{2}/\d{2}/\d{4})",
        text
    )
    if period_match:
        data["billing_period"] = period_match.group(1)

    kwh_matches = re.findall(r"(\d+)\s*kWh", text, re.IGNORECASE)
    if kwh_matches:
        data["kwh"] = int(kwh_matches[-1])

    amount_match = re.search(
        r"Net\s*Amount\s*Payab\w*\s*[:\-]?\s*([\d,]+\.\d{2})",
        text,
        re.IGNORECASE
    )
    if amount_match:
        data["amount_payable"] = float(amount_match.group(1).replace(",", ""))

    if "delhi" in text.lower():
        data["location"] = "Delhi"

    return data