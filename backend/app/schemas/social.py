"""
Social account schemas
"""
from datetime import datetime
from pydantic import BaseModel


class SocialAccountResponse(BaseModel):
    """Schema for social account response"""
    id: str
    platform: str
    account_username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
