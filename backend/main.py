from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from models import ContactRequest, ContactResponse
from config import settings
from database.service import db_service
from services.validation import ValidationService
from services.content_moderation import content_moderator

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="EmptyMug Website API",
    description="Backend API for EmptyMug website contact form with database storage",
    version="2.0.0"
)

# Configure CORS
origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Initializing application services...")
    try:
        # Initialize database
        await db_service.initialize()
        logger.info(f"Database service initialized: {settings.database_type}")
        
        # Initialize content moderator
        await content_moderator.initialize()
        logger.info("Content moderation service initialized")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise

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
        "version": "2.0.0",
        "database": settings.database_type
    }

@app.post("/api/contact", response_model=ContactResponse)
async def submit_contact_form(contact_data: ContactRequest):
    """Submit contact form and store in database"""
    try:
        logger.info(f"Received contact form submission from {contact_data.email}")
        
        # Additional validation using validation service
        is_valid_name, name_msg = ValidationService.validate_name(contact_data.fullName)
        if not is_valid_name:
            raise HTTPException(status_code=400, detail=name_msg)
            
        is_valid_email, email_msg = ValidationService.validate_email_format(contact_data.email)
        if not is_valid_email:
            raise HTTPException(status_code=400, detail=f"Invalid email: {email_msg}")
            
        is_valid_phone, phone_msg = ValidationService.validate_phone_number(
            contact_data.phoneNumber, contact_data.countryCode
        )
        if not is_valid_phone:
            raise HTTPException(status_code=400, detail=f"Invalid phone: {phone_msg}")
            
        is_valid_country, country_msg = ValidationService.validate_country_code(contact_data.countryCode)
        if not is_valid_country:
            raise HTTPException(status_code=400, detail=country_msg)
            
        is_valid_message, message_msg = ValidationService.validate_message(contact_data.message)
        if not is_valid_message:
            raise HTTPException(status_code=400, detail=message_msg)
        
        # Content moderation using LLM
        moderation_result = await content_moderator.moderate_content(contact_data.message)
        if not moderation_result.is_clean:
            logger.warning(f"Content rejected for {contact_data.email}: {moderation_result.message}")
            raise HTTPException(
                status_code=400, 
                detail="Your message contains inappropriate content. Please revise and try again."
            )
        
        # Store in database
        contact_record = {
            "full_name": contact_data.fullName,
            "email": contact_data.email,
            "phone_number": phone_msg if is_valid_phone else contact_data.phoneNumber,
            "country_code": contact_data.countryCode,
            "message": contact_data.message
        }
        
        contact_id = await db_service.create_contact(contact_record)
        
        logger.info(f"Contact form stored successfully with ID {contact_id} for {contact_data.email}")
        return ContactResponse(
            success=True,
            message="Thank you for your message! We've received your submission and will get back to you soon.",
            contact_id=contact_id
        )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in contact form submission: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )

@app.get("/api/contacts")
async def get_contacts(limit: int = 100, offset: int = 0):
    """Retrieve contacts (for admin use)"""
    try:
        contacts = await db_service.list_contacts(limit=limit, offset=offset)
        return {
            "success": True,
            "contacts": contacts,
            "count": len(contacts)
        }
    except Exception as e:
        logger.error(f"Error retrieving contacts: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve contacts"
        )

@app.get("/api/contacts/{contact_id}")
async def get_contact(contact_id: str):
    """Retrieve a specific contact by ID"""
    try:
        contact = await db_service.get_contact(contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        return {
            "success": True,
            "contact": contact
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving contact {contact_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve contact"
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
