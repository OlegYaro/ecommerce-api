import bcrypt


def hash_password(password: str) -> str:
    """Password to hash."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """Hash to password."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())
