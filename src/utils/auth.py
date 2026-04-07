import os
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..models import database, schemas

# SECURITY WARNING: Keep this secret in production!
SECRET_KEY = os.environ.get("VANGUARD_SECRET", "vanguard-secret-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

# Root Access Control
ROOT_USER = os.environ.get("VANGUARD_ROOT", "vroot")

# Bcrypt 4.0.0+ compatibility fix for passlib 1.7.4
if not hasattr(bcrypt, "__about__"):
    class About:
        __version__ = bcrypt.__version__
    bcrypt.__about__ = About()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def verify_password(plain_password, hashed_password):
    # Bcrypt has a 72-byte limit. We truncate to ensure compatibility.
    if isinstance(plain_password, str):
        plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    # Bcrypt has a 72-byte limit. We truncate to ensure compatibility.
    if isinstance(password, str):
        password = password[:72]
    return pwd_context.hash(password)

def is_root(user: database.User):
    """Internal check for elevated access."""
    return user.username == ROOT_USER

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, role=payload.get("role"))
    except JWTError:
        raise credentials_exception
    
    user = db.query(database.User).filter(database.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

def require_role(role: str):
    def role_checker(current_user: database.User = Depends(get_current_user)):
        if current_user.role != role and not is_root(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker

def require_admin(current_user: database.User = Depends(get_current_user)):
    if current_user.role != "admin" and not is_root(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized"
        )
    return current_user

def require_root(current_user: database.User = Depends(get_current_user)):
    if not is_root(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    return current_user
