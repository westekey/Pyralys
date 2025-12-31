"""
Usage tracking model for quota management
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.models.base import Base


class UsageType(str, enum.Enum):
    """Types of usage to track"""
    CAPTION = "caption"
    IMAGE = "image"
    HASHTAG = "hashtag"
    POST = "post"
    ANALYTICS = "analytics"


class Usage(Base):
    """Track user usage for quota management"""
    __tablename__ = "usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    usage_type = Column(SQLEnum(UsageType), nullable=False, index=True)

    # Count for the current period
    count = Column(Integer, default=1, nullable=False)

    # Period tracking (monthly reset)
    period_start = Column(DateTime, nullable=False, default=datetime.utcnow)
    period_end = Column(DateTime, nullable=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="usage_records")

    def __repr__(self):
        return f"<Usage {self.user_id} - {self.usage_type}: {self.count}>"


# Quota limits per plan type
QUOTA_LIMITS = {
    "free": {
        UsageType.CAPTION: 10,      # 10 captions per month
        UsageType.IMAGE: 0,         # No image generation
        UsageType.HASHTAG: 20,      # 20 hashtag generations
        UsageType.POST: 5,          # 5 posts per month
        UsageType.ANALYTICS: 0,     # No analytics
    },
    "premium": {
        UsageType.CAPTION: 100,     # 100 captions per month
        UsageType.IMAGE: 50,        # 50 images per month
        UsageType.HASHTAG: 200,     # 200 hashtag generations
        UsageType.POST: 50,         # 50 posts per month
        UsageType.ANALYTICS: 1,     # Basic analytics
    },
    "pro": {
        UsageType.CAPTION: -1,      # Unlimited (-1 means no limit)
        UsageType.IMAGE: 200,       # 200 images per month
        UsageType.HASHTAG: -1,      # Unlimited
        UsageType.POST: -1,         # Unlimited
        UsageType.ANALYTICS: 1,     # Full analytics
    }
}
