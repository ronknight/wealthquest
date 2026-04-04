from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import database, schemas
from ..utils import auth

router = APIRouter(
    prefix="/api/v1/recurring",
    tags=["recurring"],
)

@router.post("", response_model=schemas.Recurring, status_code=201)
def create_recurring(pattern: schemas.RecurringCreate, current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    db_pattern = database.RecurringPattern(**pattern.model_dump())
    db.add(db_pattern)
    db.commit()
    db.refresh(db_pattern)
    return db_pattern

@router.get("", response_model=List[schemas.Recurring])
def list_recurring(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return db.query(database.RecurringPattern).all()

@router.put("/{id}", response_model=schemas.Recurring)
def update_recurring(id: int, pattern: schemas.RecurringCreate, current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    db_pattern = db.query(database.RecurringPattern).filter(database.RecurringPattern.id == id).first()
    if not db_pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")
    
    for key, value in pattern.model_dump().items():
        setattr(db_pattern, key, value)
    
    db.commit()
    db.refresh(db_pattern)
    return db_pattern

@router.delete("/{id}", status_code=204)
def delete_recurring(id: int, current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    db_pattern = db.query(database.RecurringPattern).filter(database.RecurringPattern.id == id).first()
    if not db_pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")
    
    db.delete(db_pattern)
    db.commit()
    return None
