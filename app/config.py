"""Application settings loaded from environment variables or a `.env` file."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Typed configuration for the API.

    Each field maps to an environment variable of the same name
    (case-insensitive), e.g. ``database_hostname`` <- ``DATABASE_HOSTNAME``.
    Pydantic validates the values at startup, so a missing setting fails
    immediately instead of causing an error later.
    """

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
