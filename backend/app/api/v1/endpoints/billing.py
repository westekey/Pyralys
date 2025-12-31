"""
Billing and subscription endpoints
"""
from fastapi import APIRouter, HTTPException, status, Request

router = APIRouter()


@router.post("/create-checkout")
async def create_checkout_session(plan: str):
    """
    Create Stripe checkout session for subscription

    - **plan**: Subscription plan (pro, business)
    """
    # TODO: Implement Stripe checkout
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Checkout creation not yet implemented"
    )


@router.get("/subscription")
async def get_subscription():
    """
    Get current subscription details
    """
    # TODO: Implement get subscription
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get subscription not yet implemented"
    )


@router.post("/cancel-subscription")
async def cancel_subscription():
    """
    Cancel current subscription
    """
    # TODO: Implement subscription cancellation
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Subscription cancellation not yet implemented"
    )


@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    """
    Handle Stripe webhooks
    """
    # TODO: Implement webhook handling
    # 1. Verify webhook signature
    # 2. Handle different event types
    # 3. Update subscription status

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Stripe webhooks not yet implemented"
    )
