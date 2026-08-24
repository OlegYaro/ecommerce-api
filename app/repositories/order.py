from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.dto import OrderItemDTO
from app.models import Order, OrderItem


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
