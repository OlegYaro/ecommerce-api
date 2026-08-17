from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import get_products

from .factories import CategoryFactory, ProductFactory

PRODUCTS_URL = "/api/products"


async def test_search_matches_name(client, persist):
    await persist(
        ProductFactory(name="Ceramic mug"),
        ProductFactory(name="Notebook"),
    )

    response = await client.get(PRODUCTS_URL, params={"q": "mug"})

    assert response.status_code == 200
    assert [p["name"] for p in response.json()] == ["Ceramic mug"]


async def test_search_matches_description(client, persist):
    await persist(
        ProductFactory(name="Ceramic mug", description="Fine porcelain"),
        ProductFactory(name="Notebook", description="Recycled paper"),
    )

    response = await client.get(PRODUCTS_URL, params={"q": "porcelain"})

    assert [p["name"] for p in response.json()] == ["Ceramic mug"]


async def test_search_combines_with_category_filter(client, persist):
    mugs, books = CategoryFactory(name="Mugs"), CategoryFactory(name="Books")
    await persist(mugs, books)
    await persist(
        ProductFactory(name="Ceramic mug", categories=[mugs]),
        ProductFactory(name="Mug lovers handbook", categories=[books]),
    )
    response = await client.get(
        PRODUCTS_URL, params={"q": "mug", "category_id": mugs.id}
    )
    assert [p["name"] for p in response.json()] == ["Ceramic mug"]


async def test_repository_search_filters_by_name(db_session: AsyncSession, persist):
    await persist(
        ProductFactory(name="Ceramic mug", price=Decimal("12.50")),
        ProductFactory(name="Notebook", price=Decimal("3.00")),
    )

    products = await get_products(db_session, q="mug")

    assert [p.name for p in products] == ["Ceramic mug"]
