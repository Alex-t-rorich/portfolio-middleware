from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EducationBase(BaseModel):
    title: str
    organisation: Optional[str] = None
    location: Optional[str] = None
    graduation_year: Optional[int] = None

class EducationCreate(EducationBase):
    cv_id: int

class EducationUpdate(BaseModel):
    title: Optional[str] = None
    organisation: Optional[str] = None
    location: Optional[str] = None
    graduation_year: Optional[int] = None

class EducationResponse(EducationBase):
    id: int
    created: datetime
    updated: datetime
    cv_id: int
    
    class Config:
        from_attributes = True