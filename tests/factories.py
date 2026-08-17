from decimal import Decimal

import factory

from app.models.category import Category
from app.models.product import Product


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
