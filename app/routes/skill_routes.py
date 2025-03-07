from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.skill import SkillCreate, SkillUpdate, SkillResponse
from ..crud.skill import list_skills, get_skill, create_skill, update_skill, delete_skill

router = APIRouter(prefix="/api/v1/cvs", tags=["skills"])

@router.get("/{cv_id}/skills", response_model=List[SkillResponse])
def get_skills(cv_id: int, db: Session = Depends(get_db)):
    db_skills = list_skills(db=db, cv_id=cv_id)
    return db_skills

@router.get("/{cv_id}/skills/{skill_id}", response_model=SkillResponse)
def read_skill(cv_id: int, skill_id: int, db: Session = Depends(get_db)):
    db_skill = get_skill(db=db, skill_id=skill_id)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    if db_skill.cv_id != cv_id:
        raise HTTPException(status_code=404, detail="Skill not found in this CV")
    return db_skill

@router.post("/{cv_id}/skills", response_model=SkillResponse, status_code=201)
def create__new_skill(cv_id: int, skill: SkillCreate, db: Session = Depends(get_db)):
    skill_data = skill.model_dump()
    skill_data["cv_id"] = cv_id
    
    skill_with_cv = SkillCreate(**skill_data)
    
    return create_skill(db=db, skill=skill_with_cv)

@router.put("/{cv_id}/skills/{skill_id}", response_model=SkillResponse)
def update_exisiting_skill(cv_id: int, skill_id: int, skill: SkillUpdate, db: Session = Depends(get_db)):

    db_skill = get_skill(db=db, skill_id=skill_id)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    if db_skill.cv_id != cv_id:
        raise HTTPException(status_code=404, detail="Skill not found in this CV")
    
    updated_skill = update_skill(db=db, skill_id=skill_id, skill_data=skill)
    return updated_skill

@router.delete("/{cv_id}/skills/{skill_id}", status_code=204)
def delete_skill_endpoint(cv_id: int, skill_id: int, db: Session = Depends(get_db)):
    db_skill = get_skill(db=db, skill_id=skill_id)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    if db_skill.cv_id != cv_id:
        raise HTTPException(status_code=404, detail="Skill not found in this CV")
    
    success = delete_skill(db=db, skill_id=skill_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete skill")
    return {"detail": "Skill successfully deleted"}