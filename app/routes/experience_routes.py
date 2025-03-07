from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.experience import ExperienceCreate, ExperienceUpdate, ExperienceResponse
from ..crud.experience import list_experiences, get_experience, create_experience, update_experience, delete_experience

# Using the same nested resource pattern as with skills
router = APIRouter(prefix="/api/v1/cvs", tags=["experiences"])

@router.get("/{cv_id}/experiences", response_model=List[ExperienceResponse])
def get_experiences(cv_id: int, db: Session = Depends(get_db)):
    db_experiences = list_experiences(db=db, cv_id=cv_id)
    return db_experiences

@router.get("/{cv_id}/experiences/{experience_id}", response_model=ExperienceResponse)
def read_experience(cv_id: int, experience_id: int, db: Session = Depends(get_db)):
    db_experience = get_experience(db=db, experience_id=experience_id)
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")

    if db_experience.cv_id != cv_id:
        raise HTTPException(status_code=404, detail="Experience not found in this CV")
    return db_experience

@router.post("/{cv_id}/experiences", response_model=ExperienceResponse, status_code=201)
def create_new_experience(cv_id: int, experience: ExperienceCreate, db: Session = Depends(get_db)):

    experience_data = experience.model_dump()
    experience_data["cv_id"] = cv_id
    
    experience_with_cv = ExperienceCreate(**experience_data)
    
    return create_experience(db=db, experience=experience_with_cv)

@router.put("/{cv_id}/experiences/{experience_id}", response_model=ExperienceResponse)
def update_existing_experience(cv_id: int, experience_id: int, experience: ExperienceUpdate, db: Session = Depends(get_db)):
    db_experience = get_experience(db=db, experience_id=experience_id)
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    if db_experience.cv_id != cv_id:
        raise HTTPException(status_code=404, detail="Experience not found in this CV")
    
    updated_experience = update_experience(db=db, experience_id=experience_id, experience_data=experience)
    return updated_experience

@router.delete("/{cv_id}/experiences/{experience_id}", status_code=204)
def delete_existing_experience(cv_id: int, experience_id: int, db: Session = Depends(get_db)):
    db_experience = get_experience(db=db, experience_id=experience_id)
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    if db_experience.cv_id != cv_id:
        raise HTTPException(status_code=404, detail="Experience not found in this CV")
    
    success = delete_experience(db=db, experience_id=experience_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete experience")
    return {"detail": "Experience successfully deleted"}