from fastapi import APIRouter

from app.schemas import UserReadSchema

from .deps import CurrentUser

router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    "/profile",
    responses={401: {"description": "Not authenticated"}},
)
async def read_current_user(user: CurrentUser) -> UserReadSchema:
    """Return the account the request is authenticated as."""
    return user
