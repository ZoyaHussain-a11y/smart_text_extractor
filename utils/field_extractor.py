import re

def extract_fields(text):
    fields = {}

    # Sample regex patterns (customize these as needed)
    invoice_number = re.search(r'Invoice\s*No[:\s]*([A-Za-z0-9\-]+)', text, re.IGNORECASE)
    total = re.search(r'Total[:\s]*([\w\s]+[\d,]+\.?\d*)', text, re.IGNORECASE)
    date = re.search(r'Date[:\s]*(\d{2,4}[-/]\d{1,2}[-/]\d{1,4})', text, re.IGNORECASE)

    if invoice_number:
        fields['invoice_number'] = invoice_number.group(1)
    if total:
        fields['total'] = total.group(1)
    if date:
        fields['date'] = date.group(1)

    return fields
