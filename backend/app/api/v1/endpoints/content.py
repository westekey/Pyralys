"""
Content management endpoints - Post CRUD operations
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.post import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostPublishRequest,
    MediaCreate,
    MediaResponse
)
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.post_service import PostService

router = APIRouter()


@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new post (draft)

    - **title**: Optional post title
    - **caption**: Post caption text
    - **content**: Post content (for blog-style posts)
    - **hashtags**: List of hashtags
    - **post_type**: Type of post (photo, video, carousel, story)
    - **target_platforms**: Platforms to publish to (instagram, tiktok, linkedin, facebook, wordpress)
    - **media_urls**: URLs of uploaded media files
    - **scheduled_at**: Optional ISO datetime string for scheduling
    """
    post_service = PostService(db)

    try:
        post = await post_service.create_post(current_user, post_data)

        # Convert to response model
        return PostResponse(
            id=str(post.id),
            user_id=str(post.user_id),
            title=post.title,
            caption=post.caption,
            content=post.content,
            hashtags=post.hashtags or [],
            post_type=post.post_type.value,
            status=post.status.value,
            media_urls=post.media_urls or [],
            target_platforms=post.target_platforms or [],
            ai_generated=post.ai_generated,
            generation_params=post.generation_params,
            scheduled_at=post.scheduled_at,
            published_at=post.published_at,
            created_at=post.created_at,
            updated_at=post.updated_at,
            media=[],
            publications=[]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating post: {str(e)}"
        )


@router.get("/posts", response_model=List[PostResponse])
async def list_posts(
    status_filter: Optional[str] = Query(None, alias="status"),
    platform: Optional[str] = None,
    post_type: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List user's posts with optional filters

    - **status**: Filter by status (draft, scheduled, published, failed, archived)
    - **platform**: Filter by platform (instagram, tiktok, linkedin, facebook, wordpress)
    - **post_type**: Filter by type (photo, video, carousel, story)
    - **search**: Search in title and caption
    - **skip**: Number of posts to skip (pagination)
    - **limit**: Maximum number of posts to return (max 100)
    """
    post_service = PostService(db)

    try:
        # Limit max to 100
        limit = min(limit, 100)

        posts, total = await post_service.list_posts(
            user=current_user,
            status=status_filter,
            platform=platform,
            post_type=post_type,
            search=search,
            skip=skip,
            limit=limit
        )

        # Convert to response models
        return [
            PostResponse(
                id=str(post.id),
                user_id=str(post.user_id),
                title=post.title,
                caption=post.caption,
                content=post.content,
                hashtags=post.hashtags or [],
                post_type=post.post_type.value,
                status=post.status.value,
                media_urls=post.media_urls or [],
                target_platforms=post.target_platforms or [],
                ai_generated=post.ai_generated,
                generation_params=post.generation_params,
                scheduled_at=post.scheduled_at,
                published_at=post.published_at,
                created_at=post.created_at,
                updated_at=post.updated_at,
                media=[
                    MediaResponse(
                        id=str(m.id),
                        post_id=str(m.post_id),
                        user_id=str(m.user_id),
                        file_url=m.file_url,
                        file_type=m.file_type.value,
                        file_size=m.file_size,
                        width=m.width,
                        height=m.height,
                        duration=m.duration,
                        order_position=m.order_position,
                        ai_generated=m.ai_generated,
                        generation_prompt=m.generation_prompt,
                        created_at=m.created_at
                    ) for m in (post.media or [])
                ],
                publications=[]
            ) for post in posts
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing posts: {str(e)}"
        )


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific post by ID with all relations (media, publications)
    """
    post_service = PostService(db)

    post = await post_service.get_post(post_id, current_user, include_relations=True)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Convert to response model with full relations
    return PostResponse(
        id=str(post.id),
        user_id=str(post.user_id),
        title=post.title,
        caption=post.caption,
        content=post.content,
        hashtags=post.hashtags or [],
        post_type=post.post_type.value,
        status=post.status.value,
        media_urls=post.media_urls or [],
        target_platforms=post.target_platforms or [],
        ai_generated=post.ai_generated,
        generation_params=post.generation_params,
        scheduled_at=post.scheduled_at,
        published_at=post.published_at,
        created_at=post.created_at,
        updated_at=post.updated_at,
        media=[
            MediaResponse(
                id=str(m.id),
                post_id=str(m.post_id),
                user_id=str(m.user_id),
                file_url=m.file_url,
                file_type=m.file_type.value,
                file_size=m.file_size,
                width=m.width,
                height=m.height,
                duration=m.duration,
                order_position=m.order_position,
                ai_generated=m.ai_generated,
                generation_prompt=m.generation_prompt,
                created_at=m.created_at
            ) for m in (post.media or [])
        ],
        publications=[
            {
                "id": str(p.id),
                "post_id": str(p.post_id),
                "platform": p.platform,
                "platform_post_id": p.platform_post_id,
                "platform_url": p.platform_url,
                "status": p.status,
                "error_message": p.error_message,
                "published_at": p.published_at,
                "insights": p.insights or {},
                "created_at": p.created_at,
                "updated_at": p.updated_at
            } for p in (post.publications or [])
        ]
    )


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a post

    Only draft and failed posts can be fully edited.
    Published posts can only update certain fields.
    """
    post_service = PostService(db)

    try:
        post = await post_service.update_post(post_id, current_user, post_data)

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )

        return PostResponse(
            id=str(post.id),
            user_id=str(post.user_id),
            title=post.title,
            caption=post.caption,
            content=post.content,
            hashtags=post.hashtags or [],
            post_type=post.post_type.value,
            status=post.status.value,
            media_urls=post.media_urls or [],
            target_platforms=post.target_platforms or [],
            ai_generated=post.ai_generated,
            generation_params=post.generation_params,
            scheduled_at=post.scheduled_at,
            published_at=post.published_at,
            created_at=post.created_at,
            updated_at=post.updated_at,
            media=[],
            publications=[]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating post: {str(e)}"
        )


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a post

    This will also delete all associated media and publication records.
    """
    post_service = PostService(db)

    success = await post_service.delete_post(post_id, current_user)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return None


@router.post("/posts/{post_id}/media", response_model=MediaResponse, status_code=status.HTTP_201_CREATED)
async def add_media_to_post(
    post_id: str,
    media_data: MediaCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add media file to a post

    - **file_url**: URL of the uploaded media file
    - **file_type**: Type of file (image or video)
    - **order_position**: Position in carousel (0-9)
    """
    post_service = PostService(db)

    try:
        media = await post_service.add_media(
            post_id=post_id,
            user=current_user,
            file_url=media_data.file_url,
            file_type=media_data.file_type,
            file_size=media_data.file_size,
            width=media_data.width,
            height=media_data.height,
            duration=media_data.duration,
            order_position=media_data.order_position,
            ai_generated=media_data.ai_generated,
            generation_prompt=media_data.generation_prompt
        )

        if not media:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )

        return MediaResponse(
            id=str(media.id),
            post_id=str(media.post_id),
            user_id=str(media.user_id),
            file_url=media.file_url,
            file_type=media.file_type.value,
            file_size=media.file_size,
            width=media.width,
            height=media.height,
            duration=media.duration,
            order_position=media.order_position,
            ai_generated=media.ai_generated,
            generation_prompt=media.generation_prompt,
            created_at=media.created_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding media: {str(e)}"
        )


@router.post("/posts/{post_id}/publish")
async def publish_post(
    post_id: str,
    publish_request: PostPublishRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Publish a post to specified platforms

    - **platforms**: List of platforms to publish to
    - **publish_immediately**: If true, publish now; if false, schedule for later
    - **scheduled_for**: ISO datetime string for scheduled publishing

    Note: Actual publishing logic will be implemented in Sprint 5 with Celery tasks
    """
    post_service = PostService(db)

    # Get the post
    post = await post_service.get_post(post_id, current_user)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Validate platforms
    valid_platforms = ["instagram", "tiktok", "linkedin", "facebook", "wordpress"]
    for platform in publish_request.platforms:
        if platform not in valid_platforms:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid platform: {platform}"
            )

    # TODO: Implement actual publishing logic with Celery (Sprint 5)
    # For now, just create publication records
    publications = []
    for platform in publish_request.platforms:
        publication = await post_service.create_publication_record(
            post_id=post_id,
            platform=platform,
            status="pending"
        )
        publications.append({
            "id": str(publication.id),
            "platform": publication.platform,
            "status": publication.status
        })

    return {
        "message": "Post queued for publishing",
        "post_id": str(post.id),
        "platforms": publish_request.platforms,
        "scheduled": not publish_request.publish_immediately,
        "scheduled_for": publish_request.scheduled_for if not publish_request.publish_immediately else None,
        "publications": publications
    }


@router.post("/posts/{post_id}/schedule")
async def schedule_post(
    post_id: str,
    scheduled_at: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Schedule a post for future publishing

    - **scheduled_at**: ISO datetime string (e.g., "2025-02-01T10:00:00")

    Note: Actual scheduling logic will be implemented in Sprint 5 with Celery Beat
    """
    post_service = PostService(db)

    # Update post with scheduled time
    post_data = PostUpdate(
        scheduled_at=scheduled_at,
        status="scheduled"
    )

    post = await post_service.update_post(post_id, current_user, post_data)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return {
        "message": "Post scheduled successfully",
        "post_id": str(post.id),
        "scheduled_at": scheduled_at,
        "status": post.status.value
    }


@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload media file (image/video)

    Returns the URL of the uploaded file.

    Note: This is a placeholder. Actual implementation will use:
    - AWS S3 for production
    - Local storage or MinIO for development
    """
    # TODO: Implement actual file upload to S3/MinIO
    # For now, return a mock response

    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp", "video/mp4", "video/quicktime"]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )

    # TODO: Upload to S3 and get URL
    mock_url = f"https://storage.pyralys.com/uploads/{current_user.id}/{file.filename}"

    return {
        "url": mock_url,
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "File upload will be implemented with S3 integration"
    }


@router.get("/calendar")
async def get_calendar(
    start_date: str,
    end_date: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get scheduled posts in calendar format

    - **start_date**: Start date in ISO format (e.g., "2025-02-01")
    - **end_date**: End date in ISO format (e.g., "2025-02-28")

    Returns posts grouped by date for calendar display
    """
    post_service = PostService(db)

    # Get scheduled and published posts in date range
    posts, _ = await post_service.list_posts(
        user=current_user,
        status="scheduled",
        limit=1000  # Get all in range
    )

    # TODO: Filter by date range and group by date
    # For now, return simple list

    calendar_data = {}
    for post in posts:
        if post.scheduled_at:
            date_key = post.scheduled_at.split("T")[0]  # Extract date part
            if date_key not in calendar_data:
                calendar_data[date_key] = []

            calendar_data[date_key].append({
                "id": str(post.id),
                "title": post.title,
                "caption": post.caption[:100] if post.caption else None,
                "post_type": post.post_type.value,
                "platforms": post.target_platforms or [],
                "scheduled_at": post.scheduled_at
            })

    return {
        "start_date": start_date,
        "end_date": end_date,
        "calendar": calendar_data
    }


@router.get("/stats")
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's content statistics

    Returns counts by status, platform, and type
    """
    post_service = PostService(db)

    stats = await post_service.get_stats(current_user)

    return stats
