from app.core import hash_password, verify_password
from tests.factories import TEST_PASSWORD, UserFactory

REGISTER_URL = "/api/auth/register"

PAYLOAD = {
    "email": "oleg@test.com",
    "password": TEST_PASSWORD,
    "first_name": "Oleg",
    "last_name": "Yaroshevich",
    "address": "Legnica 48, Wroclaw",
}


async def test_register_creates_user(client):
    response = await client.post(REGISTER_URL, json=PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "oleg@test.com"
    assert body["first_name"] == "Oleg"


async def test_duplicate_email_returns_409(client, persist):
    await persist(UserFactory(email="oleg@test.com"))

    response = await client.post(REGISTER_URL, json=PAYLOAD)

    assert response.status_code == 409


async def password_hash_check():
    password_hash = hash_password(TEST_PASSWORD)
    password = verify_password(password_hash)

    assert password == TEST_PASSWORD
