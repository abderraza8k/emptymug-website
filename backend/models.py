from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re

class ContactRequest(BaseModel):
    fullName: str = Field(..., min_length=2, max_length=100, description="Full name of the person")
    email: EmailStr = Field(..., description="Valid email address")
    phoneNumber: Optional[str] = Field(None, max_length=20, description="Phone number (optional)")
    countryCode: str = Field(..., min_length=2, max_length=3, description="ISO country code")
    message: str = Field(..., min_length=10, max_length=5000, description="Message content")

    class Config:
        str_strip_whitespace = True
        min_anystr_length = 1
        
    @validator('fullName')
    def validate_full_name(cls, v):
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-'\.]+$", v):
            raise ValueError('Name contains invalid characters')
        if not re.search(r'[a-zA-ZÀ-ÿ]', v):
            raise ValueError('Name must contain at least one letter')
        return v
    
    @validator('countryCode')
    def validate_country_code(cls, v):
        return v.upper()
    
    @validator('phoneNumber')
    def validate_phone_number(cls, v):
        if v and not re.match(r'^[\d\s\-\+\(\)]+$', v):
            raise ValueError('Phone number contains invalid characters')
        return v

class ContactResponse(BaseModel):
    success: bool
    message: str
    contact_id: Optional[str] = None
