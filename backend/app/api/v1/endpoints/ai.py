"""
AI content generation endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.ai import (
    CaptionGenerationRequest,
    CaptionGenerationResponse,
    ImageGenerationRequest,
    ImageGenerationResponse,
    HashtagGenerationRequest,
    HashtagGenerationResponse
)
from app.services.ai.text_generator import TextGenerator
from app.services.ai.image_generator import ImageGenerator
from app.services.quota_service import QuotaService
from app.models.usage import UsageType

router = APIRouter()


@router.post("/generate-caption", response_model=CaptionGenerationResponse)
async def generate_caption(
    request: CaptionGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate social media caption using AI

    - **prompt**: Description of what to create
    - **platform**: Target platform (instagram, tiktok, etc.)
    - **tone**: Writing tone (casual, professional, funny, inspirational)
    """
    # Check quota
    quota_service = QuotaService(db)
    if not await quota_service.check_quota(current_user, UsageType.CAPTION):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Caption generation quota exceeded for your plan"
        )

    try:
        generator = TextGenerator()

        # Prepare user context if available
        user_context = None
        if current_user.brand_name or current_user.bio:
            user_context = {
                "brand_name": current_user.brand_name,
                "bio": current_user.bio
            }

        # Generate caption with GPT-4
        result = await generator.generate_caption(
            prompt=request.prompt,
            platform=request.platform,
            tone=request.tone,
            user_context=user_context
        )

        # Track quota usage
        await quota_service.increment_usage(current_user, UsageType.CAPTION)

        return CaptionGenerationResponse(
            caption=result["caption"],
            hashtags=result["hashtags"],
            metadata=result["metadata"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Caption generation failed: {str(e)}"
        )


@router.post("/generate-image", response_model=ImageGenerationResponse)
async def generate_image(
    request: ImageGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate image using DALL-E 3

    - **prompt**: Image description
    - **style**: Optional style modifier
    - **size**: Image dimensions
    """
    # Check quota (includes plan check)
    quota_service = QuotaService(db)
    if not await quota_service.check_quota(current_user, UsageType.IMAGE):
        if current_user.plan_type == "free":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Image generation requires Premium or Pro plan"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Image generation quota exceeded for your plan"
            )

    try:
        generator = ImageGenerator()

        # Get platform-specific size if platform provided
        size = request.size
        if request.platform:
            platform_specs = generator.get_platform_recommendations(request.platform)
            size = platform_specs["recommended_size"]

        # Validate size against DALL-E 3 supported sizes
        valid_sizes = ["1024x1024", "1024x1792", "1792x1024"]
        if size not in valid_sizes:
            # Default to square if unsupported
            size = "1024x1024"

        # Generate image with DALL-E 3
        result = await generator.generate_image(
            prompt=request.prompt,
            style=request.style,
            size=size,
            quality=request.quality or "standard"
        )

        # Track quota usage
        await quota_service.increment_usage(current_user, UsageType.IMAGE)
        # TODO: Download and upload to S3 for persistence

        return ImageGenerationResponse(
            image_url=result["image_url"],
            revised_prompt=result["revised_prompt"],
            metadata=result["metadata"]
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image generation failed: {str(e)}"
        )


@router.post("/generate-hashtags", response_model=HashtagGenerationResponse)
async def generate_hashtags(
    request: HashtagGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate optimized hashtags for a topic

    - **topic**: Main topic/keyword
    - **platform**: Target platform
    - **count**: Number of hashtags to generate (default: 10)
    """
    # Check quota
    quota_service = QuotaService(db)
    if not await quota_service.check_quota(current_user, UsageType.HASHTAG):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Hashtag generation quota exceeded for your plan"
        )

    try:
        generator = TextGenerator()

        # Generate hashtags with GPT-4
        hashtags = await generator.generate_hashtags(
            topic=request.topic,
            platform=request.platform,
            count=request.count
        )

        # Track quota usage
        await quota_service.increment_usage(current_user, UsageType.HASHTAG)

        return HashtagGenerationResponse(
            hashtags=hashtags,
            count=len(hashtags),
            platform=request.platform
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Hashtag generation failed: {str(e)}"
        )


@router.get("/quotas")
async def get_quotas(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all quota information for the current user

    Returns usage limits, current usage, and remaining quota for all features
    """
    quota_service = QuotaService(db)
    return await quota_service.get_all_quotas(current_user)


@router.post("/predict-performance")
async def predict_performance(
    post_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Predict post performance using ML model
    """
    # TODO: Implement performance prediction in Sprint 6 (Analytics)
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Performance prediction will be implemented in Sprint 6"
    )


@router.post("/optimize-content")
async def optimize_content(
    content: str,
    platform: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get AI suggestions to optimize content
    """
    try:
        generator = TextGenerator()

        # Use the optimize_caption method
        result = await generator.optimize_caption(
            original_caption=content,
            platform=platform,
            optimization_goal="engagement"
        )

        return {
            "optimized_caption": result["optimized_caption"],
            "analysis": result["full_analysis"],
            "metadata": result["metadata"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content optimization failed: {str(e)}"
        )
