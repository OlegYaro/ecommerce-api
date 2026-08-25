import asyncio

from app.db.session import AsyncSessionLocal
from app.services.order_confirm import confirm_order
from app.worker import celery_app, db_state


async def _confirm(order_id: int) -> None:
    """Creates a database session and calls the confirm_order service."""
    session_factory = db_state.SessionLocal or AsyncSessionLocal

    async with session_factory() as db:
        await confirm_order(db, order_id)


@celery_app.task(
    name="orders.confirm",
    autoretry_for=(Exception,),
    max_retries=3,
    retry_backoff=True,
)
def confirm_order_task(order_id: int) -> None:
    """Celery task that runs the _confirm async function in a synchronous context."""
    if db_state.loop:
        db_state.loop.run_until_complete(_confirm(order_id))
    else:
        asyncio.run(_confirm(order_id))
