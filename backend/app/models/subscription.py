"""
Subscription and billing models
"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class SubscriptionStatus(str, enum.Enum):
    """Subscription status enum"""
    ACTIVE = "active"
    TRIALING = "trialing"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"
    INCOMPLETE = "incomplete"


class PlanType(str, enum.Enum):
    """Plan type enum"""
    FREE = "free"
    PREMIUM = "premium"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class Subscription(Base, TimestampMixin):
    """
    User subscription model
    Tracks Stripe subscription details
    """
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)

    # Stripe IDs
    stripe_subscription_id = Column(String(255), unique=True, nullable=True, index=True)
    stripe_customer_id = Column(String(255), unique=True, nullable=True, index=True)
    stripe_price_id = Column(String(255), nullable=True)
    stripe_product_id = Column(String(255), nullable=True)

    # Subscription details
    plan_type = Column(SQLEnum(PlanType), default=PlanType.FREE, nullable=False, index=True)
    status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False, index=True)

    # Dates
    current_period_start = Column(String(50), nullable=True)
    current_period_end = Column(String(50), nullable=True)
    trial_start = Column(String(50), nullable=True)
    trial_end = Column(String(50), nullable=True)
    canceled_at = Column(String(50), nullable=True)
    ended_at = Column(String(50), nullable=True)

    # Payment
    cancel_at_period_end = Column(Boolean, default=False)

    # Metadata
    extra_data = Column(JSONB, default=dict)

    # Relationships
    user = relationship("User", back_populates="subscription")
    invoices = relationship("Invoice", back_populates="subscription", cascade="all, delete-orphan")
    payment_methods = relationship("PaymentMethod", back_populates="subscription", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, plan={self.plan_type}, status={self.status})>"


class Invoice(Base, TimestampMixin):
    """
    Invoice model for tracking payments
    """
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=False, index=True)

    # Stripe IDs
    stripe_invoice_id = Column(String(255), unique=True, nullable=False, index=True)
    stripe_payment_intent_id = Column(String(255), nullable=True)

    # Invoice details
    amount_due = Column(Integer, nullable=False)  # Amount in cents
    amount_paid = Column(Integer, default=0)
    currency = Column(String(3), default="usd")
    status = Column(String(50), nullable=False)  # paid, open, void, uncollectible

    # Dates
    invoice_date = Column(String(50), nullable=False)
    due_date = Column(String(50), nullable=True)
    paid_at = Column(String(50), nullable=True)

    # URLs
    hosted_invoice_url = Column(Text, nullable=True)
    invoice_pdf = Column(Text, nullable=True)

    # Metadata
    extra_data = Column(JSONB, default=dict)

    # Relationships
    subscription = relationship("Subscription", back_populates="invoices")

    def __repr__(self):
        return f"<Invoice(id={self.id}, stripe_id={self.stripe_invoice_id}, amount={self.amount_due}, status={self.status})>"


class PaymentMethod(Base, TimestampMixin):
    """
    Payment method model
    """
    __tablename__ = "payment_methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=False, index=True)

    # Stripe IDs
    stripe_payment_method_id = Column(String(255), unique=True, nullable=False, index=True)

    # Payment method details
    type = Column(String(50), nullable=False)  # card, bank_account, etc.
    is_default = Column(Boolean, default=False)

    # Card details (if type is card)
    card_brand = Column(String(50), nullable=True)  # visa, mastercard, etc.
    card_last4 = Column(String(4), nullable=True)
    card_exp_month = Column(Integer, nullable=True)
    card_exp_year = Column(Integer, nullable=True)

    # Metadata
    extra_data = Column(JSONB, default=dict)

    # Relationships
    subscription = relationship("Subscription", back_populates="payment_methods")

    def __repr__(self):
        return f"<PaymentMethod(id={self.id}, type={self.type}, is_default={self.is_default})>"


class UsageRecord(Base, TimestampMixin):
    """
    Usage record for tracking metered billing (if needed)
    """
    __tablename__ = "usage_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    # Usage details
    feature = Column(String(100), nullable=False)  # caption_generation, image_generation, etc.
    quantity = Column(Integer, default=1)
    timestamp = Column(String(50), nullable=False)

    # Billing
    billed = Column(Boolean, default=False)

    # Metadata
    extra_data = Column(JSONB, default=dict)

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<UsageRecord(id={self.id}, user_id={self.user_id}, feature={self.feature}, quantity={self.quantity})>"
