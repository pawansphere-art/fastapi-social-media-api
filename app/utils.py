"""Password hashing helpers using passlib's bcrypt backend."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    """Hash a plain-text password with bcrypt.

    bcrypt generates a random salt and stores it inside the returned hash,
    so no separate salt column is needed.

    Args:
        password: The user's plain-text password.

    Returns:
        str: The bcrypt hash to store in the database.
    """
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    """Check a plain-text password against a stored bcrypt hash.

    Args:
        plain_password: The password the user just submitted.
        hashed_password: The hash stored in `users.password`.

    Returns:
        bool: True if the password matches, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)
