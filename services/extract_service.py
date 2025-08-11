import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from datetime import datetime
import re
from flask import current_app

# Set Tesseract path for Windows
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path

from utils.field_guesser import get_field_guesser

def extract_fields(text):
    """Extract fields using AI-based heuristics"""
    # Get the field guesser instance
    field_guesser = get_field_guesser()
    
    # Get all possible field matches
    matches = field_guesser.guess_fields(text)
    
    # Process matches to get the most likely values
    fields = {}
    
    # Process each field type
    for field_name, values in matches.items():
        if not values:
            continue
            
        # Choose the most likely value
        # For numbers/amounts, choose the largest value
        if field_name in ['amount', 'total', 'invoice_number']:
            try:
                # Try to convert to float and get the largest
                numeric_values = [float(re.sub(r'[^0-9.]', '', v)) for v in values if v]
                if numeric_values:
                    fields[field_name] = str(max(numeric_values))
            except:
                # If conversion fails, use the first value
                fields[field_name] = values[0]
                
        # For dates, choose the most recent date
        elif field_name == 'date':
            try:
                # Try to parse dates and get the most recent
                from dateutil import parser
                dates = []
                for v in values:
                    try:
                        date = parser.parse(v)
                        dates.append((date, v))
                    except:
                        continue
                if dates:
                    fields[field_name] = max(dates)[1]
            except:
                # If parsing fails, use the first value
                fields[field_name] = values[0]
                
        # For other fields, use the first value
        else:
            fields[field_name] = values[0]
            
    return fields

def process_file(file):
    """
    Processes an uploaded file (PDF or image):
    - Saves it to disk
    - Extracts text using appropriate method (PyMuPDF for PDF, Tesseract for images)
    - Extracts common fields using regex patterns
    - Returns structured output
    """
    # Make sure upload folder exists
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)

    # Save uploaded file to UPLOAD_FOLDER
    # Use absolute path to ensure proper file access
    upload_folder = os.path.abspath(upload_folder)
    os.makedirs(upload_folder, exist_ok=True)
    
    # Use secure filename to prevent path traversal attacks
    from werkzeug.utils import secure_filename
    safe_filename = secure_filename(file.filename)
    
    # Save file with a temporary name first
    temp_file_path = os.path.join(upload_folder, f"temp_{safe_filename}")
    file.save(temp_file_path)
    
    # Move the file to its final location
    file_path = os.path.join(upload_folder, safe_filename)
    try:
        os.replace(temp_file_path, file_path)
    except Exception as e:
        # If replace fails, try renaming
        try:
            os.rename(temp_file_path, file_path)
        except Exception as e:
            raise Exception(f"Failed to move file: {str(e)}")

    try:
        # Determine file type
        file_extension = file.filename.lower().split('.')[-1]
        
        # Process PDF
        if file_extension == 'pdf':
            # Try to open the file with different methods
            try:
                # First try direct file path
                doc = fitz.open(file_path)
            except Exception as e:
                # If that fails, try reading file content directly
                try:
                    with open(file_path, 'rb') as f:
                        pdf_content = f.read()
                    doc = fitz.open(stream=pdf_content, filetype="pdf")
                except Exception as e:
                    raise Exception(f"Failed to read PDF file: {str(e)}")
            
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
            
        # Process image
        elif file_extension in ['png', 'jpg', 'jpeg', 'tiff']:
            try:
                # First try direct file path
                img = Image.open(file_path)
            except Exception as e:
                # If that fails, try reading file content directly
                try:
                    with open(file_path, 'rb') as f:
                        img = Image.open(f)
                except Exception as e:
                    raise Exception(f"Failed to read image file: {str(e)}")
            
            text = pytesseract.image_to_string(img)
            fields = extract_fields(text)
            pages = [{
                'page': 1,
                'text': text,
                'fields': fields
            }]
        
        else:
            raise ValueError("Unsupported file type")

        result = {
            'file': file.filename,
            'pages': pages,
            'processed_at': datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        # Return error as a dictionary instead of tuple
        error_result = {
            'error': str(e),
            'file': file.filename,
            'processed_at': datetime.now().isoformat()
        }
        
        # Try to clean up any temporary files
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
        
        return error_result
    return {"filename": file.filename, "extracted_text": text}
