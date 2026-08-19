from pydantic import BaseModel, ConfigDict


class UserPasswordDTO(BaseModel):
    """Sign-up data as it enters the service layer, password still plain."""

    email: str
    password: str
    first_name: str
    last_name: str
    address: str

    model_config = ConfigDict(from_attributes=True)


class UserPasswordHashDTO(BaseModel):
    """Sign-up data ready to be stored: password hashed."""

    email: str
    password_hash: str
    first_name: str
    last_name: str
    address: str


class UserDTO(BaseModel):
    """A stored user as the service layer hands it back — no password."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    first_name: str
    last_name: str
    address: str
