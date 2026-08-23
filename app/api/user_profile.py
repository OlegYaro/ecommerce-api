from fastapi import APIRouter

from app.schemas import OrderReadSchema, UserReadSchema
from app.services import OrderService

from .deps import CurrentUser, DbSession

router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    "/profile",
    responses={401: {"description": "Not authenticated"}},
)
async def read_current_user(user: CurrentUser) -> UserReadSchema:
    """Return the account the request is authenticated as."""
    return user


@router.get("/orders")
async def get_orders(db: DbSession, user: CurrentUser) -> list[OrderReadSchema]:
    """Return the orders of the current user."""
    orders = await OrderService.get_orders_of_user(db, user.id)

    return orders
