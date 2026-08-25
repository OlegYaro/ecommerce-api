from sqlalchemy.ext.asyncio import AsyncSession

from app.dto import OrderCreateDTO, OrderDTO, OrderItemDTO
from app.repositories import create_order, get_orders_by_user_id, get_products_by_ids
from app.tasks.order import confirm_order_task


class OrderService:
    """Service class for order-related operations."""

    @staticmethod
    async def create_order(
        db: AsyncSession, order: OrderCreateDTO, user_id: int
    ) -> OrderDTO:
        """The function performs all the business logic for adding an order.

        We receive a list of orders and all their data, as well as a list of products.
        First, we extract their prices from the product table and write them to the list
        for the order item table. Then, we calculate the final price and call
        the repository, passing all the data for both the orders table and
        the order_items table.
        """
        product_ids = [item.product_id for item in order.items]
        products = await get_products_by_ids(db, product_ids)

        price_of_product = dict()
        for i in products:
            price_of_product[i.id] = i.price

        items = []
        total_amount = 0
        for item in order.items:
            price = price_of_product.get(item.product_id)
            items.append(
                OrderItemDTO(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_purchase=price,
                )
            )
            total_amount += price * item.quantity

        full_order = await create_order(
            db,
            user_id=user_id,
            total_amount=total_amount,
            payment_method=order.payment_method,
            delivery_method=order.delivery_method,
            billing_information=order.billing_information,
            items=items,
        )

        await db.commit()

        confirm_order_task.delay(full_order.id)

        return OrderDTO.model_validate(full_order)

    @staticmethod
    async def get_orders_of_user(db: AsyncSession, user_id: int) -> list[OrderDTO]:
        """Return the orders of the current user."""
        orders = await get_orders_by_user_id(db, user_id)

        return [OrderDTO.model_validate(order) for order in orders]
