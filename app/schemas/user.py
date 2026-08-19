from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Fields the client sends and the API returns."""

    email: EmailStr
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    address: str = Field(min_length=1)


class UserCreateSchema(UserBase):
    """Sign-up payload."""

    password: str = Field(min_length=8)


class UserReadSchema(UserBase):
    """User as returned by the API — no password, no hash."""

    model_config = ConfigDict(from_attributes=True)

    id: int
