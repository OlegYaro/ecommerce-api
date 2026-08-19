from sqlalchemy.ext.asyncio import AsyncSession

from app.core import hash_password
from app.dto import UserDTO, UserPasswordDTO, UserPasswordHashDTO
from app.repositories import create_user, get_user_by_email

from .exceptions import EmailExistsError


class UserService:
    """Service class for user-related operations."""

    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserPasswordDTO) -> UserDTO:
        """Register a new user in the database."""
        if await get_user_by_email(db, user_data.email) is not None:
            raise EmailExistsError(user_data.email)

        password_hash = hash_password(user_data.password)

        user = await create_user(
            db,
            UserPasswordHashDTO(
                email=user_data.email,
                password_hash=password_hash,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                address=user_data.address,
            ),
        )
        await db.commit()
        return UserDTO.model_validate(user)
