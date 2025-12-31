"""
AI Text Generation Service using OpenAI GPT-4
"""
import openai
from typing import List, Dict, Optional
from openai import AsyncOpenAI

from app.core.config import settings


class TextGenerator:
    """Service for generating social media captions with AI"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    # System prompts for different tones
    TONE_PROMPTS = {
        "casual": """You are a friendly and relatable social media expert who creates engaging,
        conversational content. Use a warm, approachable tone with occasional emojis.
        Keep it fun and authentic.""",

        "professional": """You are a professional brand copywriter who creates polished,
        authoritative content. Use clear, concise language that builds trust and credibility.
        Maintain a business-appropriate tone.""",

        "funny": """You are a witty and humorous content creator who makes people laugh.
        Use clever wordplay, jokes, and relatable humor. Keep it light and entertaining
        while staying relevant to the topic.""",

        "inspirational": """You are a motivational speaker who creates uplifting and
        empowering content. Use powerful, encouraging language that inspires action.
        Focus on positive transformation and growth."""
    }

    # Platform-specific guidelines
    PLATFORM_GUIDELINES = {
        "instagram": {
            "max_length": 2200,
            "hashtag_count": "10-30",
            "best_practices": "Use line breaks for readability, start strong, include call-to-action"
        },
        "tiktok": {
            "max_length": 2200,
            "hashtag_count": "3-5",
            "best_practices": "Short, punchy, trend-focused, speak to Gen Z"
        },
        "linkedin": {
            "max_length": 3000,
            "hashtag_count": "3-5",
            "best_practices": "Professional, value-driven, industry insights"
        },
        "facebook": {
            "max_length": 63206,
            "hashtag_count": "1-2",
            "best_practices": "Conversational, storytelling, community-focused"
        }
    }

    async def generate_caption(
        self,
        prompt: str,
        platform: str = "instagram",
        tone: str = "casual",
        user_context: Optional[Dict] = None
    ) -> Dict:
        """
        Generate a social media caption using GPT-4

        Args:
            prompt: User's content description
            platform: Target platform (instagram, tiktok, linkedin, facebook)
            tone: Writing tone (casual, professional, funny, inspirational)
            user_context: Optional context about user's brand/style

        Returns:
            Dictionary with caption, hashtags, and metadata
        """
        # Get tone system prompt
        system_prompt = self.TONE_PROMPTS.get(tone, self.TONE_PROMPTS["casual"])

        # Get platform guidelines
        platform_guide = self.PLATFORM_GUIDELINES.get(
            platform,
            self.PLATFORM_GUIDELINES["instagram"]
        )

        # Build user message with platform context
        user_message = f"""Create an engaging {platform} caption for the following:

{prompt}

Platform: {platform}
Tone: {tone}
Max length: {platform_guide['max_length']} characters
Recommended hashtags: {platform_guide['hashtag_count']}
Best practices: {platform_guide['best_practices']}

{f"Brand context: {user_context}" if user_context else ""}

Requirements:
1. Write an attention-grabbing caption that hooks the reader immediately
2. Include relevant storytelling or value proposition
3. End with a clear call-to-action
4. Format for readability (use line breaks where appropriate)
5. DO NOT include hashtags in the caption itself - they will be added separately

Return ONLY the caption text, no extra commentary."""

        try:
            # Call GPT-4 Turbo
            completion = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.8,  # More creative
                max_tokens=1000,
                presence_penalty=0.3,  # Encourage diverse content
                frequency_penalty=0.3  # Reduce repetition
            )

            caption = completion.choices[0].message.content.strip()

            # Generate hashtags separately
            hashtags = await self.generate_hashtags(prompt, platform)

            return {
                "caption": caption,
                "hashtags": hashtags,
                "metadata": {
                    "model": "gpt-4-turbo-preview",
                    "tone": tone,
                    "platform": platform,
                    "tokens_used": completion.usage.total_tokens,
                    "finish_reason": completion.choices[0].finish_reason
                }
            }

        except Exception as e:
            # Handle OpenAI API errors
            raise Exception(f"AI generation failed: {str(e)}")

    async def generate_hashtags(
        self,
        topic: str,
        platform: str = "instagram",
        count: int = 15
    ) -> List[str]:
        """
        Generate relevant hashtags for a topic

        Args:
            topic: Main topic/content description
            platform: Target platform
            count: Number of hashtags to generate

        Returns:
            List of hashtags (without # symbol)
        """
        platform_guide = self.PLATFORM_GUIDELINES.get(
            platform,
            self.PLATFORM_GUIDELINES["instagram"]
        )

        prompt = f"""Generate {count} highly relevant and effective hashtags for this {platform} content:

{topic}

Requirements:
1. Mix of popular (100K-1M posts) and niche (10K-100K posts) hashtags
2. Relevant to the topic and target audience
3. Platform-optimized for {platform}
4. Include branded, trending, and evergreen tags
5. Return ONLY hashtag words (without # symbol), one per line
6. No explanations or commentary

Example format:
socialmedia
contentcreation
marketingtips"""

        try:
            completion = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a social media hashtag expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            # Parse hashtags from response
            response_text = completion.choices[0].message.content.strip()
            hashtags = [
                line.strip().replace('#', '').replace(' ', '')
                for line in response_text.split('\n')
                if line.strip()
            ]

            # Limit to requested count
            return hashtags[:count]

        except Exception as e:
            # Fallback to basic hashtags
            return ["socialmedia", "content", "marketing", platform]

    async def optimize_caption(
        self,
        original_caption: str,
        platform: str,
        optimization_goal: str = "engagement"
    ) -> Dict:
        """
        Optimize an existing caption for better performance

        Args:
            original_caption: Original caption text
            platform: Target platform
            optimization_goal: What to optimize for (engagement, conversions, reach)

        Returns:
            Optimized caption with suggestions
        """
        prompt = f"""Analyze and optimize this {platform} caption for maximum {optimization_goal}:

Original caption:
{original_caption}

Provide:
1. Optimized version of the caption
2. 3 specific improvements made
3. Predicted performance impact

Format your response as:
OPTIMIZED:
[optimized caption here]

IMPROVEMENTS:
1. [improvement 1]
2. [improvement 2]
3. [improvement 3]

IMPACT:
[predicted impact on {optimization_goal}]"""

        try:
            completion = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a social media optimization expert."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            response = completion.choices[0].message.content

            # Parse structured response
            parts = response.split("OPTIMIZED:")
            if len(parts) > 1:
                optimized_part = parts[1].split("IMPROVEMENTS:")[0].strip()

                return {
                    "optimized_caption": optimized_part,
                    "full_analysis": response,
                    "metadata": {
                        "original_length": len(original_caption),
                        "optimized_length": len(optimized_part),
                        "goal": optimization_goal
                    }
                }

            return {
                "optimized_caption": original_caption,
                "full_analysis": "Optimization could not be completed",
                "metadata": {}
            }

        except Exception as e:
            raise Exception(f"Caption optimization failed: {str(e)}")
