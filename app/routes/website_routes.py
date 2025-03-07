from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.website import WebsiteCreate, WebsiteUpdate, WebsiteResponse
from ..crud.website import list_websites, get_website, create_website, update_website, delete_website

router = APIRouter(prefix="/api/v1/websites", tags=["websites"])

@router.get("/", response_model=List[WebsiteResponse])
def get_websites(user_id: int, db: Session = Depends(get_db)):
    db_websites = list_websites(db=db, user_id=user_id)
    return db_websites

@router.get("/{website_id}", response_model=WebsiteResponse)
def read_website(website_id: int, db: Session = Depends(get_db)):
    db_website = get_website(db=db, website_id=website_id)
    if db_website is None:
        raise HTTPException(status_code=404, detail="Website not found")
    return db_website

@router.post("/", response_model=WebsiteResponse, status_code=201)
def create_new_website(website: WebsiteCreate, db: Session = Depends(get_db)):
    return create_website(db=db, website=website)

@router.put("/{website_id}", response_model=WebsiteResponse)
def update_existing_website(website_id: int, website: WebsiteUpdate, db: Session = Depends(get_db)):
    db_website = update_website(db=db, website_id=website_id, website_data=website)
    if db_website is None:
        raise HTTPException(status_code=404, detail="Website not found")
    return db_website

@router.delete("/{website_id}", status_code=204)
def delete_existing_website(website_id: int, db: Session = Depends(get_db)):
    success = delete_website(db=db, website_id=website_id)
    if not success:
        raise HTTPException(status_code=404, detail="Website not found")
    return {"detail": "Website successfully deleted"}