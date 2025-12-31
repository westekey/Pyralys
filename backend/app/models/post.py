"""
Post database model
"""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base, TimestampMixin


class Post(Base, TimestampMixin):
    """Post model"""
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500))
    caption = Column(String, nullable=False)
    media_urls = Column(JSONB, default=list)
    platform = Column(String(50), nullable=False)
    status = Column(String(50), default="draft", nullable=False)
    scheduled_at = Column(DateTime(timezone=True))
    published_at = Column(DateTime(timezone=True))
    ai_generated = Column(Boolean, default=False)
    generation_params = Column(JSONB)

    def __repr__(self):
        return f"<Post(id={self.id}, platform={self.platform}, status={self.status})>"
