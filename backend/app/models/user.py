"""
User database model
"""
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """User model"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    plan_type = Column(String(50), default="free", nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
