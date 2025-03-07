from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.cv import CVCreate, CVUpdate, CVResponse
from ..crud.cv import list_cvs_by_website, get_cv, create_cv, update_cv, delete_cv

# CVs are associated with websites, so using a nested structure
router = APIRouter(prefix="/api/v1/websites", tags=["cvs"])

@router.get("/{website_id}/cvs", response_model=List[CVResponse])
def get_cvs(website_id: int, db: Session = Depends(get_db)):
    db_cvs = list_cvs_by_website(db=db, website_id=website_id)
    return db_cvs

@router.get("/{website_id}/cvs/{cv_id}", response_model=CVResponse)
def read_cv(website_id: int, cv_id: int, db: Session = Depends(get_db)):
    db_cv = get_cv(db=db, cv_id=cv_id)
    if db_cv is None:
        raise HTTPException(status_code=404, detail="CV not found")

    if db_cv.website_id != website_id:
        raise HTTPException(status_code=404, detail="CV not found for this website")
    return db_cv

@router.post("/{website_id}/cvs", response_model=CVResponse, status_code=201)
def create_cv_endpoint(website_id: int, cv: CVCreate, db: Session = Depends(get_db)):
    cv_data = cv.model_dump()
    cv_data["website_id"] = website_id
    
    cv_with_website = CVCreate(**cv_data)
    
    return create_cv(db=db, cv=cv_with_website)

@router.put("/{website_id}/cvs/{cv_id}", response_model=CVResponse)
def update_cv_endpoint(website_id: int, cv_id: int, cv: CVUpdate, db: Session = Depends(get_db)):
    db_cv = get_cv(db=db, cv_id=cv_id)
    if db_cv is None:
        raise HTTPException(status_code=404, detail="CV not found")
    if db_cv.website_id != website_id:
        raise HTTPException(status_code=404, detail="CV not found for this website")
    
    updated_cv = update_cv(db=db, cv_id=cv_id, cv_data=cv)
    return updated_cv

@router.delete("/{website_id}/cvs/{cv_id}", status_code=204)
def delete_cv_endpoint(website_id: int, cv_id: int, db: Session = Depends(get_db)):
    db_cv = get_cv(db=db, cv_id=cv_id)
    if db_cv is None:
        raise HTTPException(status_code=404, detail="CV not found")
    if db_cv.website_id != website_id:
        raise HTTPException(status_code=404, detail="CV not found for this website")
    
    success = delete_cv(db=db, cv_id=cv_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete CV")
    return {"detail": "CV successfully deleted"}