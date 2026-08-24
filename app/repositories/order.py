from decimal import Decimal

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dto import OrderItemDTO
from app.models import Order, OrderItem, OrderStatus


async def create_order(
    db: AsyncSession,
    user_id: int,
    total_amount: Decimal,
    payment_method: str,
    delivery_method: str,
    billing_information: str,
    items: list[OrderItemDTO],
) -> Order:
    """Add new order to order table and order_items table in database."""
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        payment_method=payment_method,
        delivery_method=delivery_method,
        billing_information=billing_information,
        items=[OrderItem(**item.model_dump()) for item in items],
    )

    db.add(order)
    await db.flush()
    return order


async def confirm_pending_order(db: AsyncSession, order_id: int) -> bool:
    """Change status of order."""
    stmt = (
        update(Order)
        .where(Order.id == order_id, Order.status == OrderStatus.pending)
        .values(status=OrderStatus.approved)
    )
    result = await db.execute(stmt)
    return result


async def get_orders_by_user_id(
    db: AsyncSession,
    user_id: int,
):
    """Fetches orders from the database for a specific user."""
    stmt = (
        select(Order).where(Order.user_id == user_id).options(selectinload(Order.items))
    )
    result = await db.execute(stmt)

    return list(result.scalars().all())
