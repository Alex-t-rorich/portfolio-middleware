from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base

class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False, index=True)
    description = Column(Text, nullable=True)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    facebook = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    github = Column(String, nullable=True)
    x = Column(String, nullable=True)  # Twitter/X
    instagram = Column(String, nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    
    # Relationships
    website = relationship("Website", back_populates="cv")
    # location = relationship("Location", back_populates="cv")
    experience = relationship("Experience", back_populates="cv")
    skill = relationship("Skill", back_populates="cv")
    education = relationship("Education", back_populates="cv")
    # location = relationship("Location", back_populates="cv")

    __table_args__ = (
        Index('idx_cv_not_deleted', 'deleted', postgresql_where=Text('deleted = false')),
    )
    
    def __repr__(self):
        """String representation of the CV."""
        return f"<CV {self.id}: {self.title}>"