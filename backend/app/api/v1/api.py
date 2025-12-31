"""
API Router - Main router that includes all endpoint routers
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, content, analytics, ai, social, billing, wordpress, instagram

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(content.router, prefix="/content", tags=["Content"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Generation"])
api_router.include_router(social.router, prefix="/social", tags=["Social Accounts"])
api_router.include_router(wordpress.router, prefix="/wordpress", tags=["WordPress"])
api_router.include_router(instagram.router, prefix="/instagram", tags=["Instagram"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(billing.router, prefix="/billing", tags=["Billing"])
