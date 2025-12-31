"""
Quota Management Service
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.usage import Usage, UsageType, QUOTA_LIMITS


class QuotaService:
    """Service for managing user quotas and usage tracking"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_quota(
        self,
        user: User,
        usage_type: UsageType
    ) -> bool:
        """
        Check if user has remaining quota for the usage type

        Args:
            user: User object
            usage_type: Type of usage to check

        Returns:
            True if user has quota available, False otherwise
        """
        # Get quota limit for user's plan
        plan_limits = QUOTA_LIMITS.get(user.plan_type, QUOTA_LIMITS["free"])
        limit = plan_limits.get(usage_type, 0)

        # If limit is -1 (unlimited), always allow
        if limit == -1:
            return True

        # If limit is 0, deny
        if limit == 0:
            return False

        # Get current usage for this period
        current_usage = await self._get_current_usage(user.id, usage_type)

        # Check if usage is below limit
        return current_usage < limit

    async def increment_usage(
        self,
        user: User,
        usage_type: UsageType
    ) -> None:
        """
        Increment usage count for the user

        Args:
            user: User object
            usage_type: Type of usage to increment
        """
        # Get or create usage record for current period
        usage_record = await self._get_or_create_usage_record(user.id, usage_type)

        # Increment count
        usage_record.count += 1
        usage_record.updated_at = datetime.utcnow()

        await self.db.commit()

    async def get_remaining_quota(
        self,
        user: User,
        usage_type: UsageType
    ) -> dict:
        """
        Get remaining quota information for a user

        Args:
            user: User object
            usage_type: Type of usage

        Returns:
            Dictionary with quota information
        """
        # Get quota limit for user's plan
        plan_limits = QUOTA_LIMITS.get(user.plan_type, QUOTA_LIMITS["free"])
        limit = plan_limits.get(usage_type, 0)

        # Get current usage
        current_usage = await self._get_current_usage(user.id, usage_type)

        # Calculate remaining
        if limit == -1:
            remaining = -1  # Unlimited
        else:
            remaining = max(0, limit - current_usage)

        # Get period end date
        usage_record = await self._get_usage_record(user.id, usage_type)
        period_end = usage_record.period_end if usage_record else self._get_period_end()

        return {
            "usage_type": usage_type.value,
            "plan": user.plan_type,
            "limit": limit,
            "used": current_usage,
            "remaining": remaining,
            "period_end": period_end.isoformat(),
            "unlimited": limit == -1
        }

    async def get_all_quotas(self, user: User) -> dict:
        """
        Get all quota information for a user

        Args:
            user: User object

        Returns:
            Dictionary with all quota information
        """
        quotas = {}

        for usage_type in UsageType:
            quotas[usage_type.value] = await self.get_remaining_quota(user, usage_type)

        return {
            "user_id": str(user.id),
            "plan": user.plan_type,
            "quotas": quotas
        }

    async def _get_current_usage(
        self,
        user_id: str,
        usage_type: UsageType
    ) -> int:
        """Get current usage count for the period"""
        usage_record = await self._get_usage_record(user_id, usage_type)

        if not usage_record:
            return 0

        # Check if period has expired
        if datetime.utcnow() > usage_record.period_end:
            # Reset usage for new period
            await self._reset_usage(usage_record)
            return 0

        return usage_record.count

    async def _get_usage_record(
        self,
        user_id: str,
        usage_type: UsageType
    ) -> Optional[Usage]:
        """Get usage record for user and type"""
        result = await self.db.execute(
            select(Usage)
            .where(Usage.user_id == user_id)
            .where(Usage.usage_type == usage_type)
        )
        return result.scalar_one_or_none()

    async def _get_or_create_usage_record(
        self,
        user_id: str,
        usage_type: UsageType
    ) -> Usage:
        """Get or create usage record for current period"""
        usage_record = await self._get_usage_record(user_id, usage_type)

        if not usage_record:
            # Create new usage record
            period_start = datetime.utcnow()
            period_end = self._get_period_end(period_start)

            usage_record = Usage(
                user_id=user_id,
                usage_type=usage_type,
                count=0,
                period_start=period_start,
                period_end=period_end
            )
            self.db.add(usage_record)
            await self.db.commit()
            await self.db.refresh(usage_record)

        elif datetime.utcnow() > usage_record.period_end:
            # Reset for new period
            await self._reset_usage(usage_record)

        return usage_record

    async def _reset_usage(self, usage_record: Usage) -> None:
        """Reset usage record for new period"""
        period_start = datetime.utcnow()
        period_end = self._get_period_end(period_start)

        usage_record.count = 0
        usage_record.period_start = period_start
        usage_record.period_end = period_end
        usage_record.updated_at = datetime.utcnow()

        await self.db.commit()

    def _get_period_end(self, start_date: Optional[datetime] = None) -> datetime:
        """
        Calculate period end date (monthly reset)

        Args:
            start_date: Start date for the period (default: now)

        Returns:
            End date of the period
        """
        if start_date is None:
            start_date = datetime.utcnow()

        # Calculate next month's start date
        if start_date.month == 12:
            next_month = start_date.replace(year=start_date.year + 1, month=1, day=1)
        else:
            next_month = start_date.replace(month=start_date.month + 1, day=1)

        # Period ends at the start of next month
        return next_month
