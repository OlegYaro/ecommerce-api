from fastapi import APIRouter

from app.api.deps import DbSession
from app.schemas import ProductReadSchema
from app.services import get_products_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
async def list_product(
    db: DbSession, category_id: int | None = None, q: str | None = None
) -> list[ProductReadSchema]:
    """Return all products by category in the shop."""
    return await get_products_service(db, category_id, q)
