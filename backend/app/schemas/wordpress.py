"""
WordPress schemas for request/response validation
"""
from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional, List


class WordPressAccountCreate(BaseModel):
    """Schema for creating a WordPress account connection"""
    site_url: str
    username: str
    app_password: str
    site_name: Optional[str] = None

    @field_validator('site_url')
    @classmethod
    def validate_site_url(cls, v: str) -> str:
        """Ensure site URL is properly formatted"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Site URL must start with http:// or https://')
        return v.rstrip('/')


class WordPressAccountResponse(BaseModel):
    """Schema for WordPress account response"""
    id: int
    site_url: str
    site_name: Optional[str]
    username: str
    is_active: bool
    last_sync: Optional[str]

    class Config:
        from_attributes = True


class WordPressPublishRequest(BaseModel):
    """Schema for publishing content to WordPress"""
    wordpress_account_id: int
    title: str
    content: str
    excerpt: Optional[str] = None
    status: str = "draft"  # draft, publish, pending, private
    categories: Optional[List[int]] = None
    tags: Optional[List[str]] = None  # Tag names (will be created if don't exist)
    featured_image_url: Optional[str] = None

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate post status"""
        allowed_statuses = ['draft', 'publish', 'pending', 'private']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {", ".join(allowed_statuses)}')
        return v


class WordPressPublishResponse(BaseModel):
    """Schema for WordPress publish response"""
    success: bool
    post_id: Optional[int] = None
    post_url: Optional[str] = None
    status: Optional[str] = None
    error: Optional[str] = None


class WordPressCategoryResponse(BaseModel):
    """Schema for WordPress category"""
    id: int
    name: str
    slug: str
    count: int


class WordPressTagResponse(BaseModel):
    """Schema for WordPress tag"""
    id: int
    name: str
    slug: str
    count: int


class WordPressTestConnectionResponse(BaseModel):
    """Schema for connection test response"""
    success: bool
    site_name: Optional[str] = None
    site_description: Optional[str] = None
    api_available: bool
    error: Optional[str] = None
