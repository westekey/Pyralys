"""
Content/Post schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class PostCreate(BaseModel):
    """Schema for creating a post"""
    title: Optional[str] = None
    caption: str
    media_urls: List[str] = []
    platform: str
    ai_generated: bool = False
    generation_params: Optional[dict] = None


class PostUpdate(BaseModel):
    """Schema for updating a post"""
    title: Optional[str] = None
    caption: Optional[str] = None
    media_urls: Optional[List[str]] = None


class PostResponse(BaseModel):
    """Schema for post response"""
    id: str
    user_id: str
    title: Optional[str]
    caption: str
    media_urls: List[str]
    platform: str
    status: str
    scheduled_at: Optional[datetime]
    published_at: Optional[datetime]
    ai_generated: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
