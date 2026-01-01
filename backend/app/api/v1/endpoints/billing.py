"""
Billing and subscription endpoints
"""
import stripe
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.subscription import Subscription, Invoice, PaymentMethod
from app.services.stripe_service import StripeService, PLAN_PRICES
from app.schemas.billing import (
    SubscriptionResponse,
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    PortalSessionResponse,
    CancelSubscriptionRequest,
    CancelSubscriptionResponse,
    InvoiceResponse,
    PaymentMethodResponse,
    PlanFeatures,
    PlansResponse
)

router = APIRouter()


@router.get("/plans", response_model=PlansResponse)
async def get_available_plans():
    """
    Get all available subscription plans with features and pricing
    """
    plans_data = []

    # Free plan
    plans_data.append(PlanFeatures(
        name="Free",
        price=0,
        currency="usd",
        interval="month",
        features=[
            "10 AI captions per month",
            "Basic analytics",
            "1 social platform",
            "Community support"
        ],
        caption_limit=10,
        image_limit=0,
        post_limit=10,
        platforms=["instagram"]
    ))

    # Premium plan
    plans_data.append(PlanFeatures(
        name="Premium",
        price=1999,
        currency="usd",
        interval="month",
        features=[
            "100 AI captions per month",
            "50 AI images per month",
            "Advanced analytics",
            "3 social platforms",
            "Email support",
            "Post scheduling"
        ],
        caption_limit=100,
        image_limit=50,
        post_limit=100,
        platforms=["instagram", "tiktok", "wordpress"]
    ))

    # Pro plan
    plans_data.append(PlanFeatures(
        name="Pro",
        price=4999,
        currency="usd",
        interval="month",
        features=[
            "Unlimited AI captions",
            "200 AI images per month",
            "Premium analytics",
            "All social platforms",
            "Priority support",
            "Post scheduling",
            "Team collaboration",
            "Custom branding"
        ],
        caption_limit=-1,  # Unlimited
        image_limit=200,
        post_limit=-1,
        platforms=["instagram", "tiktok", "wordpress", "linkedin", "facebook"]
    ))

    # Enterprise plan
    plans_data.append(PlanFeatures(
        name="Enterprise",
        price=9999,
        currency="usd",
        interval="month",
        features=[
            "Unlimited AI captions",
            "Unlimited AI images",
            "Enterprise analytics",
            "All social platforms",
            "Dedicated support",
            "Post scheduling",
            "Team collaboration",
            "Custom branding",
            "API access",
            "White-label options"
        ],
        caption_limit=-1,
        image_limit=-1,
        post_limit=-1,
        platforms=["instagram", "tiktok", "wordpress", "linkedin", "facebook"]
    ))

    return PlansResponse(plans=plans_data)


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's subscription details
    """
    stripe_service = StripeService(db)
    subscription = await stripe_service.get_or_create_subscription(current_user)

    return SubscriptionResponse(
        id=str(subscription.id),
        user_id=str(subscription.user_id),
        plan_type=subscription.plan_type.value,
        status=subscription.status.value,
        stripe_subscription_id=subscription.stripe_subscription_id,
        stripe_customer_id=subscription.stripe_customer_id,
        current_period_start=subscription.current_period_start,
        current_period_end=subscription.current_period_end,
        cancel_at_period_end=subscription.cancel_at_period_end,
        created_at=subscription.created_at,
        updated_at=subscription.updated_at
    )


@router.post("/create-checkout", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    request: CheckoutSessionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create Stripe checkout session for subscription

    - **plan_type**: Subscription plan (premium, pro, enterprise)
    """
    stripe_service = StripeService(db)

    try:
        # Frontend URLs
        success_url = f"{settings.FRONTEND_URL}/dashboard/billing?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{settings.FRONTEND_URL}/dashboard/billing?canceled=true"

        session_data = await stripe_service.create_checkout_session(
            user=current_user,
            plan_type=request.plan_type,
            success_url=success_url,
            cancel_url=cancel_url
        )

        return CheckoutSessionResponse(**session_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create checkout session: {str(e)}"
        )


@router.post("/create-portal", response_model=PortalSessionResponse)
async def create_portal_session(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create Stripe Customer Portal session for managing subscription
    """
    stripe_service = StripeService(db)

    try:
        return_url = f"{settings.FRONTEND_URL}/dashboard/billing"

        portal_data = await stripe_service.create_portal_session(
            user=current_user,
            return_url=return_url
        )

        return PortalSessionResponse(**portal_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create portal session: {str(e)}"
        )


@router.post("/cancel-subscription", response_model=CancelSubscriptionResponse)
async def cancel_subscription(
    request: CancelSubscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cancel current subscription

    - **at_period_end**: If true, cancel at end of billing period
    """
    stripe_service = StripeService(db)

    try:
        result = await stripe_service.cancel_subscription(
            user=current_user,
            at_period_end=request.at_period_end
        )

        return CancelSubscriptionResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel subscription: {str(e)}"
        )


@router.get("/invoices", response_model=List[InvoiceResponse])
async def get_invoices(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's billing invoices
    """
    # Get user's subscription
    stmt = select(Subscription).where(Subscription.user_id == current_user.id)
    result = await db.execute(stmt)
    subscription = result.scalar_one_or_none()

    if not subscription:
        return []

    # Get invoices
    stmt = select(Invoice).where(
        Invoice.subscription_id == subscription.id
    ).order_by(Invoice.invoice_date.desc())

    result = await db.execute(stmt)
    invoices = result.scalars().all()

    return [
        InvoiceResponse(
            id=str(inv.id),
            subscription_id=str(inv.subscription_id),
            stripe_invoice_id=inv.stripe_invoice_id,
            amount_due=inv.amount_due,
            amount_paid=inv.amount_paid,
            currency=inv.currency,
            status=inv.status,
            invoice_date=inv.invoice_date,
            paid_at=inv.paid_at,
            hosted_invoice_url=inv.hosted_invoice_url,
            invoice_pdf=inv.invoice_pdf,
            created_at=inv.created_at
        )
        for inv in invoices
    ]


@router.get("/payment-methods", response_model=List[PaymentMethodResponse])
async def get_payment_methods(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's payment methods
    """
    # Get user's subscription
    stmt = select(Subscription).where(Subscription.user_id == current_user.id)
    result = await db.execute(stmt)
    subscription = result.scalar_one_or_none()

    if not subscription:
        return []

    # Get payment methods
    stmt = select(PaymentMethod).where(
        PaymentMethod.subscription_id == subscription.id
    )

    result = await db.execute(stmt)
    payment_methods = result.scalars().all()

    return [
        PaymentMethodResponse(
            id=str(pm.id),
            type=pm.type,
            is_default=pm.is_default,
            card_brand=pm.card_brand,
            card_last4=pm.card_last4,
            card_exp_month=pm.card_exp_month,
            card_exp_year=pm.card_exp_year
        )
        for pm in payment_methods
    ]


@router.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle Stripe webhooks

    Processes events:
    - subscription.created
    - subscription.updated
    - subscription.deleted
    - invoice.paid
    - invoice.payment_failed
    """
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook secret not configured"
        )

    payload = await request.body()

    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload,
            stripe_signature,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payload"
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature"
        )

    stripe_service = StripeService(db)

    # Handle different event types
    try:
        if event["type"] == "customer.subscription.created":
            await stripe_service.handle_subscription_created(event["data"]["object"])
        elif event["type"] == "customer.subscription.updated":
            await stripe_service.handle_subscription_updated(event["data"]["object"])
        elif event["type"] == "customer.subscription.deleted":
            await stripe_service.handle_subscription_deleted(event["data"]["object"])
        elif event["type"] == "invoice.paid":
            await stripe_service.handle_invoice_paid(event["data"]["object"])
        elif event["type"] == "invoice.payment_failed":
            await stripe_service.handle_invoice_payment_failed(event["data"]["object"])

        return {"status": "success"}
    except Exception as e:
        print(f"Error handling webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Webhook processing failed: {str(e)}"
        )
