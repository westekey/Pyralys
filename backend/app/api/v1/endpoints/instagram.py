"""
Instagram integration endpoints with OAuth 2.0
"""
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import httpx
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.instagram_account import InstagramAccount
from app.schemas.instagram import (
    InstagramAccountResponse,
    InstagramPublishPhotoRequest,
    InstagramPublishCarouselRequest,
    InstagramPublishStoryRequest,
    InstagramPublishResponse,
    InstagramInsightsResponse,
    InstagramAccountInfoResponse
)
from app.services.instagram_service import InstagramService

router = APIRouter()

# Instagram OAuth Configuration
# Ces valeurs doivent être dans .env en production
INSTAGRAM_APP_ID = getattr(settings, "FACEBOOK_APP_ID", "YOUR_FB_APP_ID")
INSTAGRAM_APP_SECRET = getattr(settings, "FACEBOOK_APP_SECRET", "YOUR_FB_APP_SECRET")
INSTAGRAM_REDIRECT_URI = "http://localhost:8000/api/v1/instagram/oauth/callback"


@router.get("/oauth/authorize")
async def instagram_oauth_authorize(
    current_user: User = Depends(get_current_user)
):
    """
    Step 1: Redirect user to Instagram OAuth authorization page

    This initiates the OAuth flow. User will be redirected to Instagram
    to authorize the application.
    """
    # Generate state for CSRF protection (in production, store in session/db)
    state = f"user_{current_user.id}"

    # Instagram OAuth authorization URL
    auth_url = (
        f"https://api.instagram.com/oauth/authorize"
        f"?client_id={INSTAGRAM_APP_ID}"
        f"&redirect_uri={INSTAGRAM_REDIRECT_URI}"
        f"&scope=user_profile,user_media"
        f"&response_type=code"
        f"&state={state}"
    )

    return {
        "authorization_url": auth_url,
        "message": "Redirect user to this URL to authorize Instagram access"
    }


@router.get("/oauth/callback")
async def instagram_oauth_callback(
    code: str,
    state: str = None,
    error: str = None,
    error_reason: str = None,
    error_description: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Step 2: OAuth callback endpoint

    Instagram redirects here after user authorizes the app.
    This exchanges the authorization code for an access token.
    """
    # Handle authorization errors
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Instagram authorization failed: {error_description or error}"
        )

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code not provided"
        )

    try:
        # Step 1: Exchange code for short-lived token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://api.instagram.com/oauth/access_token",
                data={
                    "client_id": INSTAGRAM_APP_ID,
                    "client_secret": INSTAGRAM_APP_SECRET,
                    "grant_type": "authorization_code",
                    "redirect_uri": INSTAGRAM_REDIRECT_URI,
                    "code": code
                }
            )
            token_response.raise_for_status()
            token_data = token_response.json()

            short_lived_token = token_data.get("access_token")
            instagram_user_id = token_data.get("user_id")

            # Step 2: Exchange short-lived token for long-lived token (60 days)
            long_lived_response = await client.get(
                "https://graph.instagram.com/access_token",
                params={
                    "grant_type": "ig_exchange_token",
                    "client_secret": INSTAGRAM_APP_SECRET,
                    "access_token": short_lived_token
                }
            )
            long_lived_response.raise_for_status()
            long_lived_data = long_lived_response.json()

            access_token = long_lived_data.get("access_token")
            expires_in = long_lived_data.get("expires_in", 5184000)  # 60 days

            # Calculate expiration
            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

            # Step 3: Get user info
            user_info_response = await client.get(
                f"https://graph.instagram.com/{instagram_user_id}",
                params={
                    "fields": "username,account_type,media_count",
                    "access_token": access_token
                }
            )
            user_info_response.raise_for_status()
            user_info = user_info_response.json()

            # Extract user ID from state (in production, verify state properly)
            # Format: "user_{uuid}"
            user_id_str = state.replace("user_", "") if state else None

            if not user_id_str:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid state parameter"
                )

            # Check if account already exists
            result = await db.execute(
                select(InstagramAccount)
                .where(InstagramAccount.instagram_user_id == str(instagram_user_id))
            )
            existing_account = result.scalar_one_or_none()

            if existing_account:
                # Update existing account
                existing_account.access_token = access_token
                existing_account.token_expires_at = expires_at.isoformat()
                existing_account.username = user_info.get("username")
                existing_account.account_type = user_info.get("account_type")
                existing_account.is_active = True
                existing_account.last_sync = datetime.utcnow().isoformat()

                await db.commit()
                await db.refresh(existing_account)

                return RedirectResponse(
                    url=f"http://localhost:3000/dashboard?instagram_connected=true&username={existing_account.username}"
                )

            # Create new account
            new_account = InstagramAccount(
                user_id=user_id_str,
                instagram_user_id=str(instagram_user_id),
                username=user_info.get("username", ""),
                account_type=user_info.get("account_type"),
                access_token=access_token,
                token_expires_at=expires_at.isoformat(),
                media_count=user_info.get("media_count", 0),
                is_active=True,
                last_sync=datetime.utcnow().isoformat()
            )

            db.add(new_account)
            await db.commit()
            await db.refresh(new_account)

            # Redirect to frontend with success message
            return RedirectResponse(
                url=f"http://localhost:3000/dashboard?instagram_connected=true&username={new_account.username}"
            )

    except httpx.HTTPStatusError as e:
        error_detail = e.response.json() if e.response else str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Instagram OAuth failed: {error_detail}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to connect Instagram account: {str(e)}"
        )


@router.get("/accounts", response_model=List[InstagramAccountResponse])
async def get_instagram_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all connected Instagram accounts for the current user
    """
    result = await db.execute(
        select(InstagramAccount)
        .where(InstagramAccount.user_id == current_user.id)
        .where(InstagramAccount.is_active == True)
    )
    accounts = result.scalars().all()
    return accounts


@router.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instagram_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Disconnect an Instagram account
    """
    result = await db.execute(
        select(InstagramAccount)
        .where(InstagramAccount.id == account_id)
        .where(InstagramAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )

    await db.delete(account)
    await db.commit()


@router.post("/accounts/{account_id}/refresh", response_model=InstagramAccountResponse)
async def refresh_instagram_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh Instagram account info and extend access token
    """
    result = await db.execute(
        select(InstagramAccount)
        .where(InstagramAccount.id == account_id)
        .where(InstagramAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )

    # Refresh token
    ig_service = InstagramService(account)
    refresh_result = await ig_service.refresh_access_token()

    if refresh_result["success"]:
        account.access_token = refresh_result["access_token"]
        account.token_expires_at = refresh_result["expires_at"]

    # Update account info
    info_result = await ig_service.get_account_info()
    if info_result["success"]:
        account.username = info_result.get("username", account.username)
        account.account_type = info_result.get("account_type", account.account_type)
        account.followers_count = info_result.get("followers_count", 0)
        account.follows_count = info_result.get("follows_count", 0)
        account.media_count = info_result.get("media_count", 0)
        account.profile_picture_url = info_result.get("profile_picture_url")

    account.last_sync = datetime.utcnow().isoformat()

    await db.commit()
    await db.refresh(account)

    return account


@router.post("/publish/photo", response_model=InstagramPublishResponse)
async def publish_photo_to_instagram(
    publish_data: InstagramPublishPhotoRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Publish a photo to Instagram

    Note: Image must be hosted and publicly accessible.
    Instagram will download the image from the provided URL.
    """
    # Get Instagram account
    result = await db.execute(
        select(InstagramAccount)
        .where(InstagramAccount.id == publish_data.instagram_account_id)
        .where(InstagramAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )

    # Publish photo
    ig_service = InstagramService(account)
    result = await ig_service.publish_photo(
        image_url=publish_data.image_url,
        caption=publish_data.caption,
        location_id=publish_data.location_id
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to publish photo")
        )

    return result


@router.post("/publish/carousel", response_model=InstagramPublishResponse)
async def publish_carousel_to_instagram(
    publish_data: InstagramPublishCarouselRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Publish a carousel (album) to Instagram

    Carousel must contain 2-10 images.
    """
    # Get Instagram account
    result = await db.execute(
        select(InstagramAccount)
        .where(InstagramAccount.id == publish_data.instagram_account_id)
        .where(InstagramAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )

    # Publish carousel
    ig_service = InstagramService(account)
    result = await ig_service.publish_carousel(
        images=publish_data.images,
        caption=publish_data.caption,
        location_id=publish_data.location_id
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to publish carousel")
        )

    return result


@router.post("/publish/story", response_model=InstagramPublishResponse)
async def publish_story_to_instagram(
    publish_data: InstagramPublishStoryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Publish a story to Instagram

    Stories disappear after 24 hours.
    """
    # Get Instagram account
    result = await db.execute(
        select(InstagramAccount)
        .where(InstagramAccount.id == publish_data.instagram_account_id)
        .where(InstagramAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )

    # Publish story
    ig_service = InstagramService(account)
    result = await ig_service.publish_story(
        media_url=publish_data.media_url,
        media_type=publish_data.media_type
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to publish story")
        )

    return result


@router.get("/media/{media_id}/insights", response_model=InstagramInsightsResponse)
async def get_media_insights(
    media_id: str,
    instagram_account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get insights for a published Instagram media

    Only available for Business and Creator accounts.
    """
    # Get Instagram account
    result = await db.execute(
        select(InstagramAccount)
        .where(InstagramAccount.id == instagram_account_id)
        .where(InstagramAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )

    # Get insights
    ig_service = InstagramService(account)
    result = await ig_service.get_media_insights(media_id)

    return result
