import pdfplumber

def extract_text_from_pdf(pdf_path):
    pages_data = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                pages_data.append({
                    "page": i + 1,
                    "text": text.strip() if text else ""
                })
    except Exception as e:
        print(f"[PDF Parser] Error: {e}")
    return pages_data
