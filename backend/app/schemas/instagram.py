"""
Instagram schemas for request/response validation
"""
from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class InstagramOAuthCallback(BaseModel):
    """Schema for Instagram OAuth callback"""
    code: str
    state: Optional[str] = None


class InstagramAccountResponse(BaseModel):
    """Schema for Instagram account response"""
    id: int
    instagram_user_id: str
    username: str
    account_type: Optional[str]
    profile_picture_url: Optional[str]
    followers_count: int
    follows_count: int
    media_count: int
    is_active: bool
    last_sync: Optional[str]

    class Config:
        from_attributes = True


class InstagramPublishPhotoRequest(BaseModel):
    """Schema for publishing a photo to Instagram"""
    instagram_account_id: int
    image_url: str
    caption: Optional[str] = None
    location_id: Optional[str] = None


class InstagramPublishCarouselRequest(BaseModel):
    """Schema for publishing a carousel to Instagram"""
    instagram_account_id: int
    images: List[str]
    caption: Optional[str] = None
    location_id: Optional[str] = None


class InstagramPublishStoryRequest(BaseModel):
    """Schema for publishing a story to Instagram"""
    instagram_account_id: int
    media_url: str
    media_type: str = "IMAGE"  # IMAGE or VIDEO


class InstagramPublishResponse(BaseModel):
    """Schema for Instagram publish response"""
    success: bool
    media_id: Optional[str] = None
    permalink: Optional[str] = None
    error: Optional[str] = None


class InstagramInsightsResponse(BaseModel):
    """Schema for Instagram insights response"""
    success: bool
    insights: Optional[dict] = None
    error: Optional[str] = None


class InstagramAccountInfoResponse(BaseModel):
    """Schema for Instagram account info response"""
    success: bool
    username: Optional[str] = None
    account_type: Optional[str] = None
    media_count: Optional[int] = None
    followers_count: Optional[int] = None
    follows_count: Optional[int] = None
    profile_picture_url: Optional[str] = None
    error: Optional[str] = None
