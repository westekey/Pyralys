"""
WordPress Account model for storing WordPress site connections
"""
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class WordPressAccount(Base, TimestampMixin):
    """WordPress site connection model"""
    __tablename__ = "wordpress_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # WordPress site information
    site_url = Column(String(500), nullable=False)  # e.g., https://mysite.com
    site_name = Column(String(255), nullable=True)

    # Authentication (Application Password or OAuth)
    username = Column(String(255), nullable=False)  # WordPress username
    app_password = Column(String(500), nullable=False)  # Application password (encrypted)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    last_sync = Column(String(50), nullable=True)  # ISO datetime of last successful sync

    # Relationships
    user = relationship("User", back_populates="wordpress_accounts")

    def __repr__(self):
        return f"<WordPressAccount {self.site_url} - {self.username}>"

    @property
    def display_name(self):
        """Display name for the UI"""
        return self.site_name or self.site_url
