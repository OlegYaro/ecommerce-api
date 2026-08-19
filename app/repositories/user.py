from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto import UserPasswordHashDTO
from app.models import User


async def create_user(db: AsyncSession, data: UserPasswordHashDTO) -> User:
    """Add new User to database."""
    user = User(
        email=data.email,
        password_hash=data.password_hash,
        first_name=data.first_name,
        last_name=data.last_name,
        address=data.address,
    )

    db.add(user)
    await db.flush()
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Check for user in database by email."""
    return await db.scalar(select(User).where(User.email == email))
