from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactRequest(BaseModel):
    fullName: str
    email: EmailStr
    phoneNumber: Optional[str] = None
    countryCode: str
    message: str

    class Config:
        str_strip_whitespace = True
        min_anystr_length = 1

class ContactResponse(BaseModel):
    success: bool
    message: str
