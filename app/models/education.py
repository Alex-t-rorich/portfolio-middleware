from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base

class Educations(Base):
    __tablename__ = "cv_educations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False, index=True)
    organisation = Column(String, nullable=True)
    location = Column(String, nullable=True)
    graduation_year = Column(Integer, nullable=True)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    
    # Relationships
    cv = relationship("CV", back_populates="educations")
    
    __table_args__ = (
        Index('idx_education_not_deleted', 'deleted', postgresql_where=text('deleted = false')),
    )
    
    def __repr__(self):
        """String representation of the Education."""
        return f"<Education {self.id}: {self.title} at {self.organisation}>"
