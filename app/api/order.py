from fastapi import APIRouter, status

from app.dto import OrderCreateDTO
from app.schemas import OrderCreateSchema, OrderReadSchema
from app.services import OrderService

from .deps import CurrentUser, DbSession

router = APIRouter(prefix="/order", tags=["order"])


@router.post(
    "/new_order",
    status_code=status.HTTP_201_CREATED,
    responses={401: {"description": "Not authenticated"}},
)
async def create_order(
    db: DbSession, data: OrderCreateSchema, user: CurrentUser
) -> OrderReadSchema:
    """Create a new order for the current user."""
    order = await OrderService.create_order(
        db, OrderCreateDTO.model_validate(data), user.id
    )
    return order
