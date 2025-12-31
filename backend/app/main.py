"""
Pyralys API - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI-Powered Social Media Content Creation Platform",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "environment": settings.APP_ENV
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
