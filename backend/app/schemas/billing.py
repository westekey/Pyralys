"""
Billing and subscription schemas
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class SubscriptionResponse(BaseModel):
    """Subscription response schema"""
    id: str
    user_id: str
    plan_type: str
    status: str
    stripe_subscription_id: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    current_period_start: Optional[str] = None
    current_period_end: Optional[str] = None
    cancel_at_period_end: bool = False
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class CheckoutSessionRequest(BaseModel):
    """Request to create a checkout session"""
    plan_type: str  # premium, pro, enterprise


class CheckoutSessionResponse(BaseModel):
    """Checkout session response"""
    session_id: str
    url: str


class PortalSessionResponse(BaseModel):
    """Customer portal session response"""
    url: str


class CancelSubscriptionRequest(BaseModel):
    """Request to cancel subscription"""
    at_period_end: bool = True


class CancelSubscriptionResponse(BaseModel):
    """Cancel subscription response"""
    status: str
    ends_at: Optional[str] = None


class InvoiceResponse(BaseModel):
    """Invoice response schema"""
    id: str
    subscription_id: str
    stripe_invoice_id: str
    amount_due: int
    amount_paid: int
    currency: str
    status: str
    invoice_date: str
    paid_at: Optional[str] = None
    hosted_invoice_url: Optional[str] = None
    invoice_pdf: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class PaymentMethodResponse(BaseModel):
    """Payment method response schema"""
    id: str
    type: str
    is_default: bool
    card_brand: Optional[str] = None
    card_last4: Optional[str] = None
    card_exp_month: Optional[int] = None
    card_exp_year: Optional[int] = None

    class Config:
        from_attributes = True


class PlanFeatures(BaseModel):
    """Plan features schema"""
    name: str
    price: int
    currency: str
    interval: str
    features: List[str]
    caption_limit: int
    image_limit: int
    post_limit: int
    platforms: List[str]


class PlansResponse(BaseModel):
    """Response with all available plans"""
    plans: List[PlanFeatures]
