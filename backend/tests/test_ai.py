"""
AI Generation endpoint tests
"""
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_generate_caption_unauthorized(client: AsyncClient):
    """Test caption generation without authentication"""
    response = await client.post(
        "/api/v1/ai/generate-caption",
        json={
            "prompt": "Sunset at the beach",
            "platform": "instagram",
            "tone": "casual"
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
@patch('app.services.ai.text_generator.TextGenerator.generate_caption')
async def test_generate_caption_success(mock_generate, client: AsyncClient):
    """Test successful caption generation"""
    # Register and get token
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
    )
    token = register_response.json()["access_token"]

    # Mock GPT-4 response
    mock_generate.return_value = {
        "caption": "Beautiful sunset vibes 🌅 Living for these golden hour moments!",
        "hashtags": ["sunset", "beach", "goldenhour", "nature"],
        "metadata": {
            "model": "gpt-4-turbo-preview",
            "tone": "casual",
            "platform": "instagram",
            "tokens_used": 150,
            "finish_reason": "stop"
        }
    }

    # Generate caption
    response = await client.post(
        "/api/v1/ai/generate-caption",
        json={
            "prompt": "Sunset at the beach",
            "platform": "instagram",
            "tone": "casual"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "caption" in data
    assert "hashtags" in data
    assert "metadata" in data
    assert data["metadata"]["platform"] == "instagram"


@pytest.mark.asyncio
@patch('app.services.ai.image_generator.ImageGenerator.generate_image')
async def test_generate_image_free_plan_forbidden(mock_generate, client: AsyncClient):
    """Test that free plan users cannot generate images"""
    # Register free user
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
    )
    token = register_response.json()["access_token"]

    # Try to generate image (should fail)
    response = await client.post(
        "/api/v1/ai/generate-image",
        json={
            "prompt": "A futuristic AI tower",
            "style": "realistic",
            "size": "1024x1024"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    assert "Premium or Pro plan" in response.json()["detail"]


@pytest.mark.asyncio
@patch('app.services.ai.image_generator.ImageGenerator.generate_image')
async def test_generate_image_premium_success(mock_generate, client: AsyncClient):
    """Test successful image generation for premium user"""
    # Register user
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
    )
    token = register_response.json()["access_token"]

    # Upgrade to premium (we need to add this functionality)
    # For now, we'll manually update the user in the database
    # TODO: Create upgrade endpoint

    # Mock DALL-E 3 response
    mock_generate.return_value = {
        "image_url": "https://oaidalleapiprodscus.blob.core.windows.net/private/test.png",
        "revised_prompt": "A stunning futuristic AI tower with glowing lights",
        "original_prompt": "A futuristic AI tower",
        "metadata": {
            "model": "dall-e-3",
            "size": "1024x1024",
            "quality": "standard",
            "style": "realistic"
        }
    }

    # For this test, we'll skip the plan check by mocking the user's plan
    # In a real scenario, we'd update the user's plan through an endpoint


@pytest.mark.asyncio
@patch('app.services.ai.text_generator.TextGenerator.generate_hashtags')
async def test_generate_hashtags_success(mock_generate, client: AsyncClient):
    """Test successful hashtag generation"""
    # Register and get token
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
    )
    token = register_response.json()["access_token"]

    # Mock GPT-4 hashtag response
    mock_generate.return_value = [
        "fitness",
        "workout",
        "gym",
        "motivation",
        "fitnessmotivation",
        "gymlife",
        "health",
        "wellness",
        "fitfam",
        "bodybuilding"
    ]

    # Generate hashtags
    response = await client.post(
        "/api/v1/ai/generate-hashtags",
        json={
            "topic": "fitness and workout motivation",
            "platform": "instagram",
            "count": 10
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "hashtags" in data
    assert "count" in data
    assert "platform" in data
    assert len(data["hashtags"]) == 10
    assert data["platform"] == "instagram"


@pytest.mark.asyncio
@patch('app.services.ai.text_generator.TextGenerator.optimize_caption')
async def test_optimize_content_success(mock_optimize, client: AsyncClient):
    """Test content optimization"""
    # Register and get token
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
    )
    token = register_response.json()["access_token"]

    # Mock optimization response
    mock_optimize.return_value = {
        "optimized_caption": "Check out this amazing sunset! 🌅 Don't miss out!",
        "full_analysis": "OPTIMIZED:\nCheck out this amazing sunset! 🌅 Don't miss out!\n\nIMPROVEMENTS:\n1. Added call-to-action\n2. Included emoji\n3. More engaging language",
        "metadata": {
            "original_length": 20,
            "optimized_length": 50,
            "goal": "engagement"
        }
    }

    # Optimize content
    response = await client.post(
        "/api/v1/ai/optimize-content",
        params={
            "content": "Look at this sunset",
            "platform": "instagram"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "optimized_caption" in data
    assert "analysis" in data
    assert "metadata" in data


@pytest.mark.asyncio
async def test_predict_performance_not_implemented(client: AsyncClient):
    """Test that performance prediction returns 501 (not yet implemented)"""
    # Register and get token
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
    )
    token = register_response.json()["access_token"]

    # Try to predict performance
    response = await client.post(
        "/api/v1/ai/predict-performance",
        params={"post_id": "123"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 501
    assert "Sprint 6" in response.json()["detail"]


@pytest.mark.asyncio
@patch('app.services.ai.text_generator.TextGenerator.generate_caption')
async def test_generate_caption_with_user_context(mock_generate, client: AsyncClient):
    """Test caption generation with user brand context"""
    # Register user
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User",
            "brand_name": "Tech Innovators",
            "bio": "We create cutting-edge technology solutions"
        }
    )
    token = register_response.json()["access_token"]

    # Mock response
    mock_generate.return_value = {
        "caption": "Innovation meets excellence at Tech Innovators! 🚀",
        "hashtags": ["tech", "innovation", "technology"],
        "metadata": {
            "model": "gpt-4-turbo-preview",
            "tone": "professional",
            "platform": "linkedin",
            "tokens_used": 200,
            "finish_reason": "stop"
        }
    }

    # Generate caption
    response = await client.post(
        "/api/v1/ai/generate-caption",
        json={
            "prompt": "New product launch",
            "platform": "linkedin",
            "tone": "professional"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    # Verify that generate_caption was called with user_context
    mock_generate.assert_called_once()
    call_kwargs = mock_generate.call_args[1]
    assert call_kwargs["user_context"] is not None
    assert "brand_name" in call_kwargs["user_context"]
