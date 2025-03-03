from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    login_count = Column(Integer, nullable=False, default=0)
    last_login = Column(Date, nullable=True)

    # Relationships
    websites = relationship("Website", back_populates="owner")

    # Define a partial index for efficient queries on non-deleted records
    __table_args__ = (
        Index('idx_website_not_deleted', 'deleted', postgresql_where=text('deleted = false')),
    )

    @property
    def full_name(self):
        """Returns the full name of the user."""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        """String representation of the user."""
        return f"<User {self.id}: {self.email}>"