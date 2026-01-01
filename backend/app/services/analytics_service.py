"""
Analytics service for aggregating and analyzing post performance data
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_

from app.models.post import Post, PostStatus, PostType, PostPublication
from app.models.user import User


class AnalyticsService:
    """Service for analytics data aggregation and insights"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_overview_stats(self, user: User) -> Dict:
        """
        Get overview statistics for user's account

        Returns:
            Dict with total posts, published, scheduled, platforms, engagement
        """
        # Total posts count
        total_posts_stmt = select(func.count(Post.id)).where(Post.user_id == user.id)
        total_posts = (await self.db.execute(total_posts_stmt)).scalar() or 0

        # Published posts count
        published_stmt = select(func.count(Post.id)).where(
            and_(Post.user_id == user.id, Post.status == PostStatus.PUBLISHED)
        )
        published_posts = (await self.db.execute(published_stmt)).scalar() or 0

        # Scheduled posts count
        scheduled_stmt = select(func.count(Post.id)).where(
            and_(Post.user_id == user.id, Post.status == PostStatus.SCHEDULED)
        )
        scheduled_posts = (await self.db.execute(scheduled_stmt)).scalar() or 0

        # Draft posts count
        draft_stmt = select(func.count(Post.id)).where(
            and_(Post.user_id == user.id, Post.status == PostStatus.DRAFT)
        )
        draft_posts = (await self.db.execute(draft_stmt)).scalar() or 0

        # Get platform distribution
        platforms_stmt = select(Post).where(
            and_(Post.user_id == user.id, Post.status == PostStatus.PUBLISHED)
        )
        posts = (await self.db.execute(platforms_stmt)).scalars().all()

        platform_counts = {}
        for post in posts:
            for platform in post.target_platforms or []:
                platform_counts[platform] = platform_counts.get(platform, 0) + 1

        # Get total engagement from publications
        total_engagement = 0
        total_reach = 0

        publications_stmt = select(PostPublication).join(Post).where(
            Post.user_id == user.id
        )
        publications = (await self.db.execute(publications_stmt)).scalars().all()

        for pub in publications:
            if pub.insights:
                # Instagram insights
                if pub.platform == 'instagram':
                    total_engagement += pub.insights.get('engagement', 0)
                    total_reach += pub.insights.get('reach', 0)

        return {
            "total_posts": total_posts,
            "published": published_posts,
            "scheduled": scheduled_posts,
            "draft": draft_posts,
            "failed": total_posts - published_posts - scheduled_posts - draft_posts,
            "platforms": platform_counts,
            "total_engagement": total_engagement,
            "total_reach": total_reach,
            "avg_engagement_rate": (total_engagement / total_reach * 100) if total_reach > 0 else 0
        }

    async def get_performance_by_platform(self, user: User, days: int = 30) -> Dict:
        """
        Get performance metrics by platform for the last N days

        Args:
            user: User instance
            days: Number of days to look back

        Returns:
            Dict with performance data per platform
        """
        cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()

        # Get published posts in date range
        stmt = select(Post).where(
            and_(
                Post.user_id == user.id,
                Post.status == PostStatus.PUBLISHED,
                Post.published_at >= cutoff_date
            )
        )
        posts = (await self.db.execute(stmt)).scalars().all()

        platform_stats = {}

        for post in posts:
            # Get publications for this post
            for pub in post.publications or []:
                platform = pub.platform
                if platform not in platform_stats:
                    platform_stats[platform] = {
                        "posts_count": 0,
                        "total_engagement": 0,
                        "total_reach": 0,
                        "total_impressions": 0,
                        "successful": 0,
                        "failed": 0
                    }

                platform_stats[platform]["posts_count"] += 1

                if pub.status == "published":
                    platform_stats[platform]["successful"] += 1
                else:
                    platform_stats[platform]["failed"] += 1

                # Add insights
                if pub.insights:
                    if platform == 'instagram':
                        platform_stats[platform]["total_engagement"] += pub.insights.get('engagement', 0)
                        platform_stats[platform]["total_reach"] += pub.insights.get('reach', 0)
                        platform_stats[platform]["total_impressions"] += pub.insights.get('impressions', 0)

        # Calculate averages
        for platform, stats in platform_stats.items():
            if stats["posts_count"] > 0:
                stats["avg_engagement"] = stats["total_engagement"] / stats["posts_count"]
                stats["avg_reach"] = stats["total_reach"] / stats["posts_count"]
                stats["success_rate"] = (stats["successful"] / stats["posts_count"]) * 100
                stats["engagement_rate"] = (
                    (stats["total_engagement"] / stats["total_reach"] * 100)
                    if stats["total_reach"] > 0 else 0
                )

        return platform_stats

    async def get_posts_timeline(self, user: User, days: int = 30) -> List[Dict]:
        """
        Get posts published over time for timeline chart

        Args:
            user: User instance
            days: Number of days to look back

        Returns:
            List of dicts with date and post counts
        """
        cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()

        stmt = select(Post).where(
            and_(
                Post.user_id == user.id,
                Post.status == PostStatus.PUBLISHED,
                Post.published_at >= cutoff_date
            )
        ).order_by(Post.published_at)

        posts = (await self.db.execute(stmt)).scalars().all()

        # Group by date
        timeline = {}
        for post in posts:
            if post.published_at:
                # Extract date (YYYY-MM-DD)
                date = post.published_at.split('T')[0]
                timeline[date] = timeline.get(date, 0) + 1

        # Convert to list of dicts
        return [
            {"date": date, "posts": count}
            for date, count in sorted(timeline.items())
        ]

    async def get_top_performing_posts(
        self,
        user: User,
        limit: int = 10,
        metric: str = "engagement"
    ) -> List[Dict]:
        """
        Get top performing posts by a specific metric

        Args:
            user: User instance
            limit: Number of posts to return
            metric: Metric to sort by (engagement, reach, impressions)

        Returns:
            List of top performing posts with their metrics
        """
        stmt = select(Post).where(
            and_(
                Post.user_id == user.id,
                Post.status == PostStatus.PUBLISHED
            )
        )

        posts = (await self.db.execute(stmt)).scalars().all()

        # Calculate metrics for each post
        posts_with_metrics = []
        for post in posts:
            total_engagement = 0
            total_reach = 0
            total_impressions = 0

            for pub in post.publications or []:
                if pub.insights:
                    if pub.platform == 'instagram':
                        total_engagement += pub.insights.get('engagement', 0)
                        total_reach += pub.insights.get('reach', 0)
                        total_impressions += pub.insights.get('impressions', 0)

            posts_with_metrics.append({
                "id": str(post.id),
                "title": post.title or "Untitled",
                "caption": post.caption[:100] if post.caption else "",
                "published_at": post.published_at,
                "platforms": post.target_platforms or [],
                "engagement": total_engagement,
                "reach": total_reach,
                "impressions": total_impressions,
                "engagement_rate": (total_engagement / total_reach * 100) if total_reach > 0 else 0
            })

        # Sort by metric
        posts_with_metrics.sort(key=lambda x: x.get(metric, 0), reverse=True)

        return posts_with_metrics[:limit]

    async def get_content_type_distribution(self, user: User) -> Dict:
        """
        Get distribution of content types (photo, video, carousel, story)

        Returns:
            Dict with counts per content type
        """
        stmt = select(Post).where(Post.user_id == user.id)
        posts = (await self.db.execute(stmt)).scalars().all()

        distribution = {}
        for post in posts:
            post_type = post.post_type.value
            distribution[post_type] = distribution.get(post_type, 0) + 1

        return distribution

    async def get_posting_patterns(self, user: User) -> Dict:
        """
        Analyze posting patterns (best days, best times)

        Returns:
            Dict with posting patterns analysis
        """
        stmt = select(Post).where(
            and_(
                Post.user_id == user.id,
                Post.status == PostStatus.PUBLISHED,
                Post.published_at != None
            )
        )
        posts = (await self.db.execute(stmt)).scalars().all()

        day_counts = {}
        hour_counts = {}

        for post in posts:
            if post.published_at:
                # Parse datetime
                dt = datetime.fromisoformat(post.published_at.replace('Z', '+00:00'))

                # Day of week (0 = Monday, 6 = Sunday)
                day_name = dt.strftime('%A')
                day_counts[day_name] = day_counts.get(day_name, 0) + 1

                # Hour of day
                hour = dt.hour
                hour_counts[hour] = hour_counts.get(hour, 0) + 1

        # Find best day and hour
        best_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else None
        best_hour = max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else None

        return {
            "days": day_counts,
            "hours": hour_counts,
            "best_day": best_day,
            "best_hour": best_hour
        }

    async def get_growth_metrics(self, user: User, days: int = 30) -> Dict:
        """
        Calculate growth metrics over time

        Returns:
            Dict with growth statistics
        """
        cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
        previous_cutoff = (datetime.utcnow() - timedelta(days=days * 2)).isoformat()

        # Current period
        current_stmt = select(func.count(Post.id)).where(
            and_(
                Post.user_id == user.id,
                Post.status == PostStatus.PUBLISHED,
                Post.published_at >= cutoff_date
            )
        )
        current_posts = (await self.db.execute(current_stmt)).scalar() or 0

        # Previous period
        previous_stmt = select(func.count(Post.id)).where(
            and_(
                Post.user_id == user.id,
                Post.status == PostStatus.PUBLISHED,
                Post.published_at >= previous_cutoff,
                Post.published_at < cutoff_date
            )
        )
        previous_posts = (await self.db.execute(previous_stmt)).scalar() or 0

        # Calculate growth rate
        growth_rate = 0
        if previous_posts > 0:
            growth_rate = ((current_posts - previous_posts) / previous_posts) * 100

        return {
            "current_period": {
                "posts": current_posts,
                "days": days
            },
            "previous_period": {
                "posts": previous_posts,
                "days": days
            },
            "growth_rate": growth_rate,
            "net_change": current_posts - previous_posts
        }
