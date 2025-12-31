"""
Instagram Publishing Service using Instagram Graph API
"""
import httpx
from typing import Dict, Optional, List
from datetime import datetime, timedelta

from app.models.instagram_account import InstagramAccount


class InstagramService:
    """Service for publishing content to Instagram using Graph API"""

    GRAPH_API_VERSION = "v18.0"
    GRAPH_API_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

    def __init__(self, account: InstagramAccount):
        self.account = account
        self.access_token = account.access_token
        self.instagram_user_id = account.instagram_user_id

    async def get_account_info(self) -> Dict:
        """
        Get Instagram account information

        Returns:
            Dictionary with account details
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.GRAPH_API_URL}/{self.instagram_user_id}",
                    params={
                        "fields": "username,account_type,media_count,followers_count,follows_count,profile_picture_url",
                        "access_token": self.access_token
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()

                return {
                    "success": True,
                    "username": data.get("username"),
                    "account_type": data.get("account_type"),
                    "media_count": data.get("media_count", 0),
                    "followers_count": data.get("followers_count", 0),
                    "follows_count": data.get("follows_count", 0),
                    "profile_picture_url": data.get("profile_picture_url")
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def publish_photo(
        self,
        image_url: str,
        caption: Optional[str] = None,
        location_id: Optional[str] = None,
        user_tags: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Publish a photo to Instagram

        Args:
            image_url: URL of the image to publish (must be publicly accessible)
            caption: Post caption (max 2200 characters)
            location_id: Facebook location ID
            user_tags: List of user tags [{"username": "user1", "x": 0.5, "y": 0.5}]

        Returns:
            Dictionary with publication status
        """
        if not self.account.is_business_account:
            return {
                "success": False,
                "error": "Publishing requires a Business or Creator account"
            }

        try:
            # Step 1: Create media container
            container_params = {
                "image_url": image_url,
                "access_token": self.access_token
            }

            if caption:
                container_params["caption"] = caption[:2200]  # Max 2200 chars

            if location_id:
                container_params["location_id"] = location_id

            if user_tags:
                container_params["user_tags"] = user_tags

            async with httpx.AsyncClient() as client:
                # Create container
                create_response = await client.post(
                    f"{self.GRAPH_API_URL}/{self.instagram_user_id}/media",
                    data=container_params,
                    timeout=30.0
                )
                create_response.raise_for_status()
                container_data = create_response.json()
                container_id = container_data.get("id")

                if not container_id:
                    return {
                        "success": False,
                        "error": "Failed to create media container"
                    }

                # Step 2: Publish the container
                publish_response = await client.post(
                    f"{self.GRAPH_API_URL}/{self.instagram_user_id}/media_publish",
                    data={
                        "creation_id": container_id,
                        "access_token": self.access_token
                    },
                    timeout=30.0
                )
                publish_response.raise_for_status()
                publish_data = publish_response.json()

                return {
                    "success": True,
                    "media_id": publish_data.get("id"),
                    "permalink": f"https://www.instagram.com/p/{publish_data.get('id')}/"
                }

        except httpx.HTTPStatusError as e:
            error_data = e.response.json() if e.response else {}
            return {
                "success": False,
                "error": error_data.get("error", {}).get("message", str(e))
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def publish_carousel(
        self,
        images: List[str],
        caption: Optional[str] = None,
        location_id: Optional[str] = None
    ) -> Dict:
        """
        Publish a carousel (album) to Instagram

        Args:
            images: List of image URLs (2-10 images)
            caption: Post caption
            location_id: Facebook location ID

        Returns:
            Dictionary with publication status
        """
        if not self.account.is_business_account:
            return {
                "success": False,
                "error": "Publishing requires a Business or Creator account"
            }

        if len(images) < 2 or len(images) > 10:
            return {
                "success": False,
                "error": "Carousel must contain 2-10 images"
            }

        try:
            async with httpx.AsyncClient() as client:
                # Step 1: Create containers for each image
                children_ids = []

                for image_url in images:
                    response = await client.post(
                        f"{self.GRAPH_API_URL}/{self.instagram_user_id}/media",
                        data={
                            "image_url": image_url,
                            "is_carousel_item": True,
                            "access_token": self.access_token
                        },
                        timeout=30.0
                    )
                    response.raise_for_status()
                    data = response.json()
                    children_ids.append(data.get("id"))

                # Step 2: Create carousel container
                carousel_params = {
                    "media_type": "CAROUSEL",
                    "children": ",".join(children_ids),
                    "access_token": self.access_token
                }

                if caption:
                    carousel_params["caption"] = caption[:2200]

                if location_id:
                    carousel_params["location_id"] = location_id

                carousel_response = await client.post(
                    f"{self.GRAPH_API_URL}/{self.instagram_user_id}/media",
                    data=carousel_params,
                    timeout=30.0
                )
                carousel_response.raise_for_status()
                carousel_data = carousel_response.json()
                carousel_id = carousel_data.get("id")

                # Step 3: Publish the carousel
                publish_response = await client.post(
                    f"{self.GRAPH_API_URL}/{self.instagram_user_id}/media_publish",
                    data={
                        "creation_id": carousel_id,
                        "access_token": self.access_token
                    },
                    timeout=30.0
                )
                publish_response.raise_for_status()
                publish_data = publish_response.json()

                return {
                    "success": True,
                    "media_id": publish_data.get("id"),
                    "permalink": f"https://www.instagram.com/p/{publish_data.get('id')}/"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def publish_story(
        self,
        media_url: str,
        media_type: str = "IMAGE"
    ) -> Dict:
        """
        Publish a story to Instagram

        Args:
            media_url: URL of the media (image or video)
            media_type: Type of media (IMAGE or VIDEO)

        Returns:
            Dictionary with publication status
        """
        if not self.account.is_business_account:
            return {
                "success": False,
                "error": "Publishing stories requires a Business or Creator account"
            }

        try:
            async with httpx.AsyncClient() as client:
                # Create story container
                story_params = {
                    "media_type": "STORIES",
                    "access_token": self.access_token
                }

                if media_type == "IMAGE":
                    story_params["image_url"] = media_url
                else:
                    story_params["video_url"] = media_url

                create_response = await client.post(
                    f"{self.GRAPH_API_URL}/{self.instagram_user_id}/media",
                    data=story_params,
                    timeout=30.0
                )
                create_response.raise_for_status()
                container_data = create_response.json()
                container_id = container_data.get("id")

                # Publish story
                publish_response = await client.post(
                    f"{self.GRAPH_API_URL}/{self.instagram_user_id}/media_publish",
                    data={
                        "creation_id": container_id,
                        "access_token": self.access_token
                    },
                    timeout=30.0
                )
                publish_response.raise_for_status()
                publish_data = publish_response.json()

                return {
                    "success": True,
                    "media_id": publish_data.get("id")
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def get_media_insights(self, media_id: str) -> Dict:
        """
        Get insights for a published media

        Args:
            media_id: Instagram media ID

        Returns:
            Dictionary with media insights
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.GRAPH_API_URL}/{media_id}/insights",
                    params={
                        "metric": "engagement,impressions,reach,saved",
                        "access_token": self.access_token
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()

                insights = {}
                for item in data.get("data", []):
                    insights[item.get("name")] = item.get("values", [{}])[0].get("value", 0)

                return {
                    "success": True,
                    "insights": insights
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def refresh_access_token(self) -> Dict:
        """
        Refresh long-lived access token (extends by 60 days)

        Returns:
            Dictionary with new token and expiration
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.GRAPH_API_URL}/oauth/access_token",
                    params={
                        "grant_type": "ig_refresh_token",
                        "access_token": self.access_token
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()

                new_token = data.get("access_token")
                expires_in = data.get("expires_in", 5184000)  # Default 60 days

                # Calculate expiration date
                expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

                return {
                    "success": True,
                    "access_token": new_token,
                    "expires_at": expires_at.isoformat()
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def publish_ai_content(
        self,
        caption: str,
        hashtags: List[str],
        image_url: Optional[str] = None,
        images: Optional[List[str]] = None
    ) -> Dict:
        """
        Publish AI-generated content to Instagram

        Args:
            caption: AI-generated caption
            hashtags: List of hashtags
            image_url: Single image URL (for photo post)
            images: Multiple image URLs (for carousel)

        Returns:
            Dictionary with publication status
        """
        # Combine caption and hashtags
        full_caption = caption
        if hashtags:
            hashtag_text = " ".join([f"#{tag}" for tag in hashtags])
            full_caption = f"{caption}\n\n{hashtag_text}"

        # Publish carousel if multiple images
        if images and len(images) > 1:
            return await self.publish_carousel(
                images=images,
                caption=full_caption
            )

        # Publish single photo
        if image_url:
            return await self.publish_photo(
                image_url=image_url,
                caption=full_caption
            )

        return {
            "success": False,
            "error": "Either image_url or images must be provided"
        }
