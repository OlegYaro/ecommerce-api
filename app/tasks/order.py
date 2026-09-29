from sqlalchemy.exc import InterfaceError, OperationalError

from app.services.order_confirm import confirm_order
from app.worker import async_task, db


@async_task(
    name="orders.confirm",
    autoretry_for=(OperationalError, InterfaceError),
    max_retries=3,
    retry_backoff=True,
)
async def confirm_order_task(order_id: int) -> None:
    """Celery task to confirm an order after a delay."""
    async with db() as session:
        await confirm_order(session, order_id)
