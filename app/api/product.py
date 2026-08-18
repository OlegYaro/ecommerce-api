from fastapi import APIRouter, HTTPException

from app.api.deps import DbSession
from app.schemas import ProductReadSchema
from app.services import get_product_service, get_products_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
async def list_product(
    db: DbSession, category_id: int | None = None, q: str | None = None
) -> list[ProductReadSchema]:
    """Return all products by category in the shop."""
    return await get_products_service(db, category_id, q)


@router.get("/{product_id}")
async def get_product(db: DbSession, product_id: int) -> ProductReadSchema | None:
    """Return product by id."""
    product = await get_product_service(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
