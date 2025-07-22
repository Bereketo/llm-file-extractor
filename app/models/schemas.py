from pydantic import BaseModel
from typing import Optional, Dict, Any

class ErrorResponse(BaseModel):
    code: int
    msg: str

class ContentData(BaseModel):
    document_number: str = ""
    date_of_reply_submission: str = ""
    description: str = ""
    forum: str = ""
    type: str = ""
    date_of_filing: str = ""
    party_details: str = ""
    payment_type: str = ""
    link_payment_with_issue: str = ""
    date_of_issue: str = ""
    date_of_expiry: str = ""
    reference_number: str = ""
    nature: str = ""
    date_of_filing_application: str = ""
    type_of_refund: str = ""
    link_refund_with_issue: str = ""

class ExtractResponseData(BaseModel):
    request_id: str
    message: str
    content: ContentData
    error: ErrorResponse

class ExtractResponse(BaseModel):
    status: int
    data: ExtractResponseData

class ErrorResponseModel(BaseModel):
    status: int
    data: Dict[str, Any]
