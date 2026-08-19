from decimal import Decimal

import factory

from app.core import hash_password
from app.models.category import Category
from app.models.product import Product
from app.models.user import User

TEST_PASSWORD = "lksjsdjfls"
TEST_PASSWORD_HASH = hash_password(TEST_PASSWORD)


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    description = factory.Faker("sentence", nb_words=6)
    price = factory.LazyFunction(lambda: Decimal("9.99"))


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    password_hash = TEST_PASSWORD_HASH
    first_name = "Oleg"
    last_name = "Yaroshevich"
    address = factory.Faker("address")
