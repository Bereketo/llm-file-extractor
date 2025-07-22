from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uuid

from app.routers import extract

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Document Data Extractor API",
    description="API for extracting structured data from documents using GPT-4",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(extract.router, prefix="/api/v1", tags=["extract"])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    logger.info(f"Request: {request.method} {request.url} - RequestID: {request_id}")
    
    try:
        response = await call_next(request)
        logger.info(f"Response: {response.status_code} - RequestID: {request_id}")
        return response
    except Exception as e:
        logger.error(f"Error: {str(e)} - RequestID: {request_id}")
        return JSONResponse(
            status_code=500,
            content={
                "status": 0,
                "data": {
                    "request_id": request_id,
                    "message": "Internal server error",
                    "error": {
                        "code": 500,
                        "msg": str(e)
                    }
                }
            }
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
