"""
WordPress Publishing Service using WordPress REST API
"""
import httpx
import base64
from typing import Dict, Optional, List
from datetime import datetime

from app.models.wordpress_account import WordPressAccount


class WordPressService:
    """Service for publishing content to WordPress sites"""

    def __init__(self, account: WordPressAccount):
        self.account = account
        self.base_url = account.site_url.rstrip('/')
        self.api_url = f"{self.base_url}/wp-json/wp/v2"

        # Create authentication header (Application Password)
        credentials = f"{account.username}:{account.app_password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json"
        }

    async def test_connection(self) -> Dict:
        """
        Test the WordPress connection

        Returns:
            Dictionary with connection status and site info
        """
        try:
            async with httpx.AsyncClient() as client:
                # Get site information
                response = await client.get(
                    f"{self.base_url}/wp-json",
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()

                return {
                    "success": True,
                    "site_name": data.get("name", ""),
                    "site_description": data.get("description", ""),
                    "wp_version": data.get("gmt_offset", ""),
                    "api_available": True
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "api_available": False
            }

    async def create_post(
        self,
        title: str,
        content: str,
        status: str = "draft",
        excerpt: Optional[str] = None,
        categories: Optional[List[int]] = None,
        tags: Optional[List[int]] = None,
        featured_media: Optional[int] = None
    ) -> Dict:
        """
        Create a new WordPress post

        Args:
            title: Post title
            content: Post content (HTML)
            status: Post status (draft, publish, pending, private)
            excerpt: Post excerpt/summary
            categories: List of category IDs
            tags: List of tag IDs
            featured_media: Featured image media ID

        Returns:
            Dictionary with post information
        """
        post_data = {
            "title": title,
            "content": content,
            "status": status,
        }

        if excerpt:
            post_data["excerpt"] = excerpt

        if categories:
            post_data["categories"] = categories

        if tags:
            post_data["tags"] = tags

        if featured_media:
            post_data["featured_media"] = featured_media

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/posts",
                    json=post_data,
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()

                return {
                    "success": True,
                    "post_id": data.get("id"),
                    "post_url": data.get("link"),
                    "status": data.get("status"),
                    "title": data.get("title", {}).get("rendered", "")
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def upload_image(
        self,
        image_data: bytes,
        filename: str,
        alt_text: Optional[str] = None
    ) -> Dict:
        """
        Upload an image to WordPress media library

        Args:
            image_data: Image binary data
            filename: Image filename
            alt_text: Alternative text for the image

        Returns:
            Dictionary with media information
        """
        try:
            # Prepare headers for file upload
            upload_headers = {
                "Authorization": self.headers["Authorization"],
                "Content-Disposition": f'attachment; filename="{filename}"',
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/media",
                    content=image_data,
                    headers=upload_headers,
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()

                # Update alt text if provided
                if alt_text:
                    await client.post(
                        f"{self.api_url}/media/{data['id']}",
                        json={"alt_text": alt_text},
                        headers=self.headers
                    )

                return {
                    "success": True,
                    "media_id": data.get("id"),
                    "url": data.get("source_url"),
                    "title": data.get("title", {}).get("rendered", "")
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def get_categories(self) -> List[Dict]:
        """
        Get all categories from WordPress

        Returns:
            List of categories
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/categories",
                    headers=self.headers,
                    params={"per_page": 100},
                    timeout=10.0
                )
                response.raise_for_status()
                categories = response.json()

                return [
                    {
                        "id": cat.get("id"),
                        "name": cat.get("name"),
                        "slug": cat.get("slug"),
                        "count": cat.get("count", 0)
                    }
                    for cat in categories
                ]

        except Exception as e:
            return []

    async def get_tags(self) -> List[Dict]:
        """
        Get all tags from WordPress

        Returns:
            List of tags
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/tags",
                    headers=self.headers,
                    params={"per_page": 100},
                    timeout=10.0
                )
                response.raise_for_status()
                tags = response.json()

                return [
                    {
                        "id": tag.get("id"),
                        "name": tag.get("name"),
                        "slug": tag.get("slug"),
                        "count": tag.get("count", 0)
                    }
                    for tag in tags
                ]

        except Exception as e:
            return []

    async def create_tag(self, name: str) -> Optional[int]:
        """
        Create a new tag in WordPress

        Args:
            name: Tag name

        Returns:
            Tag ID if successful, None otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/tags",
                    json={"name": name},
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("id")

        except Exception as e:
            return None

    async def publish_ai_content(
        self,
        title: str,
        caption: str,
        hashtags: List[str],
        image_url: Optional[str] = None,
        image_data: Optional[bytes] = None,
        publish_immediately: bool = False
    ) -> Dict:
        """
        Publish AI-generated content to WordPress

        Args:
            title: Post title
            caption: AI-generated caption (will be post content)
            hashtags: List of hashtags
            image_url: URL of the image (if already uploaded)
            image_data: Image binary data (if uploading new image)
            publish_immediately: Whether to publish or save as draft

        Returns:
            Dictionary with publication status
        """
        try:
            # Upload image if provided
            featured_media_id = None
            if image_data:
                image_result = await self.upload_image(
                    image_data=image_data,
                    filename=f"ai-generated-{datetime.utcnow().timestamp()}.png",
                    alt_text=title
                )
                if image_result["success"]:
                    featured_media_id = image_result["media_id"]

            # Convert caption to HTML
            content_html = caption.replace('\n', '<br>')

            # Add hashtags as tags
            tag_ids = []
            for hashtag in hashtags:
                tag_id = await self.create_tag(hashtag)
                if tag_id:
                    tag_ids.append(tag_id)

            # Create the post
            status = "publish" if publish_immediately else "draft"
            result = await self.create_post(
                title=title,
                content=content_html,
                status=status,
                excerpt=caption[:150],  # First 150 chars as excerpt
                tags=tag_ids if tag_ids else None,
                featured_media=featured_media_id
            )

            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
