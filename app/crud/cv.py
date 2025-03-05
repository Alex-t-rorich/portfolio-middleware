from sqlalchemy.orm import Session
from sqlalchemy import text
from ..models.cv import CV
from ..schemas.cv import CVCreate, CVUpdate

def list_cvs_by_website(db: Session, website_id: int):
    return db.query(CV).filter(CV.website_id == website_id, CV.deleted == False).all()

def get_cv(db: Session, cv_id: int):
    return db.query(CV).filter(CV.id == cv_id).first()

def create_cv(db: Session, cv: CVCreate):
    db_cv = CV(
        title=cv.title,
        description=cv.description,
        email=cv.email,
        phone_number=cv.phone_number,
        facebook=cv.facebook,
        linkedin=cv.linkedin,
        github=cv.github,
        x=cv.x,
        instagram=cv.instagram,
        location_id=cv.location_id,
        website_id=cv.website_id
    )
    
    db.add(db_cv)
    db.commit()
    db.refresh(db_cv)
    
    return db_cv

def update_cv(db: Session, cv_id: int, cv_data: CVUpdate):
    db_cv = db.query(CV).filter(CV.id == cv_id).first()
    
    if not db_cv:
        return None
    
    update_data = cv_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_cv, key, value)
    
    db.commit()
    db.refresh(db_cv)
    
    return db_cv

def delete_cv(db: Session, cv_id: int):
    db_cv = db.query(CV).filter(CV.id == cv_id).first()
    
    if not db_cv:
        return False
    
    db_cv.deleted = True
    db.commit()
    
    return True
