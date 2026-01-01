"""
Publishing tasks for multi-platform content distribution
Handles async publishing to Instagram, WordPress, TikTok, LinkedIn, Facebook
"""
import asyncio
from typing import Dict, Optional
from celery import Task
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.celery_app import celery_app
from app.core.config import settings
from app.models.post import Post, PostStatus
from app.models.user import User
from app.models.instagram_account import InstagramAccount
from app.models.wordpress_account import WordPressAccount
from app.services.instagram_service import InstagramService
from app.services.wordpress_service import WordPressService
from app.services.post_service import PostService


# Create async engine for Celery tasks
async_engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class AsyncTask(Task):
    """Base task class that properly handles async operations"""

    def __call__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run_async(*args, **kwargs))


@celery_app.task(base=AsyncTask, bind=True, max_retries=3)
async def publish_to_instagram(self, post_id: str, user_id: str) -> Dict:
    """
    Publish a post to Instagram

    Args:
        post_id: Post UUID
        user_id: User UUID

    Returns:
        Dict with publication result
    """
    async with AsyncSessionLocal() as db:
        try:
            post_service = PostService(db)

            # Get post
            post = await db.get(Post, post_id)
            if not post or str(post.user_id) != user_id:
                return {"success": False, "error": "Post not found"}

            # Get user's Instagram account
            user = await db.get(User, user_id)
            instagram_account = await db.query(InstagramAccount).filter(
                InstagramAccount.user_id == user.id,
                InstagramAccount.is_active == True
            ).first()

            if not instagram_account:
                await post_service.create_publication_record(
                    post_id=post_id,
                    platform="instagram",
                    status="failed",
                    error_message="No active Instagram account found"
                )
                return {"success": False, "error": "No Instagram account connected"}

            # Initialize Instagram service
            instagram_service = InstagramService(
                instagram_user_id=instagram_account.instagram_user_id,
                access_token=instagram_account.access_token
            )

            # Publish based on post type
            result = None

            if post.post_type.value == "carousel" and len(post.media_urls) > 1:
                # Publish carousel
                result = await instagram_service.publish_carousel(
                    images=post.media_urls,
                    caption=post.caption,
                    hashtags=post.hashtags
                )
            elif post.post_type.value == "story":
                # Publish story
                if post.media_urls:
                    media_type = "VIDEO" if post.media_urls[0].endswith(('.mp4', '.mov')) else "IMAGE"
                    result = await instagram_service.publish_story(
                        media_url=post.media_urls[0],
                        media_type=media_type
                    )
            else:
                # Publish single photo/video
                if post.media_urls:
                    result = await instagram_service.publish_photo(
                        image_url=post.media_urls[0],
                        caption=post.caption,
                        hashtags=post.hashtags
                    )

            if result and result.get('id'):
                # Update publication record
                publication = await post_service.create_publication_record(
                    post_id=post_id,
                    platform="instagram",
                    platform_post_id=result.get('id'),
                    platform_url=result.get('permalink') or f"https://instagram.com/p/{result.get('id')}",
                    status="published"
                )

                # Update post status
                post.status = PostStatus.PUBLISHED
                post.published_at = datetime.utcnow().isoformat()
                await db.commit()

                return {
                    "success": True,
                    "platform": "instagram",
                    "post_id": post_id,
                    "platform_post_id": result.get('id'),
                    "url": result.get('permalink')
                }
            else:
                error_msg = result.get('error', {}).get('message', 'Unknown error') if result else 'No result'
                await post_service.create_publication_record(
                    post_id=post_id,
                    platform="instagram",
                    status="failed",
                    error_message=error_msg
                )
                return {"success": False, "error": error_msg}

        except Exception as e:
            # Retry on failure
            if self.request.retries < self.max_retries:
                raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))

            # Final failure
            await post_service.create_publication_record(
                post_id=post_id,
                platform="instagram",
                status="failed",
                error_message=str(e)
            )
            return {"success": False, "error": str(e)}


@celery_app.task(base=AsyncTask, bind=True, max_retries=3)
async def publish_to_wordpress(self, post_id: str, user_id: str) -> Dict:
    """
    Publish a post to WordPress

    Args:
        post_id: Post UUID
        user_id: User UUID

    Returns:
        Dict with publication result
    """
    async with AsyncSessionLocal() as db:
        try:
            post_service = PostService(db)

            # Get post
            post = await db.get(Post, post_id)
            if not post or str(post.user_id) != user_id:
                return {"success": False, "error": "Post not found"}

            # Get user's WordPress account
            user = await db.get(User, user_id)
            wordpress_account = await db.query(WordPressAccount).filter(
                WordPressAccount.user_id == user.id,
                WordPressAccount.is_active == True
            ).first()

            if not wordpress_account:
                await post_service.create_publication_record(
                    post_id=post_id,
                    platform="wordpress",
                    status="failed",
                    error_message="No active WordPress account found"
                )
                return {"success": False, "error": "No WordPress account connected"}

            # Initialize WordPress service
            wordpress_service = WordPressService(
                site_url=wordpress_account.site_url,
                username=wordpress_account.username,
                app_password=wordpress_account.app_password
            )

            # Prepare content
            content = post.content or post.caption or ""
            if post.hashtags:
                content += "\n\n" + " ".join([f"#{tag}" for tag in post.hashtags])

            # Upload featured image if available
            featured_media_id = None
            if post.media_urls:
                # TODO: Download and upload image to WordPress
                # For now, we'll just create the post without featured image
                pass

            # Create WordPress post
            result = await wordpress_service.create_post(
                title=post.title or "Untitled Post",
                content=content,
                status="publish",
                featured_media=featured_media_id
            )

            if result and result.get('id'):
                # Update publication record
                publication = await post_service.create_publication_record(
                    post_id=post_id,
                    platform="wordpress",
                    platform_post_id=str(result.get('id')),
                    platform_url=result.get('link'),
                    status="published"
                )

                # Update post status
                post.status = PostStatus.PUBLISHED
                post.published_at = datetime.utcnow().isoformat()
                await db.commit()

                return {
                    "success": True,
                    "platform": "wordpress",
                    "post_id": post_id,
                    "platform_post_id": result.get('id'),
                    "url": result.get('link')
                }
            else:
                error_msg = result.get('message', 'Unknown error') if result else 'No result'
                await post_service.create_publication_record(
                    post_id=post_id,
                    platform="wordpress",
                    status="failed",
                    error_message=error_msg
                )
                return {"success": False, "error": error_msg}

        except Exception as e:
            # Retry on failure
            if self.request.retries < self.max_retries:
                raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))

            # Final failure
            await post_service.create_publication_record(
                post_id=post_id,
                platform="wordpress",
                status="failed",
                error_message=str(e)
            )
            return {"success": False, "error": str(e)}


@celery_app.task(base=AsyncTask, bind=True)
async def publish_to_multiple_platforms(self, post_id: str, user_id: str, platforms: list) -> Dict:
    """
    Publish a post to multiple platforms simultaneously

    Args:
        post_id: Post UUID
        user_id: User UUID
        platforms: List of platform names

    Returns:
        Dict with results for each platform
    """
    results = {}
    tasks = []

    # Map platforms to their publishing tasks
    platform_tasks = {
        'instagram': publish_to_instagram,
        'wordpress': publish_to_wordpress,
        # Add more platforms as they're implemented
        # 'tiktok': publish_to_tiktok,
        # 'linkedin': publish_to_linkedin,
        # 'facebook': publish_to_facebook,
    }

    # Queue tasks for each platform
    for platform in platforms:
        if platform in platform_tasks:
            task = platform_tasks[platform].apply_async(
                args=[post_id, user_id],
                countdown=0
            )
            tasks.append((platform, task))
        else:
            results[platform] = {
                "success": False,
                "error": f"Platform {platform} not yet implemented"
            }

    # Wait for all tasks to complete
    for platform, task in tasks:
        try:
            result = task.get(timeout=300)  # 5 minute timeout
            results[platform] = result
        except Exception as e:
            results[platform] = {
                "success": False,
                "error": str(e)
            }

    return {
        "post_id": post_id,
        "platforms": results,
        "total": len(platforms),
        "successful": sum(1 for r in results.values() if r.get('success')),
        "failed": sum(1 for r in results.values() if not r.get('success'))
    }
