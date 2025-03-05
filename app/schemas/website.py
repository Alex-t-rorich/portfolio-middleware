from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class WebsiteBase(BaseModel):
    title: str
    description: Optional[str] = None
    website_url: Optional[HttpUrl] = None

class WebsiteCreate(WebsiteBase):
    user_id: int

class WebsiteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[HttpUrl] = None
    deleted: Optional[bool] = None

class WebsiteResponse(WebsiteBase):
    id: int
    created: datetime
    updated: datetime
    deleted: bool
    user_id: int
    
    class Config:
        from_attributes = True