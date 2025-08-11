from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return [{
            "page": 1,
            "text": text.strip()
        }]
    except Exception as e:
        print(f"[Image Parser] Error: {e}")
        return []
