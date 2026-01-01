"""
Scheduling tasks for managing scheduled posts
Handles periodic checks and cleanup
"""
import asyncio
from typing import List
from datetime import datetime, timedelta
from celery import Task
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, and_

from app.celery_app import celery_app
from app.core.config import settings
from app.models.post import Post, PostStatus
from app.tasks.publishing import publish_to_multiple_platforms


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


@celery_app.task(base=AsyncTask, name='app.tasks.scheduling.check_scheduled_posts')
async def check_scheduled_posts(self) -> dict:
    """
    Check for scheduled posts that are ready to be published
    Runs every minute via Celery Beat

    Returns:
        Dict with count of posts processed
    """
    async with AsyncSessionLocal() as db:
        try:
            current_time = datetime.utcnow()

            # Find all scheduled posts that are ready to publish
            stmt = select(Post).where(
                and_(
                    Post.status == PostStatus.SCHEDULED,
                    Post.scheduled_at != None,
                    Post.scheduled_at <= current_time.isoformat()
                )
            )

            result = await db.execute(stmt)
            scheduled_posts = result.scalars().all()

            published_count = 0
            failed_count = 0

            for post in scheduled_posts:
                try:
                    # Update status to publishing
                    post.status = PostStatus.PUBLISHED  # Will be updated by publishing tasks
                    await db.commit()

                    # Queue publishing task for each platform
                    if post.target_platforms:
                        publish_to_multiple_platforms.apply_async(
                            args=[str(post.id), str(post.user_id), post.target_platforms],
                            countdown=0
                        )
                        published_count += 1
                    else:
                        # No platforms specified, mark as failed
                        post.status = PostStatus.FAILED
                        await db.commit()
                        failed_count += 1

                except Exception as e:
                    print(f"Error processing post {post.id}: {str(e)}")
                    post.status = PostStatus.FAILED
                    await db.commit()
                    failed_count += 1

            return {
                "checked_at": current_time.isoformat(),
                "total_scheduled": len(scheduled_posts),
                "published": published_count,
                "failed": failed_count
            }

        except Exception as e:
            print(f"Error in check_scheduled_posts: {str(e)}")
            return {
                "error": str(e),
                "checked_at": datetime.utcnow().isoformat()
            }


@celery_app.task(base=AsyncTask, name='app.tasks.scheduling.schedule_post')
async def schedule_post(self, post_id: str, user_id: str, scheduled_at: str, platforms: list) -> dict:
    """
    Schedule a post for future publishing

    Args:
        post_id: Post UUID
        user_id: User UUID
        scheduled_at: ISO datetime string
        platforms: List of platforms to publish to

    Returns:
        Dict with scheduling result
    """
    async with AsyncSessionLocal() as db:
        try:
            # Get post
            post = await db.get(Post, post_id)
            if not post or str(post.user_id) != user_id:
                return {"success": False, "error": "Post not found"}

            # Update post with scheduling info
            post.status = PostStatus.SCHEDULED
            post.scheduled_at = scheduled_at
            post.target_platforms = platforms or post.target_platforms

            await db.commit()

            return {
                "success": True,
                "post_id": post_id,
                "scheduled_at": scheduled_at,
                "platforms": platforms,
                "message": "Post scheduled successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


@celery_app.task(base=AsyncTask, name='app.tasks.scheduling.cancel_scheduled_post')
async def cancel_scheduled_post(self, post_id: str, user_id: str) -> dict:
    """
    Cancel a scheduled post

    Args:
        post_id: Post UUID
        user_id: User UUID

    Returns:
        Dict with cancellation result
    """
    async with AsyncSessionLocal() as db:
        try:
            # Get post
            post = await db.get(Post, post_id)
            if not post or str(post.user_id) != user_id:
                return {"success": False, "error": "Post not found"}

            if post.status != PostStatus.SCHEDULED:
                return {"success": False, "error": "Post is not scheduled"}

            # Revert to draft
            post.status = PostStatus.DRAFT
            post.scheduled_at = None

            await db.commit()

            return {
                "success": True,
                "post_id": post_id,
                "message": "Scheduled post cancelled"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


@celery_app.task(base=AsyncTask, name='app.tasks.scheduling.cleanup_old_tasks')
async def cleanup_old_tasks(self) -> dict:
    """
    Clean up old published and failed posts
    Runs weekly via Celery Beat

    Returns:
        Dict with cleanup statistics
    """
    async with AsyncSessionLocal() as db:
        try:
            # Archive posts older than 90 days
            cutoff_date = (datetime.utcnow() - timedelta(days=90)).isoformat()

            stmt = select(Post).where(
                and_(
                    Post.status.in_([PostStatus.PUBLISHED, PostStatus.FAILED]),
                    Post.created_at < cutoff_date
                )
            )

            result = await db.execute(stmt)
            old_posts = result.scalars().all()

            archived_count = 0
            for post in old_posts:
                post.status = PostStatus.ARCHIVED
                archived_count += 1

            await db.commit()

            return {
                "cleanup_at": datetime.utcnow().isoformat(),
                "archived_count": archived_count,
                "cutoff_date": cutoff_date
            }

        except Exception as e:
            return {
                "error": str(e),
                "cleanup_at": datetime.utcnow().isoformat()
            }


@celery_app.task(base=AsyncTask, name='app.tasks.scheduling.reschedule_failed_post')
async def reschedule_failed_post(self, post_id: str, user_id: str, new_scheduled_at: str) -> dict:
    """
    Reschedule a failed post

    Args:
        post_id: Post UUID
        user_id: User UUID
        new_scheduled_at: New ISO datetime string

    Returns:
        Dict with rescheduling result
    """
    async with AsyncSessionLocal() as db:
        try:
            # Get post
            post = await db.get(Post, post_id)
            if not post or str(post.user_id) != user_id:
                return {"success": False, "error": "Post not found"}

            # Update post
            post.status = PostStatus.SCHEDULED
            post.scheduled_at = new_scheduled_at

            await db.commit()

            return {
                "success": True,
                "post_id": post_id,
                "scheduled_at": new_scheduled_at,
                "message": "Post rescheduled successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
