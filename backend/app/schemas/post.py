"""
Post schemas for request/response validation
"""
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime


class MediaBase(BaseModel):
    """Base schema for media"""
    filename: str
    file_url: str
    file_type: str
    alt_text: Optional[str] = None
    order: int = 0


class MediaCreate(MediaBase):
    """Schema for creating media"""
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    ai_generated: bool = False
    ai_prompt: Optional[str] = None


class MediaResponse(MediaBase):
    """Schema for media response"""
    id: str
    post_id: str
    user_id: str
    file_size: Optional[int]
    width: Optional[int]
    height: Optional[int]
    ai_generated: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class PostPublicationResponse(BaseModel):
    """Schema for post publication response"""
    id: str
    post_id: str
    platform: str
    platform_post_id: Optional[str]
    platform_url: Optional[str]
    account_username: Optional[str]
    published: bool
    published_at: Optional[str]
    error_message: Optional[str]
    insights: Optional[dict]

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    """Schema for creating a post"""
    title: Optional[str] = None
    caption: Optional[str] = None
    content: Optional[str] = None
    hashtags: List[str] = []
    post_type: str = "photo"  # photo, carousel, video, story, article
    target_platforms: List[str] = []
    ai_generated: bool = False
    ai_prompt: Optional[str] = None
    generation_params: Optional[dict] = None
    media_urls: List[str] = []
    scheduled_at: Optional[str] = None

    @field_validator('post_type')
    @classmethod
    def validate_post_type(cls, v: str) -> str:
        allowed_types = ['photo', 'carousel', 'video', 'story', 'article']
        if v not in allowed_types:
            raise ValueError(f'Post type must be one of: {", ".join(allowed_types)}')
        return v


class PostUpdate(BaseModel):
    """Schema for updating a post"""
    title: Optional[str] = None
    caption: Optional[str] = None
    content: Optional[str] = None
    hashtags: Optional[List[str]] = None
    post_type: Optional[str] = None
    status: Optional[str] = None
    target_platforms: Optional[List[str]] = None
    media_urls: Optional[List[str]] = None
    scheduled_at: Optional[str] = None

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        allowed_statuses = ['draft', 'scheduled', 'published', 'failed', 'archived']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {", ".join(allowed_statuses)}')
        return v


class PostResponse(BaseModel):
    """Schema for post response"""
    id: str
    user_id: str
    title: Optional[str]
    caption: Optional[str]
    content: Optional[str]
    hashtags: List[str]
    post_type: str
    status: str
    media_urls: List[str]
    target_platforms: List[str]
    ai_generated: bool
    ai_prompt: Optional[str]
    generation_params: Optional[dict]
    scheduled_at: Optional[str]
    published_at: Optional[str]
    created_at: str
    updated_at: str
    media: List[MediaResponse] = []
    publications: List[PostPublicationResponse] = []

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    """Schema for list of posts"""
    total: int
    posts: List[PostResponse]
    page: int
    page_size: int


class PostPublishRequest(BaseModel):
    """Schema for publishing a post to platforms"""
    platforms: List[str]  # List of platforms to publish to
    publish_immediately: bool = True
    scheduled_for: Optional[str] = None  # ISO datetime for scheduling

    @field_validator('platforms')
    @classmethod
    def validate_platforms(cls, v: List[str]) -> List[str]:
        allowed_platforms = ['wordpress', 'instagram', 'linkedin', 'facebook', 'tiktok']
        for platform in v:
            if platform not in allowed_platforms:
                raise ValueError(f'Platform must be one of: {", ".join(allowed_platforms)}')
        return v


class PostPublishResponse(BaseModel):
    """Schema for post publish response"""
    success: bool
    post_id: str
    published_platforms: List[str] = []
    failed_platforms: List[dict] = []  # [{"platform": "instagram", "error": "..."}]
    message: str
