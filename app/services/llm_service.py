import os
import openai
from typing import Dict, Any
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMService:
    def __init__(self):
        # Configure OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = openai.OpenAI(api_key=api_key)
        #self.model = "gpt-4"  # Using GPT-4 as GPT-4.1 is not available
        
    async def extract_data(self, file_content: str) -> Dict[str, Any]:
        """
        Extract structured data from file content using GPT-4
        """
        prompt = """
        Extract the following information from the provided document and return it in a structured JSON format:
        - document_number
        - date_of_reply_submission
        - description
        - forum
        - type
        - date_of_filing
        - party_details
        - payment_type
        - link_payment_with_issue
        - date_of_issue
        - date_of_expiry
        - reference_number
        - nature
        - date_of_filing_application
        - type_of_refund
        - link_refund_with_issue
        
        If any field is not present in the document, leave it as an empty string.
        
        Document content:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts information from documents and returns it in a structured JSON format."},
                    {"role": "user", "content": f"{prompt}\n\n{file_content[:15000]}"}
                ],
                temperature=0.1
            )
            
            # Extract the JSON from the response
            content = response.choices[0].message.content.strip()
            
            # Sometimes the response might be wrapped in markdown code blocks
            if content.startswith('```json'):
                content = content[7:-3].strip()
            elif content.startswith('```'):
                content = content[3:-3].strip()
            
            # Parse the JSON response
            extracted_data = json.loads(content)
            
            # Ensure all fields are strings
            string_fields = [
                'document_number', 'date_of_reply_submission', 'description',
                'forum', 'type', 'date_of_filing', 'payment_type',
                'link_payment_with_issue', 'date_of_issue', 'date_of_expiry',
                'reference_number', 'nature', 'date_of_filing_application',
                'type_of_refund', 'link_refund_with_issue', 'party_details'
            ]
            
            for field in string_fields:
                if field in extracted_data and extracted_data[field] is not None:
                    if isinstance(extracted_data[field], dict):
                        # Convert dictionary to string representation
                        extracted_data[field] = json.dumps(extracted_data[field], ensure_ascii=False)
                    elif not isinstance(extracted_data[field], str):
                        # Convert other non-string types to string
                        extracted_data[field] = str(extracted_data[field])
                else:
                    # Ensure all fields are present as empty strings if missing
                    extracted_data[field] = ""
            
            # Format the response according to the sample output
            return {
                "status": 1,
                "data": {
                    "request_id": "",  # This should be generated uniquely per request
                    "message": "Request processed successfully",
                    "content": extracted_data,
                    "error": {
                        "code": 0,
                        "msg": "No Error"
                    }
                }
            }
            
        except Exception as e:
            return {
                "status": 0,
                "data": {
                    "request_id": "",
                    "message": "Error processing request",
                    "content": {},
                    "error": {
                        "code": 1,
                        "msg": str(e)
                    }
                }
            }
