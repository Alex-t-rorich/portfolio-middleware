# app/schemas/users.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Base schema with common attributes
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    title: Optional[str] = None
    deleted: bool = True

# Schema for creating a user
class UserCreate(UserBase):
    password: str

# Schema for updating a user
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    title: Optional[str] = None
    deleted: Optional[bool] = None
    password: Optional[str] = None

# Schema for response (excludes password)
class User(UserBase):
    id: int
    login_count: int
    last_login: Optional[date] = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str