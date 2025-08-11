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

```

### GET /history
Get a list of previously processed files with their extracted fields.

#### Using Postman:
1. Create a new GET request to `http://localhost:5000/history`
2. Click "Send"

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

### Expected Responses


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



