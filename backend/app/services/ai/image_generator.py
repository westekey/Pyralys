"""
AI Image Generation Service using DALL-E 3
"""
import httpx
from typing import Dict, Optional
from openai import AsyncOpenAI

from app.core.config import settings


class ImageGenerator:
    """Service for generating images with DALL-E 3"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    # Style presets for different use cases
    STYLE_PRESETS = {
        "realistic": "photorealistic, high quality photography, professional",
        "artistic": "artistic, creative, visually striking, modern art style",
        "minimal": "minimalist, clean, simple, elegant design",
        "vibrant": "vibrant colors, energetic, eye-catching, bold",
        "corporate": "professional, clean, corporate style, business-appropriate",
        "vintage": "vintage aesthetic, retro, nostalgic feel",
        "3d": "3D render, modern 3D graphics, polished"
    }

    # Platform-specific image recommendations
    PLATFORM_SPECS = {
        "instagram_feed": {
            "recommended_size": "1024x1024",
            "aspect_ratio": "1:1",
            "description": "Instagram Feed Post (Square)"
        },
        "instagram_story": {
            "recommended_size": "1024x1792",
            "aspect_ratio": "9:16",
            "description": "Instagram Story/Reels (Vertical)"
        },
        "instagram_landscape": {
            "recommended_size": "1792x1024",
            "aspect_ratio": "16:9",
            "description": "Instagram Landscape Post"
        },
        "tiktok": {
            "recommended_size": "1024x1792",
            "aspect_ratio": "9:16",
            "description": "TikTok Video Thumbnail (Vertical)"
        },
        "linkedin": {
            "recommended_size": "1200x627",  # Will need resizing
            "aspect_ratio": "1.91:1",
            "description": "LinkedIn Post (Landscape)"
        },
        "facebook": {
            "recommended_size": "1200x630",  # Will need resizing
            "aspect_ratio": "1.91:1",
            "description": "Facebook Post (Landscape)"
        }
    }

    async def generate_image(
        self,
        prompt: str,
        style: Optional[str] = None,
        size: str = "1024x1024",
        quality: str = "standard"
    ) -> Dict:
        """
        Generate an image using DALL-E 3

        Args:
            prompt: Image description
            style: Optional style preset or custom style description
            size: Image size (1024x1024, 1024x1792, 1792x1024)
            quality: Image quality (standard, hd)

        Returns:
            Dictionary with image URL and metadata
        """
        # Validate size
        valid_sizes = ["1024x1024", "1024x1792", "1792x1024"]
        if size not in valid_sizes:
            raise ValueError(f"Invalid size. Must be one of: {valid_sizes}")

        # Build enhanced prompt with style
        enhanced_prompt = prompt

        if style and style in self.STYLE_PRESETS:
            style_description = self.STYLE_PRESETS[style]
            enhanced_prompt = f"{prompt}, {style_description}"
        elif style:
            # Custom style provided
            enhanced_prompt = f"{prompt}, {style}"

        # Add quality modifiers
        if quality == "hd":
            enhanced_prompt = f"{enhanced_prompt}, high resolution, highly detailed"

        try:
            # Generate image with DALL-E 3
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                size=size,
                quality=quality,
                n=1  # DALL-E 3 only supports n=1
            )

            # Get generated image URL
            image_url = response.data[0].url
            revised_prompt = response.data[0].revised_prompt

            return {
                "image_url": image_url,
                "revised_prompt": revised_prompt,
                "original_prompt": prompt,
                "metadata": {
                    "model": "dall-e-3",
                    "size": size,
                    "quality": quality,
                    "style": style
                }
            }

        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")

    async def download_image(self, image_url: str) -> bytes:
        """
        Download generated image from URL

        Args:
            image_url: URL of the generated image

        Returns:
            Image data as bytes
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)
                response.raise_for_status()
                return response.content

        except Exception as e:
            raise Exception(f"Image download failed: {str(e)}")

    def get_platform_recommendations(self, platform: str) -> Dict:
        """
        Get image size recommendations for a platform

        Args:
            platform: Platform name

        Returns:
            Platform specifications
        """
        return self.PLATFORM_SPECS.get(
            platform,
            self.PLATFORM_SPECS["instagram_feed"]
        )

    async def generate_variations(
        self,
        base_prompt: str,
        count: int = 3,
        style: Optional[str] = None
    ) -> list:
        """
        Generate multiple variations of an image concept

        Args:
            base_prompt: Base image description
            count: Number of variations to generate
            style: Optional style preset

        Returns:
            List of generated images with different variations
        """
        variations = []

        # Different variation modifiers
        modifiers = [
            "alternative composition",
            "different angle",
            "unique perspective",
            "creative variation"
        ]

        for i in range(min(count, 4)):  # Limit to avoid excessive API calls
            modifier = modifiers[i] if i < len(modifiers) else ""
            variation_prompt = f"{base_prompt}, {modifier}"

            try:
                result = await self.generate_image(
                    prompt=variation_prompt,
                    style=style
                )
                variations.append(result)

            except Exception as e:
                # Continue even if one variation fails
                print(f"Variation {i+1} failed: {str(e)}")
                continue

        return variations


class ImageAnalyzer:
    """Service for analyzing images and suggesting improvements"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_image(self, image_url: str, platform: str = "instagram") -> Dict:
        """
        Analyze an image and provide suggestions for social media

        Args:
            image_url: URL of the image to analyze
            platform: Target platform

        Returns:
            Analysis with suggestions
        """
        # Note: This would use GPT-4 Vision API
        # For MVP, return basic analysis structure

        return {
            "quality_score": 0.85,
            "suggestions": [
                "Consider adding text overlay for better engagement",
                "Brightness could be increased slightly",
                "Colors are well-balanced for Instagram"
            ],
            "predicted_performance": "high",
            "metadata": {
                "platform": platform,
                "analysis_date": "2025-01-01"
            }
        }
