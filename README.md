# Document Data Extractor API

A FastAPI-based service that extracts structured data from documents using GPT-4.

## Features

- Accepts text files as input
- Extracts structured data using GPT-4
- Returns data in a consistent JSON format
- Handles file uploads and processing asynchronously
- Includes request logging and error handling

## Prerequisites

- Python 3.8+
- OpenAI API key

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Extract Data from Document

- **URL**: `/api/v1/extract`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Body**: `file` (required) - The document file to process

#### Example Request

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@document.txt;type=text/plain'
```

#### Example Response

```json
{
  "status": 1,
  "data": {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Request processed successfully",
    "content": {
      "document_number": "",
      "date_of_reply_submission": "",
      "description": "",
      "forum": "",
      "type": "",
      "date_of_filing": "",
      "party_details": "",
      "payment_type": "",
      "link_payment_with_issue": "",
      "date_of_issue": "",
      "date_of_expiry": "",
      "reference_number": "",
      "nature": "",
      "date_of_filing_application": "",
      "type_of_refund": "",
      "link_refund_with_issue": ""
    },
    "error": {
      "code": 0,
      "msg": "No Error"
    }
  }
}
```

## Error Handling

The API returns appropriate HTTP status codes along with error details in the response body.
