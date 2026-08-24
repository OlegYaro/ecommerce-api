from decimal import Decimal

from app.core.security import create_access_token
from tests.factories import ProductFactory, UserFactory

URL = "/api/order/new_order"


async def test_create_an_order(client, persist, mocker):
    mocker.patch("app.services.order.confirm_order_task.delay")
    user = UserFactory(email="oleg@test.com")
    mug = ProductFactory(price=Decimal("110"))
    mug2 = ProductFactory(price=Decimal("5.50"))
    await persist(user, mug, mug2)
    token = create_access_token(user.email)

    response = await client.post(
        URL,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "items": [
                {"product_id": mug.id, "quantity": 2},
                {"product_id": mug2.id, "quantity": 3},
            ],
            "payment_method": "card",
            "delivery_method": "courier",
            "billing_information": "string",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    assert Decimal(response.json()["total_amount"]) == Decimal("236.50")
