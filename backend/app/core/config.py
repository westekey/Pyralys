"""
Application Configuration
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "Pyralys API"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str

    # Database
    DATABASE_URL: str
    DATABASE_WRITE_URL: str = None
    DATABASE_READ_URL: str = None

    # Redis
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # JWT
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # OpenAI
    OPENAI_API_KEY: str

    # Anthropic
    ANTHROPIC_API_KEY: str = None

    # AWS
    AWS_ACCESS_KEY_ID: str = None
    AWS_SECRET_ACCESS_KEY: str = None
    AWS_REGION: str = "eu-west-1"
    AWS_S3_BUCKET: str = None

    # Social Media APIs
    FACEBOOK_APP_ID: str = None
    FACEBOOK_APP_SECRET: str = None
    TIKTOK_CLIENT_KEY: str = None
    TIKTOK_CLIENT_SECRET: str = None

    # Stripe
    STRIPE_SECRET_KEY: str = None
    STRIPE_PUBLISHABLE_KEY: str = None
    STRIPE_WEBHOOK_SECRET: str = None

    # SendGrid
    SENDGRID_API_KEY: str = None
    FROM_EMAIL: str = "noreply@pyralys.com"

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]

    # Monitoring
    SENTRY_DSN: str = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
