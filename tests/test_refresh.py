from app.core import create_access_token, create_refresh_token

from .factories import UserFactory

URL = "/api/auth/refresh"


async def test_refresh_returns_new_access_token(client, persist):
    user = UserFactory(email="oleg@test.com")
    await persist(user)

    response = await client.post(
        URL, json={"refresh_token": create_refresh_token(user.email)}
    )

    assert response.status_code == 201
    assert response.json()["access_token"]


async def test_an_access_toke_not_accepted(client, persist):
    user = UserFactory(email="oleg@test.com")
    await persist(user)

    # Same signature, same subject, wrong kind.
    response = await client.post(
        URL, json={"refresh_token": create_access_token(user.email)}
    )

    assert response.status_code == 401


async def test_a_fail_refresh_token(client):
    response = await client.post(URL, json={"refresh_token": "asdasdasd"})

    assert response.status_code == 401
