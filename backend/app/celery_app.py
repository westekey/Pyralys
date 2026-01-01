"""
Celery application configuration for Pyralys
Handles async task processing and scheduled jobs
"""
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "pyralys",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        'app.tasks.publishing',
        'app.tasks.scheduling',
        'app.tasks.analytics',
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes max
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    result_expires=3600,  # Results expire after 1 hour
)

# Celery Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    # Check for scheduled posts every minute
    'check-scheduled-posts': {
        'task': 'app.tasks.scheduling.check_scheduled_posts',
        'schedule': crontab(minute='*'),  # Every minute
    },
    # Refresh Instagram tokens daily
    'refresh-instagram-tokens': {
        'task': 'app.tasks.analytics.refresh_instagram_tokens',
        'schedule': crontab(hour=2, minute=0),  # Every day at 2 AM
    },
    # Collect analytics data every 6 hours
    'collect-analytics': {
        'task': 'app.tasks.analytics.collect_platform_analytics',
        'schedule': crontab(hour='*/6', minute=0),  # Every 6 hours
    },
    # Clean up old tasks weekly
    'cleanup-old-tasks': {
        'task': 'app.tasks.scheduling.cleanup_old_tasks',
        'schedule': crontab(day_of_week=0, hour=3, minute=0),  # Sunday at 3 AM
    },
}

# Optional: Custom task routes
celery_app.conf.task_routes = {
    'app.tasks.publishing.*': {'queue': 'publishing'},
    'app.tasks.scheduling.*': {'queue': 'scheduling'},
    'app.tasks.analytics.*': {'queue': 'analytics'},
}
