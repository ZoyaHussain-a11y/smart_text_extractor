from flask import Blueprint, request, jsonify, send_file
from services.history_service import save_history
from PIL import Image
from io import BytesIO
from services.extract_service import extract_fields
import pytesseract
from datetime import datetime
import fitz  # PyMuPDF
from utils.auth import require_token
from utils.csv_export import export_to_csv

# Set Tesseract path for Windows
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path

extract_bp = Blueprint('extract', __name__, url_prefix='/extract')

@extract_bp.route('/', methods=['POST'])
@require_token
def extract_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Read file content directly from request
        file_content = file.read()
        
        # Get file extension
        file_extension = file.filename.lower().split('.')[-1]
        
        # Process PDF directly from memory
        if file_extension == 'pdf':
            try:
                doc = fitz.open(stream=file_content, filetype="pdf")
                pages = []
                
                for page_num, page in enumerate(doc):
                    text = page.get_text()
                    fields = extract_fields(text)
                    pages.append({
                        'page': page_num + 1,
                        'text': text,
                        'fields': fields
                    })
                
                doc.close()
                
                result = {
                    'file': file.filename,
                    'pages': pages,
                    'processed_at': datetime.now().isoformat()
                }
                
                save_history(file.filename, result)
                return jsonify(result), 200
                
            except Exception as e:
                return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 500
        
        # Process image using PIL
        elif file_extension in ['png', 'jpg', 'jpeg', 'tiff']:
            try:
                from io import BytesIO
                img = Image.open(BytesIO(file_content))
                text = pytesseract.image_to_string(img)
                fields = extract_fields(text)
                pages = [{
                    'page': 1,
                    'text': text,
                    'fields': fields
                }]
                
                result = {
                    'file': file.filename,
                    'pages': pages,
                    'processed_at': datetime.now().isoformat()
                }
                
                save_history(file.filename, result)
                return jsonify(result), 200
                
            except Exception as e:
                return jsonify({"error": f"Failed to process image: {str(e)}"}), 500
        
        else:
            return jsonify({"error": "Unsupported file type"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


