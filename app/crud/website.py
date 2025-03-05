from sqlalchemy.orm import Session
from ..models.website import Website
from ..schemas.website import WebsiteCreate, WebsiteUpdate

def list_websites(db: Session, user_id: int):
    return db.query(Website).filter(Website.user_id == user_id, Website.deleted == False).all()

def get_website(db: Session, website_id: int):
    return db.query(Website).filter(Website.id == website_id).first()

def create_website(db: Session, website: WebsiteCreate):
    db_website = Website(
        title=website.title,
        description=website.description,
        website_url=website.website_url,
        user_id=website.user_id
    )
    
    db.add(db_website)
    db.commit()
    db.refresh(db_website)
    
    return db_website

def update_website(db: Session, website_id: int, website_data: WebsiteUpdate):
    db_website = db.query(Website).filter(Website.id == website_id).first()
    
    if not db_website:
        return None
    
    update_data = website_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_website, key, value)
    
    db.commit()
    db.refresh(db_website)
    
    return db_website

def delete_website(db: Session, website_id: int):
    db_website = db.query(Website).filter(Website.id == website_id).first()
    
    if not db_website:
        return False
    
    # Soft delete
    db_website.deleted = True
    db.commit()
    
    return True