from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date  # Added date import

class ExperienceBase(BaseModel):
    title: str
    description: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    current: Optional[bool] = False
    company_name: Optional[str] = None
    experience: Optional[str] = None

class ExperienceCreate(ExperienceBase):
    cv_id: int

class ExperienceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    current: Optional[bool] = None
    company_name: Optional[str] = None
    experience: Optional[str] = None

class ExperienceResponse(ExperienceBase):
    id: int
    created: datetime
    updated: datetime
    cv_id: int
    
    class Config:
        from_attributes = True