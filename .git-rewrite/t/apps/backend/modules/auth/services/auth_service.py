"""Auth service - Business logic for authentication."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt

from modules.auth.models.user import User, UserRole
from modules.auth.schemas.login import LoginRequest, TokenResponse
from modules.auth.schemas.user import UserCreate, UserResponse
from core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service."""

    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(
        user_id: int, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token."""
        if expires_delta is None:
            expires_delta = timedelta(hours=24)

        expire = datetime.utcnow() + expires_delta
        payload = {"sub": str(user_id), "exp": expire}

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token

    async def register(self, user_data: UserCreate) -> UserResponse:
        """Register new user."""
        # Check if user already exists
        stmt = select(User).where(User.email == user_data.email)
        result = await self.db.execute(stmt)
        if result.scalars().first():
            raise ValueError(f"User with email {user_data.email} already exists")

        # Create new user
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
            full_name=user_data.full_name,
            role=UserRole.CITIZEN,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return UserResponse.model_validate(user)

    async def login(self, login_data: LoginRequest) -> TokenResponse:
        """Authenticate user and return token."""
        stmt = select(User).where(User.email == login_data.email)
        result = await self.db.execute(stmt)
        user = result.scalars().first()

        if not user or not self.verify_password(
            login_data.password, user.password_hash
        ):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is inactive")

        access_token = self.create_access_token(user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=None,
            token_type="Bearer",
        )

    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        """Get user by ID."""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalars().first()

        return UserResponse.model_validate(user) if user else None
