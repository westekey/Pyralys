"""
Instagram Account model for storing Instagram connections via OAuth
"""
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class InstagramAccount(Base, TimestampMixin):
    """Instagram account connection model (OAuth 2.0)"""
    __tablename__ = "instagram_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # Instagram account info
    instagram_user_id = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(255), nullable=False)
    account_type = Column(String(50), nullable=True)  # BUSINESS, CREATOR, PERSONAL

    # OAuth tokens
    access_token = Column(Text, nullable=False)  # Long-lived token (60 days)
    token_expires_at = Column(String(50), nullable=True)  # ISO datetime

    # Account metadata
    profile_picture_url = Column(String(500), nullable=True)
    followers_count = Column(Integer, default=0)
    follows_count = Column(Integer, default=0)
    media_count = Column(Integer, default=0)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    last_sync = Column(String(50), nullable=True)  # ISO datetime of last successful sync

    # Relationships
    user = relationship("User", back_populates="instagram_accounts")

    def __repr__(self):
        return f"<InstagramAccount @{self.username} - {self.instagram_user_id}>"

    @property
    def display_name(self):
        """Display name for the UI"""
        return f"@{self.username}"

    @property
    def is_business_account(self):
        """Check if this is a business or creator account"""
        return self.account_type in ["BUSINESS", "CREATOR"]
