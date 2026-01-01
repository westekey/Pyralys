"""
Analytics tasks for collecting platform insights and metrics
Handles token refresh and data collection
"""
import asyncio
from typing import Dict
from datetime import datetime, timedelta
from celery import Task
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from app.celery_app import celery_app
from app.core.config import settings
from app.models.instagram_account import InstagramAccount
from app.models.post import Post, PostStatus, PostPublication
from app.services.instagram_service import InstagramService
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


@celery_app.task(base=AsyncTask, name='app.tasks.analytics.refresh_instagram_tokens')
async def refresh_instagram_tokens(self) -> dict:
    """
    Refresh Instagram long-lived access tokens
    Runs daily via Celery Beat (tokens expire after 60 days)

    Returns:
        Dict with refresh statistics
    """
    async with AsyncSessionLocal() as db:
        try:
            # Find accounts that need token refresh (expiring in next 7 days)
            expiry_threshold = (datetime.utcnow() + timedelta(days=7)).isoformat()

            stmt = select(InstagramAccount).where(
                InstagramAccount.is_active == True,
                InstagramAccount.token_expires_at <= expiry_threshold
            )

            result = await db.execute(stmt)
            accounts = result.scalars().all()

            refreshed_count = 0
            failed_count = 0

            for account in accounts:
                try:
                    # Initialize Instagram service
                    instagram_service = InstagramService(
                        instagram_user_id=account.instagram_user_id,
                        access_token=account.access_token
                    )

                    # Refresh token
                    refresh_result = await instagram_service.refresh_access_token()

                    if refresh_result and refresh_result.get('access_token'):
                        # Update account with new token
                        account.access_token = refresh_result['access_token']
                        account.token_expires_at = (
                            datetime.utcnow() + timedelta(days=60)
                        ).isoformat()
                        await db.commit()
                        refreshed_count += 1
                    else:
                        failed_count += 1

                except Exception as e:
                    print(f"Error refreshing token for account {account.id}: {str(e)}")
                    failed_count += 1

            return {
                "refreshed_at": datetime.utcnow().isoformat(),
                "total_accounts": len(accounts),
                "refreshed": refreshed_count,
                "failed": failed_count
            }

        except Exception as e:
            return {
                "error": str(e),
                "refreshed_at": datetime.utcnow().isoformat()
            }


@celery_app.task(base=AsyncTask, name='app.tasks.analytics.collect_platform_analytics')
async def collect_platform_analytics(self) -> dict:
    """
    Collect analytics data from all platforms
    Runs every 6 hours via Celery Beat

    Returns:
        Dict with collection statistics
    """
    async with AsyncSessionLocal() as db:
        try:
            # Find all published posts from the last 30 days
            cutoff_date = (datetime.utcnow() - timedelta(days=30)).isoformat()

            stmt = select(Post).where(
                Post.status == PostStatus.PUBLISHED,
                Post.published_at >= cutoff_date
            )

            result = await db.execute(stmt)
            posts = result.scalars().all()

            instagram_collected = 0
            total_posts = len(posts)

            for post in posts:
                # Collect Instagram insights
                if 'instagram' in post.target_platforms:
                    try:
                        await collect_instagram_insights.apply_async(
                            args=[str(post.id)],
                            countdown=0
                        )
                        instagram_collected += 1
                    except Exception as e:
                        print(f"Error queuing Instagram insights for post {post.id}: {str(e)}")

                # TODO: Add other platforms (TikTok, LinkedIn, etc.)

            return {
                "collected_at": datetime.utcnow().isoformat(),
                "total_posts": total_posts,
                "instagram_collected": instagram_collected
            }

        except Exception as e:
            return {
                "error": str(e),
                "collected_at": datetime.utcnow().isoformat()
            }


@celery_app.task(base=AsyncTask, name='app.tasks.analytics.collect_instagram_insights')
async def collect_instagram_insights(self, post_id: str) -> dict:
    """
    Collect Instagram insights for a specific post

    Args:
        post_id: Post UUID

    Returns:
        Dict with insights data
    """
    async with AsyncSessionLocal() as db:
        try:
            post_service = PostService(db)

            # Get post
            post = await db.get(Post, post_id)
            if not post:
                return {"success": False, "error": "Post not found"}

            # Find Instagram publication record
            stmt = select(PostPublication).where(
                PostPublication.post_id == post.id,
                PostPublication.platform == 'instagram',
                PostPublication.platform_post_id != None
            )

            result = await db.execute(stmt)
            publication = result.scalar_one_or_none()

            if not publication:
                return {"success": False, "error": "Instagram publication not found"}

            # Get user's Instagram account
            user = await db.get(User, post.user_id)
            stmt = select(InstagramAccount).where(
                InstagramAccount.user_id == user.id,
                InstagramAccount.is_active == True
            )

            result = await db.execute(stmt)
            instagram_account = result.scalar_one_or_none()

            if not instagram_account:
                return {"success": False, "error": "Instagram account not found"}

            # Initialize Instagram service
            instagram_service = InstagramService(
                instagram_user_id=instagram_account.instagram_user_id,
                access_token=instagram_account.access_token
            )

            # Get media insights
            insights = await instagram_service.get_media_insights(publication.platform_post_id)

            if insights:
                # Update publication with insights
                await post_service.update_publication_insights(
                    publication_id=str(publication.id),
                    insights=insights
                )

                return {
                    "success": True,
                    "post_id": post_id,
                    "platform": "instagram",
                    "insights": insights
                }
            else:
                return {"success": False, "error": "Failed to fetch insights"}

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


@celery_app.task(base=AsyncTask, name='app.tasks.analytics.generate_weekly_report')
async def generate_weekly_report(self, user_id: str) -> dict:
    """
    Generate weekly analytics report for a user

    Args:
        user_id: User UUID

    Returns:
        Dict with weekly report data
    """
    async with AsyncSessionLocal() as db:
        try:
            # Get posts from last 7 days
            week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()

            stmt = select(Post).where(
                Post.user_id == user_id,
                Post.status == PostStatus.PUBLISHED,
                Post.published_at >= week_ago
            )

            result = await db.execute(stmt)
            posts = result.scalars().all()

            # Calculate statistics
            total_posts = len(posts)
            platforms_used = set()
            total_engagements = 0

            for post in posts:
                platforms_used.update(post.target_platforms or [])

                # Sum up insights from publications
                if post.publications:
                    for pub in post.publications:
                        if pub.insights:
                            # Instagram insights
                            if pub.platform == 'instagram':
                                total_engagements += pub.insights.get('engagement', 0)

            return {
                "user_id": user_id,
                "period_start": week_ago,
                "period_end": datetime.utcnow().isoformat(),
                "total_posts": total_posts,
                "platforms_used": list(platforms_used),
                "total_engagements": total_engagements,
                "avg_engagement_per_post": total_engagements / total_posts if total_posts > 0 else 0
            }

        except Exception as e:
            return {
                "error": str(e),
                "user_id": user_id
            }
