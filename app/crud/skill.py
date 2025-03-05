from sqlalchemy.orm import Session
from ..models.skill import Skill
from ..schemas.skill import SkillCreate, SkillUpdate

def list_skills(db: Session, cv_id: int):
    return db.query(Skill).filter(Skill.cv_id == cv_id).all()

def get_skill(db: Session, skill_id: int):
    return db.query(Skill).filter(Skill.id == skill_id).first()

def create_skill(db: Session, skill: SkillCreate):
    db_skill = Skill(
        title=skill.title,
        description=skill.description,
        ranking=skill.ranking,
        cv_id=skill.cv_id
    )
   
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
   
    return db_skill

def update_skill(db: Session, skill_id: int, skill_data: SkillUpdate):
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
   
    if not db_skill:
        return None
   
    update_data = skill_data.model_dump(exclude_unset=True)
   
    for key, value in update_data.items():
        setattr(db_skill, key, value)
   
    db.commit()
    db.refresh(db_skill)
   
    return db_skill

def delete_skill(db: Session, skill_id: int):
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
   
    if not db_skill:
        return False
   
    db_user.deleted = True
    db.commit()
       
    return True