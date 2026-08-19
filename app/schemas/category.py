from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    """Base pydantic schema for category."""

    id: int
    name: str


class CategoryReadSchema(CategoryBase):
    """Pydantic schema for read data from ORM model."""

    model_config = ConfigDict(from_attributes=True)
