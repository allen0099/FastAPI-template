import secrets

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import config

if config.get("DEBUG", False):
    # In debug mode, we should use a fixed key, so we can test the API
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

else:
    # In production, we should use a random key, or any other secure way to generate and store the key
    SECRET_KEY: str = secrets.token_hex(32)

ALGORITHM: str = "HS256"
ACCESS_TOKEN_DAY: int = 1
OAUTH2_SCHEMA: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="user/login")


# Some validate user logic or something security related


def get_current_user(token: str = Depends(OAUTH2_SCHEMA)):
    """Get current user from token."""
    pass


def get_jwt_payload():
    """Something related to JWT."""
    pass
