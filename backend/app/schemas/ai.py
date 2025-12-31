"""
AI generation schemas
"""
from typing import Optional, List
from pydantic import BaseModel


class CaptionGenerationRequest(BaseModel):
    """Request schema for caption generation"""
    prompt: str
    platform: str = "instagram"
    tone: str = "casual"
    user_context: Optional[dict] = None


class CaptionGenerationResponse(BaseModel):
    """Response schema for caption generation"""
    caption: str
    hashtags: List[str]
    metadata: dict


class ImageGenerationRequest(BaseModel):
    """Request schema for image generation"""
    prompt: str
    style: Optional[str] = None
    size: str = "1024x1024"


class ImageGenerationResponse(BaseModel):
    """Response schema for image generation"""
    image_url: str
    prompt_used: str


class HashtagGenerationRequest(BaseModel):
    """Request schema for hashtag generation"""
    topic: str
    platform: str = "instagram"
    count: int = 10


class HashtagGenerationResponse(BaseModel):
    """Response schema for hashtag generation"""
    hashtags: List[str]
