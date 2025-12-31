"""
Social Account database model
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.models.base import Base, TimestampMixin


class SocialAccount(Base, TimestampMixin):
    """Social Media Account model"""
    __tablename__ = "social_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False)
    platform_user_id = Column(String(255))
    access_token = Column(Text)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime(timezone=True))
    account_username = Column(String(255))
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<SocialAccount(id={self.id}, platform={self.platform}, username={self.account_username})>"
