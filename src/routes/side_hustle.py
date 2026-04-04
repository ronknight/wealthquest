from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..models import database, schemas

from ..utils import auth

router = APIRouter(
    prefix="/api/v1/side-hustle",
    tags=["side-hustle"],
)

@router.post("/payments", response_model=schemas.Payment, status_code=201)
def create_payment(payment: schemas.PaymentCreate, current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    db_payment = database.Transaction(
        amount=payment.amount,
        date=payment.date,
        source=payment.source,
        category=payment.category,
        tax_flag=payment.tax_flag
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/payments", response_model=List[schemas.Payment])
def read_payments(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: database.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    query = db.query(database.Transaction)
    if start_date:
        query = query.filter(database.Transaction.date >= start_date)
    if end_date:
        query = query.filter(database.Transaction.date <= end_date)
    return query.order_by(database.Transaction.date.desc()).offset(offset).limit(limit).all()

@router.put("/payments/{id}", response_model=schemas.Payment)
def update_payment(id: int, payment: schemas.PaymentCreate, current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    db_payment = db.query(database.Transaction).filter(database.Transaction.id == id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    db_payment.amount = payment.amount
    db_payment.date = payment.date
    db_payment.source = payment.source
    db_payment.category = payment.category
    db_payment.tax_flag = payment.tax_flag
    
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.delete("/payments/{id}", status_code=204)
def delete_payment(id: int, current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    db_payment = db.query(database.Transaction).filter(database.Transaction.id == id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    db.delete(db_payment)
    db.commit()
    return None

@router.get("/net-cash")
def read_net_cash(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    # Calculate separate totals
    main_total = db.query(func.sum(database.Transaction.amount)).filter(database.Transaction.category == "main").scalar() or 0.0
    side_total = db.query(func.sum(database.Transaction.amount)).filter(database.Transaction.category == "side").scalar() or 0.0
    
    # Standard net cash (non-taxable side hustle)
    net_side = db.query(func.sum(database.Transaction.amount)).filter(
        database.Transaction.category == "side",
        database.Transaction.tax_flag == 0
    ).scalar() or 0.0
    
    return {
        "main_income": main_total,
        "side_hustle": side_total,
        "net_side_hustle": net_side,
        "total_liquidity": main_total + net_side
    }

@router.get("/stats/monthly-trends")
def get_monthly_trends(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    # Returns last 6 months of income
    # SQLite specific date formatting
    results = db.query(
        func.strftime("%Y-%m", database.Transaction.date).label("month"),
        func.sum(database.Transaction.amount).label("total")
    ).group_by("month").order_by("month").limit(6).all()
    
    return [{"month": r.month, "total": r.total} for r in results]
