from sqlalchemy.orm import Session
from ..models.education import Education
from ..schemas.education import EducationCreate, EducationUpdate

def list_educations(db: Session, cv_id: int):
    return db.query(Education).filter(Education.cv_id == cv_id).all()

def get_education(db: Session, education_id: int):
    return db.query(Education).filter(Education.id == education_id).first()

def create_education(db: Session, education: EducationCreate):
    db_education = Education(
        title=education.title,
        organisation=education.organisation,
        location=education.location,
        graduation_year=education.graduation_year,
        cv_id=education.cv_id
    )
    
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    
    return db_education

def update_education(db: Session, education_id: int, education_data: EducationUpdate):
    db_education = db.query(Education).filter(Education.id == education_id).first()
    
    if not db_education:
        return None
    
    update_data = education_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_education, key, value)
    
    db.commit()
    
    db.refresh(db_education)
    
    return db_education

def delete_education(db: Session, education_id: int):
    db_education = db.query(Education).filter(Education.id == education_id).first()
    
    if not db_education:
        return False
    
    db_user.deleted = True
    db.commit()
    
    return True