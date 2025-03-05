from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SkillBase(BaseModel):
    title: str
    description: Optional[str] = None
    ranking: Optional[int] = None

class SkillCreate(SkillBase):
    cv_id: int

class SkillUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    ranking: Optional[int] = None

class SkillResponse(SkillBase):
    id: int
    created: datetime
    updated: datetime
    cv_id: int
    
    class Config:
        from_attributes = True