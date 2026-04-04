from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
from ..models import database, schemas
from ..utils import auth

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(database.User).filter(database.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.User)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Simple check if any users exist - if not, first user is admin
    user_count = db.query(database.User).count()
    role = "admin" if user_count == 0 else user_in.role
    
    existing_user = db.query(database.User).filter(database.User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = database.User(
        username=user_in.username,
        hashed_password=auth.get_password_hash(user_in.password),
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users", response_model=List[schemas.User])
def list_users(current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    """Admin only: list all users."""
    return db.query(database.User).all()

@router.post("/change-password")
def change_password(
    old_password: str, 
    new_password: str, 
    current_user: database.User = Depends(auth.get_current_user), 
    db: Session = Depends(database.get_db)
):
    """Change the current user's password."""
    if not auth.verify_password(old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    current_user.hashed_password = auth.get_password_hash(new_password)
    db.commit()
    return {"status": "success", "message": "Password updated successfully"}
