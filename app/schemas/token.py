from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Tokens as returned after login."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class RefreshTokenSchema(BaseModel):
    """Request body for the refresh endpoint."""

    refresh_token: str
