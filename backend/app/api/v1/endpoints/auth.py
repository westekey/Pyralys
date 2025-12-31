"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, Token, UserResponse
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.security import decode_token
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user

    - **email**: User email (unique)
    - **password**: User password (min 8 characters)
    - **full_name**: User full name

    Returns access token, refresh token, and user data
    """
    auth_service = AuthService(db)

    # Create user
    user = await auth_service.create_user(user_data)

    # Generate tokens
    tokens = auth_service.create_tokens(user)

    # Return tokens + user data
    return {
        **tokens,
        "user": UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            plan_type=user.plan_type,
            created_at=user.created_at
        )
    }


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password

    Returns JWT access and refresh tokens

    **OAuth2 compatible endpoint - use username field for email**
    """
    auth_service = AuthService(db)

    # Authenticate user (OAuth2 uses 'username' field for email)
    user = await auth_service.authenticate_user(
        email=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate tokens
    tokens = auth_service.create_tokens(user)

    # Return tokens + user data
    return {
        **tokens,
        "user": UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            plan_type=user.plan_type,
            created_at=user.created_at
        )
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token

    - **refresh_token**: Valid JWT refresh token

    Returns new access and refresh tokens
    """
    # Decode refresh token
    payload = decode_token(refresh_token)

    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Get user
    auth_service = AuthService(db)
    user = await auth_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Generate new tokens
    tokens = auth_service.create_tokens(user)

    return {
        **tokens,
        "user": UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            plan_type=user.plan_type,
            created_at=user.created_at
        )
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information

    Requires valid JWT token in Authorization header
    """
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        plan_type=current_user.plan_type,
        created_at=current_user.created_at
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    full_name: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user information

    - **full_name**: New full name (optional)
    """
    auth_service = AuthService(db)

    update_data = {}
    if full_name:
        update_data["full_name"] = full_name

    if not update_data:
        return UserResponse(
            id=str(current_user.id),
            email=current_user.email,
            full_name=current_user.full_name,
            plan_type=current_user.plan_type,
            created_at=current_user.created_at
        )

    updated_user = await auth_service.update_user(
        user_id=current_user.id,
        update_data=update_data
    )

    return UserResponse(
        id=str(updated_user.id),
        email=updated_user.email,
        full_name=updated_user.full_name,
        plan_type=updated_user.plan_type,
        created_at=updated_user.created_at
    )


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Change user password

    - **current_password**: Current password for verification
    - **new_password**: New password (min 8 characters)
    """
    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )

    auth_service = AuthService(db)

    await auth_service.change_password(
        user_id=current_user.id,
        current_password=current_password,
        new_password=new_password
    )

    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
async def forgot_password(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Request password reset

    Sends password reset email if user exists
    Returns same message regardless to prevent email enumeration
    """
    auth_service = AuthService(db)

    user = await auth_service.get_user_by_email(email)

    if user:
        # TODO: Implement email sending with reset token
        # For now, just return success message
        pass

    # Always return same message (security best practice)
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Reset password using reset token

    - **token**: Password reset token from email
    - **new_password**: New password (min 8 characters)
    """
    # TODO: Implement password reset with token validation
    # 1. Validate reset token
    # 2. Check token expiration
    # 3. Update password
    # 4. Invalidate token

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Password reset not yet fully implemented - requires email service"
    )
