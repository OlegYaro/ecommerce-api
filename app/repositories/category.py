from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CategoryOrm


async def get_categories(db: AsyncSession) -> list[CategoryOrm]:
    """Fetches all categories from the database, ordered by name."""
    statment = select(CategoryOrm).order_by(CategoryOrm.name)
    result = await db.execute(statment)

    return list(result.scalars().all())
