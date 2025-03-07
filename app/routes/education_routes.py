from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.education import EducationCreate, EducationUpdate, EducationResponse
from ..crud.education import list_educations, get_education, create_education, update_education, delete_education

router = APIRouter(prefix="/api/v1/cvs", tags=["education"])

@router.get("/{cv_id}/education", response_model=List[EducationResponse])
def get_educations(cv_id: int, db: Session = Depends(get_db)):
    db_educations = list_educations(db=db, cv_id=cv_id)
    return db_educations

@router.get("/{cv_id}/education/{education_id}", response_model=EducationResponse)
def read_education(cv_id: int, education_id: int, db: Session = Depends(get_db)):
    db_education = get_education(db=db, education_id=education_id)
    if db_education is None:
        raise HTTPException(status_code=404, detail="Education entry not found")
    if db_education.cv_id != cv_id:
        raise HTTPException(status_code=404, detail="Education entry not found in this CV")
    return db_education

@router.post("/{cv_id}/education", response_model=EducationResponse, status_code=201)
def create_new_education(cv_id: int, education: EducationCreate, db: Session = Depends(get_db)):
    education_data = education.model_dump()
    education_data["cv_id"] = cv_id
    
    education_with_cv = EducationCreate(**education_data)
    
    return create_education(db=db, education=education_with_cv)

@router.put("/{cv_id}/education/{education_id}", response_model=EducationResponse)
def update_exisiting_education(cv_id: int, education_id: int, education: EducationUpdate, db: Session = Depends(get_db)):

    db_education = get_education(db=db, education_id=education_id)
    if db_education is None:
        raise HTTPException(status_code=404, detail="Education entry not found")
    if db_education.cv_id != cv_id:
        raise HTTPException(status_code=404, detail="Education entry not found in this CV")
    
    updated_education = update_education(db=db, education_id=education_id, education_data=education)
    return updated_education

@router.delete("/{cv_id}/education/{education_id}", status_code=204)
def delete_exisiting_education(cv_id: int, education_id: int, db: Session = Depends(get_db)):
    db_education = get_education(db=db, education_id=education_id)
    if db_education is None:
        raise HTTPException(status_code=404, detail="Education entry not found")
    if db_education.cv_id != cv_id:
        raise HTTPException(status_code=404, detail="Education entry not found in this CV")
    
    success = delete_education(db=db, education_id=education_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete education entry")
    return {"detail": "Education entry successfully deleted"}