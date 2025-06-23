from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from models import ContactRequest, ContactResponse
from email_service import email_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="EmptyMug Website API",
    description="Backend API for EmptyMug website contact form",
    version="1.0.0"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "EmptyMug Website API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "EmptyMug Website API",
        "version": "1.0.0"
    }

@app.post("/api/contact", response_model=ContactResponse)
async def submit_contact_form(contact_data: ContactRequest):
    """Submit contact form and send email"""
    try:
        logger.info(f"Received contact form submission from {contact_data.email}")
        
        # Validate required fields
        if not contact_data.fullName.strip():
            raise HTTPException(
                status_code=400, 
                detail="Full name is required"
            )
        
        if not contact_data.email.strip():
            raise HTTPException(
                status_code=400, 
                detail="Email is required"
            )
        
        if not contact_data.message.strip():
            raise HTTPException(
                status_code=400, 
                detail="Message is required"
            )
        
        if len(contact_data.message.strip()) < 10:
            raise HTTPException(
                status_code=400, 
                detail="Message must be at least 10 characters long"
            )
        
        # Send email
        email_sent = await email_service.send_contact_email(contact_data)
        
        if email_sent:
            logger.info(f"Contact form email sent successfully for {contact_data.email}")
            return ContactResponse(
                success=True,
                message="Thank you for your message! I'll get back to you soon."
            )
        else:
            logger.error(f"Failed to send contact form email for {contact_data.email}")
            raise HTTPException(
                status_code=500,
                detail="Failed to send email. Please try again later."
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in contact form submission: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
