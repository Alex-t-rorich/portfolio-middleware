from sqlalchemy.orm import Session
from ..models.education import Experience
from ..schemas.experience import ExperienceCreate, ExperienceUpdate

def list_experiences(db: Session, cv_id: int):
    return db.query(Experience).filter(Experience.cv_id == cv_id).all()

def get_experience(db: Session, experience_id: int):
    return db.query(Experience).filter(Experience.id == experience_id).first()

def create_experience(db: Session, education: ExperienceCreate):
    db_experience = Experience(
        title=experience.title,
        description=experience.description,
        position=experience.position,
        start_date=experience.start_date,
        end_date=experience.end_date,
        current=experience.current,
        company_name=experience.company_name,
        experience=experience.experience,
        cv_id=experience.cv_id
    )
    
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    
    return db_experience

def update_experience(db: Session, experience_id: int, experience_data: ExperienceUpdate):
    db_experience = db.query(Experience).filter(Experience.id == experience_id).first()
    
    if not db_experience:
        return None
    
    update_data = education_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_experience, key, value)
    
    db.commit()
    
    db.refresh(db_experience)
    
    return db_experience

def delete_experience(db: Session, experience_id: int):
    db_experience = db.query(Experience).filter(Experience.id == experience_id).first()
    
    if not db_experience:
        return False
    
    db_user.deleted = True
    db.commit()
    
    return True