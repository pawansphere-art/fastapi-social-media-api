"""Pydantic schemas describing request bodies and API responses."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class PostBase(BaseModel):
    """Fields a client can set on a post."""

    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    """Request body for creating or updating a post."""
    pass


class UserOut(BaseModel):
    """Public view of a user. Never includes the password hash."""

    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    """A post as returned by the API, including its owner."""

    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    """A post together with its vote count."""

    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """Request body for registering a new user."""

    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Email and password credentials."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """OAuth2 bearer token returned by `/login`."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data extracted from a verified access token."""

    id: Optional[str] = None


class Vote(BaseModel):
    """Request body for voting. `dir` = 1 adds a vote, 0 removes it."""

    post_id: int
    dir: conint(le=1)
