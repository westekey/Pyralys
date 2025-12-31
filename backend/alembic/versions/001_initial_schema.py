"""Initial schema - Users, Posts, Social Accounts

Revision ID: 001
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('plan_type', sa.String(50), server_default='free', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Social Accounts table
    op.create_table(
        'social_accounts',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('platform', sa.String(50), nullable=False),
        sa.Column('platform_user_id', sa.String(255)),
        sa.Column('access_token', sa.Text()),
        sa.Column('refresh_token', sa.Text()),
        sa.Column('token_expires_at', sa.DateTime(timezone=True)),
        sa.Column('account_username', sa.String(255)),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Posts table
    op.create_table(
        'posts',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(500)),
        sa.Column('caption', sa.Text(), nullable=False),
        sa.Column('media_urls', JSONB(), server_default='[]'),
        sa.Column('platform', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), server_default='draft', nullable=False),
        sa.Column('scheduled_at', sa.DateTime(timezone=True)),
        sa.Column('published_at', sa.DateTime(timezone=True)),
        sa.Column('ai_generated', sa.Boolean(), server_default='false'),
        sa.Column('generation_params', JSONB()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Create indexes
    op.create_index('idx_posts_user_status', 'posts', ['user_id', 'status'])
    op.create_index('idx_posts_scheduled', 'posts', ['scheduled_at'])
    op.create_index('idx_social_accounts_user', 'social_accounts', ['user_id'])


def downgrade() -> None:
    op.drop_index('idx_posts_user_status')
    op.drop_index('idx_posts_scheduled')
    op.drop_index('idx_social_accounts_user')

    op.drop_table('posts')
    op.drop_table('social_accounts')
    op.drop_table('users')
