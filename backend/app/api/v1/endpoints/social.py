"""
Social media accounts management endpoints
"""
from typing import List
from fastapi import APIRouter, HTTPException, status

from app.schemas.social import SocialAccountResponse

router = APIRouter()


@router.get("/instagram/auth-url")
async def get_instagram_auth_url():
    """
    Get Instagram OAuth authorization URL
    """
    # TODO: Generate Instagram OAuth URL
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Instagram OAuth not yet implemented"
    )


@router.get("/instagram/callback")
async def instagram_oauth_callback(code: str, state: str = None):
    """
    Handle Instagram OAuth callback
    """
    # TODO: Handle OAuth callback
    # 1. Exchange code for access token
    # 2. Get long-lived token
    # 3. Fetch user's Instagram accounts
    # 4. Store account info

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Instagram OAuth callback not yet implemented"
    )


@router.get("/accounts", response_model=List[SocialAccountResponse])
async def list_connected_accounts():
    """
    List all connected social media accounts
    """
    # TODO: Implement account listing
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Account listing not yet implemented"
    )


@router.delete("/accounts/{account_id}")
async def disconnect_account(account_id: str):
    """
    Disconnect a social media account
    """
    # TODO: Implement account disconnection
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Account disconnection not yet implemented"
    )


@router.post("/accounts/{account_id}/refresh")
async def refresh_account_token(account_id: str):
    """
    Refresh access token for an account
    """
    # TODO: Implement token refresh
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh not yet implemented"
    )
