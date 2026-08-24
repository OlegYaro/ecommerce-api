from app.core.security import create_access_token
from tests.factories import UserFactory

URL = "/api/user/profile"


async def test_profile_returns_the_current_user(client, persist):
    user = UserFactory(email="oleg@test.com")
    await persist(user)
    token = create_access_token(user.email)

    response = await client.get(URL, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["email"] == user.email
