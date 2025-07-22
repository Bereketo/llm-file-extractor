import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging

from app.models.schemas import ExtractResponse, ErrorResponseModel
from app.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

@router.post(
    "/extract",
    response_model=ExtractResponse,
    responses={
        200: {"model": ExtractResponse},
        400: {"model": ErrorResponseModel},
        500: {"model": ErrorResponseModel}
    }
)
async def extract_data(file: UploadFile = File(...)):
    """
    Extract structured data from an uploaded file using GPT-4.
    
    This endpoint accepts various document types and returns extracted information
    in a structured JSON format.
    """
    # Check if file is provided
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded"
        )
    
    # Check file size (limit to 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    file.file.seek(0, 2)  # Move to end of file
    file_size = file.file.tell()
    file.file.seek(0)  # Reset file pointer
    
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {max_size} bytes"
        )
    
    try:
        # Read file content
        content = await file.read()
        file_content = content.decode('utf-8')
        
        # Process file with LLM
        result = await llm_service.extract_data(file_content)
        
        # Add request ID to the response
        request_id = str(uuid.uuid4())
        if 'data' in result and isinstance(result['data'], dict):
            result['data']['request_id'] = request_id
        
        return result
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not decode file content as UTF-8 text"
        )
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )
