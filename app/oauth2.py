"""JWT access tokens: creating them at login and resolving them to a user."""

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """Create a signed JWT that expires after the configured number of minutes.

    Args:
        data: Claims to embed in the token, e.g. ``{"user_id": 1}``. The dict
            is copied, so the caller's object is not changed.

    Returns:
        str: The encoded token to send back to the client.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """Decode a JWT and check its signature and expiry.

    Args:
        token: The raw bearer token from the ``Authorization`` header.
        credentials_exception: The 401 error to raise if the token is invalid.

    Returns:
        schemas.TokenData: The user id stored in the token.

    Raises:
        HTTPException: If the token is invalid, expired or has no user_id.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """FastAPI dependency that turns the bearer token into the logged-in user.

    Add ``current_user = Depends(oauth2.get_current_user)`` to an endpoint to
    make it require authentication.

    Returns:
        models.User: The user the token belongs to.

    Raises:
        HTTPException: 401 if the token is missing or invalid.
    """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
