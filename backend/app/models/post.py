"""
Post model for content management
"""
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum
import uuid

from app.models.base import Base, TimestampMixin


class PostStatus(str, enum.Enum):
    """Post status types"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    ARCHIVED = "archived"


class PostType(str, enum.Enum):
    """Post content types"""
    PHOTO = "photo"
    CAROUSEL = "carousel"
    VIDEO = "video"
    STORY = "story"
    ARTICLE = "article"  # For WordPress


class Post(Base, TimestampMixin):
    """Post model for storing content"""
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # Content
    title = Column(String(500), nullable=True)
    caption = Column(Text, nullable=True)  # Main content/caption
    content = Column(Text, nullable=True)  # Full content for articles
    hashtags = Column(JSONB, default=list)  # List of hashtags

    # Post metadata
    post_type = Column(SQLEnum(PostType), default=PostType.PHOTO, nullable=False)
    status = Column(SQLEnum(PostStatus), default=PostStatus.DRAFT, nullable=False, index=True)

    # Media URLs (for backward compatibility and quick access)
    media_urls = Column(JSONB, default=list)

    # Target platforms
    target_platforms = Column(JSONB, default=list)  # ['instagram', 'wordpress', etc.]

    # AI Generation metadata
    ai_generated = Column(Boolean, default=False)
    ai_prompt = Column(Text, nullable=True)
    generation_params = Column(JSONB, nullable=True)  # Store full AI generation params

    # Scheduling
    scheduled_at = Column(String(50), nullable=True)  # ISO datetime for scheduled posts
    published_at = Column(String(50), nullable=True)  # ISO datetime when published

    # Relationships
    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post", cascade="all, delete-orphan")
    publications = relationship("PostPublication", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post {self.id} - {self.status}>"

    @property
    def is_published(self):
        """Check if post has been published"""
        return self.status == PostStatus.PUBLISHED

    @property
    def is_scheduled(self):
        """Check if post is scheduled"""
        return self.status == PostStatus.SCHEDULED


class Media(Base, TimestampMixin):
    """Media files associated with posts"""
    __tablename__ = "media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # File info
    filename = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)  # URL to access the file
    file_path = Column(String(500), nullable=True)  # Local path if stored locally
    file_type = Column(String(50), nullable=False)  # image/jpeg, image/png, video/mp4
    file_size = Column(Integer, nullable=True)  # Size in bytes

    # Image metadata
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    alt_text = Column(String(255), nullable=True)

    # AI Generated
    ai_generated = Column(Boolean, default=False)
    ai_prompt = Column(Text, nullable=True)

    # Order in carousel
    order = Column(Integer, default=0)

    # Relationships
    post = relationship("Post", back_populates="media")
    user = relationship("User", back_populates="media")

    def __repr__(self):
        return f"<Media {self.id} - {self.filename}>"

    @property
    def is_image(self):
        """Check if media is an image"""
        return self.file_type.startswith("image/")

    @property
    def is_video(self):
        """Check if media is a video"""
        return self.file_type.startswith("video/")


class PostPublication(Base, TimestampMixin):
    """Track publications across different platforms"""
    __tablename__ = "post_publications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False, index=True)

    # Platform info
    platform = Column(String(50), nullable=False, index=True)  # wordpress, instagram, linkedin, facebook
    platform_post_id = Column(String(255), nullable=True)  # ID on the platform
    platform_url = Column(String(500), nullable=True)  # URL to the published post

    # Account used
    account_id = Column(String(255), nullable=True)  # Generic account ID
    account_username = Column(String(255), nullable=True)

    # Publication status
    published = Column(Boolean, default=False)
    published_at = Column(String(50), nullable=True)  # ISO datetime
    error_message = Column(Text, nullable=True)

    # Insights (if available)
    insights = Column(JSONB, nullable=True)  # Store platform insights

    # Relationships
    post = relationship("Post", back_populates="publications")

    def __repr__(self):
        return f"<PostPublication {self.platform} - {self.platform_post_id}>"
