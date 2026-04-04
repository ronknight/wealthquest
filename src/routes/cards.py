from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import database, schemas
from ..utils.date_utils import calculate_days_remaining

from ..utils import auth

router = APIRouter(
    prefix="/api/v1/cards",
    tags=["cards"],
)

@router.post("", response_model=schemas.Card, status_code=201)
def create_card(card: schemas.CardCreate, current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    db_card = database.Card(
        name=card.name,
        statement_date=card.statement_date,
        due_date=card.due_date,
        balance=card.balance,
        alert_threshold=card.alert_threshold
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    
    res_card = schemas.Card.from_orm(db_card)
    res_card.days_remaining = calculate_days_remaining(db_card.due_date)
    return res_card

@router.get("", response_model=List[schemas.Card])
def read_cards(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    cards = db.query(database.Card).all()
    res_cards = []
    for card in cards:
        c = schemas.Card.from_orm(card)
        c.days_remaining = calculate_days_remaining(card.due_date)
        res_cards.append(c)
    
    return sorted(res_cards, key=lambda x: x.days_remaining if x.days_remaining is not None else 0)

@router.put("/{id}/alert-threshold", response_model=schemas.Card)
def update_card_threshold(id: int, days: int = Body(..., embed=True), current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    db_card = db.query(database.Card).filter(database.Card.id == id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    db_card.alert_threshold = days
    db.commit()
    db.refresh(db_card)
    
    res_card = schemas.Card.from_orm(db_card)
    res_card.days_remaining = calculate_days_remaining(db_card.due_date)
    return res_card

@router.put("/{id}", response_model=schemas.Card)
def update_card(id: int, card: schemas.CardCreate, current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    db_card = db.query(database.Card).filter(database.Card.id == id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    db_card.name = card.name
    db_card.statement_date = card.statement_date
    db_card.due_date = card.due_date
    db_card.balance = card.balance
    db_card.alert_threshold = card.alert_threshold
    
    db.commit()
    db.refresh(db_card)
    
    res_card = schemas.Card.from_orm(db_card)
    res_card.days_remaining = calculate_days_remaining(db_card.due_date)
    return res_card

@router.delete("/{id}", status_code=204)
def delete_card(id: int, current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    db_card = db.query(database.Card).filter(database.Card.id == id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    db.delete(db_card)
    db.commit()
    return None
