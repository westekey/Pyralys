"""
WordPress integration endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.wordpress_account import WordPressAccount
from app.schemas.wordpress import (
    WordPressAccountCreate,
    WordPressAccountResponse,
    WordPressPublishRequest,
    WordPressPublishResponse,
    WordPressCategoryResponse,
    WordPressTagResponse,
    WordPressTestConnectionResponse
)
from app.services.wordpress_service import WordPressService

router = APIRouter()


@router.post("/accounts", response_model=WordPressAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_wordpress_account(
    account_data: WordPressAccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Connect a WordPress site to your account

    Requires WordPress Application Password:
    1. Go to your WordPress site
    2. Navigate to Users > Profile
    3. Scroll to "Application Passwords"
    4. Create a new application password
    5. Use that password here
    """
    # Create temporary account for testing
    temp_account = WordPressAccount(
        user_id=current_user.id,
        site_url=account_data.site_url,
        username=account_data.username,
        app_password=account_data.app_password,
        site_name=account_data.site_name
    )

    # Test the connection
    wp_service = WordPressService(temp_account)
    test_result = await wp_service.test_connection()

    if not test_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to connect to WordPress site: {test_result.get('error', 'Unknown error')}"
        )

    # Update site name from WordPress if not provided
    if not account_data.site_name:
        temp_account.site_name = test_result.get("site_name", "")

    # Save to database
    db.add(temp_account)
    await db.commit()
    await db.refresh(temp_account)

    return temp_account


@router.get("/accounts", response_model=List[WordPressAccountResponse])
async def get_wordpress_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all connected WordPress sites
    """
    result = await db.execute(
        select(WordPressAccount)
        .where(WordPressAccount.user_id == current_user.id)
        .where(WordPressAccount.is_active == True)
    )
    accounts = result.scalars().all()
    return accounts


@router.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wordpress_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Disconnect a WordPress site
    """
    result = await db.execute(
        select(WordPressAccount)
        .where(WordPressAccount.id == account_id)
        .where(WordPressAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WordPress account not found"
        )

    await db.delete(account)
    await db.commit()


@router.post("/accounts/{account_id}/test", response_model=WordPressTestConnectionResponse)
async def test_wordpress_connection(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Test connection to a WordPress site
    """
    result = await db.execute(
        select(WordPressAccount)
        .where(WordPressAccount.id == account_id)
        .where(WordPressAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WordPress account not found"
        )

    wp_service = WordPressService(account)
    test_result = await wp_service.test_connection()

    return test_result


@router.get("/accounts/{account_id}/categories", response_model=List[WordPressCategoryResponse])
async def get_wordpress_categories(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all categories from a WordPress site
    """
    result = await db.execute(
        select(WordPressAccount)
        .where(WordPressAccount.id == account_id)
        .where(WordPressAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WordPress account not found"
        )

    wp_service = WordPressService(account)
    categories = await wp_service.get_categories()

    return categories


@router.get("/accounts/{account_id}/tags", response_model=List[WordPressTagResponse])
async def get_wordpress_tags(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all tags from a WordPress site
    """
    result = await db.execute(
        select(WordPressAccount)
        .where(WordPressAccount.id == account_id)
        .where(WordPressAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WordPress account not found"
        )

    wp_service = WordPressService(account)
    tags = await wp_service.get_tags()

    return tags


@router.post("/publish", response_model=WordPressPublishResponse)
async def publish_to_wordpress(
    publish_data: WordPressPublishRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Publish content to WordPress

    This can be used to publish AI-generated content or any custom content
    """
    # Get WordPress account
    result = await db.execute(
        select(WordPressAccount)
        .where(WordPressAccount.id == publish_data.wordpress_account_id)
        .where(WordPressAccount.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WordPress account not found"
        )

    # Create WordPress service
    wp_service = WordPressService(account)

    # Create tag IDs from tag names
    tag_ids = []
    if publish_data.tags:
        for tag_name in publish_data.tags:
            tag_id = await wp_service.create_tag(tag_name)
            if tag_id:
                tag_ids.append(tag_id)

    # Download featured image if URL provided
    featured_media_id = None
    if publish_data.featured_image_url:
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                img_response = await client.get(publish_data.featured_image_url)
                img_response.raise_for_status()
                image_data = img_response.content

                upload_result = await wp_service.upload_image(
                    image_data=image_data,
                    filename=f"post-image-{publish_data.title[:30]}.jpg",
                    alt_text=publish_data.title
                )

                if upload_result["success"]:
                    featured_media_id = upload_result["media_id"]
        except Exception as e:
            # Continue without image if upload fails
            pass

    # Create the post
    result = await wp_service.create_post(
        title=publish_data.title,
        content=publish_data.content,
        status=publish_data.status,
        excerpt=publish_data.excerpt,
        categories=publish_data.categories,
        tags=tag_ids if tag_ids else None,
        featured_media=featured_media_id
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to publish to WordPress: {result.get('error', 'Unknown error')}"
        )

    return result
