from datetime import UTC, datetime, timedelta

import jwt

from app.services import InvalidCredentialsError

from .config import settings


def create_token(subject: str, token_type: str, lifetime: timedelta) -> str:
    """Return a signed token of the given type."""
    now = datetime.now(UTC)
    payload = {
        "sub": subject,
        "type": token_type,
        "exp": now + lifetime,
    }
    return jwt.encode(
        payload, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM
    )


def create_access_token(subject: str) -> str:
    """Return a signed access token."""
    lifetime = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(subject, "access", lifetime)


def create_refresh_token(subject: str) -> str:
    """Return a signed refresh token."""
    lifetime = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token(subject, "refresh", lifetime)


def decode_token(token: str, token_type: str) -> str:
    """Return the subject of a signed token if the type matches."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM],
            options={"require": ["exp", "sub", "type"]},
        )
    except jwt.InvalidTokenError:
        return None
    if payload["type"] != token_type:
        return None
    if payload["sub"] is None:
        raise InvalidCredentialsError
    return payload["sub"]
