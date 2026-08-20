from .factories import TEST_PASSWORD, UserFactory

URL = "/api/auth/login"


async def test_login_returns_two_tokens(client, persist):
    user = UserFactory(email="oleg@test.com")
    await persist(user)

    response = await client.post(
        URL, data={"username": user.email, "password": TEST_PASSWORD}
    )

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["refresh_token"]


async def test_login_with_a_wrong_password(client, persist):
    user = UserFactory(email="oleg@test.com")
    await persist(user)

    response = await client.post(
        URL, data={"username": user.email, "password": "password"}
    )

    assert response.status_code == 401


async def test_login_with_an_unknown_email(client):
    response = await client.post(
        URL, data={"username": "test@test.com", "password": TEST_PASSWORD}
    )

    assert response.status_code == 401
