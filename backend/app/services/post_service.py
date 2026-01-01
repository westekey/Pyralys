"""
Post Management Service
"""
from typing import List, Optional, Dict
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.models.post import Post, Media, PostPublication, PostStatus, PostType
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    """Service for managing posts"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_post(
        self,
        user: User,
        post_data: PostCreate
    ) -> Post:
        """
        Create a new post

        Args:
            user: User creating the post
            post_data: Post data

        Returns:
            Created post
        """
        # Create post
        post = Post(
            user_id=user.id,
            title=post_data.title,
            caption=post_data.caption,
            content=post_data.content,
            hashtags=post_data.hashtags,
            post_type=PostType(post_data.post_type),
            status=PostStatus.DRAFT,
            media_urls=post_data.media_urls,
            target_platforms=post_data.target_platforms,
            ai_generated=post_data.ai_generated,
            ai_prompt=post_data.ai_prompt,
            generation_params=post_data.generation_params,
            scheduled_at=post_data.scheduled_at
        )

        # If scheduled_at is set, mark as scheduled
        if post_data.scheduled_at:
            post.status = PostStatus.SCHEDULED

        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)

        return post

    async def get_post(
        self,
        post_id: str,
        user: User,
        include_relations: bool = True
    ) -> Optional[Post]:
        """
        Get a post by ID

        Args:
            post_id: Post ID
            user: User requesting the post
            include_relations: Include media and publications

        Returns:
            Post if found and belongs to user, None otherwise
        """
        query = select(Post).where(
            Post.id == post_id,
            Post.user_id == user.id
        )

        if include_relations:
            query = query.options(
                selectinload(Post.media),
                selectinload(Post.publications)
            )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def list_posts(
        self,
        user: User,
        status: Optional[str] = None,
        post_type: Optional[str] = None,
        platform: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> tuple[List[Post], int]:
        """
        List posts for a user with filters

        Args:
            user: User to list posts for
            status: Filter by status
            post_type: Filter by post type
            platform: Filter by target platform
            search: Search in title/caption
            skip: Number of posts to skip
            limit: Maximum posts to return

        Returns:
            Tuple of (posts, total_count)
        """
        # Base query
        query = select(Post).where(Post.user_id == user.id)

        # Apply filters
        if status:
            query = query.where(Post.status == PostStatus(status))

        if post_type:
            query = query.where(Post.post_type == PostType(post_type))

        if platform:
            # Use JSONB contains operator
            query = query.where(Post.target_platforms.contains([platform]))

        if search:
            search_pattern = f"%{search}%"
            query = query.where(
                or_(
                    Post.title.ilike(search_pattern),
                    Post.caption.ilike(search_pattern)
                )
            )

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Get posts with relations
        query = query.options(
            selectinload(Post.media),
            selectinload(Post.publications)
        ).order_by(Post.created_at.desc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        posts = result.scalars().all()

        return posts, total

    async def update_post(
        self,
        post_id: str,
        user: User,
        post_data: PostUpdate
    ) -> Optional[Post]:
        """
        Update a post

        Args:
            post_id: Post ID
            user: User updating the post
            post_data: Updated post data

        Returns:
            Updated post if found and belongs to user
        """
        # Get post
        post = await self.get_post(post_id, user, include_relations=False)
        if not post:
            return None

        # Update fields
        update_data = post_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if value is not None:
                # Handle enum types
                if field == "status":
                    setattr(post, field, PostStatus(value))
                elif field == "post_type":
                    setattr(post, field, PostType(value))
                else:
                    setattr(post, field, value)

        await self.db.commit()
        await self.db.refresh(post)

        return post

    async def delete_post(
        self,
        post_id: str,
        user: User
    ) -> bool:
        """
        Delete a post

        Args:
            post_id: Post ID
            user: User deleting the post

        Returns:
            True if deleted, False if not found
        """
        post = await self.get_post(post_id, user, include_relations=False)
        if not post:
            return False

        await self.db.delete(post)
        await self.db.commit()

        return True

    async def add_media(
        self,
        post_id: str,
        user: User,
        file_url: str,
        filename: str,
        file_type: str,
        **kwargs
    ) -> Optional[Media]:
        """
        Add media to a post

        Args:
            post_id: Post ID
            user: User adding media
            file_url: URL to the media file
            filename: Filename
            file_type: MIME type
            **kwargs: Additional media attributes

        Returns:
            Created media if post found
        """
        post = await self.get_post(post_id, user, include_relations=False)
        if not post:
            return None

        # Create media
        media = Media(
            post_id=post_id,
            user_id=user.id,
            filename=filename,
            file_url=file_url,
            file_type=file_type,
            **kwargs
        )

        self.db.add(media)

        # Update post media_urls
        if file_url not in post.media_urls:
            post.media_urls = post.media_urls + [file_url]

        await self.db.commit()
        await self.db.refresh(media)

        return media

    async def create_publication_record(
        self,
        post_id: str,
        platform: str,
        platform_post_id: Optional[str] = None,
        platform_url: Optional[str] = None,
        account_id: Optional[str] = None,
        account_username: Optional[str] = None,
        published: bool = True,
        error_message: Optional[str] = None
    ) -> PostPublication:
        """
        Create a publication record

        Args:
            post_id: Post ID
            platform: Platform name
            platform_post_id: ID on the platform
            platform_url: URL to the published post
            account_id: Account ID used
            account_username: Account username
            published: Whether successfully published
            error_message: Error message if failed

        Returns:
            Created publication record
        """
        publication = PostPublication(
            post_id=post_id,
            platform=platform,
            platform_post_id=platform_post_id,
            platform_url=platform_url,
            account_id=str(account_id) if account_id else None,
            account_username=account_username,
            published=published,
            published_at=datetime.utcnow().isoformat() if published else None,
            error_message=error_message
        )

        self.db.add(publication)
        await self.db.commit()
        await self.db.refresh(publication)

        return publication

    async def update_publication_insights(
        self,
        publication_id: str,
        insights: Dict
    ) -> Optional[PostPublication]:
        """
        Update publication insights

        Args:
            publication_id: Publication ID
            insights: Insights data

        Returns:
            Updated publication
        """
        result = await self.db.execute(
            select(PostPublication).where(PostPublication.id == publication_id)
        )
        publication = result.scalar_one_or_none()

        if not publication:
            return None

        publication.insights = insights
        await self.db.commit()
        await self.db.refresh(publication)

        return publication

    async def get_stats(self, user: User) -> Dict:
        """
        Get post statistics for a user

        Args:
            user: User to get stats for

        Returns:
            Dictionary with statistics
        """
        # Total posts
        total_result = await self.db.execute(
            select(func.count(Post.id)).where(Post.user_id == user.id)
        )
        total_posts = total_result.scalar()

        # Posts by status
        status_result = await self.db.execute(
            select(Post.status, func.count(Post.id))
            .where(Post.user_id == user.id)
            .group_by(Post.status)
        )
        posts_by_status = {
            status.value: count for status, count in status_result.all()
        }

        # Total publications
        pub_result = await self.db.execute(
            select(func.count(PostPublication.id))
            .join(Post)
            .where(Post.user_id == user.id)
        )
        total_publications = pub_result.scalar()

        # Publications by platform
        platform_result = await self.db.execute(
            select(PostPublication.platform, func.count(PostPublication.id))
            .join(Post)
            .where(Post.user_id == user.id)
            .where(PostPublication.published == True)
            .group_by(PostPublication.platform)
        )
        publications_by_platform = {
            platform: count for platform, count in platform_result.all()
        }

        return {
            "total_posts": total_posts,
            "posts_by_status": posts_by_status,
            "total_publications": total_publications,
            "publications_by_platform": publications_by_platform
        }
