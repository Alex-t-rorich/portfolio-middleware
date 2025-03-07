from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Index, Text, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base

class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)
    website_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="website")
    cv = relationship("CV", back_populates="website")
    
    # Define a partial index for efficient queries on non-deleted records
    __table_args__ = (
        Index('idx_website_not_deleted', 'deleted', postgresql_where=text('deleted = false')),
    )
    
    def __repr__(self):
        """String representation of the website."""
        return f"<Website {self.id}: {self.title}>"