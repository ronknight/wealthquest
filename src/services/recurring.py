from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..models import database

def get_next_date(current_date_str: str, frequency: str) -> str:
    current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
    if frequency == "daily":
        next_date = current_date + timedelta(days=1)
    elif frequency == "weekly":
        next_date = current_date + timedelta(weeks=1)
    elif frequency == "monthly":
        # Simplified monthly: just add 30 days or handle month rollover
        if current_date.month == 12:
            next_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            try:
                next_date = current_date.replace(month=current_date.month + 1)
            except ValueError:
                # Handle month end cases like Jan 31 -> Feb 28
                next_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    else:
        next_date = current_date + timedelta(days=1)
    return next_date.strftime("%Y-%m-%d")

def process_recurring_transactions(db: Session):
    today = datetime.now().strftime("%Y-%m-%d")
    patterns = db.query(database.RecurringPattern).filter(
        database.RecurringPattern.is_active == 1,
        database.RecurringPattern.next_run_date <= today
    ).all()
    
    for pattern in patterns:
        # 1. Create the transaction
        transaction = database.Transaction(
            amount=pattern.amount,
            date=pattern.next_run_date,
            source=f"[Recurring] {pattern.source}",
            category=pattern.category,
            tax_flag=pattern.tax_flag,
            notes=pattern.notes
        )
        db.add(transaction)
        
        # 2. Update the pattern's next run date
        pattern.next_run_date = get_next_date(pattern.next_run_date, pattern.frequency)
        
    db.commit()
