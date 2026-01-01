"""
Stripe service for managing subscriptions and payments
"""
from typing import Dict, Optional
import stripe
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.core.config import settings
from app.models.user import User
from app.models.subscription import Subscription, SubscriptionStatus, PlanType, Invoice, PaymentMethod


# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# Plan pricing configuration
PLAN_PRICES = {
    "free": {
        "price_id": None,
        "amount": 0,
        "currency": "usd",
        "interval": "month"
    },
    "premium": {
        "price_id": "price_premium_monthly",  # Replace with actual Stripe price ID
        "amount": 1999,  # $19.99
        "currency": "usd",
        "interval": "month"
    },
    "pro": {
        "price_id": "price_pro_monthly",  # Replace with actual Stripe price ID
        "amount": 4999,  # $49.99
        "currency": "usd",
        "interval": "month"
    },
    "enterprise": {
        "price_id": "price_enterprise_monthly",  # Replace with actual Stripe price ID
        "amount": 9999,  # $99.99
        "currency": "usd",
        "interval": "month"
    }
}


class StripeService:
    """Service for Stripe operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_customer(self, user: User) -> str:
        """
        Create a Stripe customer for a user

        Args:
            user: User instance

        Returns:
            Stripe customer ID
        """
        try:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.full_name,
                metadata={
                    "user_id": str(user.id)
                }
            )
            return customer.id
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create Stripe customer: {str(e)}")

    async def get_or_create_subscription(self, user: User) -> Subscription:
        """
        Get existing subscription or create a new one (free plan)

        Args:
            user: User instance

        Returns:
            Subscription instance
        """
        # Check if subscription exists
        stmt = select(Subscription).where(Subscription.user_id == user.id)
        result = await self.db.execute(stmt)
        subscription = result.scalar_one_or_none()

        if subscription:
            return subscription

        # Create new subscription (free plan)
        subscription = Subscription(
            user_id=user.id,
            plan_type=PlanType.FREE,
            status=SubscriptionStatus.ACTIVE
        )
        self.db.add(subscription)
        await self.db.commit()
        await self.db.refresh(subscription)

        return subscription

    async def create_checkout_session(
        self,
        user: User,
        plan_type: str,
        success_url: str,
        cancel_url: str
    ) -> Dict:
        """
        Create a Stripe Checkout session for subscription

        Args:
            user: User instance
            plan_type: Plan to subscribe to (premium, pro, enterprise)
            success_url: URL to redirect on success
            cancel_url: URL to redirect on cancel

        Returns:
            Checkout session data
        """
        if plan_type not in PLAN_PRICES or plan_type == "free":
            raise ValueError(f"Invalid plan type: {plan_type}")

        plan = PLAN_PRICES[plan_type]

        # Get or create subscription record
        subscription = await self.get_or_create_subscription(user)

        # Create or get Stripe customer
        if not subscription.stripe_customer_id:
            customer_id = await self.create_customer(user)
            subscription.stripe_customer_id = customer_id
            await self.db.commit()
        else:
            customer_id = subscription.stripe_customer_id

        try:
            # Create checkout session
            session = stripe.checkout.Session.create(
                customer=customer_id,
                mode="subscription",
                payment_method_types=["card"],
                line_items=[{
                    "price": plan["price_id"],
                    "quantity": 1
                }],
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "user_id": str(user.id),
                    "plan_type": plan_type
                }
            )

            return {
                "session_id": session.id,
                "url": session.url
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create checkout session: {str(e)}")

    async def create_portal_session(
        self,
        user: User,
        return_url: str
    ) -> Dict:
        """
        Create a Stripe Customer Portal session for managing subscription

        Args:
            user: User instance
            return_url: URL to return to after portal session

        Returns:
            Portal session data
        """
        subscription = await self.get_or_create_subscription(user)

        if not subscription.stripe_customer_id:
            raise ValueError("No Stripe customer found for user")

        try:
            session = stripe.billing_portal.Session.create(
                customer=subscription.stripe_customer_id,
                return_url=return_url
            )

            return {
                "url": session.url
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create portal session: {str(e)}")

    async def handle_subscription_created(self, stripe_subscription: Dict) -> None:
        """Handle subscription.created webhook"""
        user_id = stripe_subscription.get("metadata", {}).get("user_id")
        if not user_id:
            return

        user = await self.db.get(User, user_id)
        if not user:
            return

        subscription = await self.get_or_create_subscription(user)

        # Update subscription
        subscription.stripe_subscription_id = stripe_subscription["id"]
        subscription.stripe_price_id = stripe_subscription["items"]["data"][0]["price"]["id"]
        subscription.stripe_product_id = stripe_subscription["items"]["data"][0]["price"]["product"]
        subscription.status = SubscriptionStatus(stripe_subscription["status"])
        subscription.current_period_start = datetime.fromtimestamp(
            stripe_subscription["current_period_start"]
        ).isoformat()
        subscription.current_period_end = datetime.fromtimestamp(
            stripe_subscription["current_period_end"]
        ).isoformat()
        subscription.cancel_at_period_end = stripe_subscription.get("cancel_at_period_end", False)

        # Determine plan type from price ID
        for plan, details in PLAN_PRICES.items():
            if details.get("price_id") == subscription.stripe_price_id:
                subscription.plan_type = PlanType(plan)
                user.plan_type = plan
                break

        await self.db.commit()

    async def handle_subscription_updated(self, stripe_subscription: Dict) -> None:
        """Handle subscription.updated webhook"""
        stmt = select(Subscription).where(
            Subscription.stripe_subscription_id == stripe_subscription["id"]
        )
        result = await self.db.execute(stmt)
        subscription = result.scalar_one_or_none()

        if not subscription:
            return

        # Update subscription
        subscription.status = SubscriptionStatus(stripe_subscription["status"])
        subscription.current_period_start = datetime.fromtimestamp(
            stripe_subscription["current_period_start"]
        ).isoformat()
        subscription.current_period_end = datetime.fromtimestamp(
            stripe_subscription["current_period_end"]
        ).isoformat()
        subscription.cancel_at_period_end = stripe_subscription.get("cancel_at_period_end", False)

        if stripe_subscription.get("canceled_at"):
            subscription.canceled_at = datetime.fromtimestamp(
                stripe_subscription["canceled_at"]
            ).isoformat()

        await self.db.commit()

    async def handle_subscription_deleted(self, stripe_subscription: Dict) -> None:
        """Handle subscription.deleted webhook"""
        stmt = select(Subscription).where(
            Subscription.stripe_subscription_id == stripe_subscription["id"]
        )
        result = await self.db.execute(stmt)
        subscription = result.scalar_one_or_none()

        if not subscription:
            return

        # Update subscription to canceled
        subscription.status = SubscriptionStatus.CANCELED
        subscription.ended_at = datetime.utcnow().isoformat()

        # Downgrade user to free plan
        user = await self.db.get(User, subscription.user_id)
        if user:
            user.plan_type = "free"
            subscription.plan_type = PlanType.FREE

        await self.db.commit()

    async def handle_invoice_paid(self, stripe_invoice: Dict) -> None:
        """Handle invoice.paid webhook"""
        subscription_id = stripe_invoice.get("subscription")
        if not subscription_id:
            return

        stmt = select(Subscription).where(
            Subscription.stripe_subscription_id == subscription_id
        )
        result = await self.db.execute(stmt)
        subscription = result.scalar_one_or_none()

        if not subscription:
            return

        # Create or update invoice record
        invoice = Invoice(
            subscription_id=subscription.id,
            stripe_invoice_id=stripe_invoice["id"],
            stripe_payment_intent_id=stripe_invoice.get("payment_intent"),
            amount_due=stripe_invoice["amount_due"],
            amount_paid=stripe_invoice["amount_paid"],
            currency=stripe_invoice["currency"],
            status="paid",
            invoice_date=datetime.fromtimestamp(stripe_invoice["created"]).isoformat(),
            paid_at=datetime.fromtimestamp(stripe_invoice["status_transitions"]["paid_at"]).isoformat()
            if stripe_invoice["status_transitions"].get("paid_at") else None,
            hosted_invoice_url=stripe_invoice.get("hosted_invoice_url"),
            invoice_pdf=stripe_invoice.get("invoice_pdf")
        )

        self.db.add(invoice)
        await self.db.commit()

    async def handle_invoice_payment_failed(self, stripe_invoice: Dict) -> None:
        """Handle invoice.payment_failed webhook"""
        subscription_id = stripe_invoice.get("subscription")
        if not subscription_id:
            return

        stmt = select(Subscription).where(
            Subscription.stripe_subscription_id == subscription_id
        )
        result = await self.db.execute(stmt)
        subscription = result.scalar_one_or_none()

        if not subscription:
            return

        # Update subscription status to past_due
        subscription.status = SubscriptionStatus.PAST_DUE
        await self.db.commit()

    async def cancel_subscription(self, user: User, at_period_end: bool = True) -> Dict:
        """
        Cancel a user's subscription

        Args:
            user: User instance
            at_period_end: If True, cancel at end of billing period

        Returns:
            Cancellation result
        """
        subscription = await self.get_or_create_subscription(user)

        if not subscription.stripe_subscription_id:
            raise ValueError("No active subscription to cancel")

        try:
            if at_period_end:
                # Cancel at period end
                stripe_subscription = stripe.Subscription.modify(
                    subscription.stripe_subscription_id,
                    cancel_at_period_end=True
                )
                subscription.cancel_at_period_end = True
            else:
                # Cancel immediately
                stripe_subscription = stripe.Subscription.delete(
                    subscription.stripe_subscription_id
                )
                subscription.status = SubscriptionStatus.CANCELED
                subscription.ended_at = datetime.utcnow().isoformat()

                # Downgrade to free
                user.plan_type = "free"
                subscription.plan_type = PlanType.FREE

            await self.db.commit()

            return {
                "status": "canceled" if not at_period_end else "will_cancel",
                "ends_at": subscription.current_period_end
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to cancel subscription: {str(e)}")
