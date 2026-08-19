from fastapi import APIRouter, HTTPException, status

from app.api.deps import DbSession
from app.dto.user import UserPasswordDTO
from app.schemas.user import UserCreateSchema, UserReadSchema
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_register(db: DbSession, user: UserCreateSchema) -> UserReadSchema:
    """Register a new user in the database."""
    user = await UserService.register_user(db, UserPasswordDTO.model_validate(user))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )
    return user
