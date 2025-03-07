from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CVBase(BaseModel):
    title: str
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    facebook: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    x: Optional[str] = None
    instagram: Optional[str] = None

class CVCreate(CVBase):
    website_id: int
    location_id: Optional[int] = None

class CVUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    facebook: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    x: Optional[str] = None
    instagram: Optional[str] = None
    location_id: Optional[int] = None
    deleted: Optional[bool] = None

class CVResponse(CVBase):
    id: int
    created: datetime
    updated: datetime
    deleted: bool
    website_id: int
    location_id: Optional[int] = None
   
    class Config:
        from_attributes = True