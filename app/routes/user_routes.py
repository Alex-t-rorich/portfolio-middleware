from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.user import UserCreate, UserUpdate, UserResponse
from ..crud.user import list_users, get_user, get_user_by_email, create_user, update_user, delete_user, increment_login_count

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    db_users = list_users(db=db)
    return db_users

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/email/{email}", response_model=UserResponse)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/", response_model=UserResponse, status_code=201)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db=db, user_id=user_id, user_data=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=204)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User successfully deleted"}

@router.post("/{user_id}/login", response_model=UserResponse)
def login_user(user_id: int, db: Session = Depends(get_db)):
    db_user = increment_login_count(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user