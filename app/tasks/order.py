import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.services.order_confirm import confirm_order
from app.worker import celery_app


async def _confirm(order_id: int) -> None:
    """Creates a database session and calls the confirm_order service."""
    engine = create_async_engine(str(settings.DB_URL))
    try:
        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        async with session_factory() as db:
            await confirm_order(db, order_id)
    finally:
        await engine.dispose()


@celery_app.task(
    name="orders.confirm",
    autoretry_for=(Exception,),
    max_retries=3,
    retry_backoff=True,
)
def confirm_order_task(order_id: int) -> None:
    """Celery task that runs the _confirm async function in a synchronous context."""
    asyncio.run(_confirm(order_id))
