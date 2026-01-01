"""
Analytics and reporting endpoints
"""
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/overview")
async def get_overview_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get dashboard overview statistics

    Returns:
        - Total posts count
        - Published, scheduled, draft counts
        - Platform distribution
        - Total engagement and reach
    """
    analytics_service = AnalyticsService(db)
    stats = await analytics_service.get_overview_stats(current_user)
    return stats


@router.get("/performance")
async def get_performance_by_platform(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get performance metrics by platform

    Args:
        days: Number of days to analyze (1-365)

    Returns:
        Performance data per platform with engagement, reach, and success rates
    """
    analytics_service = AnalyticsService(db)
    performance = await analytics_service.get_performance_by_platform(current_user, days)
    return {
        "period_days": days,
        "platforms": performance
    }


@router.get("/timeline")
async def get_posts_timeline(
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get posts published over time for timeline chart

    Args:
        days: Number of days to show (7-365)

    Returns:
        List of dates with post counts for charting
    """
    analytics_service = AnalyticsService(db)
    timeline = await analytics_service.get_posts_timeline(current_user, days)
    return {
        "period_days": days,
        "timeline": timeline
    }


@router.get("/top-posts")
async def get_top_performing_posts(
    limit: int = Query(10, ge=1, le=50),
    metric: str = Query("engagement", regex="^(engagement|reach|impressions)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get top performing posts by metric

    Args:
        limit: Number of posts to return (1-50)
        metric: Sort by engagement, reach, or impressions

    Returns:
        List of top posts with their metrics
    """
    analytics_service = AnalyticsService(db)
    top_posts = await analytics_service.get_top_performing_posts(current_user, limit, metric)
    return {
        "metric": metric,
        "limit": limit,
        "posts": top_posts
    }


@router.get("/content-types")
async def get_content_type_distribution(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get distribution of content types (photo, video, carousel, story)

    Returns:
        Counts per content type for pie chart
    """
    analytics_service = AnalyticsService(db)
    distribution = await analytics_service.get_content_type_distribution(current_user)
    return distribution


@router.get("/posting-patterns")
async def get_posting_patterns(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze posting patterns to find best days and times

    Returns:
        - Posts per day of week
        - Posts per hour of day
        - Best day and hour recommendations
    """
    analytics_service = AnalyticsService(db)
    patterns = await analytics_service.get_posting_patterns(current_user)
    return patterns


@router.get("/growth")
async def get_growth_metrics(
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Calculate growth metrics comparing current period vs previous period

    Args:
        days: Period length in days

    Returns:
        Growth rate, net change, and period comparisons
    """
    analytics_service = AnalyticsService(db)
    growth = await analytics_service.get_growth_metrics(current_user, days)
    return growth


@router.get("/dashboard")
async def get_dashboard_complete(
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get complete dashboard data in a single request

    Combines overview, performance, timeline, and growth metrics

    Args:
        days: Period for time-based analytics

    Returns:
        Complete dashboard data object
    """
    analytics_service = AnalyticsService(db)

    # Fetch all data concurrently would be better, but for simplicity we'll do sequentially
    overview = await analytics_service.get_overview_stats(current_user)
    performance = await analytics_service.get_performance_by_platform(current_user, days)
    timeline = await analytics_service.get_posts_timeline(current_user, days)
    top_posts = await analytics_service.get_top_performing_posts(current_user, limit=5)
    content_types = await analytics_service.get_content_type_distribution(current_user)
    patterns = await analytics_service.get_posting_patterns(current_user)
    growth = await analytics_service.get_growth_metrics(current_user, days)

    return {
        "period_days": days,
        "overview": overview,
        "performance": performance,
        "timeline": timeline,
        "top_posts": top_posts,
        "content_types": content_types,
        "posting_patterns": patterns,
        "growth": growth
    }


@router.get("/export")
async def export_analytics(
    format: str = Query("csv", regex="^(csv|json)$"),
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Export analytics data

    Args:
        format: Export format (csv or json)
        days: Number of days to include

    Returns:
        Analytics data in requested format
    """
    analytics_service = AnalyticsService(db)

    # Get all analytics data
    overview = await analytics_service.get_overview_stats(current_user)
    performance = await analytics_service.get_performance_by_platform(current_user, days)
    timeline = await analytics_service.get_posts_timeline(current_user, days)
    top_posts = await analytics_service.get_top_performing_posts(current_user, limit=20)

    export_data = {
        "user_id": str(current_user.id),
        "export_date": datetime.utcnow().isoformat(),
        "period_days": days,
        "overview": overview,
        "performance": performance,
        "timeline": timeline,
        "top_posts": top_posts
    }

    if format == "csv":
        # For CSV, we'd need to flatten the data structure
        # For now, return JSON with a note
        return {
            "format": "json",
            "note": "CSV export coming soon",
            "data": export_data
        }
    else:
        return export_data
