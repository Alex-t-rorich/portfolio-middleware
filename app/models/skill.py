# SQLAlchemy Model
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Text, Index, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Skill(Base):
    __tablename__ = "cv_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False, index=True)
    description = Column(Text, nullable=True)
    cv_id = Column(Integer, ForeignKey("cvs.id"), nullable=False)
    ranking = Column(Integer, nullable=True)
    
    # Relationships
    cv = relationship("CV", back_populates="skills")
    
    __table_args__ = (
        Index('idx_skill_not_deleted', 'deleted', postgresql_where=text('deleted = false')),
    )
    
    def __repr__(self):
        """String representation of the Skill."""
        return f"<Skill {self.id}: {self.title} (Ranking: {self.ranking})>"