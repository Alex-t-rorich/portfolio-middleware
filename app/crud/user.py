from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

def list_users(db: Session):
    return db.query(User).filter(User.deleted == False).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        title=user.title,
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        return None
    
    update_data = user_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        return False
    
    # Soft delete
    db_user.deleted = True
    db.commit()
    
    return True

def increment_login_count(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        return None
    
    # Increment login count
    db_user.login_count += 1
    # Update last login date
    db_user.last_login = func.now()
    
    db.commit()
    db.refresh(db_user)
    
    return db_user