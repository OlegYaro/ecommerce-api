from sqlalchemy.ext.asyncio import AsyncSession

from app.core import hash_password, verify_password
from app.dto import UserDTO, UserPasswordDTO, UserPasswordHashDTO
from app.repositories import create_user, get_user_by_email

from .exceptions import EmailExistsError, InvalidCredentialsError


class UserService:
    """Service class for user-related operations."""

    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> UserDTO:
        """Authenticate a user by email and password.

        Return UserDTO if successful, raise InvalidCredentialsError otherwise.
        """
        email = email.lower()
        user = await get_user_by_email(db, email)
        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        return UserDTO.model_validate(user)

    @staticmethod
    async def get_user(db: AsyncSession, email: str) -> UserDTO | None:
        """Return the user with this email, or None."""
        user = await get_user_by_email(db, email)
        return UserDTO.model_validate(user) if user else None

    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserPasswordDTO) -> UserDTO:
        """Register a new user in the database."""
        email = user_data.email.lower()
        if await get_user_by_email(db, email) is not None:
            raise EmailExistsError(email)

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
