from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text, Date, Index, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Experience(Base):
    __tablename__ = "cv_experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False, index=True)
    description = Column(Text, nullable=True)
    position = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    current = Column(Boolean, default=False)
    company_name = Column(String, nullable=True)
    experience = Column(Text, nullable=True)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    # location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    
    # Relationships
    cv = relationship("CV", back_populates="experiences")
    # location = relationship("Location", back_populates="experiences")  # Fixed relationship name
    
    __table_args__ = (
        Index('idx_experience_not_deleted', 'deleted', postgresql_where=text('deleted = false')),  # Fixed index name
    )
    
    def __repr__(self):
        """String representation of the Experience."""
        return f"<Experience {self.id}: {self.title} at {self.company_name}>"  # Changed Education to Experience
