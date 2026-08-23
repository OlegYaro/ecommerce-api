import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.order import confirm_pending_order


async def confirm_order(db: AsyncSession, order_id: int) -> None:
    """Service function that call repo for change status."""
    await asyncio.sleep(5)  # Simulate a delay for demonstration purpose
    await confirm_pending_order(db, order_id)
    await db.commit()
