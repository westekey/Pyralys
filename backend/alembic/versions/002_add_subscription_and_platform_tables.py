"""Add subscription, billing, and platform-specific tables

Revision ID: 002
Revises: 001
Create Date: 2025-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Subscriptions table
    op.create_table(
        'subscriptions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('plan_type', sa.String(50), server_default='free', nullable=False),
        sa.Column('status', sa.String(50), server_default='active', nullable=False),
        sa.Column('stripe_subscription_id', sa.String(255), unique=True),
        sa.Column('stripe_customer_id', sa.String(255), unique=True),
        sa.Column('stripe_price_id', sa.String(255)),
        sa.Column('stripe_product_id', sa.String(255)),
        sa.Column('current_period_start', sa.String(50)),
        sa.Column('current_period_end', sa.String(50)),
        sa.Column('cancel_at_period_end', sa.Boolean(), server_default='false'),
        sa.Column('canceled_at', sa.String(50)),
        sa.Column('ended_at', sa.String(50)),
        sa.Column('trial_start', sa.String(50)),
        sa.Column('trial_end', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('idx_subscriptions_user', 'subscriptions', ['user_id'])
    op.create_index('idx_subscriptions_stripe_customer', 'subscriptions', ['stripe_customer_id'])

    # Invoices table
    op.create_table(
        'invoices',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('subscription_id', UUID(as_uuid=True), sa.ForeignKey('subscriptions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('stripe_invoice_id', sa.String(255), unique=True, nullable=False),
        sa.Column('stripe_payment_intent_id', sa.String(255)),
        sa.Column('amount_due', sa.Integer(), nullable=False),  # in cents
        sa.Column('amount_paid', sa.Integer(), nullable=False),  # in cents
        sa.Column('currency', sa.String(10), server_default='usd', nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('invoice_date', sa.String(50), nullable=False),
        sa.Column('paid_at', sa.String(50)),
        sa.Column('hosted_invoice_url', sa.Text()),
        sa.Column('invoice_pdf', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('idx_invoices_subscription', 'invoices', ['subscription_id'])
    op.create_index('idx_invoices_stripe', 'invoices', ['stripe_invoice_id'])

    # Payment Methods table
    op.create_table(
        'payment_methods',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('subscription_id', UUID(as_uuid=True), sa.ForeignKey('subscriptions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('stripe_payment_method_id', sa.String(255), unique=True, nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('is_default', sa.Boolean(), server_default='false'),
        sa.Column('card_brand', sa.String(50)),
        sa.Column('card_last4', sa.String(4)),
        sa.Column('card_exp_month', sa.Integer()),
        sa.Column('card_exp_year', sa.Integer()),
        sa.Column('billing_email', sa.String(255)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('idx_payment_methods_subscription', 'payment_methods', ['subscription_id'])

    # Usage table
    op.create_table(
        'usage',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('usage_type', sa.String(50), nullable=False),
        sa.Column('count', sa.Integer(), server_default='1', nullable=False),
        sa.Column('period_start', sa.DateTime(timezone=True), nullable=False),
        sa.Column('period_end', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('idx_usage_user', 'usage', ['user_id'])
    op.create_index('idx_usage_type', 'usage', ['usage_type'])
    op.create_index('idx_usage_period', 'usage', ['user_id', 'usage_type', 'period_start'])

    # Instagram Accounts table
    op.create_table(
        'instagram_accounts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('instagram_user_id', sa.String(255), unique=True, nullable=False),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('account_type', sa.String(50)),
        sa.Column('access_token', sa.Text(), nullable=False),
        sa.Column('token_expires_at', sa.String(50)),
        sa.Column('profile_picture_url', sa.String(500)),
        sa.Column('followers_count', sa.Integer(), server_default='0'),
        sa.Column('follows_count', sa.Integer(), server_default='0'),
        sa.Column('media_count', sa.Integer(), server_default='0'),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('last_sync', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('idx_instagram_accounts_user', 'instagram_accounts', ['user_id'])
    op.create_index('idx_instagram_accounts_instagram_id', 'instagram_accounts', ['instagram_user_id'])

    # WordPress Accounts table
    op.create_table(
        'wordpress_accounts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('site_url', sa.String(500), nullable=False),
        sa.Column('site_name', sa.String(255)),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('app_password', sa.String(500), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('last_sync', sa.String(50)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('idx_wordpress_accounts_user', 'wordpress_accounts', ['user_id'])

    # Update posts table with new columns for analytics
    op.add_column('posts', sa.Column('platform_post_id', sa.String(255)))
    op.add_column('posts', sa.Column('likes_count', sa.Integer(), server_default='0'))
    op.add_column('posts', sa.Column('comments_count', sa.Integer(), server_default='0'))
    op.add_column('posts', sa.Column('shares_count', sa.Integer(), server_default='0'))
    op.add_column('posts', sa.Column('reach', sa.Integer(), server_default='0'))
    op.add_column('posts', sa.Column('impressions', sa.Integer(), server_default='0'))
    op.add_column('posts', sa.Column('engagement_rate', sa.Float(), server_default='0.0'))
    op.add_column('posts', sa.Column('insights', JSONB(), server_default='{}'))
    op.add_column('posts', sa.Column('error_message', sa.Text()))
    op.add_column('posts', sa.Column('task_id', sa.String(255)))

    op.create_index('idx_posts_platform_id', 'posts', ['platform_post_id'])


def downgrade() -> None:
    # Drop indexes first
    op.drop_index('idx_posts_platform_id')

    # Drop new columns from posts
    op.drop_column('posts', 'task_id')
    op.drop_column('posts', 'error_message')
    op.drop_column('posts', 'insights')
    op.drop_column('posts', 'engagement_rate')
    op.drop_column('posts', 'impressions')
    op.drop_column('posts', 'reach')
    op.drop_column('posts', 'shares_count')
    op.drop_column('posts', 'comments_count')
    op.drop_column('posts', 'likes_count')
    op.drop_column('posts', 'platform_post_id')

    # Drop tables
    op.drop_index('idx_wordpress_accounts_user')
    op.drop_table('wordpress_accounts')

    op.drop_index('idx_instagram_accounts_instagram_id')
    op.drop_index('idx_instagram_accounts_user')
    op.drop_table('instagram_accounts')

    op.drop_index('idx_usage_period')
    op.drop_index('idx_usage_type')
    op.drop_index('idx_usage_user')
    op.drop_table('usage')

    op.drop_index('idx_payment_methods_subscription')
    op.drop_table('payment_methods')

    op.drop_index('idx_invoices_stripe')
    op.drop_index('idx_invoices_subscription')
    op.drop_table('invoices')

    op.drop_index('idx_subscriptions_stripe_customer')
    op.drop_index('idx_subscriptions_user')
    op.drop_table('subscriptions')
