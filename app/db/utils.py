from urllib.parse import urljoin
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from pydantic import BaseModel

from app.db.models import User
from app.db.schemas import UserBase
from app.dependencies import FASTAPI_PORT, FASTAPI_URL

# Set up password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes a plain text password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_full_image_url(image_path: str) -> str:
    base_url = f"{FASTAPI_URL}:{FASTAPI_PORT}/"
    return urljoin(base_url, image_path)