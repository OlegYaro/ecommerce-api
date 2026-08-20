from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import DbSession
from app.core import create_access_token, create_refresh_token, decode_token
from app.dto.user import UserPasswordDTO
from app.schemas import (
    RefreshTokenSchema,
    TokenSchema,
    UserCreateSchema,
    UserReadSchema,
)
from app.services import EmailExistsError, InvalidCredentialsError, UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_register(db: DbSession, user: UserCreateSchema) -> UserReadSchema:
    """Register a new user in the database."""
    try:
        user = await UserService.register_user(db, UserPasswordDTO.model_validate(user))
    except EmailExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        ) from e
    return user


@router.post("/login", status_code=status.HTTP_200_OK)
@router.post("/login")
async def login(
    db: DbSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """Authenticate a user and return access and refresh tokens."""
    try:
        user = await UserService.authenticate_user(
            db, form_data.username, form_data.password
        )
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        ) from e

    access_token = create_access_token(subject=user.email)
    refresh_token = create_refresh_token(subject=user.email)

    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", status_code=status.HTTP_201_CREATED)
async def refresh(db: DbSession, token: RefreshTokenSchema) -> TokenSchema:
    """Refresh the access token using a valid refresh token."""
    email = decode_token(token.refresh_token, "refresh")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserService.get_user(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenSchema(access_token=create_access_token(user.email))
