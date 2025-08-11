# Smart Text Extractor API

A RESTful API that extracts text and key fields from PDFs and scanned images using OCR technology.

## Features

- Extract text from PDFs and scanned images
- Detect and extract common fields (invoice number, date, total amount)
- Support for multi-page PDFs
- File processing history
- Clean and modular architecture

## Setup

1. Install Python 3.8 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Tesseract OCR:
   - Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
   - Add Tesseract to your system PATH

## API Endpoints

### POST /extract
Upload a file (PDF or image) to extract text and fields.

#### Using Postman:
1. Create a new POST request to `http://localhost:5000/extract`
2. Go to the "Body" tab and select "form-data"
3. Add a new key-value pair:
   - Key: `file`
   - Value: Click the "Select File" button and choose your PDF or image file
4. Click "Send"

Response:
```json
{
    "file": "example.pdf",
    "pages": [
        {
            "page": 1,
            "text": "Invoice No: 1234\nTotal: PKR 4500",
            "fields": {
                "invoice_number": "1234",
                "total": "PKR 4500"
            }
        }
    ],
    "processed_at": "2025-08-08T12:25:27+00:00"
}
```

### GET /history
Get a list of previously processed files with their extracted fields.

#### Using Postman:
1. Create a new GET request to `http://localhost:5000/history`
2. Click "Send"

Response:
```json
[
    {
        "filename": "example.pdf",
        "processed_at": "2025-08-08T12:25:27+00:00",
        "extracted_fields": {
            "invoice_number": "1234",
            "date": "2025-08-08",
            "total": "PKR 4500"
        }
    }
]
```

## Supported File Types

- PDF (.pdf)
- Images (.png, .jpg, .jpeg, .tiff)

## Testing with Postman

### Prerequisites
1. Install Postman (download from https://www.postman.com/downloads/)
2. Ensure Tesseract OCR is installed on your system
3. Run the API server using `python app.py`

### Step-by-Step Guide

#### 1. Generate JWT Token via API
Before testing other endpoints, you need to get a JWT token:
1. Create a new POST request in Postman
2. Set URL to `http://localhost:5000/api/auth/token`
3. Click "Send"
4. The response will contain your JWT token in the format:
```json
{
    "token": "your-jwt-token-here",
    "expires_in": 86400  // seconds (1 day)
}
```
5. Copy the token value

#### 2. Validate Token (Optional)
You can verify if your token is valid before using it:
1. Create a new GET request in Postman
2. Set URL to `http://localhost:5000/api/auth/validate`
3. Go to "Headers" tab
4. Add a header:
   - Key: `Authorization`
   - Value: `Bearer [Your JWT Token]`
5. Click "Send"

The response will indicate if the token is valid:
```json
{
    "valid": true,
    "message": "Token is valid"
}
```

#### 2. Test File Extraction
1. Create a new POST request in Postman
2. Set URL to `http://localhost:5000/extract`
3. Go to "Headers" tab
4. Add a header:
   - Key: `Authorization`
   - Value: `Bearer [Your JWT Token]`
5. Go to "Body" tab
6. Select "form-data"
7. Add a key-value pair:
   - Key: `file`
   - Value: Click "Select Files" and choose your PDF or image file
8. Click "Send"

#### 3. Test History Endpoint
1. Create a new GET request in Postman
2. Set URL to `http://localhost:5000/history`
3. Go to "Headers" tab
4. Add a header:
   - Key: `Authorization`
   - Value: `Bearer [Your JWT Token]`
5. Click "Send"

Response will contain detailed history of all processed files:
```json

1. **"No file uploaded" error**
   - Ensure you've selected the file in Postman
   - Check if the file path is correct
   - Verify file size (should be reasonable)

2. **"Unsupported file type" error**
   - Make sure the file has one of these extensions:
     - PDF: .pdf
     - Images: .png, .jpg, .jpeg, .tiff

3. **"Unauthorized" error (401)**
   - Verify you've included the API key header
   - Check if the API key is correct
   - Make sure there are no extra spaces in the API key

4. **"No history to export" error**
   - Make sure you've processed at least one file first
   - Try processing a file through the `/extract` endpoint

### Expected Responses

#### Success Response for File Extraction
```json
{
    "file": "example.pdf",
    "pages": [
        {
            "page": 1,
            "text": "Invoice Number: INV-12345\nDate: 2025-08-08",
            "fields": {
                "invoice_number": "INV-12345",
                "date": "2025-08-08"
            }
        }
    ],
    "processed_at": "2025-08-08T12:25:27+00:00"
}
```

#### Success Response for History
```json
[
    {
        "filename": "example.pdf",
        "processed_at": "2025-08-08T12:25:27+00:00",
        "extracted_fields": {
            "invoice_number": "INV-12345",
            "date": "2025-08-08"
        }
    }
]
```

#### Sample CSV Export
```
file,page,processed_at,invoice_number,date
example.pdf,1,2025-08-08T12:25:27+00:00,INV-12345,2025-08-08
```

## Technical Details

### Project Structure
```
smart_text_extractor/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── routes/            # API route definitions
│   ├── extract_routes.py
│   └── history_routes.py
├── services/          # Business logic
│   ├── extract_service.py
│   └── history_service.py
├── storage/           # File storage
├── uploads/           # Uploaded files
└── utils/            # Utility functions
```

### Dependencies
- Flask: Web framework
- PyMuPDF: PDF processing
- Pillow: Image processing
- pytesseract: OCR functionality
- SQLite: Database storage

## Running the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Access the API at http://localhost:5000

## Security Considerations

- The API should be protected with authentication in production
- Sensitive data should be properly sanitized
- File uploads should be validated for size and type
- Error messages should not expose sensitive information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
